# -*- coding: utf-8 -*-
"""右键行头/单元格 → dump 菜单项，确认「排序」是否还在、插入行项长什么样。临时目录，不碰真实数据。"""
import datetime, io, os, shutil, socket, sys, tempfile, threading, time

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "_menu_probe_out.txt")
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

TMP = tempfile.mkdtemp(prefix="menup_")
app.FIN_DIR = TMP
app.CN_REPORT = os.path.join(TMP, "cn_report.xlsx")
app.CN_SNAP_KEY = os.path.join(TMP, "cn_report.snapshot.key")
app.CN_SNAP_PREFIX = "cn_report.snapshot."
app.CN_TITLES_PATH = os.path.join(TMP, "fin_sheet_titles_cn.json")
app._cn_seed_if_missing()
PORT = 5175
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
  var els = document.querySelectorAll('.univer-menu li, [role="menuitem"], .univer-menu-item');
  for (var i = 0; i < els.length; i++){
    var e = els[i];
    var t = (e.textContent || '').replace(/\\s+/g, ' ').trim();
    if (!t) continue;
    var inp = e.querySelector('input');
    out.push(t.slice(0, 40) + ' || cls=' + String(e.className).slice(0, 70) +
             ' || disp=' + (e.style && e.style.display) +
             ' || input=' + (inp ? ('"' + inp.value + '"') : '-'));
  }
  return out;
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
    pg.evaluate("() => { var t = document.querySelector('#fin-tabs .fin-tab[data-key=\\'cn\\']'); if (t) t.click(); }")
    for _ in range(70):
        pg.wait_for_timeout(400)
        if pg.evaluate("() => (typeof finReady !== 'undefined') && !!finReady"):
            break
    pg.wait_for_timeout(3000)

    rect = pg.evaluate("""() => {
      var c = document.querySelector('#univer_container') || document.body;
      var r = c.getBoundingClientRect();
      return { l: r.left, t: r.top, w: r.width, h: r.height };
    }""")
    log("容器 = %s" % rect)

    for name, x, y in (("行头", rect["l"] + 25, rect["t"] + 60 + 5 * 24),
                       ("单元格", rect["l"] + 260, rect["t"] + 60 + 5 * 24),
                       ("列头", rect["l"] + 260, rect["t"] + 14)):
        pg.mouse.click(x, y, button="right")
        pg.wait_for_timeout(1000)
        items = pg.evaluate(DUMP)
        log("")
        log("=== 右键「%s」处菜单（%d 项）===" % (name, len(items)))
        for it in items:
            log("   %s" % it)
        pg.keyboard.press("Escape")
        pg.wait_for_timeout(400)

    log("")
    log("页面报错 = %s" % errors[:5])
    b.close()
shutil.rmtree(TMP, ignore_errors=True)
log("临时目录已清理")
print("\n".join(LOG))
