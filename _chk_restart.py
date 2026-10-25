# -*- coding: utf-8 -*-
"""检查服务是否已重启成功：5050 监听情况 + 新接口 merge-report 的 HTTP 状态。"""
import io
import os
import subprocess
import sys
import urllib.error
import urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_chk_restart_out.txt")
L = []


def log(s):
    L.append(str(s))
    io.open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(s)


try:
    out = subprocess.run(["netstat", "-ano"], capture_output=True, text=True,
                         errors="replace").stdout
    ls = [l.strip() for l in out.splitlines() if ":5050" in l and "LISTENING" in l]
    log("5050 LISTENING：%s" % (ls if ls else "（没有进程在监听）"))
except Exception as e:
    log("netstat 失败：%s" % e)

for label, url in (("merge-report", "http://127.0.0.1:5050/api/finance/merge-report/snapshot"),
                   ("vn-report", "http://127.0.0.1:5050/api/finance/vn-report/snapshot")):
    try:
        with urllib.request.urlopen(urllib.request.Request(url), timeout=90) as r:
            head = r.read(300)
            log("%-13s → HTTP %d，前 200 字节：%s" % (label, r.status, head[:200]))
    except urllib.error.HTTPError as e:
        log("%-13s → HTTPError %d %s" % (label, e.code, e.reason))
    except Exception as e:
        log("%-13s → %s：%s" % (label, type(e).__name__, e))

log("done")
