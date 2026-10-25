import sqlite3, io, json
from playwright.sync_api import sync_playwright

OUT = []
c = sqlite3.connect("agi_pm.db"); c.row_factory = sqlite3.Row
pw = {r["username"]: r["password"] for r in c.execute("SELECT username,password FROM users WHERE lower(username)='tom'").fetchall()}
c.close()

VIEWS = ["dashboard", "won", "worklog", "production", "install", "finance", "library", "equity", "approvals", "users"]

try:
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)[:160]))
        pg.goto("http://127.0.0.1:5050/lite", wait_until="domcontentloaded", timeout=25000)
        pg.wait_for_timeout(2500)
        pg.fill("#loginUser", "tom"); pg.fill("#loginPwd", pw["tom"]); pg.click("#loginBtn")
        pg.wait_for_timeout(4000)
        for v in VIEWS:
            try:
                pg.evaluate("switchView('%s')" % v)
            except Exception as e:
                OUT.append("%s switch ERR %s" % (v, str(e)[:80])); continue
            pg.wait_for_timeout(2200)
            info = pg.evaluate("""(function(){
              var d=document.documentElement, b=document.body;
              var view=document.querySelector('#app .view.active');
              var tb=document.getElementById('topbar');
              var cs=tb?getComputedStyle(tb):null;
              return JSON.stringify({
                docW: d.scrollWidth, winW: innerWidth,
                bodyW: b.scrollWidth,
                viewW: view?view.scrollWidth:null,
                viewH: view?Math.round(view.getBoundingClientRect().height):null,
                barBottom: cs?cs.bottom:null,
                over: (d.scrollWidth - innerWidth)
              });
            })()""")
            OUT.append("%s %s" % (v, info))
            pg.screenshot(path="_phone_%s.png" % v, full_page=False)
        OUT.append("errs=%s" % errs)
        b.close()
except Exception as ex:
    OUT.append("ERR %s" % ex)
io.open("_dbg_phone_sweep_out.txt", "w", encoding="utf-8").write("\n".join(OUT))
