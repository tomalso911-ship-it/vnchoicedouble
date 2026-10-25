# -*- coding: utf-8 -*-
"""输出 choice_lite.html 的 FIN-EXCEL-KEYS 补丁块 与 验证床 _univer_kb_fix.html 的完整差异。"""
import difflib
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

PATCH_HEAD = "/* =========================================================================\n   ★ Excel 键盘行为补丁"
MARK = "/* ===== FIN-EXCEL-KEYS：Excel 键盘行为补丁"
ANCHOR = "async function fin_initUniver(){"


def read_norm(p):
    return open(p, 'rb').read().decode('utf-8').replace('\r\n', '\n')


bed = read_norm('_univer_kb_fix.html')
start = bed.index(PATCH_HEAD)
end = bed.rindex('</script>')
bed_patch = bed[start:end].rstrip()

t = read_norm('choice_lite.html')
i = t.index(MARK)
j = t.index(ANCHOR)
inj = t[i:j].rstrip()
body = inj.split('===== */\n', 1)[1]
mine = "\n".join(l[4:] if l.startswith('    ') else l for l in body.split('\n')).rstrip()

d = list(difflib.unified_diff(bed_patch.split('\n'), mine.split('\n'),
                              '验证床', 'choice_lite', lineterm='', n=3))
open('_diff_keys_bed_out.txt', 'w', encoding='utf-8').write('\n'.join(d))
print('差异行数: %d' % len(d))
print('验证床补丁行数: %d ；生产补丁行数: %d' % (bed_patch.count('\n') + 1, mine.count('\n') + 1))
