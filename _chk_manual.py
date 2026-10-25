import re, os
html = open(r'C:\vnchoicedouble\training_manual.html', encoding='utf-8').read()
imgs = re.findall(r'src="([^"]+)"', html)
shots = [s for s in imgs if 'training_shots' in s or s.endswith('.png')]
out = []
out.append('HTML bytes: %d' % len(html.encode('utf-8')))
out.append('total img refs: %d' % len(imgs))
out.append('screenshot refs: %d' % len(shots))
missing = []
for s in shots:
    p = os.path.join(r'C:\vnchoicedouble', s) if not s.startswith('http') else None
    if p and not os.path.exists(p):
        missing.append(s)
out.append('MISSING: %s' % (missing if missing else 'none'))
out.append('--- snippet img list ---')
for s in shots[:40]:
    out.append(s)
open(r'C:\vnchoicedouble\_chk_manual_out.txt','w',encoding='utf-8').write('\n'.join(out))
print('\n'.join(out))
