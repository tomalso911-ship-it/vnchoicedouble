import os, json
p = r'C:\vnchoicedouble\_prod_tabs.json'
out = []
if os.path.exists(p):
    try:
        d = json.load(open(p, encoding='utf-8'))
        out.append('KEYS: ' + ','.join(d.keys()))
        out.append('FINAL: ' + str(d.get('final')))
        out.append('TAB_A_len: ' + str(len(d.get('A',{}).get('text',''))))
    except Exception as e:
        out.append('JSONERR: ' + str(e))
else:
    out.append('NO FILE YET')
open(r'C:\vnchoicedouble\_chk4.txt','w',encoding='utf-8').write('\n'.join(out))
print('\n'.join(out))
