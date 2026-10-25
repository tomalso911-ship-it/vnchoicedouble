# -*- coding: utf-8 -*-
"""只读排查：在 finance_data 下的各个报表 xlsx 里找出写着「全部的」的单元格，
以及各类合计标签（TỔNG CỘNG / Tổng cộng / TOTAL / 合计 / 总计）分布，确定要改哪些文件。"""
import io
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from openpyxl import load_workbook

ROOT = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(ROOT, "finance_data")

TARGETS = ["全部的", "总计", "TỔNG CỘNG", "Tổng cộng", "TOTAL"]

for fn in sorted(os.listdir(FD)):
    if not fn.lower().endswith(".xlsx"):
        continue
    fp = os.path.join(FD, fn)
    try:
        wb = load_workbook(fp, data_only=False, read_only=True)
    except Exception as e:
        print("!! %s -> %s" % (fn, e))
        continue
    print("=" * 88)
    print(fn)
    for ws in wb.worksheets:
        hits = []
        for row in ws.iter_rows():
            for c in row:
                v = c.value
                if isinstance(v, str) and v.strip() in TARGETS:
                    hits.append((c.coordinate, v.strip()))
        if hits:
            print("   [%s] %s" % (ws.title, ", ".join("%s=%s" % (a, b) for a, b in hits)))
    try:
        wb.close()
    except Exception:
        pass
