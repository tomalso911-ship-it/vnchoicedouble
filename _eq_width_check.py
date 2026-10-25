# -*- coding: utf-8 -*-
"""只读体检：股东权益文件/快照里到底有没有「列宽 / 行高」。
1) finance_data/equity_report.snapshot*.json 里每张表的 columnData / rowData 条目数；
2) finance_data/equity_report.xlsx 里每张表 column_dimensions 的有效宽度。
"""
import glob
import io
import json
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

BASE = os.path.dirname(os.path.abspath(__file__))
FIN = os.path.join(BASE, 'finance_data')

print('=== snapshot cache ===')
for p in sorted(glob.glob(os.path.join(FIN, 'equity_report.snapshot.*.json'))):
    try:
        d = json.load(io.open(p, encoding='utf-8'))
    except Exception as e:
        print(os.path.basename(p), 'ERR', e)
        continue
    sheets = d.get('sheets') or {}
    print(os.path.basename(p), 'size=%dKB' % (os.path.getsize(p) // 1024), 'sheets=%d' % len(sheets))
    for sid, sh in list(sheets.items()):
        cd = sh.get('columnData') or {}
        rd = sh.get('rowData') or {}
        widths = {k: v.get('w') for k, v in cd.items() if isinstance(v, dict) and v.get('w')}
        heights = {k: v.get('h') for k, v in rd.items() if isinstance(v, dict) and v.get('h')}
        print('   ', sh.get('name'), '| colData=%d (w:%d)' % (len(cd), len(widths)),
              '| rowData=%d (h:%d)' % (len(rd), len(heights)),
              '| defaultCW=', sh.get('defaultColumnWidth'), 'defaultRH=', sh.get('defaultRowHeight'))
        if widths:
            print('      sample w:', list(widths.items())[:8])
        if heights:
            print('      sample h:', list(heights.items())[:8])

print()
print('=== xlsx column widths ===')
try:
    import openpyxl
    xp = os.path.join(FIN, 'equity_report.xlsx')
    print('xlsx:', xp, os.path.exists(xp), os.path.getsize(xp) if os.path.exists(xp) else '')
    wb = openpyxl.load_workbook(xp)
    for ws in wb.worksheets:
        dims = {k: v.width for k, v in ws.column_dimensions.items() if getattr(v, 'width', None)}
        rdims = {k: v.height for k, v in ws.row_dimensions.items() if getattr(v, 'height', None)}
        print('   ', ws.title, '| col_dims=', len(dims), list(dims.items())[:8],
              '| row_dims=', len(rdims), list(rdims.items())[:5])
except Exception as e:
    print('openpyxl ERR', e)
