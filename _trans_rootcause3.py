# -*- coding: utf-8 -*-
"""列出各候选 xlsx / 备份的结构：表名、列数、是否三语并列（hits>=3）。"""
import os
import sys
import openpyxl

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

BASE = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(BASE, "finance_data")


def tri_hits(ws):
    h = 0
    for r in range(1, min(21, ws.max_row + 1)):
        for c in range(1, 9):
            a = ws.cell(r, c).value
            b = ws.cell(r, c + 10).value
            if a not in (None, "") and b not in (None, ""):
                h += 1
    return h


cands = ["vn_report.xlsx"]
for f in sorted(os.listdir(FD)):
    if f.startswith("vn_report") and f != "vn_report.xlsx":
        cands.append(f)
bd = os.path.join(FD, "backups")
if os.path.isdir(bd):
    for f in sorted(os.listdir(bd), reverse=True)[:6]:
        cands.append(os.path.join("backups", f))

for rel in cands:
    p = os.path.join(FD, rel)
    if not os.path.isfile(p):
        continue
    try:
        wb = openpyxl.load_workbook(p, read_only=True)
    except Exception as e:
        print("%-44s 打不开: %s" % (rel, e))
        continue
    tri_sheets = [ws.title for ws in wb.worksheets if tri_hits(ws) >= 3]
    print("%-42s 表数=%d 三语表=%d %s" % (rel, len(wb.worksheets), len(tri_sheets),
                                        ("✓ " + ",".join(tri_sheets[:3])) if tri_sheets else "✗ 无"))
    print("    表名: " + " | ".join(ws.title for ws in wb.worksheets))
