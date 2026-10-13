# -*- coding: utf-8 -*-
"""确认锁死区启动自检在真实浏览器里跑过且通过（window.__FIN_CN_LOCK_FAILED 不得为 true）。"""
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_verify_lock_boot_out.txt")
L = []


def log(s):
    L.append(s)
    io.open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(s)


with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True, args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 1500, "height": 900})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append("console.error: " + m.text) if m.type == "error" else None)
    pg.goto("http://127.0.0.1:5050/lite", wait_until="domcontentloaded")
    pg.wait_for_timeout(1500)
    pg.fill("#loginUser", "tom")
    pg.fill("#loginPwd", "66668888")
    pg.click("#loginBtn")
    pg.wait_for_selector("#topbar:not(.hidden)", timeout=20000)
    pg.evaluate("() => { try { switchView('finance'); } catch(e){} }")
    pg.wait_for_timeout(1200)
    pg.evaluate("() => { var t = document.querySelector('#fin-tabs .fin-tab[data-key=\\'cn\\']'); if (t) t.click(); }")
    for _ in range(70):
        pg.wait_for_timeout(500)
        if pg.evaluate("() => (typeof finReady !== 'undefined') && !!finReady"):
            break
    pg.wait_for_timeout(2500)
    r = pg.evaluate("""() => ({
      failed: window.__FIN_CN_LOCK_FAILED,
      bad: (typeof finCnLockCheck === 'function') ? finCnLockCheck() : 'NO-FUNC',
      stat: (typeof window.__finStatInfo !== 'undefined') ? window.__finStatInfo : null
    })""")
    log("启动自检结果 = %s" % json.dumps(r, ensure_ascii=False))
    log("自检是否通过 = %s" % ("✔ 通过" if (not r.get("failed") and r.get("bad") == []) else "✘ 失败"))
    log("页面报错 = %s" % (errs[:5] if errs else "无"))
    b.close()
