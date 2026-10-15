#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国财务报表「统计栏 + 保存不丢」锁死检查（lint / CI / git pre-commit 均可用）。

契约编号：FIN-CN-STAT-LOCK-20261013（见 choice_lite.html 中的 ★★锁死区★★ 注释，
         以及 app.py 中的 CN-BASIS-GUARD-20261013 / FIN-CN-ATOMIC-SAVE-20261013）

为什么需要这个硬锁（2026-10-13 用户连续发现的三类事故，逐条对应下面的不变量）：

  ① 统计栏取选区：这版 Univer 的 getSelection().getRanges() / getActiveRange()
     常常只返回"活动单元格"那一格 → 用户拉选一整段，统计栏仍显示「计数: 1」。
     必须改为从命令流 sheet.operation.set-selections（params.selections）里取【全部】选区，
     并以 fin_statSize(cmdSel) > fin_statSize(ranges) 为准（含 Ctrl 多选、换表作废）。
  ② 统计栏去重：Univer 的 selections 同时带着「整块选区 + 锚点单元格」（[[4,4,14,4],[4,4,4,4]]），
     不去重就会把锚点格算两次（实测 E5:E15 → 计数 12、总计多出 10,664）。
     必须逐格 seen[r,c] 去重（Excel 语义：每格只算一次）。
  ③ 挂起窗口内的改动【不得丢弃】：finCnMarkDirty 旧实现 `if (Date.now() < finCnHoldUntil) return;`
     直接把改动丢掉、窗口结束后也不补排 → 勾选核销/录入数字只把 finDirty 置真，永远没有定时器落盘。
     必须是 defer：finCnHoldTimer = setTimeout(… if (finDirty) finCnScheduleSave() …, wait + 60)。
     另需 finCnBindFlush 里的 2 秒看门狗兜底（有 dirty / 无定时器 / 窗口已过 → 补排一次）。
  ④ 保存是异步的（服务端 2~4 秒）：旧代码保存成功就无条件 finDirty = false，
     于是"保存已发出、响应未回来"期间的新改动被静默抹掉（界面显示已勾选、文件里没有）。
     必须有 finDirtyGen 代数：真实改动 +1，finCnSave 用 genAtBuild 比对，
     只有代数未变才清 dirty，否则 resaveNeeded → finally 里再排一次保存。
     另：finCnFlushBeacon 拿不到响应，禁止清 finDirty。
  ⑤ 服务端金额守卫（勿移除）：/api/finance/cn-report/save 落盘前用 _cn_block_total 比对
     ① 新基准块/旧基准块 < 0.02（÷3882 换算污染）② 新基准块/新中文块 < 0.5（三块必须同值）；
     命中就删 tmp、保留服务器文件、返回 HTTP 200 {ok, stale, guard:'currency-regression'}。
     （2026-10-13 这层守卫一度从代码里消失，被污染的保存直接落盘，
       把 41,400,000 写成 10,664.14 又写成 2.75 —— 必须锁死。）
  ⑥ 原子落盘：外观归一化 4 处不得再 wb.save(CN_REPORT)（就地截断重写，
     实测能被读到坏 zip），必须走 _cn_ws_save_atomic（.norm.tmp + os.replace）。
  ⑦ 前端三块对账（FIN-CN-TRI-CONSIST-20261013）：落盘 payload 上，数值格若基准块 ≠ 中文块
     则以中文块为准（_fx.v = _zv），让已被污染的基准块在下一次保存时自动修回。

用法：
  python3 check_fin_cn_lock.py [path/to/choice_lite.html] [path/to/app.py]
  不传路径时默认检查同目录下的 choice_lite.html 与 app.py。
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

DOC_ID = "FIN-CN-STAT-LOCK-20261013"


def fn_body(text, name):
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
    return None


def py_fn_body(text, name):
    m = re.search(r"def\s+" + re.escape(name) + r"\s*\(", text)
    if not m:
        return None
    # 取到下一个同级 def 或文件末尾（Python：按缩进判断，简化处理）
    tail = text[m.end():]
    nxt = re.search(r"\ndef\s+", tail)
    body = tail[:nxt.start()] if nxt else tail
    return body


def line_of(text, idx):
    return text.count("\n", 0, idx) + 1


def check_html(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    errors = []

    # ---- 0) 契约标记 ----
    if DOC_ID not in text:
        errors.append("找不到锁标记 %s（锁死区注释被删除？）" % DOC_ID)

    # ---- ① 命令流取选区 ----
    for pat, msg in (
        (r"var\s+finStatSel\s*=\s*null\s*;", "①缺 finStatSel（命令流选区缓存）"),
        (r"var\s+finStatSelSid\s*=\s*''\s*;", "①缺 finStatSelSid（换表作废判定）"),
    ):
        if not re.search(pat, text):
            errors.append(msg)
    scan = fn_body(text, "fin_statScanRanges")
    if scan is None:
        errors.append("①找不到 fin_statScanRanges（命令流选区解析器被删除）")
    else:
        if "typeof o.startRow === 'number'" not in scan:
            errors.append("①fin_statScanRanges 不再识别 {startRow,startColumn,endRow,endColumn} 对象形式")
        if "o.length === 4" not in scan:
            errors.append("①fin_statScanRanges 不再识别 [起行,起列,止行,止列] 四元数组形式")
    if fn_body(text, "fin_statSize") is None:
        errors.append("①找不到 fin_statSize（选区大小比较器被删除）")
    oncmd = fn_body(text, "fin_statOnCommand")
    if oncmd is None:
        errors.append("①找不到 fin_statOnCommand")
    else:
        if "set-selections" not in oncmd:
            errors.append("①fin_statOnCommand 不再监听 sheet.operation.set-selections")
        if "finStatSel = found" not in oncmd:
            errors.append("①fin_statOnCommand 没有把命令流选区写进 finStatSel")

    # ---- ①+② 统计计算本体 ----
    comp = fn_body(text, "fin_statCompute")
    if comp is None:
        errors.append("找不到 fin_statCompute（统计栏计算入口被删除）")
    else:
        if "fin_statSize(cmdSel) > fin_statSize(ranges)" not in comp:
            errors.append("①fin_statCompute 未采用「命令流选区更大者优先」（会退化成只统计一格 → 计数恒为 1）")
        if not re.search(r"}?\s*if\s*\(\s*cmdSel\s*&&\s*fin_statSize\(cmdSel\)\s*>\s*fin_statSize\(ranges\)\s*\)\s*ranges\s*=\s*cmdSel\s*;", comp):
            errors.append("①fin_statCompute 缺少 `if (cmdSel && fin_statSize(cmdSel) > fin_statSize(ranges)) ranges = cmdSel;`")
        if "var seen = {};" not in comp:
            errors.append("②fin_statCompute 缺少格级去重 seen 容器（锚点格会被算两次）")
        if "if (seen[_key]) continue;" not in comp or "seen[_key] = 1;" not in comp:
            errors.append("②fin_statCompute 的格级去重逻辑不完整")
        if "COUNT-CELLS-ALL-20261016" not in comp or "cnt++;" not in comp:
            errors.append("②fin_statCompute 计数逻辑未改为「选中单元格总数（含空格）」")
        if "fin_activeSheetId()" not in comp:
            errors.append("①fin_statCompute 未使用 fin_activeSheetId() 取活动工作表 id（仍用 fin_curSheetId 会导致非首表统计为空）")
        if "fin_curSheetId()" in comp:
            errors.append("①fin_statCompute 仍直接调用 fin_curSheetId()（活动表不是第一张时统计为空）")

    # ---- ③ 挂起窗口：defer 而不是 drop ----
    if not re.search(r"var\s+finCnHoldTimer\s*=\s*null\s*;", text):
        errors.append("③找不到 finCnHoldTimer（挂起窗口补排定时器被删除）")
    mark = fn_body(text, "finCnMarkDirty")
    if mark is None:
        errors.append("③找不到 finCnMarkDirty")
    else:
        if "finCnHoldTimer = setTimeout(function(){" not in mark:
            errors.append("③finCnMarkDirty 挂起窗口内没有排补发定时器（改动会被丢弃）")
        if "if (finDirty) finCnScheduleSave();" not in mark:
            errors.append("③补发定时器里没有 `if (finDirty) finCnScheduleSave();`")
        if re.search(r"if\s*\(\s*Date\.now\(\)\s*<\s*finCnHoldUntil\s*\)\s*return\s*;", mark):
            errors.append("③出现旧 BUG 写法：挂起窗口内直接 return（丢弃改动，永不落盘）")
    flush = fn_body(text, "finCnBindFlush")
    if flush is None:
        errors.append("③找不到 finCnBindFlush")
    else:
        if "setInterval(function(){" not in flush or "}, 2000);" not in flush:
            errors.append("③看门狗（2 秒 setInterval）被删除")
        if "if (!finDirty || finSaveTimer || finCnHoldTimer) return;" not in flush:
            errors.append("③看门狗的触发条件被改动（应为：有 dirty + 无待发定时器 + 挂起窗口已过）")

    # ---- ④ 改动代数 ----
    if not re.search(r"var\s+finDirtyGen\s*=\s*0\s*;", text):
        errors.append("④找不到 finDirtyGen 改动代数（保存期间的新改动会被静默吞掉）")
    md = fn_body(text, "fin_markDirty")
    if md is not None and "finDirtyGen++" not in md:
        errors.append("④fin_markDirty 的中国报表分支没有把代数 +1")
    save = fn_body(text, "finCnSave")
    if save is None:
        errors.append("找不到 finCnSave")
    else:
        if "var genAtBuild = finDirtyGen;" not in save:
            errors.append("④finCnSave 未记录本份快照对应的改动代数")
        if "finDirtyGen === genAtBuild" not in save:
            errors.append("④finCnSave 保存成功时未做代数判定（会无条件清 dirty）")
        if "resaveNeeded = true;" not in save:
            errors.append("④finCnSave 缺少 resaveNeeded 标记")
        if "if (ok && (resaveNeeded || finDirty) && fin_isCn())" not in save:
            errors.append("④finCnSave 的 finally 未再排一次保存（新改动会丢）")
    beacon = fn_body(text, "finCnFlushBeacon")
    if beacon is not None and re.search(r"if\s*\(\s*sent\s*\)\s*finDirty\s*=\s*false\s*;", beacon):
        errors.append("④finCnFlushBeacon 又清了 finDirty（sendBeacon 拿不到响应，服务器拒收就丢数据）")

    # ---- ④+⑦ 三块对账 ----
    if "FIN-CN-TRI-CONSIST-20261013" not in text:
        errors.append("⑦找不到 FIN-CN-TRI-CONSIST-20261013（三语块对账被删除：基准块被人民币换算值污染后无法自愈）")
    if "_fx.v = _zv;" not in text:
        errors.append("⑦三块对账的写回语句 _fx.v = _zv 被删除")

    # ---- 自检函数本体 ----
    for nm in ("finCnLockCheck",):
        if fn_body(text, nm) is None:
            errors.append("找不到 %s（锁死区行为级自检被删除）" % nm)
    bind = fn_body(text, "fin_statBind")
    if bind is not None and "finCnLockCheck()" not in bind:
        errors.append("启动自检未被调用：fin_statBind 里找不到 finCnLockCheck()")

    return errors


def check_py(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    errors = []

    if "CN-BASIS-GUARD" not in text:
        errors.append("⑤服务端金额守卫被删除（2026-10-13 就是这么把 41,400,000 写成 10,664.14 → 2.75 的）")
    if fn_body is None:  # pragma: no cover
        pass
    if py_fn_body(text, "_cn_block_total") is None:
        errors.append("⑤找不到 _cn_block_total（三块合计比对的基础函数被删除）")
    if "def _cn_block_total(" not in text:
        errors.append("⑤_cn_block_total 定义异常")
    # ★判据必须就在这段守卫代码里（不能只是文件别处出现过同样的数字）
    gi = text.find("CN-BASIS-GUARD")
    zone = text[gi:gi + 4000] if gi >= 0 else ""
    if not zone:
        errors.append("⑤定位不到守卫代码段（CN-BASIS-GUARD 标记被删除？）")
    for pat, msg in (
        (r'"guard"\s*:\s*"currency-regression"', "⑤守卫响应缺少 guard: currency-regression 标记"),
        (r"_bad_total\s*=\s*bool\(", "⑤缺少「整表缩水」判据 _bad_total"),
        (r"_bad_ratio\s*=\s*bool\(", "⑤缺少「三块不同量级」判据 _bad_ratio"),
        (r"\(_new_base\s*/\s*_old_base\)\s*<\s*0\.02", "⑤缩水阈值 0.02 被改动（÷3882 的换算污染将不再被拦截）"),
        (r"\(_new_base\s*/\s*_new_zh\)\s*<\s*0\.5", "⑤三块量级阈值 0.5 被改动（基准块写成人民币将不再被拦截）"),
        (r"os\.remove\(tmp\)", "⑤守卫命中后没有删除临时文件（会留下脏 tmp）"),
    ):
        if not re.search(pat, zone):
            errors.append(msg)

    if py_fn_body(text, "_cn_ws_save_atomic") is None:
        errors.append("⑥找不到 _cn_ws_save_atomic（原子落盘函数被删除）")
    atomic = py_fn_body(text, "_cn_ws_save_atomic")
    if atomic is not None and "os.replace(tmp, p)" not in atomic:
        errors.append("⑥_cn_ws_save_atomic 没有用 os.replace 原子替换")
    for mm in re.finditer(r"wb\.save\(CN_REPORT\)", text):
        errors.append("第 %d 行出现非原子写盘 wb.save(CN_REPORT)（就地截断重写会把报表写成坏 zip）"
                      % line_of(text, mm.start()))
    return errors


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    html = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "choice_lite.html")
    py = sys.argv[2] if len(sys.argv) > 2 else os.path.join(here, "app.py")

    errors = []
    for p, fn in ((html, check_html), (py, check_py)):
        if not os.path.exists(p):
            print("✗ 找不到文件: %s" % p)
            sys.exit(1)
        errors += ["[%s] %s" % (os.path.basename(p), e) for e in fn(p)]

    print("检查目标: %s / %s" % (os.path.basename(html), os.path.basename(py)))
    if not errors:
        print("✓ 通过：中国报表「统计栏 + 保存不丢」锁定契约未被破坏（%s，①②③④⑤⑥⑦ 全在）" % DOC_ID)
        sys.exit(0)
    for e in errors:
        print("  ✗ 违规: %s" % e)
    print("✗ 失败：共 %d 处违规。这是「锁死」契约，禁止篡改；请恢复后再提交。" % len(errors))
    sys.exit(1)


if __name__ == "__main__":
    main()
