# -*- coding: utf-8 -*-
"""严查：所有项目在生产/安装/出库记录里的天气(weatherAm/weatherPm)覆盖情况"""
import sqlite3, json, sys, os
sys.stdout.reconfigure(encoding="utf-8")

DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agi_pm.db")
conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row

rows = conn.execute("SELECT project_id, data, updated_by, updated_at FROM prod_factory").fetchall()
print("prod_factory 项目数:", len(rows))

def bad(x):
    am, pm = (x or {}).get("weatherAm"), (x or {}).get("weatherPm")
    b = []
    if not am or am.get("v") != 2: b.append("AM")
    if not pm or pm.get("v") != 2: b.append("PM")
    return b

grand = []
for r in rows:
    f = json.loads(r["data"])
    pid = str(r["project_id"])
    res = {"pid": pid, "upd": r["updated_at"], "by": r["updated_by"]}
    for name, m in (("生产-人员", f.get("workers")), ("生产-每日", f.get("production")), ("安装-人员", ((f.get("installation") or {}).get("workers")))):
        m = m or {}
        miss = [(d, ",".join(bad(m[d]))) for d in sorted(m.keys()) if bad(m[d])]
        res[name] = (len(m), miss)
    ho = f.get("houseOut") or {}
    ho_miss = []
    for k, rec in ho.items():
        for fld in ("outDaily", "inDaily"):
            for d, e in (rec.get(fld) or {}).items():
                if isinstance(e, dict) and bad(e): ho_miss.append((k + "|" + fld[-5:] + ":" + d, ",".join(bad(e))))
    res["出库/入库日天气"] = ho_miss
    grand.append(res)

print("\n=== 明细 ===")
for x in grand:
    print("\n[pid=%s] 更新人=%s 时间=%s" % (x["pid"], x["by"], x["upd"]))
    for name in ("生产-人员", "生产-每日", "安装-人员"):
        n, miss = x[name]
        print("  %-8s 记录日=%3d  缺天气行=%3d" % (name, n, len(miss)), (" -> " + "; ".join("%s(%s)" % (a, b) for a, b in miss[:25]) + (" ...共%d" % len(miss) if len(miss) > 25 else "")) if miss else "")
    if x["出库/入库日天气"]:
        print("  出库/入库日 缺天气=%d -> %s" % (len(x["出库/入库日天气"]), "; ".join("%s(%s)" % (a, b) for a, b in x["出库/入库日天气"][:25])))

print("\n=== 汇总 ===")
for name in ("生产-人员", "生产-每日", "安装-人员"):
    tot = sum(x[name][0] for x in grand); miss = sum(len(x[name][1]) for x in grand)
    print("%-8s 记录日总计=%d 缺天气=%d" % (name, tot, miss))
print("出库/入库日 缺天气=%d" % sum(len(x["出库/入库日天气"]) for x in grand))
conn.close()
