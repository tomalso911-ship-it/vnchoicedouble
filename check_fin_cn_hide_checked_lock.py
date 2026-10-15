# -*- coding: utf-8 -*-
"""硬锁自检：中国报表「隐藏核销记录」按钮（FIN-CN-HIDE-CHECKED-20261015）。

契约（用户 2026-10-15 要求，任何重构不得破坏）：
  ① 三语文案 key fin_btn_hide_checked / fin_btn_show_checked 各在 zh/en/vi 三个字典里各 1 次；
  ② 工具栏按钮 id=fin_cn_hide_checked_btn、onclick=fin_cnToggleHideChecked()、
     初始 data-i18n=fin_btn_hide_checked；
  ③ 按钮位置必须在「查报表」(fin_btn_report) 与「导出 xlsx」(fin_btn_export) 之间；
  ④ 四个 JS 函数必须存在：fin_cnCheckedRowsIn / fin_cnHideCheckedInView /
     fin_cnHideCheckedBtnLabel / fin_cnToggleHideChecked；
  ⑤ 调用点必须在 fin_rptHideInView 之前（后跑者优先，否则「恢复」会放不出查报表隐藏的日期行）；
  ⑥ 仅在中国报表显示（fin_applyReadonlyUI 里按 isCn 显隐）+ 刷新按钮文案；
  ⑦ 隐藏机制与「查报表」一致：只写显示快照 rowData[行].hd = 1（用 fin_rptCloneRowData 克隆），
     恢复时 delete .hd；【绝不碰 cellData、绝不删数据】。

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


print("1) 三语 key")
chk(src.count('fin_btn_hide_checked:') == 3, "fin_btn_hide_checked 在 3 个语言字典里各 1 次（实际 %d）"
    % src.count('fin_btn_hide_checked:'))
chk(src.count('fin_btn_show_checked:') == 3, "fin_btn_show_checked 在 3 个语言字典里各 1 次（实际 %d）"
    % src.count('fin_btn_show_checked:'))

print("2) 工具栏按钮")
chk('id="fin_cn_hide_checked_btn"' in src, "按钮 id=fin_cn_hide_checked_btn 存在")
chk('onclick="fin_cnToggleHideChecked()"' in src, "按钮 onclick=fin_cnToggleHideChecked()")
chk('data-i18n="fin_btn_hide_checked"' in src, "按钮初始 data-i18n=fin_btn_hide_checked")

print("3) 按钮位置：查报表 与 导出 xlsx 之间")
i_rep = src.index('data-i18n="fin_btn_report"')
i_new = src.index('id="fin_cn_hide_checked_btn"')
i_exp = src.index('data-i18n="fin_btn_export"')
chk(i_rep < i_new < i_exp, "顺序 = 查报表(%d) < 新按钮(%d) < 导出xlsx(%d)" % (i_rep, i_new, i_exp))

print("4) JS 函数")
for fn in ("fin_cnCheckedRowsIn", "fin_cnHideCheckedInView", "fin_cnHideCheckedBtnLabel",
           "fin_cnToggleHideChecked"):
    chk(("function %s(" % fn) in src, "定义 function %s" % fn)

print("5) 调用点：必须在 fin_rptHideInView 之前（后跑者优先）")
calls = [m.start() for m in re.finditer(r'fin_cnHideCheckedInView\(', src)]
# 排除函数定义本身：定义处紧随其后的名字前面是 "function "
call_sites = [p for p in calls if not re.search(r'\bfunction\s+$', src[max(0, p - 20):p])]
chk(len(call_sites) >= 2, "至少 2 处调用（实际 %d）" % len(call_sites))
order_ok = True
for p in call_sites:
    nxt = src.find('fin_rptHideInView(', p)
    if nxt < 0 or nxt - p > 200:
        order_ok = False
chk(order_ok, "每处调用后面紧跟 fin_rptHideInView（都在 200 字符内）")

print("6) 只在中国报表显示 + 标签刷新")
chk("if (hc) hc.style.display = isCn ? '' : 'none';" in src, "fin_applyReadonlyUI 里按 isCn 显隐")
chk("fin_cnHideCheckedBtnLabel();" in src, "fin_applyReadonlyUI 里刷新按钮文案")

print("7) 隐藏机制与查报表一致（rowData[].hd + 克隆）")
blk = src[src.index("function fin_cnHideCheckedInView("):]
blk = blk[:blk.index("\n    }\n") + 6]
chk("fin_rptCloneRowData" in blk, "用 fin_rptCloneRowData 克隆 rowData")
chk("hd = 1" in blk, "写 rowData[行].hd = 1")
chk("delete" in blk and ".hd" in blk, "恢复时 delete .hd")
chk("cellData" not in blk, "绝不碰 cellData（不删数据）")

print()
print("总体:", "全部通过 ✓" if ok else "有失败 ✗")
sys.exit(0 if ok else 1)
