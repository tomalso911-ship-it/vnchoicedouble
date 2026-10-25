# -*- coding: utf-8 -*-
import os, time

KWS = ['clipboard', 'clipWrite', 'win_clipWrite', 'finClipKey', 'EQ-CLIP',
       'FIN-CLIP-PASS-LOCK', '__hsEndDrag', 'win_fmtNum']

def info(p):
    if not os.path.exists(p):
        print(p, 'NOT_FOUND'); return
    d = open(p, encoding='utf-8', errors='ignore').read()
    print('==== %s ====' % p)
    print('  bytes=%d  mtime=%s' % (len(d.encode('utf-8', 'ignore')),
                                     time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(p)))))
    for k in KWS:
        print('  %-20s %d' % (k, d.count(k)))

for p in ['choice_lite.html', 'choice_lite.min.html']:
    info(p)
