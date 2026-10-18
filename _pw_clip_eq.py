# -*- coding: utf-8 -*-
"""诊断：股东权益 #equity_container 里 Ctrl+C / Ctrl+X / Ctrl+V 是否真的能写/读到剪贴板。"""
import json
import sys

from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:5050/lite?v=clipeq"
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

DBG = r"""
() => {
  window.__clipDbg = { keys: [], copies: [], cuts: [], pastes: [] };
  function desc(t){
    if (!t) return 'null';
    var cls = (t.className && String(t.className)) ? String(t.className).slice(0,50) : '';
    return (t.tagName || '') + (cls ? '.' + cls : '');
  }
  window.addEventListener('keydown', function(e){
    if ((e.ctrlKey || e.metaKey) && /^[cxvCX V]$/.test(e.key)) {
      var rec = { k: e.key, target: desc(e.target) };
      window.__clipDbg.keys.push(rec);
      setTimeout(function(){ rec.prevented = e.defaultPrevented; }, 0);
    }
  }, true);
  document.addEventListener('copy', function(e){ window.__clipDbg.copies.push({ prevented: e.defaultPrevented }); }, true);
  document.addEventListener('cut', function(e){ window.__clipDbg.cuts.push({ prevented: e.defaultPrevented }); }, true);
  document.addEventListener('paste', function(e){
    var t = '';
    try { t = e.clipboardData ? e.clipboardData.getData('text/plain') : ''; } catch(_){}
    window.__clipDbg.pastes.push({ len: t.length, txt: t.slice(0,50) });
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
        # 权益页有长轮询，networkidle 可能永远不触发 → 用 domcontentloaded + 手动等待
        pg.goto(URL, wait_until="domcontentloaded", timeout=45000)
        pg.wait_for_timeout(3000)
        if pg.evaluate("() => { var e=document.getElementById('loginPage'); return e && !e.classList.contains('hidden'); }"):
            pg.fill("#loginUser", "tom")
            pg.fill("#loginPwd", "66668888")
            pg.click("#loginBtn")
        pg.wait_for_selector("#topbar:not(.hidden)", timeout=25000)
        pg.wait_for_timeout(600)

        pg.evaluate("() => { switchView('equity'); }")
        ok = False
        for _ in range(120):
            pg.wait_for_timeout(400)
            if pg.evaluate("() => !!document.querySelector('#equity_container canvas')"):
                ok = True
                break
        out['canvas'] = ok
        if not ok:
            out['errs'] = errs[:3]
            print(json.dumps(out, ensure_ascii=False))
            b.close()
            return
        pg.wait_for_timeout(3000)

        geo = pg.evaluate("""() => { const c = document.querySelector('#equity_container canvas');
            if (!c) return null; const r = c.getBoundingClientRect();
            return { x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) }; }""")
        out['canvasGeo'] = geo
        if geo:
            pg.mouse.click(geo["x"] + 120, geo["y"] + 90)
            pg.wait_for_timeout(700)

        pg.evaluate(DBG)
        out['active'] = pg.evaluate(
            "() => { var a=document.activeElement; return a ? (a.tagName+'|'+String(a.className||'').slice(0,50)) : 'null'; }")

        out['selectAll'] = pg.evaluate("() => { try { return eqSelectAll(); } catch(e){ return 'ERR ' + e.message; } }")
        pg.wait_for_timeout(600)

        # 编辑覆盖层尺寸（全局 vs 各容器内）—— 判断 isEditingCell 是否被另一套实例带偏
        out['editors'] = pg.evaluate("""() => {
          function dump(root, sel){
            var arr = [];
            try {
              (root || document).querySelectorAll('.univer-editor-container').forEach(function(el){
                var r = el.getBoundingClientRect();
                arr.push({ w: Math.round(r.width), h: Math.round(r.height) });
              });
            } catch(e){}
            return arr;
          }
          return {
            all: dump(document, null),
            fin: dump(document.getElementById('univer_container'), null),
            eq: dump(document.getElementById('equity_container'), null)
          };
        }""")
        out['clipLockFailed'] = pg.evaluate("() => !!window.__CLIP_LOCK_FAILED")
        out['hasWinClip'] = pg.evaluate("() => typeof window.win_clipWrite")

        out['clipBefore'] = pg.evaluate("() => { try { return navigator.clipboard.readText(); } catch(e){ return 'ERR'; } }")

        pg.keyboard.press("Control+c")
        pg.wait_for_timeout(1200)
        out['finClipLast'] = pg.evaluate("() => window.__finClipLast || null")
        try:
            out['clipAfterCopy'] = pg.evaluate("() => navigator.clipboard.readText()")
        except Exception as e:
            out['clipAfterCopy'] = 'ERR ' + str(e)[:80]

        # 换到空白处粘贴
        pg.keyboard.press("Control+Home")
        pg.wait_for_timeout(300)
        for _ in range(3):
            pg.keyboard.press("ArrowDown")
            pg.wait_for_timeout(60)
        pg.keyboard.press("Control+v")
        pg.wait_for_timeout(1500)

        out['dbg'] = pg.evaluate("() => window.__clipDbg")
        out['errs'] = errs[:3]
        b.close()

    txt = json.dumps(out, ensure_ascii=False, indent=1)
    open('_clip_eq_out.txt', 'w', encoding='utf-8').write(txt)


main()
