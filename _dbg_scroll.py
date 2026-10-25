import sqlite3, io
from playwright.sync_api import sync_playwright

out = []
c = sqlite3.connect("agi_pm.db")
c.row_factory = sqlite3.Row
r = c.execute("SELECT username, password FROM users WHERE lower(username)='minh'").fetchone()
c.close()
user, pwd = r["username"], r["password"]

try:
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1500, "height": 900})
        errs = []
        pg.on("pageerror", lambda e: errs.append("PAGEERROR %s" % str(e)[:200]))
        pg.on("console", lambda m: errs.append("CONSOLE[%s] %s" % (m.type, m.text[:200])) if m.type == "error" else None)
        pg.goto("http://127.0.0.1:5050/lite", wait_until="domcontentloaded")
        pg.wait_for_timeout(3500)
        pg.fill("#loginUser", user)
        pg.fill("#loginPwd", pwd)
        pg.click("#loginBtn")
        pg.wait_for_timeout(4000)
        # 进入股东权益
        pg.evaluate("switchView('equity')")
        pg.wait_for_timeout(9000)
        out.append("equity canvas: %s" % pg.evaluate("!!document.querySelector('#equity_container canvas')"))
        out.append("ro-lock installed: %s" % pg.evaluate("(function(){var c=window.__eqCmdSvc;return !!(c&&c.__eqPermRoPatched);})()"))
        out.append("sheetLv 总投资数据: %s" % pg.evaluate("window.__eqPermSheetLv ? window.__eqPermSheetLv('总投资数据') : 'no-fn'"))
        # 找 Univer 垂直滚动条 thumb（transform 会随滚动变化）
        thumb_info = pg.evaluate("""(function(){
          var els = document.querySelectorAll('#equity_container [class*="scrollbar"] [class*="thumb"], #equity_container [class*="scroll-bar"] > div');
          var arr = [];
          els.forEach(function(e){ var r = e.getBoundingClientRect(); if (r.height > 8 && r.width > 4) arr.push({cls: e.className.toString().slice(0,60), y: Math.round(r.top), h: Math.round(r.height), transform: e.style.transform || ''}); });
          return JSON.stringify(arr.slice(0, 6));
        })()""")
        out.append("thumbs before: %s" % thumb_info)
        # 在 canvas 上滚轮
        box = pg.evaluate("(function(){var c=document.querySelector('#equity_container canvas'); if(!c) return null; var r=c.getBoundingClientRect(); return {x:r.x+r.width/2, y:r.y+r.height/2};})()")
        if box:
            pg.mouse.move(box["x"], box["y"])
            pg.mouse.wheel(0, 400)
            pg.wait_for_timeout(800)
        thumb_after = pg.evaluate("""(function(){
          var els = document.querySelectorAll('#equity_container [class*="scrollbar"] [class*="thumb"], #equity_container [class*="scroll-bar"] > div');
          var arr = [];
          els.forEach(function(e){ var r = e.getBoundingClientRect(); if (r.height > 8 && r.width > 4) arr.push({cls: e.className.toString().slice(0,60), y: Math.round(r.top), h: Math.round(r.height), transform: e.style.transform || ''}); });
          return JSON.stringify(arr.slice(0, 6));
        })()""")
        out.append("thumbs after wheel: %s" % thumb_after)
        # 用键盘 PageDown 试试（导航键我们放行了）
        pg.keyboard.press("PageDown")
        pg.wait_for_timeout(600)
        thumb_pgd = pg.evaluate("""(function(){
          var els = document.querySelectorAll('#equity_container [class*="scrollbar"] [class*="thumb"], #equity_container [class*="scroll-bar"] > div');
          var arr = [];
          els.forEach(function(e){ var r = e.getBoundingClientRect(); if (r.height > 8 && r.width > 4) arr.push({y: Math.round(r.top)}); });
          return JSON.stringify(arr.slice(0, 6));
        })()""")
        out.append("thumbs after PageDown: %s" % thumb_pgd)
        out.append("---- errors ----")
        for e in errs:
            if e:
                out.append(e)
        b.close()
except Exception as ex:
    out.append("SCRIPT_ERR %s" % ex)
io.open("_dbg_scroll_out.txt", "w", encoding="utf-8").write("\n".join(out))
