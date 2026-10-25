# -*- coding: utf-8 -*-
"""只读差异对比：当前 vn_report.xlsx  vs  将要还原成的 before_merge 备份。
目的：还原前确认「除了中国记录，没有别的改动会被抹掉」。
"""
import io
import os
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import openpyxl  # noqa: E402
from openpyxl.utils import get_column_letter  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
FIN = os.path.join(HERE, "finance_data")
VN = os.path.join(FIN, "vn_report.xlsx")
BAK = os.path.join(FIN, "backups", "vn_report_20261014_055253_before_merge.xlsx.bak")
SHEET = "Chi th\u1ef1c t\u1ebf"
MARK_COL = 40
OUT = os.path.join(HERE, "_diff_vn_backup_out.txt")
L = []


def log(s):
    L.append(str(s))
    io.open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(s)


def load_data(path):
    probe = None
    src = path
    if not path.lower().endswith(".xlsx"):
        probe = path + ".probe.xlsx"
        shutil.copyfile(path, probe)
        src = probe
    wb = openpyxl.load_workbook(src, data_only=False)
    data = {}
    for ws in wb.worksheets:
        cells = {}
        for (r, c), cell in ws._cells.items():
            if cell.value is not None:
                cells[(r, c)] = cell.value
        data[ws.title] = cells
    wb.close()
    if probe:
        try:
            os.remove(probe)
        except OSError:
            pass
    return data


def same(a, b):
    if isinstance(a, (int, float)) and isinstance(b, (int, float)) \
            and not isinstance(a, bool) and not isinstance(b, bool):
        return abs(float(a) - float(b)) < 0.005
    return a == b


def fmt(v):
    s = str(v)
    return s[:38]


A = load_data(VN)
B = load_data(BAK)
log("工作表（当前 vn_report.xlsx）：%s" % " | ".join(A.keys()))
log("工作表（备份 055253）      ：%s" % " | ".join(B.keys()))
log("只当前有的表：%s" % (set(A) - set(B)))
log("只备份有的表：%s" % (set(B) - set(A)))
log("")

TOTAL = 0
for sh in sorted(set(A) | set(B)):
    ra, rb = A.get(sh, {}), B.get(sh, {})
    diffs = []
    for k in set(ra) | set(rb):
        if not same(ra.get(k), rb.get(k)):
            diffs.append((k, ra.get(k), rb.get(k)))
    if not diffs:
        continue
    rows = sorted(set(k[0] for k, _, _ in diffs))
    TOTAL += len(diffs)
    log("== %s：差异 %d 格，涉及 %d 行（行号：%s）"
        % (sh, len(diffs), len(rows), rows[:40]))
    for k, va, vb in sorted(diffs)[:14]:
        log("     %s%-4d 当前=%-38s 备份=%s"
            % (get_column_letter(k[1]), k[0], fmt(va), fmt(vb)))

log("")
log("差异格合计 = %d" % TOTAL)

# 差异行里，哪些在当前文件里带 CN 标记（= 中国记录）
ws_cn = None
wb2 = openpyxl.load_workbook(VN, data_only=False)
ws_cn = wb2[SHEET]
cn_rows = set()
for r in range(5, 420):
    mk = ws_cn.cell(r, MARK_COL).value
    if isinstance(mk, str) and mk.startswith("CN:"):
        cn_rows.add(r)
log("当前文件里带 CN 标记的行（中国记录）= %d 行：%s" % (len(cn_rows), sorted(cn_rows)))
wb2.close()
log("done")
