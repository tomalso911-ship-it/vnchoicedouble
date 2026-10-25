# -*- coding: utf-8 -*-
"""抽出 choice_lite.html 里的财务主内联脚本，用 esprima 做语法检查（定位行号）。"""
import io
import re
import sys

import esprima

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
html = io.open("c:/vnchoicedouble/choice_lite.html", encoding="utf-8", errors="replace").read()
lines = html.split("\n")

# 找出包含 fin_patchFormulaService 的内联 <script> 块
target = None
for m in re.finditer(r"<script(?![^>]*\bsrc=)([^>]*)>(.*?)</script>", html, re.S):
    if "fin_patchFormulaService" in m.group(2):
        start_line = html[:m.start(2)].count("\n") + 1
        target = (start_line, m.group(2), m.group(1))
        break
if not target:
    print("!! 没找到目标 script 块")
    raise SystemExit(1)

start_line, src, attrs = target
print("script 块：起始行 %d，属性 %r，长度 %d 字符" % (start_line, attrs.strip(), len(src)))
try:
    esprima.parseScript(src)
    print("✓ 语法 OK")
except Exception as e:
    msg = str(e)
    ln = re.search(r"Line (\d+)", msg)
    if ln:
        real = start_line + int(ln.group(1)) - 1
        print("✗ 语法错误：" + msg)
        print("   → 文件第 %d 行: %s" % (real, lines[real - 1][:180] if real - 1 < len(lines) else ""))
    else:
        print("✗ " + msg)
