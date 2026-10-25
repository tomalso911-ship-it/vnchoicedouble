# -*- coding: utf-8 -*-
"""撤销刚才那次合并：把 vn_report.xlsx 还原成合并前的备份（避免同一笔钱记两遍）。"""
import os
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
FIN = os.path.join(HERE, "finance_data")
VN = os.path.join(FIN, "vn_report.xlsx")
BAK = os.path.join(FIN, "backups", "vn_report_20261014_052849_before_merge.xlsx.bak")

if not os.path.isfile(BAK):
    print("✗ 找不到备份 %s" % BAK)
    sys.exit(1)

tmp = VN + ".undo.tmp"
shutil.copyfile(BAK, tmp)
os.replace(tmp, VN)
print("✔ 已从备份还原 vn_report.xlsx（%s，%d 字节）" % (os.path.basename(BAK), os.path.getsize(VN)))
key = os.path.join(FIN, "vn_report.snapshot.key")
if os.path.isfile(key):
    os.remove(key)
    print("✔ 已清掉快照缓存键（重新载入即回到合并前的数据）")
