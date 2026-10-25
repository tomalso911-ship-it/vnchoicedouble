# -*- coding: utf-8 -*-
"""按 choice_lite.html 的 prod_houseSpecProduced() 精确口径复核项目 19：
   lines 是「按线号索引的 dict」；产量优先取 line.qtyDetail[spec][house]，
   未覆盖的规格再回退 matrix / line.qty 按需求比例拆分。
另外报告 qty 与 qtyDetail 是否一致（判断回退分支是否真的会被触发）。"""
import os
import json
import sqlite3
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(HERE, "agi_pm.db")
PID = sys.argv[1] if len(sys.argv) > 1 else "19"

conn = sqlite3.connect("file:%s?mode=ro" % DB.replace("\\", "/"), uri=True)
conn.row_factory = sqlite3.Row
row = conn.execute("SELECT data FROM prod_factory WHERE project_id=?", (PID,)).fetchone()
if not row:
    print("无项目 %s" % PID); sys.exit(0)
f = json.loads(row["data"])

# 需求矩阵（prod_slatsMatrix 的口径）：来自 CRM 签约项目的 concrete_floor_spec
mat = {"specs": {}}
try:
    cols = [r["name"] for r in conn.execute("PRAGMA table_info(won_projects)")]
    cfs_col = "concrete_floor_spec" if "concrete_floor_spec" in cols else None
    idcol = "id" if "id" in cols else ("project_id" if "project_id" in cols else None)
    if cfs_col and idcol:
        w = conn.execute("SELECT * FROM won_projects WHERE CAST(%s AS TEXT)=?" % idcol, (str(PID),)).fetchone()
        raw = w[cfs_col] if w else None
        rows = json.loads(raw) if isinstance(raw, str) and raw.strip().startswith("[") else (raw or [])
        if isinstance(rows, list):
            last_ph = ""
            for r0 in rows:
                if not isinstance(r0, dict):
                    continue
                L = r0.get("floor_len", r0.get("L")); W = r0.get("floor_wid", r0.get("W")); H = r0.get("floor_hgt", r0.get("H"))
                def num(v):
                    try: return float(str(v).replace(",", "") or 0)
                    except Exception: return 0.0
                qu = num(r0.get("qty_unit")); ub = num(r0.get("unit_per_building")); bc = num(r0.get("building_count"))
                qty = round(qu * ub * bc)
                if not qty and r0.get("qty_whole") is not None:
                    q = num(r0.get("qty_whole"))
                    if q: qty = int(q)
                ph = str(r0.get("pig_house") or "").strip()
                if ph == "":
                    ph = last_ph
                else:
                    last_ph = ph
                houses = [x.strip() for x in __import__("re").split(r"[,，+/、&\s]+", ph) if x.strip()] if ph else []
                if not houses: houses = ["—"]
                key = "%s×%s×%s" % (L or "?", W or "?", H or "?")
                sp = mat["specs"].setdefault(key, {"houses": {}, "total": 0})
                for h in houses:
                    sp["houses"][h] = sp["houses"].get(h, 0) + qty
                sp["total"] += qty * len(houses)
    print("需求矩阵(concrete_floor_spec) 规格数 =", len(mat["specs"]))
except Exception as e:
    print("需求矩阵读取失败(回退分支将无法精确拆分): %s" % e)
conn.close()


def house_spec_produced_exact(f, mm):
    mp = {}
    fallback_used = []
    for d, rec in (f.get("production") or {}).items():
        if not isinstance(rec, dict) or not rec.get("lines"):
            continue
        for n, line in rec["lines"].items():
            if not isinstance(line, dict):
                continue
            done = {}
            for ds, dm in (line.get("qtyDetail") or {}).items():
                if not isinstance(dm, dict):
                    continue
                dsum = 0
                for dh, dq in dm.items():
                    dq = float(dq or 0)
                    if dq <= 0:
                        continue
                    mp.setdefault(dh, {})[ds] = mp.get(dh, {}).get(ds, 0) + dq
                    dsum += dq
                if dsum > 0:
                    done[ds] = 1
            qty = line.get("qty") or {}
            houses = line.get("houses") or []
            has_rest = any((not done.get(s)) and float(q or 0) > 0 for s, q in qty.items())
            if has_rest and houses and not line.get("matrix"):
                fallback_used.append((d, n))
                for s, q in qty.items():
                    if done.get(s):
                        continue
                    q = float(q or 0)
                    if q <= 0:
                        continue
                    elig = []
                    tot = 0.0
                    for h in houses:
                        dem = float(((mm["specs"].get(s) or {}).get("houses") or {}).get(h, 0) or 0)
                        if dem > 0:
                            elig.append([h, dem, 0]); tot += dem
                    if not elig:
                        for h in houses:
                            mp.setdefault(h, {})[s] = mp.get(h, {}).get(s, 0) + q
                        continue
                    alloc = 0; mx = 0
                    for i, e in enumerate(elig):
                        e[2] = round(q * e[1] / tot) if tot > 0 else 0
                        alloc += e[2]
                        if e[2] > elig[mx][2]: mx = i
                    if alloc != q and elig:
                        elig[mx][2] += q - alloc
                    for e in elig:
                        if e[2] <= 0:
                            continue
                        mp.setdefault(e[0], {})[s] = mp.get(e[0], {}).get(s, 0) + e[2]
            elif line.get("matrix"):
                for mh, specs in line["matrix"].items():
                    for ms, mv in (specs.items() if isinstance(specs, dict) else []):
                        if done.get(ms):
                            continue
                        mv = float(mv or 0)
                        if mv > 0:
                            mp.setdefault(mh, {})[ms] = mp.get(mh, {}).get(ms, 0) + mv
    return mp, fallback_used


mp, fb = house_spec_produced_exact(f, mat)
print("触发 qty 比例回退的天/线 =", len(fb), (fb[:6] if fb else ""))

print()
print("=== houseOut 逐条复核（精确口径）===")
viol = []
for key, r in (f.get("houseOut") or {}).items():
    out = float((r or {}).get("out") or 0)
    if out <= 0:
        continue
    h, _, s = key.partition("|")
    pr = mp.get(h, {}).get(s, 0)
    flag = "★违规" if out > pr else "ok"
    if out > pr:
        viol.append(key)
    print("  %-22s out=%-8s produced=%-8s %s" % (key, int(out), int(pr), flag))
print()
print("精确口径违规数 =", len(viol), viol)
print()
print("=== 其他项目（精确口径，全库扫一遍）===")
conn = sqlite3.connect("file:%s?mode=ro" % DB.replace("\\", "/"), uri=True)
conn.row_factory = sqlite3.Row
n_v = 0
for r in conn.execute("SELECT project_id, data FROM prod_factory ORDER BY project_id"):
    g = json.loads(r["data"])
    mp2, _ = house_spec_produced_exact(g, mat)
    for key, rec in (g.get("houseOut") or {}).items():
        out = float((rec or {}).get("out") or 0)
        if out <= 0:
            continue
        h, _, s = key.partition("|")
        pr = mp2.get(h, {}).get(s, 0)
        if out > pr:
            n_v += 1
            print("  pid=%s %s out=%s produced=%s" % (r["project_id"], key, int(out), int(pr)))
print("全库精确口径违规数 =", n_v)
conn.close()
