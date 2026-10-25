# -*- coding: utf-8 -*-
"""看 Chi tiết thu-chi 里 5 个账户区块的边界、期初行与余额列(F)的值，为「月末余额」算法定型。"""
import json, glob, os, sys, io, datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
path = sorted(glob.glob('finance_data/vn_report.snapshot.*.json'), key=os.path.getmtime)[-1]
snap = json.load(open(path, encoding='utf-8'))
sh = snap['sheets']['sheet_2']
cd = sh.get('cellData') or {}
print('sheet_2 rows:', len(cd))


def show(r):
    row = cd.get(str(r)) or {}
    out = []
    for c in range(0, 8):
        cell = row.get(str(c))
        if cell is None:
            continue
        v = cell.get('v'); f = cell.get('f')
        if f:
            out.append('[%d]f=%s' % (c, f))
        elif v is not None:
            if isinstance(v, float) and 20000 <= v <= 80000:
                d = datetime.date(1899, 12, 30) + datetime.timedelta(days=int(v))
                out.append('[%d]%s' % (c, d))
            else:
                out.append('[%d]%r' % (c, v))
    return '  r%-4d %s' % (r, ' | '.join(out))


for rng in [(0, 8), (70, 82), (285, 305), (560, 576)]:
    print('\n----- rows %d..%d -----' % rng)
    for r in range(rng[0], rng[1] + 1):
        print(show(r))
