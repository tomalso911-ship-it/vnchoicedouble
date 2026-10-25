# -*- coding: utf-8 -*-
"""看一眼服务器 /api/fx-rates 的最新一期（只为判断探针里 700→697 是不是数据源本身的口径）。"""
import json
import sys
import urllib.request

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

try:
    with urllib.request.urlopen("http://127.0.0.1:5050/api/fx-rates", timeout=8) as r:
        j = json.loads(r.read().decode("utf-8"))
except Exception as e:
    print("ERR:", e)
    raise SystemExit

s = (j or {}).get("series") or {}
for k in ("usd_vnd", "cny_vnd", "usd_cny"):
    arr = s.get(k) or []
    tail = arr[-3:] if arr else []
    print("%-9s n=%s tail=%s" % (k, len(arr), tail))
print("ok:", j.get("ok"), "keys:", list(j.keys())[:10])
