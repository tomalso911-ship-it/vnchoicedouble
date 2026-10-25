# -*- coding: utf-8 -*-
"""验证：① 快照接口是否带回 X-Fin-Rev；② 保存接口是否拒绝过期版本（且不写文件）；
③ 中国报表换算是否仍按 VND 基准（E8 应为 1947.36）。
安全：先备份 cn_report.xlsx，测试后比对哈希，若被改动立刻还原。"""
import hashlib
import io
import json
import os
import shutil
import sys
import urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
OUT = io.open("c:/vnchoicedouble/_verify_rev_out.txt", "w", encoding="utf-8", newline="\n")

CN = "c:/vnchoicedouble/finance_data/cn_report.xlsx"
BAK = "c:/vnchoicedouble/finance_data/backups/cn_report_verify_rev_safety.xlsx.bak"
BASE = "http://127.0.0.1:5050"


def log(s):
    OUT.write(str(s) + "\n")
    print(s)


def sha(p):
    return hashlib.sha256(io.open(p, "rb").read()).hexdigest()[:16]


shutil.copy2(CN, BAK)
h0 = sha(CN)
log("① 备份完成，文件哈希 %s" % h0)

# 1) 快照接口的 X-Fin-Rev
try:
    r = urllib.request.urlopen(BASE + "/api/finance/cn-report/snapshot", timeout=120)
    rev = r.headers.get("X-Fin-Rev")
    body = r.read()
    log("② 快照接口: HTTP %s  X-Fin-Rev=%r  字节=%d  %s"
        % (r.status, rev, len(body), "★乐观锁已生效" if rev else "★没有 rev（服务还是旧代码，需要重启）"))
except Exception as e:
    log("② 快照接口失败: %r" % e)

# 2) 用【过期版本号】提交保存 → 必须被拒且不写文件
try:
    req = urllib.request.Request(
        BASE + "/api/finance/cn-report/save",
        data=json.dumps({"__rev": "0-0", "sheetOrder": [], "sheets": {}}).encode("utf-8"),
        headers={"Content-Type": "application/json"})
    j = json.loads(urllib.request.urlopen(req, timeout=120).read().decode("utf-8"))
    log("③ 过期版本保存: %r" % j)
except Exception as e:
    log("③ 过期版本保存失败: %r" % e)

h1 = sha(CN)
log("④ 文件哈希 %s  %s" % (h1, "未被改动 ✔" if h1 == h0 else "★被改动了！立刻还原"))
if h1 != h0:
    shutil.copy2(BAK, CN)
    log("   已还原；还原后哈希 = %s" % sha(CN))

# 3) 换算仍按 VND 基准
try:
    req = urllib.request.Request(BASE + "/api/finance/convert-currency",
                                 data=json.dumps({"kind": "cn", "target": "RMB"}).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    j = json.loads(urllib.request.urlopen(req, timeout=120).read().decode("utf-8"))
    e8 = ((j.get("values") or {}).get("实际支出") or {}).get("7", {}).get("4")
    log("⑤ 换算 kind=cn/RMB: base=%s rate=%s factor=%s E8=%r （期望 1947.36）"
        % (j.get("base"), j.get("rate"), j.get("factor"), e8))
except Exception as e:
    log("⑤ 换算失败: %r" % e)

OUT.close()
print("done")
