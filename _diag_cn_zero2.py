# -*- coding: utf-8 -*-
"""追时间线：cn_report.xlsx 的「收入列（D / N / X）等于 0」是什么时候开始的。
对 finance_data/backups 下所有 cn_report 备份 + 当前文件，统计三块收入列的 0 计数。
"""
import glob
import io
import os
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import openpyxl  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
FIN = os.path.join(HERE, "finance_data")
BAK = os.path.join(FIN, "backups")
CN = os.path.join(FIN, "cn_report.xlsx")
OUT = os.path.join(HERE, "_diag_cn_zero2_out.txt")
L = []


def log(s):
    L.append(str(s))
    io.open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(s)


def counts(path):
    """返回 (D0, N0, X0, E空, O空, Y空) —— 收入列 0 的个数 + 支出列空的个数。"""
    p = path
    tmp = None
    if not path.lower().endswith(".xlsx"):
        tmp = path + ".probe.xlsx"
        shutil.copyfile(path, tmp)
        p = tmp
    try:
        wb = openpyxl.load_workbook(p, data_only=False)
        ws = wb[wb.sheetnames[0]]
        res = []
        for col in (4, 14, 24):          # D / N / X = 收入
            n = 0
            for r in range(5, 206):
                v = ws.cell(r, col).value
                if isinstance(v, (int, float)) and not isinstance(v, bool) and float(v) == 0.0:
                    n += 1
            res.append(n)
        for col in (5, 15, 25):          # E / O / Y = 支出（应为空的行数）
            n = 0
            for r in range(5, 206):
                v = ws.cell(r, col).value
                if isinstance(v, (int, float)) and not isinstance(v, bool) and float(v) == 0.0:
                    n += 1
            res.append(n)
        wb.close()
        return res
    except Exception as e:
        log("   读取失败 %s：%s" % (os.path.basename(path), e))
        return None
    finally:
        if tmp:
            try:
                os.remove(tmp)
            except OSError:
                pass


log("文件                                                   D0  N0  X0 | E0  O0  Y0")
log("当前 cn_report.xlsx                                    %s" % (counts(CN),))
log("")
log("--- 备份（按文件名排序 = 时间排序）---")
for bk in sorted(glob.glob(os.path.join(BAK, "cn_report_*.xlsx.bak"))):
    c = counts(bk)
    if c is None:
        continue
    log("%-52s %s" % (os.path.basename(bk), c))
log("")
log("--- 每日备份 ---")
for bk in sorted(glob.glob(os.path.join(BAK, "cn_report_2026-*.xlsx.bak"))):
    c = counts(bk)
    log("%-52s %s" % (os.path.basename(bk), c))
log("done")
