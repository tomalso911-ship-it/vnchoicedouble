# -*- coding: utf-8 -*-
"""查项目16/21的省份线索（won_projects 各列 + prod-factory profile）。"""
import json, sys, sqlite3, os, urllib.request, urllib.parse
sys.stdout.reconfigure(encoding="utf-8")
BASE = "/opt/choice-pm"
con = sqlite3.connect(os.path.join(BASE, "agi_pm.db"))
con.row_factory = sqlite3.Row
cols = [c[1] for c in con.execute("PRAGMA table_info(won_projects)")]
print("won_projects 列:", cols)
for pid in ("16", "21"):
    for r in con.execute("SELECT * FROM won_projects WHERE id=?", (pid,)):
        d = dict(r)
        print("\n[%s]" % pid)
        for k, v in d.items():
            s = str(v)
            if v is not None and s.strip() and k != "data":
                print("  %s = %r" % (k, s[:80]))
        if "data" in d and d["data"]:
            try:
                j = json.loads(d["data"])
                prof = j.get("profile") or j
                for k in ("province", "region", "location", "address", "name", "projectName"):
                    if prof.get(k):
                        print("  data.%s = %r" % (k, str(prof[k])[:80]))
            except Exception as e:
                print("  data JSON 解析失败:", e)
con.close()
for pid in ("16", "21"):
    u = "http://127.0.0.1:5060/api/prod-factory/%s?me=tom" % pid
    try:
        d = json.loads(urllib.request.urlopen(u, timeout=20).read().decode()).get("data") or {}
        prof = d.get("profile") or {}
        print("\n[%s] prod-factory profile keys=%s" % (pid, list(prof.keys())[:16]))
        for k in ("province", "region", "location", "address", "name", "projectName", "site"):
            if prof.get(k):
                print("  profile.%s = %r" % (k, str(prof[k])[:80]))
        w = (d.get("workers") or {})
        for k, o in w.items():
            print("  workers[%r] keys=%s" % (k, list(o.keys())[:10] if isinstance(o, dict) else o))
    except Exception as e:
        print("[%s] API失败: %s" % (pid, e))
