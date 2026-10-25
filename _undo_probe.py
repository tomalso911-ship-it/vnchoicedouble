# -*- coding: utf-8 -*-
"""复现并解剖「撤销按钮失灵」：
   1) 探测 window.finPresets / IUndoRedoService token / 工具栏按钮清单；
   2) 行为测试：在表格里真敲一个值 → 点撤销/按 Ctrl+Z → 看值有没有回去；
   3) 收集控制台里 undo-clean / hi 相关日志。"""
import json
import sys
from playwright.sync_api import sync_playwright

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

URL = "http://127.0.0.1:5050/lite?v=undodiag1"
out = []
logs = []


def L(*a):
    out.append(" ".join(str(x) for x in a))


with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True, args=["--no-sandbox"])
    try:
        pg = b.new_context(viewport={"width": 1500, "height": 950}).new_page()
        pg.set_default_timeout(30000)
        pg.on("console", lambda m: logs.append("[%s] %s" % (m.type, m.text[:220])))
        pg.on("pageerror", lambda e: logs.append("[pageerror] %s" % str(e)[:300]))
        pg.goto(URL, wait_until="domcontentloaded", timeout=60000)
        pg.wait_for_timeout(1000)
        if pg.evaluate("() => { var e=document.getElementById('loginPage'); return e && !e.classList.contains('hidden'); }"):
            pg.fill("#loginUser", "tom")
            pg.fill("#loginPwd", "66668888")
            pg.click("#loginBtn")
        pg.wait_for_selector("#topbar:not(.hidden)", timeout=30000)
        pg.evaluate("() => switchView('finance')")
        pg.wait_for_function("() => !!(window.finReady && document.querySelector('#univer_container canvas'))", timeout=90000)
        pg.wait_for_timeout(6000)

        info = pg.evaluate("""() => {
          var r = {};
          r.finPresetsType = typeof window.finPresets;
          r.undoToken = !!(window.finPresets && window.finPresets.IUndoRedoService);
          r.apiType = typeof window.api;
          r.finUniverAPIType = typeof window.finUniverAPI;
          try { r.apiHasInjector = !!(window.api && window.api._injector); } catch(e){ r.apiHasInjector = 'err'; }
          try { r.apiMethods = window.api ? Object.getOwnPropertyNames(Object.getPrototypeOf(window.api)).slice(0,30) : []; } catch(e){ r.apiMethods = 'err'; }
          var btns = [];
          document.querySelectorAll('button,[role=button],.univer-btn').forEach(function(x){
            var t = ((x.getAttribute('aria-label')||'') + '|' + (x.title||'') + '|' + (x.textContent||'').trim()).slice(0,60);
            if (t.replace(/\\|/g,'').trim()) btns.push(t);
          });
          r.buttons = btns.slice(0, 80);
          r.buttonCount = btns.length;
          r.ready = !!window.finReady;
          return r;
        }""")
        L("=== 页面内部状态 ===")
        L(json.dumps(info, ensure_ascii=False, indent=1))

        # ---------- 行为测试：敲一个值，再撤销 ----------
        L("")
        L("=== 行为测试：编辑 → 撤销 ===")
        try:
            before = pg.evaluate("""() => {
              var sn = window.fin_currentSnapshot ? window.fin_currentSnapshot() : null;
              if (!sn) return 'no-snapshot-hook';
              var sid = sn.sheetOrder[0];
              var rows = Object.keys(sn.sheets[sid].cellData||{}).map(Number).sort(function(a,b){return a-b;});
              var r = rows[rows.length-1];
              var cd = (sn.sheets[sid].cellData[String(r)]||{})['0'];
              return { sid: sid, row: r, v: cd ? cd.v : null };
            }""")
            L("末行: %s" % json.dumps(before, ensure_ascii=False))
        except Exception as e:
            L("取末行失败: %r" % e)

        pg.click("#univer_container", position={"x": 260, "y": 180})
        pg.wait_for_timeout(500)
        pg.keyboard.type("ZZTEST", delay=60)
        pg.wait_for_timeout(400)
        pg.keyboard.press("Enter")
        pg.wait_for_timeout(1500)
        after_edit = pg.evaluate("""() => {
          var sn = window.fin_currentSnapshot();
          var sid = sn.sheetOrder[0];
          var cd = sn.sheets[sid].cellData;
          var hit = [];
          for (var rk in cd) for (var ck in cd[rk]) { var v = cd[rk][ck] && cd[rk][ck].v; if (String(v).indexOf('ZZTEST') >= 0) hit.push(rk+','+ck); }
          return hit;
        }""")
        L("编辑后含有 ZZTEST 的格子: %s" % json.dumps(after_edit))

        # 按 Ctrl+Z
        pg.keyboard.press("Control+z")
        pg.wait_for_timeout(1500)
        after_undo = pg.evaluate("""() => {
          var sn = window.fin_currentSnapshot();
          var sid = sn.sheetOrder[0];
          var cd = sn.sheets[sid].cellData;
          var hit = [];
          for (var rk in cd) for (var ck in cd[rk]) { var v = cd[rk][ck] && cd[rk][ck].v; if (String(v).indexOf('ZZTEST') >= 0) hit.push(rk+','+ck); }
          return hit;
        }""")
        L("Ctrl+Z 后仍含 ZZTEST 的格子: %s   → %s" % (
            json.dumps(after_undo),
            "撤销生效（值已回退）" if not after_undo else "★撤销无效（值还在）"))

        # 找撤销按钮并点击
        clicked = pg.evaluate("""() => {
          var cands = [];
          document.querySelectorAll('button,[role=button]').forEach(function(x){
            var t = ((x.getAttribute('aria-label')||'') + ' ' + (x.title||'') + ' ' + (x.textContent||'')).toLowerCase();
            if (t.indexOf('undo') >= 0 || t.indexOf('撤销') >= 0 || t.indexOf('复原') >= 0 || t.indexOf('hoàn') >= 0) cands.push(t.trim().slice(0,80));
          });
          return cands;
        }""")
        L("疑似撤销按钮: %s" % json.dumps(clicked, ensure_ascii=False))

        L("")
        L("=== 控制台相关日志 ===")
        for l in logs:
            low = l.lower()
            if ("undo-clean" in low or "[hi]" in low or "error" in low or "warn" in low
                    or "fin-keys" in low or "permission" in low):
                L("  " + l)
    except Exception as e:
        L("FAIL: %r" % e)
    finally:
        try:
            b.close()
        except Exception:
            pass

txt = "\n".join(out)
print(txt)
open("_undo_probe_out.txt", "w", encoding="utf-8").write(txt)
