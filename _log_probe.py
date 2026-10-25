# -*- coding: utf-8 -*-
import io
import re
from collections import Counter

p = 'logs/serve_app.log'
d = io.open(p, encoding='utf-8', errors='replace').read().split('\n')
print('total lines', len(d))
print('==== tail 40 ====')
for s in d[-40:]:
    print(s.encode('ascii', 'backslashreplace').decode('ascii')[:200])
print('==== equity mentions ====')
c = Counter()
for s in d:
    if 'equity' in s or 'fx-rates' in s or 'translate' in s:
        c[re.sub(r'\d', '#', s[:60])] += 1
for k, v in c.most_common(20):
    print(v, k)
