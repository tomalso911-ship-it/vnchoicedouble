#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Excel 键盘行为补丁「锁死」检查（lint / CI / git pre-commit 均可用）。

契约编号：FIN-EXCEL-KEYS-LOCK-20261011
真源：_univer_kb_fix.html（验证床）；由 _port_fin_keys.py 注入 choice_lite.html 的财务 Univer 模块。

为什么需要这个硬锁：
  Univer 0.5.5 自身的键盘行为与 Excel 不一致（到边界会回卷、缺 Home/End/PageUp/PageDown、
  编辑态 Delete 无效、Ctrl+方向键不是数据边界语义、选区不跟随滚动）。补丁把这些差异逐个补上，
  而每一处补丁都依赖一个「实测得来的前提」。前提一旦被重构掉，症状是「Excel 手感又坏了」，
  但代码看起来仍然完整，很难回顾是哪里改坏的。以下不变量就是这些前提本身：

  ① 接管方式：必须挂在 window 的【捕获阶段】（window → document → … → target 的第一站）。
     挂 document 会因注册先后被 Univer 抢先，读到的选区已经移动过（实测 A1 按 Ctrl+↓
     期望 A4，实际走成 A61）。同时必须（a）幂等守卫 __finExcelKeysBound；
     （b）作用域只在 Univer 内生效，且认 .univer-editor 这个 portal 类名
     （它挂在 body 上，c.contains(activeElement) === false，只看容器会完全不接管）；
     （c）放行 Alt/Meta 组合键。
  ② 编辑态：只补 Delete = 删除光标右侧字符（doc.command.delete-right），其余键一律交回 Univer。
  ③ 非编辑态边界判定：唯一来源 finSheetSize()（= max(getMaxRows, getLastRow+1)），
     禁止在该处理块里直接用 getMaxRows()/getMaxColumns()（实测报表里它返回 42、getLastRow 是 43，
     直接用会把光标卡住、最后几行走不到）。且 Ctrl+方向键的基准必须取「按键之前」的快照
     finPrevCur（Univer 已先动过手），普通方向键要识别并撤销 Univer 的回卷。
  ④ 绝不吞键：算不出边界（超大表 finDataEdge 返回 null）或量不到行数（finPageRows() <= 0）时，
     必须交回 Univer 原生处理，只补跟随滚动。
  ⑤ 生产接线：finExcelKeysBind() 必须在 fin_initUniver() 内、finReady = true; 之前调用。
  ⑥ 同一份实现：choice_lite.html 里的补丁块必须与验证床 _univer_kb_fix.html 逐行一致
     （不一致说明改了验证床却忘了同步；跑 `python _port_fin_keys.py` 一键同步）。
     验证床不存在时降级为警告（它可能被清理掉）。
  ⑦ 代码内★锁死区★：契约常量 FIN_EXCEL_KEYS_LOCK（五个开关必须都为 true）与
     行为级自检 finExcelKeysLockCheck() 必须存在，且必须在 finExcelKeysBind() 末尾被调用。
     静态扫描看不出「实测前提被悄悄改掉」，这层自检会在浏览器里真的验证一遍。

用法：
  python3 check_fin_excel_keys_lock.py [path/to/choice_lite.html] [path/to/_univer_kb_fix.html]
  不传路径时默认检查同目录下的 choice_lite.html 与 _univer_kb_fix.html。
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

DOC_ID = "FIN-EXCEL-KEYS-LOCK-20261011"
MARK = "/* ===== FIN-EXCEL-KEYS：Excel 键盘行为补丁"
ANCHOR = "async function fin_initUniver(){"
PATCH_HEAD = "/* =========================================================================\n   ★ Excel 键盘行为补丁"

# 补丁依赖的辅助函数（缺一个，某些键就会失效或行为退回 Univer 原样）
REQUIRED_FNS = [
    "finExcelKeysBind", "finAPI", "finSheetObj", "finIsEditingCell", "finActiveCell",
    "finVisibleRange", "finScrollState", "finScrollTo", "finEnsureVisible",
    "finLastUsedCell", "finRowLastCol", "finSheetSize", "finGridCanvas", "finPageRows",
    "finGotoCell", "finDataEdge", "finRememberCur", "finRememberSoon",
    "finContainer", "finScrollToSoon",
]


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


def line_of(text, idx):
    return text.count("\n", 0, idx) + 1


def read_norm(path):
    """按文本读取并统一换行（CRLF/LF → LF）。"""
    with open(path, "rb") as f:
        raw = f.read()
    return raw.decode("utf-8").replace("\r\n", "\n")


def extract_bed_patch(bed):
    """从验证床抽出补丁正文（与 _port_fin_keys.py 完全同一套切法）。"""
    start = bed.index(PATCH_HEAD)
    end = bed.rindex("</script>")
    return bed[start:end].rstrip()


def extract_injected(text):
    """从生产文件抽出注入块正文（去掉 4 空格缩进、去壳注释）。"""
    i = text.index(MARK)
    j = text.index(ANCHOR)
    injected = text[i:j].rstrip()
    body = injected.split("===== */\n", 1)[1]
    return "\n".join(ln[4:] if ln.startswith("    ") else ln for ln in body.split("\n")).rstrip()


def check_html(path, bed_path=None):
    text = read_norm(path)
    errors = []
    warnings = []

    # ---- 0) 补丁块必须在，且唯一、位置正确（定义在 fin_initUniver 之前） ----
    if MARK not in text:
        errors.append("找不到补丁块标记 FIN-EXCEL-KEYS（补丁被删除？这是锁死契约，禁止移除）")
        return errors, warnings
    if text.count(MARK) != 1:
        errors.append("补丁块出现 %d 次（应为 1 次，可能重复注入）" % text.count(MARK))
    if ANCHOR not in text:
        errors.append("找不到 `%s`（财务 Univer 初始化入口被改名/删除？）" % ANCHOR.strip())
    elif text.index(MARK) > text.index(ANCHOR):
        errors.append("补丁块位置不对：应在 `%s` 之前" % ANCHOR.strip())

    # ---- 1) 依赖的辅助函数必须都在 ----
    for nm in REQUIRED_FNS:
        if fn_body(text, nm) is None:
            errors.append("不变量③/④被破坏：找不到辅助函数 %s（键盘补丁依赖它）" % nm)

    bind = fn_body(text, "finExcelKeysBind")
    if bind is None:
        errors.append("找不到 finExcelKeysBind（键盘补丁主入口被删除？）")
    else:
        # ---- ① 接管方式 ----
        if not re.search(r"if\s*\(\s*window\.__finExcelKeysBound\s*\)\s*return", bind):
            errors.append("不变量①被破坏：finExcelKeysBind 缺少幂等守卫 "
                          "`if (window.__finExcelKeysBound) return;`")
        if not re.search(r"window\.__finExcelKeysBound\s*=\s*true", bind):
            errors.append("不变量①被破坏：finExcelKeysBind 没有把 __finExcelKeysBound 置为 true")
        mk = re.search(r"window\.addEventListener\(\s*['\"]keydown['\"]\s*,\s*function\s*\(\s*e\s*\)\s*\{", bind)
        if not mk:
            errors.append("不变量①被破坏：keydown 不是挂在 window 上（挂 document 会被 Univer 抢先，"
                          "Ctrl+方向键整段错位）")
        if re.search(r"document\.addEventListener\(\s*['\"]keydown['\"]", bind):
            errors.append("不变量①被破坏：出现挂 document 的 keydown 监听（注册顺序在 Univer 之后，必错位）")
        if mk:
            # 取 keydown 回调的结束（`}, true);`）——窗口本身上还注册过别的监听，
            # 所以只在 keydown 注册点【之后】找第一个，并确认捕获参数为 true。
            cap = re.search(r"\}\s*,\s*(true|false)\s*\)\s*;", bind[mk.end():])
            if not cap:
                errors.append("不变量①被破坏：找不到 keydown 监听的回调结束（capture 参数丢了？）")
            elif cap.group(1) != "true":
                errors.append("不变量①被破坏：keydown 监听没有用【捕获阶段】（第三个参数必须为 true）")
        if not re.search(r"if\s*\(\s*!inScope\(e\)\s*\)\s*return", bind):
            errors.append("不变量①被破坏：没有 `if (!inScope(e)) return;`（补丁会抢走页面其它地方的键盘事件）")
        if fn_body(text, "finIsUniverElem") is None and not re.search(r"function\s+finIsUniverElem\s*\(", bind):
            errors.append("不变量①被破坏：找不到 finIsUniverElem（作用域判定被删）")
        if "'univer-editor'" not in bind and '"univer-editor"' not in bind:
            errors.append("不变量①被破坏：作用域判定不再认 `.univer-editor`（它是挂 body 的 portal，"
                          "只看容器会完全不接管）")
        if "offsetHeight" not in bind or "getClientRects" not in bind:
            errors.append("不变量①被破坏：inScope 不再判断容器可见性（标签页隐藏时会误接管按键）")
        if not re.search(r"if\s*\(\s*e\.altKey\s*\|\|\s*e\.metaKey\s*\)\s*return", bind):
            errors.append("不变量①被破坏：没有放行 Alt/Meta 组合键（`if (e.altKey || e.metaKey) return;`）")

        # ---- ② 编辑态只补 Delete ----
        if not re.search(r"finIsEditingCell\s*\(\s*\)", bind):
            errors.append("不变量②被破坏：没有调用 finIsEditingCell()（编辑态与浏览态不再区分）")
        if not re.search(r"if\s*\(\s*editing\s*\)\s*\{", bind):
            errors.append("不变量②被破坏：找不到编辑态分支 `if (editing) {`")
        if not re.search(r"k\s*===\s*['\"]Delete['\"]", bind):
            errors.append("不变量②被破坏：编辑态没有接管 Delete 键")
        if "doc.command.delete-right" not in bind:
            errors.append("不变量②被破坏：编辑态 Delete 不再派发 `doc.command.delete-right`"
                          "（Univer 0.5.5 对编辑态 Delete 完全不处理）")
        if not re.search(r"k\s*===\s*['\"]Delete['\"][\s\S]{0,400}?return;", bind):
            errors.append("不变量②被破坏：编辑态 Delete 分支缺少 return")

        # ---- ③ 边界判定唯一来源 finSheetSize() ----
        if not re.search(r"var\s+sz\s*=\s*finSheetSize\(\)\s*\|\|\s*\{\s*\}", bind):
            errors.append("不变量③被破坏：边界不再取 `finSheetSize() || {}`")
        if not re.search(r"sz\.rows", bind) or not re.search(r"sz\.cols", bind):
            errors.append("不变量③被破坏：maxR/maxC 不再来自 finSheetSize() 的 rows/cols")
        for mm in re.finditer(r"getMax(Rows|Columns)\s*\(", bind):
            errors.append("不变量③被破坏：第 %d 行在键盘处理块里直接用了 getMax%s()；"
                          "边界必须走 finSheetSize()（= max(getMaxRows, getLastRow+1)）"
                          % (line_of(text, text.index(bind) + mm.start()), mm.group(1)))
        if not re.search(r"finPrevCur\s*\|\|\s*cur", bind):
            errors.append("不变量③被破坏：不再使用「按键之前」的选区快照 finPrevCur 作基准"
                          "（直接读实时 cur 会拿到 Univer 已移动过的位置）")
        if len(re.findall(r"finPrevCur\s*\|\|\s*cur", bind)) < 2:
            errors.append("不变量③被破坏：普通方向键与 Ctrl+方向键应各自取 finPrevCur 基准"
                          "（只找到 %d 处）" % len(re.findall(r"finPrevCur\s*\|\|\s*cur", bind)))
        if not re.search(r"finGotoCell\(\s*prev\.row\s*,\s*prev\.col\s*\)", bind):
            errors.append("不变量③被破坏：不再撤销 Univer 的方向键回卷（找不到 finGotoCell(prev.row, prev.col)）")

        # ---- ④ 绝不吞键 ----
        if len(re.findall(r"finRememberSoon\s*\(\s*\)", bind)) < 2:
            errors.append("不变量④被破坏：交回 Univer 后不再调用 finRememberSoon() 校准快照"
                          "（快照会一直陈旧，下次按键基准就错了）")
        if not re.search(r"finPageRows\s*\(\s*\)", bind):
            errors.append("不变量④被破坏：PageUp/PageDown 不再用 finPageRows() 量行数")
        if not re.search(r"if\s*\(\s*page\s*<=\s*0\s*\)\s*return", bind):
            errors.append("不变量④被破坏：量不到行数时必须直接 return（交回 Univer），"
                          "不得强行 preventDefault")
        if not re.search(r"finDataEdge\s*\(", bind):
            errors.append("不变量④被破坏：Ctrl+方向键不再走 finDataEdge 的数据边界语义")

    # ---- finSheetSize / finGridCanvas / finDataEdge 的实现前提 ----
    szf = fn_body(text, "finSheetSize")
    if szf is not None:
        if not re.search(r"getLastRow", szf) or not re.search(r"getLastColumn", szf):
            errors.append("不变量③被破坏：finSheetSize 不再合并 getLastRow/getLastColumn"
                          "（报表里 getMaxRows() 会偏小，光标会卡住走不到最后几行）")
        if not re.search(r"Math\.max\(\s*r\s*,\s*lr\s*\+\s*1\s*\)", szf):
            errors.append("不变量③被破坏：finSheetSize 对行数不再取 Math.max(r, lr + 1)")

    if fn_body(text, "finGridCanvas") is None:
        errors.append("找不到 finGridCanvas（可见行/列数来源被删除？）")
    else:
        gc = fn_body(text, "finGridCanvas")
        if "univer-workbench-container-canvas" not in gc:
            errors.append("不变量④被破坏：finGridCanvas 不再优先取 .univer-workbench-container-canvas"
                          "（第一个 .univer-render-canvas 是公式栏里的小画布，实测会让 finPageRows() 返回 0，"
                          "PageUp/PageDown 彻底失效）")

    de = fn_body(text, "finDataEdge")
    if de is None:
        errors.append("找不到 finDataEdge（Ctrl+方向键的数据边界算法被删除？）")
    else:
        if "FIN_EDGE_SCAN" not in de:
            errors.append("不变量④被破坏：finDataEdge 不再受 FIN_EDGE_SCAN 保护"
                          "（超大表会退化成逐格扫描）")
    if not re.search(r"var\s+FIN_EDGE_SCAN\s*=\s*\d+", text):
        errors.append("不变量④被破坏：FIN_EDGE_SCAN 常量被删除")

    # ---- ⑤ 生产接线：绑定在 finReady = true; 之前 ----
    init = fn_body(text, "fin_initUniver")
    if init is None:
        errors.append("不变量⑤被破坏：找不到 fin_initUniver")
    else:
        mb = re.search(r"finExcelKeysBind\s*\(\s*\)\s*;", init)
        mr = re.search(r"finReady\s*=\s*true\s*;", init)
        if not mb:
            errors.append("不变量⑤被破坏：fin_initUniver 里没有调用 finExcelKeysBind()"
                          "（补丁不会生效）")
        if not mr:
            errors.append("不变量⑤被破坏：fin_initUniver 里找不到 `finReady = true;`")
        if mb and mr and mb.start() > mr.start():
            errors.append("不变量⑤被破坏：finExcelKeysBind() 被挪到了 `finReady = true;` 之后"
                          "（api 尚未就绪就绑定，补丁会拿不到 api）")

    # ---- ⑦ 代码内★锁死区★（契约常量 + 行为级自检） ----
    if DOC_ID not in text:
        errors.append("找不到锁标记 %s（锁死区注释被删除？）" % DOC_ID)
    if not re.search(r"var\s+FIN_EXCEL_KEYS_LOCK\s*=\s*\{", text):
        errors.append("不变量⑦被破坏：找不到契约常量 FIN_EXCEL_KEYS_LOCK")
    else:
        for key in ("captureOnWindow", "editDeleteRight", "sheetSizeOnly",
                    "snapshotBase", "neverSwallow"):
            if not re.search(r"%s\s*:\s*true" % key, text):
                errors.append("不变量⑦被破坏：FIN_EXCEL_KEYS_LOCK.%s 不再是 true"
                              "（契约开关被改动）" % key)
        if not re.search(r"boundFlag\s*:\s*['\"]__finExcelKeysBound['\"]", text):
            errors.append("不变量⑦被破坏：FIN_EXCEL_KEYS_LOCK.boundFlag 被改动")
        if not re.search(r"id\s*:\s*['\"]" + re.escape(DOC_ID) + r"['\"]", text):
            errors.append("不变量⑦被破坏：FIN_EXCEL_KEYS_LOCK.id 不再是 %s" % DOC_ID)
    if fn_body(text, "finExcelKeysLockCheck") is None:
        errors.append("不变量⑦被破坏：找不到 finExcelKeysLockCheck()（锁死区行为级自检被删除）")
    if bind is not None and not re.search(r"finExcelKeysLockCheck\s*\(\s*\)\s*;", bind):
        errors.append("不变量⑦被破坏：finExcelKeysBind 末尾不再调用 finExcelKeysLockCheck()")

    # ---- ⑥ 与验证床逐行一致 ----
    if bed_path and os.path.exists(bed_path):
        try:
            bed_patch = extract_bed_patch(read_norm(bed_path))
            mine = extract_injected(text)
            if bed_patch != mine:
                import difflib
                d = list(difflib.unified_diff(bed_patch.split("\n"), mine.split("\n"),
                                              "验证床", "choice_lite", lineterm=""))
                head = "\n".join("      " + x for x in d[:24])
                errors.append("不变量⑥被破坏：生产文件里的补丁与验证床 %s 不一致"
                              "（改了验证床却忘了同步 → 跑 `python _port_fin_keys.py` 一键同步）\n%s"
                              % (os.path.basename(bed_path), head))
        except Exception as e:
            warnings.append("无法与验证床比对（%s）" % e)
    elif bed_path:
        warnings.append("验证床 %s 不存在，跳过「同一份实现」比对" % os.path.basename(bed_path))

    return errors, warnings


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "choice_lite.html")
    bed = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(path)),
                                                             "_univer_kb_fix.html")
    if not os.path.exists(path):
        print("✗ 找不到文件: %s" % path)
        sys.exit(1)

    errors, warnings = check_html(path, bed)

    print("检查目标: %s" % path)
    for w in warnings:
        print("  ! 警告: %s" % w)
    if not errors:
        print("✓ 通过：Excel 键盘补丁锁定契约未被破坏（%s 七条不变量全在）" % DOC_ID)
        sys.exit(0)
    for e in errors:
        print("  ✗ 违规: %s" % e)
    print("✗ 失败：共 %d 处违规。这是「锁死」契约，禁止篡改；"
          "请恢复 %s 的不变量后再提交。" % (len(errors), DOC_ID))
    sys.exit(1)


if __name__ == "__main__":
    main()
