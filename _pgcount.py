import os, datetime
p = r'C:\vnchoicedouble\Choice_Slats_Ops_Manual.pdf'
out = []
if os.path.exists(p):
    out.append('EXISTS: yes')
    out.append('BYTES: %d' % os.path.getsize(p))
    out.append('MTIME: %s' % datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime('%H:%M:%S'))
    try:
        import pypdf
        r = pypdf.PdfReader(p)
        out.append('PAGES: %d' % len(r.pages))
    except Exception as e:
        out.append('PDFERR: %s' % e)
else:
    out.append('EXISTS: no')
open(r'C:\vnchoicedouble\_pgcount.txt','w',encoding='utf-8').write('\n'.join(out))
print('\n'.join(out))
