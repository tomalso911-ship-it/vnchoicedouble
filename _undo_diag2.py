# -*- coding: utf-8 -*-
"""对比新旧文件里「日期行」的红+粗分布，以及日期数字格式。
   前端 finHiRecompute 每 2s 轮询一次：若"应该高亮的行"和文件里已带红的行不一致，
   它就会不停重写样式；每次样式写入都会把撤销栈静默最多 1.5s → 表现为「撤销按钮按不动」。"""
import os
import sys
import datetime
import shutil
import openpyxl
from openpyxl.utils import get_column_letter

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

BASE = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(BASE, "finance_data")
RED = "FFFF0000"


def loader(path):
    if not path.lower().endswith(".xlsx"):
        tmp = os.path.join(BASE, "_tmp_probe2.xlsx")
        shutil.copyfile(path, tmp)
        path = tmp
    return openpyxl.load_workbook(path)


def font_info(cell):
    f = cell.font
    rgb = ""
    try:
        c = f.color
        rgb = str(getattr(c, "rgb", "") or "")
    except Exception:
        rgb = ""
    return rgb.upper(), bool(f.bold)


def scan(path, label):
    print("=" * 78)
    print("%s   (%s)" % (label, os.path.basename(path)))
    if not os.path.isfile(path):
        print("  <不存在>")
        return
    wb = loader(path)
    for ws in wb.worksheets:
        # 1) 日期列数字格式分布（前 8 行表头 + 第一条数据行）
        fmts = {}
        first_data = None
        for r in range(1, min(ws.max_row, 400) + 1):
            v = ws.cell(r, 1).value
            if isinstance(v, (datetime.datetime, datetime.date)):
                if first_data is None:
                    first_data = (r, v, ws.cell(r, 1).number_format)
                fmts[ws.cell(r, 1).number_format] = fmts.get(ws.cell(r, 1).number_format, 0) + 1
        # 2) 红+粗的行（只看 A..J 显示块）
        redrows = []
        for r in range(1, min(ws.max_row, 800) + 1):
            hits = 0
            for c in range(1, 11):
                rgb, bold = font_info(ws.cell(r, c))
                if RED in rgb and bold:
                    hits += 1
            if hits:
                redrows.append((r, hits))
        # 3) 最大日期行
        maxrow, maxval = None, None
        for r in range(1, min(ws.max_row, 400) + 1):
            v = ws.cell(r, 1).value
            if isinstance(v, (datetime.datetime, datetime.date)):
                v = datetime.datetime(v.year, v.month, v.day)
                if maxval is None or v > maxval:
                    maxval, maxrow = v, r
        print("  %-22s 日期格式=%s  首数据行=%s" % (ws.title, fmts or "-",
                                                 ("r%d %s %s" % (first_data[0], first_data[1].date(), first_data[2])) if first_data else "-"))
        print("      最大日期行=r%s (%s)   红+粗行=%s" % (
            maxrow, (maxval.date() if maxval else "-"),
            (", ".join("r%d(%d)" % t for t in redrows[:12]) + (" …共%d行" % len(redrows) if len(redrows) > 12 else "")) or "无"))


scan(os.path.join(FD, "vn_report.xlsx.bak_before_postfix"), "昨天可用版")
scan(os.path.join(FD, "vn_report.xlsx"), "今天新上传并重翻版")
