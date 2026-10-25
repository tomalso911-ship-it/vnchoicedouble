# -*- coding: utf-8 -*-
"""镜像 choice_lite.html 的 finLedger* 逻辑，找出 F 列 #VALUE! 的落点。
约定（已验证）：Univer 快照 cellData 行索引 r 为 0 基，公式文本用 A1(1 基) 记法，
即 0 基 r 对应 1 基行 r+1。"""
import json, glob, os, io, sys, re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
path = sorted(glob.glob('finance_data/vn_report.snapshot.*.json'), key=os.path.getmtime)[-1]
print('snapshot:', path)
snap = json.load(open(path, encoding='utf-8'))
cd = snap['sheets']['sheet_2']['cellData']


def cell(r, c):
    x = cd.get(str(r), {}).get(str(c))
    return x if isinstance(x, dict) else None


def is_date_serial(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and 20000 <= v <= 80000


def parse_date_text(s):
    s = s.strip()
    m = re.match(r'^(\d{1,2})[/\-](\d{1,2})[/\-](\d{4})$', s)
    return m and True or None


def cell_serial(c):
    if not c:
        return None
    v = c.get('v')
    if is_date_serial(v):
        return v
    if isinstance(v, str):
        if parse_date_text(v):
            return v
        n = None
        try:
            n = float(v)
        except Exception:
            pass
        if n is not None and is_date_serial(n):
            return n
    return None


def title_rows():
    t = []
    for rk in cd:
        r = int(rk)
        c0 = cell(r, 0)
        if c0 and cell_serial(c0) is not None:
            continue
        a = c0.get('v') if c0 else None
        if a is None or a == '':
            continue
        if isinstance(a, (int, float)) and not isinstance(a, bool):
            continue
        dv = cell(r, 3) and cell(r, 3).get('v')
        ev = cell(r, 4) and cell(r, 4).get('v')
        if dv is not None and dv != '':
            continue
        if ev is not None and ev != '':
            continue
        t.append(r)
    t.sort()
    return t


def max_row():
    m = 0
    for rk in cd:
        r = int(rk)
        if r > m:
            m = r
    return m


T = title_rows()
MX = max_row()
print('title rows (0基):', T)
print('max row (0基):', MX)

bounds = T + [MX + 1]
regs = []
for i in range(len(T)):
    lo = T[i] + 1
    hi = (bounds[i + 1] - 1) if (i + 1 < len(bounds)) else MX
    regs.append((lo, hi))
print('regions (0基 lo..hi):', regs)


def date_rows(lo, hi):
    out = []
    for r in range(lo, hi + 1):
        c0 = cell(r, 0)
        if c0 and cell_serial(c0) is not None:
            out.append(r)
    return out


def colletter(c):
    s = ''
    c += 1
    while c > 0:
        m = (c - 1) % 26
        s = chr(65 + m) + s
        c = (c - 1) // 26
    return s


BLOCKS = [(3, 4, 5), (13, 14, 15), (23, 24, 25)]
print()
print('=== 按 finLedgerBuildMap 逻辑生成的公式（0基入参 / 实际落格为 1基 r+1）===')
bad = 0
for (lo, hi) in regs:
    rows = date_rows(lo, hi)
    print('-- region %d..%d, date rows %d 个: %s' % (lo, hi, len(rows), rows[:5] + (['...'] if len(rows) > 5 else [])))
    if not rows:
        continue
    for (dc, ec, fc) in BLOCKS:
        prev = None
        for i, r in enumerate(rows):
            ref = (r - 1) if i == 0 else prev
            d = cell(r, dc) and cell(r, dc).get('v')
            e = cell(r, ec) and cell(r, ec).get('v')
            pv = cell(ref, fc) and cell(ref, fc).get('v')
            f = '=%s%d+%s%d-%s%d' % (colletter(fc), ref, colletter(dc), r, colletter(ec), r)
            # 该公式实际落在 1 基第 r+1 行
            real = '=%s%d+%s%d-%s%d' % (colletter(fc), ref + 1, colletter(dc), r + 1, colletter(ec), r + 1)
            if i < 3 or ref == r - 1:
                pcell = cell(ref, fc)
                flag = ''
                if pcell is None:
                    flag = '<空,按0算>'
                elif isinstance(pcell.get('v'), str) and pcell.get('v') != '':
                    flag = '<<<引用了文字格 %r → 真值必为 #VALUE!>>>' % pcell.get('v')
                print('   blk%d r=%d -> 写入 F%d  代码文本 %-22s 真值应为 %-22s prev.v=%r %s'
                      % (dc, r, r + 1, f, real, pv, flag))
                if '<<<' in flag:
                    bad += 1
            prev = r
print()
print('可疑(引用文字格)条数:', bad)
print()
print('=== 关键行 D/E/F 原始内容（0基 vs 1基）===')
for r in [0, 1, 3, 4, 5, 77, 78, 79, 291, 292, 293, 298, 299, 300, 301, 302, 568, 569, 570]:
    row = []
    for c in (0, 3, 4, 5):
        x = cell(r, c)
        if x is None:
            row.append('')
        elif x.get('f'):
            row.append('%s=%s' % (colletter(c), x.get('f')))
        else:
            row.append('%s=%r' % (colletter(c), x.get('v')))
    print('  0基r%-4d(1基%-4d) %s' % (r, r + 1, ' | '.join(row)))
