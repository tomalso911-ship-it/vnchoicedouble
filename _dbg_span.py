import sqlite3, io
from playwright.sync_api import sync_playwright

OUT = []
c = sqlite3.connect("agi_pm.db"); c.row_factory = sqlite3.Row
pw = c.execute("SELECT password FROM users WHERE lower(username)='tom'").fetchone()[0]
c.close()

P = """(function(){
  var s=document.querySelector('#view-production .prod-sub');
  var ph=s?s.parentElement:null;
  var cs=s?getComputedStyle(s):null, cp=ph?getComputedStyle(ph):null;
  return JSON.stringify({
    inner: innerWidth,
    span: s?{w:Math.round(s.getBoundingClientRect().width), sw:s.scrollWidth,
             display:cs.display, width:cs.width, minWidth:cs.minWidth, ws:cs.whiteSpace,
             flex:cs.flex, maxWidth:cs.maxWidth, text:(s.textContent||'').slice(0,40)}:null,
    ph: ph?{w:Math.round(ph.getBoundingClientRect().width), sw:ph.scrollWidth, display:cp.display,
            wrap:cp.flexWrap, ws:cp.whiteSpace}:null
  });
})()"""

try:
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width":390,"height":844}, is_mobile=True, has_touch=True, device_scale_factor=2)
        pg.goto("http://127.0.0.1:5050/lite", wait_until="domcontentloaded", timeout=25000)
        pg.wait_for_timeout(2200)
        pg.fill("#loginUser","tom"); pg.fill("#loginPwd",pw); pg.click("#loginBtn")
        pg.wait_for_timeout(3500)
        pg.evaluate("switchView('production')"); pg.wait_for_timeout(2500)
        OUT.append(pg.evaluate(P))
        b.close()
except Exception as ex:
    OUT.append("ERR %s" % ex)
io.open("_dbg_span_out.txt","w",encoding="utf-8").write("\n".join(OUT))
