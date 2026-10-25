# -*- coding: utf-8 -*-
"""看 /api/finance/convert-currency 返回的 values 是否包含汇总表金额格（会覆盖本期重算值）。"""
import sys, json, urllib.request

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

req = urllib.request.Request(
    'http://127.0.0.1:5050/api/finance/convert-currency',
    data=json.dumps({'target': 'VND'}).encode(),
    headers={'Content-Type': 'application/json'})
j = json.loads(urllib.request.urlopen(req, timeout=120).read().decode())
v = j.get('values', {})
print('keys of response:', list(j.keys()))
print('sheets in values:', list(v.keys()))
for name in v:
    if 'SUM' in name.upper() or 'ỔNG' in name.upper() or 'TỔNG' in name.upper():
        s = v[name]
        rows = sorted(s.keys(), key=lambda x: int(x))
        print('---', name, 'rows:', rows)
        for r in rows[:30]:
            print('   r%-4s %s' % (r, s[r]))
fmt = j.get('fmt', {})
for name in fmt:
    if 'SUM' in name.upper() or 'TỔNG' in name.upper():
        print('--- fmt', name, fmt[name][:30])
