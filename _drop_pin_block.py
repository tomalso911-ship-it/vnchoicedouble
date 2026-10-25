# -*- coding: utf-8 -*-
"""删除 choice_lite.html 里今天新增的「浮层钉住」整块代码（UNIVER-POPUP-PIN-20261018），
回到 10-17 版的行为（不干预 Univer 浮层尺寸）。只删这一块，其它不动。"""
import io
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
PATH = 'choice_lite.html'

with io.open(PATH, 'r', encoding='utf-8', newline='') as f:
    lines = f.readlines()

# 定位：从注释分隔线（★UNIVER-POPUP-PIN 上面一行 "// ===="）到 "setInterval(tick, 120);" 后的 "})();"
hdr = None
for i, ln in enumerate(lines):
    if 'UNIVER-POPUP-PIN-20261018' in ln:
        hdr = i
        break
if hdr is None:
    print('NOT_FOUND')
    sys.exit(1)

start = hdr
while start > 0 and lines[start - 1].lstrip().startswith('//'):
    start -= 1

tick_line = None
for i in range(hdr, min(hdr + 400, len(lines))):
    if 'setInterval(tick, 120);' in lines[i]:
        tick_line = i
        break
if tick_line is None:
    print('END_NOT_FOUND')
    sys.exit(1)

end = tick_line
# 往下吃掉 "})();" 与紧随的空行
j = tick_line + 1
while j < len(lines) and lines[j].strip() in (')();', '})();', '})()', ''):
    end = j
    if lines[j].strip() in (')();', '})();'):
        break
    j += 1

print('delete lines %d..%d' % (start + 1, end + 1))
print('first:', lines[start].rstrip()[:80])
print('last :', lines[end].rstrip()[:80])
assert 'UNIVER-POPUP-PIN' in lines[hdr]
assert '})();' in lines[end]

del lines[start:end + 1]
with io.open(PATH, 'w', encoding='utf-8', newline='') as f:
    f.writelines(lines)
print('done, new line count =', len(lines))
