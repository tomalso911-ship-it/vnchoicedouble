# -*- coding: utf-8 -*-
"""列出工作区 choice_lite.html 相对 HEAD(213a1cf) 的【新增】块（用于判断是否有人手工加了新功能）。"""
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

d = subprocess.run(['git', 'diff', '--unified=0', '--', 'choice_lite.html'],
                   capture_output=True).stdout.decode('utf-8', 'replace')
lines = d.split('\n')
out = []
for i, ln in enumerate(lines):
    m = re.match(r'^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@(.*)$', ln)
    if not m:
        continue
    new_len = int(m.group(4) or 1)
    if new_len >= 5:
        body = []
        j = i + 1
        while j < len(lines) and lines[j].startswith('+') and len(body) < 4:
            body.append(lines[j][1:].strip()[:100])
            j += 1
        out.append('add %4d 行 @ 现在:%s | %s' % (new_len, m.group(3), ' // '.join(body)))
open('_cmp_add_out.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('新增块（>=5 行）: %d 块' % len(out))
for x in out[:60]:
    print('  ' + x)
