# -*- coding: utf-8 -*-
"""只比对最近 8 份备份，定位污染引入点。结果写入 _eq_timeline.txt"""
import os, sys, io, glob
import openpyxl

BASE = os.path.join("finance_data", "equity_report.xlsx")
BAKDIR = os.path.join("finance_data", "backups", "eq_history")
OUT = "_eq_timeline.txt"
lines = []


def load(path):
    with open(path, "rb") as fh:
        buf = io.BytesIO(fh.read())
    wb = openpyxl.load_workbook(buf, data_only=False)
    d = {}
    for ws in wb.worksheets:
        cells = {}
        for row in ws.iter_rows():
            for c in row:
                if c.value is not None:
                    cells[(c.row, c.column)] = c.value
        d[ws.title] = cells
    return d


def diff(a, b):
    out = []
    for sh in set(list(a.keys()) + list(b.keys())):
        ca, cb = a.get(sh, {}), b.get(sh, {})
        for k in set(list(ca.keys()) + list(cb.keys())):
            if ca.get(k) != cb.get(k):
                out.append((sh, k, ca.get(k), cb.get(k)))
    out.sort(key=lambda x: (x[0], x[1]))
    return out


base = load(BASE)
baks = sorted(glob.glob(os.path.join(BAKDIR, "*.bak")))[-8:]
lines.append("baseline = equity_report.xlsx (restored)")
for p in baks:
    name = os.path.basename(p).replace("_presave.xlsx.bak", "")
    try:
        d = diff(base, load(p))
    except Exception as e:
        lines.append("%-30s READ-ERR %s" % (name, e))
        continue
    lines.append("%-30s diffs=%d" % (name, len(d)))
    for x in d[:8]:
        lines.append("      %s %s  base=%r  bak=%r" % (x[0], x[1], x[2], x[3]))

with open(OUT, "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines) + "\n")
