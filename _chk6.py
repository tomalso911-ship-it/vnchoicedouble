import os, json
p=r'C:\vnchoicedouble\_inst_detail.json'
out=[]
if os.path.exists(p):
    try:
        d=json.load(open(p,encoding='utf-8'))
        out.append('KEYS: '+','.join(d.keys()))
        out.append('FINAL: '+str(d.get('final')))
        out.append('CANDS: '+json.dumps(d.get('cands',[]),ensure_ascii=False)[:500])
        out.append('DETAIL_TABS: '+json.dumps(d.get('detail_tabs',[]),ensure_ascii=False)[:400])
        out.append('DETAIL_TEXT(head): '+d.get('detail_text','')[:600].replace('\n',' '))
    except Exception as e:
        out.append('ERR: '+str(e))
else:
    out.append('NO FILE YET')
open(r'C:\vnchoicedouble\_chk6.txt','w',encoding='utf-8').write('\n'.join(out))
print('ok')
