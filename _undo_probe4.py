# -*- coding: utf-8 -*-
"""解剖 IUndoRedoService：为什么 pushUndoRedo 赋值失败、怎么才能正确静默。"""
import json
from playwright.sync_api import sync_playwright

F = open("_undo4.txt", "w", encoding="utf-8")


def P(*a):
    s = " ".join(str(x) for x in a)
    F.write(s + "\n")
    F.flush()
    print(s, flush=True)


URL = "http://127.0.0.1:5050/lite?v=undodiag4"

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True, args=["--no-sandbox"])
    try:
        pg = b.new_context(viewport={"width": 1400, "height": 900}).new_page()
        pg.set_default_timeout(25000)
        pg.goto(URL, wait_until="domcontentloaded", timeout=45000)
        pg.wait_for_timeout(600)
        if pg.evaluate("() => { var e=document.getElementById('loginPage'); return e && !e.classList.contains('hidden'); }"):
            pg.fill("#loginUser", "tom")
            pg.fill("#loginPwd", "66668888")
            pg.click("#loginBtn")
        pg.wait_for_selector("#topbar:not(.hidden)", timeout=20000)
        pg.evaluate("() => switchView('finance')")
        pg.wait_for_function("() => !!(window.finReady && document.querySelector('#univer_container canvas'))", timeout=60000)
        pg.wait_for_timeout(3000)

        P("### service 解剖")
        P(json.dumps(pg.evaluate("""() => {
          var out = {};
          try {
            var inj = window.finUniver.__getInjector();
            var tok = window.finPresets.IUndoRedoService;
            var ur = inj.get(tok);
            out.ctor = ur && ur.constructor && ur.constructor.name;
            out.isFrozen = Object.isFrozen(ur);
            out.isSealed = Object.isSealed(ur);
            out.isProxyLike = String(ur);
            out.own = Object.getOwnPropertyNames(ur).slice(0, 25);
            var d1 = Object.getOwnPropertyDescriptor(ur, 'pushUndoRedo');
            out.ownDesc = d1 ? {writable: d1.writable, get: !!d1.get, set: !!d1.set, config: d1.configurable} : null;
            var proto = Object.getPrototypeOf(ur);
            out.protoName = proto && proto.constructor && proto.constructor.name;
            var d2 = Object.getOwnPropertyDescriptor(proto, 'pushUndoRedo');
            out.protoDesc = d2 ? {writable: d2.writable, get: !!d2.get, set: !!d2.set, config: d2.configurable} : null;
            out.protoFrozen = Object.isFrozen(proto);
            out.keys = Object.keys(ur).slice(0, 25);
            // 实测赋值
            var orig = ur.pushUndoRedo;
            try { ur.pushUndoRedo = function(){}; out.assignOk = (ur.pushUndoRedo !== orig); }
            catch(e){ out.assignErr = String(e).slice(0,80); }
            try { delete ur.pushUndoRedo; } catch(e){}
            // 用 defineProperty 试
            try {
              Object.defineProperty(ur, 'pushUndoRedo', { value: function(){}, configurable: true, writable: true });
              out.definePropOk = (ur.pushUndoRedo !== orig);
            } catch(e){ out.definePropErr = String(e).slice(0,80); }
            try { delete ur.pushUndoRedo; } catch(e){}
            // 原型级赋值试
            try {
              proto.pushUndoRedo = function(){};
              out.protoAssignOk = (ur.pushUndoRedo !== orig);
            } catch(e){ out.protoAssignErr = String(e).slice(0,80); }
            try { delete proto.pushUndoRedo; } catch(e){}
            // undo 栈
            try {
              var s = ur._getUndoStack ? ur._getUndoStack('vn-report') : null;
              out.undoStackIsArray = Array.isArray(s);
              out.undoStackLen = s ? s.length : -1;
              var s2 = ur._getUndoStack ? ur._getUndoStack('vn-report') : null;
              out.undoStackSameRef = (s === s2);
            } catch(e){ out.stackErr = String(e).slice(0,80); }
            out.hasGetRedoStack = (typeof ur._getRedoStack === 'function');
            return out;
          } catch(e){ return { fatal: String(e).slice(0,120) }; }
        }"""), ensure_ascii=False, indent=1))

        P("### 栈长度随时间变化（3 次采样，间隔 1.2s）")
        for i in range(3):
            P("  采样%d: %s" % (i, pg.evaluate("""() => {
              try { var ur = window.finUniver.__getInjector().get(window.finPresets.IUndoRedoService);
                    var s = ur._getUndoStack('vn-report'); return s ? s.length : -1; } catch(e){ return 'err'; }
            }""")))
            pg.wait_for_timeout(1200)

        P("### 手动真编辑 → 看栈长度与撤销效果")
        def zz():
            return pg.evaluate("""() => {
              var sn = window.fin_currentSnapshot();
              var sid = sn.sheetOrder[0], cd = sn.sheets[sid].cellData, hit = [];
              for (var rk in cd) for (var ck in cd[rk]) {
                var v = cd[rk][ck] && cd[rk][ck].v;
                if (String(v).indexOf('QQTEST') >= 0) hit.push(rk + ',' + ck);
              }
              return hit;
            }""")
        pg.click("#univer_container", position={"x": 320, "y": 210})
        pg.wait_for_timeout(250)
        pg.keyboard.type("QQTEST", delay=45)
        pg.wait_for_timeout(250)
        pg.keyboard.press("Enter")
        pg.wait_for_timeout(1500)
        P("  编辑后含 QQTEST: %s" % json.dumps(zz()))
        P("  编辑后栈长: %s" % pg.evaluate("""() => { try { return window.finUniver.__getInjector().get(window.finPresets.IUndoRedoService)._getUndoStack('vn-report').length; } catch(e){ return 'err'; } }"""))
        P("  pushUndoRedo 是否仍是原函数: %s" % pg.evaluate("""() => { try { var ur = window.finUniver.__getInjector().get(window.finPresets.IUndoRedoService); return /function/.test(String(ur.pushUndoRedo).slice(0,20)) ? String(ur.pushUndoRedo).slice(0,90) : 'other'; } catch(e){ return 'err'; } }"""))
    except Exception as e:
        P("FAIL: %r" % e)
    finally:
        try:
            b.close()
        except Exception:
            pass
        F.close()
