import sqlite3, io
from playwright.sync_api import sync_playwright

OUT = []
c = sqlite3.connect("agi_pm.db"); c.row_factory = sqlite3.Row
pw = c.execute("SELECT password FROM users WHERE lower(username)='tom'").fetchone()[0]
c.close()

VIEWS = ["dashboard", "won", "worklog", "production", "install", "finance", "library", "equity", "approvals", "users"]

P = """(function(){
  var d=document.documentElement;
  var tb=document.getElementById('topbar');
  var cs=tb?getComputedStyle(tb):null;
  var items=document.querySelectorAll('#tbMenu .tb-item');
  var vis=0;
  for(var i=0;i<items.length;i++){ var r=items[i].getBoundingClientRect(); if(r.width>0 && r.height>0) vis++; }
  return JSON.stringify({
    inner:innerWidth, docW:d.scrollWidth, over:(d.scrollWidth-innerWidth),
    barBottom:cs?cs.bottom:null, barH:cs?Math.round(parseFloat(cs.height)):null,
    tabs:items.length, tabsVisible:vis,
    note:(function(){var n=document.querySelector('.mapp-note');return n?n.textContent.slice(0,26):'';})()
  });
})()"""

try:
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width":390,"height":844}, is_mobile=True, has_touch=True, device_scale_factor=2)
        errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)[:160]))
        pg.goto("http://127.0.0.1:5050/lite", wait_until="domcontentloaded", timeout=25000)
        pg.wait_for_timeout(2200)
        pg.fill("#loginUser","tom"); pg.fill("#loginPwd",pw); pg.click("#loginBtn")
        pg.wait_for_timeout(4000)
        for v in VIEWS:
            pg.evaluate("switchView('%s')" % v); pg.wait_for_timeout(1600)
            OUT.append("%s %s" % (v, pg.evaluate(P)))
            if v in ("production", "finance", "equity"):
                pg.screenshot(path="_m_%s.png" % v)
        OUT.append("errs=%s" % errs)
        pg.close()

        # 桌面回归
        pg2 = b.new_page(viewport={"width":1440,"height":900})
        errs2=[]; pg2.on("pageerror", lambda e: errs2.append(str(e)[:160]))
        pg2.goto("http://127.0.0.1:5050/lite", wait_until="domcontentloaded", timeout=25000)
        pg2.wait_for_timeout(2200)
        pg2.fill("#loginUser","tom"); pg2.fill("#loginPwd",pw); pg2.click("#loginBtn")
        pg2.wait_for_timeout(4000)
        for v in ("production", "finance"):
            pg2.evaluate("switchView('%s')" % v); pg2.wait_for_timeout(2000)
            OUT.append("DESK %s %s" % (v, pg2.evaluate(P)))
        pg2.screenshot(path="_m_desk.png")
        OUT.append("desk_errs=%s" % errs2)
        b.close()
except Exception as ex:
    OUT.append("ERR %s" % ex)
io.open("_dbg_mobile2_out.txt","w",encoding="utf-8").write("\n".join(OUT))
