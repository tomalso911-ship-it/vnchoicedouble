# -*- coding: utf-8 -*-
"""看快照里那 4 个数字格的实际值 —— 判断是否被汇率反复乘爆。"""
import json
import urllib.request


def w(s):
    print(s.encode('ascii', 'backslashreplace').decode('ascii'))


url = 'http://127.0.0.1:5050/api/finance/equity-report/snapshot'
req = urllib.request.Request(url, headers={'User-Agent': 'probe'})
data = json.loads(urllib.request.urlopen(req, timeout=30).read().decode('utf-8'))
for sid, sh in (data.get('sheets') or {}).items():
    cd = sh.get('cellData') or {}
    for rk, row in cd.items():
        for ck, cell in (row or {}).items():
            if not isinstance(cell, dict):
                continue
            v = cell.get('v')
            if isinstance(v, (int, float)) and abs(v) > 1:
                w('%-22s R%-4s C%-3s v=%s   s=%s' % (sh.get('name'), int(rk) + 1, int(ck) + 1, repr(v), repr(cell.get('s'))[:60]))
# 文件时间
import os
p = 'finance_data/equity_report.xlsx'
try:
    import datetime
    w('xlsx mtime: %s  size=%d' % (datetime.datetime.fromtimestamp(os.path.getmtime(p)), os.path.getsize(p)))
except Exception as e:
    w('xlsx: %s' % e)
