# -*- coding: utf-8 -*-
"""确认 app 能正常载入合并后的越南报表：行数是 389、合并进来的中国行在屏幕上、字体蓝色。"""
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_verify_app_vn_out.txt")
L = []


def log(s):
    L.append(s)
    io.open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(s)


JS = """() => {
  try {
    var snap = finLastSnapshot || fin_currentSnapshot();
    var names = [];
    var sid = null;
    for (var k in snap.sheets){
      var nm = (snap.sheets[k] || {}).name || '';
      names.push(nm);
      if (!sid && /Chi th|Actual Payments|实际支出|Chi thực/i.test(nm)) sid = k;
    }
    if (!sid) sid = snap.sheetOrder[0];
    var cd = snap.sheets[sid].cellData || {};
    var styles = snap.styles || {};
    var rows = Object.keys(cd).length;
    function info(r, c){
      var cell = (cd[String(r)] || {})[String(c)];
      if (!cell) return null;
      var st = (typeof cell.s === 'string') ? styles[cell.s] : cell.s;
      var rgb = (st && st.cl && st.cl.rgb) || (st && st.cl) || null;
      return { v: cell.v, rgb: rgb };
    }
    return {
      sheet: sid, sheetNames: names, rows: rows,
      row21: info(21, 2), row21desc: info(21, 2),
      row21B: info(21, 1), row21E: info(21, 4),
      row20B: info(20, 1), row20E: info(20, 4),
      row3E: info(2, 4),
      title: (document.getElementById('fin_status') || {}).textContent
    };
  } catch(e){ return { err: String(e) }; }
}"""

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True, args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 1500, "height": 900})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append("console.error: " + m.text) if m.type == "error" else None)
    pg.goto("http://127.0.0.1:5050/lite", wait_until="domcontentloaded")
    pg.wait_for_timeout(1500)
    pg.fill("#loginUser", "tom")
    pg.fill("#loginPwd", "66668888")
    pg.click("#loginBtn")
    pg.wait_for_selector("#topbar:not(.hidden)", timeout=20000)
    pg.evaluate("() => { try { switchView('finance'); } catch(e){} }")
    ok = False
    for _ in range(60):
        pg.wait_for_timeout(500)
        st = pg.evaluate("() => ({ r: (typeof finReady!=='undefined')&&finReady, k: (typeof FIN_KIND!=='undefined')?FIN_KIND:'?' })")
        if st.get("r"):
            ok = True
            break
    # 等快照真正进来（越南报表 389 行，转换+建单元需要几秒）
    snap_ok = False
    for _ in range(60):
        pg.wait_for_timeout(1000)
        try:
            if pg.evaluate("() => { try { var s = fin_currentSnapshot(); return !!(s && s.sheetOrder && s.sheetOrder.length); } catch(e){ return false; } }"):
                snap_ok = True
                break
        except Exception:
            pass
    log("Univer 就绪 = %s（当前报表 = %s）；快照已载入 = %s" % (ok, st.get("k"), snap_ok))
    r = pg.evaluate(JS)
    log("快照诊断 = %s" % json.dumps(r, ensure_ascii=False, default=str))
    if not r.get("err"):
        log("  行数（含表头等）= %s" % r.get("rows"))
        log("  第 22 行（Excel，0 基 21）B=%s E=%s 字色=%s"
            % (r.get("row21B"), r.get("row21E"), (r.get("row21B") or {}).get("rgb")))
        log("  第 21 行（相邻越南行）B=%s E=%s 字色=%s"
            % (r.get("row20B"), r.get("row20E"), (r.get("row20B") or {}).get("rgb")))
    log("页面报错 = %s" % (errs[:6] if errs else "无"))
    b.close()
