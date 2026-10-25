# -*- coding: utf-8 -*-
"""只读排查：找出「全部的」这个中文译文是从谁翻译来的（哪个原文 → 全部的），
以及它出现在哪些快照/文件里。"""
import io
import json
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = os.path.dirname(os.path.abspath(__file__))


def walk(o, p, out):
    if isinstance(o, dict):
        for k, v in o.items():
            walk(v, p + "/" + str(k), out)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, p + "/" + str(i), out)
    elif isinstance(o, str):
        if "全部的" in o or "总计" in o:
            out.append((p, o))


for name in ("finance_data/fin_trans_cache.json",
             "finance_data/cn_report.snapshot.c4aa9b2c68d447ef.json"):
    fp = os.path.join(ROOT, name)
    if not os.path.isfile(fp):
        print("!! missing %s" % name)
        continue
    with io.open(fp, encoding="utf-8") as f:
        txt = f.read()
    print("=" * 90)
    print(name, len(txt), "chars")
    try:
        d = json.loads(txt)
    except Exception as e:
        print("  json error:", e)
        continue
    out = []
    walk(d, "", out)
    for p, v in out[:60]:
        print("   %-60s => %s" % (p[:60], v))
    print("   total hits:", len(out))
