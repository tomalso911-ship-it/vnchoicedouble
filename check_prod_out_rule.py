#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生产「出库/转移至猪舍待安装」不得超过「当前生产总量」业务规则检查。

硬规则（前端 choice_lite.html 已焊死三层：H 表输入实时夹回、blur 再夹、出库弹窗保存拦截）：
  对每个项目的每个 (猪舍, 规格) 组合：
      出库总量 = f.houseOut["猪舍|规格"].out
      当前生产总量 = 从 f.production 聚合的该 (猪舍, 规格) 实际产量
  必须满足：出库总量 <= 当前生产总量。

注意：本脚本是「数据一致性」巡检——专门抓绕过前端（旧数据、手工改库）导致落库了
出库量大于生产量的非法记录。前端已保证新建/编辑不会写入违规值。

★解析口径必须与前端 choice_lite.html 的 prod_houseSpecProduced() 严格一致（2026-10-11 修正）：
  1) production[日期].lines 是【按线号索引的 dict】（键 "1"/"2"/...），不是数组。
     旧实现写的是 `for line in lines:`（按数组遍历），对 dict 迭代会得到字符串键，
     过不了 isinstance(line, dict) 被静默跳过 → 所有产量算成 0 →
     项目 19 误报 8 条「出库 3644 > 当前生产总量 0」。这是误报，不是脏数据。
  2) 产量优先取精确明细 line.qtyDetail[规格][猪舍]；
  3) qtyDetail 未覆盖的规格再回退：有 line.matrix 用 matrix；否则用 line.qty
     按「该规格各猪舍需求量」比例拆分（需求量来自 CRM 签约项目的 concrete_floor_spec，
     复刻前端 prod_slatsMatrix()）。拆分所需需求拿不到时，该规格不做违规判定（防误报）。
  4) 形状守卫：production 里有生产线却一条产量都解析不出来时，判定为「解析口径失效」，
     直接报错退出（2），绝不静默判为通过或违规。

用法：
  python3 check_prod_out_rule.py [path/to/agi_pm.db]
不传路径时默认检查同目录下的 agi_pm.db。
退出码：0 = 通过；1 = 发现违规；2 = 运行错误（含解析口径失效）。
"""
import os
import re
import sqlite3
import sys
import json

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def _num(v):
    """等价于前端 parseFloat(String(v).replace(/[^0-9.\\-]/g,''))||0。"""
    if v is None or isinstance(v, bool):
        return 0.0
    if isinstance(v, (int, float)):
        return float(v)
    s = re.sub(r"[^0-9.\-]", "", str(v))
    try:
        return float(s) if s else 0.0
    except ValueError:
        return 0.0


def _iter_lines(rec):
    """遍历 production[日期].lines。
    ★现行数据是「按线号索引的 dict」（{"1": {...}, "2": {...}}，与前端 Object.keys(rec.lines) 一致）；
      历史/测试数据里出现过 list。两种都要支持——只认 list 会静默丢掉全部产量（误报根因）。"""
    if not isinstance(rec, dict):
        return []
    lines = rec.get("lines")
    if isinstance(lines, dict):
        return [lines[k] for k in lines]
    if isinstance(lines, list):
        return lines
    return []


def load_demand_matrix(conn, pid):
    """复刻前端 prod_slatsMatrix()：从 CRM 签约项目 won_projects.concrete_floor_spec
    算出 {规格: {猪舍: 需求量}}。只服务于『qtyDetail 未覆盖的规格按需求比例拆分』兜底分支。
    拿不到就返回 {}（此时触发兜底的规格不做违规判定，避免再次误报）。"""
    try:
        cols = [r[1] for r in conn.execute("PRAGMA table_info(won_projects)")]
        if "concrete_floor_spec" not in cols:
            return {}
        idcol = "id" if "id" in cols else ("project_id" if "project_id" in cols else None)
        if not idcol:
            return {}
        row = conn.execute(
            "SELECT concrete_floor_spec FROM won_projects WHERE CAST(%s AS TEXT)=?" % idcol,
            (str(pid),)).fetchone()
        rows = row[0] if row else None
    except Exception:
        return {}
    if isinstance(rows, str):
        try:
            rows = json.loads(rows)
        except Exception:
            return {}
    if isinstance(rows, dict):
        rows = rows.get("rows") or rows.get("specs") or []
    if not isinstance(rows, list):
        return {}

    specs = {}
    last_ph = ""
    for r in rows:
        if not isinstance(r, dict):
            continue
        L = r.get("floor_len", r.get("L")); W = r.get("floor_wid", r.get("W")); H = r.get("floor_hgt", r.get("H"))
        # 与前端一致：数量不再信任存值，按 数量/单元 × 单元/栋 × 栋数 重算
        qty = int(round(_num(r.get("qty_unit")) * _num(r.get("unit_per_building")) * _num(r.get("building_count"))))
        if not qty and r.get("qty_whole") is not None:
            q = _num(r.get("qty_whole"))
            if q:
                qty = int(q)
        ph = str(r.get("pig_house") or "").strip()
        if ph == "":
            ph = last_ph          # 合并行兜底：空猪舍行继承上一非空猪舍
        else:
            last_ph = ph
        houses = [x for x in re.split(r"[,，+/、&\s]+", ph) if x] if ph else ["—"]
        key = "%s×%s×%s" % (L if L is not None else "?", W if W is not None else "?", H if H is not None else "?")
        sp = specs.setdefault(key, {})
        for h in houses:
            sp[h] = sp.get(h, 0) + qty
    return specs


def house_spec_produced(f, demand=None):
    """从 f.production 聚合 猪舍×规格 的实际产量（口径与前端 prod_houseSpecProduced 一致）。
    返 (map, stats)：map = {猪舍: {规格: 产量}}；
    stats 记录解析到多少条生产线/多少处产量，以及哪些 (猪舍,规格) 因缺需求量无法兜底拆分（不作违规判定）。"""
    demand = demand or {}
    mp = {}
    stats = {"lines": 0, "hits": 0, "qty_seen": 0, "fallback_lines": 0, "unknown": []}
    production = f.get("production") or {}
    if not isinstance(production, dict):
        return mp, stats

    for d in production:
        rec = production[d]
        for line in _iter_lines(rec):
            if not isinstance(line, dict):
                continue
            stats["lines"] += 1

            # ① 精确明细：line.qtyDetail[规格][猪舍]（有数值才算覆盖，避免混合数据丢产量）
            done_spec = {}
            qty_detail = line.get("qtyDetail")
            if isinstance(qty_detail, dict):
                for ds, dm in qty_detail.items():
                    if not isinstance(dm, dict):
                        continue
                    dsum = 0.0
                    for dh, dq in dm.items():
                        dq = _num(dq)
                        if dq <= 0:
                            continue
                        mp.setdefault(dh, {})[ds] = mp.get(dh, {}).get(ds, 0) + dq
                        dsum += dq
                        stats["hits"] += 1
                        stats["qty_seen"] += 1
                    if dsum > 0:
                        done_spec[ds] = 1

            # ② 回退：line.qty 里 qtyDetail 未覆盖的规格
            qty = line.get("qty")
            houses = line.get("houses")
            matrix = line.get("matrix")
            rest = []
            if isinstance(qty, dict):
                for s, q in qty.items():
                    if not done_spec.get(s) and _num(q) > 0:
                        rest.append((s, _num(q)))
            if rest and isinstance(houses, list) and houses and not isinstance(matrix, dict):
                stats["fallback_lines"] += 1
                for s, q in rest:
                    stats["qty_seen"] += 1
                    elig = []
                    total_demand = 0.0
                    for h in houses:
                        dem = _num((demand.get(s) or {}).get(h, 0))
                        if dem > 0:
                            elig.append([h, dem, 0])
                            total_demand += dem
                    if not elig:
                        # 没有需求基线：无法复刻前端拆分 → 该规格不作违规判定（宁可漏报不可误报）
                        for h in houses:
                            stats["unknown"].append((h, s, d))
                        continue
                    alloc = 0
                    max_i = 0
                    for i, e in enumerate(elig):
                        e[2] = int(round(q * e[1] / total_demand)) if total_demand > 0 else 0
                        alloc += e[2]
                        if e[2] > elig[max_i][2]:
                            max_i = i
                    if alloc != q:
                        elig[max_i][2] += int(q - alloc)
                    for h, _dem, share in elig:
                        if share <= 0:
                            continue
                        mp.setdefault(h, {})[s] = mp.get(h, {}).get(s, 0) + share
                        stats["hits"] += 1
            elif isinstance(matrix, dict):
                # 旧数据：line.matrix[猪舍][规格] 已天然按猪舍拆分
                for mh, m_specs in matrix.items():
                    if not isinstance(m_specs, dict):
                        continue
                    for s, q in m_specs.items():
                        if done_spec.get(s) or _num(q) <= 0:
                            continue
                        mp.setdefault(mh, {})[s] = mp.get(mh, {}).get(s, 0) + _num(q)
                        stats["hits"] += 1
                        stats["qty_seen"] += 1
    return mp, stats


def _ro_connect(db_path):
    """只读连接。本脚本每次提交都会被 pre-commit 钩子跑一遍，绝不能对生产库
    产生任何写入/回滚/WAL 检查点副作用（普通 connect 是读写模式，会碰主库文件）。"""
    try:
        from pathlib import Path
        return sqlite3.connect(Path(os.path.abspath(db_path)).as_uri() + "?mode=ro", uri=True)
    except Exception:
        return sqlite3.connect(db_path)


def check_db(db_path):
    if not os.path.exists(db_path):
        print("✗ 找不到数据库: %s" % db_path)
        return 2
    try:
        conn = _ro_connect(db_path)
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT project_id, data FROM prod_factory").fetchall()
    except Exception as e:
        print("✗ 打开/读取数据库失败: %s" % e)
        return 2

    violations = []     # (project_id, house, spec, out_qty, produced_qty)
    shape_broken = []   # 有出库可判、但解析不出任何产量的项目（口径失效，不作判定）
    skipped = []        # (project_id, house, spec) 缺需求基线，未作判定
    projects = 0

    for r in rows:
        pid = r["project_id"]
        raw = r["data"]
        if not raw:
            continue
        try:
            f = json.loads(raw) if isinstance(raw, str) else raw
        except Exception:
            print("  ! 警告: 项目 %s 的 data 不是合法 JSON，已跳过" % pid)
            continue
        if not isinstance(f, dict):
            continue
        projects += 1

        ho = f.get("houseOut") or {}
        if not isinstance(ho, dict):
            ho = {}
        out_total = sum(_num(rec.get("out")) for rec in ho.values() if isinstance(rec, dict))

        produced, stats = house_spec_produced(f, load_demand_matrix(conn, pid))

        # ★形状守卫：有生产线、有出库，却【一处数量都认不出来】→ 解析口径失效
        #   （旧实现只认 list 形态的 lines，正是这样把产量全算成 0 并误报 8 条违规）
        #   注意：只要认出了任何数量（qty/qtyDetail/matrix），就说明形状没问题，
        #   此时某个 (猪舍,规格) 产量为 0 属于正常判定范围，不能当形状失效。
        if stats["lines"] > 0 and stats["qty_seen"] == 0 and out_total > 0:
            shape_broken.append(pid)
            print("  ! 项目 %s：production 有 %d 条生产线、有出库，却认不出任何产量 —— "
                  "数据形状可能又变了，请检查本脚本解析口径（本次不作违规判定）。" % (pid, stats["lines"]))
            continue
        if stats["lines"] == 0 and out_total > 0:
            print("  · 项目 %s：没有任何每日生产记录，但有出库 %.0f（按规则照常判定）。" % (pid, out_total))

        unknown = set((h, s) for (h, s, _d) in stats["unknown"])
        for key, rec in ho.items():
            if not isinstance(rec, dict):
                continue
            out = _num(rec.get("out"))
            if out <= 0:
                continue
            parts = key.split("|")
            if len(parts) < 2:
                continue
            h = parts[0]
            s = "|".join(parts[1:])
            if (h, s) in unknown:
                skipped.append((pid, h, s))
                continue
            prod = (produced.get(h) or {}).get(s, 0)
            if out > prod:
                violations.append((pid, h, s, out, prod))

    conn.close()

    print("检查目标: %s" % db_path)
    print("已扫描项目: %d 个" % projects)
    if skipped:
        print("  · 说明: %d 处（猪舍×规格）既无 qtyDetail 明细、又缺 concrete_floor_spec 需求量基线，"
              "无法复刻前端拆分口径，未作违规判定。示例: %s" % (len(skipped), skipped[:3]))
    if shape_broken:
        print("✗ 运行错误：项目 %s 的生产数据结构无法被本脚本解析（解析口径可能与前端不一致），"
              "未作违规判定，请先修脚本。" % ", ".join(str(x) for x in shape_broken))
        return 2
    if not violations:
        print("✓ 通过：所有「出库/转移至猪舍待安装」数量均 ≤「当前生产总量」，未发现违规。")
        return 0

    print("✗ 失败：发现 %d 处「出库量超过当前生产总量」的违规记录：" % len(violations))
    for pid, h, s, out, prod in violations:
        print("  - 项目[%s] %s | %s：出库 %s > 当前生产总量 %s" % (pid, h, s, int(out), int(prod)))
    print("请修复：出库/转移至猪舍待安装数量不能大于该猪舍×规格的当前生产总量。")
    return 1


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "agi_pm.db")
    rc = check_db(path)
    sys.exit(rc)


if __name__ == "__main__":
    main()
