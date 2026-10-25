import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
d = json.load(open('finance_data/vn_report.snapshot.53de90780c95c7e1.json', encoding='utf-8'))
cd = d['sheets']['sheet_2']['cellData']
def cell(r, c):
    x = cd.get(str(r), {}).get(str(c)); return x if isinstance(x, dict) else None
def desc(r, c):
    x = cell(r, c)
    if not x: return '.'
    if x.get('f'): return 'F[' + str(x['f'])[:26] + ']'
    v = x.get('v')
    if v is None: return '(v=None)'
    tag = '' if x.get('t') in (None, 2) else '#t'+str(x.get('t'))
    return str(v)[:16] + tag
# 收支明细 A 列日期判定：打印前 45 行
print('row | A(0) | D(3) | E(4) | F(5)')
for r in range(0, 46):
    print(r, '|', desc(r,0), '|', desc(r,3), '|', desc(r,4), '|', desc(r,5))
