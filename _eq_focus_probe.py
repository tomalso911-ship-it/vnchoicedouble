# -*- coding: utf-8 -*-
"""探针 3：确认 Univer 0.5.5 的 IUniverInstanceService 上有没有把某个 unit 设为
「当前活动单元」的公开方法（focusUnit / setCurrentUnitForType / setCurrentUnit …），
用来修「多实例下原生命令跑到财务报表」这一类问题。只读，不改仓库文件。"""
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
    "https://esm.sh/@univerjs/core@0.5.5/es2022/core.mjs",
]

WORDS = ["focusUnit", "setCurrentUnitForType", "getCurrentUnitForType",
         "getCurrentUnitForType$", "getCurrentTypeOfUnitUnit", "setCurrentUnit"]


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return r.read().decode("utf-8", "replace")


def main():
    for url in URLS:
        try:
            t = fetch(url)
        except Exception as e:
            print("!! %s -> %s" % (url, e))
            continue
        print("=" * 96)
        print("%s (%d chars)" % (url, len(t)))
        for w in WORDS:
            idx = [m.start() for m in re.finditer(re.escape(w), t)]
            print("   %-26s x%d" % (w, len(idx)))
            for i in idx[:3]:
                seg = t[max(0, i - 220):i + 260].replace("\n", " ")
                print("      …%s…" % seg)
        # 导出符号里有没有 focusUnit
        for m in re.finditer(r"\b(\w+)\s+as\s+focusUnit\b|\bfocusUnit\b", t):
            s = max(0, m.start() - 90)
            print("   [export] %s" % t[s:m.end() + 60].replace("\n", " "))


if __name__ == "__main__":
    main()
