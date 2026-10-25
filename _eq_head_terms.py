#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""读「中国投资数据」表头原文 + 取引擎现在给出的 en/vi 说法（作为锁定基准）。"""
import json
import os
import sys
import urllib.parse
import urllib.request

import openpyxl

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(ROOT, "finance_data", "equity_report.xlsx")

wb = openpyxl.load_workbook(P, data_only=False)
heads = []
for ws in wb.worksheets:
    if ws.title != "Đầu tư Trung Quốc":
        continue
    print("工作表:", ws.title, "dims:", ws.dimensions)
    for r in (1, 2, 3):
        row = []
        for c in range(1, 18):
            v = ws.cell(r, c).value
            if v not in (None, ""):
                row.append("%s%d=%r" % (ws.cell(r, c).column_letter, r, v))
        print("  第%d行: %s" % (r, " | ".join(row)))
    for c in range(1, 18):
        v = ws.cell(2, c).value
        if v not in (None, "") and isinstance(v, str):
            heads.append(v.strip())
wb.close()

print("-" * 70)
print("表头原文（去重，按出现顺序）:", json.dumps(heads, ensure_ascii=False))
print("-" * 70)


def tr(q, target):
    u = "http://127.0.0.1:5050/api/translate?q=%s&target=%s" % (urllib.parse.quote(q), target)
    try:
        with urllib.request.urlopen(u, timeout=25) as r:
            return r.read().decode("utf-8").strip()
    except Exception as e:
        return "ERR %s" % e


print("%-14s | %-26s | %s" % ("中文", "英文(en)", "越南文(vi)"))
print("-" * 70)
for h in heads:
    print("%-14s | %-26s | %s" % (h, tr(h, "en"), tr(h, "vi")))
print("-" * 70)
for h in ("现金", "转账"):
    print("%-14s | %-26s | %s" % (h, tr(h, "en"), tr(h, "vi")))
print("=" * 70)
