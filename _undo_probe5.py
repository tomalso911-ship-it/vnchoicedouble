# -*- coding: utf-8 -*-
"""用页面内的 finUndoDiag() 钩子拿撤销机制的真实状态。"""
import json
from playwright.sync_api import sync_playwright

F = open("_undo5.txt", "w", encoding="utf-8")


def P(*a):
    s = " ".join(str(x) for x in a)
    F.write(s + "\n")
    F.flush()
    print(s, flush=True)


URL = "http://127.0.0.1:5050/lite?v=undodiag5"

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True, args=["--no-sandbox"])
    try:
        pg = b.new_context(viewport={"width": 1400, "height": 900}).new_page()
        pg.set_default_timeout(25000)
        pg.goto(URL, wait_until="domcontentloaded", timeout=45000)
        pg.wait_for_timeout(600)
        if pg.evaluate("() => { var e=document.getElementById('loginPage'); return e && !e.classList.contains('hidden'); }"):
            pg.fill("#loginUser", "tom")
            pg.fill("#loginPwd", "66668888")
            pg.click("#loginBtn")
        pg.wait_for_selector("#topbar:not(.hidden)", timeout=20000)
        pg.evaluate("() => switchView('finance')")
        pg.wait_for_function("() => !!(window.finReady && document.querySelector('#univer_container canvas'))", timeout=60000)
        pg.wait_for_timeout(3000)

        P("hasHook: %s" % pg.evaluate("() => typeof window.finUndoDiag"))
        P("### D0 载入后静止态")
        P(json.dumps(pg.evaluate("() => window.finUndoDiag()"), ensure_ascii=False, indent=1))

        def zz():
            return pg.evaluate("""() => {
              var sn = window.fin_currentSnapshot();
              var sid = sn.sheetOrder[0], cd = sn.sheets[sid].cellData, hit = [];
              for (var rk in cd) for (var ck in cd[rk]) {
                var v = cd[rk][ck] && cd[rk][ck].v;
                if (String(v).indexOf('QQTEST') >= 0) hit.push(rk + ',' + ck);
              }
              return hit;
            }""")

        P("### 真编辑")
        pg.click("#univer_container", position={"x": 320, "y": 210})
        pg.wait_for_timeout(250)
        pg.keyboard.type("QQTEST", delay=45)
        pg.wait_for_timeout(250)
        pg.keyboard.press("Enter")
        pg.wait_for_timeout(1600)
        P("  含 QQTEST: %s" % json.dumps(zz()))
        P("### D1 编辑后")
        P(json.dumps(pg.evaluate("() => window.finUndoDiag()"), ensure_ascii=False, indent=1))

        P("### Ctrl+Z")
        pg.keyboard.press("Control+z")
        pg.wait_for_timeout(1600)
        P("  含 QQTEST: %s" % json.dumps(zz()))
        P("### D2 撤销后")
        P(json.dumps(pg.evaluate("() => window.finUndoDiag()"), ensure_ascii=False, indent=1))

        P("### 再按 3 次 Ctrl+Z")
        for i in range(3):
            pg.keyboard.press("Control+z")
            pg.wait_for_timeout(700)
        P("  含 QQTEST: %s" % json.dumps(zz()))
        P(json.dumps(pg.evaluate("() => window.finUndoDiag()"), ensure_ascii=False, indent=1))
    except Exception as e:
        P("FAIL: %r" % e)
    finally:
        try:
            b.close()
        except Exception:
            pass
        F.close()
