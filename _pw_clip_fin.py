# -*- coding: utf-8 -*-
"""诊断（只读）：财务报表 #univer_container 里 Ctrl+C / Ctrl+X / Ctrl+V 到底卡在哪一环。

判定分叉（这是本次排查的关键）：
  · keydown 到达 window 且 defaultPrevented=true  → Univer 认了这个快捷键；
  · copy/cut 事件是否触发                        → Univer 的复制命令有没有真正执行；
  · 剪贴板内容是否为空                          → 写剪贴板成功/失败；
  · paste 事件是否触发                          → Univer 有没有收到粘贴。
"""
import json
import sys

from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:5050/lite?v=clipfin"
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

DBG = r"""
() => {
  window.__clipDbg = { keys: [], copies: [], cuts: [], pastes: [], active: '' };
  function desc(t){
    if (!t) return 'null';
    var cls = (t.className && String(t.className)) ? String(t.className).slice(0,60) : '';
    return (t.tagName || '') + (cls ? '.' + cls : '');
  }
  window.addEventListener('keydown', function(e){
    if ((e.ctrlKey || e.metaKey) && /^[cxvCX V]$/.test(e.key)) {
      var rec = { k: e.key, target: desc(e.target), at: desc(document.activeElement) };
      window.__clipDbg.keys.push(rec);
      setTimeout(function(){ rec.prevented = e.defaultPrevented; }, 0);
    }
  }, true);
  document.addEventListener('copy', function(e){
    var t = '';
    try { t = String(window.getSelection && window.getSelection()); } catch(_){}
    window.__clipDbg.copies.push({ prevented: e.defaultPrevented, sel: t.slice(0,80) });
  }, true);
  document.addEventListener('cut', function(e){ window.__clipDbg.cuts.push({ prevented: e.defaultPrevented }); }, true);
  document.addEventListener('paste', function(e){
    var t = '';
    try { t = e.clipboardData ? e.clipboardData.getData('text/plain') : ''; } catch(_){}
    window.__clipDbg.pastes.push({ prevented: e.defaultPrevented, len: t.length, txt: t.slice(0,60) });
  }, true);
  return true;
}
"""


def main():
    out = {}
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True, args=["--no-sandbox"])
        ctx = b.new_context(viewport={"width": 1500, "height": 950},
                            permissions=["clipboard-read", "clipboard-write"])
        pg = ctx.new_page()
        pg.on("dialog", lambda d: d.dismiss())
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)[:200]))
        pg.add_init_script("try{localStorage.setItem('won_lang','\"zh\"');}catch(e){}")
        pg.goto(URL, wait_until="networkidle")
        pg.wait_for_timeout(800)
        if pg.evaluate("() => { var e=document.getElementById('loginPage'); return e && !e.classList.contains('hidden'); }"):
            pg.fill("#loginUser", "tom")
            pg.fill("#loginPwd", "66668888")
            pg.click("#loginBtn")
        pg.wait_for_selector("#topbar:not(.hidden)", timeout=25000)
        pg.wait_for_timeout(600)

        pg.evaluate("() => { switchView('finance'); }")
        ok = False
        for _ in range(90):
            pg.wait_for_timeout(400)
            if pg.evaluate("() => !!document.querySelector('#univer_container canvas')"):
                ok = True
                break
        out['canvas'] = ok
        if not ok:
            print(json.dumps(out, ensure_ascii=False))
            b.close()
            return
        pg.wait_for_timeout(2500)

        geo = pg.evaluate("""() => { const c = document.querySelector('#univer_container canvas');
            if (!c) return null; const r = c.getBoundingClientRect();
            return { x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) }; }""")
        out['canvasGeo'] = geo
        if geo:
            pg.mouse.click(geo["x"] + 90, geo["y"] + 70)
            pg.wait_for_timeout(600)

        pg.evaluate(DBG)
        out['activeAfterClick'] = pg.evaluate(
            "() => { var a=document.activeElement; return a ? (a.tagName+'|'+String(a.className||'').slice(0,60)+'|tab='+(a.getAttribute&&a.getAttribute('tabindex'))) : 'null'; }")

        # 让选区落在有内容的格子上：先 Ctrl+Home 回 A1，再走两格
        pg.keyboard.press("Control+Home")
        pg.wait_for_timeout(300)
        pg.keyboard.press("ArrowDown")
        pg.keyboard.press("ArrowRight")
        pg.wait_for_timeout(400)

        out['sel'] = pg.evaluate("() => { try { var a=window.finUniverAPI; return String(a && a.getActiveWorkbook && 1); } catch(e){ return 'ERR'; } }")

        # --- Ctrl+C ---
        pg.evaluate("() => { try { navigator.clipboard.writeText('__CLEAR__'); } catch(e){} }")
        pg.wait_for_timeout(200)
        # 先全选（保证选区内一定有内容），再复制
        out['selectAll'] = pg.evaluate("() => { try { return finSelectAll(); } catch(e){ return 'ERR ' + e.message; } }")
        pg.wait_for_timeout(500)
        pg.keyboard.press("Control+c")
        pg.wait_for_timeout(1200)
        try:
            out['clipAfterCopy'] = pg.evaluate("() => navigator.clipboard.readText()")
        except Exception as e:
            out['clipAfterCopy'] = 'ERR ' + str(e)[:100]
        out['finClipLastC'] = pg.evaluate("() => window.__finClipLast || null")

        # --- Ctrl+X ---
        pg.keyboard.press("Control+x")
        pg.wait_for_timeout(1200)
        try:
            out['clipAfterCut'] = pg.evaluate("() => navigator.clipboard.readText()")
        except Exception as e:
            out['clipAfterCut'] = 'ERR ' + str(e)[:100]

        # --- Ctrl+V（换到下面几行的空格）---
        for _ in range(6):
            pg.keyboard.press("ArrowDown")
            pg.wait_for_timeout(60)
        pg.wait_for_timeout(300)
        pg.keyboard.press("Control+v")
        pg.wait_for_timeout(1500)

        out['dbg'] = pg.evaluate("() => window.__clipDbg")
        out['errs'] = errs[:3]
        try:
            pg.screenshot(path="_clip_fin_test.png")
        except Exception:
            pass
        b.close()

    txt = json.dumps(out, ensure_ascii=False, indent=1)
    open('_clip_fin_out.txt', 'w', encoding='utf-8').write(txt)
    print(txt)


main()
