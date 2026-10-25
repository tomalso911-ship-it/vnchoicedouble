# -*- coding: utf-8 -*-
"""拉一份股东权益快照，找【自引用/循环引用】的公式（无限重算的典型根因）。"""
import json
import urllib.request


def w(s):
    print(s.encode('ascii', 'backslashreplace').decode('ascii'))


url = 'http://127.0.0.1:5050/api/finance/equity-report/snapshot'
data = None
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'probe'})
    data = json.loads(urllib.request.urlopen(req, timeout=30).read().decode('utf-8'))
except Exception as e:
    w('fetch failed: %s' % e)

if data:
    sheets = data.get('sheets') or {}
    w('sheets: %d' % len(sheets))
    for sid, sh in sheets.items():
        cd = sh.get('cellData') or {}
        fmls = []
        numeric = 0
        for rk, row in cd.items():
            for ck, cell in (row or {}).items():
                if not isinstance(cell, dict):
                    continue
                if cell.get('f'):
                    fmls.append((int(rk), int(ck), str(cell.get('f'))))
                elif isinstance(cell.get('v'), (int, float)):
                    numeric += 1
        w('  -- %s formulas=%d numeric=%d rows=%s cols=%s' % (
            sh.get('name'), len(fmls), numeric, sh.get('rowCount'), sh.get('columnCount')))
        for r, c, f in fmls[:50]:
            w('     R%dC%d = %s' % (r + 1, c + 1, f))
