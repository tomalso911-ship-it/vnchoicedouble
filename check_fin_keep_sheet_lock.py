# -*- coding: utf-8 -*-
"""硬锁自检：财务「重建后留在用户原来看的那张工作表」（FIN-KEEP-SHEET-20261015）。

用户 2026-10-15 要求：「查报表选好年月点确认后，整张表竟然跳到主表格 —— 表格必须仍然停在我
正在看的那张工作表里，不能跳动」（越南财务报表 + 合并报表都算）。

契约（任何重构不得破坏）：
  ① 必须先记后重建：fin_reload 里 fin_captureSheetState() 出现在 fin_applySnapshot(snap) 之前；
  ② 重建后必须恢复：fin_restoreSheetState(keepSheet) 存在，且至少补 3 次（首帧渲染会再跳一次）；
  ③ 合并报表的「强切到中国区块」只能由按钮触发（__FIN_MERGE_FOCUS_CN 在
     fin_mergeToggleCnGroup 里置位、在 fin_applySnapshot 里消费并清零），
     查报表 / 复位 / 载入刷新走 fin_applySnapshot 时不许强切表；
  ④ 有强切标记时不许再抢焦点（fin_reload 的恢复必须被 __FIN_MERGE_FOCUS_CN 挡住）；
  ⑤ 查报表确认仍走 fin_reload（否则这套恢复根本不生效）；
  ⑥ 语言切换路径的 FIN-KEEP-SHEET-20261012 三条恢复调用不得被删。
失败即 exit 1（已登记进 .githooks/pre-commit 硬锁列表）。
"""
import re
import sys
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

src = open("choice_lite.html", encoding="utf-8", errors="replace").read()
ok = True


def chk(cond, msg):
    global ok
    print(("  ✓ " if cond else "  ✗ ") + msg)
    if not cond:
        ok = False


def func_text(sig):
    try:
        i = src.index(sig)
    except ValueError:
        return ""
    j = src.index('{', i)
    depth, k = 0, j
    while k < len(src):
        if src[k] == '{':
            depth += 1
        elif src[k] == '}':
            depth -= 1
            if depth == 0:
                return src[i:k + 1]
        k += 1
    return ""


print("1) 先记后重建")
reload_src = func_text("async function fin_reload(opts){")
chk(reload_src != "", "找到 async function fin_reload(opts)")
i_cap = reload_src.find("fin_captureSheetState()")
i_apply = reload_src.find("fin_applySnapshot(snap)")
chk(i_cap >= 0 and i_apply >= 0 and i_cap < i_apply,
    "fin_captureSheetState() 出现在 fin_applySnapshot(snap) 之前")

print("2) 重建后恢复（多补几次）")
chk("fin_restoreSheetState(keepSheet)" in reload_src, "调用 fin_restoreSheetState(keepSheet)")
n_restore = len(re.findall(r"setTimeout\(restoreSheet,", reload_src))
chk(n_restore >= 3, "至少补 3 次恢复（实际 %d）" % n_restore)
chk("function fin_captureSheetState()" in src and "function fin_restoreSheetState(st)" in src,
    "两个底层函数都在（记录/恢复工作表 + 滚动 + 选区）")

print("3) 合并报表强切表只能由按钮触发")
chk("window.__FIN_MERGE_FOCUS_CN = true;" in func_text("function fin_mergeToggleCnGroup(){"),
    "fin_mergeToggleCnGroup 置位 __FIN_MERGE_FOCUS_CN")
snap_src = func_text("function fin_applySnapshot(snap){")
chk("if (window.__FIN_MERGE_FOCUS_CN){" in snap_src, "fin_applySnapshot 里按标记决定是否强切表")
chk("window.__FIN_MERGE_FOCUS_CN = false;" in snap_src, "用完即清零（不许残留影响下一次重建）")
# 强切表的两条 setTimeout 必须在标记判断之内：直接比较文本顺序
i_flag = snap_src.find("if (window.__FIN_MERGE_FOCUS_CN){")
i_focus = snap_src.find("fin_mergeFocusCnSheet(); } catch(e){} }, 700)")
chk(i_flag >= 0 and i_focus > i_flag, "fin_mergeFocusCnSheet 的两条调用落在标记判断之内")

print("4) 有强切标记时不许抢焦点")
chk(re.search(r"if \(!window\.__FIN_MERGE_FOCUS_CN\)\{\s*var restoreSheet", reload_src) is not None,
    "fin_reload 的恢复被 __FIN_MERGE_FOCUS_CN 挡住（点击切换分组时不抢）")

print("5) 查报表确认仍走 fin_reload")
chk(re.search(r"function fin_rptApplyFilter\(year, month\)\{[\s\S]{0,200}finRptFilter = \{ year: year, month: month \|\| 0 \};[\s\S]{0,120}await fin_reload\(\{ keepFilter: true \}\)",
              src) is not None, "fin_rptApplyFilter → fin_reload({keepFilter:true})")

print("6) 语言切换路径的既有恢复不得被删")
chk("var restore = function(){ try { fin_restoreSheetState(keep); } catch(e){} };" in src,
    "fin_applyLangView 的 FIN-KEEP-SHEET-20261012 恢复仍在")

print()
print("总体:", "全部通过 ✓" if ok else "有失败 ✗")
sys.exit(0 if ok else 1)
