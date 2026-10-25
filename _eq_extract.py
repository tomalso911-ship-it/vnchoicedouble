# -*- coding: utf-8 -*-
"""抽出真正的股东权益模块（含 equity_container 的 <script type="module">）到 _eq_block.txt"""
import io
import re

src = io.open('choice_lite.html', encoding='utf-8').read()
found = False
for mm in re.finditer(r'^\s*<script type="module">\s*$', src, re.M):
    s = mm.start()
    e = src.find('</script>', s)
    if 'equity_container' in src[s:e]:
        block = src[s:e]
        io.open('_eq_block.txt', 'w', encoding='utf-8').write(block)
        print('start_line=%d end_line=%d chars=%d' % (
            src.count('\n', 0, s) + 1, src.count('\n', 0, e) + 1, len(block)))
        found = True
        break
if not found:
    print('not found')
