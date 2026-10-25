# -*- coding: utf-8 -*-
"""直接解析后端生成的快照 JSON：数 CN: 标记行，定位在哪张工作表、哪一行、什么颜色。"""
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
FINDIR = os.path.join(HERE, "finance_data")
OUT = os.path.join(HERE, "_chk_snap_cn_out.txt")
L = []


def log(s):
    L.append(str(s))
    io.open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(s)


def scan(path, label):
    log("=== %s" % label)
    log("    文件：%s（%d bytes）" % (os.path.basename(path), os.path.getsize(path)))
    with io.open(path, "r", encoding="utf-8") as fh:
        j = json.load(fh)
    log("    工作表：%s" % [j["sheets"][sid]["name"] for sid in j["sheetOrder"]])
    total = 0
    for sid in j["sheetOrder"]:
        sh = j["sheets"][sid]
        cd = sh.get("cellData") or {}
        rows = []
        for r, row in cd.items():
            for c, cell in row.items():
                v = cell.get("v")
                if isinstance(v, str) and v.startswith("CN:"):
                    rows.append((int(r) + 1, int(c) + 1, v,
                                 (cd[r].get("1") or {}).get("v"),
                                 (cd[r].get("4") or {}).get("v")))
        if rows:
            total += len(rows)
            log("    ▸ 工作表 %s：CN 标记 %d 行" % (sh["name"], len(rows)))
            for x in rows[:14]:
                log("        行%-4d 列%-3d %-26s 凭证=%-10s 金额=%s" % (x[0], x[1], x[2], x[3], x[4]))
    log("    CN 标记合计 = %d" % total)
    return total


for fn in sorted(os.listdir(FINDIR)):
    if fn.startswith("merge_report.snapshot.") and fn.endswith(".json"):
        scan(os.path.join(FINDIR, fn), "合并报表快照 merge-report")
for fn in sorted(os.listdir(FINDIR)):
    if fn.startswith("vn_report.snapshot.") and fn.endswith(".json"):
        scan(os.path.join(FINDIR, fn), "越南报表快照 vn-report")
log("done")
