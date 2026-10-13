# -*- coding: utf-8 -*-
"""把 _univer_kb_fix.html 里验证通过的 Excel 键盘补丁，原样（重新）注入 choice_lite.html 财务 Univer 模块。
   · 直接抽取验证床里的补丁源码 → 保证两处实现完全一致；
   · 已注入过会先移除旧块再重新注入（可重复执行，用于同步最新实现）；
   · 保持原文件行尾风格；注完自检两边代码逐行一致。"""
import os
import shutil
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
BED = os.path.join(HERE, "_univer_kb_fix.html")
TGT = os.path.join(HERE, "choice_lite.html")
MARK = "/* ===== FIN-EXCEL-KEYS：Excel 键盘行为补丁"
ANCHOR = "    async function fin_initUniver(){"
BIND_OLD = "        finReady = true;"
BIND_NEW = ("        /* Excel 键盘补丁（FIN-EXCEL-KEYS）：api 就绪后绑定，capture 阶段抢在 Univer 之前 */\n"
            "        try { finExcelKeysBind(); } catch(e){ console.warn('[fin-keys] bind failed', e); }\n"
            "        finReady = true;")


def read_text(path):
    raw = open(path, "rb").read()
    crlf = raw.count(b"\r\n")
    lf = raw.count(b"\n") - crlf
    return raw.decode("utf-8").replace("\r\n", "\n"), ("\r\n" if crlf > lf else "\n")


bed, _ = read_text(BED)
start = bed.index("/* =========================================================================\n   ★ Excel 键盘行为补丁")
end = bed.rindex("</script>")
patch = bed[start:end].rstrip()
print("抽取补丁: %d 行, %d 字符" % (patch.count("\n") + 1, len(patch)))

cl, nl = read_text(TGT)
print("目标行尾: %s" % ("CRLF" if nl == "\r\n" else "LF"))

if MARK in cl:
    if cl.count(MARK) != 1 or cl.count(ANCHOR) != 1:
        print("✗ 旧块结构异常，放弃（MARK=%d ANCHOR=%d）" % (cl.count(MARK), cl.count(ANCHOR)))
        sys.exit(2)
    i = cl.index(MARK)
    j = cl.index(ANCHOR)
    cl = cl[:i] + cl[j:]
    if cl.count(BIND_NEW) != 1:
        print("✗ 找不到唯一的绑定调用，放弃")
        sys.exit(2)
    cl = cl.replace(BIND_NEW, BIND_OLD, 1)
    print("已移除旧补丁块，准备重新注入")

if cl.count(ANCHOR) != 1 or cl.count(BIND_OLD) != 1:
    print("✗ 锚点不唯一（ANCHOR=%d BIND=%d）" % (cl.count(ANCHOR), cl.count(BIND_OLD)))
    sys.exit(2)

indented = "\n".join(("    " + ln) if ln.strip() else ln for ln in patch.split("\n"))
block = (MARK + "（与 _univer_kb_fix.html 保持同一份实现，勿删）\n"
         "       实现/验证记录见补丁头部注释；任何重构都不得删除本补丁或其调用。 ===== */\n"
         + indented + "\n\n")

bak = TGT + ".bak_before_fin_keys"
if not os.path.exists(bak):
    shutil.copyfile(TGT, bak)
new = cl.replace(ANCHOR, block + ANCHOR, 1).replace(BIND_OLD, BIND_NEW, 1)
open(TGT, "wb").write(new.replace("\n", nl).encode("utf-8"))

# ---- 自检：注入区的代码必须与验证床逐行一致 ----
chk, _ = read_text(TGT)
i = chk.index(MARK)
j = chk.index(ANCHOR)
injected = chk[i:j].rstrip()
body = injected.split("===== */\n", 1)[1]
deindented = "\n".join(ln[4:] if ln.startswith("    ") else ln for ln in body.split("\n")).rstrip()
same = (deindented == patch)
print("✓ 已注入 choice_lite.html")
print("  自检：注入代码与验证床%s" % ("逐行一致 ✔" if same else "不一致 ✗"))
if not same:
    import difflib
    d = list(difflib.unified_diff(patch.split("\n"), deindented.split("\n"), "bed", "choice", lineterm=""))
    print("\n".join(d[:40]))
    sys.exit(3)
print("  绑定调用: finReady = true; 之前；备份: %s" % os.path.basename(bak))

# ---- 注完顺手跑一次硬锁检查（FIN-EXCEL-KEYS-LOCK-20261011）----
_lock = os.path.join(HERE, "check_fin_excel_keys_lock.py")
if os.path.exists(_lock):
    import subprocess
    r = subprocess.run([sys.executable, _lock, TGT], capture_output=True,
                       encoding="utf-8", errors="replace")
    out = (r.stdout or "").strip()
    if out:
        print(out)
    if r.returncode != 0:
        print("✗ 硬锁检查未通过（见上），请勿提交。")
        sys.exit(4)
