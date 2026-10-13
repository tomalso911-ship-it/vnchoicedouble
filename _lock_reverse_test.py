# -*- coding: utf-8 -*-
"""反向测试：故意破坏 check_fin_cn_lock.py 守着的每一条不变量，
确认硬锁脚本【真的能拦住】（篡改 → 必须报错）。全部在临时副本上做，不碰源文件。"""
import io
import os
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_fin_cn_lock as L  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
TMP_HTML = os.path.join(HERE, "_locktest.html")
TMP_PY = os.path.join(HERE, "_locktest.py")
SRC_HTML = os.path.join(HERE, "choice_lite.html")
SRC_PY = os.path.join(HERE, "app.py")
results = []


def case(name, src, tmp, mutate, checker, expect_kw):
    shutil.copyfile(src, tmp)
    text = io.open(tmp, encoding="utf-8").read()
    new = mutate(text)
    if new == text:
        results.append((name, False, "篡改没生效（找不到目标字符串）"))
        return
    io.open(tmp, "w", encoding="utf-8").write(new)
    errs = checker(tmp)
    hit = any(expect_kw in e for e in errs)
    results.append((name, hit, ("拦截到：%s" % errs[0]) if hit else "没拦住！errs=%s" % errs))


# ① 统计栏不再用命令流选区（退化成门面 API → 计数恒为 1）
def m1(t):
    return t.replace("if (cmdSel && fin_statSize(cmdSel) > fin_statSize(ranges)) ranges = cmdSel;",
                     "ranges = fin_getSelectionRanges();")


# ② 去掉格级去重（锚点格算两次）
def m2(t):
    return t.replace("if (seen[_key]) continue;", "")


# ③ 挂起窗口内直接丢弃改动（旧 BUG）
def m3(t):
    return t.replace("if (!fin_isCn()) return;                 // ★越南报表绝不自动保存",
                     "if (!fin_isCn()) return;\n      if (Date.now() < finCnHoldUntil) return;")


# ③ 删掉看门狗
def m4(t):
    return t.replace("if (!finDirty || finSaveTimer || finCnHoldTimer) return;", "")


# ④ 保存成功无条件清 dirty（旧 BUG）
def m5(t):
    return t.replace("if (finDirtyGen === genAtBuild){", "if (true){")


# ④ beacon 又清 dirty
def m6(t):
    return t.replace("/* ★不要在这里清 finDirty：sendBeacon 拿不到响应，服务器可能因 stale/守卫拒收，",
                     "if (sent) finDirty = false;   /*")


# ⑦ 删掉三块对账
def m7(t):
    return t.replace("FIN-CN-TRI-CONSIST-20261013", "FIN-CN-TRI-CONSIST-REMOVED")


case("① 统计栏改用门面选区（计数会退化成 1）", SRC_HTML, TMP_HTML, m1, L.check_html, "①")
case("② 去掉格级去重（锚点格算两次）", SRC_HTML, TMP_HTML, m2, L.check_html, "②")
case("③ 挂起窗口内丢弃改动（旧 BUG 回归）", SRC_HTML, TMP_HTML, m3, L.check_html, "③")
case("③ 删除看门狗", SRC_HTML, TMP_HTML, m4, L.check_html, "③")
case("④ 保存成功无条件清 dirty（旧 BUG 回归）", SRC_HTML, TMP_HTML, m5, L.check_html, "④")
case("④ beacon 又清 finDirty", SRC_HTML, TMP_HTML, m6, L.check_html, "④")
case("⑦ 删除三块对账标记", SRC_HTML, TMP_HTML, m7, L.check_html, "⑦")


# ⑤ 服务端守卫被删
def p1(t):
    return t.replace("CN-BASIS-GUARD", "BASIS-GUARD-REMOVED")


# ⑤ 阈值被放宽（放掉 ÷3882 污染）
def p2(t):
    return t.replace("(_new_base / _old_base) < 0.02", "(_new_base / _old_base) < 0.0")


# ⑥ 又用非原子写盘
def p3(t):
    return t.replace("def _cn_seed_if_missing():", "def _cn_seed_if_missing():\n    wb = None\n    wb.save(CN_REPORT)")


case("⑤ 服务端金额守卫被删除", SRC_PY, TMP_PY, p1, L.check_py, "⑤")
case("⑤ 守卫阈值被放宽（放掉换算污染）", SRC_PY, TMP_PY, p2, L.check_py, "⑤")
case("⑥ 又用非原子写盘 wb.save(CN_REPORT)", SRC_PY, TMP_PY, p3, L.check_py, "非原子写盘")

for f in (TMP_HTML, TMP_PY):
    try:
        os.remove(f)
    except OSError:
        pass

print("=== 反向测试（篡改必须被拦）===")
bad = 0
for name, ok, msg in results:
    print("  %s %s —— %s" % ("✔" if ok else "✘", name, msg))
    if not ok:
        bad += 1
print("===> %s" % ("全部拦住（硬锁有效）" if bad == 0 else ("有 %d 种篡改没被拦住！" % bad)))
sys.exit(1 if bad else 0)
