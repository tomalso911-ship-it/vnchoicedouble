# -*- coding: utf-8 -*-
"""探针：@univerjs/sheets/facade 的 FWorkbook/FWorksheet 是否暴露 getScroll/setScroll/scrollToCell/
       以及工作表列数读取方法（用于自建水平滚动条并实时反映滚动位置）。只读。"""
import re
import sys
import urllib.request

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
URL = "https://esm.sh/@univerjs/sheets@0.5.5/es2022/sheets.mjs"

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", "replace")

t = get(URL)
print("len", len(t))
for w in ("getScroll", "setScroll", "scrollToCell", "getColumnCount", "getScrollX", "getScrollY", "scrollToRange"):
    hits = list(re.finditer(re.escape(w), t))
    print("  %-16s x%d" % (w, len(hits)))
    for m in hits[:3]:
        print("     …%s…" % t[max(0, m.start() - 160):m.end() + 200].replace("\n", " "))
