import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
d = json.load(open('finance_data/vn_report.snapshot.53de90780c95c7e1.json', encoding='utf-8'))
cd = d['sheets']['sheet_2']['cellData']
def cell(r, c):
    x = cd.get(str(r), {}).get(str(c)); return x if isinstance(x, dict) else None

# 1) D/E 里的公式格（27个）具体是什么
print('=== D/E formula cells ===')
for (dc, ec) in [(3,4),(13,14),(23,24)]:
    for r in range(0, 600):
        for c in (dc, ec):
            x = cell(r, c)
            if x and x.get('f'):
                print('  row', r, 'col', c, 'f=', x['f'], 'v=', x.get('v'), 't=', x.get('t'))

# 2) F 列公式里，引用"上一行"的：检查被引用的 F 格本身是否是公式/文本
print()
print('=== check F chain: any F cell whose formula refs a cell that is TEXT ===')
# 简化：找出所有 A 列为日期、F 有公式的行，打印公式
cnt=0
for r in range(0, 600):
    a = cell(r,0); f = cell(r,5)
    if f and f.get('f') and isinstance(f.get('f'),str) and f['f'].startswith('=F'):
        cnt+=1
print('F cells with =F.. rolling formula:', cnt)
