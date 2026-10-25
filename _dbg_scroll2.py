import sqlite3, io, hashlib
from playwright.sync_api import sync_playwright

out = []
c = sqlite3.connect("agi_pm.db")
c.row_factory = sqlite3.Row
r = c.execute("SELECT username, password FROM users WHERE lower(username)='minh'").fetchone()
c.close()
user, pwd = r["username"], r["password"]

def h(img):
    return hashlib.md5(img).hexdigest()[:10]

try:
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1500, "height": 900})
        errs = []
        pg.on("pageerror", lambda e: errs.append("PAGEERROR %s" % str(e)[:200]))
        pg.goto("http://127.0.0.1:5050/lite", wait_until="domcontentloaded")
        pg.wait_for_timeout(3500)
        pg.fill("#loginUser", user)
        pg.fill("#loginPwd", pwd)
        pg.click("#loginBtn")
        pg.wait_for_timeout(4000)
        pg.evaluate("switchView('equity')")
        pg.wait_for_timeout(9000)
        el = pg.query_selector("#equity_container canvas")
        out.append("canvas: %s" % bool(el))
        s0 = el.screenshot()
        box = el.bounding_box()
        pg.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
        pg.mouse.wheel(0, 500)
        pg.wait_for_timeout(900)
        s1 = el.screenshot()
        out.append("wheel changed canvas: %s (%s -> %s)" % (h(s0) != h(s1), h(s0), h(s1)))
        pg.keyboard.press("PageDown")
        pg.wait_for_timeout(700)
        s2 = el.screenshot()
        out.append("PageDown changed canvas: %s (%s)" % (h(s1) != h(s2), h(s2)))
        # 再滚回顶部试试（确认能往返）
        pg.mouse.wheel(0, -2000)
        pg.wait_for_timeout(900)
        s3 = el.screenshot()
        out.append("wheel-up changed canvas: %s" % (h(s2) != h(s3)))
        out.append("---- errors ----")
        for e in errs:
            if e:
                out.append(e)
        b.close()
except Exception as ex:
    out.append("SCRIPT_ERR %s" % ex)
io.open("_dbg_scroll2_out.txt", "w", encoding="utf-8").write("\n".join(out))
