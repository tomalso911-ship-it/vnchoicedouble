# -*- coding: utf-8 -*-
"""从 esm.sh 上 @univerjs/sheets@0.5.5 的打包文件里抓「合并」相关命令 id 常量。"""
import re
import sys
import urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

URLS = [
    "https://esm.sh/@univerjs/sheets@0.5.5/es2022/sheets.mjs",
    "https://esm.sh/@univerjs/sheets@0.5.5",
    "https://esm.sh/@univerjs/sheets-ui@0.5.5/es2022/sheets-ui.mjs",
]

pat = re.compile(r'["\'](sheet\.command\.[A-Za-z0-9_\-\.]*[Mm]erge[A-Za-z0-9_\-\.]*)["\']')
pat2 = re.compile(r'["\'](sheet\.command\.[A-Za-z0-9_\-\.]*)["\']')

found = {}
for u in URLS:
    try:
        req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(req, timeout=45).read().decode("utf-8", "ignore")
    except Exception as e:
        print("ERR", u, e)
        continue
    print("OK  ", u, len(data))
    for m in pat.findall(data):
        found.setdefault(m, []).append(u)
    if u.endswith("sheets.mjs"):
        # 顺手把 insert/remove 也确认一下
        others = sorted(set(x for x in pat2.findall(data)
                            if re.search(r'(insert|remove|delete).*(row|col)', x, re.I)))
        print("   row/col cmds:", others[:20])

print("\n=== merge cmds ===")
for k in sorted(found):
    print(k)
if not found:
    print("(none found)")
