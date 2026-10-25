# -*- coding: utf-8 -*-
"""复现：看板（#fin_dk_merge / #fin_dk_vn）在「切换语言」后文字没有跟着切换。
   步骤：登录 → 财务页 → 点「合并报表看板」→ 记录文字 → 点 EN → 再记录 → 手动调 fin_renderDashCur 看是否恢复。"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_verify_dash_lang_out.txt")
L = []


def log(s):
    L.append(str(s))
    io.open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(s)


from playwright.sync_api import sync_playwright  # noqa: E402

ERRS, PAGES = [], []

PROBE = r"""() => {
  var out = {};
  out.curLang = window.CUR_LANG;
  out.winLang = window.__lang;
  out.activeTab = (typeof FIN_ACTIVE_TAB !== 'undefined') ? FIN_ACTIVE_TAB : null;
  out.hasRenderCur = (typeof fin_renderDashCur === 'function');
  out.fired = window.__dkFired || 0;
  out.hasData = (typeof FIN_DK_DATA !== 'undefined') ? Object.keys(FIN_DK_DATA) : null;
  var b = document.getElementById('fin_dk_merge');
  out.txt = b ? (b.innerText || '').replace(/\s+/g, ' ').trim().slice(0, 150) : null;
  out.unitEN = (function(){ try { return (I18N['en']||{}).fin_dk_unit; } catch(e){ return 'ERR'; } })();
  out.tUnit = (function(){ try { return T().fin_dk_unit; } catch(e){ return 'ERR:'+e; } })();
  out.tBnk = (function(){ try { return T().fin_dk_kpi_open; } catch(e){ return 'ERR'; } })();
  return out;
}"""


def show(tag, pg):
    info = pg.evaluate(PROBE)
    log("── %s" % tag)
    for k in ("curLang", "winLang", "activeTab", "fired", "hasRenderCur", "hasData",
              "tUnit", "tBnk", "unitEN"):
        log("   %-14s = %s" % (k, info.get(k)))
    log("   txt            = %s" % info.get("txt"))
    return info


with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True, args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 1500, "height": 900})
    pg.on("console", lambda m: ERRS.append(m.text[:160]) if m.type == "error" else None)
    pg.on("pageerror", lambda e: PAGES.append(str(e)[:160]))

    pg.goto("http://127.0.0.1:5050/lite", wait_until="domcontentloaded")
    pg.wait_for_timeout(1200)
    pg.fill("#loginUser", "tom")
    pg.fill("#loginPwd", "66668888")
    pg.click("#loginBtn")
    pg.wait_for_selector("#topbar:not(.hidden)", timeout=25000)

    # 统计 app:langchange 到底触发了几次（独立于业务监听器）
    pg.evaluate("() => { window.__dkFired = 0;"
                "  window.addEventListener('app:langchange', function(){ window.__dkFired = (window.__dkFired||0)+1; }); }")

    pg.evaluate("() => { try { switchView('finance'); } catch(e){} }")
    pg.wait_for_timeout(4000)
    pg.evaluate("() => { try { fin_switchTab('dashm'); } catch(e){} }")
    pg.wait_for_timeout(8000)
    A = show("A 看板已渲染（当前中文）", pg)

    pg.evaluate("() => { try { setLangDebug('en'); } catch(e){ window.__setLangErr = String(e); } }")
    pg.wait_for_timeout(1500)
    B = show("B 切成 EN 之后", pg)
    log("   setLangErr = %s" % pg.evaluate("() => window.__setLangErr || null"))

    pg.evaluate("() => { try { fin_renderDashCur(); } catch(e){ window.__renderErr = String(e); } }")
    pg.wait_for_timeout(1200)
    C = show("C 手动调 fin_renderDashCur() 之后", pg)
    log("   renderErr = %s" % pg.evaluate("() => window.__renderErr || null"))

    log("")
    log("=== 判定 ===")
    log("  B.fired 增加了吗        : %s -> %s" % (A["fired"], B["fired"]))
    log("  A 文本 == B 文本        : %s" % (A["txt"] == B["txt"]))
    log("  B 文本 == C 文本        : %s" % (B["txt"] == C["txt"]))
    log("  B.tUnit (T() 值)        : %s   (en 应为 bn)" % B["tUnit"])
    log("")
    log("console error 合计 = %d" % len(ERRS))
    for x in ERRS[:8]:
        log("   ERR " + x)
    log("pageerror = %s" % PAGES[:4])
    b.close()
log("done")
