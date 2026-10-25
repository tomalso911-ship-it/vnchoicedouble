# -*- coding: utf-8 -*-
"""只读：分别用「逐行累加 E 列(实际支出)」算出 vn 与 merge 的真实实际支出，
   确认 merge = vn + 中国(235,215,160)。并看 E3/E384 是静态值还是公式。"""
import os, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import openpyxl
FIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "finance_data")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_audit_real_exp_out.txt")
L = []
def log(s=""):
    L.append(str(s)); open(OUT,"w",encoding="utf-8").write("\n".join(L)+"\n"); print(s)

CN = 235215160  # 中国三块每块合计（已知）

def analyze(fn):
    wbf = openpyxl.load_workbook(os.path.join(FIN, fn), data_only=False)
    wbd = openpyxl.load_workbook(os.path.join(FIN, fn), data_only=True)
    ws_f = wbf["Chi thực tế"]; ws_d = wbd["Chi thực tế"]
    sum_e = 0.0; n = 0
    for r in range(1, ws_f.max_row + 1):
        f = ws_f.cell(r, 5).value   # E 列公式
        d = ws_d.cell(r, 5).value   # E 列值
        if isinstance(d, (int, float)):
            # 跳过明显的“合计行”：标题/合计文字所在行（B 列含 TỔNG/合计）
            lbl = ws_d.cell(r, 3).value
            if isinstance(lbl, str) and ("TỔNG" in lbl or "ổng" in lbl or "合计" in lbl or "ồng" in lbl):
                continue
            sum_e += d; n += 1
    e3_f = ws_f.cell(3, 5).value
    e384_f = ws_f.cell(384, 5).value
    log("%-18s 逐行累加实际支出(E)= %s (行数%d) | E3=%r E384=%r" % (fn, sum_e, n, e3_f, e384_f))
    wbf.close(); wbd.close()
    return sum_e

vn = analyze("vn_report.xlsx")
mg = analyze("merge_report.xlsx")
log("")
log("越南实际支出 ≈ %s" % vn)
log("合并实际支出(逐行累加,含中国) ≈ %s" % mg)
log("差额 = %s  （中国应贡献 %s）" % (mg - vn, CN))
log("差额 - 中国 = %s" % (mg - vn - CN))
log("done")
