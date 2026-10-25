# -*- coding: utf-8 -*-
"""埋点：记录每条 column-width 报错发生时 #univer_container 的实测尺寸，判断过滤器是否生效。"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_verify_colwarn_fix2_out.txt")
L = []


def log(s):
    L.append(str(s))
    io.open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(s)


log("start")

from playwright.sync_api import sync_playwright  # noqa: E402

HOOK = """
() => {
  window.__cerr = [];
  var oe = console.error;
  console.error = function(){
    try {
      var t = String(arguments[0]||'');
      if (/column width is less than 0/i.test(t)) {
        var el = document.getElementById('univer_container');
        window.__cerr.push({
          m: t.slice(0,60),
          w: el ? el.offsetWidth : -1,
          h: el ? el.offsetHeight : -1,
          r: el && el.getClientRects ? el.getClientRects().length : -1,
          disp: el ? (el.style.display || '(default)') : 'NULL'
        });
      }
    } catch(e){}
    return oe.apply(console, arguments);
  };
}
"""

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True, args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 1500, "height": 900})
    pg.goto("http://127.0.0.1:5050/lite", wait_until="domcontentloaded")
    pg.wait_for_timeout(1200)
    pg.fill("#loginUser", "tom")
    pg.fill("#loginPwd", "66668888")
    pg.click("#loginBtn")
    pg.wait_for_selector("#topbar:not(.hidden)", timeout=15000)
    pg.evaluate("() => { try { switchView('finance'); } catch(e){} }")
    pg.wait_for_timeout(12000)
    pg.evaluate(HOOK)

    def drain(tag):
        r = pg.evaluate("() => { var a = window.__cerr||[]; window.__cerr=[]; return a; }")
        log("[%s] 漏网 %d" % (tag, len(r)))
        for x in r:
            log("    " + str(x))
        return len(r)

    def edit(col=0):
        pg.evaluate("(c) => { try { finUniverAPI.getActiveWorkbook().getActiveSheet().getRange(6, c).activate(); } catch(e){} }", col)
        pg.wait_for_timeout(250)
        pg.keyboard.press("F2")
        pg.wait_for_timeout(500)
        pg.keyboard.press("Escape")
        pg.wait_for_timeout(250)

    pg.evaluate("() => { var el = document.getElementById('univer_container'); if (el) el.style.display = 'none'; }")
    pg.wait_for_timeout(600)
    log("隐藏后实测: " + str(pg.evaluate("() => { var el=document.getElementById('univer_container'); return {w:el.offsetWidth,h:el.offsetHeight,r:el.getClientRects().length}; }")))
    edit(0)
    drain("容器 display:none 时编辑")
    pg.evaluate("() => { var el = document.getElementById('univer_container'); if (el) el.style.display = ''; }")
    pg.wait_for_timeout(800)

    pg.evaluate("() => { var el = document.getElementById('univer_container'); if (el) el.style.width = '0px'; }")
    pg.wait_for_timeout(600)
    edit(0)
    drain("容器 width:0 时编辑")
    pg.evaluate("() => { var el = document.getElementById('univer_container'); if (el) el.style.width = ''; }")
    pg.wait_for_timeout(800)

    b.close()
log("done")
