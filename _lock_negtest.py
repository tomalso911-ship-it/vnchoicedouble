# -*- coding: utf-8 -*-
"""反向测试：故意篡改四条不变量，确认 check_fin_hi_lock.py 会拦截。"""
import os
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "choice_lite.html")
src = open(SRC, encoding="utf-8").read()

TAMPERS = [
    ("① 去掉静默窗口", "if (finHiApplying || Date.now() < finHiQuietUntil) return;",
     "if (finHiApplying) return;"),
    ("② 恢复旧 BUG：不克隆直接塞实时样式对象", "cell.s = fin_cloneStyleObj(st);", "cell.s = st;"),
    ("② 恢复旧 BUG：直接 delete 实时样式对象",
     "                  var _cp4 = fin_cloneStyleObj(_s4);\n                  delete _cp4.cl;",
     "                  var _cp4 = _s4;\n                  delete _s4.cl;"),
    ("③ 恢复旧 BUG：只看行号就 return", "if (rowsSame && styleOk) return;", "if (rowsSame) return;"),
    ("③ 删掉自愈抽查", "if (!finHiRowHasHi(snap, sid, newRows[_hi])){ styleOk = false; break; }",
     "if (false){ styleOk = false; break; }"),
]

ok = True
for name, old, new in TAMPERS:
    if old not in src:
        print("!! 篡改点未找到（锚点变了）:", name)
        ok = False
        continue
    tmp = os.path.join(HERE, "_tamper_tmp.html")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(src.replace(old, new, 1))
    r = subprocess.run([sys.executable, os.path.join(HERE, "check_fin_hi_lock.py"), tmp],
                       capture_output=True, text=True, encoding="utf-8", errors="replace",
                       env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    caught = (r.returncode != 0)
    print(("✓ 已拦截  " if caught else "✗ 漏检!!  ") + name + "  (exit=%d)" % r.returncode)
    if caught:
        first = [l for l in (r.stdout or "").splitlines() if "违规" in l]
        if first:
            print("     ", first[0].strip())
    else:
        ok = False
    os.remove(tmp)

print()
print("反向测试结果:", "全部拦截 ✓" if ok else "存在漏检 ✗")
sys.exit(0 if ok else 1)
