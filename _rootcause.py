# -*- coding: utf-8 -*-
"""根因排查：① 5050 现在是谁在服务；② 我的新路由在【当前 app.py】里到底注册了没有；
③ 启动 new code 会不会直接报错（所以重启失败、老进程继续服务）——_rootcause_out.txt"""
import io
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "_rootcause_out.txt")
L = []


def log(s):
    L.append(str(s))
    io.open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")


def run(cmd, timeout=120):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                           encoding="utf-8", errors="replace",
                           cwd=HERE, env=dict(os.environ, PYTHONIOENCODING="utf-8"))
        return r.returncode, (r.stdout or ""), (r.stderr or "")
    except Exception as e:
        return -1, "", str(e)


log("=== ① 现在谁在监听 5050 ===")
ps = ("Get-NetTCPConnection -LocalPort 5050 -State Listen -ErrorAction SilentlyContinue | "
      "ForEach-Object { $p = Get-CimInstance Win32_Process -Filter ('ProcessId=' + $_.OwningProcess); "
      "'PID=' + $_.OwningProcess + ' | start=' + $p.CreationDate + ' | ' + $p.CommandLine }")
rc, out, err = run(["powershell", "-NoProfile", "-Command", ps])
log(out.strip() or "(没人监听 5050)")
if err.strip():
    log("  stderr: " + err.strip()[:200])

log("")
log("=== ② 导入当前 app.py，看新路由注册情况（不启服务） ===")
py = ("import app, sys\n"
      "rs = sorted(str(r) for r in app.app.url_map.iter_rules() if 'cn-report' in str(r))\n"
      "print('CN_ROUTES=', len(rs))\n"
      "for r in rs: print('   ', r)\n"
      "print('HAS_CN_SEED=', hasattr(app, '_cn_seed_if_missing'))\n"
      "print('CN_REPORT=', getattr(app, 'CN_REPORT', None))\n")
rc, out, err = run([sys.executable, "-c", py], timeout=180)
log("exit=%s" % rc)
log(out.strip() or "(无输出)")
if err.strip():
    log("--- stderr ---")
    log(err.strip()[:4000])

log("")
log("=== ③ 真正跑一次 app.py，看会不会启动失败（端口被占用时的表现） ===")
rc, out, err = run([sys.executable, "app.py"], timeout=25)
log("exit=%s (超时/被占用都正常，重点看有没有 Traceback)" % rc)
tail = (out or "")[-2500:]
log(tail.strip() or "(stdout 无输出)")
if err.strip():
    log("--- stderr ---")
    log(err.strip()[-2500:])

log("")
log("=== ④ 仓库里可能的其它入口 ===")
for pat in ("*.bat", "*.cmd", "*.spec", "*.exe", "app.py"):
    for p in sorted(__import__("glob").glob(os.path.join(HERE, pat))):
        log("  %s  (%d bytes)" % (os.path.basename(p), os.path.getsize(p)))
import glob as _g
for p in sorted(_g.glob(os.path.join(HERE, "**", "app.py"), recursive=True)):
    log("  app.py 副本: %s" % p)

print("\n".join(L))
