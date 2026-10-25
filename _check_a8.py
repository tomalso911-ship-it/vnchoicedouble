# -*- coding: utf-8 -*-
import os, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import openpyxl
FIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "finance_data")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_check_a8_out.txt")
L = []
def log(s=""):
    L.append(str(s)); open(OUT,"w",encoding="utf-8").write("\n".join(L)+"\n"); print(s)

for fn, tag in (("vn_report.xlsx","vn"), ("merge_report.xlsx","merge")):
    p = os.path.join(FIN, fn)
    wb = openpyxl.load_workbook(p, data_only=False)
    ws = wb["TỔNG HỢP"]
    log("=== %s / TỔNG HỢP ===" % tag)
    for r in range(5, 12):
        row = []
        for c in range(1, 6):
            cell = ws.cell(r, c)
            v = cell.value
            row.append("%s=%r" % (cell.coordinate, v))
        log("  " + " | ".join(row))
    wb.close()
log("done")
