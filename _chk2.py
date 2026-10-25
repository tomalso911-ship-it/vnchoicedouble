import os, json
p = r'C:\vnchoicedouble\_prod_dump.json'
out = []
if os.path.exists(p):
    try:
        d = json.load(open(p, encoding='utf-8'))
        out.append('KEYS: ' + str(list(d.keys())))
        out.append('HAS production_list: ' + str('production_list' in d))
        out.append('HAS prod_tabs: ' + str('prod_tabs' in d))
        out.append('SIZE: ' + str(os.path.getsize(p)))
        out.append('FINAL: ' + str(d.get('final')))
    except Exception as e:
        out.append('JSONERR: ' + str(e))
else:
    out.append('NO FILE')
open(r'C:\vnchoicedouble\_chk2.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('\n'.join(out))
