import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
d = json.load(open('finance_data/vn_report.snapshot.53de90780c95c7e1.json', encoding='utf-8'))
cd = d['sheets']['sheet_2']['cellData']
def cell(r, c):
    x = cd.get(str(r), {}).get(str(c)); return x if isinstance(x, dict) else None

# 三套 D/E 列
DE = [(3,4),(13,14),(23,24)]
txt_cells = []   # (r, c, v, t)
num_cells = 0
frm_cells = 0
for (dc, ec) in DE:
    for r in range(0, 600):
        for c in (dc, ec):
            x = cell(r, c)
            if not x: continue
            if x.get('f'):
                frm_cells += 1; continue
            v = x.get('v'); t = x.get('t')
            if isinstance(v, str):
                txt_cells.append((r, c, v, t))
            elif isinstance(v, (int, float)):
                num_cells += 1
print('D/E numeric cells =', num_cells, '| formula cells =', frm_cells, '| TEXT cells =', len(txt_cells))
print('--- sample TEXT D/E cells (first 40) ---')
for (r, c, v, t) in txt_cells[:40]:
    print('  row', r, 'col', c, 't=', t, 'v=', repr(v)[:40])
