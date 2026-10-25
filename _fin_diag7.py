import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
d = json.load(open('finance_data/vn_report.snapshot.53de90780c95c7e1.json', encoding='utf-8'))
cd = d['sheets']['sheet_2']['cellData']
def cell(r, c):
    x = cd.get(str(r), {}).get(str(c)); return x if isinstance(x, dict) else None
print('row | D(3).v | E(4).v | F(5).f | F(5).v')
for r in range(4, 15):
    D = cell(r,3); E = cell(r,4); F = cell(r,5)
    print(r, '|', (D or {}).get('v'), '|', (E or {}).get('v'), '|', (F or {}).get('f'), '|', (F or {}).get('v'))
