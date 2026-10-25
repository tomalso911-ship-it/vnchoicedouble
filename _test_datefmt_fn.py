# -*- coding: utf-8 -*-
"""行为测试：把 app.py 里「日期格式强制统一」那段真实代码抽出来跑，验证
   ① 文本/中文/美式日期 + General 的真日期都会被改成 dd-mm-yyyy；
   ② 金额列、摘要列、以及「长得像日期序列号的数值列」一格都不许动；
   ③ 已经规范的文件再跑一次 = 0 改动（幂等，不重写文件）。"""
import datetime as _fdt
import os
import re
import shutil
import sys
import tempfile

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import openpyxl  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
FIN = os.path.join(HERE, "finance_data")
OUT = os.path.join(HERE, "_test_datefmt_out.txt")
L = []
FAILS = []


def log(s=""):
    L.append(str(s))
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print(s)


def check(cond, msg):
    log("   %s %s" % ("✓" if cond else "✗", msg))
    if not cond:
        FAILS.append(msg)


# ---------- 抽取 app.py 里的真实代码 ----------
src = open(os.path.join(HERE, "app.py"), encoding="utf-8").read()
i = src.index("# ===================== 日期格式强制统一（FIN-DATE-FMT-20261014）")
j = src.index("def _cn_normalize_style():")
block = src[i:j]
ns = {"os": os, "re": re, "sys": sys, "openpyxl": openpyxl, "_fdt": _fdt}
exec(compile(block, "app.py#FIN-DATE-FMT", "exec"), ns)
force = ns["_fin_force_date_fmt"]
parse = ns["_fin_parse_datetext"]
log("已从 app.py 抽出真实函数 _fin_force_date_fmt / _fin_parse_datetext 并加载")

log("")
log("=== 0) 解析函数单测 ===")
for s, want in (("2026年8月18日", "2026-08-18"), ("18/8/2026", "2026-08-18"),
                ("9/25/2026", "2026-09-25"), ("2026-07-19", "2026-07-19"),
                ("18-8-26", "2026-08-18"), ("Ngày hạch toán", None), ("0", None), ("", None)):
    got = parse(s)
    got = got.strftime("%Y-%m-%d") if got else None
    check(got == want, "%r -> %s（期望 %s）" % (s, got, want))

# ---------- 场景 A：合成表 ----------
tmpd = tempfile.mkdtemp(prefix="datefmt_test_")
pa = os.path.join(tmpd, "syn.xlsx")
wb = openpyxl.Workbook()
ws = wb.active
ws["A4"], ws["B4"], ws["C4"], ws["D4"], ws["E4"] = "Ngày hạch toán", "Số chứng từ", "Diễn giải", "Thu", "Chi"
ws["K4"], ws["M4"], ws["O4"] = "记账日期", "摘要", "支出"
ws["U4"], ws["W4"], ws["Y4"] = "Accounting date", "Description", "Payments"
ws["Z4"] = "Số lượng"          # 数值列（40000~60000，与日期序列号同形）
vals_k = ["2026年8月18日", "18/8/2026", "9/25/2026", "2026-01-05", _fdt.datetime(2026, 3, 3)]
for n, r in enumerate(range(5, 10)):
    ws.cell(r, 1).value = _fdt.datetime(2026, 6, 19 + n)
    ws.cell(r, 1).number_format = "General"                       # 真日期但没格式
    ws.cell(r, 2).value = "UNC0000%d" % n
    ws.cell(r, 3).value = "mô tả %d" % n
    ws.cell(r, 4).value = 0
    ws.cell(r, 5).value = 41400000 + n
    ws.cell(r, 5).number_format = "General"
    ws.cell(r, 11).value = vals_k[n]                              # 文本日期
    ws.cell(r, 13).value = "中文摘要%d" % n
    ws.cell(r, 15).value = 41400000 + n
    ws.cell(r, 21).value = 46109 + n                              # 序列号，General
    ws.cell(r, 23).value = "desc %d" % n
    ws.cell(r, 25).value = 41400000 + n
    ws.cell(r, 26).value = 45000                                  # 数值列，必须不动
wb.save(pa)
wb.close()

log("")
log("=== 1) 合成表：第一次运行 ===")
n1 = force(pa)
log("  改动格数 = %d" % n1)
check(n1 > 0, "检测到并按需修改")
wb = openpyxl.load_workbook(pa, data_only=False)
ws = wb.active
for r in range(5, 10):
    a = ws.cell(r, 1)
    check(isinstance(a.value, _fdt.datetime) and a.number_format == "dd-mm-yyyy",
          "行%d A 列 %r 格式=%s" % (r, a.value, a.number_format))
want_k = ["2026-08-18", "2026-08-18", "2026-09-25", "2026-01-05", "2026-03-03"]
for n, r in enumerate(range(5, 10)):
    c = ws.cell(r, 11)
    ok = (c.value is None) if want_k[n] is None else (isinstance(c.value, _fdt.datetime)
                                                     and c.value.strftime("%Y-%m-%d") == want_k[n])
    check(ok and (want_k[n] is None or c.number_format == "dd-mm-yyyy"),
          "行%d K 列 %r 格式=%s" % (r, c.value, c.number_format))
for r in range(5, 10):
    u = ws.cell(r, 21)
    check(isinstance(u.value, _fdt.datetime) and u.number_format == "dd-mm-yyyy"
          and u.value.strftime("%Y-%m-%d") == (_fdt.datetime(1899, 12, 30)
                                               + _fdt.timedelta(days=46109 + r - 5)).strftime("%Y-%m-%d"),
          "行%d U 列序列号 %s -> 日期 %s" % (r, 46109 + r - 5, u.value))
    for c, tag in ((5, "E 支出"), (15, "O 支出"), (25, "Y 支出"), (26, "Z 数量")):
        cell = ws.cell(r, c)
        check(cell.number_format == "General" and cell.value == (45000 if c == 26 else 41400000 + r - 5),
              "行%d %s 未被碰（值=%r 格式=%s）" % (r, tag, cell.value, cell.number_format))
    check(ws.cell(r, 13).value == "中文摘要%d" % (r - 5), "行%d M 摘要未被碰" % r)
wb.close()

log("")
log("=== 2) 合成表：第二次运行（必须 0 改动 = 幂等）===")
n2 = force(pa)
log("  改动格数 = %d" % n2)
check(n2 == 0, "第二次 0 改动（不重写文件）")

log("")
log("=== 3) 真实 vn_report.xlsx 副本：应为 0 改动（已规范化）===")
pb = os.path.join(tmpd, "vn_copy.xlsx")
shutil.copy2(os.path.join(FIN, "vn_report.xlsx"), pb)
mt = os.path.getmtime(pb)
n3 = force(pb)
log("  改动格数 = %d，mtime 变化 = %s" % (n3, os.path.getmtime(pb) != mt))
check(n3 == 0, "已规范的文件 0 改动")
check(os.path.getmtime(pb) == mt, "文件未被重写（mtime 不动）")

log("")
log("=== 4) 真实 vn 副本里注入 4 个坏日期（中文/美式/文本 + General 真日期）===")
wb = openpyxl.load_workbook(pb, data_only=False)
ws = wb["Chi th\u1ef1c t\u1ebf"]
before_amt = sum(ws.cell(r, c).value for r in range(5, 205) for c in (5, 15, 25)
                 if isinstance(ws.cell(r, c).value, (int, float)))
ws.cell(213, 11).value = "2026年8月18日"
ws.cell(213, 11).number_format = "General"
ws.cell(214, 11).value = "18/8/2026"
ws.cell(215, 11).value = "9/25/2026"
ws.cell(216, 11).number_format = "General"          # 真日期 + General
wb.save(pb)
wb.close()
n4 = force(pb)
log("  改动格数 = %d" % n4)
check(n4 >= 4, "至少修正注入的 4 格（实际 %d）" % n4)
wb = openpyxl.load_workbook(pb, data_only=False)
ws = wb["Chi th\u1ef1c t\u1ebf"]
after_amt = sum(ws.cell(r, c).value for r in range(5, 205) for c in (5, 15, 25)
                if isinstance(ws.cell(r, c).value, (int, float)))
check(before_amt == after_amt, "金额合计未变（%s）" % format(after_amt, ","))
for r in (213, 214, 215, 216):
    c = ws.cell(r, 11)
    check(isinstance(c.value, _fdt.datetime) and c.number_format == "dd-mm-yyyy",
          "行%d K 列 -> %s (%s)" % (r, c.value, c.number_format))
# 其它工作表不该被牵连
check(ws.cell(5, 1).number_format == "dd-mm-yyyy", "行5 A 列仍是 dd-mm-yyyy")
wb.close()

log("")
log("=== 结果 ===")
if FAILS:
    log("✗ 失败 %d 项：" % len(FAILS))
    for f in FAILS:
        log("   - %s" % f)
else:
    log("✓ 全部通过")
shutil.rmtree(tmpd, ignore_errors=True)
log("done")
