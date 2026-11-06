# -*- coding: utf-8 -*-
"""诊断：每日记录报告页天气为空的根因——遍历 prod-factory，打印 profile/日期键/天气字段结构。"""
import json, sys, urllib.request, urllib.parse, sqlite3, os
sys.stdout.reconfigure(encoding="utf-8")
SRV = "http://127.0.0.1:5060"
ME = "tom"
BASE = "/opt/choice-pm"
def get(pid):
    u = "%s/api/prod-factory/%s?me=%s" % (SRV, urllib.parse.quote(str(pid)), ME)
    return json.loads(urllib.request.urlopen(u, timeout=30).read().decode()).get("data")
con = sqlite3.connect(os.path.join(BASE, "agi_pm.db"))
con.row_factory = sqlite3.Row
names = {str(r["id"]): (r["name"] or r["project_name"] or "") for r in con.execute("SELECT * FROM won_projects LIMIT 0")} if False else {}
try:
    names = {str(r["id"]): str(r["name"] or "") for r in con.execute("SELECT id, name FROM won_projects")}
except Exception:
    try:
        cols = [c[1] for c in con.execute("PRAGMA table_info(won_projects)")]
        ncol = "name" if "name" in cols else ("project_name" if "project_name" in cols else cols[1])
        names = {str(r["id"]): str(r[ncol] or "") for r in con.execute("SELECT id, %s FROM won_projects" % ncol)}
    except Exception as e:
        names = {}
        print("won_projects 读取失败:", e)
con.close()
TARGETS = ["03-11-2026", "03/11/2026", "2026-11-03", "04-11-2026", "04/11/2026", "2026-11-04", "05-11-2026", "05/11/2026", "2026-11-05"]
for pid in ["15","16","17","19","21","25","26","27"]:
    d = get(pid)
    if not d:
        print("[%s] 无数据" % pid); continue
    prof = d.get("profile") or {}
    print("\n[%s] name=%r profile.name=%r province=%r keys=%s" % (
        pid, names.get(str(pid), ""), prof.get("name") or prof.get("projectName") or "",
        d.get("province") or prof.get("province") or prof.get("region") or "",
        [k for k in d.keys() if k not in ("id",)][:14]))
    for mapk in ("workers", "production"):
        m = d.get(mapk) or {}
        if not isinstance(m, dict): continue
        ks = list(m.keys())
        print("  %s: %d 条, 样例键=%s" % (mapk, len(ks), ks[:6]))
        for k in ks:
            if any(t in k for t in ("2026-11", "11/2026")) or k in TARGETS:
                o = m[k]
                wa = o.get("weatherAm") if isinstance(o, dict) else None
                wp = o.get("weatherPm") if isinstance(o, dict) else None
                print("    键=%r weatherAm=%s weatherPm=%s 全字段=%s" % (k, json.dumps(wa, ensure_ascii=False), json.dumps(wp, ensure_ascii=False), (list(o.keys())[:12] if isinstance(o, dict) else type(o).__name__)))
