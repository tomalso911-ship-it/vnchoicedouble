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

用法：
  python3 check_prod_out_rule.py [path/to/agi_pm.db]
不传路径时默认检查同目录下的 agi_pm.db。
退出码：0 = 通过；1 = 发现违规；2 = 运行错误。
"""
import os
import sqlite3
import sys
import json

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def house_spec_produced(f):
    """从 f.production 聚合 猪舍×规格 的实际产量（兼容 line.qty+houses 新数据与 line.matrix 旧数据）。返 {house:{spec:qty}}。"""
    mp = {}
    production = f.get("production") or {}
    if not isinstance(production, dict):
        return mp
    for d, rec in production.items():
        if not isinstance(rec, dict):
            continue
        lines = rec.get("lines") or []
        if not isinstance(lines, list):
            continue
        for line in lines:
            if not isinstance(line, dict):
                continue
            # 新数据：line.qty[spec] + line.houses[]
            qty = line.get("qty")
            houses = line.get("houses")
            if isinstance(qty, dict) and isinstance(houses, list) and houses:
                for s, q in qty.items():
                    qv = float(q) if q else 0.0
                    for h in houses:
                        mp.setdefault(h, {})[s] = mp.get(h, {}).get(s, 0) + qv
                continue
            # 旧数据：line.matrix[house][spec]
            matrix = line.get("matrix")
            if isinstance(matrix, dict):
                for h, specs in matrix.items():
                    if not isinstance(specs, dict):
                        continue
                    for s, q in specs.items():
                        qv = float(q) if q else 0.0
                        mp.setdefault(h, {})[s] = mp.get(h, {}).get(s, 0) + qv
    return mp


def check_db(db_path):
    if not os.path.exists(db_path):
        print("✗ 找不到数据库: %s" % db_path)
        return 2
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT project_id, data FROM prod_factory").fetchall()
        conn.close()
    except Exception as e:
        print("✗ 打开/读取数据库失败: %s" % e)
        return 2

    violations = []  # (project_id, house, spec, out_qty, produced_qty)
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

        produced = house_spec_produced(f)
        ho = f.get("houseOut") or {}
        if not isinstance(ho, dict):
            continue
        for key, rec in ho.items():
            if not isinstance(rec, dict):
                continue
            out = float(rec.get("out") or 0)
            if out <= 0:
                continue
            parts = key.split("|")
            if len(parts) < 2:
                continue
            h = parts[0]
            s = "|".join(parts[1:])
            prod = (produced.get(h) or {}).get(s, 0)
            if out > prod:
                violations.append((pid, h, s, out, prod))

    print("检查目标: %s" % db_path)
    print("已扫描项目: %d 个" % projects)
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
