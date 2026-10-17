# -*- coding: utf-8 -*-
"""硬锁自检：财务 / 股东权益 Univer 表格的「Excel 风格水平滚动条」（FIN-HSCROLL-LOCK-20261017）。

契约（用户 2026-10-17 定稿：能拖、跟手、不闪、表格真的跟着走，任何重构不得破坏）：

  ① 节点生命周期
     · window.makeHScroll 存在；滚动条用 id = 'fin-hscroll-' + containerId，靠
       document.getElementById 复用；节点必须 append 到 document.body
       （挂在表格容器里会被 Univer 重渲染清空 → "看着有、一拖就没"）。
  ② 驱动方式（唯一）
     · 必须用 FWorksheet.getScrollState() + FWorksheet.scrollToCell(row, col) 驱动；
       ★ scrollToCell 的第 1 个参数必须是当前 sheetViewStartRow，不能写 0
         （否则横向滚动会把纵向位置重置到第 1 行）。
     · ★ 禁止向 canvas 派发合成 WheelEvent：Univer 0.5.5 不处理合成滚轮，
       派发等于白做，还会和真滚动互相拉扯（历史 BUG：拖了不动 / 闪烁跳动）。
     · sheet.command.scroll-to-cell 只允许作为「拿不到 FWorksheet」的兜底，
       必须出现在 if (!ok ...) 之后，不得当主驱动（绝对定位会和增量互相拉扯）。
  ③ 滑块尺寸口径
     · visible 必须优先取 getVisibleRange()（endColumn - startColumn + 1），
       getColumnWidth 累加 / clientWidth÷73 只能作兜底（固定 73px 会算出
       visible >= total → 滑块撑满、可移动量为 0 → "拖不动"）。
  ④ 拖拽状态必须跨闭包共享
     · 状态存 bar.__hsState；几何量存 bar.__hsGeom；
       并把 __hsScroll / __hsSetFrac / __hsFrac 挂到 bar 上
       （本函数每 400ms 重入会新建闭包，函数内局部 var 会让 pointermove
        永远读到旧闭包 → "拖了完全不动"）。
  ⑤ 平滑（不闪、慢慢走）
     · 拖动必须用 requestAnimationFrame 合并（一帧最多滚一次）；
     · 目标列没变（bar.__hsLastCol === target）不得重复下命令；
     · layout() 必须比对 __hsPX/__hsPY，只在变化时写样式
       （400ms 轮询 + finFitHeight 同步改高度会让条子 1~2px 来回跳）；
     · 非拖拽态必须用 sheetViewStartColumn 反推滑块位置，且操作后 260ms 内不反推。
  ⑥ CSS
     · .fin-hscroll-thumb 必须有 left/width 过渡（慢慢行走）；
     · .fin-hscroll.fin-hs-drag .fin-hscroll-thumb 必须 transition:none（拖拽严格跟手）；
     · thumb.onpointerdown 必须有可移动量守卫（mv < 2 不进拖拽）并加 fin-hs-drag 类，
       endDrag 必须移除该类。
  ⑦ 拖拽自愈（FIN-HSCROLL-DRAGSAFE-20261017）
     · pointerup / pointercancel 必须用【捕获阶段】监听，并挂 blur / visibilitychange；
     · pointermove 里 e.buttons === 0（pointerup 丢了）时必须立即调用 bar.__hsEndDrag()；
       ★否则 dragging 永久为 true，之后每一次鼠标移动都会 preventDefault + 滚动表格，
         选区与焦点被打断，Ctrl+C / Ctrl+X / Ctrl+V 就"莫名其妙不能用"；
     · endDrag 必须把焦点还给 Univer 的 canvas（快捷键监听都绑在它上面）。

失败即 exit 1（已登记进 .githooks/pre-commit 与 .git/hooks/pre-commit 硬锁列表）。
"""
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


# ---------- 截取 makeHScroll 函数体 ----------
START = "window.makeHScroll = function("
END = "function fin_patchCommandService("
i0 = src.find(START)
i1 = src.find(END, i0) if i0 >= 0 else -1
chk(i0 >= 0, "window.makeHScroll 定义存在")
chk(i1 > i0, "能定位到 makeHScroll 函数体（其后紧跟 fin_patchCommandService）")
blk = src[i0:i1] if (i0 >= 0 and i1 > i0) else ""

print("1) 节点生命周期")
chk("var barId = 'fin-hscroll-' + containerId;" in blk, "barId = 'fin-hscroll-' + containerId")
chk("document.getElementById(barId)" in blk, "用 document.getElementById(barId) 复用节点")
chk("document.body.appendChild(bar)" in blk, "★节点 append 到 document.body（不被 Univer 清空）")
chk("bar.style.position = 'fixed'" in blk, "fixed 定位贴容器右下角")

print("2) 驱动方式：getScrollState + scrollToCell")
chk("sh2.getScrollState()" in blk, "调 FWorksheet.getScrollState() 读当前滚动状态")
chk("ss.sheetViewStartRow" in blk, "★从 getScrollState 取 sheetViewStartRow 作为纵向基准")
chk("sh2.scrollToCell(curRow, target)" in blk, "★用 scrollToCell(curRow, target) 驱动（带当前行，不重置纵向）")
chk("new WheelEvent" not in blk, "★绝不向 canvas 派发合成 WheelEvent（Univer 0.5.5 不认，且会互相拉扯）")
_i_cmd = blk.find("sheet.command.scroll-to-cell")
_i_fb = blk.find("if (!ok && a && typeof a.executeCommand")
chk(_i_cmd >= 0, "保留 sheet.command.scroll-to-cell 兜底通道")
chk(_i_fb >= 0 and _i_cmd > _i_fb, "★命令只出现在 if (!ok ...) 兜底分支之后，不得当主驱动")

print("3) 可滚范围口径")
chk("if (sh && typeof sh.getVisibleRange === 'function'){" in blk,
    "visible 优先取 getVisibleRange()（判定语句必须真实可达，不得写成 if (false)）")
chk("vr0.endColumn - vr0.startColumn + 1" in blk, "visible = endColumn - startColumn + 1")
chk("(total > 0) ? Math.min(1, visible / total) : 1" in blk, "滑块宽按 visible/total 比例")

print("4) 拖拽状态跨闭包共享")
chk("bar.__hsScroll = scrollToFrac" in blk, "__hsScroll 外置")
chk("bar.__hsSetFrac = setFrac" in blk, "__hsSetFrac 外置")
chk("bar.__hsFrac = getFrac" in blk, "__hsFrac 外置")
chk("bar.__hsState || (bar.__hsState =" in blk, "__hsState 状态外置（不得用函数内 var dragging）")
chk("bar.__hsGeom = { tw: tw, w: w, mv: maxX }" in blk, "__hsGeom 几何量外置")
chk("Math.abs(bar.__hsState" not in blk, "无异常的 __hsState 误用")
chk("var s = bar.__hsState" in blk, "pointermove 读 bar.__hsState")
chk("if (!bar.__hsGeom || bar.__hsGeom.mv < 2) return;" in blk, "★可移动量 < 2 不进入拖拽（内容未溢出）")

print("5) 平滑：rAF 合并 + 同列去重 + 定位防抖 + 反向同步")
chk("requestAnimationFrame(hsFlush)" in blk, "★拖动用 requestAnimationFrame 合并（一帧最多滚一次）")
chk("cancelAnimationFrame(hsRaf)" in blk, "松手时取消未执行帧")
chk("bar.__hsLastCol === target" in blk, "★目标列未变不重复下命令（避免每帧重排）")
chk("bar.__hsLaidOnce && bar.__hsPX === nx && bar.__hsPY === ny" in blk,
    "★layout() 只在坐标变化时写样式（防 1~2px 抖动）")
chk("'resize', relayout" in blk, "resize 时重新贴容器")
chk("'scroll', relayout, true" in blk, "页面滚动（捕获）时重新贴容器")
chk("ss5.sheetViewStartColumn" in blk, "★非拖拽时用 sheetViewStartColumn 反推滑块位置")
chk("Date.now() - (bar.__hsLastAct || 0) > 260" in blk, "操作后 260ms 内不反推（防状态未刷新把滑块拽回）")

print("6) CSS 过渡")
chk("transition:left .12s linear,width .12s linear;" in src, "★thumb 有 left/width 过渡（慢慢行走）")
chk(".fin-hscroll.fin-hs-drag .fin-hscroll-thumb{transition:none;}" in src,
    "★拖拽态 transition:none（严格跟手）")
chk("bar.classList.add('fin-hs-drag')" in blk, "pointerdown 加 fin-hs-drag 类")
chk("bar.classList.remove('fin-hs-drag')" in blk, "endDrag 移除 fin-hs-drag 类")

print("7) 拖拽自愈（否则 pointerup 丢失后每次移动鼠标都 preventDefault → 快捷键失效）")
chk("if (e.buttons === 0){ if (bar.__hsEndDrag) bar.__hsEndDrag(); return; }" in blk,
    "★pointermove 里按键已松开（buttons===0）必须立即收尾拖拽")
chk("bar.__hsEndDrag = endDrag" in blk, "endDrag 外置到 bar.__hsEndDrag（供自愈路径调用）")
chk("window.addEventListener('pointerup', endDrag, true)" in blk,
    "★pointerup 用【捕获阶段】（Univer 会 stopPropagation，冒泡阶段收不到）")
chk("window.addEventListener('pointercancel', endDrag, true)" in blk, "pointercancel 捕获阶段收尾")
chk("window.addEventListener('blur', endDrag)" in blk, "窗口失焦收尾")
chk("if (document.hidden) endDrag();" in blk, "标签页隐藏收尾")
chk("cvf.focus({ preventScroll: true })" in blk,
    "★拖拽结束把焦点还给 Univer canvas（复制/粘贴/快捷键监听都绑在 canvas 上）")

print("8) 接入点：财务报表 + 股东权益两处轮询都还在")
chk("window.makeHScroll('univer_container'" in src, "财务报表 #univer_container 已接入")
chk("window.makeHScroll('equity_container'" in src, "股东权益 #equity_container 已接入")

print()
print("总体:", "全部通过 ✓" if ok else "有失败 ✗")
sys.exit(0 if ok else 1)
