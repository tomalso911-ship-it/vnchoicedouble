# -*- coding: utf-8 -*-
import subprocess

KWS = ['clipboard', 'clipWrite', 'win_fmtNum', 'clip-lock', 'finClipKey',
       'EQ-CLIP', 'FIN-EDIT-SCOPE', 'EQ-EDIT-SCOPE', '__hsEndDrag', 'win_clipWrite',
       'FIN-CLIP-PASS-LOCK', 'execCommand']

def report(tag, text):
    print('==== %s ====' % tag)
    print('lines=%d bytes=%d' % (text.count('\n') + 1, len(text.encode('utf-8', 'ignore'))))
    for kw in KWS:
        print('  %-22s %d' % (kw, text.count(kw)))

cur = open('choice_lite.html', encoding='utf-8', errors='ignore').read()
report('WORKING choice_lite.html', cur)

try:
    out = subprocess.run(['git', 'show', 'HEAD:choice_lite.html'], capture_output=True)
    ht = out.stdout.decode('utf-8', 'ignore')
    report('HEAD:choice_lite.html', ht)
except Exception as e:
    print('HEAD read err', e)

# 也看两个备份
for p in ['choice_lite.html.bak_20261018_total', 'choice_lite.html.bak_20261018_undo2']:
    try:
        t = open(p, encoding='utf-8', errors='ignore').read()
        report('BK ' + p, t)
    except Exception as e:
        print(p, 'err', e)
