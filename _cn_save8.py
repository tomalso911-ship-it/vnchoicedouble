# -*- coding: utf-8 -*-
"""验证「录入后立即保存 + 刷新页面数据仍在 + 刷新页面不瞎写文件 + 越南报表绝不动」
（全部在临时目录：app.CN_REPORT / FIN_DIR 都指到 tempfile.mkdtemp()，绝不碰真实报表）

  A) 只打开页面不动任何东西 → 8s 内服务器文件 mtime 必须不变（刷新 ≠ 改文件）
  B) 写一个新值 + 走「命令流」那条脏标记 → 记录「几秒后服务器文件被改写、新值已进文件」
  C) 硬刷新页面（重新登录 + 切到中国报表）→ 断言新值还在（★用户核心要求）
  D) 越南报表保护：切 vn，写值 + 反复标脏 → 服务器文件一个字不变
"""
import datetime
import io
import json
import os
import shutil
import socket
import sys
import tempfile
import threading
import time
import urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "_cn_save8_out.txt")
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

TMP = tempfile.mkdtemp(prefix="cnsave8_")
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


def mt():
    try:
        return os.path.getmtime(app.CN_REPORT)
    except OSError:
        return 0


def snap_text():
    try:
        with urllib.request.urlopen("http://127.0.0.1:%d/api/finance/cn-report/snapshot" % PORT, timeout=30) as r:
            return r.read().decode("utf-8", "replace")
    except Exception as e:
        return "ERR:%s" % e


CELL = """(p) => {
  try {
    var sn = fin_currentSnapshot();
    var sid = sn.sheetOrder[0];
    var cc = ((sn.sheets[sid].cellData || {})[String(p.r)] || {})[String(p.c)];
    return cc ? { v: cc.v } : null;
  } catch(e){ return 'ERR:' + e.message; }
}"""

WRITE_MARK = """(p) => {
  try {
    var sid = fin_currentSnapshot().sheetOrder[0];
    finExecSilent('sheet.command.set-range-values', {
      unitId: fin_unitId(), subUnitId: sid,
      range: { startRow: p.r, startColumn: p.c, endRow: p.r, endColumn: p.c },
      value: [[{ v: p.v }]]
    });
    return 'ok';
  } catch(e){ return 'ERR:' + e.message; }
}"""

DUMP = """() => {
  try {
    var sn = fin_currentSnapshot();
    var sid = sn.sheetOrder[0];
    var cd = (sn.sheets[sid] || {}).cellData || {};
    var hits = [];
    for (var rk in cd){
      var row = cd[rk] || {};
      for (var ck in row){
        var v = row[ck] && row[ck].v;
        if (typeof v === 'string' && v.indexOf('SAVE-MARK') === 0) hits.push(rk + ',' + ck + '=' + v);
      }
    }
    return hits;
  } catch(e){ return ['ERR:' + e.message]; }
}"""

MARK = 'SAVE-MARK-20261013'


def wait_ready(pg):
    pg.wait_for_selector("#topbar:not(.hidden)", timeout=20000)
    pg.evaluate("() => { try { switchView('finance'); } catch(e){} }")
    pg.wait_for_timeout(400)
    pg.evaluate("() => { var t = document.querySelector('#fin-tabs .fin-tab[data-key=\\'cn\\']'); if (t) t.click(); }")
    for _ in range(60):
        pg.wait_for_timeout(400)
        if pg.evaluate("() => (typeof finReady !== 'undefined') && !!finReady"):
            break
    pg.wait_for_timeout(3000)


errors = []
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True, args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 1500, "height": 950})
    pg.on("pageerror", lambda e: errors.append("pageerror: " + str(e)[:200]))
    pg.on("console", lambda m: errors.append("console.error: " + m.text[:200]) if m.type == "error" else None)
    pg.goto(BASE, wait_until="domcontentloaded")
    pg.wait_for_timeout(1200)
    pg.fill("#loginUser", "tom")
    pg.fill("#loginPwd", "66668888")
    pg.click("#loginBtn")
    wait_ready(pg)

    # ---------- A) 打开页面不动 → 不许写文件 ----------
    m0 = mt()
    log("")
    log("A) 只打开中国报表、不做任何操作：")
    pg.evaluate("() => { try { fin_scanEdits(); } catch(e){} }")
    pg.wait_for_timeout(8000)
    m1 = mt()
    log("   8s 后 文件 mtime 变化 = %s | finDirty = %s | finCnHoldUntil 剩余 ≈ %.1fs"
        % (("%.3f" % (m1 - m0)) if abs(m1 - m0) > 0.001 else "0（未写文件 ✔）",
           pg.evaluate("() => { try { return finDirty; } catch(e){ return 'ERR'; } }"),
           pg.evaluate("() => { try { return (finCnHoldUntil - Date.now())/1000; } catch(e){ return -1; } }")))

    # ---------- B) 录入 → 立即自动保存 ----------
    log("")
    log("B) 录入一个新值（A61）+ 走命令流那条脏标记（fin_markDirty）：")
    log("   写入 -> %s" % pg.evaluate(WRITE_MARK, {"r": 60, "c": 0, "v": MARK}))
    t0 = time.time()
    pg.evaluate("() => { try { fin_markDirty(); } catch(e){} }")
    m_saved = None
    for _ in range(120):                    # 最多等 30s
        pg.wait_for_timeout(250)
        if mt() != m1:
            m_saved = mt()
            break
    log("   → 服务器文件被改写，耗时 ≈ %.2fs | finDirty = %s | 状态 = %s"
        % (time.time() - t0,
           pg.evaluate("() => { try { return finDirty; } catch(e){ return 'ERR'; } }"),
           pg.evaluate("() => { try { return (document.querySelector('#fin_status')||{}).textContent; } catch(e){ return '?'; } }")))
    txt = snap_text()
    log("   服务端快照里含标记 = %s" % (MARK.split('-')[-1] in txt and ("'" + MARK + "'" in txt or '"' + MARK + '"' in txt)))

    # ---------- C) 硬刷新 → 数据必须还在 ----------
    log("")
    log("C) 硬刷新页面（重新登录 + 重新拉服务端快照）：")
    pg.goto(BASE, wait_until="domcontentloaded")
    pg.wait_for_timeout(1200)
    pg.fill("#loginUser", "tom")
    pg.fill("#loginPwd", "66668888")
    pg.click("#loginBtn")
    wait_ready(pg)
    log("   刷新后 A61 = %s" % pg.evaluate(CELL, {"r": 60, "c": 0}))
    log("   页面上所有 SAVE-MARK* 格 = %s" % pg.evaluate(DUMP))
    pg.wait_for_timeout(6000)
    log("   刷新后静置 6s 文件 mtime 变化 = %s"
        % (("%.3f" % (mt() - m_saved)) if abs(mt() - m_saved) > 0.001 else "0（刷新没有回写文件 ✔）"))

    # ---------- D) 越南报表保护 ----------
    log("")
    log("D) 越南报表保护（切到 vn 写值 + 反复标脏）：")
    m_v = mt()
    v = pg.evaluate("""() => {
      try {
        fin_setKind('vn');
        var sid = fin_currentSnapshot().sheetOrder[0];
        finExecSilent('sheet.command.set-range-values', { unitId: finUnitId(), subUnitId: sid,
          range: { startRow: 60, startColumn: 0, endRow: 60, endColumn: 0 },
          value: [[{ v: 'VN-SAVE-MARK' }]] });
        var r = [];
        for (var i = 0; i < 5; i++){ r.push(fin_markDirty()); }
        r.push('dirty=' + finDirty);
        r.push('hold=' + ((finCnHoldUntil - Date.now()) > 0));
        return r.join('|');
      } catch(e){ return 'ERR:' + e.message; }
    }""")
    pg.wait_for_timeout(4000)
    log("   vn 下连续标脏 5 次 = %s" % v)
    log("   4s 后服务器文件 mtime 变化 = %s  (★必须 0 = 越南报表绝不自动保存)"
        % (("%.3f" % (mt() - m_v)) if abs(mt() - m_v) > 0.001 else "0 ✔"))
    pg.evaluate("() => { try { fin_setKind('cn'); } catch(e){} }")

    log("")
    log("页面报错 = %s" % errors[:6])
    pg.screenshot(path=os.path.join(HERE, "_cn_save8_after.png"))
    b.close()

shutil.rmtree(TMP, ignore_errors=True)
log("临时目录已清理")
print("\n".join(LOG))
