# -*- coding: utf-8 -*-
import urllib.request, gzip

url = 'http://127.0.0.1:5050/lite'
req = urllib.request.Request(url, headers={'Accept-Encoding': 'gzip'})
r = urllib.request.urlopen(req, timeout=30)
raw = r.read()
if 'gzip' in (r.headers.get('Content-Encoding') or '').lower():
    raw = gzip.decompress(raw)
t = raw.decode('utf-8', 'ignore')
print('final_url =', r.geturl())
print('bytes     =', len(raw))
for k in ['FIN-CLIP-RANGE-20261018', 'win_clipWrite', 'finClipKey', 'EQ-CLIP-RANGE-20261018', 'clip-lock']:
    print('  %-26s %d' % (k, t.count(k)))
