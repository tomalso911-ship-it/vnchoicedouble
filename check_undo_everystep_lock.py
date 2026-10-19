# -*- coding: utf-8 -*-
"""硬锁：撤销账本必须"每一步动作都可撤销" + 带格式粘贴必须换行归一化。

FIN-UNDO-EVERYSTEP-20261018（用户 2026-10-18：「要求每一步动作都可以撤回，
而不是输入数值才可以撤回」）
CLIP-TEXT-NORM-20261018（用户 2026-10-18：「粘贴的时候没有把背后的格式全部复制过去」）

任何一条被删/退化 → 退出码 1（pre-commit / pre-push 会拦下）。
"""
import io
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

BASE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(BASE, "choice_lite.html")

fails = []


def chk(cond, msg):
    print(("  OK  " if cond else "  ✗   ") + msg)
    if not cond:
        fails.append(msg)


def main():
    path = TARGET
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        path = sys.argv[1]
    with io.open(path, "r", encoding="utf-8", errors="replace") as f:
        src = f.read()
    print("检查目标:", path)

    print("1) 撤销账本：排除法（不是白名单）")
    chk("FIN-UNDO-EVERYSTEP-20261018" in src, "标记 FIN-UNDO-EVERYSTEP-20261018 在")
    chk("if (id.indexOf('sheet.command.') !== 0) return;" in src,
        "只按前缀接收 sheet.command.* （不再逐条枚举命令名）")
    chk("FIN_UNDO_SKIP_UI.test(id)" in src, "纯界面命令黑名单在生效")
    chk("FIN_UNDO_SKIP_STRUCT.test(id)" in src, "结构类命令黑名单在生效（防错位回滚）")

    print("2) 结构类必须排除（快照式回滚会写错格子）")
    _lines = [l for l in src.splitlines() if l.strip().startswith("var FIN_UNDO_SKIP_STRUCT")]
    seg = _lines[0] if _lines else ""
    for kw in ("insert-row", "delete-row", "insert-column", "delete-column",
               "move-rows", "move-columns", "set-range-merged"):
        chk(kw in seg, "黑名单包含 %s" % kw)

    print("3) 样式/格式类命令不得再被白名单挡住")
    chk("numfmt" not in seg, "numfmt 没被结构黑名单误伤（应可撤销）")
    chk("set-style" not in seg, "set-style 没被黑名单误伤（对齐/字号都走它）")
    chk("set-border" not in seg, "set-border 没被黑名单误伤")
    chk("set-range-values" not in seg, "set-range-values 没被黑名单误伤（值/样式主通道）")

    print("4) 账本录制条件仍在")
    chk("if (finUndoProg > 0) return;" in src, "程序写入不记账（finUndoProg 门）")
    chk("(Date.now() - (finLastUserInputAt || 0)) > 2500" in src, "只记真实用户动作（2500ms 窗口）")
    chk("（B && B.snap）" not in src and "pend.push({ id: id" in src, "记账走 pend 队列（嵌套命令只记一步）")

    print("5) 带格式粘贴：换行归一化（\\r\\n 是根因）")
    chk("CLIP-TEXT-NORM-20261018" in src, "标记 CLIP-TEXT-NORM-20261018 在")
    chk("function normText(s)" in src, "normText 归一化函数在")
    chk("replace(/\\r\\n?/g, '\\n')" in src, "归一化把 \\r\\n 统一成 \\n")
    chk("window.clipNormText" in src, "clipNormText 暴露给两套适配器")
    _rich = src.split("CLIP-RICH-20261018")
    chk(len(_rich) >= 3, "财务/权益两套 rich 通道都在")
    chk("_nt(M.text) !== _nt(text)" in src, "财务 rich 用归一化比较（不是严格相等）")
    chk("_nt2(M.text) !== _nt2(text)" in src, "权益 rich 用归一化比较（不是严格相等）")
    chk("String(M.text) !== String(text)" not in src, "禁止退回严格字符串比较（多行必失配）")

    print("6) 跨模块镜像（财务↔权益粘贴也能带格式）")
    chk("CLIP-RICH-XMODULE-20261018" in src, "标记 CLIP-RICH-XMODULE-20261018 在")
    chk("window.__clipRichGlobal = window.__finClipMirror;" in src, "财务写全局镜像")
    chk("window.__clipRichGlobal = window.__eqClipMirror;" in src, "权益写全局镜像")
    chk(src.count("window.__clipRichGlobal && window.__clipRichGlobal.mat") >= 2,
        "两套 rich 都能回退到全局镜像")

    print("7) 撤销写回：范围取最宽 + 空格子三键全 null")
    chk("FIN-UNDO-WIDEST-20261018" in src, "标记 FIN-UNDO-WIDEST-20261018 在")
    chk("function fin_undoSnapCells(sn)" in src, "快照覆盖格数计算函数在")
    chk("if (_n > bestN){ bestN = _n; snap = pend[si].snap; }" in src,
        "记账取【覆盖格数最多】的快照（不是队首那份 1 格的）")
    chk("FIN-UNDO-NULLCLEAR-20261018" in src, "标记 FIN-UNDO-NULLCLEAR-20261018 在")
    chk("oc = { v: null, t: null, f: null };" in src,
        "空格子写回用 v/t/f 三键全 null（实测唯一能真清空的写法）")
    chk("oc = { v: '', t: 1 };" not in src,
        "禁止退回 {v:'',t:1}（只会留空串，快照里 v 由 null 变 ''）")
    chk("FIN-UNDO-AFTERDELAY-20261018" in src, "标记 FIN-UNDO-AFTERDELAY-20261018 在")
    chk("}, 120);" in src, "记账推迟 120ms（让 after 抓到铺完样式的最终态，恢复才有格式）")
    chk("FIN-UNDO-PASTEDIM-20261018" in src, "标记 FIN-UNDO-PASTEDIM-20261018 在")
    chk("function fin_undoPasteDim(p)" in src, "粘贴区行列数推导函数在（原生粘贴只发 mutation，params 无 range）")
    chk(src.count("fin_undoPasteDim(p)") >= 2, "pre 快照与常规快照两条路径都做了扩展")

    print("")
    if fails:
        print("✗ 失败 %d 项：" % len(fails))
        for f in fails:
            print("   -", f)
        return 1
    print("✓ 通过：每一步动作可撤销 + 带格式粘贴换行归一化（FIN-UNDO-EVERYSTEP / CLIP-TEXT-NORM-20261018）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
