# -*- coding: utf-8 -*-
"""验证 FIN-COLWIDTH-20261014：0 宽容器下的告警被静音；可见时编辑功能不受影响。"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_verify_colwarn_fix_out.txt")
L = []


def log(s):
    L.append(str(s))
    io.open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(s)


log("start")

from playwright.sync_api import sync_playwright  # noqa: E402

HOOK = """
() => {
  window.__cerr = []; window.__cinfo = [];
  var oe = console.error;
  console.error = function(){ try { window.__cerr.push(String(arguments[0]||'').slice(0,90)); } catch(e){} return oe.apply(console, arguments); };
  var oi = console.info;
  console.info = function(){ try { window.__cinfo.push(String(arguments[0]||'').slice(0,140)); } catch(e){} return oi.apply(console, arguments); };
}
"""

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True, args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 1500, "height": 900})
    pg.on("pageerror", lambda e: log("PAGEERROR " + str(e)[:200]))
    pg.goto("http://127.0.0.1:5050/lite", wait_until="domcontentloaded")
    pg.wait_for_timeout(1200)
    pg.fill("#loginUser", "tom")
    pg.fill("#loginPwd", "66668888")
    pg.click("#loginBtn")
    pg.wait_for_selector("#topbar:not(.hidden)", timeout=15000)
    pg.evaluate("() => { try { switchView('finance'); } catch(e){} }")
    pg.wait_for_timeout(12000)
    pg.evaluate(HOOK)

    log("helper=" + str(pg.evaluate("() => typeof window.fin_stopEditBeforeHide")))

    def drain(tag):
        r = pg.evaluate("() => { var a=window.__cerr||[], b=window.__cinfo||[]; window.__cerr=[]; window.__cinfo=[]; return {a:a,b:b}; }")
        hit = [x for x in r["a"] if "column width" in x]
        log("[%s] 可见告警 %d / 其它error %d / info %d %s" % (
            tag, len(hit), len(r["a"]), len(r["b"]),
            ("; ".join(x[:60] for x in r["b"] if "column width" in x))))
        return len(hit)

    def edit(col=4):
        pg.evaluate("(c) => { try { finUniverAPI.getActiveWorkbook().getActiveSheet().getRange(6, c).activate(); } catch(e){} }", col)
        pg.wait_for_timeout(250)
        pg.keyboard.press("F2")
        pg.wait_for_timeout(500)
        pg.keyboard.press("Escape")
        pg.wait_for_timeout(250)

    # 1) 先故意制造「容器 0 宽 + 编辑」→ 应被静音
    pg.evaluate("() => { var el = document.getElementById('univer_container'); if (el) el.style.display = 'none'; }")
    pg.wait_for_timeout(500)
    edit(0)
    drain("容器 display:none 时编辑（应被静音）")
    pg.evaluate("() => { var el = document.getElementById('univer_container'); if (el) el.style.display = ''; }")
    pg.wait_for_timeout(800)

    # 2) 可见时正常编辑 → 功能不受影响
    edit(4)
    drain("可见时正常编辑")

    # 3) 切到 merge 标签（工作区 hide）→ 再切回；确认无告警
    pg.evaluate("() => { try { fin_switchTab('merge'); } catch(e){} }")
    pg.wait_for_timeout(1200)
    drain("切到 merge 标签")
    pg.evaluate("() => { try { fin_switchTab('vn'); } catch(e){} }")
    pg.wait_for_timeout(2500)
    drain("切回 vn 标签")

    # 4) 切走模块再回来
    pg.evaluate("() => { try { switchView('dashboard'); } catch(e){} }")
    pg.wait_for_timeout(1500)
    drain("切到 dashboard")
    pg.evaluate("() => { try { switchView('finance'); } catch(e){} }")
    pg.wait_for_timeout(2500)
    drain("切回 finance")

    # 5) 统计栏仍在（没被新代码影响）
    st = pg.evaluate("() => { var el = document.getElementById('fin_statbar'); return el ? (el.textContent||'').slice(0,120) : 'MISSING'; }")
    log("统计栏: " + st)

    b.close()
log("done")
