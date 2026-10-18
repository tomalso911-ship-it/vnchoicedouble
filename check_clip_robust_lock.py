# -*- coding: utf-8 -*-
"""硬锁自检：财务/股东权益 Ctrl+C / Ctrl+X / Ctrl+V —— 新架构（CLIP-ENGINE-20261018）。

背景（用户 2026-10-18：「Ctrl+X/C/V 又没了，整套重写！」）：
  · 局域网 http（非安全上下文）下 navigator.clipboard 不可用 → Univer 的粘贴读不到剪贴板；
  · document.execCommand('copy') 在部分机器上「假成功」；
  · 过去两张表各写一套补丁，改好一张另一张又坏。
  ⇒ 现在只有【一个全局引擎】，两张表只注册适配器（text / write / clear / el）。

契约（任何重构不得删改，失败即 exit 1）：
  ① window.__clipEngine 必须提供 register / handleKey / write / parse / paste；
  ② 复制：execCommand('copy') + copy/cut 事件里 clipboardData.setData 双通道；
  ③ 粘贴：自己接管 paste 事件，从 e.clipboardData.getData('text/plain') 读 →
     preventDefault 掉 Univer 的坏路径 → 用自己的适配器 write 写回表格；
  ④ 两张表都必须注册适配器并置 __clipEvtFin / __clipEvtEq；
  ⑤ 粘贴写单元格必须走 setValues（fin_clipPasteText / eq_clipPasteText）；
  ⑥ C/X/V 键盘补丁分支内不得 preventDefault / stopPropagation；
  ⑦ 复制内容必须是屏幕文本（win_fmtNum + numfmt pattern）；
  ⑧ 3 秒自检必须同时断言 win_clipWrite / eq_clipMatrixText / 两条适配器通道；
  ⑨ 浮层稳定器（POPUP-STABLE-20261018）必须：逐帧采样、只认「更高」的一帧、用 !important 钉死。
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
    print(("  \u2713 " if cond else "  \u2717 ") + msg)
    if not cond:
        ok = False


def cnt(s):
    return src.count(s)


print("1) 全局引擎（唯一一套剪贴板逻辑）")
chk("window.__clipEngine = {" in src, "window.__clipEngine 已定义")
for api in ("register: register", "handleKey: handleKey", "write: writeClipboard",
            "parse: matrixOf", "paste: function"):
    chk(api in src, "引擎导出 %s" % api)

print("2) 复制：同步 execCommand + copy/cut 事件双通道")
chk("ok = document.execCommand('copy');" in src, "execCommand('copy') 仍在（同步通道，代码不是注释）")
chk(cnt("document.addEventListener('copy', onCopyCut, true);") == 1, "copy 事件通道已注册")
chk(cnt("document.addEventListener('cut', onCopyCut, true);") == 1, "cut 事件通道已注册")
chk("e.clipboardData.setData('text/plain', pending);" in src, "事件通道用 setData 落盘")
chk("left:-99999px" not in src, "隐藏 textarea 不得放到 -99999px（会假成功写空）")
chk("var ok = writeClipboard(text);" in src, "复制必须真正写入剪贴板（writeClipboard 调用在）")
chk("try { if (prev && prev.focus) prev.focus({ preventScroll: true }); } catch (e) {}" in src,
    "写剪贴板后必须把焦点还给原元素（否则后续按键全打到隐藏 textarea）")

print("3) 粘贴：自己接管 paste 事件（绕开 navigator.clipboard）")
chk(cnt("document.addEventListener('paste', function (e) {") == 1, "paste 捕获监听已注册")
chk("e.clipboardData ? e.clipboardData.getData('text/plain')" in src, "从 clipboardData 读文本")
chk("applyPaste(o, txt);" in src, "读到内容后交给适配器写入")
# ★CLIP-COPY-EMPTY-20261018：clipboardData 为空时，仍必须用「本页最近复制的内容」兜底，
#   但要先区分「本页最近一次复制的确实是空内容」→ 按 Excel 语义清空目标，而不是粘回旧数据。
chk("else if (lastText) txt = lastText;" in src, "clipboardData 为空时用本页最近复制内容兜底")
chk("selfEmpty" in src, "空复制可粘贴清空目标（CLIP-COPY-EMPTY，不得粘回旧数据）")

print("4) 两张表注册适配器")
chk("window.__clipEngine.register('fin'" in src, "财务适配器已注册（fin）")
chk("window.__clipEngine.register('eq'" in src, "权益适配器已注册（eq）")
chk("window.__clipEvtFin = true;" in src, "财务接线标记 __clipEvtFin")
chk("window.__clipEvtEq = true;" in src, "权益接线标记 __clipEvtEq")
chk("forceName && tables[forceName]" in src, "键盘补丁可指定表格（避免抢到另一张表）")

print("5) 粘贴写单元格（自己的 setValues）")
for fn in ("fin_clipPasteText", "eq_clipPasteText"):
    chk(("function %s(text){" % fn) in src, "存在 %s" % fn)
chk(cnt(".setValues(m0);") == 2, "两处都用 setValues 写回（实际 %d）" % cnt(".setValues(m0);"))
chk("window.__clipEngine.parse(text)" in src or "window.__clipEngine.parse" in src,
    "粘贴文本经引擎 parse（TSV + 数值还原）")

print("6) C/X/V 放行（补丁不得拦截）")


def _code_calls(seg):
    bad = []
    for ln in seg.splitlines():
        s = ln.strip()
        if s.startswith("/*") or s.startswith("*") or s.startswith("//"):
            continue
        if "preventDefault(" in s or "stopPropagation(" in s:
            bad.append(s[:60])
    return bad


MARK = "\u2605\u7edd\u4e0d preventDefault"
i_fin = src.find("var finClipKey = (k === 'c' || k === 'C' || k === 'x' || k === 'X' || k === 'v' || k === 'V');")
chk(i_fin > 0, "财务 finClipKey 三键放行存在")
if i_fin > 0:
    seg = src[i_fin:i_fin + 1400]
    _j = seg.find(MARK)
    if _j > 0:
        seg = seg[:_j]
    _bf = _code_calls(seg)
    chk(not _bf, "财务放行分支内无 preventDefault / stopPropagation" + ("：" + " | ".join(_bf) if _bf else ""))
i_eq = src.find("(k === 'c' || k === 'C' || k === 'x' || k === 'X' || k === 'v' || k === 'V')) {")
chk(i_eq > 0, "权益三键放行分支存在")
if i_eq > 0:
    seg2 = src[i_eq:i_eq + 900]
    _j2 = seg2.find(MARK)
    if _j2 > 0:
        seg2 = seg2[:_j2]
    _be = _code_calls(seg2)
    chk(not _be, "权益放行分支内无 preventDefault / stopPropagation" + ("：" + " | ".join(_be) if _be else ""))

print("7) 复制内容 = 屏幕文本")
chk("window.win_fmtNum(_raw, _pat)" in src, "财务按 numfmt pattern 还原")
chk("window.win_fmtNum(v, _epat)" in src, "权益按 numfmt pattern 还原")

print("7b) 复制的「空内容」语义（CLIP-COPY-EMPTY-20261018）")
chk("if (text === null || text === undefined) return false;" in src,
    "text() 返回 null（无选区）才不接管；返回 ''（空白格）必须照常复制")
chk("if (pending === null || pending === undefined) return;" in src,
    "copy/cut 事件允许写空内容（否则剪贴板残留旧文本 → 粘出旧数据）")
chk("var text = null;" in src and "text = String(text);" in src,
    "复制文本先按 null 判定再转字符串（空白格也必须走复制，不得静默返回）")

print("8) 3 秒自检")
chk("'[clip-lock] OK" in src, "[clip-lock] OK 日志存在")
chk("window.__CLIP_LOCK_FAILED = true;" in src, "失败时置 __CLIP_LOCK_FAILED")
chk("var hasEvtF = !!window.__clipEvtFin, hasEvtE = !!window.__clipEvtEq;" in src,
    "自检断言两条适配器通道")
# ★CLIP-SELFCHECK-VIEW-20261018（用户 2026-10-18「又没了」的误报来源）：
#   财务适配器要等用户打开财务报表才注册，旧自检在加载 3 秒时无条件要求两张表都在
#   → 停留在看板/生产/权益页必然打出红字「剪贴板接线缺失 → Ctrl+C/X/V 会失效」，
#   用户看到就以为功能坏了。判据必须按【已初始化的视图】来。
chk("CLIP-SELFCHECK-VIEW-20261018" in src, "自检按已初始化视图判定（防误报红字）")
chk("(needFin && !hasEvtF)" in src and "(needEq && !hasEvtE)" in src,
    "缺失判据必须带 needFin/needEq 前置（不得无条件要求两张表）")
chk("(Date.now() - t0) < 20000" in src, "未初始化表的宽限期存在（不得加载即报错）")
chk("setInterval(clipSelfCheck" in src, "持续复查（表打开后也能发现真缺失）")

print("9) 浮层稳定器（POPUP-STABLE-20261018）")
chk("window.__POPUP_STABLE_VER" in src, "版本标记存在")
chk("if (r.height > rec.best.h + 0.5) {" in src, "只认「更高」的那一帧（内容完整的自然尺寸）")
chk("st.setProperty('height', h + 'px', 'important');" in src, "用 !important 钉死高度")
chk("st.setProperty('width', w + 'px', 'important');" in src, "用 !important 钉死宽度")
chk("st.setProperty('top', t + 'px', 'important');" in src, "钉死 top（防上下来回跳）")
chk("requestAnimationFrame(tick)" in src and "setInterval" not in src.split("POPUP-STABLE")[1][:4000],
    "逐帧 rAF 驱动（不再用 setInterval 轮询）")

print()
if ok:
    print("\u2713 通过：Ctrl+C / Ctrl+X / Ctrl+V 新引擎锁定契约未被破坏（CLIP-ENGINE-20261018）")
    sys.exit(0)
print("\u2717 失败：剪贴板锁定契约被破坏（见上）。这是「锁死」契约，禁止篡改；请恢复后再提交。")
sys.exit(1)
