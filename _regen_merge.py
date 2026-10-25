# -*- coding: utf-8 -*-
"""A+B 落地：用【当前】vn_report + cn_report 重建合并报表（--keep-dup：中国蓝记录照插、参与合计）。
   流程（与 2026-10-14 原始合并工作流一致、幂等、原子）：
     1) 备份当前 merge_report.xlsx
     2) 跑 _merge_cn_into_vn.py --keep-dup --apply  → 把合并结果写进 vn_report.xlsx（脚本自带 before_merge 备份）
     3) 把合并后的 vn_report.xlsx 复制为 merge_report.xlsx（前端只读服务这份）
     4) 用脚本生成的 before_merge 备份把 vn_report.xlsx 恢复成干净版（不含中国行）
     5) 失效 merge/vn/cn 三份快照缓存键 → 下次载入自动重建
     6) 复核：merge 里中国蓝行数 + Chi thực tế 静态合计
"""
import datetime
import glob
import os
import shutil
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
FIN = os.path.join(HERE, "finance_data")
BKD = os.path.join(FIN, "backups")
VN = os.path.join(FIN, "vn_report.xlsx")
CN = os.path.join(FIN, "cn_report.xlsx")
MR = os.path.join(FIN, "merge_report.xlsx")
OUT = os.path.join(HERE, "_regen_merge_out.txt")
L = []


def log(s=""):
    L.append(str(s))
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print(s)


ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
log("=== 重建合并报表 --keep-dup  @ %s ===" % ts)

# 1) 备份当前 merge
bak_mr = os.path.join(BKD, "merge_report_%s_before_regen.xlsx.bak" % ts)
shutil.copyfile(MR, bak_mr)
log("备份 merge → %s" % os.path.basename(bak_mr))

# 2) 跑合并（写进 vn_report.xlsx）
rc = subprocess.run([sys.executable, os.path.join(HERE, "_merge_cn_into_vn.py"),
                    "--keep-dup", "--apply"], capture_output=False)
log("合并脚本 rc=%s" % rc.returncode)
if rc.returncode != 0:
    log("✗ 合并脚本失败，中止（merge/vn 未改动）")
    sys.exit(1)

# 3) 找脚本刚生成的 before_merge 备份（最新的）
cands = sorted(glob.glob(os.path.join(BKD, "vn_report_*_before_merge.xlsx.bak")))
if not cands:
    log("✗ 找不到 before_merge 备份，中止（不恢复 vn）")
    sys.exit(2)
vn_clean = cands[-1]
log("干净 vn 备份 = %s" % os.path.basename(vn_clean))

# 4) 合并后的 vn → merge_report.xlsx
shutil.copyfile(VN, MR)
log("merged vn → merge_report.xlsx  ✔")

# 5) 恢复 vn 为干净版
shutil.copyfile(vn_clean, VN)
log("恢复 vn_report.xlsx 为干净版（不含中国行）✔")

# 5.5) 合并报表是派生报表，把其 TỔNG HỢP / Chi thực tế 合计格写成静态值，
#      确保快照能直接显示中国实际支出带来的差额（不改动越南报表）。
rc2 = subprocess.run([sys.executable, os.path.join(HERE, "_fix_merge_tonghop.py")],
                     capture_output=False)
log("合并报表合计格静态化 rc=%s" % rc2.returncode)

# 6) 失效快照缓存键
for key in ("merge_report.snapshot.key", "vn_report.snapshot.key", "cn_report.snapshot.key"):
    p = os.path.join(FIN, key)
    try:
        os.remove(p)
        log("删快照键 %s" % key)
    except OSError:
        pass

# 7) 复核
wb = openpyxl.load_workbook(MR, data_only=False)
ws = wb["Chi thực tế"]
cn_rows = 0
for r in range(5, ws.max_row + 1):
    v = ws.cell(r, 40).value
    if isinstance(v, str) and v.startswith("CN:"):
        cn_rows += 1
# 静态合计（表头行 3 的 E/O/Y + 底部 TỔNG CỘNG 行）
e3 = ws.cell(3, 5).value
o3 = ws.cell(3, 15).value
y3 = ws.cell(3, 25).value
log("复核 merge/Chi thực tế：中国蓝行数=%d | 表头静态合计 E=%s O=%s Y=%s" % (cn_rows, e3, o3, y3))
wb.close()
log("done")
