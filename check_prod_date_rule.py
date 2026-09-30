#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生产「操作日期 ≥ 排产开始日期」业务规则检查（lint / CI / 定时巡检均可）。

硬规则（前端 choice_lite.html 已焊死三层：日历 data-min 禁用、选择兜底、保存校验）：
  任意项目里，所有「生产操作日期」(#pop_date) 都必须 ≥ 该项目的「排产开始日期」(#pa_start_prod)。
  排产开始日期 = dmyToYmd(f.prepEnd || f.planStart)。
  生产操作日期落在 f.houseOut 下：
      - 出库：rec.outDate、rec.outDaily[<ymd>].date
      - 入库：rec.retDate
  均为 YYYY-MM-DD 存储，可直接按字典序与排产开始日期比较。

注意：本脚本是「数据一致性」巡检——专门抓那些绕过前端（旧草稿、服务端种子、手工改库）
导致落库了早于排产开始日期的非法记录。前端已保证新建/编辑不会写入违规值。

用法：
  python3 check_prod_date_rule.py [path/to/agi_pm.db]
不传路径时默认检查同目录下的 agi_pm.db。
退出码：0 = 通过（无违规）；1 = 发现违规；2 = 运行错误（库不存在/打不开等）。
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

YMD_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DMY_RE = re.compile(r"^\d{2}-\d{2}-\d{4}$")


def to_ymd(s):
    """统一成 YYYY-MM-DD；无法识别返回 None。同时兼容已规范化的 YYYY-MM-DD 与显示的 DD-MM-YYYY。"""
    if not s or not isinstance(s, str):
        return None
    s = s.strip()
    if YMD_RE.match(s):
        return s
    if DMY_RE.match(s):
        d, m, y = s.split("-")
        return "%s-%s-%s" % (y, m, d)
    return None


def collect_op_dates(rec):
    """从一条 houseOut 记录里收集所有操作日期（YYYY-MM-DD 或 None）。"""
    dates = []
    for k in ("outDate", "retDate"):
        v = to_ymd(rec.get(k)) if isinstance(rec, dict) else None
        if v:
            dates.append((k, v))
    out_daily = rec.get("outDaily") if isinstance(rec, dict) else None
    if isinstance(out_daily, dict):
        for dk, dv in out_daily.items():
            y = to_ymd(dk)
            if y:
                dates.append(("outDaily[%s]" % dk, y))
            if isinstance(dv, dict) and dv.get("date"):
                y2 = to_ymd(dv.get("date"))
                if y2:
                    dates.append(("outDaily[].date", y2))
    return dates


def check_db(db_path):
    if not os.path.exists(db_path):
        print("✗ 找不到数据库: %s" % db_path)
        return 2
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT project_id, data FROM prod_factory"
        ).fetchall()
        conn.close()
    except Exception as e:
        print("✗ 打开/读取数据库失败: %s" % e)
        return 2

    violations = []  # (project_id, op_key, op_date, start_prod)
    projects = 0
    skipped_no_start = 0

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

        start = to_ymd(f.get("prepEnd")) or to_ymd(f.get("planStart"))
        if not start:
            # 无排产开始日期（prepEnd / planStart 均缺）→ 无可比对基线，跳过且不计入违规
            skipped_no_start += 1
            continue

        house_out = f.get("houseOut")
        if not isinstance(house_out, dict):
            continue
        for key, rec in house_out.items():
            if not isinstance(rec, dict):
                continue
            for label, op_date in collect_op_dates(rec):
                if op_date < start:
                    violations.append((pid, key, label, op_date, start))

    # ---- 输出 ----
    print("检查目标: %s" % db_path)
    print("已扫描项目(含 houseOut 数据): %d 个；无可比基线(缺 prepEnd/planStart)跳过: %d 个"
          % (projects, skipped_no_start))

    if not violations:
        print("✓ 通过：所有生产操作日期(#pop_date)均 ≥ 排产开始日期(#pa_start_prod)，"
              "未发现早于排产开始日期的非法记录。")
        return 0

    print("✗ 失败：发现 %d 处「操作日期早于排产开始日期」的违规记录：" % len(violations))
    for pid, key, label, op_date, start in violations:
        print("  - 项目[%s] houseOut[%s].%s = %s  <  排产开始日期 %s"
              % (pid, key, label, op_date, start))
    print("请修复上述记录（将操作日期调整到 ≥ 排产开始日期，或在前端重新打开对应弹窗保存以触发自动夹正）。")
    return 1


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    db_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "agi_pm.db")
    rc = check_db(db_path)
    sys.exit(rc)


if __name__ == "__main__":
    main()
