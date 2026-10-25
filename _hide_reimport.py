# -*- coding: utf-8 -*-
"""验收「中国报表隐藏『重导』按钮 / 越南报表保留『重导』按钮 + 保存按钮状态正确」。
只在临时目录跑，不碰真实报表。"""
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
OUT = os.path.join(HERE, "_hide_reimport_out.txt")
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

TMP = tempfile.mkdtemp(prefix="hidereim_")
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

PROBE = """() => {
  try {
    var re = document.getElementById('fin_reimport_btn');
    var sv = document.querySelector('#fin_workspace button[onclick="fin_autoSave()"]');
    var vnTab = document.querySelector('#fin-tabs .fin-tab[data-key=\\'vn\\']');
    var cnTab = document.querySelector('#fin-tabs .fin-tab[data-key=\\'cn\\']');
    return {
      kind: FIN_KIND,
      reimport_display: re ? (getComputedStyle(re).display) : 'MISSING',
      reimport_visible: !!(re && re.offsetParent !== null),
      save_disabled: sv ? !!sv.disabled : 'MISSING',
      vnTab: !!vnTab, cnTab: !!cnTab
    };
  } catch(e){ return 'ERR:' + e.message; }
}"""


def click_tab(pg, key):
    pg.evaluate("(k) => { var t = document.querySelector('#fin-tabs .fin-tab[data-key=\\'' + k + '\\']'); if (t) t.click(); }", key)
    for _ in range(60):
        pg.wait_for_timeout(400)
        if pg.evaluate("() => (typeof finReady !== 'undefined') && !!finReady"):
            break
    pg.wait_for_timeout(1200)


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
    pg.wait_for_selector("#topbar:not(.hidden)", timeout=25000)
    pg.evaluate("() => { try { switchView('finance'); } catch(e){} }")
    pg.wait_for_timeout(600)

    log("")
    log("① 越南报表（默认标签）：")
    log("   %s   ← 重导必须可见、保存按钮在只读下禁用" % pg.evaluate(PROBE))

    log("")
    log("② 切到中国报表：")
    click_tab(pg, "cn")
    log("   %s   ← 重导必须 display=none" % pg.evaluate(PROBE))

    log("")
    log("③ 切回越南报表：")
    click_tab(pg, "vn")
    log("   %s   ← 重导必须恢复可见" % pg.evaluate(PROBE))

    log("")
    log("④ 再切到中国报表（验证来回切也稳定）：")
    click_tab(pg, "cn")
    log("   %s" % pg.evaluate(PROBE))

    log("")
    log("页面报错 = %s" % errors[:8])
    pg.screenshot(path=os.path.join(HERE, "_hide_reimport_cn.png"))
    b.close()

shutil.rmtree(TMP, ignore_errors=True)
log("临时目录已清理")
print("\n".join(LOG))
