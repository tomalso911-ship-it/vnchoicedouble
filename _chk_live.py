# -*- coding: utf-8 -*-
import urllib.request, gzip

url = 'http://127.0.0.1:5050/lite'
req = urllib.request.Request(url, headers={'Accept-Encoding': 'gzip'})
r = urllib.request.urlopen(req, timeout=30)
raw = r.read()
enc = (r.headers.get('Content-Encoding') or '').lower()
if 'gzip' in enc:
    raw = gzip.decompress(raw)
txt = raw.decode('utf-8', 'ignore')
print('final_url =', r.geturl())
print('bytes     =', len(raw))
for k in ['win_clipWrite', 'finClipKey', '__hsEndDrag', 'win_fmtNum', 'clip-lock', 'EQ-CLIP-EDITSAFE']:
    print('  %-20s %d' % (k, txt.count(k)))
