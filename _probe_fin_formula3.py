# -*- coding: utf-8 -*-
"""验证 FIN-FORMULA-STACK-20261013（v3，安全 + 分步落盘）：
  ① 财务页加载无报错；等 6s（等第一个 unit 建好、DI 实例化完）再探。
  ② 探针 1：safeFlag / protoFlag / guardFlag（实例级） / 同步回放计数 A/B。
  ③ 探针 2（单独一步，万一卡住也不丢 ② 的结论）：
       svc.calculateStarted$.next(true) —— 打补丁前这一步会无限重入卡死页面，打上后必须秒回。
  ④ fin_reload() 冒烟后仍无报错。"""
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
OUT = os.path.join(HERE, "_probe_fin_formula3_out.txt")
LOG = []


def log(s):
    LOG.append("[%s] %s" % (datetime.datetime.now().strftime("%H:%M:%S"), s))
    io.open(OUT, "w", encoding="utf-8").write("\n".join(LOG) + "\n")
    print(LOG[-1])


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

TMP = tempfile.mkdtemp(prefix="probefx3_")
app.FIN_DIR = TMP
app.CN_REPORT = os.path.join(TMP, "cn_report.xlsx")
app.CN_SNAP_KEY = os.path.join(TMP, "cn_report.snapshot.key")
app.CN_SNAP_PREFIX = "cn_report.snapshot."
app.CN_TITLES_PATH = os.path.join(TMP, "fin_sheet_titles_cn.json")
app._cn_seed_if_missing()

PORT = 5168
BASE = "http://127.0.0.1:%d/lite" % PORT
if not port_open(PORT):
    threading.Thread(target=lambda: app.app.run(host="127.0.0.1", port=PORT, debug=False,
                                               use_reloader=False, threaded=True),
                     daemon=True).start()
    for _ in range(60):
        if port_open(PORT):
            break
        time.sleep(0.3)

GET_SVC = r"""
async () => {
  const m = await import('https://esm.sh/@univerjs/sheets-formula@0.5.5/es2022/sheets-formula.mjs');
  const rx = await import('https://esm.sh/rxjs@>=7.0.0?target=es2022');
  window.__P = { rx: rx, m: m };
  let svc = null, getErr = null;
  try { svc = window.finUniver.__getInjector().get(m.RegisterOtherFormulaService); }
  catch (e) { getErr = String(e).slice(0, 110); }
  return { getErr: getErr, safeFlag: !!window.__FIN_FORMULA_SAFE,
           protoFlag: !!(m.RegisterOtherFormulaService.prototype.__finFormulaSafe),
           svcOk: !!svc };
}
"""

STEP1 = r"""
() => {
  const rx = window.__P.rx, m = window.__P.m;
  const svc = window.finUniver.__getInjector().get(m.RegisterOtherFormulaService);
  const started = svc.calculateStarted$;
  const countReplay = (obs) => { let hits = 0; const s = obs.subscribe(function(){ hits++; }); try { s.unsubscribe(); } catch(e){} return hits; };
  const rawBS = new rx.BehaviorSubject(true);
  return {
    guardFlag: !!started.__finEdge,
    value: started.getValue(),
    rawHits: countReplay(rawBS.pipe(rx.filter(v => v))),      // 原样：订阅即回放 → 1
    guardHits: countReplay(started.pipe(rx.filter(v => v))),  // 打过补丁 → 0
    srcObs: (svc._formulaChangeWithRange$.observers || []).length,
    csObsClosed: (started.observers || []).map(function(o){ return o.closed; }).slice(0, 5)
  };
}
"""

STEP2 = r"""
() => {
  const m = window.__P.m;
  const svc = window.finUniver.__getInjector().get(m.RegisterOtherFormulaService);
  const t0 = performance.now();
  let err = null;
  try { svc.calculateStarted$.next(true); } catch (e) { err = String(e).slice(0, 80); }
  return { ms: Math.round(performance.now() - t0), err: err, value: svc.calculateStarted$.getValue() };
}
"""

errs = []
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True, args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 1500, "height": 950})
    pg.on("pageerror", lambda e: errs.append("pageerror: " + str(e)[:200]))
    pg.on("console", lambda m: errs.append("console.error: " + m.text[:200]) if m.type == "error" else None)
    pg.goto(BASE, wait_until="domcontentloaded")
    pg.wait_for_timeout(1200)
    pg.fill("#loginUser", "tom")
    pg.fill("#loginPwd", "66668888")
    pg.click("#loginBtn")
    pg.wait_for_selector("#topbar:not(.hidden)", timeout=25000)
    pg.evaluate("() => { try { switchView('finance'); } catch(e){} }")
    for _ in range(60):
        pg.wait_for_timeout(500)
        if pg.evaluate("() => (typeof finReady !== 'undefined') && !!finReady"):
            break
    pg.wait_for_timeout(6000)
    log("① 加载期报错 = %s" % errs[:4])

    log("② 取服务 = %s" % pg.evaluate(GET_SVC))
    r1 = pg.evaluate(STEP1)
    log("③ 回放 A/B = %s" % r1)
    pg.wait_for_timeout(800)
    log("③ 之后报错 = %s" % errs[:4])

    r2 = pg.evaluate(STEP2)
    log("④ next(true) 计时 = %s" % r2)
    pg.wait_for_timeout(800)
    log("④ 之后报错 = %s" % errs[:4])

    pg.evaluate("() => { try { fin_reload(); } catch(e){} }")
    pg.wait_for_timeout(6000)
    st = pg.evaluate("() => { var e=document.getElementById('fin_status'); return e ? e.textContent.trim() : null; }")
    log("⑤ 重载后状态栏 = %s 报错 = %s" % (st, errs[:4]))
    b.close()

shutil.rmtree(TMP, ignore_errors=True)
log("临时目录已清理")
