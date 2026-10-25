# -*- coding: utf-8 -*-
"""合并报表 vs 越南报表：彻底对账（A 同步方向 / B 历史分叉 / C 合并口径）。
   只读 finance_data/backups 下的副本，不改动任何文件。"""
import datetime
import os
import shutil
import sys
import tempfile

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
FIN = os.path.join(HERE, "finance_data")
BKD = os.path.join(FIN, "backups")
OUT = os.path.join(HERE, "_audit_merge_vn_out.txt")
L = []


def log(s=""):
    L.append(str(s))
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print(s)


def as_xlsx(p):
    if p.lower().endswith(".xlsx"):
        return p
    tmp = os.path.join(tempfile.gettempdir(), os.path.basename(p) + ".audit.xlsx")
    shutil.copy2(p, tmp)
    return tmp


def fmt(v):
    if v is None:
        return ""
    if isinstance(v, datetime.datetime):
        return v.strftime("%Y-%m-%d")
    if isinstance(v, float) and v == int(v):
        return str(int(v))
    return str(v)


def num(v):
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str) and v.strip():
        try:
            return float(v.replace(",", ""))
        except ValueError:
            return None
    return None


def load(p):
    return openpyxl.load_workbook(as_xlsx(p), data_only=False)


def align(wb, sn):
    ws = wb[sn]
    m = {}
    for r in range(1, min(ws.max_row, 1200) + 1):
        vou = str(ws.cell(r, 2).value or "").strip().upper()
        if not vou:
            continue
        d = fmt(ws.cell(r, 1).value)
        thu = num(ws.cell(r, 4).value)
        chi = num(ws.cell(r, 5).value)
        desc = fmt(ws.cell(r, 3).value)
        m[(d, vou)] = (r, thu, chi, desc, ws.cell(r, 1).value)
    return ws, m


def audit(m_path, v_path, tag):
    log("")
    log("#" * 78)
    log("# %s" % tag)
    log("#   merge = %s" % os.path.basename(m_path))
    log("#   vn    = %s" % os.path.basename(v_path))
    log("#" * 78)
    try:
        wbm = load(m_path)
        wbv = load(v_path)
    except Exception as e:
        log("  加载失败：%s" % e)
        return
    sheets = [s for s in wbm.sheetnames if s in wbv.sheetnames]
    for sn in sheets:
        wsm, mm = align(wbm, sn)
        wsv, vm = align(wbv, sn)
        only_m = [(k, mm[k]) for k in mm if k not in vm]
        only_v = [(k, vm[k]) for k in vm if k not in mm]
        shared = [k for k in mm if k in vm]
        swaps = []
        valm = []
        datediff = []
        for k in shared:
            r_m, thu_m, chi_m, desc_m, _ = mm[k]
            r_v, thu_v, chi_v, desc_v, _ = vm[k]
            if thu_m != thu_v or chi_m != chi_v:
                if (thu_m, chi_m) == (chi_v, thu_v):
                    swaps.append((k, thu_m, chi_m, thu_v, chi_v))
                else:
                    valm.append((k, thu_m, chi_m, thu_v, chi_v))
            if fmt(wsm.cell(r_m, 1).value) != fmt(wsv.cell(r_v, 1).value):
                datediff.append((k, fmt(wsm.cell(r_m, 1).value), fmt(wsv.cell(r_v, 1).value)))
        log("")
        log("[%s] 共享凭证行=%d | 仅merge(多半CN行)=%d | 仅vn=%d | 方向反=%d | 数值异=%d | 日期异=%d"
            % (sn, len(shared), len(only_m), len(only_v), len(swaps), len(valm), len(datediff)))
        if only_m:
            ex = only_m[:8]
            log("   仅merge行(示例)：")
            for (d, vou), (r, thu, chi, desc, _) in ex:
                log("       %s %s  Thu=%s Chi=%s  %s" % (d, vou, fmt(thu), fmt(chi), desc[:28]))
            if len(only_m) > 8:
                log("       …(其余 %d)" % (len(only_m) - 8))
        if swaps:
            log("   方向反示例(merge 收列↔vn 支列)：")
            for (d, vou), tm, cm, tv, cv in swaps[:12]:
                log("       %s %s  merge Thu=%s Chi=%s  | vn Thu=%s Chi=%s" % (d, vou, fmt(tm), fmt(cm), fmt(tv), fmt(cv)))
            if len(swaps) > 12:
                log("       …(其余 %d)" % (len(swaps) - 12))
        if valm:
            log("   数值异示例：")
            for (d, vou), tm, cm, tv, cv in valm[:12]:
                log("       %s %s  merge Thu=%s Chi=%s  | vn Thu=%s Chi=%s" % (d, vou, fmt(tm), fmt(cm), fmt(tv), fmt(cv)))
            if len(valm) > 12:
                log("       …(其余 %d)" % (len(valm) - 12))
    wbm.close()
    wbv.close()


log("="*78)
log("A+B+C 合并报表彻底审计   %s" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
log("="*78)

# 1) 现在：merge_report vs vn_report
audit(os.path.join(FIN, "merge_report.xlsx"), os.path.join(FIN, "vn_report.xlsx"),
      "① 当前状态：merge_report.xlsx  vs  vn_report.xlsx")

# 2) 合并当时：merged_result vs before_merge 的纯vn
orig_merge = os.path.join(BKD, "vn_report_20261014_072847_merged_result.xlsx.bak")
orig_v = os.path.join(BKD, "vn_report_20261014_052849_before_merge.xlsx.bak")
if os.path.isfile(orig_merge) and os.path.isfile(orig_v):
    audit(orig_merge, orig_v, "② 合并诞生时(07:28)：merged_result  vs  before_merge(纯vn)")

# 3) vn 自己从合并前到现在变了多少
audit(os.path.join(FIN, "vn_report.xlsx"), orig_v, "③ vn 自合并前(05:28)到现在变了多少")

# 4) merge 从诞生到现在漂了多少
audit(os.path.join(FIN, "merge_report.xlsx"), orig_merge, "④ merge_report 从诞生(07:28)到现在漂了多少")

log("")
log("done")
