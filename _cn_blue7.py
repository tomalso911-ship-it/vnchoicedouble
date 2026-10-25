# -*- coding: utf-8 -*-
"""更严谨地验证「新录入/粘贴进来的记录【立即】变蓝」+ 越南报表【完全不动】
（全部在临时目录，绝不触碰真实数据）：
   ① 粘贴式写入一个黑色格（非高亮行）→ 不保存/不刷新，看是否自动变蓝；
   ② 真·用户编辑路径（走 fin_scanEdits）→ 测「从写到蓝」的耗时；
   ③ CN 下人为造一个黑格 → finCnBluePass() 必须 > 0（证明确实在干活）；
      VN 下同样造黑格 → finCnBluePass() 必须 = 0，且 2.5s 后该格仍为黑（证明越南报表绝不被碰）。
"""
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
OUT = os.path.join(HERE, "_cn_blue7_out.txt")
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

TMP = tempfile.mkdtemp(prefix="cnblue7_")
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

WRITE_BLACK = """(p) => {
  try {
    var sid = fin_currentSnapshot().sheetOrder[0];
    finExecSilent('sheet.command.set-range-values', {
      unitId: fin_unitId(), subUnitId: sid,
      range: { startRow: p.r, startColumn: p.c, endRow: p.r, endColumn: p.c },
      value: [[{ v: p.v, s: { cl: { rgb: '#000000' } } }]]
    });
    return 'ok';
  } catch(e){ return 'ERR:' + e.message; }
}"""

HI_ROWS = """() => {
  try {
    var sid = fin_currentSnapshot().sheetOrder[0];
    var a = (finHiState && finHiState[sid]) || [];
    return a.map(function(h){ return h && h.row; });
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
    log("高亮行（0 基）= %s" % pg.evaluate(HI_ROWS))

    log("")
    log("① 粘贴黑色样式（非高亮行，行40=AO41）：")
    log("   写入 -> %s" % pg.evaluate(WRITE_BLACK, {"r": 40, "c": 2, "v": "PASTE-BLACK"}))
    t0 = time.time()
    pg.wait_for_timeout(120)
    log("   120ms 后  = %s  (应仍为 #000000)" % pg.evaluate(CELL, {"r": 40, "c": 2}))
    got = None
    for _ in range(40):                      # 最多再等 3s
        pg.wait_for_timeout(100)
        got = pg.evaluate(CELL, {"r": 40, "c": 2})
        if got and isinstance(got, dict) and str(got.get("cl") or "").upper().find("0000FF") >= 0:
            break
    log("   → 变蓝耗时 ≈ %.2fs，结果 = %s  (★期望 #0000FF，且全程未保存/未刷新)"
        % (time.time() - t0, got))

    log("")
    log("② 真·用户编辑路径耗时（写值后立刻模拟一次改动扫描 fin_scanEdits）：")
    pg.evaluate("() => { try { var sid = fin_currentSnapshot().sheetOrder[0];"
                " finExecSilent('sheet.command.set-range-values', { unitId: fin_unitId(), subUnitId: sid,"
                " range: { startRow: 41, startColumn: 0, endRow: 41, endColumn: 0 }, value: [[{ v: 777, s:{cl:{rgb:'#000000'}} }]] }); } catch(e){} }")
    pg.wait_for_timeout(60)
    t1 = time.time()
    pg.evaluate("() => { try { fin_scanEdits(); } catch(e){} }")
    got2 = None
    for _ in range(30):
        pg.wait_for_timeout(50)
        got2 = pg.evaluate(CELL, {"r": 41, "c": 0})
        if got2 and isinstance(got2, dict) and str(got2.get("cl") or "").upper().find("0000FF") >= 0:
            break
    log("   → 耗时 ≈ %.2fs，A42 = %s  (★期望 #0000FF)" % (time.time() - t1, got2))

    log("")
    log("③ 越南报表保护：")
    pg.evaluate(WRITE_BLACK, {"r": 45, "c": 2, "v": "CN-BLACK-MARK"})
    pg.wait_for_timeout(400)
    log("   CN 下先确认兜底逻辑确实在干活：finCnBluePass() = %s  (★期望 > 0)"
        % pg.evaluate("() => { try { return finCnBluePass(); } catch(e){ return 'ERR:' + e.message; } }"))
    v = pg.evaluate("""() => {
      try {
        fin_setKind('vn');
        var sid = fin_currentSnapshot().sheetOrder[0];
        finExecSilent('sheet.command.set-range-values', { unitId: fin_unitId(), subUnitId: sid,
          range: { startRow: 45, startColumn: 2, endRow: 45, endColumn: 2 },
          value: [[{ v: 'VN-BLACK-MARK', s: { cl: { rgb: '#000000' } } }]] });
        return finCnBluePass();
      } catch(e){ return 'ERR:' + e.message; }
    }""")
    log("   切到 vn 后 finCnBluePass() = %s  (★必须是 0 = 完全不动越南报表)" % v)
    pg.wait_for_timeout(2600)               # 等过两轮 2s 兜底轮询
    log("   2.6s（两轮兜底轮询）后该格 = %s  (★必须仍是 #000000，越南报表一个字都不许改)"
        % pg.evaluate(CELL, {"r": 45, "c": 2}))
    back = pg.evaluate("""() => { try { fin_setKind('cn');
        var sid = fin_currentSnapshot().sheetOrder[0];
        finExecSilent('sheet.command.set-range-values', { unitId: finUnitId(), subUnitId: sid,
          range: { startRow: 45, startColumn: 2, endRow: 45, endColumn: 2 },
          value: [[{ v: 'CN-AGAIN', s: { cl: { rgb: '#000000' } } }]] });
        return 1; } catch(e){ return 0; } }""")
    log("   切回 cn（%s）后 finCnBluePass() = %s  (★期望 > 0 = 逻辑恢复)"
        % (back, pg.evaluate("() => { try { return finCnBluePass(); } catch(e){ return 'ERR:' + e.message; } }")))

    log("")
    log("页面报错 = %s" % errors[:6])
    pg.screenshot(path=os.path.join(HERE, "_cn_blue7_after.png"))
    b.close()

shutil.rmtree(TMP, ignore_errors=True)
log("临时目录已清理")
print("\n".join(LOG))
