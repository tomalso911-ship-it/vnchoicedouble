# -*- coding: utf-8 -*-
import os, sys, json, glob
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
FIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "finance_data")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_check_snap_a8_out.txt")
L = []
def log(s=""):
    L.append(str(s)); open(OUT,"w",encoding="utf-8").write("\n".join(L)+"\n"); print(s)

for tag, pat in (("vn","vn_report.snapshot.*.json"), ("merge","merge_report.snapshot.*.json")):
    files = sorted(glob.glob(os.path.join(FIN, pat)))
    if not files: 
        log("%s: 无快照" % tag); continue
    f = files[-1]
    data = json.load(open(f, encoding="utf-8"))
    sheets = data.get("sheets", {})
    for k, v in sheets.items():
        if not (isinstance(v, dict) and v.get("name") == "TỔNG HỢP"): continue
        cd = v.get("cellData")
        log("=== %s / TỔNG HỢP (cellData type=%s) ===" % (tag, type(cd).__name__))
        # 支持两种结构: list[list[cell]] 或 dict{"r_c": cell}
        hits = []
        if isinstance(cd, list):
            for r, row in enumerate(cd):
                if row is None: continue
                if isinstance(row, list):
                    for c, cell in enumerate(row):
                        if cell and isinstance(cell, dict) and isinstance(cell.get("v"), str) and ("我" in cell["v"] or cell["v"].strip() in ("I",)):
                            hits.append((r, c, cell["v"]))
                elif isinstance(row, dict):
                    for ck, cell in row.items():
                        if isinstance(cell, dict) and isinstance(cell.get("v"), str) and ("我" in cell["v"] or cell["v"].strip() in ("I",)):
                            hits.append((r, ck, cell["v"]))
        elif isinstance(cd, dict):
            for key, cell in cd.items():
                if isinstance(cell, dict) and isinstance(cell.get("v"), str) and ("我" in cell["v"] or cell["v"].strip() in ("I",)):
                    hits.append((key, "?", cell["v"]))
        log("  含「我」或「I」的格子: %s" % hits)
        # 直接定位 A8 = 0-indexed row7,col0
        if isinstance(cd, list) and len(cd) > 7 and isinstance(cd[7], (list, dict)):
            row7 = cd[7]
            if isinstance(row7, list):
                log("  A8[7][0] = %r" % (row7[0].get("v") if row7 and isinstance(row7[0],dict) else row7[0] if row7 else None))
            else:
                log("  A8[7][0] = %r" % (row7.get(0, {}).get("v") if isinstance(row7.get(0),dict) else None))
        log("")
log("done")
