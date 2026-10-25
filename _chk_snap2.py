# -*- coding: utf-8 -*-
import sys, json, glob, os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=max(glob.glob('finance_data/vn_report.snapshot.*.json'), key=os.path.getmtime)
snap=json.load(open(p,encoding='utf-8'))
sid=snap['sheetOrder'][1]
s=snap['sheets'][sid]
print('sheet', sid, 'keys =', list(s.keys()))
for k,v in s.items():
    if isinstance(v,(dict,list)):
        print('  %s: %s len=%d  sample=%s' % (k, type(v).__name__, len(v), str(v)[:220]))
    else:
        print('  %s = %r' % (k, v))
# 看 TỔNG HỢP 的一个公式格 & 合并信息
s1=snap['sheets'][snap['sheetOrder'][0]]
print('\nTỔNG HỢP keys:', list(s1.keys()))
print('mergeData sample:', str(s1.get('mergeData'))[:300])
print('columnData sample:', str(s1.get('columnData'))[:300])
