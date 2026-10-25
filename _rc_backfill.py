"""回填历史“TET=否 且 整行人数=0”的日记录为默认模板值。
扫描所有 prod_factory；仅处理日期落在 2026-10-09~13（即截图里的 09/10–13/10）且 holiday!=='yes' 且 11 个角色合计==0 的记录。
默认走试运行（打印将要改的内容），加 --apply 才真正写入（经服务端 API，服务端自动留历史版本）。
"""
import json, sqlite3, sys, io, urllib.request, urllib.error

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

DB = "agi_pm.db"
SRV = "http://127.0.0.1:5050"
ME = "tom"
APPLY = "--apply" in sys.argv

ROLES = ["manager","machinist","welder","forklift","loader","mixer","press","repair","cook","temp","keeper"]
DEFAULTS = {"manager":1,"machinist":1,"welder":3,"forklift":1,"loader":0,"mixer":1,"press":4,"repair":8,"cook":1,"temp":0,"keeper":0}
RANGE_YMD = {"2026-10-09","2026-10-10","2026-10-11","2026-10-12","2026-10-13"}

def key_to_ymd(k):
    k = str(k).strip()
    for sep in ("-", "/"):
        p = k.split(sep)
        if len(p) == 3:
            d, m, y = p
            try:
                return f"{int(y):04d}-{int(m):02d}-{int(d):02d}"
            except: return None
    return None

def db_project_ids():
    con = sqlite3.connect(DB); cur = con.cursor(); ids = set()
    try:
        for (i,) in cur.execute("SELECT id FROM won_projects"): ids.add(str(i))
    except Exception as e: print("won_projects:", e)
    try:
        for (i,) in cur.execute("SELECT project_id FROM prod_factory"): ids.add(str(i))
    except Exception as e: print("prod_factory:", e)
    con.close(); return sorted(ids)

def api_get(pid):
    url = f"{SRV}/api/prod-factory/{pid}?me={ME}"
    try:
        with urllib.request.urlopen(url, timeout=30) as r: return json.loads(r.read().decode())
    except Exception as e: print("  GET", pid, "err:", e); return None

def api_put(pid, data):
    url = f"{SRV}/api/prod-factory/{pid}"
    req = urllib.request.Request(url, data=json.dumps({"requester":ME,"data":data}).encode(),
                                 headers={"Content-Type":"application/json"}, method="PUT")
    try:
        with urllib.request.urlopen(req, timeout=30) as r: return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        print("  PUT", pid, "HTTP", e.code, e.read().decode()[:160]); return None
    except Exception as e: print("  PUT", pid, "err:", e); return None

def main():
    ids = db_project_ids(); print("projects:", ids)
    total = 0
    for pid in ids:
        d = api_get(pid)
        if not d or not d.get("ok") or not d.get("data"): continue
        f = d["data"]; w = f.get("workers") or {}; changed = []
        for dd in list(w.keys()):
            rec = w[dd]
            if not isinstance(rec, dict): continue
            ymd = key_to_ymd(dd)
            if ymd not in RANGE_YMD: continue
            if rec.get("holiday") == "yes": continue   # TET 行，0 人合法，跳过
            total_sum = sum((rec.get(r) or 0) for r in ROLES)
            if total_sum != 0: continue
            for r in ROLES: rec[r] = DEFAULTS[r]
            changed.append(dd)
        if changed:
            print(f"  pid={pid}: 将补默认模板 -> {changed}")
            total += len(changed)
            if APPLY:
                j = api_put(pid, f)
                print("     PUT ->", (j.get("ok"), "stale=" + str(j.get("stale"))) if j else "FAIL")
    print("待补/已补 行数:", total)
    if not APPLY: print("(试运行；加 --apply 才写入)")

main()
