# -*- coding: utf-8 -*-
"""跑 app.py 语法编译 + 5 个财务硬锁脚本（含两个反向测试），结果落到 _run_locks_out.txt。"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "_run_locks_out.txt")
L = []


def dump():
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


def run(args, tag):
    L.append("=" * 78)
    L.append("== %s" % tag)
    L.append("=" * 78)
    dump()
    r = subprocess.run(args, capture_output=True, text=True, cwd=HERE,
                       encoding="utf-8", errors="replace", timeout=900)
    L.append("rc=%d" % r.returncode)
    if r.stdout:
        L.append(r.stdout.rstrip())
    if r.stderr:
        L.append("[stderr]\n" + r.stderr.rstrip())
    L.append("")
    dump()
    return r.returncode


PY = sys.executable
run([PY, "-m", "py_compile", "app.py"], "py_compile app.py")
for nm, extra in (("check_fin_cn_lock.py", []),
                  ("check_fin_snap_cache.py", []),
                  ("check_fin_hi_lock.py", []),
                  ("check_fin_formula_lock.py", []),
                  ("check_fin_excel_keys_lock.py", []),
                  ("check_fin_no_trans_lock.py", []),
                  ("check_fin_cn_lock.py", ["--selftest"]),
                  ("check_fin_snap_cache.py", ["--selftest"])):
    if os.path.isfile(os.path.join(HERE, nm)):
        run([PY, nm] + extra, nm + (" " + " ".join(extra) if extra else ""))
    else:
        L.append("（缺文件：%s）" % nm)
        dump()
dump()
print("done")
