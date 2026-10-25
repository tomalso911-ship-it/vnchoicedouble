# -*- coding: utf-8 -*-
"""扫描权益表历史备份，找出「探针写入之前」的最近一份干净版本。"""
import glob
import os
import sys

import openpyxl

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

BASE = r"C:\vnchoicedouble\finance_data"
CELLS = [(3, 3), (6, 6), (9, 3)]


def dump(path):
    wb = openpyxl.load_workbook(path, read_only=True)
    out = []
    for ws in wb.worksheets[:2]:
        vals = []
        for (r, c) in CELLS:
            try:
                vals.append("%s!%s%d=%r" % (ws.title, "ABCDEFGHIJ"[c], r + 1, ws.cell(row=r + 1, column=c + 1).value))
            except Exception as e:
                vals.append("err:" + str(e))
        out.append(" | ".join(vals))
    wb.close()
    return " || ".join(out)


def main():
    files = sorted(glob.glob(os.path.join(BASE, "backups", "eq_history", "*.bak")))
    files = files[-14:]
    for f in files:
        try:
            print(os.path.basename(f), "->", dump(f), flush=True)
        except Exception as e:
            print(os.path.basename(f), "READ-FAIL", e, flush=True)
    print("--- current ---", flush=True)
    print("equity_report.xlsx ->", dump(os.path.join(BASE, "equity_report.xlsx")), flush=True)


if __name__ == "__main__":
    main()
