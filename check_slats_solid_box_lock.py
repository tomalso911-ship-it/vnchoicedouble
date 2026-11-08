#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""硬锁：实心板?=YES 的水泥漏缝地板规格「双线黑框」契约（SLATS-SOLID-BOX-20261108）。

背景（用户 2026-11-08 需求）：
  规格表里「实心板?」选 YES 的那些水泥漏缝地板尺寸，全站所有表格/弹窗/打印/导出
  都要把这个尺寸外面加上 Excel 式双线黑框；同尺寸多行时【只看这一行】。

本脚本静态扫描，任何一条不变量被改坏 → 退出码 1，pre-commit 直接拦截。

运行：python check_slats_solid_box_lock.py
"""
from __future__ import annotations

import sys
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent
HTML = ROOT / "choice_lite.html"
APP = ROOT / "app.py"

problems: list[str] = []


def need(text: str, needle: str, label: str) -> None:
    if needle not in text:
        problems.append("%s —— 缺少: %r" % (label, needle[:90]))


def deny(text: str, needle: str, label: str) -> None:
    if needle in text:
        problems.append("%s —— 不应出现: %r" % (label, needle[:90]))


def main() -> int:
    if not HTML.is_file():
        print("[slats-solid-box-lock] 找不到 choice_lite.html")
        return 1
    html = HTML.read_text(encoding="utf-8", errors="replace")
    app = APP.read_text(encoding="utf-8", errors="replace") if APP.is_file() else ""

    # ① 判定必须来自 concrete_floor_spec 的 solid_slat，且只认 YES
    need(html, "function slatsRowSolidYes(r){",
         "① 行级判定 slatsRowSolidYes 被删")
    need(html, "String(r.solid_slat||'').trim().toUpperCase()==='YES'",
         "① solid_slat 判定口径被改（必须 trim + 大写 + 等于 YES）")

    # ② 尺寸归一化只能按乘号切分（千分位逗号不是分隔符）
    need(html, "function slatsSizeKeyNumeric(s){",
         "② 尺寸归一化 slatsSizeKeyNumeric 被删")
    need(html, ".split(/[×xX*]+/)",
         "② 归一化必须只按乘号切分")
    deny(html, "[×xX*,，\\s]+",
         "② 归一化把逗号/空格当分隔符（会把 1,550×525×70 拆成 1×550×525×70）")
    need(html, ".replace(/[,\\s，]/g,'')",
         "② 归一化必须剥掉千分位逗号与空格")

    # ③ 尺寸级判定：任一行 YES 即 true（不能改成"最后一行说了算"）
    need(html, "function slatsSizeSolidMap(){",
         "③ 尺寸级判定 slatsSizeSolidMap 被删")
    need(html, "if(!slatsRowSolidYes(r)) return;",
         "③ slatsSizeSolidMap 必须逐行调用 slatsRowSolidYes")
    need(html, "map[k] = 1;",
         "③ slatsSizeSolidMap 必须把 YES 尺寸记进 map")
    need(html, "function slatsSizeSolidYes(s){",
         "③ slatsSizeSolidYes 被删")

    # ④ 生产矩阵给每个规格挂 solidYes（全线表格共用这一份判定）
    need(html, "specs[_sk].solidYes = !!_solidMap[slatsSizeKeyNumeric(_sk)];",
         "④ prod_slatsMatrix 必须在规格上挂 solidYes")

    # ⑤ 样式：黄色 2px 单线框（用户 2026-11-08 修正：紧贴文字、黄色、加粗，不要双线）
    need(html, ".slats-solid-cell.slats-solid-cell{border:2px solid #FFC400 !important;}",
         "⑤ 拆分三格的黄框样式被删/被改色")
    need(html, ".slats-solid-box{border:2px solid #FFC400;",
         "⑤ 文字黄框样式被删/被改色")
    need(html, "@media print",
         "⑤ 打印样式缺失")
    need(html, "body > .modal-overlay.show .slats-solid-box{border:2px solid #FFC400 !important;}",
         "⑤ 打印时黄框必须保留")
    deny(html, "3px double #000",
         "⑤ 又用回黑色双线框（用户明确不要双线）")

    # ⑥ 规格当列头的表：表头由通用补框器包黄框（元素级），渲染里不再加 cell class
    need(html, "var els = root.querySelectorAll('td,th,b,strong');",
         "⑥ 通用补框器的元素级包框逻辑被删（表头/带 ▸ 的规格会漏框）")

    # ⑦ 规格编辑弹窗：行级，只框 8/9/10（长/宽/高 mm），不能框 4/5/6（房舍尺寸，带 rowspan）
    need(html, "var _solidBoxOci = [8, 9, 10];",
         "⑦ 规格弹窗加框列被改（必须是 8/9/10）")
    deny(html, "var _solidBoxOci = [4, 5, 6, 8, 9, 10];",
         "⑦ 规格弹窗又框了 4/5/6（那是房舍长宽高，不是地板尺寸）")
    need(html, "btd.classList.remove('slats-solid-cell');",
         "⑦ YES→NO 必须能把框摘掉")

    # ⑧ 智能报告：YES 行框住该行「长/宽/高」
    need(html, "var _solidSegCls = function(seg){",
         "⑧ 智能报告没有按行加框")
    need(html, "_solidSegCls('start')", "⑧ 智能报告长/宽/高没有拼成整框")

    # ⑨ 通用补框器 & 渲染钩子（少一处就会出现"某些表格没框"）
    need(html, "function slatsSolidSweep(root){",
         "⑨ 通用补框器 slatsSolidSweep 被删")
    need(html, "function slatsSolidBoxBoot(){",
         "⑨ MutationObserver 启动器被删")
    need(html, "mo.observe(document.body, { childList:true, subtree:true });",
         "⑨ 全局观察器被删（弹窗/审批等动态内容会漏框）")
    for anchor, label in (
        ("slatsSolidNow(body);", "⑨ prod_renderTab 渲染后补框被删"),
        ("if(bodyEl && typeof slatsSolidNow==='function')", "⑨ 出库/入库弹窗补框被删"),
        ("slatsSolidNow(tb);", "⑨ 规格表重绘后补框被删"),
        ("slatsSolidNow(el('slatsReportOverview'));", "⑨ 智能报告概述表补框被删"),
        ("slatsSolidNow(modal);", "⑨ 智能报告整个弹窗（规格分布/材料分布）补框被删"),
    ):
        need(html, anchor, label)
    if html.count("slatsSolidNow(") < 6:
        problems.append("⑨ slatsSolidNow 调用点少于 6 处（覆盖不全）")

    # ⑩ 导出 xlsx：前端按钮 + 三语 key + 后端黄色加粗边框
    need(html, "function exportSlatsSpecXlsx(){", "⑩ 导出函数被删")
    need(html, "onclick=\"exportSlatsSpecXlsx()\"", "⑩ 导出按钮被删")
    if html.count("slats_btn_export") < 4:
        problems.append("⑩ slats_btn_export 三语 key 不足（应有 按钮+zh/en/vi 共 4 处）")
    need(app, '@app.route("/api/slats-spec-export", methods=["POST"])',
         "⑩ 后端导出路由被删")
    need(app, 'color="FFFFC400"', "⑩ 后端必须用黄色边框（#FFC400）")
    need(app, "box_yes", "⑩ 后端黄色粗边框对象被删")

    if problems:
        print("[slats-solid-box-lock] ✗ 失败 %d 项：" % len(problems))
        for p in problems:
            print("   -", p)
        return 1
    print("[slats-solid-box-lock] ✓ OK · 实心板 YES 黄色加粗框契约完整")
    return 0


if __name__ == "__main__":
    sys.exit(main())
