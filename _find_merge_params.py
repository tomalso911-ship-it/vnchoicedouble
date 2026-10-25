# -*- coding: utf-8 -*-
"""从 sheets.mjs / sheets-ui.mjs 里定位 add-worksheet-merge 的实现，打印参数解构代码。"""
import re
import sys
import urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

URLS = [
    "https://esm.sh/@univerjs/sheets@0.5.5/es2022/sheets.mjs",
    "https://esm.sh/@univerjs/sheets-ui@0.5.5/es2022/sheets-ui.mjs",
]

for u in URLS:
    try:
        req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "ignore")
    except Exception as e:
        print("ERR", u, e)
        continue
    print("=" * 70)
    print(u, len(data))
    for key in ["add-worksheet-merge", "remove-worksheet-merge"]:
        idxs = [m.start() for m in re.finditer(re.escape(key), data)]
        print("-- %s : %d hits" % (key, len(idxs)))
        for i in idxs[:3]:
            seg = data[max(0, i - 900): i + 700]
            print("   ...", seg.replace("\n", " ")[:1600])
            print("   ---")
