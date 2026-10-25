# -*- coding: utf-8 -*-
"""只读巡检：项目 19 production 的真实数据结构 + 复核「出库 > 生产量」是否只是解析口径不一致造成的误报。"""
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
PID = "19"

conn = sqlite3.connect("file:%s?mode=ro" % DB.replace("\\", "/"), uri=True)
conn.row_factory = sqlite3.Row
f = json.loads(conn.execute("SELECT data FROM prod_factory WHERE project_id=?", (PID,)).fetchone()["data"])
conn.close()

prod = f.get("production") or {}
d0 = sorted(prod.keys())[0]
rec0 = prod[d0]
print("=== production[%r] 的键 ===" % d0)
print("  ", sorted(rec0.keys()))
lines = rec0.get("lines")
print("  lines 类型 =", type(lines).__name__, " 键 =", (sorted(lines.keys())[:8] if isinstance(lines, dict) else len(lines)))
if isinstance(lines, dict):
    k0 = sorted(lines.keys())[0]
    print("  lines[%r] =" % k0, json.dumps(lines[k0], ensure_ascii=False)[:600])
    if len(lines) > 1:
        k1 = sorted(lines.keys())[1]
        print("  lines[%r] =" % k1, json.dumps(lines[k1], ensure_ascii=False)[:600])

# 按「lines 是 dict」的解析口径重新聚合产量
def produced_fixed(f):
    mp = {}
    production = f.get("production") or {}
    for d, rec in production.items():
        if not isinstance(rec, dict):
            continue
        lines = rec.get("lines")
        it = []
        if isinstance(lines, dict):
            it = [lines[k] for k in lines]
        elif isinstance(lines, list):
            it = lines
        for line in it:
            if not isinstance(line, dict):
                continue
            qty = line.get("qty")
            houses = line.get("houses")
            if isinstance(qty, dict) and isinstance(houses, list) and houses:
                for s, q in qty.items():
                    qv = float(q) if q else 0.0
                    for h in houses:
                        mp.setdefault(h, {})[s] = mp.get(h, {}).get(s, 0) + qv
                continue
            matrix = line.get("matrix")
            if isinstance(matrix, dict):
                for h, specs in matrix.items():
                    for s, q in (specs.items() if isinstance(specs, dict) else []):
                        mp.setdefault(h, {})[s] = mp.get(h, {}).get(s, 0) + (float(q) if q else 0.0)
    return mp

mp = produced_fixed(f)
print()
print("=== 修正解析口径后逐条复核 ===")
viol = 0
for key, r in (f.get("houseOut") or {}).items():
    out = float((r or {}).get("out") or 0)
    if out <= 0:
        continue
    p = key.split("|")
    h, s = p[0], "|".join(p[1:])
    pr = (mp.get(h) or {}).get(s, 0)
    flag = "违规" if out > pr else "ok"
    if out > pr:
        viol += 1
    print("  %-22s out=%-8s produced=%-8s %s" % (key, int(out), int(pr), flag))
print("  修正口径后违规数 =", viol)

print()
print("=== 该猪舍/规格的产量来源（哪些日期、哪条线贡献）===")
targets = set()
for key, r in (f.get("houseOut") or {}).items():
    if float((r or {}).get("out") or 0) > 0:
        targets.add(tuple(key.split("|", 1)))
shown = 0
for d in sorted(prod.keys()):
    rec = prod[d] or {}
    lines = rec.get("lines")
    it = ([lines[k] for k in sorted(lines.keys())] if isinstance(lines, dict) else (lines or []))
    for i, line in enumerate(it):
        if not isinstance(line, dict):
            continue
        qty = line.get("qty") or {}
        houses = line.get("houses") or []
        hits = [(h, s, qty.get(s)) for (h, s) in targets if h in houses and s in qty]
        if hits:
            shown += 1
            if shown <= 12:
                print("  %s 线%s houses=%s hits=%s" % (d, i + 1, houses, hits))
print("  命中明细行数 =", shown)
