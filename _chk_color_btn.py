# -*- coding: utf-8 -*-
"""列出财务/权益两套 Univer 工具栏里所有按钮的 svg class，用来定位原生「颜色」按钮。"""
import sys

from playwright.sync_api import sync_playwright

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

URL = "http://127.0.0.1:5050/lite?v=chkcolor"

JS = """(root) => {
  var host = document.querySelector(root + ' .univer-toolbar-container');
  if (!host) return { err: 'no-toolbar' };
  var out = [];
  var svgs = host.querySelectorAll('svg');
  for (var i = 0; i < svgs.length; i++) {
    var cls = svgs[i].getAttribute('class') || '';
    var btn = svgs[i].closest('button') || svgs[i].parentElement;
    var item = svgs[i].closest('.univer-toolbar-item-select-button') || null;
    out.push({
      cls: cls,
      btnTitle: btn ? (btn.getAttribute('title') || btn.getAttribute('aria-label') || '') : '',
      inSelect: !!item,
      visible: !!(svgs[i].getBoundingClientRect().width > 1)
    });
  }
  return { n: svgs.length, items: out };
}"""


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
        pg.wait_for_timeout(3500)
        r = pg.evaluate(JS, "#univer_container")
        print("=== finance ===", flush=True)
        for it in (r.get("items") or []):
            print(("V " if it["visible"] else "- ") + (it["cls"] or "(no-class)")
                  + " | sel=" + str(it["inSelect"]) + " | " + it["btnTitle"], flush=True)
        pg.evaluate("() => switchView('equity')")
        pg.wait_for_function("() => !!document.querySelector('#equity_container .univer-toolbar-container')", timeout=60000)
        pg.wait_for_timeout(4000)
        r2 = pg.evaluate(JS, "#equity_container")
        print("=== equity ===", flush=True)
        for it in (r2.get("items") or []):
            print(("V " if it["visible"] else "- ") + (it["cls"] or "(no-class)")
                  + " | sel=" + str(it["inSelect"]) + " | " + it["btnTitle"], flush=True)
        b.close()


if __name__ == "__main__":
    main()
