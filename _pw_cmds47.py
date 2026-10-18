# -*- coding: utf-8 -*-
"""探针 47：抓真实命令 id（对齐 / 字号 / 边框 / 加粗 / 小数位），用于扩展撤销白名单。

只点安全按钮（不改行列结构、不合并），避免动到真实报表。
"""
import json
import sys
import traceback

from playwright.sync_api import sync_playwright

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

URL = "http://127.0.0.1:5050/lite?v=cmds47"
R, C = 6, 6
TARGETS = ["bold", "vertical-center", "left-justifying", "add-digits", "reduce-digits", "all-border"]


def say(*a, **kw):
    print(*a, flush=True)


def main():
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True, args=["--no-sandbox"])
        pg = b.new_context(viewport={"width": 1600, "height": 950}).new_page()
        pg.set_default_timeout(25000)
        pg.goto(URL, wait_until="domcontentloaded", timeout=60000)
        pg.wait_for_timeout(800)
        if pg.evaluate("() => { var e=document.getElementById('loginPage'); return e && !e.classList.contains('hidden'); }"):
            pg.fill("#loginUser", "tom")
            pg.fill("#loginPwd", "66668888")
            pg.click("#loginBtn")
        pg.wait_for_selector("#topbar:not(.hidden)", timeout=30000)
        pg.evaluate("() => switchView('finance')")
        pg.wait_for_function("() => !!(window.finReady && document.querySelector('#univer_container canvas'))", timeout=60000)
        pg.wait_for_timeout(4000)

        pg.evaluate("""() => {
          window.__cmdLog = [];
          var cs = window.__finCmdSvc;
          if (cs && cs.onCommandExecuted){
            cs.onCommandExecuted(function(cmd){
              try {
                window.__cmdLog.push({ id: cmd.id, keys: Object.keys(cmd.params || {}),
                                       p: JSON.stringify(cmd.params || {}).slice(0, 320) });
              } catch(e){}
            });
          }
        }""")

        for kw in TARGETS:
            pg.evaluate("""(arg) => {
              window.finUniverAPI.getActiveWorkbook().getActiveSheet().getRange(arg.r, arg.c).activate();
              var c = document.querySelector('#univer_container canvas');
              if (c) { c.setAttribute('tabindex','0'); c.focus(); }
              window.__cmdLog = [];
            }""", {"r": R, "c": C})
            pg.wait_for_timeout(600)
            el = pg.evaluate("""(kw) => {
              var best = null;
              document.querySelectorAll('#univer_container svg').forEach(function(sv){
                var cls = sv.getAttribute('class') || '';
                if (cls.indexOf(kw) < 0) return;
                var host = sv.closest('button') || sv.parentElement;
                var r = host.getBoundingClientRect();
                if (r.width < 2) return;
                if (!best) best = { x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2) };
              });
              return best;
            }""", kw)
            if not el:
                say("[%s] 找不到按钮" % kw, flush=True)
                continue
            pg.mouse.click(el["x"], el["y"])
            pg.wait_for_timeout(1400)
            log = pg.evaluate("() => window.__cmdLog")
            say("=== [%s] ===" % kw, flush=True)
            for it in log:
                say("   id: %-52s keys=%s" % (it["id"], ",".join(it["keys"])), flush=True)
                say("      %s" % it["p"], flush=True)

        b.close()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.exit(2)
