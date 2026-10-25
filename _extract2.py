import io, json, re

lines = io.open('choice_lite.html', encoding='utf-8', errors='replace').read().split('\n')
out = []
for i in range(4520, 4531):
    s = lines[i - 1]
    if len(s) > 3000:
        s = s[:3000] + ' ...[len=%d]' % len(lines[i - 1])
    out.append('%d: %s' % (i, s))

# 提取 flow_ 键值
blob = '\n'.join(lines[4520:4529])
for m in re.finditer(r"flow_[a-z_]+:[^,}]+", blob):
    out.append('FLOW> ' + m.group(0))

out.append('==== _prod_tabs.json inputs ====')
try:
    d = json.load(io.open('_prod_tabs.json', encoding='utf-8'))
    for k in ['A', 'B', 'C', 'D', 'E', 'H', 'F']:
        if k not in d:
            continue
        out.append('--- TAB ' + k + ' ---')
        ins = d[k].get('inputs', [])
        if isinstance(ins, list):
            for x in ins:
                if isinstance(x, dict):
                    out.append('   in: id=%s ph=%s' % (x.get('id', ''), x.get('p', '')))
                else:
                    out.append('   in: ' + str(x))
        b = d[k].get('buttons', [])
        if isinstance(b, list):
            out.append('   btns: ' + ' | '.join([str(y) for y in b[:18]]))
except Exception as e:
    out.append('JSONERR ' + str(e))

io.open('_wl_extract2.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('OK')
