# -*- coding: utf-8 -*-
"""诊断：合并财务报表 vs 越南财务报表，到底是不是同一份数据；
   merge 里有没有指向 vn/cn 的外部公式链接。"""
import datetime
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
FIN = os.path.join(HERE, "finance_data")
OUT = os.path.join(HERE, "_compare_merge_vn_out.txt")
L = []


def log(s=""):
    L.append(str(s))
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print(s)


def fmt(v):
    if v is None:
        return "-"
    if isinstance(v, datetime.datetime):
        return v.strftime("%Y-%m-%d")
    if isinstance(v, float) and v == int(v):
        return str(int(v))
    return str(v)


def is_ext_formula(v):
    return isinstance(v, str) and v.startswith("=") and ("[" in v or "]" in v or ".xlsx" in v.lower() or "'" in v)


wbm = openpyxl.load_workbook(os.path.join(FIN, "merge_report.xlsx"), data_only=False)
wbv = openpyxl.load_workbook(os.path.join(FIN, "vn_report.xlsx"), data_only=False)

log("=== 工作表 ===")
log("merge sheets: %s" % wbm.sheetnames)
log("vn    sheets: %s" % wbv.sheetnames)

log("")
log("=== 逐表对比（行数 / 数据区取值差异）===")
for sm in wbm.sheetnames:
    wsm = wbm[sm]
    wsv = wbv[sm] if sm in wbv.sheetnames else None
    if wsv is None:
        log("[%s] vn 里没有这张表" % sm)
        continue
    log("")
    log("[%s] merge max_row=%d  max_col=%d  |  vn max_row=%d  max_col=%d" % (
        sm, wsm.max_row, wsm.max_column, wsv.max_row, wsv.max_column))
    # 找数据行（凭证列 B 非空）
    m_rows = [r for r in range(1, wsm.max_row + 1) if wsm.cell(r, 2).value is not None]
    v_rows = [r for r in range(1, wsv.max_row + 1) if wsv.cell(r, 2).value is not None]
    log("   merge 数据行=%d  vn 数据行=%d" % (len(m_rows), len(v_rows)))
    # 前 5 行样板
    for n, r in enumerate(m_rows[:5], 1):
        log("   merge 行%03d: %s | %s | 收=%s | 支=%s | 摘要=%s" % (
            r, fmt(wsm.cell(r, 1).value), fmt(wsm.cell(r, 2).value), fmt(wsm.cell(r, 4).value),
            fmt(wsm.cell(r, 5).value), fmt(wsm.cell(r, 3).value)[:24]))
        if n <= len(v_rows):
            rv = v_rows[n - 1]
            log("   vn    行%03d: %s | %s | 收=%s | 支=%s | 摘要=%s" % (
                rv, fmt(wsv.cell(rv, 1).value), fmt(wsv.cell(rv, 2).value), fmt(wsv.cell(rv, 4).value),
                fmt(wsv.cell(rv, 5).value), fmt(wsv.cell(rv, 3).value)[:24]))
    # 数值差异（只比对凭证号一致的行，merge 可能多了 CN 行）
    diffs = 0
    for r in m_rows:
        vou_m = str(wsm.cell(r, 2).value or "").strip().upper()
        if not vou_m:
            continue
        # 在 vn 同一张表里找同行号或同凭证
        v_val = None
        for rv in v_rows:
            if str(wsv.cell(rv, 2).value or "").strip().upper() == vou_m:
                v_val = (wsv.cell(rv, 4).value, wsv.cell(rv, 5).value)
                break
        if v_val is None:
            # merge 里有但 vn 里没有 → 可能是 CN 行
            log("   merge 行%03d %s 在 vn 侧不存在（可能是 CN 行）" % (r, vou_m))
            continue
        m_val = (wsm.cell(r, 4).value, wsm.cell(r, 5).value)
        # 数值比较，允许浮点
        for i, (a, b) in enumerate(zip(m_val, v_val), 4):
            a_num = float(a) if isinstance(a, (int, float)) else None
            b_num = float(b) if isinstance(b, (int, float)) else None
            if a_num is not None and b_num is not None:
                if abs(a_num - b_num) > 1:
                    log("   差异 merge 行%03d 列%s: merge=%s vn=%s" % (r, i, fmt(a), fmt(b)))
                    diffs += 1
            elif (a is None) != (b is None) or (a is not None and b is not None and fmt(a) != fmt(b)):
                log("   差异 merge 行%03d 列%s: merge=%s vn=%s" % (r, i, fmt(a), fmt(b)))
                diffs += 1
    log("   金额差异（不含 CN 行）= %d" % diffs)

log("")
log("=== merge_report 里是否还有外部公式链接？ ===")
ext_f = 0
for sm in wbm.sheetnames:
    wsm = wbm[sm]
    for r in range(1, min(wsm.max_row, 250) + 1):
        for c in range(1, min(wsm.max_column, 45) + 1):
            v = wsm.cell(r, c).value
            if is_ext_formula(v):
                ext_f += 1
                if ext_f <= 15:
                    log("   [%s] 行%03d 列%02d 公式 = %s" % (sm, r, c, v))
log("   外部公式总数 = %d" % ext_f)

log("")
log("=== merge_report 里是否还有任何公式？ ===")
all_f = 0
for sm in wbm.sheetnames:
    wsm = wbm[sm]
    for r in range(1, min(wsm.max_row, 250) + 1):
        for c in range(1, min(wsm.max_column, 45) + 1):
            v = wsm.cell(r, c).value
            if isinstance(v, str) and v.startswith("="):
                all_f += 1
                if all_f <= 10:
                    log("   [%s] 行%03d 列%02d = %s" % (sm, r, c, v[:80]))
log("   公式总数 = %d" % all_f)

wbm.close()
wbv.close()
log("done")
