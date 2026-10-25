# -*- coding: utf-8 -*-
"""验证「新录入/粘贴进来的记录【立即】变蓝」（全在临时目录，不碰真实数据）：
   ① 页面里写一个黑色样式格（模拟粘贴带进来的黑字）→ 不做任何操作，看是否在 2s 内自动变蓝；
   ② 往空行里真实敲一个值 → 看是否立刻就是蓝字；
   ③ 把报表种类切到 vn → 确认 finCnBluePass() 直接返回 0（越南报表绝不被碰）。"""
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
OUT = os.path.join(HERE, "_cn_blue6_out.txt")
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

TMP = tempfile.mkdtemp(prefix="cnblue6_")
app.FIN_DIR = TMP
app.CN_REPORT = os.path.join(TMP, "cn_report.xlsx")
app.CN_SNAP_KEY = os.path.join(TMP, "cn_report.snapshot.key")
app.CN_SNAP_PREFIX = "cn_report.snapshot."
app.CN_TITLES_PATH = os.path.join(TMP, "fin_sheet_titles_cn.json")
log("临时报表目录 = %s" % TMP)
app._cn_seed_if_missing()

PORT = 5162
BASE = "http://127.0.0.1:%d/lite" % PORT
if not port_open(PORT):
    threading.Thread(target=lambda: app.app.run(host="127.0.0.1", port=PORT, debug=False,
                                               use_reloader=False, threaded=True),
                     daemon=True).start()
    for _ in range(60):
        if port_open(PORT):
            break
        time.sleep(0.3)

CELL = """(p) => {
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

PASTE_BLACK = """() => {
  try {
    var sid = fin_currentSnapshot().sheetOrder[0];
    finExecSilent('sheet.command.set-range-values', {
      unitId: fin_unitId(), subUnitId: sid,
      range: { startRow: 6, startColumn: 2, endRow: 6, endColumn: 2 },
      value: [[{ v: 'PASTE-BLACK', s: { cl: { rgb: '#000000' } } }]]
    });
    return 'ok';
  } catch(e){ return 'ERR:' + e.message; }
}"""

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
    log("① 模拟粘贴黑色样式到 C7（不保存、不刷新）：")
    log("   写入 -> %s" % pg.evaluate(PASTE_BLACK))
    pg.wait_for_timeout(120)
    log("   120ms 后  C7 = %s  (此时应还是黑的)" % pg.evaluate(CELL, {"r": 6, "c": 2}))
    pg.wait_for_timeout(1500)
    log("   1.6s  后  C7 = %s  (★应自动变蓝 #0000FF)" % pg.evaluate(CELL, {"r": 6, "c": 2}))

    log("")
    log("② 往空数据行真实敲入一个新值（A9 / E9）：")
    pg.evaluate("""() => { var sid = fin_currentSnapshot().sheetOrder[0];
      finExecSilent('sheet.command.set-range-values', { unitId: fin_unitId(), subUnitId: sid,
        range: { startRow: 8, startColumn: 0, endRow: 8, endColumn: 0 }, value: [[{ v: 46000 }]] });
      finExecSilent('sheet.command.set-range-values', { unitId: fin_unitId(), subUnitId: sid,
        range: { startRow: 8, startColumn: 4, endRow: 8, endColumn: 4 }, value: [[{ v: 1234567 }]] });
    }""")
    pg.wait_for_timeout(1200)
    log("   A9 = %s | E9 = %s" % (pg.evaluate(CELL, {"r": 8, "c": 0}), pg.evaluate(CELL, {"r": 8, "c": 4})))

    log("")
    log("③ 越南报表保护检查：")
    log("   CN 下 finCnBluePass() = %s" % pg.evaluate("() => { try { return finCnBluePass(); } catch(e){ return 'ERR:' + e.message; } }"))
    v = pg.evaluate("""() => {
      try { fin_setKind('vn'); var r = finCnBluePass(); fin_setKind('cn'); return r; }
      catch(e){ return 'ERR:' + e.message; }
    }""")
    log("   切到 vn 时 finCnBluePass() = %s  (★必须是 0 = 完全不动越南报表)" % v)
    log("   回到 cn 后 finCnBluePass() = %s" % pg.evaluate("() => { try { return finCnBluePass(); } catch(e){ return 'ERR:' + e.message; } }"))

    log("")
    log("页面报错 = %s" % errors[:6])
    pg.screenshot(path=os.path.join(HERE, "_cn_blue6_after.png"))
    b.close()

shutil.rmtree(TMP, ignore_errors=True)
log("临时目录已清理")
print("\n".join(LOG))
