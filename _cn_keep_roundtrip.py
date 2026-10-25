#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""关键回归：确认「正常的完整保存」不会被新的数据量守卫误拦。

做法（绝不碰真文件）：把服务器当前快照原样喂给 univer_convert 写成
   finance_data/_tmp_roundtrip.xlsx
再拿它去跑 _fin_loss_guard。若守卫把「忠实往返」的报表也拦下来，说明阈值定错了，
   正常录入会被拒绝 → 必须立刻调阈值。
"""
import json
import os
import sys
import urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

CN = os.path.join(ROOT, "finance_data", "cn_report.xlsx")
TMP = os.path.join(ROOT, "finance_data", "_tmp_roundtrip.xlsx")

req = urllib.request.Request("http://127.0.0.1:5050/api/finance/cn-report/snapshot")
with urllib.request.urlopen(req, timeout=60) as r:
    snap = json.loads(r.read().decode("utf-8"))
print("快照已取到，sheetOrder =", snap.get("sheetOrder"))

import univer_convert  # noqa: E402
univer_convert.univer_to_xlsx(snap, TMP)
print("往返文件已写出:", os.path.getsize(TMP), "字节")

import app  # noqa: E402  （只是加载模块，不会启动服务：__main__ 块不执行）

o_nz, o_rows = app._fin_cell_stats(CN)
n_nz, n_rows = app._fin_cell_stats(TMP)
print("现有文件  : 非空 %d / 有数据行 %d" % (o_nz, o_rows))
print("往返文件  : 非空 %d / 有数据行 %d" % (n_nz, n_rows))
blocked, detail = app._fin_loss_guard("cn", CN, TMP)
print("守卫判定  :", "拦截" if blocked else "放行", detail)

try:
    os.remove(TMP)
except OSError:
    pass

if blocked:
    print("✗ FAIL：正常往返保存会被守卫拦下（阈值过严，必须调整）")
    sys.exit(1)
print("✓ PASS：正常的完整保存不会被误拦（比率 %.3f / %.3f）" % (n_nz / max(1, o_nz), n_rows / max(1, o_rows)))
