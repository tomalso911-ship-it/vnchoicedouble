# -*- coding: utf-8 -*-
"""针对性验证新前端逻辑 finCnNeedsBlueReload()（全在临时目录）：
   在页面里把 C5 的字体样式直接写成黑色（等价于"从别处粘贴带进来的黑字"），
   然后点「保存」→ 应自动重载成蓝字。"""
import datetime
import io
import os
import shutil
import socket
import sys
import tempfile
import threading
import time

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "_cn_blue5_out.txt")
LOG = []


def log(s):
    LOG.append("[%s] %s" % (datetime.datetime.now().strftime("%H:%M:%S"), s))
    io.open(OUT, "w", encoding="utf-8").write("\n".join(LOG) + "\n")


def port_open(port):
    s = socket.socket()
    s.settimeout(0.6)
    try:
        s.connect(("127.0.0.1", port))
        return True
    except Exception:
        return False
    finally:
        s.close()


import app  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

TMP = tempfile.mkdtemp(prefix="cnblue5_")
app.FIN_DIR = TMP
app.CN_REPORT = os.path.join(TMP, "cn_report.xlsx")
app.CN_SNAP_KEY = os.path.join(TMP, "cn_report.snapshot.key")
app.CN_SNAP_PREFIX = "cn_report.snapshot."
app.CN_TITLES_PATH = os.path.join(TMP, "fin_sheet_titles_cn.json")
log("临时报表目录 = %s" % TMP)
app._cn_seed_if_missing()

PORT = 5161
BASE = "http://127.0.0.1:%d/lite" % PORT
if not port_open(PORT):
    threading.Thread(target=lambda: app.app.run(host="127.0.0.1", port=PORT, debug=False,
                                               use_reloader=False, threaded=True),
                     daemon=True).start()
    for _ in range(60):
        if port_open(PORT):
            break
        time.sleep(0.3)

CELL_JS = """(p) => {
  try {
    var sn = fin_currentSnapshot();
    var sid = sn.sheetOrder[0];
    var cc = ((sn.sheets[sid].cellData || {})[String(p.r)] || {})[String(p.c)];
    if (!cc) return null;
    var s = cc.s;
    if (typeof s === 'string') s = (sn.styles && sn.styles[s]) || null;
    return { v: cc.v, cl: (s && s.cl) ? (s.cl.rgb || s.cl) : null };
  } catch(e){ return 'ERR:' + e.message; }
}"""

SET_BLACK_A = """() => {
  try {
    var sid = fin_currentSnapshot().sheetOrder[0];
    finExecSilent('sheet.command.set-range-values', {
      unitId: fin_unitId(), subUnitId: sid,
      range: { startRow: 4, startColumn: 2, endRow: 4, endColumn: 2 },
      value: [[{ v: 'PASTE-BLACK-A', s: { cl: { rgb: '#000000' } } }]]
    });
    return 'A-sent';
  } catch(e){ return 'A-ERR:' + e.message; }
}"""

SET_BLACK_B = """() => {
  try {
    var sid = fin_currentSnapshot().sheetOrder[0];
    finExecSilent('sheet.command.set-range-values', {
      unitId: fin_unitId(), subUnitId: sid,
      value: { 4: { 2: { v: 'PASTE-BLACK-B', s: { cl: { rgb: '#000000' } } } } }
    });
    return 'B-sent';
  } catch(e){ return 'B-ERR:' + e.message; }
}"""

NEED = "() => { try { return finCnNeedsBlueReload(); } catch(e){ return 'ERR:' + e.message; } }"

errors = []
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True, args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 1500, "height": 950})
    pg.on("pageerror", lambda e: errors.append("pageerror: " + str(e)[:220]))
    pg.on("console", lambda m: errors.append("console.error: " + m.text[:220]) if m.type == "error" else None)
    pg.goto(BASE, wait_until="domcontentloaded")
    pg.wait_for_timeout(1200)
    pg.fill("#loginUser", "tom")
    pg.fill("#loginPwd", "66668888")
    pg.click("#loginBtn")
    pg.wait_for_selector("#topbar:not(.hidden)", timeout=15000)
    pg.evaluate("() => { try { switchView('finance'); } catch(e){} }")
    pg.wait_for_timeout(400)
    pg.evaluate("() => { var t = document.querySelector('#fin-tabs .fin-tab[data-key=\\'cn\\']'); if (t) t.click(); }")
    for _ in range(60):
        pg.wait_for_timeout(400)
        if pg.evaluate("() => (typeof finReady !== 'undefined') && !!finReady"):
            break
    pg.wait_for_timeout(3500)

    log("")
    log("基准：C5 = %s | finCnNeedsBlueReload() = %s (干净数据区应为 False)"
        % (pg.evaluate(CELL_JS, {"r": 4, "c": 2}), pg.evaluate(NEED)))

    log("")
    log("写黑色样式（形状A）-> %s" % pg.evaluate(SET_BLACK_A))
    pg.wait_for_timeout(1500)
    log("   C5 = %s | finCnNeedsBlueReload() = %s" % (pg.evaluate(CELL_JS, {"r": 4, "c": 2}), pg.evaluate(NEED)))
    if pg.evaluate(NEED) is not True:
        log("写黑色样式（形状B）-> %s" % pg.evaluate(SET_BLACK_B))
        pg.wait_for_timeout(1500)
        log("   C5 = %s | finCnNeedsBlueReload() = %s" % (pg.evaluate(CELL_JS, {"r": 4, "c": 2}), pg.evaluate(NEED)))

    log("")
    log("点「保存」…")
    pg.click('#fin_workspace button[onclick="fin_autoSave()"]')
    pg.wait_for_timeout(7000)
    log("   保存后 C5 = %s (期望 #0000FF)" % pg.evaluate(CELL_JS, {"r": 4, "c": 2}))
    log("   finCnNeedsBlueReload() = %s (期望 False)" % pg.evaluate(NEED))
    d = pg.evaluate("""() => { try { return { st: fin_statusKey, lbl: (document.getElementById('fin_status')||{}).textContent }; } catch(e){ return 'ERR'; } }""")
    log("   状态栏 = %s" % d)
    log("")
    log("页面报错 = %s" % errors[:6])
    b.close()

shutil.rmtree(TMP, ignore_errors=True)
log("临时目录已清理")
print("\n".join(LOG))
