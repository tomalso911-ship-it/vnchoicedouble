# -*- coding: utf-8 -*-
import os, sys, json, glob
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
FIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "finance_data")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_check_snap_tonghop_out.txt")
L = []
def log(s=""):
    L.append(str(s)); open(OUT,"w",encoding="utf-8").write("\n".join(L)+"\n"); print(s)

for tag, pat in (("vn","vn_report.snapshot.*.json"), ("merge","merge_report.snapshot.*.json")):
    files = sorted(glob.glob(os.path.join(FIN, pat)))
    if not files:
        log("%s: 无快照" % tag); continue
    data = json.load(open(files[-1], encoding="utf-8"))
    for k,v in data.get("sheets",{}).items():
        if isinstance(v,dict) and v.get("name")=="TỔNG HỢP":
            cd = v.get("cellData") or {}
            # 0-index: C21=row20,col2; C19=row18,col2; C22=row21,col2; C14=row13,col2
            def g(r,c):
                row = cd.get(str(r)) or {}
                cell = row.get(str(c)) if isinstance(row,dict) else None
                return cell.get("v") if isinstance(cell,dict) else None
            log("%s / TỔNG HỢP: C14(收入合计)=%r  C19(支出合计)=%r  C21(实际支出)=%r  C22(期末余额)=%r"
                % (tag, g(13,2), g(18,2), g(20,2), g(21,2)))
            break
log("done")
