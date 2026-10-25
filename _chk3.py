import os, json
p = r'C:\vnchoicedouble\_prod_detail.json'
out = []
if os.path.exists(p):
    try:
        d = json.load(open(p, encoding='utf-8'))
        out.append('KEYS: ' + str(list(d.keys())))
        out.append('FINAL: ' + str(d.get('final')))
        out.append('TAB_LIKE: ' + json.dumps(d.get('tab_like', []), ensure_ascii=False)[:1500])
        out.append('ONCLICKS(count): ' + str(len(d.get('all_onclicks', []))))
    except Exception as e:
        out.append('JSONERR: ' + str(e))
else:
    out.append('NO FILE')
open(r'C:\vnchoicedouble\_chk3.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('\n'.join(out))
