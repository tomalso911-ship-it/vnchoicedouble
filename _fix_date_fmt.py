# -*- coding: utf-8 -*-
"""强制把所有日期列（含文本型日期、无格式的日期序列号）改成 dd-mm-yyyy。
   对象：finance_data/vn_report.xlsx（全部工作表）+ finance_data/cn_report.xlsx
   规则：
     · 日期列判定 = 该列非空格中「日期对象/文本日期/日期序列号」占比 >= 0.8，
       或 >= 0.6 且表头含 Ngày/ngày/date/Date/日期/Tháng/tháng/月
     · 日期对象  -> number_format = dd-mm-yyyy
     · 序列号    -> number_format = dd-mm-yyyy（值不动）
     · 文本日期  -> 解析成真日期 + dd-mm-yyyy（'18/8/2026'、'2026-08-18'、'2026年8月18日' 等）
     · 空格子    -> 也套上 dd-mm-yyyy（保证以后录入的日期不再按中文区域格式显示）
     · 认不出的文字 -> 原样保留，只在日志里列出来
   金额列/凭证列/摘要列一律不碰。落盘：备份 + 原子替换。
"""
import datetime
import os
import re
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import openpyxl  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
FIN = os.path.join(HERE, "finance_data")
BKD = os.path.join(FIN, "backups")
OUT = os.path.join(HERE, "_fix_date_fmt_out.txt")
TARGETS = [os.path.join(FIN, "vn_report.xlsx"), os.path.join(FIN, "cn_report.xlsx")]
FMT = "dd-mm-yyyy"
MAXROW = 800
MAXCOL = 60
HEADER_HINT = re.compile(r"(ng[aà]y|\bdate\b|日期|th[aá]ng|月份)", re.I)

PATTERNS = [
    (re.compile(r"^(\d{1,2})[/\-.](\d{1,2})[/\-.](\d{4})$"), "dmy"),
    (re.compile(r"^(\d{4})[/\-.](\d{1,2})[/\-.](\d{1,2})$"), "ymd"),
    (re.compile(r"^(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日?$"), "cn"),
    (re.compile(r"^(\d{1,2})\s*[/\-.]\s*(\d{1,2})\s*[/\-.]\s*(\d{2})$"), "dmy2"),
    (re.compile(r"^(\d{1,2})\s*月\s*(\d{1,2})\s*日$"), None),
]
L = []


def log(s=""):
    L.append(str(s))
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print(s)


def parse_date(s):
    t = s.strip()
    for rx, kind in PATTERNS:
        m = rx.match(t)
        if not m:
            continue
        g = [int(x) for x in m.groups()]
        if kind in ("ymd", "cn"):
            cands = [(g[2], g[1], g[0])]                    # (日, 月, 年)
        elif kind == "dmy":
            cands = [(g[0], g[1], g[2])]                    # 越南写法 dd/mm/yyyy 优先
            cands.append((g[1], g[0], g[2]))                # 兼美式 mm/dd/yyyy（'9/25/2026'）
        elif kind == "dmy2":
            cands = [(g[0], g[1], 2000 + g[2]), (g[1], g[0], 2000 + g[2])]
        else:
            return None
        for d, mo, y in cands:
            try:
                return datetime.datetime(y, mo, d)
            except ValueError:
                continue
        return None
    return None


def is_serial(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and float(v).is_integer() and 40000 <= v <= 60000


def classify(v):
    if v is None:
        return "blank", None
    if isinstance(v, (datetime.datetime, datetime.date)):
        return "dt", None
    if isinstance(v, str):
        if not v.strip():
            return "blank", None
        d = parse_date(v)
        return ("txt", d) if d else ("other", None)
    if is_serial(v):
        return "ser", None
    return "other", None


def scan_sheet(ws):
    last = min(max(ws.max_row, 1), MAXROW)
    ncol = min(max(ws.max_column, 1), MAXCOL)
    cols = {}
    for c in range(1, ncol + 1):
        kinds = {"dt": 0, "txt": 0, "ser": 0, "blank": 0, "other": 0}
        others = []
        for r in range(1, last + 1):
            k, _ = classify(ws.cell(r, c).value)
            kinds[k] += 1
            if k == "other":
                v = ws.cell(r, c).value
                if v is not None and len(others) < 4:
                    others.append((r, str(v)[:24]))
        dated = kinds["dt"] + kinds["txt"] + kinds["ser"]
        nonblank = dated + kinds["other"]
        if dated < 3 or nonblank <= 0:
            continue
        ratio = dated / float(nonblank)
        header = ""
        hint = False
        for r in range(1, 7):          # 表头可能在第 1/2/4 行，整块都要看
            v = ws.cell(r, c).value
            if isinstance(v, str) and v.strip():
                if not header:
                    header = v.strip()
                if HEADER_HINT.search(v):
                    hint = True
        if ratio >= 0.8 or (ratio >= 0.6 and hint):
            cols[c] = (kinds, ratio, header, others)
    return cols, last


def do_file(path):
    log("")
    log("############################################################")
    log("### %s" % os.path.basename(path))
    log("############################################################")
    wb = openpyxl.load_workbook(path, data_only=False)
    plan = []
    for sn in wb.sheetnames:
        ws = wb[sn]
        cols, last = scan_sheet(ws)
        if not cols:
            log("[%s] 没有识别到日期列" % sn)
            continue
        log("[%s] 识别到日期列：" % sn)
        for c, (kinds, ratio, header, others) in sorted(cols.items()):
            cl = openpyxl.utils.get_column_letter(c)
            log("   %-3s 占比=%.2f 表头=%-24s dt=%d txt=%d ser=%d other=%d"
                % (cl, ratio, header[:24], kinds["dt"], kinds["txt"], kinds["ser"], kinds["other"]))
            for r, s in others:
                log("        非日期内容 行%-4d %r（保留不动）" % (r, s))
            plan.append((sn, c, last))
    # 报告当前异常的日期格式
    log("")
    log("-- 改动前：日期列里 number_format 不是 %s 的日期格（样例 ≤12）--" % FMT)
    shown = 0
    for sn, c, last in plan:
        ws = wb[sn]
        for r in range(1, last + 1):
            k, _ = classify(ws.cell(r, c).value)
            if k in ("dt", "ser", "txt"):
                nf = (ws.cell(r, c).number_format or "").strip()
                if nf.lower() != FMT:
                    if shown < 12:
                        log("   [%s] %s%-4d 值=%r 格式=%r" % (sn, openpyxl.utils.get_column_letter(c), r,
                                                            ws.cell(r, c).value, nf))
                    shown += 1
    log("   （共 %d 格）" % shown)

    # ---- 执行 ----
    changed = {"fmt": 0, "txt2date": 0, "blank": 0}
    txt_samples = []
    for sn, c, last in plan:
        ws = wb[sn]
        for r in range(1, last + 1):
            cell = ws.cell(r, c)
            k, d = classify(cell.value)
            if k == "txt":
                if len(txt_samples) < 12:
                    txt_samples.append((sn, openpyxl.utils.get_column_letter(c), r, cell.value, d))
                cell.value = d
                cell.number_format = FMT
                changed["txt2date"] += 1
            elif k in ("dt", "ser"):
                if (cell.number_format or "").strip().lower() != FMT:
                    cell.number_format = FMT
                    changed["fmt"] += 1
                else:
                    cell.number_format = FMT
            elif k == "blank":
                cell.number_format = FMT
                changed["blank"] += 1
    log("")
    log("-- 文本日期 -> 真日期（样例 ≤12）--")
    for sn, cl, r, old, new in txt_samples:
        log("   [%s] %s%d  %r -> %s" % (sn, cl, r, old, new.strftime("%Y-%m-%d")))
    log("")
    log("格式改写 %d 格 / 文本转日期 %d 格 / 空格套格式 %d 格" % (changed["fmt"], changed["txt2date"], changed["blank"]))

    if changed["fmt"] == 0 and changed["txt2date"] == 0:
        log("无需改动，未落盘。")
        return

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = os.path.join(BKD, "%s_%s_before_datefmt.xlsx.bak" % (os.path.splitext(os.path.basename(path))[0], ts))
    shutil.copy2(path, bak)
    tmp = path + ".datefmt.tmp"
    wb.save(tmp)
    wb.close()
    os.replace(tmp, path)
    log("已备份 -> %s" % bak)
    log("已原子落盘 -> %s" % path)

    # ---- 复核 ----
    wb2 = openpyxl.load_workbook(path, data_only=False)
    bad = 0
    for sn in wb2.sheetnames:
        ws = wb2[sn]
        cols, last = scan_sheet(ws)
        for c in cols:
            for r in range(1, last + 1):
                k, _ = classify(ws.cell(r, c).value)
                if k in ("dt", "ser", "txt"):
                    if (ws.cell(r, c).number_format or "").strip().lower() != FMT:
                        bad += 1
    log("复核：日期列里仍不是 %s 的日期格 = %d %s" % (FMT, bad, "✓" if bad == 0 else "!!"))
    wb2.close()


for p in TARGETS:
    if os.path.isfile(p):
        do_file(p)
    else:
        log("跳过（文件不存在）：%s" % p)
log("")
log("done")
