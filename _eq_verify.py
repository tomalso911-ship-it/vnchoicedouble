# -*- coding: utf-8 -*-
"""回滚后核对：股东权益表 D4/G7/D10 的值与样式应为「干净」状态。"""
import sys

from playwright.sync_api import sync_playwright

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

URL = "http://127.0.0.1:5050/lite?v=eqverify"
CELLS = [(3, 3), (6, 6), (9, 3)]

READ = """(cells) => {
  var sn = window.__eqAPI().getActiveWorkbook().getSnapshot();
  var sid = window.__eqAPI().getActiveWorkbook().getActiveSheet().getSheetId();
  var sh = sn.sheets[sid];
  var out = [];
  for (var i = 0; i < cells.length; i++){
    var cell = sh.cellData && sh.cellData[cells[i][0]] ? sh.cellData[cells[i][0]][cells[i][1]] : null;
    out.push({ r: cells[i][0], c: cells[i][1], v: cell ? cell.v : null, hasS: !!(cell && cell.s) });
  }
  return out;
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
        pg.evaluate("() => switchView('equity')")
        pg.wait_for_function("() => !!document.querySelector('#equity_container canvas')", timeout=60000)
        pg.wait_for_timeout(6000)
        print("cells:", pg.evaluate(READ, CELLS), flush=True)
        b.close()


if __name__ == "__main__":
    main()
