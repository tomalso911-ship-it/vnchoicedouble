# -*- coding: utf-8 -*-
"""运行时解剖「撤销失灵」——边跑边落盘 _undo3.txt，任何阶段都能读。
   1) 列出页面暴露的全局（找 finUniver / finUniverAPI / api）
   2) window.finPresets 有没有值、undo-clean 机制有没有启用（控制台那行日志）
   3) 行为测试：真敲值 → Ctrl+Z → 值回不回退
   4) 找撤销按钮并真实点击，看值回不回退
"""
import json
import sys
from playwright.sync_api import sync_playwright

F = open("_undo3.txt", "w", encoding="utf-8")


def P(*a):
    s = " ".join(str(x) for x in a)
    F.write(s + "\n")
    F.flush()
    print(s, flush=True)


logs = []
URL = "http://127.0.0.1:5050/lite?v=undodiag3"

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True, args=["--no-sandbox"])
    try:
        pg = b.new_context(viewport={"width": 1400, "height": 900}).new_page()
        pg.set_default_timeout(25000)
        pg.on("console", lambda m: logs.append("[%s] %s" % (m.type, m.text[:200])))
        pg.on("pageerror", lambda e: logs.append("[pageerror] %s" % str(e)[:250]))
        pg.goto(URL, wait_until="domcontentloaded", timeout=45000)
        pg.wait_for_timeout(600)
        if pg.evaluate("() => { var e=document.getElementById('loginPage'); return e && !e.classList.contains('hidden'); }"):
            pg.fill("#loginUser", "tom")
            pg.fill("#loginPwd", "66668888")
            pg.click("#loginBtn")
            P("已登录")
        pg.wait_for_selector("#topbar:not(.hidden)", timeout=20000)
        pg.evaluate("() => switchView('finance')")
        P("已切到财务页，等待 Univer…")
        pg.wait_for_function("() => !!(window.finReady && document.querySelector('#univer_container canvas'))", timeout=60000)
        pg.wait_for_timeout(1500)
        P("Univer 就绪")

        P("### 1) 暴露的全局（/univer|preset|fin/i）")
        P(json.dumps(pg.evaluate("""() => Object.keys(window).filter(function(k){
            return /univer|preset|^fin/i.test(k);
        }).slice(0,60)"""), ensure_ascii=False))

        P("### 2) finPresets / token")
        P(json.dumps(pg.evaluate("""() => ({
          finPresets: typeof window.finPresets,
          hasIUndoRedo: !!(window.finPresets && window.finPresets.IUndoRedoService),
          api: typeof window.api,
          apiKeys: (window.api && typeof window.api === 'object') ? Object.keys(window.api).slice(0,25) : null
        })"""), ensure_ascii=False))

        def zz():
            return pg.evaluate("""() => {
              try {
                var sn = window.fin_currentSnapshot();
                var sid = sn.sheetOrder[0], cd = sn.sheets[sid].cellData, hit = [];
                for (var rk in cd) for (var ck in cd[rk]) {
                  var v = cd[rk][ck] && cd[rk][ck].v;
                  if (String(v).indexOf('ZZTEST') >= 0) hit.push(rk + ',' + ck);
                }
                return hit;
              } catch(e){ return 'ERR:' + e.message; }
            }""")

        P("### 3) 行为测试：编辑 → Ctrl+Z")
        pg.click("#univer_container", position={"x": 300, "y": 200})
        pg.wait_for_timeout(250)
        pg.keyboard.type("ZZTEST", delay=45)
        pg.wait_for_timeout(250)
        pg.keyboard.press("Enter")
        pg.wait_for_timeout(1200)
        e1 = zz()
        P("  编辑后含 ZZTEST: %s" % json.dumps(e1))
        pg.keyboard.press("Control+z")
        pg.wait_for_timeout(1200)
        e2 = zz()
        P("  Ctrl+Z 后: %s  → %s" % (json.dumps(e2),
                                     "撤销生效" if (e1 and not e2 and isinstance(e1, list)) else
                                     ("编辑未生效" if not e1 else "★撤销无效")))

        P("### 4) 撤销按钮清单与点击")
        btns = pg.evaluate("""() => {
          var r = [];
          document.querySelectorAll('[data-u-comp],button,[role=button]').forEach(function(x, i){
            var comp = x.getAttribute('data-u-comp') || '';
            var t = ((x.getAttribute('aria-label')||'') + ' ' + (x.title||'') + ' ' + (x.textContent||'')).trim();
            if (/undo|redo|撤销|重做|复原|hoàn|phục/i.test(comp + ' ' + t)) {
              r.push({ i: i, comp: comp.slice(0,50), t: t.slice(0,40) });
            }
          });
          return r.slice(0, 15);
        }""")
        P(json.dumps(btns, ensure_ascii=False))
        if btns:
            try:
                sel = '[data-u-comp="%s"]' % btns[0]["comp"] if btns[0].get("comp") else None
                if sel:
                    pg.click(sel, timeout=4000)
                    pg.wait_for_timeout(1200)
                    P("  点击后含 ZZTEST: %s" % json.dumps(zz()))
            except Exception as e:
                P("  点击失败: %r" % e)

        P("### 5) 控制台")
        for l in logs:
            low = l.lower()
            if "undo-clean" in low or "fin-keys" in low or "hi]" in low or "error" in low or "warn" in low:
                P("  " + l)
    except Exception as e:
        P("FAIL: %r" % e)
    finally:
        try:
            b.close()
        except Exception:
            pass
        F.close()
