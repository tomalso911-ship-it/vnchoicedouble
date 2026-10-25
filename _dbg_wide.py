import sqlite3, io
from playwright.sync_api import sync_playwright

OUT = []
c = sqlite3.connect("agi_pm.db"); c.row_factory = sqlite3.Row
pw = c.execute("SELECT password FROM users WHERE lower(username)='tom'").fetchone()[0]
c.close()

SCAN = """(function(){
  var root=document.querySelector('#app .view.active')||document.body;
  var out=[];
  var all=root.querySelectorAll('*');
  for (var i=0;i<all.length;i++){
    var el=all[i], r=el.getBoundingClientRect();
    if (r.width>392 || el.scrollWidth>392){
      out.push({tag:el.tagName.toLowerCase(), id:el.id||'', cls:(el.className&&el.className.toString?el.className.toString():'').slice(0,60),
                w:Math.round(r.width), sw:el.scrollWidth, ws:getComputedStyle(el).whiteSpace});
      if (out.length>14) break;
    }
  }
  return JSON.stringify({inner:innerWidth, items:out});
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
        OUT.append("production " + pg.evaluate(SCAN))
        pg.evaluate("switchView('install')"); pg.wait_for_timeout(2000)
        OUT.append("install " + pg.evaluate(SCAN))
        b.close()
except Exception as ex:
    OUT.append("ERR %s" % ex)
io.open("_dbg_wide_out.txt","w",encoding="utf-8").write("\n".join(OUT))
