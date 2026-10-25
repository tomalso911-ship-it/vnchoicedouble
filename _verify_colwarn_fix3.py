# -*- coding: utf-8 -*-
"""用 Chrome 真实 console 事件（DevTools 协议）判定：只有真正打印到控制台的才算数。"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_verify_colwarn_fix3_out.txt")
L = []


def log(s):
    L.append(str(s))
    io.open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(s)


log("start")

from playwright.sync_api import sync_playwright  # noqa: E402

ERRS = []
INFOS = []
PAGES = []


with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True, args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 1500, "height": 900})
    pg.on("console", lambda m: (
        ERRS.append(m.text[:90]) if (m.type == "error" and "column width" in m.text) else
        INFOS.append(m.text[:150]) if (m.type == "info" and "column width" in m.text) else None))
    pg.on("pageerror", lambda e: PAGES.append(str(e)[:150]))

    pg.goto("http://127.0.0.1:5050/lite", wait_until="domcontentloaded")
    pg.wait_for_timeout(1200)
    pg.fill("#loginUser", "tom")
    pg.fill("#loginPwd", "66668888")
    pg.click("#loginBtn")
    pg.wait_for_selector("#topbar:not(.hidden)", timeout=15000)
    pg.evaluate("() => { try { switchView('finance'); } catch(e){} }")
    pg.wait_for_timeout(12000)

    def drain(tag):
        e, n = list(ERRS), len(INFOS)
        del ERRS[:]
        log("[%s] 真实控制台 error %d 条 / info %d 条" % (tag, len(e), n))
        for x in e[:3]:
            log("    ERR " + x)
        return len(e)

    def edit(col=0):
        pg.evaluate("(c) => { try { finUniverAPI.getActiveWorkbook().getActiveSheet().getRange(6, c).activate(); } catch(e){} }", col)
        pg.wait_for_timeout(250)
        pg.keyboard.press("F2")
        pg.wait_for_timeout(500)
        pg.keyboard.press("Escape")
        pg.wait_for_timeout(250)

    drain("登录后基线")

    pg.evaluate("() => { var el = document.getElementById('univer_container'); if (el) el.style.display = 'none'; }")
    pg.wait_for_timeout(600)
    edit(0)
    drain("容器 display:none 时编辑（修复后应为 0 条 error）")
    pg.evaluate("() => { var el = document.getElementById('univer_container'); if (el) el.style.display = ''; }")
    pg.wait_for_timeout(800)

    pg.evaluate("() => { var el = document.getElementById('univer_container'); if (el) el.style.width = '0px'; }")
    pg.wait_for_timeout(600)
    edit(0)
    drain("容器 width:0 时编辑（修复后应为 0 条 error）")
    pg.evaluate("() => { var el = document.getElementById('univer_container'); if (el) el.style.width = ''; }")
    pg.wait_for_timeout(800)

    edit(4)
    drain("可见时正常编辑")

    pg.evaluate("() => { try { fin_switchTab('merge'); } catch(e){} }")
    pg.wait_for_timeout(1200)
    drain("切到 merge 标签")
    pg.evaluate("() => { try { fin_switchTab('vn'); } catch(e){} }")
    pg.wait_for_timeout(2500)
    drain("切回 vn 标签")

    log("pageerror: " + str(PAGES[:3]))
    b.close()
log("done")
