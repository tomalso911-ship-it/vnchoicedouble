# -*- coding: utf-8 -*-
"""对比工作区 choice_lite.html 与 HEAD(213a1cf) 的差异块，定位被删掉的功能区。"""
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

cur = open('choice_lite.html', 'rb').read()
head = subprocess.run(['git', 'show', '213a1cf:choice_lite.html'],
                      capture_output=True).stdout
print('当前行数: %d' % cur.count(b'\n'))
print('HEAD 行数: %d' % head.count(b'\n'))
print('当前字节: %d' % len(cur))
print('HEAD 字节: %d' % len(head))

d = subprocess.run(['git', 'diff', '--unified=0', '--', 'choice_lite.html'],
                   capture_output=True).stdout.decode('utf-8', 'replace')
lines = d.split('\n')
out = []
for i, ln in enumerate(lines):
    m = re.match(r'^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@(.*)$', ln)
    if m:
        old_len = int(m.group(2) or 1)
        if old_len >= 20:            # 只列大块删除
            # 取被删的第一行内容作为提示
            nxt = lines[i + 1] if i + 1 < len(lines) else ''
            out.append('del %5d 行 @ HEAD:%s  %s' % (old_len, m.group(1), nxt[:110]))
outf = open('_cmp_head_out.txt', 'w', encoding='utf-8')
outf.write('\n'.join(out))
outf.close()
print('大块删除（>=20 行）: %d 块' % len(out))
for x in out[:40]:
    print('  ' + x)
