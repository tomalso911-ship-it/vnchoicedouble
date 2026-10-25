# -*- coding: utf-8 -*-
"""探针：从 esm.sh 拉 Univer 0.5.5 sheets-ui / sheets 的 ESM 产物，
在里面找「全选（Select all）」菜单项与它执行的命令 id。
只读、只打印，不改仓库任何文件。"""
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
    "https://esm.sh/@univerjs/sheets@0.5.5/es2022/sheets.mjs",
    "https://esm.sh/@univerjs/sheets-ui@0.5.5",
]


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", "replace")


def main():
    for url in URLS:
        try:
            t = fetch(url)
        except Exception as e:
            print("!! %s -> %s" % (url, e))
            continue
        print("=" * 100)
        print("%s  (%d chars)" % (url, len(t)))
        # 收集所有形如 'xxx.select-all' / 'selectAll' 的字符串字面量
        ids = sorted(set(re.findall(r"['\"]([A-Za-z0-9_.\-]*select[-\w]*)['\"]", t, re.I)))
        for i in ids:
            print("   ID  %s" % i)
        # 打印含 select-all / selectAll 的上下文片段
        for m in re.finditer(r"select-all|selectAll|SelectAll", t):
            s = max(0, m.start() - 260)
            e = min(len(t), m.end() + 260)
            print("   --- @%d ---" % m.start())
            print("   " + t[s:e].replace("\n", " "))
        if len(sys.argv) > 1 and "--dump" in sys.argv:
            open("_sheetsui_dump.txt", "w", encoding="utf-8").write(t)
            print("   (dumped)")


if __name__ == "__main__":
    main()
