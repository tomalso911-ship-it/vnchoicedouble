import sqlite3, io
from playwright.sync_api import sync_playwright

OUT = []
c = sqlite3.connect("agi_pm.db"); c.row_factory = sqlite3.Row
pw = c.execute("SELECT password FROM users WHERE lower(username)='tom'").fetchone()[0]
c.close()

P = """(function(){
  var s=document.querySelector('#view-production .prod-sub');
  return JSON.stringify({inner:innerWidth, docW:document.documentElement.scrollWidth,
    barTop:getComputedStyle(document.getElementById('topbar')).top,
    prodSubMinW:s?s.style.minWidth:null});
})()"""

try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width":1440,"height":900})
        errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)[:160]))
        pg.goto("http://127.0.0.1:5050/lite", wait_until="domcontentloaded", timeout=25000)
        pg.wait_for_timeout(2200)
        pg.fill("#loginUser","tom"); pg.fill("#loginPwd",pw); pg.click("#loginBtn")
        pg.wait_for_timeout(3500)
        pg.evaluate("switchView('production')"); pg.wait_for_timeout(2500)
        OUT.append(pg.evaluate(P)); OUT.append("errs=%s" % errs)
        pg.screenshot(path="_desk_prod.png")
        b.close()
except Exception as ex:
    OUT.append("ERR %s" % ex)
io.open("_dbg_desk_out.txt","w",encoding="utf-8").write("\n".join(OUT))
