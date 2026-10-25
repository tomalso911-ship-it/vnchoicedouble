# -*- coding: utf-8 -*-
"""精简版：只问三个决定性问题
   Q1 window.finPresets 到底有没有？IUndoRedoService token 拿得到吗？（决定 undo-clean 是否还活着）
   Q2 内部写入是否进了撤销栈？
   Q3 编辑后撤销，值回不回退？
"""
import json
import sys
from playwright.sync_api import sync_playwright

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

URL = "http://127.0.0.1:5050/lite?v=undodiag2"
logs = []


def P(*a):
    print(*a, flush=True)


with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True, args=["--no-sandbox"])
    try:
        pg = b.new_context(viewport={"width": 1400, "height": 900}).new_page()
        pg.set_default_timeout(25000)
        pg.on("console", lambda m: logs.append("[%s] %s" % (m.type, m.text[:200])))
        pg.on("pageerror", lambda e: logs.append("[pageerror] %s" % str(e)[:200]))
        pg.goto(URL, wait_until="domcontentloaded", timeout=45000)
        pg.wait_for_timeout(700)
        if pg.evaluate("() => { var e=document.getElementById('loginPage'); return e && !e.classList.contains('hidden'); }"):
            pg.fill("#loginUser", "tom")
            pg.fill("#loginPwd", "66668888")
            pg.click("#loginBtn")
        pg.wait_for_selector("#topbar:not(.hidden)", timeout=20000)
        pg.evaluate("() => switchView('finance')")
        pg.wait_for_function("() => !!(window.finReady && document.querySelector('#univer_container canvas'))", timeout=60000)
        pg.wait_for_timeout(2500)

        P("### Q1 内部状态")
        P(json.dumps(pg.evaluate("""() => ({
          finPresets: typeof window.finPresets,
          undoToken: !!(window.finPresets && window.finPresets.IUndoRedoService),
          api: typeof window.api,
          finUniverAPI: typeof window.finUniverAPI,
          hiCleanup: typeof window.finHiCleanup,
          curSnap: typeof window.fin_currentSnapshot
        })"""), ensure_ascii=False))

        # 工具栏里所有带 undo/撤销 字样的按钮
        P("### 撤销候选按钮: " + json.dumps(pg.evaluate("""() => {
          var r = [];
          document.querySelectorAll('button,[role=button],[class*=btn]').forEach(function(x){
            var t = ((x.getAttribute('aria-label')||'')+' '+(x.title||'')+' '+(x.getAttribute('data-u-comp')||'')+' '+(x.textContent||'')).toLowerCase();
            if (t.indexOf('undo')>=0 || t.indexOf('撤销')>=0 || t.indexOf('hoàn')>=0 || t.indexOf('redo')>=0) r.push(t.trim().slice(0,70));
          });
          return r.slice(0,20);
        }"""), ensure_ascii=False))
        # 工具栏总貌（前 40 个按钮的 data-u-comp）
        P("### 工具栏按钮: " + json.dumps(pg.evaluate("""() => {
          var r = [];
          document.querySelectorAll('[class*=toolbar] button,[data-u-comp]').forEach(function(x){
            var t = (x.getAttribute('data-u-comp')||'')+'|'+((x.getAttribute('aria-label')||x.title||x.textContent||'').trim().slice(0,14));
            if (t.replace(/\\|/g,'').trim()) r.push(t);
          });
          return r.slice(0,40);
        }"""), ensure_ascii=False))

        P("### Q3 编辑→撤销")
        pg.click("#univer_container", position={"x": 300, "y": 200})
        pg.wait_for_timeout(300)
        pg.keyboard.type("ZZTEST", delay=50)
        pg.wait_for_timeout(300)
        pg.keyboard.press("Enter")
        pg.wait_for_timeout(1200)

        def zz():
            return pg.evaluate("""() => {
              var sn = window.fin_currentSnapshot();
              var sid = sn.sheetOrder[0], cd = sn.sheets[sid].cellData, hit = [];
              for (var rk in cd) for (var ck in cd[rk]) { var v = cd[rk][ck] && cd[rk][ck].v; if (String(v).indexOf('ZZTEST')>=0) hit.push(rk+','+ck); }
              return hit;
            }""")

        e1 = zz()
        P("  编辑后: %s" % json.dumps(e1))
        pg.keyboard.press("Control+z")
        pg.wait_for_timeout(1200)
        e2 = zz()
        P("  Ctrl+Z 后: %s  → %s" % (json.dumps(e2), "撤销生效" if (e1 and not e2) else ("编辑都没生效" if not e1 else "★撤销无效")))

        P("### 控制台（undo-clean / hi / fin-keys / error）")
        for l in logs:
            low = l.lower()
            if "undo-clean" in low or "[hi]" in low or "fin-keys" in low or "error" in low or "warn" in low:
                P("  " + l)
    except Exception as e:
        P("FAIL: %r" % e)
    finally:
        try:
            b.close()
        except Exception:
            pass
