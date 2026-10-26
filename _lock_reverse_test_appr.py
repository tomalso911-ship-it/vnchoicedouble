# -*- coding: utf-8 -*-
"""_lock_reverse_test_appr.py —— check_appr_need_edit_lock.py 的反向测试。

把 choice_lite.html 复制到临时目录，逐个注入「会让 BUG 复发」的破坏，断言锁脚本必须拦截。
运行：python _lock_reverse_test_appr.py
"""
import io
import os
import shutil
import subprocess
import sys
import tempfile

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "choice_lite.html")
LOCK = os.path.join(HERE, "check_appr_need_edit_lock.py")


def run_lock(path):
    p = subprocess.run([sys.executable, LOCK, path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return p.returncode, p.stdout.decode("utf-8", "replace")


def mutate(fn):
    d = tempfile.mkdtemp(prefix="apprlock_")
    dst = os.path.join(d, "choice_lite.html")
    with io.open(SRC, "r", encoding="utf-8", errors="replace") as fh:
        s = fh.read()
    s2 = fn(s)
    if s2 == s:
        shutil.rmtree(d, ignore_errors=True)
        return False, "注入失败（没找到目标文本）"
    with io.open(dst, "w", encoding="utf-8", newline="") as fh:
        fh.write(s2)
    rc, txt = run_lock(dst)
    shutil.rmtree(d, ignore_errors=True)
    return rc != 0, (txt.strip().splitlines() or [""])[-1]


def m1(s):   # ① 回到事故原样：MarkNeedEdit 直接用 prod_save
    return s.replace("prodApprSaveFactory(pid, f); if(PROD_CUR===pid && typeof prod_renderTab==='function') prod_renderTab('D');\n  });\n}\nfunction applyApprovalsLang",
                     "prod_save(f); if(PROD_CUR===pid && typeof prod_renderTab==='function') prod_renderTab('D');\n  });\n}\nfunction applyApprovalsLang", 1)


def m2(s):   # ② 门禁不放开
    return s.replace("window.__PROD_SYNCED[pid]=true;\n          if(window.__PROD_SYNC_INFLIGHT)",
                     "if(window.__PROD_SYNC_INFLIGHT)", 1)


def m3(s):   # ③ 删掉 ✎ 按钮
    return s.replace('onclick="prod_reeditReceipt(', 'onclick="prod_noopReedit(', 1)


def m4(s):   # ④ 删掉 prodApprSaveFactory
    i = s.find("function prodApprSaveFactory(pid, f){")
    j = s.find("\nfunction prodApprApplyInbound(pl)", i)
    if i < 0 or j < 0:
        return s
    return s[:i] + s[j + 1:]


CASES = [
    ("① 回写退回裸 prod_save（事故原样）", m1),
    ("② 取数后不放开门禁", m2),
    ("③ 去掉 ✎ 重新填写 按钮", m3),
    ("④ 删掉 prodApprSaveFactory", m4),
]


def main():
    total, passed = 0, 0
    total += 1
    rc, txt = run_lock(SRC)
    if rc == 0:
        passed += 1
        print("[PASS] 原始文件通过")
    else:
        print("[FAIL] 原始文件被误拦：%s" % txt.strip()[-160:])
    for name, fn in CASES:
        total += 1
        blocked, detail = mutate(fn)
        if blocked:
            passed += 1
            print("[PASS] %s → 已拦截" % name)
        else:
            print("[FAIL] %s → 未拦截 %s" % (name, detail))
    print("\n反向测试：%d/%d" % (passed, total))
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
