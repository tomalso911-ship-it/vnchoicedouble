# -*- coding: utf-8 -*-
"""_lock_reverse_test_pyname.py —— check_py_name_lock.py 的反向测试。

做法：把 app.py 复制一份，逐个注入「真实事故同款」的破坏，再对副本跑锁脚本，
      断言每一种都必须被拦截（退出码非 0）。全部拦截 = 锁有效。

运行：python _lock_reverse_test_pyname.py
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "app.py")
LOCK = os.path.join(HERE, "check_py_name_lock.py")


def run_lock(path):
    r = subprocess.run([sys.executable, LOCK, path],
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return r.returncode, r.stdout.decode("utf-8", "replace")


def mutate(name, fn):
    tmpdir = tempfile.mkdtemp(prefix="pyname_")
    dst = os.path.join(tmpdir, "app.py")
    shutil.copyfile(SRC, dst)
    src = open(dst, "r", encoding="utf-8").read()
    out = fn(src)
    if out == src:
        shutil.rmtree(tmpdir, ignore_errors=True)
        return name, False, "注入失败（没找到目标文本）"
    open(dst, "w", encoding="utf-8").write(out)
    rc, txt = run_lock(dst)
    shutil.rmtree(tmpdir, ignore_errors=True)
    return name, rc != 0, txt.strip().splitlines()[0] if txt.strip() else ""


def m1(src):
    """还原 2026-10-26 的线上 BUG：中国报表备份函数改名 → 三处调用变 NameError。"""
    return src.replace("def _cn_daily_backup():", "def _fin_daily_backup():", 1)


def m2(src):
    """只在调用处改名（函数没定义）。"""
    return src.replace("_cn_daily_backup()", "_cn_daily_backups()", 1)


def m3(src):
    """新增一个未定义调用（模拟重构时漏改函数名）。"""
    return src.replace("def _cn_rev():", "def _cn_rev():\n    _cn_rev_check()\n", 1)


def m4(src):
    """顶层函数被别人撞名（顶掉）。"""
    return src.replace("def _cn_daily_backup():", "def _fin_daily_backup():", 1) + \
        "\n\ndef _fin_daily_backup():\n    return None\n"


CASES = [
    ("① 备份函数改名（线上事故原样）", m1),
    ("② 调用处写错名字", m2),
    ("③ 函数体调用未定义函数", m3),
    ("④ 顶层函数重名追加", m4),
]


def main():
    if not os.path.isfile(SRC):
        print("找不到 app.py")
        return 1
    ok = 0
    total = 0
    # 先确认未破坏的版本能通过
    rc, txt = run_lock(SRC)
    total += 1
    if rc == 0:
        ok += 1
        print("[PASS] 原始 app.py 通过检查")
    else:
        print("[FAIL] 原始 app.py 竟被拦下：%s" % txt.strip()[:200])

    for name, fn in CASES:
        total += 1
        n, blocked, detail = mutate(name, fn)
        if blocked:
            ok += 1
            print("[PASS] %s → 已被拦截" % n)
        else:
            print("[FAIL] %s → 未被拦截 %s" % (n, detail))
    print("\n反向测试：%d/%d" % (ok, total))
    return 0 if ok == total else 1


if __name__ == "__main__":
    sys.exit(main())
