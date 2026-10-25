# -*- coding: utf-8 -*-
"""压力复现 2：查报表(筛选) / 复位 / 手动保存(含刷屏) / 录入 / 切语言 / 排序 / 静置，
并统计控制台里 '[hi] cmd'（命令流）等日志频次，看有没有命令风暴或堆栈溢出。
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
OUT = os.path.join(HERE, "_stress_cn3_out.txt")
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

TMP = tempfile.mkdtemp(prefix="stresscn3_")
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

saves = {"n": 0}
cnt = {}
errors = []


def on_console(m):
    t = m.text or ""
    key = "[hi] cmd" if "[hi] cmd" in t else ("[cn-blue]" if "[cn-blue]" in t else None)
    if key:
        cnt[key] = cnt.get(key, 0) + 1
    if m.type == "error":
        errors.append("console.error: " + t[:300])


def click_tab(pg, key):
    pg.evaluate("(k) => { var t = document.querySelector('#fin-tabs .fin-tab[data-key=\\'' + k + '\\']'); if (t) t.click(); }", key)
    for _ in range(60):
        pg.wait_for_timeout(400)
        if pg.evaluate("() => (typeof finReady !== 'undefined') && !!finReady"):
            break
    pg.wait_for_timeout(1200)


def type_cells(pg, n, prefix="T"):
    try:
        pg.click("#fin_workspace canvas", timeout=6000)
    except Exception as e:
        log("   点 canvas 失败（可能被弹窗挡住）：%s" % str(e)[:80])
        return
    pg.wait_for_timeout(400)
    for i in range(n):
        try:
            pg.keyboard.type("%s%d" % (prefix, i), delay=10)
            pg.keyboard.press("Enter")
        except Exception as e:
            log("   第 %d 格打字失败：%s" % (i, str(e)[:80]))
            break
        pg.wait_for_timeout(220)


with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True, args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 1500, "height": 950})
    pg.on("pageerror", lambda e: errors.append("pageerror: " + str(e)[:300]))
    pg.on("console", on_console)
    pg.on("request", lambda r: saves.__setitem__("n", saves["n"] + 1)
          if (r.method == "POST" and "/api/finance/" in r.url and r.url.endswith("/save")) else None)
    pg.goto(BASE, wait_until="domcontentloaded")
    pg.wait_for_timeout(1200)
    pg.fill("#loginUser", "tom")
    pg.fill("#loginPwd", "66668888")
    pg.click("#loginBtn")
    pg.wait_for_selector("#topbar:not(.hidden)", timeout=25000)
    pg.evaluate("() => { try { switchView('finance'); } catch(e){} }")
    pg.wait_for_timeout(800)
    click_tab(pg, "cn")
    saves["n"] = 0

    log("")
    log("① 先录入 6 格")
    type_cells(pg, 6, "A")
    pg.wait_for_timeout(2000)
    log("   报错=%d | [hi]cmd=%d | POST /save=%d" % (len(errors), cnt.get("[hi] cmd", 0), saves["n"]))

    log("② 查报表筛选 2026-04（fin_rptApplyFilter）")
    pg.evaluate("() => { try { fin_rptApplyFilter(2026, 4); } catch(e){ console.error('rpt filter: ' + e.message); } }")
    pg.wait_for_timeout(6000)
    log("   报错=%d %s" % (len(errors), errors[-2:] if errors else []))

    log("③ 复位（fin_reload）")
    pg.evaluate("() => { try { fin_reload(); } catch(e){ console.error('reload: ' + e.message); } }")
    pg.wait_for_timeout(6000)
    log("   报错=%d %s" % (len(errors), errors[-2:] if errors else []))

    log("④ 手动保存（fin_autoSave → 可能触发刷屏 fin_reload）")
    pg.evaluate("() => { try { fin_autoSave(); } catch(e){ console.error('save: ' + e.message); } }")
    pg.wait_for_timeout(9000)
    log("   报错=%d | POST /save=%d" % (len(errors), saves["n"]))

    log("⑤ 再录入 10 格 + 切语言两次")
    type_cells(pg, 10, "B")
    pg.wait_for_timeout(2000)
    for lg in ("zh", "vi"):
        pg.evaluate("(l) => { try { setLangDebug(l); } catch(e){} }", lg)
        pg.wait_for_timeout(3000)
    log("   报错=%d %s" % (len(errors), errors[-2:] if errors else []))

    log("⑥ 静置 20s（等所有定时器/翻译/保存落地）")
    pg.wait_for_timeout(20000)
    log("   报错=%d | [hi]cmd=%d | POST /save=%d" % (len(errors), cnt.get("[hi] cmd", 0), saves["n"]))

    log("")
    log("★报错去重：")
    seen = []
    for e in errors:
        if e[:120] not in seen:
            seen.append(e[:120])
    for k in seen[:10]:
        log("   - %s" % k)
    if not seen:
        log("   （无）")

    pg.screenshot(path=os.path.join(HERE, "_stress_cn3_after.png"))
    b.close()

shutil.rmtree(TMP, ignore_errors=True)
log("临时目录已清理")
print("\n".join(LOG))
