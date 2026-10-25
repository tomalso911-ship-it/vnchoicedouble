# -*- coding: utf-8 -*-
"""探针：找 Univer 0.5.5 里「单元格编辑提交」走的是哪条命令，以及有没有拦截钩子
（interceptCommand / beforeCommandExecuted），用于实现 Excel 的「' 前缀 = 强制文本」。
只读，不改仓库文件。"""
import re
import sys
import urllib.request

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

URLS = [
    "https://esm.sh/@univerjs/sheets-ui@0.5.5/es2022/sheets-ui.mjs",
    "https://esm.sh/@univerjs/core@0.5.5/es2022/core.mjs",
]


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read().decode("utf-8", "replace")


def show(t, pat, before=300, after=900, limit=4, tag=""):
    n = 0
    for m in re.finditer(pat, t):
        n += 1
        if n > limit:
            break
        s = max(0, m.start() - before)
        e = min(len(t), m.end() + after)
        print("  --- %s @%d ---" % (tag or pat, m.start()))
        print("  " + t[s:e].replace("\n", " "))
    if not n:
        print("  (无 %s)" % (tag or pat))


for url in URLS:
    try:
        t = fetch(url)
    except Exception as e:
        print("!! %s -> %s" % (url, e))
        continue
    print("=" * 100)
    print("%s (%d chars)" % (url, len(t)))
    if "sheets-ui" in url:
        print("[1] _submitCellData")
        show(t, r"_submitCellData\(", 200, 1200, 2)
        print("[2] command ids: set-range-values / cell-edit")
        ids = sorted(set(re.findall(r"['\"]([a-z0-9.\-]*(?:set-range-values|cell-edit)[a-z0-9.\-]*)['\"]", t)))
        for i in ids:
            print("   ID %s" % i)
        print("[3] ParseFormula / typed value")
        ids2 = sorted(set(re.findall(r"['\"]([a-z0-9.\-]*(?:parse|typed)[a-z0-9.\-]*)['\"]", t, re.I)))
        for i in ids2[:20]:
            print("   ID %s" % i)
    else:
        print("[4] interceptCommand / beforeCommandExecuted")
        show(t, r"interceptCommand", 200, 400, 3)
        show(t, r"beforeCommandExecuted", 150, 350, 2)
