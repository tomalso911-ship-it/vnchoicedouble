import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
d = json.load(open('finance_data/vn_report.snapshot.53de90780c95c7e1.json', encoding='utf-8'))
cd = d['sheets']['sheet_2']['cellData']
def cell(r, c):
    x = cd.get(str(r), {}).get(str(c)); return x if isinstance(x, dict) else None
def desc(r, c):
    x = cell(r, c)
    if not x: return '.'
    if x.get('f'): return 'F[' + str(x['f'])[:24] + ']'
    v = x.get('v')
    if v is None: return '(None)'
    tag = '' if x.get('t') in (None, 2) else '#t'+str(x.get('t'))
    return str(v)[:16] + tag
titles = [4, 78, 292, 299, 569]
for t in titles:
    print('==== title row', t, '| A=', desc(t,0), '====')
    for r in range(t, t+5):
        print('   ', r, '| A=', desc(r,0), '| D=', desc(r,3), '| E=', desc(r,4), '| F=', desc(r,5))
    print()
