# -*- coding: utf-8 -*-
"""中文界面下右键【行头】→ 展开「插入」子菜单 → dump 菜单项。
   目的：确认 ①「排序」还在不在；②「插入」子菜单里各项的真实文案与是否有行数输入栏。
   临时目录，不碰真实数据。"""
import datetime, io, os, shutil, socket, sys, tempfile, threading, time

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "_menu_probe2_out.txt")
LOG = []


def log(s):
    LOG.append("[%s] %s" % (datetime.datetime.now().strftime("%H:%M:%S"), s))
    io.open(OUT, "w", encoding="utf-8").write("\n".join(LOG) + "\n")


def port_open(p):
    s = socket.socket(); s.settimeout(0.6)
    try:
        s.connect(("127.0.0.1", p)); return True
    except Exception:
        return False
    finally:
        s.close()


import app
from playwright.sync_api import sync_playwright

TMP = tempfile.mkdtemp(prefix="menup2_")
app.FIN_DIR = TMP
app.CN_REPORT = os.path.join(TMP, "cn_report.xlsx")
app.CN_SNAP_KEY = os.path.join(TMP, "cn_report.snapshot.key")
app.CN_SNAP_PREFIX = "cn_report.snapshot."
app.CN_TITLES_PATH = os.path.join(TMP, "fin_sheet_titles_cn.json")
app._cn_seed_if_missing()
PORT = 5176
BASE = "http://127.0.0.1:%d/lite" % PORT
if not port_open(PORT):
    threading.Thread(target=lambda: app.app.run(host="127.0.0.1", port=PORT, debug=False,
                                                use_reloader=False, threaded=True), daemon=True).start()
    for _ in range(60):
        if port_open(PORT):
            break
        time.sleep(0.3)

DUMP = """() => {
  var out = [];
  var els = document.querySelectorAll('.univer-menu li, [role="menuitem"], .univer-menu-item, .univer-menu-submenu-title');
  var seen = {};
  for (var i = 0; i < els.length; i++){
    var e = els[i];
    var t = (e.textContent || '').replace(/\\s+/g, ' ').trim();
    if (!t || seen[t + e.className]) continue;
    seen[t + e.className] = 1;
    var inp = e.querySelector('input');
    var r = e.getBoundingClientRect();
    out.push(t.slice(0, 30) + ' | cls=' + String(e.className).replace('univer-menu-', '') +
             ' | input=' + (inp ? '"' + inp.value + '"' : '-') +
             ' | xy=' + Math.round(r.left) + ',' + Math.round(r.top));
  }
  return out;
}"""

RECT_OF = """(txt) => {
  var els = document.querySelectorAll('.univer-menu-submenu-title, .univer-menu-item');
  for (var i = 0; i < els.length; i++){
    var t = (els[i].textContent || '').replace(/\\s+/g, ' ').trim();
    if (t === txt){ var r = els[i].getBoundingClientRect(); return { x: r.left + r.width * 0.5, y: r.top + r.height * 0.5 }; }
  }
  return null;
}"""

BIGCANVAS = """() => {
  var cs = document.querySelectorAll('canvas'), best = null, a = 0;
  for (var i = 0; i < cs.length; i++){
    var r = cs[i].getBoundingClientRect(), ar = r.width * r.height;
    if (ar > a){ a = ar; best = { l: r.left, t: r.top, w: r.width, h: r.height }; }
  }
  return best;
}"""

errors = []
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True, args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 1500, "height": 950})
    pg.on("pageerror", lambda e: errors.append(str(e)[:150]))
    pg.goto(BASE, wait_until="domcontentloaded")
    pg.wait_for_timeout(1200)
    pg.fill("#loginUser", "tom"); pg.fill("#loginPwd", "66668888"); pg.click("#loginBtn")
    pg.wait_for_selector("#topbar:not(.hidden)", timeout=25000)
    pg.evaluate("() => { try { switchView('finance'); } catch(e){} }")
    pg.wait_for_timeout(600)
    pg.evaluate("() => { try { setLangDebug('zh'); } catch(e){} }")
    pg.wait_for_timeout(1200)
    pg.evaluate("() => { var t = document.querySelector('#fin-tabs .fin-tab[data-key=\\'cn\\']'); if (t) t.click(); }")
    for _ in range(70):
        pg.wait_for_timeout(400)
        if pg.evaluate("() => (typeof finReady !== 'undefined') && !!finReady"):
            break
    pg.wait_for_timeout(3000)

    cv = pg.evaluate(BIGCANVAS)
    log("最大 canvas = %s" % cv)

    def probe(name, x, y):
        pg.mouse.click(x, y, button="right")
        pg.wait_for_timeout(1100)
        items = pg.evaluate(DUMP)
        log("")
        log("=== 右键「%s」(%.0f,%.0f) 菜单：%d 项 ===" % (name, x, y, len(items)))
        for it in items:
            log("   %s" % it)
        return items

    probe("行头第6行", cv["l"] + 20, cv["t"] + 26 + 5 * 24)
    pg.keyboard.press("Escape"); pg.wait_for_timeout(400)
    probe("列头C列", cv["l"] + 46 + 200, cv["t"] + 12)
    pg.keyboard.press("Escape"); pg.wait_for_timeout(400)
    probe("单元格", cv["l"] + 46 + 200, cv["t"] + 26 + 5 * 24)

    log("")
    log("④ 在单元格菜单里悬停「插入」展开子菜单")
    for label in ("Insert", "插入"):
        pos = pg.evaluate(RECT_OF, label)
        if pos:
            pg.mouse.move(pos["x"], pos["y"])
            pg.wait_for_timeout(900)
            sub = pg.evaluate(DUMP)
            log("   悬停「%s」后：%d 项" % (label, len(sub)))
            for it in sub:
                log("      %s" % it)
            break

    log("")
    log("页面报错 = %s" % errors[:5])
    pg.screenshot(path=os.path.join(HERE, "_menu_probe2.png"))
    b.close()
shutil.rmtree(TMP, ignore_errors=True)
log("临时目录已清理")
print("\n".join(LOG))
