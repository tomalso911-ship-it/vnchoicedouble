# -*- coding: utf-8 -*-
"""硬锁自检：股东权益报表「独立第二套 Univer 实例」（FIN-EQUITY-20261015）。

用户 2026-10-15 要求：
  · 顶部已有「股东权益」标签（原占位页）→ 换成和越南财务报表一样的 Excel 界面；
  · ★用户明确选【② 真·独立视图】：#view-equity 里另起容器 + 第二套 Univer，不与财务 fin* 单例共享；
  · 5 张工作簿平级：总投资数据 / 中国投资数据 / 越南投资数据 / 股东结构 / 分红记录，表名三语；
  · 语言逻辑完全照搬财务：三语 + 自动翻译（/api/translate）；
  · 新建 equity_report.xlsx，可编辑 + 保存（自动 0.7s + 手动按钮）；
  · ★不需要「重导」按钮。

契约（任何重构不得破坏）：
  ① 后端 EQ_SHEET_DEFS 必须 5 张表，且每张都有 vi/zh/en 三语表名；
  ② 文件里的表名固定【越文】：总投资表的跨表公式必须引用越文表名（切语言才不会 #REF!）；
  ③ 后端必须有 snapshot(GET) / save(POST) / 下载(GET)，且★绝不能有 equity 的 init「重导」路由；
  ④ 前端 #view-equity 不得再是占位页，必须有 #equity_container；
  ⑤ createUniver 的 container 必须是 equity_container，unitId 必须是 equity-report；
  ⑥ 工具栏不得出现「重导」(fin_btn_reimport)，必须有「保存」(fin_btn_save) 与「导出」(fin_btn_export)；
  ⑦ 自动保存 700ms + 手动保存按钮双通道；
  ⑧ 币种：屏幕换算，保存前必须乘回 VND 原值（文件永远只有 VND）；
  ⑨ 三语：applyTrans + applyTitles + /api/translate；★改名时必须同步改公式里的表名引用；
  ⑩ 查报表：按年月用 rowData.hd 隐藏行；
  ⑪ 前端 SHEETS 列定义必须与后端 EQ_SHEET_DEFS 的 5 个越文表名一一对应。
失败即 exit 1（已登记进 .githooks/pre-commit 与 pre-push 硬锁列表）。
"""
import re
import sys
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

html = open("choice_lite.html", encoding="utf-8", errors="replace").read()
py = open("app.py", encoding="utf-8", errors="replace").read()
ok = True
NAMES = ['Tổng đầu tư', 'Đầu tư Trung Quốc', 'Đầu tư Việt Nam', 'Cơ cấu cổ đông', 'Cổ tức']


def chk(cond, msg):
    global ok
    print(("  ✓ " if cond else "  ✗ ") + msg)
    if not cond:
        ok = False


def block(start_marker, end_marker):
    try:
        i = html.index(start_marker)
        j = html.index(end_marker, i)
        return html[i:j]
    except ValueError:
        return ""


print("1) 后端：5 张表 + 三语表名")
for n in NAMES:
    chk(("\"vi\": \"%s\"" % n) in py or ("'vi': '%s'" % n) in py, "后端定义表 %s" % n)
for zh in ('总投资数据', '中国投资数据', '越南投资数据', '股东结构', '分红记录'):
    chk(zh in py, "后端含中文表名 %s" % zh)
for en in ('Total Investment', 'China Investment', 'Vietnam Investment', 'Shareholder Structure', 'Dividend Records'):
    chk(en in py, "后端含英文表名 %s" % en)

print("2) 后端：跨表公式引用【越文】表名")
chk("=SUM('Đầu tư Trung Quốc'!" in py, "总投资 → 中国投资 公式引用越文表名")
chk("=SUM('Đầu tư Việt Nam'!" in py, "总投资 → 越南投资 公式引用越文表名")

print("3) 后端接口：snapshot / save / 下载；★无重导")
for pat, name in (('/api/finance/equity-report/snapshot', 'GET snapshot'),
                  ('/api/finance/equity-report/save', 'POST save'),
                  ('/api/finance/equity-report"', 'GET 下载 xlsx')):
    chk(pat in py, name)
chk('/api/finance/equity-report/init' not in py, "★没有「重导/init」上传路由（用户明确不要）")

print("4) 前端：#view-equity 不再是占位页")
chk('股东权益模块开发中，敬请期待。' not in html, "占位文案已移除")
chk('id="equity_container"' in html, "存在独立容器 #equity_container")

print("5) 前端：第二套实例（container / unitId）")
chk("container: 'equity_container'" in html, "createUniver 指向 equity_container")
chk("'equity-report'" in html and "v.id = 'equity-report'" in html, "unitId = equity-report")
chk("univer.createUnit(" in html, "用 createUnit 建单元（与财务同构）")

print("6) 工具栏：用户 2026-10-15 拍板 —— 只留 币种下拉 + 保存 + 导出")
sec = block('id="view-equity"', 'id="equity_container"')
chk(sec != "", "定位到股东权益视图区块")
chk('fin_btn_reimport' not in sec, "★工具栏没有「重导」按钮")
for k, n in (('fin_btn_save', '保存'), ('fin_btn_export', '导出 xlsx')):
    chk(k in sec, "工具栏有「%s」按钮" % n)
for k, n in (('fin_btn_report', '查报表'), ('fin_btn_sort_asc', '升序'), ('fin_btn_sort_desc', '降序'),
             ('fin_btn_ins_rows', '在下方插入行'), ('fin_btn_load', '载入/刷新报表'),
             ('fin_merge_group_btn_on', '恢复原显示顺序')):
    chk(k not in sec, "★已删按钮：「%s」不在工具栏" % n)
chk('id="eq_cur"' in sec and 'id="eq_inline"' in sec, "币种下拉与按钮组容器存在")
# ★用户 2026-10-15 第五次调整（照越南财务报表的做法）：
#   保存 / 导出 xlsx 留在表格上方的按钮行；只有币种下拉那组 #eq_inline 会被挂进 Excel 工具栏。
i_sel = sec.find('id="eq_cur"')
i_save = sec.find('fin_btn_save')
i_exp = sec.find('fin_btn_export')
chk(i_save >= 0 and i_exp > i_save, "DOM 顺序：保存 在 导出 xlsx 之前")
chk(i_sel > i_exp, "DOM 顺序：币种下拉组 #eq_inline 排在按钮行之后")
_m = re.search(r'<div id="eq_inline".*?</div>', sec, re.S)
chk(_m is not None and 'fin_btn_save' not in _m.group(0) and 'fin_btn_export' not in _m.group(0),
    "★保存/导出不在 #eq_inline 里（只有币种下拉挂进 Excel 工具栏）")

print("6b) 币种下拉挂 Excel 自带工具栏最左侧 + Univer 工具栏留在 Excel 表内表头 + 隐藏 $/漏斗/保护图标")
eqblk = block('股东权益报表引擎（FIN-EQUITY-20261015）', 'window.__eqSwitchWrapped')
if not eqblk:
    try:
        i = html.index('股东权益报表引擎（FIN-EQUITY-20261015）')
        j = html.index('</script>', i)
        eqblk = html[i:j]
    except ValueError:
        eqblk = ""
chk(eqblk != "", "定位到股东权益引擎脚本块")
chk("'sheet.command.numfmt.set.currency': { hidden: true }" in eqblk, "★Univer 自带 $ 按钮已隐藏（与财务同机制）")
chk("'sheet.command.smart-toggle-filter': { hidden: true }" in eqblk, "★内置筛选（漏斗）已隐藏")
chk("'sheet.command.add-range-protection-from-toolbar': { hidden: true }" in eqblk, "★工具栏「保护范围」图标已隐藏")
chk(re.search(r"querySelector\('#equity_container \.univer-toolbar-container'\)", eqblk) is not None,
    "找到 Univer 工具栏宿主 .univer-toolbar-container")
chk(re.search(r"host\.insertBefore\(sel, host\.firstChild\)", eqblk) is not None,
    "★币种下拉插到 Excel 自带工具栏最左侧（与财务 fin_mountToolbar2 同机制）")
# ★用户 2026-10-15 第五次调整（照财务报表）：Univer 自带工具栏（字体/字号/数字格式那些「展开」下拉）
#   必须留在 Excel 里面的表头位置，不许再被搬出到表格外。
chk("bar.appendChild(host)" not in eqblk and "function safeDom(node)" not in eqblk,
    "★Univer 工具栏不被搬出 Excel（留在表内表头，照财务做法）")
chk("more-function-single" in eqblk, "★隐藏 Univer 自带「⋮」收纳按钮（展开下拉不会被藏起来）")
chk("new MutationObserver(" in eqblk, "DOM 变动自动重挂（切表后不掉下来）")

print("7) 自动保存 0.7s + 手动保存")
chk(re.search(r"saveTimer = setTimeout\(function\(\)\{ saveTimer = null; if \(dirty\) save\(false\); \}, 700\)", html) is not None,
    "录入后 0.7 秒自动落盘")
chk("save: function(m){ save(!!m); }" in html, "手动「保存」按钮通道")

print("8) 币种：屏幕换算、保存乘回 VND")
chk("cell.v = Math.round(cell.v / rate * 100) / 100" in html, "显示时 ÷ 汇率")
chk("cell.v = Math.round(cell.v * rate)" in html, "★保存时 × 汇率还原成 VND 原值")

print("9) 三语：翻译 + 表名改名同步改公式")
chk("/api/translate?q=" in html, "走 /api/translate 自动翻译")
chk("function applyTrans(" in html, "applyTrans（单元格译文回填）")
chk("function applyTitles(" in html, "applyTitles（表名三语）")
chk(re.search(r"cell\.f = cell\.f\.split\(\"'\" \+ old \+ \"'\"\)\.join\(\"'\" \+ neu \+ \"'\"\)", html) is not None,
    "★改名时同步替换公式里的表名引用（否则 #REF!）")

print("10) 查报表：按年月隐藏行")
chk("sh.rowData[rk].hd = 1" in html, "非匹配行 rowData.hd = 1")

print("11) 前后端 5 张表一一对应")
for n in NAMES:
    chk(("vi:'%s'" % n) in html, "前端 SHEETS 定义 %s" % n)

print()
print("总体:", "全部通过 ✓" if ok else "有失败 ✗")
sys.exit(0 if ok else 1)
