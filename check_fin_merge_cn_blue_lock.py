# -*- coding: utf-8 -*-
"""硬锁自检：合并报表「中国区块蓝字守卫」（FIN-MERGE-CN-BLUE-GUARD-20261015）。

用户 2026-10-15 要求：「合并报表里中国成本记录那一块，必须全是蓝字」。
契约（任何重构不得破坏）：
  ① finMergeCnBlueGuard() 必须存在；
  ② 必须只在合并报表 + 分组状态生效：FIN_KIND !== 'merge' || !FIN_MERGE_CN_GROUP 直接返回；
  ③ 必须【整行跳过红高亮行】（hiRows 判断 + 红字判断两条都要在）——
     用户 2026-10-15 明确选 A：保留"离今天最近那一行"的红高亮，蓝字守卫不许盖掉它；
  ④ 必须静默写入（finHiApplying + finHiQuietUntil），只写样式不写值，绝不触发保存/翻译；
  ⑤ 必须每轮高亮之后兜底调用（载入 700ms 块 + 2 秒轮询 + 两条重建路径），
     这样任何一次"撤高亮写黑"都能在 2 秒内自己修回来；
  ⑥ 两条重建路径（fin_loadReport / fin_applySnapshot）必须清空陈旧高亮坐标 finHiState，
     否则会用旧布局行号去撤高亮 → 把（分组后行号已变的）中国行写成黑色。
失败即 exit 1（已登记进 .githooks/pre-commit 硬锁列表）。
"""
import re
import sys
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

SRC = "choice_lite.html"
src = open(SRC, encoding="utf-8", errors="replace").read()
ok = True


def chk(cond, msg):
    global ok
    print(("  ✓ " if cond else "  ✗ ") + msg)
    if not cond:
        ok = False


def block_of(name):
    """按大括号配平切出整个函数体（够用的粗切法）。"""
    try:
        start = src.index("function %s(" % name)
    except ValueError:
        return None
    i = src.index('{', start)
    depth, j = 0, i
    while j < len(src):
        if src[j] == '{':
            depth += 1
        elif src[j] == '}':
            depth -= 1
            if depth == 0:
                return src[start:j + 1]
        j += 1
    return None


print("1) 守卫函数")
g = block_of("finMergeCnBlueGuard")
chk(g is not None, "定义 function finMergeCnBlueGuard()")
g = g or ""

print("2) 只在合并报表 + 分组状态生效")
chk("FIN_KIND !== 'merge' || !FIN_MERGE_CN_GROUP" in g, "开头 return 判定（合并 + 分组）")
chk("window.__FIN_MERGE_CN_ROWBASE" in g and "window.__FIN_MERGE_CN_ROWS" in g,
    "中国区块行号取 __FIN_MERGE_CN_ROWBASE/ROWS（不靠已被裁掉的 AN 列）")

print("3) 红高亮行整行不碰（用户选 A）")
chk("hiRows.indexOf(r) >= 0) continue" in g, "按 finHiState 高亮行跳过")
chk("'FF0000'\" >= 0) continue" in g or "FF0000" in g, "红字格跳过（绝不盖掉红高亮）")

print("4) 静默写入 + 只写样式")
chk("finHiApplying = true" in g and "finHiQuietUntil" in g, "复用高亮静默窗口")
chk("finExecSilent('sheet.command.set-range-values'" in g, "走 finExecSilent 写样式")
chk(re.search(r"ns\.cl = \{ rgb: FIN_CN_BLUE \}", g) is not None, "只换字色 cl（粗体/边框/格式保留）")

print("5) 调用点：必须排在高亮之后")
call_sites = [m.start() for m in re.finditer(r'finMergeCnBlueGuard\(\)', src)
              if "function " not in src[max(0, m.start() - 12):m.start()]]
chk(len(call_sites) >= 4, "至少 4 处调用（实际 %d）" % len(call_sites))
# 载入 700ms 块：finHiRecompute(); 之后必须紧跟守卫
init_ok = re.search(r'finHiRecompute\(\);\s*(if \(_cleaned > 0\) fin_markDirty\(\);)?\s*/\* ★FIN-MERGE-CN-BLUE-GUARD', src) is not None
chk(init_ok, "载入块：finHiRecompute() 之后紧跟守卫")
poll_ok = re.search(r"try \{ finHiRecompute\(\); \} catch\(e\)\{ console\.warn\('\[hi\] poll error', e\); \}\s*/\* ★FIN-MERGE-CN-BLUE-GUARD", src) is not None
chk(poll_ok, "2 秒轮询：finHiRecompute() 之后紧跟守卫")

print("6) 重建路径必须清空陈旧高亮坐标（三处：切报表 / fin_loadReport / fin_applySnapshot）")


def func_region(sig):
    """切出某个函数定义体（到下一个顶层 function 之前）。"""
    try:
        i = src.index(sig)
    except ValueError:
        return ""
    j = src.find("\n    function ", i + len(sig))
    return src[i:j if j > 0 else len(src)]


load_reg = func_region("function fin_loadReport(")
chk("finHiState = {};" in load_reg and "FIN-HI-STALE-STATE-20261015" in load_reg,
    "fin_loadReport 重建前 finHiState = {}（带 STALE-STATE 说明）")
snap_reg = func_region("function fin_applySnapshot(snap){")
chk("finHiState = {};" in snap_reg and "FIN-HI-STALE-STATE-20261015" in snap_reg,
    "fin_applySnapshot 重建前 finHiState = {}（带 STALE-STATE 说明）")

print()
print("总体:", "全部通过 ✓" if ok else "有失败 ✗")
sys.exit(0 if ok else 1)
