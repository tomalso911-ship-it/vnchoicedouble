import sqlite3, io
from playwright.sync_api import sync_playwright

OUT = []
c = sqlite3.connect("agi_pm.db"); c.row_factory = sqlite3.Row
pw = c.execute("SELECT password FROM users WHERE lower(username)='tom'").fetchone()[0]
c.close()

P = """(function(){
  var items=document.querySelectorAll('#tbMenu .tb-item');
  var arr=[];
  for(var i=0;i<items.length;i++){
    var it=items[i], cs=getComputedStyle(it);
    arr.push({t:(it.textContent||'').trim(), fs:cs.fontSize, col:cs.color, ov:cs.overflow,
              w:Math.round(it.getBoundingClientRect().width), sw:it.scrollWidth});
  }
  return JSON.stringify(arr);
})()"""

try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width":390,"height":844}, is_mobile=True, has_touch=True, device_scale_factor=2)
        pg.goto("http://127.0.0.1:5050/lite", wait_until="domcontentloaded", timeout=25000)
        pg.wait_for_timeout(2200)
        pg.fill("#loginUser","tom"); pg.fill("#loginPwd",pw); pg.click("#loginBtn")
        pg.wait_for_timeout(4000)
        OUT.append(pg.evaluate(P))
        b.close()
except Exception as ex:
    OUT.append("ERR %s" % ex)
io.open("_dbg_tabs_out.txt","w",encoding="utf-8").write("\n".join(OUT))
