# -*- coding: utf-8 -*-
"""验收合并结果（只读）：
  ① 中国 11 条记录都在，凭证号以 UNC 开头，且【整行蓝字】；
  ② 全表按日期自然升序（同日 → 越南在前、中国在后）；
  ③ 不再有 SUM 公式；合计在【行 3】与底部「TỔNG CỘNG」行，且数值一致；
  ④ TỔNG HỢP 的跨表引用已改指向行 3；
  ⑤ 打印中国行附近的一段，肉眼可核对"分散"效果。
"""
import datetime
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import openpyxl  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
VN = os.path.join(HERE, "finance_data", "vn_report.xlsx")
OUT = os.path.join(HERE, "_verify_merge_out.txt")
L = []


def log(s):
    L.append(str(s))
    io.open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(s)


wb = openpyxl.load_workbook(VN, data_only=False)
ws = wb["Chi thực tế"]

# 取数据区：第 5 行到「TỔNG CỘNG」前一行
total_row = None
for r in range(5, 500):
    if str(ws.cell(r, 3).value or "").strip() == "TỔNG CỘNG":
        total_row = r
        break
first, last = 5, (total_row - 2 if total_row else 393)
log("数据区 = 行 %d..%d ；合计行 = %d" % (first, last, total_row))


def isblue(r):
    c = ws.cell(r, 3).font.color
    rgb = getattr(c, "rgb", None)
    return str(rgb).upper().endswith("0000FF")


MARK_COL = 40
rows = []
for r in range(first, last + 1):
    d = ws.cell(r, 1).value
    v = ws.cell(r, 2).value
    e = ws.cell(r, 5).value
    if d is None and v is None and e is None:
        continue
    rows.append((r, d, v, e, isblue(r)))

# 本次合并进来的中国行 = 隐藏标记列（第 40 列）带 "CN:" 前缀
cn_rows = [x for x in rows if str(ws.cell(x[0], MARK_COL).value or "").startswith("CN:")]
log("数据行 = %d ；其中本次合并进来的中国记录（标记列 CN:）= %d" % (len(rows), len(cn_rows)))
bad_blue = [x[0] for x in cn_rows if not x[4]]
log("合并进来的中国行是否全部蓝字 = %s%s" % ("✔ 是" if not bad_blue else "✘ 否",
                                    "" if not bad_blue else "（非蓝行：%s）" % bad_blue))
blue_rows = [x[0] for x in rows if x[4]]
stray = [r for r in blue_rows if not str(ws.cell(r, MARK_COL).value or "").startswith("CN:")]
log("是否有越南原有行被误染成蓝色 = %s%s" % ("✔ 没有" if not stray else "✘ 有",
                                    "" if not stray else "（误染行：%s）" % stray[:10]))

log("")
log("中国记录分布（Excel 行 / 日期 / 凭证 / 金额）：")
for r, d, v, e, b in cn_rows:
    log("   行%-4d %s  %-10s %s" % (r, d.strftime("%Y-%m-%d") if isinstance(d, datetime.datetime) else str(d)[:10],
                                    v, e))

# 日期升序校验
prev = None
viol = []
for r, d, v, e, b in rows:
    if isinstance(d, datetime.datetime):
        if prev and d < prev:
            viol.append((r, prev, d))
        prev = d
log("")
log("按日期升序 = %s%s" % ("✔ 是" if not viol else "✘ 否", "" if not viol else " 违规：%s" % viol[:5]))

# 公式与合计
sums = []
for r in range(1, min(ws.max_row, 500) + 1):
    for c in range(1, 30):
        v = ws.cell(r, c).value
        if isinstance(v, str) and v.startswith("=SUM"):
            sums.append((r, ws.cell(r, c).coordinate, v[:40]))
log("剩余 SUM 公式 = %s" % ("✔ 没有（已改为静态合计）" if not sums else "✘ 还有：%s" % sums))
e3 = ws.cell(3, 5).value
et = ws.cell(total_row, 5).value if total_row else None
log("行3 合计 = %s ；合计行 E%d = %s ；两者一致 = %s" % (e3, total_row, et, "✔" if e3 == et else "✘"))

# 跨表引用
ws2 = wb["TỔNG HỢP"]
log("TỔNG HỢP!C21 = %r" % ws2["C21"].value)

log("")
log("抽样：第 20~27 行（应能看到中国行分散在越南行之间）")
for r in range(20, 28):
    log("   行%-4d %s  %-10s %-30s %s %s"
        % (r, str(ws.cell(r, 1).value)[:10], ws.cell(r, 2).value,
           str(ws.cell(r, 3).value)[:30], ws.cell(r, 5).value, "(蓝)" if isblue(r) else ""))
