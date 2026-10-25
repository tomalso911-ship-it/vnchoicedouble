import os, json
p=r'C:\vnchoicedouble\_inst_detail.json'
out=[]
if os.path.exists(p):
    try:
        d=json.load(open(p,encoding='utf-8'))
        out.append('KEYS: '+','.join(d.keys()))
        out.append('FINAL: '+str(d.get('final')))
        out.append('PROJ: '+json.dumps(d.get('proj',[]),ensure_ascii=False)[:400])
        out.append('SUBTABS: '+json.dumps(d.get('subtabs',[]),ensure_ascii=False)[:600])
    except Exception as e:
        out.append('ERR: '+str(e))
else:
    out.append('NO FILE YET')
open(r'C:\vnchoicedouble\_chk5.txt','w',encoding='utf-8').write('\n'.join(out))
print('\n'.join(out))
