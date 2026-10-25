# -*- coding: utf-8 -*-
import io, os
base = r'C:\vnchoicedouble'
files = ['choice_lite.html', 'index.html', 'crm_table.js', 'lost_table.js', 'vault.html']
out = []
def w(x=''): out.append(str(x))

for fn in files:
    p = os.path.join(base, fn)
    if not os.path.exists(p):
        w(fn + '  MISSING'); continue
    s = io.open(p, encoding='utf-8', errors='ignore').read()
    w('== %s  len=%d ==' % (fn, len(s)))
    for kw in ['V2026.09.10.06', 'CHOICE SLATS VIET NAM', 'win_imgLightbox', 'img-lightbox-20261025',
               'target="_blank"', 'uploads', '<img', 'serviceWorker']:
        w('  %-28s : %d' % (kw, s.count(kw)))
    # 所有 V2026.09.10.06 出现处 + 上下文
    idx = 0
    while True:
        i = s.find('V2026.09.10.06', idx)
        if i < 0: break
        w('  [ctx] ' + repr(s[max(0, i-220):i+60]))
        idx = i + 1
    w()

io.open(os.path.join(base, '_probe33.txt'), 'w', encoding='utf-8').write('\n'.join(out))
print('done')
