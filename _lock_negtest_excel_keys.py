# -*- coding: utf-8 -*-
"""FIN-EXCEL-KEYS 硬锁的【反向测试】。

做法：把 choice_lite.html / _univer_kb_fix.html 复制到临时目录，逐个模拟「篡改」，
      断言 check_fin_excel_keys_lock.check_html() 必须报错（= 提交会被拦截）。
      任何一个篡改没被拦住，说明锁有漏洞，脚本以非 0 退出。

注意：篡改【同时】打在生产文件和验证床上（两边一致），这样「不变量⑥ 与验证床不一致」
      这条不会提前命中，才能真正验证 ①~⑤ 每条具体检查是否有效；
      只在需要时（生产接线 ⑤、整块删除、故意不同步）才关闭/利用 ⑥ 这条。
用法：python _lock_negtest_excel_keys.py
"""
import os
import re
import shutil
import sys
import tempfile

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_fin_excel_keys_lock as C  # noqa: E402

SRC_HTML = os.path.join(HERE, "choice_lite.html")
SRC_BED = os.path.join(HERE, "_univer_kb_fix.html")


# ---------- 篡改工具 ----------
def rep(old, new):
    """整文件替换（old 必须存在）。"""
    def _f(t):
        assert old in t, "篡改目标不存在: %r" % old
        return t.replace(old, new)
    return _f


def rep2(*pairs):
    def _f(t):
        for old, new in pairs:
            assert old in t, "篡改目标不存在: %r" % old
            t = t.replace(old, new)
        return t
    return _f


def resub(pattern, repl, what):
    """单次正则替换并断言命中。"""
    def _f(t):
        new, n = re.subn(pattern, repl, t, count=1)
        assert n == 1, "篡改失败（%s，命中 %d 次）" % (what, n)
        return new
    return _f


CAP_PROD = r"\}, true\);(\s*\n\s*/\* ★锁死区自检)"
CAP_BED = CAP_PROD


def drop_bind_call(t):
    """删掉 fin_initUniver 里的 finExcelKeysBind() 调用行（仅生产文件）。"""
    new, n = re.subn(r"^[ \t]*try \{ finExcelKeysBind\(\); \}.*\n", "", t, flags=re.M)
    assert n == 1, "找不到绑定调用行 (n=%d)" % n
    return new


def move_after_finready(t):
    """把绑定调用挪到 finReady = true; 之后（api 未就绪就绑定，仅生产文件）。"""
    pat = (r"([ \t]*try \{ finExcelKeysBind\(\); \} catch\(e\)\{ "
           r"console\.warn\('\[fin-keys\] bind failed', e\); \}\n)"
           r"([ \t]*finReady = true;\n)")
    new, n = re.subn(pat, r"\2\1", t, count=1)
    assert n == 1, "挪动绑定调用失败 (n=%d)" % n
    return new


def kill_whole_block(t):
    i = t.index(C.MARK)
    j = t.index(C.ANCHOR)
    return t[:i] + t[j:]


# (名称, html 篡改, bed 篡改(None=与 html 相同), 是否把验证床交给检查器)
CASES = [
    ("① keydown 改挂 document（会被 Univer 抢先）",
     rep("window.addEventListener('keydown', function(e){",
         "document.addEventListener('keydown', function(e){"), None, True),

    ("① keydown 监听失去捕获阶段（true → false）",
     resub(CAP_PROD, r"}, false);\1", "capture-prod"),
     resub(CAP_BED, r"}, false);\1", "capture-bed"), True),

    ("① 删掉作用域判定 if (!inScope(e)) return;",
     rep("if (!inScope(e)) return;", "if (false) return;"), None, True),

    ("① 作用域判定不再认 .univer-editor（portal 在 body 上）",
     rep("el.classList.contains('univer-editor')", "el.classList.contains('univer-xxx')"), None, True),

    ("① 删掉幂等守卫 __finExcelKeysBound",
     rep("if (window.__finExcelKeysBound) return;", "if (false) return;"), None, True),

    ("① 不再放行 Alt/Meta 组合键",
     rep("if (e.altKey || e.metaKey) return;", "if (false) return;"), None, True),

    ("② 编辑态不再派发 doc.command.delete-right",
     rep("doc.command.delete-right", "doc.command.noop"), None, True),

    ("② 不再区分编辑态 finIsEditingCell()",
     rep("var editing = finIsEditingCell();", "var editing = false;"), None, True),

    ("③ 边界改回直接用 getMaxRows()/getMaxColumns()",
     rep("var sz = finSheetSize() || {};",
         "var sz = { rows: sh.getMaxRows(), cols: sh.getMaxColumns() };"), None, True),

    ("③ 基准不再用按键前快照 finPrevCur（改用实时 cur）",
     rep("finPrevCur || cur", "cur"), None, True),

    ("③ 不再撤销 Univer 的方向键回卷",
     rep("finGotoCell(prev.row, prev.col);", "/* noop */;"), None, True),

    ("③ finSheetSize 不再合并 getLastRow（报表里会卡住光标）",
     rep("sh.getLastRow", "sh.getFooRow"), None, True),

    ("④ 交回 Univer 后不再校准快照 finRememberSoon()",
     rep("finRememberSoon();", ";"), None, True),

    ("④ PageUp/PageDown 量不到行数仍强行接管",
     rep("if (page <= 0) return;", "if (false) return;"), None, True),

    ("④ finGridCanvas 改取公式栏那块小画布",
     rep("univer-workbench-container-canvas", "univer-render-canvas"), None, True),

    ("④ finDataEdge 不再受 FIN_EDGE_SCAN 保护",
     rep2(("scanned < FIN_EDGE_SCAN", "scanned < 4000"),
          ("scanned >= FIN_EDGE_SCAN", "scanned >= 4000")), None, True),

    ("④ FIN_EDGE_SCAN 常量被删除/改名",
     rep("var FIN_EDGE_SCAN = 4000;", "var FIN_EDGE_SCAN_X = 4000;"), None, True),

    ("⑤ fin_initUniver 里不再调用 finExcelKeysBind()",
     drop_bind_call, None, False),

    ("⑤ 绑定调用被挪到 finReady = true; 之后",
     move_after_finready, None, False),

    ("⑥ 整块删除补丁",
     kill_whole_block, None, False),

    ("⑦ 锁死区：删掉契约标记/常量 id",
     rep("'FIN-EXCEL-KEYS-LOCK-20261011'", "'FIN-EXCEL-KEYS-LOCK-XXXX'"), None, True),

    ("⑦ 锁死区：契约常量 FIN_EXCEL_KEYS_LOCK 被删/改名",
     rep("var FIN_EXCEL_KEYS_LOCK = {", "var FIN_EXCEL_KEYS_LOCK_X = {"), None, True),

    ("⑦ 锁死区：开关 captureOnWindow 被改成 false",
     rep("captureOnWindow: true,", "captureOnWindow: false,"), None, True),

    ("⑦ 锁死区：行为级自检函数被删除",
     rep("function finExcelKeysLockCheck(){", "function finExcelKeysLockCheckX(){"), None, True),

    ("⑦ 锁死区：finExcelKeysBind 末尾不再调用自检",
     rep("try { finExcelKeysLockCheck(); } catch(e){}", ";"), None, True),
]


def main():
    tmp = tempfile.mkdtemp(prefix="fin_keys_negtest_")
    try:
        html = os.path.join(tmp, "choice_lite.html")
        bed = os.path.join(tmp, "_univer_kb_fix.html")
        base_html = open(SRC_HTML, encoding="utf-8").read()
        base_bed = open(SRC_BED, encoding="utf-8").read()

        def run(h, b, use_bed=True):
            open(html, "wb").write(h.encode("utf-8"))
            open(bed, "wb").write(b.encode("utf-8"))
            return C.check_html(html, bed if use_bed else None)

        # 对照组：未改动 → 必须通过
        errs, _ = run(base_html, base_bed)
        if errs:
            print("✗ 对照组失败：未改动的文件竟然报错：")
            for e in errs:
                print("   ", e)
            return 2
        print("对照组（未改动）→ 通过 ✔")
        print("-" * 78)

        leaked = []
        for name, hf, bf, use_bed in CASES:
            h = hf(base_html)
            b = (bf or hf)(base_bed) if use_bed else base_bed
            errs, _ = run(h, b, use_bed)
            if errs:
                print("拦截 ✔  %s" % name)
                print("        → %s" % errs[0].split("\n")[0])
            else:
                print("漏过 ✗  %s" % name)
                leaked.append(name)

        # 附加：只改了验证床、忘了同步到生产 → 也必须拦截
        bed_changed = base_bed.replace("var FIN_EDGE_SCAN = 4000;", "var FIN_EDGE_SCAN = 5000;")
        errs, _ = run(base_html, bed_changed, True)
        if errs:
            print("拦截 ✔  ⑥ 改了验证床但忘了同步到生产（两边实现不一致）")
        else:
            print("漏过 ✗  ⑥ 改了验证床但忘了同步到生产（两边实现不一致）")
            leaked.append("两边不一致未拦截")

        print("-" * 78)
        total = len(CASES) + 1
        if leaked:
            print("✗ 反向测试失败：%d/%d 种篡改没被拦住 → %s" % (len(leaked), total, leaked))
            return 1
        print("✓ 反向测试通过：%d 种篡改全部被硬锁拦截。" % total)
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
