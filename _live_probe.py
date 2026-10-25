# -*- coding: utf-8 -*-
"""探查 5050 上正在服务的进程：新旧接口是否都在、进程启动时间（_live_probe_out.txt）。"""
import io
import os
import subprocess
import sys
import urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_live_probe_out.txt")
L = []


def log(s):
    L.append(str(s))
    io.open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")


BASE = "http://127.0.0.1:5050"
for path in ("/api/finance/vn-report/snapshot",
             "/api/finance/cn-report/snapshot",
             "/api/finance/sheet-titles?kind=vn",
             "/api/finance/sheet-titles?kind=cn"):
    try:
        with urllib.request.urlopen(BASE + path, timeout=15) as r:
            body = r.read()
            log("GET %-42s -> %s  (%d bytes)" % (path, r.status, len(body)))
    except Exception as e:
        code = getattr(e, "code", None)
        log("GET %-42s -> %s  %s" % (path, code if code else "ERR", str(e)[:90]))

# 谁在监听 5050 + 进程启动时间/命令行
ps = ("$c = Get-NetTCPConnection -LocalPort 5050 -State Listen -ErrorAction SilentlyContinue; "
      "foreach ($x in $c) { $p = Get-CimInstance Win32_Process -Filter (\"ProcessId=\" + $x.OwningProcess); "
      "Write-Output ('PID=' + $x.OwningProcess + ' | start=' + $p.CreationDate + ' | cmd=' + $p.CommandLine) }")
try:
    out = subprocess.run(["powershell", "-NoProfile", "-Command", ps],
                         capture_output=True, text=True, timeout=60)
    log("")
    log("=== 监听 5050 的进程 ===")
    log(out.stdout.strip() or "(没有进程在监听 5050)")
    if out.stderr.strip():
        log("stderr: " + out.stderr.strip()[:300])
except Exception as e:
    log("ps 失败: " + str(e))

# 所有 python 进程
ps2 = ("Get-CimInstance Win32_Process -Filter \"Name like '%python%'\" | "
       "ForEach-Object { 'PID=' + $_.ProcessId + ' | start=' + $_.CreationDate + ' | ' + $_.CommandLine }")
try:
    out2 = subprocess.run(["powershell", "-NoProfile", "-Command", ps2],
                          capture_output=True, text=True, timeout=60)
    log("")
    log("=== 所有 python 进程 ===")
    log(out2.stdout.strip() or "(无)")
except Exception as e:
    log("ps2 失败: " + str(e))

print("\n".join(L))
