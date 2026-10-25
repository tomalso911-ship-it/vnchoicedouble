# -*- coding: utf-8 -*-
"""直接调用 app.py 里的中国报表归一化，把"核销灰+斜体"和"剔除已勾选的合计公式"
立即写进线上 cn_report.xlsx（避免逻辑漂移：用的是服务端同一份代码）。

等价于服务端每次保存后自动跑的那一步，只是这里手动触发一次，让用户刷新就能看到效果。
用法: python _cn_run_normalize.py [--dry]
"""
import glob
import os
import shutil
import sys
import time

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
CN = os.path.join(HERE, "finance_data", "cn_report.xlsx")

import app  # noqa: E402  （app.py 的启动逻辑都在 __main__ 里，import 不会起服务）

dry = "--dry" in sys.argv
ts = time.strftime("%Y%m%d_%H%M%S")
if not dry:
    bak = CN + ".bak_before_checkgray." + ts
    shutil.copyfile(CN, bak)
    print("已备份 ->", os.path.basename(bak))

print("CN_TEXT_BLUE =", app.CN_TEXT_BLUE)
print("CN_TEXT_GRAY =", app.CN_TEXT_GRAY)
print("CN_TOTAL_ROW =", app.CN_TOTAL_ROW)
print("合计公式样例 E3 =", app._cn_total_formula("E"))

print("--- 数据区字色（未勾选蓝 / 勾选灰+斜体）---")
print("  _cn_normalize_text_color() ->", app._cn_normalize_text_color())
print("--- 合计公式（剔除已勾选核销）---")
print("  _cn_normalize_total_formula() ->", app._cn_normalize_total_formula())

if not dry:
    n = 0
    for p in glob.glob(os.path.join(HERE, "finance_data", "cn_report.snapshot.*")) + \
             [os.path.join(HERE, "finance_data", "cn_report.snapshot.key")]:
        try:
            os.remove(p)
            n += 1
        except OSError:
            pass
    print("已失效中国报表快照缓存文件数:", n)
