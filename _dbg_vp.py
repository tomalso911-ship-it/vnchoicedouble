import sqlite3, io
from playwright.sync_api import sync_playwright

OUT = []
c = sqlite3.connect("agi_pm.db"); c.row_factory = sqlite3.Row
pw = c.execute("SELECT password FROM users WHERE lower(username)='tom'").fetchone()[0]
c.close()

P = """(function(){var m=document.querySelector('meta[name=viewport]');
return JSON.stringify({inner:innerWidth, client:document.documentElement.clientWidth,
 dpr:devicePixelRatio, vv: visualViewport?Math.round(visualViewport.width):null,
 scale: visualViewport?visualViewport.scale:null, meta:m?m.getAttribute('content'):null});})()"""

try:
    with sync_playwright() as p:
        b = p.chromium.launch()
        for mobile in (False, True):
            pg = b.new_page(viewport={"width":390,"height":844}, is_mobile=mobile, has_touch=mobile, device_scale_factor=2 if mobile else 1)
            pg.goto("http://127.0.0.1:5050/lite", wait_until="domcontentloaded", timeout=25000)
            pg.wait_for_timeout(2200)
            pg.fill("#loginUser","tom"); pg.fill("#loginPwd",pw); pg.click("#loginBtn")
            pg.wait_for_timeout(3500)
            OUT.append("mobile=%s dashboard %s" % (mobile, pg.evaluate(P)))
            pg.evaluate("switchView('production')"); pg.wait_for_timeout(2500)
            OUT.append("mobile=%s production %s" % (mobile, pg.evaluate(P)))
            pg.evaluate("switchView('install')"); pg.wait_for_timeout(2000)
            OUT.append("mobile=%s install %s" % (mobile, pg.evaluate(P)))
            pg.close()
        b.close()
except Exception as ex:
    OUT.append("ERR %s" % ex)
io.open("_dbg_vp_out.txt","w",encoding="utf-8").write("\n".join(OUT))
