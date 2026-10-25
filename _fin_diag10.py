# -*- coding: utf-8 -*-
"""镜像【修复后】的 finLedgerBuildMap，验证：
 1) 每个写入公式的每个被引用格都必须是 数字/空（否则渲染 #VALUE!）；
 2) 每个工作区【末笔余额】== 该区表头 Tồn（=D-E 汇总），即链条自洽；
 3) 首行规则：上一行是静态数字才引用，否则从 0 起算。
数据源：源 xlsx（干净），用 openpyxl 直接取 A 列日期 + D/E/F。"""
import io, sys, re, datetime
from openpyxl import load_workbook

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
wb = load_workbook('finance_data/vn_report.xlsx', data_only=False)
ws = wb['Chi tiết thu-chi']
wbv = load_workbook('finance_data/vn_report.xlsx', data_only=True)
wsv = wbv['Chi tiết thu-chi']

MAX = ws.max_row


def g(r, c):
    return ws.cell(row=r, column=c).value


def gv(r, c):
    return wsv.cell(row=r, column=c).value


def is_serial(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and 20000 <= v <= 80000


def is_date(v):
    if isinstance(v, datetime.datetime) or isinstance(v, datetime.date):
        return True
    if is_serial(v):
        return True
    if isinstance(v, str) and re.match(r'^\d{1,2}[/\-]\d{1,2}[/\-]\d{4}$', v.strip()):
        return True
    return False


def isnum(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def isnum_text(v):
    if isinstance(v, str) and v.strip():
        try:
            float(v.replace(',', ''))
            return True
        except Exception:
            return False
    return False


# --- 分区（与 finLedgerTitleRows 同口径：A 为文字且 D/E 皆空）---
T = []
for r in range(1, MAX + 1):
    a = g(r, 1)
    if a is None or a == '':
        continue
    if is_date(a):
        continue
    if isnum(a):
        continue
    if g(r, 4) not in (None, '') or g(r, 5) not in (None, ''):
        continue
    T.append(r)
print('工作区标题行(1基):', T)
bounds = T + [MAX + 1]
regs = []
for i in range(len(T)):
    lo = T[i] + 1
    hi = bounds[i + 1] - 1
    regs.append((lo, hi))
print('工作区(1基 lo..hi):', regs)

BLOCKS = [(4, 5, 6), (14, 15, 16), (24, 25, 26)]
bad = 0
mismatch = 0
for (lo, hi) in regs:
    rows = [r for r in range(lo, hi + 1) if is_date(g(r, 1))]
    if not rows:
        continue
    print('\n== 工作区 %d..%d 共 %d 笔 ==' % (lo, hi, len(rows)))
    for (dc, ec, fc) in BLOCKS:
        run = 0.0
        start_ref = None
        prev = None
        for i, r in enumerate(rows):
            dv = g(r, dc) or 0
            ev = g(r, ec) or 0
            dvn = float(dv) if isnum(dv) else (float(str(dv).replace(',', '')) if isnum_text(dv) else 0.0)
            evn = float(ev) if isnum(ev) else (float(str(ev).replace(',', '')) if isnum_text(ev) else 0.0)
            if i == 0:
                pv = g(r - 1, fc)
                if pv is not None and not (isinstance(pv, str) and pv.startswith('=')) and isnum(pv):
                    start_ref = r - 1
                    run = float(pv)
                else:
                    start_ref = None
                    run = 0.0
            run = run + dvn - evn
            if i == 0 and start_ref is None:
                f = '=%s%d-%s%d' % (chr(64 + dc), r, chr(64 + ec), r)
                refs = [(dc, r), (ec, r)]
            else:
                refr = start_ref if i == 0 else prev
                f = '=%s%d+%s%d-%s%d' % (chr(64 + fc), refr, chr(64 + dc), r, chr(64 + ec), r)
                refs = [(fc, refr), (dc, r), (ec, r)]
            for (rc, rr) in refs:
                v = g(rr, rc)
                is_formula = isinstance(v, str) and v.startswith('=')
                ok = v is None or isnum(v) or isnum_text(v) or is_formula
                if not ok:
                    bad += 1
                    print('   !!! #VALUE! 风险: F%d 公式 %s 引用了 %s%d = %r' % (r, f, chr(64 + rc), rr, v))
            if i in (0, 1, len(rows) - 1):
                print('   F%-4d = %-26s v=%s  (%s)' % (r, f, run, '首行' if i == 0 else ('末笔' if i == len(rows) - 1 else '')))
            prev = r
        if fc == 6:
            # 校验末笔 == 表头 Tồn
            hdr_f = g(lo - 1, fc)
            total = sum((float(g(r, dc) or 0) if isnum(g(r, dc)) else 0) for r in rows)
            totchi = sum((float(g(r, ec) or 0) if isnum(g(r, ec)) else 0) for r in rows)
            opening = 0.0
            if start_ref is not None:
                opening = float(g(start_ref, fc))
            expect = opening + total - totchi
            mark = 'OK' if abs(expect - run) <= 0.01 else '不一致!'
            print('   [自检] 表头F=%r  期初=%s  末笔(算)=%.2f  应为=%.2f  %s'
                  % (hdr_f, opening, run, expect, mark))
            if mark != 'OK':
                mismatch += 1

print('\n引用文字格(会 #VALUE!)条数 =', bad, '  自检不一致工作区 =', mismatch)
