# -*- coding: utf-8 -*-
"""抽取 choice_lite.html 里的内联 <script> 块并做 JS 语法检查。
优先用 esprima；没有就试 pyjsparser；都没有则报告并退出（不静默通过）。"""
import importlib.util
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HTML = r"choice_lite.html"


def have(mod):
    try:
        return importlib.util.find_spec(mod) is not None
    except Exception:
        return False


parser_name = None
if have("esprima"):
    parser_name = "esprima"
elif have("pyjsparser"):
    parser_name = "pyjsparser"

print("可用解析器:", parser_name)
if not parser_name:
    print("NO_JS_PARSER")
    sys.exit(3)

src = open(HTML, "r", encoding="utf-8", errors="replace").read()
# 找所有内联 script（跳过 src= 的）
blocks = []
for m in re.finditer(r"<script\b([^>]*)>(.*?)</script\s*>", src, re.S | re.I):
    attrs = m.group(1) or ""
    if re.search(r"\bsrc\s*=", attrs, re.I):
        continue
    body = m.group(2)
    start_line = src[: m.start(2)].count("\n") + 1
    if body.strip():
        blocks.append((start_line, body))
print("内联 script 块数:", len(blocks))

bad = 0
for start_line, body in blocks:
    try:
        if parser_name == "esprima":
            import esprima
            esprima.parseScript(body, {"tolerant": False})
        else:
            import pyjsparser
            pyjsparser.parse(body)
        print("  OK  (起始行 %d, %d 字符)" % (start_line, len(body)))
    except Exception as e:
        bad += 1
        line = getattr(e, "lineNumber", None)
        col = getattr(e, "column", None)
        print("  FAIL 起始行 %d: %s (内部 line=%s col=%s -> 文件第 %s 行)"
              % (start_line, e, line, col,
                 (start_line + line - 1) if line else "?"))
print("FAILED_BLOCKS =", bad)
sys.exit(1 if bad else 0)
