# -*- coding: utf-8 -*-
"""导出 Tổng đầu tư 表前 10 行完整网格 + 合并区域，写入 _eq_grid.txt"""
import os, io, openpyxl

SRC = os.path.join("finance_data", "equity_report.xlsx")
OUT = "_eq_grid.txt"
lines = []

wb = openpyxl.load_workbook(SRC, data_only=False)
ws = wb["Tổng đầu tư"]
lines.append("max_row=%d max_col=%d" % (ws.max_row, ws.max_column))

merged = [str(m) for m in ws.merged_cells.ranges]
lines.append("merged_cells(%d): %s" % (len(merged), merged))

lines.append("--- grid rows 1..10 ---")
for r in range(1, 11):
    parts = []
    for c in range(1, min(ws.max_column, 26) + 1):
        v = ws.cell(row=r, column=c).value
        if v is not None:
            parts.append("%s=%r" % (openpyxl.utils.get_column_letter(c), v))
    lines.append("r%-3d %s" % (r, " | ".join(parts) if parts else "(empty)"))

lines.append("--- rows with any value (>=11) ---")
for r in range(11, ws.max_row + 1):
    parts = []
    for c in range(1, min(ws.max_column, 26) + 1):
        v = ws.cell(row=r, column=c).value
        if v is not None:
            parts.append("%s=%r" % (openpyxl.utils.get_column_letter(c), v))
    if parts:
        lines.append("r%-3d %s" % (r, " | ".join(parts)))

with open(OUT, "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines) + "\n")
print("written", OUT)
