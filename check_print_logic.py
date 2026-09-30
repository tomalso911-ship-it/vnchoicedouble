#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
打印逻辑「锁死」检查（lint / CI / git pre-commit 均可用）。

契约（见 choice_lite.html 中 [FROZEN 契约 · 打印] 注释）：

  A. 甘特(横道图)打印 —— 必须「左右两栏 + 一页装下」
    A1  printPdf 注入的打印 CSS 必须含 flex-direction:row !important。
        原因：模板里有 @media (max-width:1000px){ .layout{flex-direction:column} }，
        打印时纸宽按纸张算（A4 竖版可打印宽≈748px < 1000px）会命中这条移动端规则，
        不覆盖就会把「左表」和「横道图」拆成上下两半。
    A2  左表必须固定宽度 width:var(--tbl-w,470px) !important。
        改成 width:auto 会让 flex:0 0 auto 吃光整行，把横道图挤成 0 宽 → 打印时看不见。
    A3  必须按纸张宽度提供三档缩放分支：max-width:1120px / max-width:800px。
    A4  打印时必须排除甘特下方的「区汇总 + 小组负载 + 图例」(#cardsWrap)，否则多一张空白废页。
    A5  禁止在 printPdf 里强制分页 break-before:page / page-break-before:always
        （会把甘特整块顶到第 2 页，第 1 页只剩标题）。
    A6  缩放用的 totalH 必须把版面顶部内容(offTop)算进去，否则甘特被顶到第 2 页。

  B. 智能报告打印 —— 必须「块级流 + 可跨页 + 不依赖 JS 时序」
    B1  .modal 在打印下必须 display:block。.modal 基础样式是 display:flex;flex-direction:column，
        Chrome/Edge 对 flex 容器的分页支持极差，会把 <h2> 留在第 1 页、正文整块推到第 2 页。
    B2  必须有 body > .modal-overlay.show 兜底打印目标（Edge 打印预览是异步快照，
        只依赖 JS 临时标记时，标记一丢整页就会被 body>*{display:none} 隐藏 → 打印空白）。
    B3  #slatsReportBody 必须解除 max-height:65vh / overflow 裁剪，否则只打出容器可视区那一页。
    B4  段落 break-inside 必须为 auto：超高段落若整段 avoid，会被整段推到下一页，页尾留大片空白。

  C. 打印标记生命周期
    C1  禁止在 window.print() 之后用 300ms 定时器摘标记/摘类
        （打印是异步的，Edge 抓 DOM 更慢，摘早了预览整页空白 / 内容残缺）。
    C2  必须存在 __clearPrintTarget / __lazyClearPrintTarget 这一对延迟清理函数。
    C3  禁止在 JS 字符串里出现字面 '<script>(function(){'：未转义的 script 开始标签
        会被 HTML 解析器当成真标签，把脚本块从中间切断，
        导致 printModalById / printDashboard 等全部未定义（点「打印PDF」毫无反应）。

用法：
  python3 check_print_logic.py [path/to/choice_lite.html]
  不传路径时默认检查同目录下的 choice_lite.html。
退出码：0 = 通过；1 = 发现违规（可用于 CI 失败 / pre-commit 拦截）。
"""
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "choice_lite.html")


def fn_body(src, name):
    """截取顶层函数体：从 'function xxx(' 到行首的 '}'。"""
    i = src.find(name)
    if i < 0:
        return ""
    j = src.find("\n}", i)
    return src[i:j + 2] if j > 0 else src[i:]


def main():
    if not os.path.isfile(SRC):
        print("✗ 找不到文件：" + SRC)
        return 1
    src = open(SRC, encoding="utf-8", errors="replace").read()
    printPdf = fn_body(src, "function printPdf()")
    fails = []

    def need(ok, code, msg, hint=""):
        if not ok:
            fails.append((code, msg, hint))

    # ---------- A. 甘特打印 ----------
    if not printPdf:
        need(False, "A0", "找不到 function printPdf()（甘特打印入口）")
    else:
        need("flex-direction:row !important" in printPdf, "A1",
             "甘特打印 CSS 缺少 flex-direction:row !important",
             "窄纸打印会命中模板的 @media (max-width:1000px){.layout{flex-direction:column}}，把左表与横道图拆成上下两半")
        need("width:var(--tbl-w,470px) !important" in printPdf, "A2",
             "甘特打印缺少左表固定宽度 width:var(--tbl-w,470px) !important",
             "改成 auto 会把右侧横道图挤成 0 宽 → 打印时看不见")
        need("max-width:1120px" in printPdf and "max-width:800px" in printPdf, "A3",
             "甘特打印缺少按纸张宽度分档的缩放分支（max-width:1120px / max-width:800px）",
             "否则 A4 纸张会装不下 / 装得下但被裁切")
        need(".cards-wrap,#cardsWrap" in printPdf, "A4",
             "甘特打印未排除下方卡片 .cards-wrap/#cardsWrap",
             "窄纸下它们会被挤出一张几乎空白的第 2 页")
        bad_break = re.search(r"break-before:page|page-break-before:always", printPdf)
        need(bad_break is None, "A5",
             "甘特打印里出现强制分页（break-before:page / page-break-before:always）",
             "会把甘特整块顶到第 2 页，第 1 页只剩标题")
        need(re.search(r"totalH\s*=\s*offTop\s*\+", printPdf), "A6",
             "甘特缩放的 totalH 未把版面顶部内容(offTop)算进去",
             "甘特会被顶到第 2 页")
        need("@page{size:A3 landscape" in printPdf, "A7",
             "甘特打印缺少 @page{size:A3 landscape;margin:6mm}")

    # 前提：模板里的移动端规则必须仍然存在，A1 的覆盖才有意义
    need(re.search(r"@media \(max-width:1000px\)\{\s*\.layout\{height:auto;flex-direction:column\}", src),
         "A8", "找不到模板里的移动端规则 @media (max-width:1000px){.layout{flex-direction:column}}",
         "若已删除请同步删除本检查；若被改写，A1 的覆盖规则需要重新评估")

    # ---------- B. 智能报告打印 ----------
    need(re.search(r"\.print-target \.modal,\s*\n?\s*body > \.modal-overlay\.show \.modal\{[^}]*display:block", src),
         "B1", "智能报告打印未把 .modal 改成 display:block",
         ".modal 是 display:flex;flex-direction:column，flex 容器分页会把正文整块推到第 2 页（标题栏独占一页）")
    need("body > .modal-overlay.show{display:block !important;}" in src, "B2",
         "缺少 body > .modal-overlay.show 兜底打印目标",
         "Edge 打印预览是异步快照，标记一丢整页就会被 body>*{display:none} 隐藏 → 打印空白")
    need("body > .modal-overlay.show #slatsReportBody" in src, "B3",
         "缺少对 #slatsReportBody 的兜底解裁剪规则（body > .modal-overlay.show #slatsReportBody）",
         "只解除 .print-target 的话，兜底路径会被 max-height:65vh 裁成一页")
    need("break-inside:auto !important;page-break-inside:auto !important" in src, "B4",
         "智能报告段落缺少 break-inside:auto（超高段落会被整段推到下一页，页尾留大片空白）")

    # ---------- C. 打印标记生命周期 ----------
    for pat, code, msg in (
        (r"classList\.remove\('print-target'\);\s*\},\s*300\)", "C1a", "仍有 print() 之后 300ms 摘 .print-target 的写法"),
        (r"classList\.remove\('printing-dashboard'\);\s*\},\s*300\)", "C1b", "仍有 print() 之后 300ms 摘 .printing-dashboard 的写法"),
    ):
        need(re.search(pat, src) is None, code, msg, "打印是异步的：Edge 抓 DOM 更慢，摘早了打印会空白 / 内容残缺")
    need(re.search(r"function __clearPrintTarget\s*\(", src) is not None, "C2",
         "缺少 __clearPrintTarget() 延迟清理函数")
    need(re.search(r"function __lazyClearPrintTarget\s*\(", src) is not None, "C2a",
         "缺少 __lazyClearPrintTarget() 延迟清理函数")
    need(re.search(r"setTimeout\(\s*__lazyClearPrintTarget", src) is not None, "C2b",
         "printModalById / prodReportPrint 没有接上延迟清理（setTimeout(__lazyClearPrintTarget, …)）",
         "打印结束后必须保留打印标记一段时间，否则 Edge 预览会空白")
    need(re.search(r"function printModalById\s*\(", src) is not None, "C2c", "缺少 function printModalById()")
    need(re.search(r"function printDashboard\s*\(", src) is not None, "C2d", "缺少 function printDashboard()")
    need("'<script>(function(){'" not in src, "C3",
         "JS 字符串里出现字面 '<script>(function(){'",
         "会被 HTML 解析器当成真标签切断脚本块 → printModalById / printDashboard 等全部未定义")
    need("'<scr' + 'ipt>" in src, "C3b", "缺少拆分写法 '<scr' + 'ipt>（脚本块拼接必须拆开标签名）")

    # ---------- 输出 ----------
    if not fails:
        print("✓ 打印逻辑锁定契约通过：" + os.path.basename(SRC))
        print("   A 甘特打印（左右两栏 / 一页装下）· B 智能报告打印（块级流 / 兜底目标）· C 打印标记生命周期")
        return 0

    print("✗ 打印逻辑锁定契约被破坏，共 %d 处：" % len(fails))
    for code, msg, hint in fails:
        print("  [%s] %s" % (code, msg))
        if hint:
            print("        → " + hint)
    print("\n修复方式：见 choice_lite.html 中 [FROZEN 契约 · 打印] 注释；"
          "\n导出/打印相关改动请保持本契约，否则 pre-commit 会拦截提交。")
    return 1


if __name__ == "__main__":
    sys.exit(main())
