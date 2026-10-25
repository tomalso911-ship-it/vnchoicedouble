# -*- coding: utf-8 -*-
import os
import sys

import openpyxl

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

CELLS = [(20, 2), (20, 3), (21, 2), (21, 3), (25, 2), (25, 3), (26, 2), (26, 3)]

eq = os.path.join("finance_data", "equity_report.xlsx")
wb = openpyxl.load_workbook(eq, read_only=True)
ws = wb.worksheets[0]
out = []
for r, c in CELLS:
    out.append("R%dC%d=%r" % (r + 1, c + 1, ws.cell(row=r + 1, column=c + 1).value))
print("equity:", " | ".join(out))
wb.close()
print("mtime equity:", os.path.getmtime(eq))
print("mtime vn    :", os.path.getmtime(os.path.join("finance_data", "vn_report.xlsx")))
