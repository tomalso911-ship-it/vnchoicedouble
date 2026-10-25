# -*- coding: utf-8 -*-
import sqlite3, json, sys, os
sys.stdout.reconfigure(encoding="utf-8")
DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agi_pm.db")
conn = sqlite3.connect(DB); conn.row_factory = sqlite3.Row
for r in conn.execute("SELECT project_id, data FROM prod_factory ORDER BY project_id"):
    f = json.loads(r["data"])
    pid = r["project_id"]
    prof = f.get("profile") or {}
    w = f.get("workers") or {}
    print("\n===== pid=%s profile=%s" % (pid, json.dumps(prof, ensure_ascii=False)[:200]))
    for d in sorted(w.keys()):
        x = w[d] or {}
        am = x.get("weatherAm"); pm = x.get("weatherPm")
        print("   %-12s holiday=%-3s rec=%-8s AM=%s PM=%s" % (d, x.get("holiday"), x.get("recorder"),
              (str(am.get("temp"))+"/v"+str(am.get("v"))) if am else "-",
              (str(pm.get("temp"))+"/v"+str(pm.get("v"))) if pm else "-"))
conn.close()
