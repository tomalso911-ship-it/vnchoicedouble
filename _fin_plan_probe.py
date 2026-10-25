import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
d = json.load(open('finance_data/vn_report.snapshot.53de90780c95c7e1.json', encoding='utf-8'))
s = d['sheets']['sheet_2']
cd = s.get('cellData', {})
def v(r, c):
    cell = cd.get(str(r), {}).get(str(c))
    if not isinstance(cell, dict): return None
    return cell.get('v')
def num(x):
    try: return float(x)
    except: return None

# 所有 A 列(0) 为文本（非数字）的行 -> 标题/子标题候选
print('=== A 列为文本的所有行(标题/区块) ===')
for r in sorted(int(x) for x in cd.keys()):
    a = v(r, 0)
    if a is not None and not isinstance(a, (int, float)):
        d0, e0, f0, fT = v(r,3), v(r,4), v(r,5), v(r,5)
        print(f'@{r}: {str(a)[:40]!r} | D={d0} E={e0} F={f0}')

print('\n=== 各工作区块首数据行(核对期初) ===')
# 把 A 列文本行当成区块分隔；区块内首个 D/E 同时非空的行即首数据行
titles = [r for r in sorted(int(x) for x in cd.keys()) if (v(r,0) is not None and not isinstance(v(r,0),(int,float)) and v(r,3) is None and v(r,4) is None)]
# 跳过主标题行0
titles = [t for t in titles if t > 0]
for i, t in enumerate(titles):
    nxt = titles[i+1] if i+1 < len(titles) else 589
    r0 = t+1
    while r0 < nxt and (v(r0,3) is None or v(r0,4) is None):
        r0 += 1
    if r0 >= nxt: 
        print(f'block after @{t} {str(v(t,0))[:24]!r}: no data rows'); continue
    d0, e0, f0 = num(v(r0,3)), num(v(r0,4)), num(v(r0,5))
    de = (d0 or 0) - (e0 or 0)
    print(f'block @{t} {str(v(t,0))[:26]!r} -> firstData@{r0}: D={d0} E={e0} F={f0} | F==D-E? {f0==de if f0 is not None else "F为空"}')
