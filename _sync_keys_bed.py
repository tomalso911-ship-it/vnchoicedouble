# -*- coding: utf-8 -*-
"""把 choice_lite.html 里 FIN-EXCEL-KEYS 补丁块的【当前正文】同步回验证床 _univer_kb_fix.html。

背景：2026-10-16 的 FIN-EXCEL-SELALL 只加在了生产文件，验证床落后 2 段，
导致 check_fin_excel_keys_lock.py 不变量⑥ 失败（钩子会拦截提交）。
方向：生产 → 验证床（不碰生产文件；_port_fin_keys.py 是反向的，会把新代码覆盖掉，不能用）。
"""
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

PATCH_HEAD = "/* =========================================================================\n   ★ Excel 键盘行为补丁"
MARK = "/* ===== FIN-EXCEL-KEYS：Excel 键盘行为补丁"
ANCHOR = "async function fin_initUniver(){"
BED = "_univer_kb_fix.html"
TGT = "choice_lite.html"


def read_raw(p):
    return open(p, 'rb').read()


def norm(raw):
    return raw.decode('utf-8').replace('\r\n', '\n')


raw_bed = read_raw(BED)
crlf = raw_bed.count(b"\r\n")
lf = raw_bed.count(b"\n") - crlf
nl = "\r\n" if crlf > lf else "\n"
bed = norm(raw_bed)

raw_tgt = read_raw(TGT)
t = norm(raw_tgt)
i = t.index(MARK)
j = t.index(ANCHOR)
inj = t[i:j].rstrip()
body = inj.split('===== */\n', 1)[1]
mine = "\n".join(l[4:] if l.startswith('    ') else l for l in body.split('\n')).rstrip()

start = bed.index(PATCH_HEAD)
end = bed.rindex("</script>")
orig = bed[start:end]
ws = orig[len(orig.rstrip()):]          # 保留原尾部空白/换行

if orig.rstrip() == mine:
    print("已经一致，无需同步")
    sys.exit(0)

shutil.copyfile(BED, BED + ".bak_before_sync_selall")
new = bed[:start] + mine + ws + bed[end:]
open(BED, 'wb').write(new.replace("\n", nl).encode('utf-8'))
print("✓ 已同步验证床（备份 %s.bak_before_sync_selall）" % BED)
print("  生产补丁 %d 行 ；验证床补丁 %d 行" % (mine.count('\n') + 1, orig.rstrip().count('\n') + 1))
