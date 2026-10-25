# -*- coding: utf-8 -*-
"""往返测试：equity_report.xlsx -> univer 快照 -> xlsx，检测 3 格污染是否由转换层产生。"""
import os, sys, io, json, tempfile
import openpyxl

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import univer_convert

SRC = os.path.join("finance_data", "equity_report.xlsx")
TMP = os.path.join("_roundtrip_eq.xlsx")
OUT = "_eq_roundtrip.txt"
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


snap = univer_convert.xlsx_to_univer(SRC, snap_id="equity-report")
lines.append("snapshot sheets: %s" % snap.get("sheetOrder"))

# 快照里 A1/B1/C1 是什么
for sid, sh in (snap.get("sheets") or {}).items():
    if sh.get("name") != "Tổng đầu tư":
        continue
    cd = sh.get("cellData") or {}
    for r in range(0, 4):
        row = cd.get(str(r)) or {}
        got = {}
        for c in range(0, 4):
            if str(c) in row:
                got[c] = row[str(c)].get("v")
        lines.append("  SNAP r%d(col0-3) = %s" % (r, got))
    lines.append("  mergeData = %s" % (sh.get("mergeData"),))

univer_convert.univer_to_xlsx(snap, TMP)
a, b = load(SRC), load(TMP)
diffs = []
for shn in set(list(a.keys()) + list(b.keys())):
    ca, cb = a.get(shn, {}), b.get(shn, {})
    for k in set(list(ca.keys()) + list(cb.keys())):
        if ca.get(k) != cb.get(k):
            diffs.append((shn, k, ca.get(k), cb.get(k)))
lines.append("ROUNDTRIP diffs = %d" % len(diffs))
for x in sorted(diffs)[:20]:
    lines.append("  %s %s  orig=%r  rt=%r" % x)

with open(OUT, "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines) + "\n")
print("done, diffs =", len(diffs))
