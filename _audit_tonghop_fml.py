# -*- coding: utf-8 -*-
"""只读：看 TỔNG HỢP 总表里的公式结构（data_only=False）。
   重点：哪些合计引用了 'Chi thực tế'，哪些合计/总览是写死的静态值（从 vn 抄来不会涨）。"""
import os, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import openpyxl
FIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "finance_data")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_audit_tonghop_fml_out.txt")
L = []
def log(s=""):
    L.append(str(s)); open(OUT,"w",encoding="utf-8").write("\n".join(L)+"\n"); print(s)

for fn in ("vn_report.xlsx", "merge_report.xlsx"):
    wb = openpyxl.load_workbook(os.path.join(FIN, fn), data_only=False)
    ws = wb["TỔNG HỢP"]
    log("===== %s / TỔNG HỢP 里的公式 & 合计行 =====" % fn)
    for r in range(1, ws.max_row + 1):
        for c in range(1, ws.max_column + 1):
            v = ws.cell(r, c).value
            if isinstance(v, str) and v.startswith("="):
                label = ws.cell(r, 2).value
                log("  行%-3d %s2=%r | 公式 %s%s = %s" % (
                    r, "", "", openpyxl.utils.get_column_letter(c), r, v))
        # 也打印含 TỔNG/总计/实际 字样的行标签
        a = ws.cell(r, 1).value; b = ws.cell(r, 2).value
        if isinstance(b, str) and ("TỔNG" in b or "ồng" in b or "实际" in b or "Chi" in b or "chi" in b):
            log("  行%-3d 标签 A=%r B=%r | C=%r" % (r, a, b, ws.cell(r,3).value))
    wb.close()
log("done")
