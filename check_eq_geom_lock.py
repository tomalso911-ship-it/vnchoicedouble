#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
股东权益「列宽 / 行高自由调整 + 永不回弹」+「权益版 bufferWhen 爆栈防护」锁死检查。
（lint / CI / git pre-commit 均可用）

契约编号：
  EQ-GEOM-KEEP-20261018 / EQ-GEOM-STORE-20261018
  FIN-FORMULA-STACK-20261018（权益那套独立 Univer 也必须装同一份补丁）

用户原话：
  2026-10-18「股东结构表格，必须允许我自由调整列宽，和行距！不用改变其他的！」
  2026-10-18 追问后确认症状：「能拖，但过后变回去」
  2026-10-18「Uncaught RangeError: Maximum call stack size exceeded ... bufferWhen」

不变量（缺一条，两个 BUG 之一就会复发）：
  ① render() 的第一步必须 eqCaptureGeomToSnap()（重建前抓版面），
     且必须在 api.disposeUnit('equity-report') 之前；
  ② buildView() 之后、createUnit 之前必须 eqApplyGeomStore(v)（把本机版面盖回待建视图）；
  ③ 版面记录键必须仍是 localStorage 'eq_geom_v1'；
  ④ eqApplyGeomStore 只允许写 columnData[...].w / rowData[...].h，
     ★绝不许碰 cellData（碰了就是「重建把数据洗掉」）；
  ⑤ eqCaptureGeomToSnap 必须把活表的 w / h 记进本机记录（rec.c / rec.r），
     ★只记 h，不许记 hd（查报表隐藏行标记）；
  ⑥ bindChange 必须在列宽/行高相关命令上触发记账（否则拖完立刻 F5 会丢）；
  ⑦ eqUnitAlive 必须在 disposeUnit 之后置 false、createUnit 之后置 true
     （否则会去读已销毁单元的版面）；
  ⑧ 权益模块（含 equity_container 的 <script type="module">）在自己的 createUniver
     之前必须 await window.fin_ensureFormulaPatch()；
  ⑨ 财务脚本必须把 fin_patchFormulaService 缓存的模块暴露成 window.__finFormulaMods，
     并提供幂等的 window.fin_ensureFormulaPatch；
  ⑩ 补丁核心 skip(1) 不得被删（删掉即 bufferWhen 同步无限重入 → 栈溢出）。

用法：
  python3 check_eq_geom_lock.py [choice_lite.html]
  不传路径时默认检查同目录下的 choice_lite.html。
退出码：0 = 通过；1 = 契约被破坏（CI 失败 / pre-commit 拦截）。
"""
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

DOC_GEOM = "EQ-GEOM-KEEP-20261018"
DOC_STORE = "EQ-GEOM-STORE-20261018"
DOC_FORMULA = "FIN-FORMULA-STACK-20261018"
GEOM_KEY = "eq_geom_v1"


def fn_body(text, name):
    """取出 `function <name>(...)` 的函数体（含花括号配对），找不到返回 None。"""
    m = re.search(r"function\s+" + re.escape(name) + r"\s*\(", text)
    if not m:
        return None
    fb = text.find("{", m.end())
    if fb < 0:
        return None
    depth = 0
    i = fb
    while i < len(text):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[fb:i + 1]
        i += 1
    return text[fb:]


def equity_block(text):
    """取出含 equity_container 的那个 <script type="module"> ... </script> 正文。"""
    for m in re.finditer(r"^\s*<script type=\"module\">\s*$", text, re.M):
        s = m.start()
        e = text.find("</script>", s)
        if e > s and "equity_container" in text[s:e]:
            return text[s:e]
    return None


def check(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    errors = []

    # ---- 0) 锁标记 ----
    for doc in (DOC_GEOM, DOC_STORE, DOC_FORMULA):
        if doc not in text:
            errors.append("找不到锁标记 %s（锁死区注释被删除？）" % doc)

    # ---- ③ 本机版面记录键 ----
    if not re.search(r"var\s+EQ_GEOM_KEY\s*=\s*['\"]%s['\"]" % re.escape(GEOM_KEY), text):
        errors.append("③ 找不到 var EQ_GEOM_KEY = '%s'（本机版面记录的键被改/被删）" % GEOM_KEY)

    # ---- ④ eqApplyGeomStore 只写 w / h ----
    ap = fn_body(text, "eqApplyGeomStore")
    if ap is None:
        errors.append("④ 找不到 eqApplyGeomStore（建表前套回版面的函数被删除？）")
    else:
        if ".w = w" not in ap.replace(" ", " "):
            if not re.search(r"\.w\s*=\s*w\s*;", ap):
                errors.append("④ eqApplyGeomStore 不再写列宽（.w = w 缺失）")
        if not re.search(r"\.h\s*=\s*h\s*;", ap):
            errors.append("④ eqApplyGeomStore 不再写行高（.h = h 缺失）")
        if "cellData" in ap:
            errors.append("④ eqApplyGeomStore 里出现了 cellData —— ★版面函数绝不许碰单元格数据")

    # ---- ⑤ eqCaptureGeomToSnap 记账 ----
    cap = fn_body(text, "eqCaptureGeomToSnap")
    if cap is None:
        errors.append("① 找不到 eqCaptureGeomToSnap（重建前抓版面的函数被删除？）")
    else:
        if not re.search(r"rec\.c\s*\[\s*ck\s*\]\s*=\s*cd\.w", cap):
            errors.append("⑤ eqCaptureGeomToSnap 不再把列宽记进本机记录（rec.c[ck] = cd.w 缺失）")
        if not re.search(r"rec\.r\s*\[\s*rk\s*\]\s*=\s*rd\.h", cap):
            errors.append("⑤ eqCaptureGeomToSnap 不再把行高记进本机记录（rec.r[rk] = rd.h 缺失）")
        if not re.search(r"eqGeomSaveSoon\s*\(\s*\)", cap):
            errors.append("⑤ eqCaptureGeomToSnap 不再落 localStorage（eqGeomSaveSoon() 缺失）")
        if "dst.cellData" in cap or "cellData =" in cap:
            errors.append("⑤ eqCaptureGeomToSnap 里出现了 cellData 赋值 —— ★只许搬版面")
        if not re.search(r"typeof\s+rd\.h\s*!==\s*'number'\)\s*return", cap):
            errors.append("⑤ eqCaptureGeomToSnap 搬 rowData 时必须只挑 h（hd 隐藏标记绝不许搬）")

    # ---- ① / ② / ⑦ render() 内的顺序 ----
    rd = fn_body(text, "render")
    if rd is None:
        errors.append("找不到 render()（股东权益建表函数被删除？）")
    else:
        i_cap = rd.find("eqCaptureGeomToSnap()")
        i_apply = rd.find("eqApplyGeomStore(v)")
        i_build = rd.find("buildView()")
        i_dispose = rd.find("disposeUnit('equity-report')")
        i_create = rd.find("createUnit(")
        if i_cap < 0:
            errors.append("① render() 里没有 eqCaptureGeomToSnap()（重建前不抓版面 → 拖完会回弹）")
        if i_apply < 0:
            errors.append("② render() 里没有 eqApplyGeomStore(v)（建表前不套回版面 → 拖完会回弹）")
        if i_build < 0:
            errors.append("render() 里找不到 buildView()（建表流程被改？）")
        if i_dispose < 0:
            errors.append("render() 里找不到 disposeUnit('equity-report')（单元销毁被改？）")
        if i_create < 0:
            errors.append("render() 里找不到 createUnit(（建表调用被改？）")
        if i_cap >= 0 and i_dispose >= 0 and not (i_cap < i_dispose):
            errors.append("① eqCaptureGeomToSnap() 必须在 disposeUnit 之前（晚于销毁就读不到版面了）")
        if i_apply >= 0 and i_build >= 0 and not (i_build < i_apply):
            errors.append("② eqApplyGeomStore(v) 必须在 buildView() 之后（否则被 buildView 覆盖）")
        if i_apply >= 0 and i_create >= 0 and not (i_apply < i_create):
            errors.append("② eqApplyGeomStore(v) 必须在 createUnit 之前（晚于建表就不生效）")
        if not re.search(r"eqUnitAlive\s*=\s*false\s*;", rd):
            errors.append("⑦ 销毁旧单元后必须 eqUnitAlive = false（否则去读已销毁单元的版面）")
        if not re.search(r"eqUnitAlive\s*=\s*true\s*;", rd):
            errors.append("⑦ 新建单元后必须 eqUnitAlive = true")
        if rd.find("eqUnitAlive = false") > rd.find("eqUnitAlive = true") >= 0:
            errors.append("⑦ eqUnitAlive 的 false / true 顺序反了（应先 false 后 true）")

    # ---- ⑥ bindChange 记账 ----
    bc = fn_body(text, "bindChange")
    if bc is None:
        errors.append("找不到 bindChange()（自动保存的改动监听被删除？）")
    elif "worksheet-col-width" not in bc or "worksheet-row-height" not in bc:
        errors.append("⑥ bindChange 不再监听 set-worksheet-col-width / set-worksheet-row-height"
                      "（拖完立刻刷新会丢版面）")
    elif "eqCaptureGeomToSnap()" not in bc:
        errors.append("⑥ bindChange 命中列宽/行高命令后没有记账（eqCaptureGeomToSnap() 缺失）")

    # ---- ⑧ 权益模块自己的 createUniver 前必须装补丁 ----
    eqb = equity_block(text)
    if eqb is None:
        errors.append("找不到股东权益模块（含 equity_container 的 <script type=\"module\">）")
    else:
        i_ensure = eqb.find("await window.fin_ensureFormulaPatch()")
        i_cu = eqb.find("createUniver(")
        if i_ensure < 0:
            errors.append("⑧ 权益 init() 里没有 await window.fin_ensureFormulaPatch()"
                          "（先开权益页时 bufferWhen 仍会爆栈）")
        if i_cu < 0:
            errors.append("⑧ 权益模块里找不到 createUniver(（结构被改？）")
        if i_ensure >= 0 and i_cu >= 0 and not (i_ensure < i_cu):
            errors.append("⑧ 装补丁必须在权益自己的 createUniver 之前（晚了就来不及）")

    # ---- ⑨ 财务侧暴露幂等入口 ----
    if not re.search(r"window\.__finFormulaMods\s*=\s*\{\s*f\s*:\s*formulaMod\s*,\s*r\s*:\s*rxMod\s*\}", text):
        errors.append("⑨ fin_patchFormulaService 必须缓存模块引用 window.__finFormulaMods = { f, r }")
    if not re.search(r"window\.fin_ensureFormulaPatch\s*=\s*function", text):
        errors.append("⑨ 必须暴露幂等的 window.fin_ensureFormulaPatch（权益模块靠它装补丁）")

    # ---- ⑩ skip(1) 核心行 ----
    if not re.search(r"rxMod\.skip\(1\)", text):
        errors.append("⑩ 找不到 rxMod.skip(1) —— bufferWhen 的同步回放没被掐掉，爆栈会复发")

    return errors


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "choice_lite.html")
    if not os.path.isfile(path):
        print("✗ 找不到文件：%s" % path)
        return 2
    errors = check(path)
    if errors:
        print("✗ %s 未通过（%s / %s / %s）" % (os.path.basename(path), DOC_GEOM, DOC_STORE, DOC_FORMULA))
        for e in errors:
            print("   - " + e)
        return 1
    print("✓ %s：列宽/行高版面锁 + 权益版 bufferWhen 防护 全部通过" % os.path.basename(path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
