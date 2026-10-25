# -*- coding: utf-8 -*-
"""用 esprima 校验 choice_lite.html 内联脚本的语法（不执行任何代码）。"""
import io
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import esprima  # noqa: E402

src = io.open("c:/vnchoicedouble/choice_lite.html", encoding="utf-8").read()
blocks = re.findall(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", src, re.S | re.I)
print("内联脚本块数 =", len(blocks))
bad = 0
for i, code in enumerate(blocks):
    line0 = src[:src.index(code)].count("\n") + 1 if code in src else 0
    try:
        esprima.parseScript(code)
    except Exception as e:
        bad += 1
        msg = str(e)
        m = re.search(r"Line (\d+)", msg)
        extra = ("  （文件约第 %d 行）" % (line0 + int(m.group(1)) - 1)) if m else ""
        print("  ✗ 第 %d 块 语法错误: %s%s" % (i + 1, msg[:200], extra))
print("结果：", "全部通过" if not bad else "%d 块有语法错误" % bad)
