# -*- coding: utf-8 -*-
import io, os, urllib.request
base = r'C:\vnchoicedouble'
files = ['choice_lite.html', 'index.html', 'crm_table.js', 'lost_table.js', 'vault.html']
out = []
def w(x=''): out.append(str(x))

for fn in files:
    p = os.path.join(base, fn)
    if not os.path.exists(p):
        w(fn + '  MISSING'); w(); continue
    s = io.open(p, encoding='utf-8', errors='ignore').read()
    w('== %s  len=%d ==' % (fn, len(s)))
    for kw in ['V2026.09.10.06', 'CHOICE SLATS VIET NAM', 'win_imgLightbox', 'img-lightbox-20261025',
               'target="_blank"', 'uploads', '<img', 'serviceWorker']:
        w('  %-28s : %d' % (kw, s.count(kw)))
    i = s.find('V2026.09.10.06')
    if i >= 0:
        w('  [V2026.09.10.06 ctx] ' + repr(s[max(0, i-200):i+80]))
    w()

for path in ['/lite', '/sw.js']:
    try:
        r = urllib.request.urlopen('https://choice-vn-crm.duckdns.org' + path, timeout=6)
        b = r.read().decode('utf-8', 'ignore')
        w('REMOTE %s  status=%s len=%d' % (path, r.status, len(b)))
        w('  win_imgLightbox(onclick)=%s' % ('win_imgLightbox(this.getAttribute' in b))
        w('  new ver v2026.10.25.2=%s' % ('v2026.10.25.2' in b))
        w('  target_blank_count=%d  uploads_count=%d' % (b.count('target="_blank"'), b.count('/uploads/')))
        w('  sw_selfdestruct=%s' % ('self.registration.unregister' in b))
        w()
    except Exception as e:
        w('REMOTE %s  ERR %r' % (path, e)); w()

io.open(os.path.join(base, '_probe32.txt'), 'w', encoding='utf-8').write('\n'.join(out))
print('done')
