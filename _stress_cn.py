# -*- coding: utf-8 -*-
"""压力复现：在中国报表里「真·键盘录入 + 切语言 + 切标签 + 切币种 + 排序 + 查报表」，
捕捉 pageerror / console.error（重点：RangeError: Maximum call stack size exceeded）。
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
OUT = os.path.join(HERE, "_stress_cn_out.txt")
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

TMP = tempfile.mkdtemp(prefix="stresscn_")
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


def on_req(r):
    try:
        if r.method == "POST" and "/api/finance/" in r.url and r.url.endswith("/save"):
            saves["n"] += 1
    except Exception:
        pass


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
    pg.on("pageerror", lambda e: errors.append("pageerror: " + str(e)[:300]))
    pg.on("console", lambda m: errors.append("console.error: " + m.text[:300]) if m.type == "error" else None)
    pg.on("request", on_req)
    pg.goto(BASE, wait_until="domcontentloaded")
    pg.wait_for_timeout(1200)
    pg.fill("#loginUser", "tom")
    pg.fill("#loginPwd", "66668888")
    pg.click("#loginBtn")
    pg.wait_for_selector("#topbar:not(.hidden)", timeout=25000)
    pg.evaluate("() => { try { switchView('finance'); } catch(e){} }")
    pg.wait_for_timeout(800)

    log("")
    log("① 切到中国报表")
    click_tab(pg, "cn")
    saves["n"] = 0

    log("② 真·键盘录入 12 格（点格 + 打字 + 回车）")
    try:
        pg.click("#fin_workspace canvas", timeout=8000)
    except Exception as e:
        log("   点 canvas 失败：%s" % e)
    pg.wait_for_timeout(500)
    for i in range(12):
        try:
            pg.keyboard.type("STRESS-%d" % i, delay=12)
            pg.keyboard.press("Enter")
        except Exception as e:
            log("   第 %d 格打字失败：%s" % (i, e))
            break
        pg.wait_for_timeout(260)
    pg.wait_for_timeout(2500)
    log("   打字期间/之后 POST /save 次数 = %d" % saves["n"])
    log("   报错累计 = %d %s" % (len(errors), errors[:3]))

    log("③ 切语言 vi → zh → en → vi")
    for lg in ("zh", "en", "vi"):
        pg.evaluate("(l) => { try { setLangDebug(l); } catch(e){} }", lg)
        pg.wait_for_timeout(2500)
        log("   切到 %s 后 报错累计 = %d %s" % (lg, len(errors), errors[-2:] if errors else []))

    log("④ 切到越南报表再切回中国报表")
    click_tab(pg, "vn")
    pg.wait_for_timeout(1500)
    click_tab(pg, "cn")
    log("   报错累计 = %d %s" % (len(errors), errors[-2:] if errors else []))

    log("⑤ 币种下拉切 USD → RMB → VND")
    for cur in ("USD", "RMB", "VND"):
        pg.select_option("#fin_currency", cur)
        pg.wait_for_timeout(2500)
        log("   切到 %s 后 报错累计 = %d %s" % (cur, len(errors), errors[-2:] if errors else []))

    log("⑥ 排序 / 复位 / 再录入 3 格")
    pg.evaluate("() => { try { fin_sortByColumn(1); } catch(e){} }")
    pg.wait_for_timeout(2500)
    pg.evaluate("() => { try { fin_sortByColumn(-1); } catch(e){} }")
    pg.wait_for_timeout(2500)
    pg.evaluate("() => { try { fin_sortReset(); } catch(e){} }")
    pg.wait_for_timeout(4000)
    try:
        pg.click("#fin_workspace canvas", timeout=8000)
        pg.wait_for_timeout(400)
        for i in range(3):
            pg.keyboard.type("AFTER-%d" % i, delay=12)
            pg.keyboard.press("Enter")
            pg.wait_for_timeout(300)
    except Exception as e:
        log("   再录入失败：%s" % e)
    pg.wait_for_timeout(3000)
    log("   全程 POST /save 次数 = %d" % saves["n"])
    log("   报错累计 = %d" % len(errors))

    log("")
    log("★全部报错去重：")
    seen = []
    for e in errors:
        k = e[:120]
        if k not in seen:
            seen.append(k)
    for k in seen[:10]:
        log("   - %s" % k)

    pg.screenshot(path=os.path.join(HERE, "_stress_cn_after.png"))
    b.close()

shutil.rmtree(TMP, ignore_errors=True)
log("临时目录已清理")
print("\n".join(LOG))
