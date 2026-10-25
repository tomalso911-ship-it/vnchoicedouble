import sqlite3, io
from playwright.sync_api import sync_playwright

OUT = []
c = sqlite3.connect("agi_pm.db"); c.row_factory = sqlite3.Row
pw = c.execute("SELECT password FROM users WHERE lower(username)='tom'").fetchone()[0]
c.close()

P = """(function(){
  var s=document.querySelector('#view-production .prod-sub');
  if(!s) return 'no span';
  var hits=[];
  for (var i=0;i<document.styleSheets.length;i++){
    var ss=document.styleSheets[i], rules;
    try{ rules=ss.cssRules; }catch(e){ continue; }
    if(!rules) continue;
    (function walk(list, media){
      for (var j=0;j<list.length;j++){
        var r=list[j];
        if (r.type===4){ walk(r.cssRules, r.conditionText); continue; }   // @media
        if (!r.selectorText) continue;
        var sel=r.selectorText;
        try{ if(!s.matches(sel)) continue; }catch(e){ continue; }
        var t=r.style.cssText||'';
        if (/min-width|white-space|width:/.test(t)) hits.push((media?'@media '+media+' ':'')+sel+' { '+t.slice(0,120)+' }');
      }
    })(rules, '');
  }
  var cs=getComputedStyle(s);
  return JSON.stringify({n:document.querySelectorAll('#view-production .prod-sub').length,
    w:Math.round(s.getBoundingClientRect().width), minW:cs.minWidth, ws:cs.whiteSpace,
    html:s.outerHTML.slice(0,120), hits:hits.slice(0,20)}, null, 1);
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
io.open("_dbg_rules_out.txt","w",encoding="utf-8").write("\n".join(OUT))
