# -*- coding: utf-8 -*-
"""对比「今天新上传并重新三语化的报表」与「昨天那份可用的三语报表」，
   重点看会不会让前端的高亮/日期内部写入行为变掉（高亮写入会静默撤销栈 →
   写得太频繁就会表现为「撤销按钮失灵」）。"""
import os
import sys
import datetime
import openpyxl

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

BASE = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(BASE, "finance_data")

NEW = os.path.join(FD, "vn_report.xlsx")
OLD = os.path.join(FD, "vn_report.xlsx.bak_before_postfix")

SHEET = "Chi tiết thu-chi"


def probe(path, label):
    print("=" * 70)
    print("%s  (%s)" % (label, os.path.basename(path)))
    if not os.path.isfile(path):
        print("  <不存在>")
        return
    print("  size=%d" % os.path.getsize(path))
    if not path.lower().endswith(".xlsx"):          # openpyxl 只认扩展名
        import shutil as _sh
        tmp = os.path.join(BASE, "_tmp_probe.xlsx")
        _sh.copyfile(path, tmp)
        path = tmp
    wb = openpyxl.load_workbook(path)
    ws = wb[SHEET] if SHEET in wb.sheetnames else wb.worksheets[0]
    print("  sheet=%r rows=%d cols=%d" % (ws.title, ws.max_row, ws.max_column))
    # A 列（日期列）前 12 个非空格：类型很关键
    shown = 0
    for r in range(1, ws.max_row + 1):
        c = ws.cell(r, 1)
        if c.value in (None, ""):
            continue
        t = type(c.value).__name__
        nf = c.number_format
        print("   A%-4d %-9s %-30s numfmt=%r" % (r, t, str(c.value)[:30], nf))
        shown += 1
        if shown >= 12:
            break
    # 顶部两行的样式（前端高亮"原始色"依赖它）
    for r in (1, 4, 5, 6):
        parts = []
        for cc in range(1, 9):
            cell = ws.cell(r, cc)
            f = cell.font
            parts.append("%s:%s%s" % (openpyxl.utils.get_column_letter(cc),
                                      (f.color.rgb if (f and f.color and f.color.rgb) else "-"),
                                      ("/B" if (f and f.bold) else "")))
        print("   样式r%-2d %s" % (r, " ".join(parts)))
    # 合并单元格数（前端视图重建要用）
    try:
        print("   mergeData=%d" % len(ws.merged_cells.ranges))
    except Exception as e:
        print("   mergeData err %s" % e)
    # 各表列数一览
    for w in wb.worksheets:
        print("     %-24s rows=%-6d cols=%d" % (w.title, w.max_row, w.max_column))


probe(OLD, "昨天可用版（三语）")
probe(NEW, "今天新上传并重翻版")
