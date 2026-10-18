# -*- coding: utf-8 -*-
"""探针 37：标准颜色面板（COLOR-MERGE / COLOR-HIDE-BUCKET-20261018）验收。

覆盖：
  1) 原生填充颜色按钮（paint-bucket）与字体颜色按钮都已整块隐藏；
  2) 自建面板「字体颜色」= 12 深色 + 12 浅色，「填充颜色」= 12 浅色 + 12 深色（各 24 个色块）；
  3) 用浅色上字体色、用深色上填充色都能真正落盘，并且各记一步撤销；
  4) Ctrl+Z 能依次撤销回基线；
  5) 股东权益表同样：按钮隐藏 + 面板 24 色。
退出码：全过 0，有失败 1。
"""
import json
import sys
import traceback

from playwright.sync_api import sync_playwright

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

URL = "http://127.0.0.1:5050/lite?v=color37"
FR, FC = 6, 6
ER, EC = 3, 3
FAILS = []

TEXT_COLORS = ['#000000', '#374151', '#6b7280', '#dc2626', '#ea580c', '#d97706',
               '#ca8a04', '#16a34a', '#0d9488', '#2563eb', '#7c3aed', '#db2777']
BG_COLORS = ['#ffffff', '#f3f4f6', '#fef3c7', '#dcfce7', '#dbeafe', '#fae8ff',
             '#fee2e2', '#e0f2fe', '#fef9c3', '#e5e7eb', '#fde68a', '#bbf7d0']

ST = """(arg) => {
  var sel = arg.sel, R = arg.r, C = arg.c;
  var out = { histFin: 0, histEq: 0, style: null };
  try {
    var h = window.finUndoHist || [];
    for (var i = 0; i < h.length; i++){
      if (String(h[i].unitId) === 'equity-report') out.histEq++; else out.histFin++;
    }
  } catch(e){}
  try {
    var sn, sid;
    if (sel === 'eq'){
      sn = window.__eqAPI().getActiveWorkbook().getSnapshot();
      try { sid = window.__eqAPI().getActiveWorkbook().getActiveSheet().getSheetId(); } catch(e){ sid = null; }
    } else {
      sn = window.fin_currentSnapshot();
      try { var sh = window.finSheetObj(); sid = sh && sh.getSheetId ? sh.getSheetId() : null; } catch(e){ sid = null; }
    }
    var ks = Object.keys(sn.sheets || {});
    var sh1 = (sid && sn.sheets[sid]) ? sn.sheets[sid] : sn.sheets[ks[0]];
    var cell = (sh1 && sh1.cellData && sh1.cellData[R]) ? sh1.cellData[R][C] : null;
    var s = cell ? cell.s : null;
    if (typeof s === 'string') s = (sn.styles || {})[s];
    out.style = s || null;
  } catch(e){ out.style = 'ERR:' + e; }
  return out;
}"""

BTN = """(root) => {
  var out = {};
  ['paint-bucket', 'font-color'].forEach(function(k){
    var svg = document.querySelector(root + ' svg.univerjs-icon-' + k);
    if (!svg){ out[k] = 'gone'; return; }
    var host = svg.closest('.univer-toolbar-item-select-button') || svg.closest('button') || svg;
    var r = host.getBoundingClientRect();
    out[k] = { display: host.style.display, w: Math.round(r.width), h: Math.round(r.height) };
  });
  return out;
}"""

GRID = """() => {
  var p = document.getElementById('stdColorPop');
  if (!p) return { visible: false, grids: null };
  var out = { visible: p.style.display !== 'none', grids: {} };
  ['text','bg'].forEach(function(m){
    var g = p.querySelector('.scp-grid[data-mode="' + m + '"]');
    out.grids[m] = g ? Array.prototype.map.call(g.querySelectorAll('.scp-sw'), function(s){
      return s.getAttribute('data-hex');
    }) : null;
  });
  return out;
}"""

POS = """(arg) => {
  var p = document.getElementById('stdColorPop');
  if (!p) return null;
  var g = p.querySelector('.scp-grid[data-mode="' + arg.mode + '"]');
  if (!g) return null;
  var sws = g.querySelectorAll('.scp-sw');
  for (var i = 0; i < sws.length; i++){
    if (String(sws[i].getAttribute('data-hex')).toLowerCase() !== arg.hex) continue;
    var r = sws[i].getBoundingClientRect();
    if (r.width < 2) return null;
    return { x: Math.round(r.x + r.width / 2), y: Math.round(r.y + r.height / 2) };
  }
  return null;
}"""


def say(*a):
    print(*a, flush=True)


def ok(name, cond, extra=""):
    say(("PASS  " if cond else "FAIL  ") + name + (("  |  " + str(extra)) if extra else ""))
    if not cond:
        FAILS.append(name)


def blob(s):
    try:
        return json.dumps(s, ensure_ascii=False)[:260]
    except Exception:
        return str(s)[:260]


def st(pg, sel, r, c):
    return pg.evaluate(ST, {"sel": sel, "r": r, "c": c})


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
        say("BUILD:", pg.evaluate("() => window.FIN_UNDO_BUILD"))

        # ---- 1. 原生颜色按钮是否都隐藏 ----
        btns = pg.evaluate(BTN, "#univer_container")
        say("原生按钮状态:", blob(btns))
        pb = btns.get("paint-bucket")
        fc = btns.get("font-color")
        ok("财务 填充颜色按钮已隐藏",
           isinstance(pb, dict) and pb.get("display") == "none" and pb.get("w", 0) == 0, blob(pb))
        ok("财务 字体颜色按钮已隐藏",
           (fc == "gone") or (isinstance(fc, dict) and fc.get("display") == "none" and fc.get("w", 0) == 0), blob(fc))

        # ---- 2. 面板两组各 24 色（互相追加彼此的颜色）----
        pg.evaluate("""() => { var c=document.querySelector('#univer_container canvas'); if(c){ c.setAttribute('tabindex','0'); c.focus(); } }""")
        pg.evaluate("([r,c]) => { window.finUniverAPI.getActiveWorkbook().getActiveSheet().getRange(r,c).activate(); }", [FR, FC])
        pg.wait_for_timeout(600)
        base = st(pg, "fin", FR, FC)
        pg.click('[data-std-color-btn="fin"]')
        pg.wait_for_timeout(500)
        g = pg.evaluate(GRID)
        say("面板色块:", blob(g))
        exp_text = TEXT_COLORS + BG_COLORS
        exp_bg = BG_COLORS + TEXT_COLORS
        ok("面板已打开", bool(g.get("visible")), g.get("visible"))
        ok("字体颜色 24 色（深12+浅12）", g["grids"].get("text") == exp_text,
           "%s 个" % (len(g["grids"].get("text") or [])))
        ok("填充颜色 24 色（浅12+深12）", g["grids"].get("bg") == exp_bg,
           "%s 个" % (len(g["grids"].get("bg") or [])))

        # ---- 3. 用「浅色」上字体色 → 记一步 ----
        pos = pg.evaluate(POS, {"mode": "text", "hex": "#fef3c7"})
        ok("字体颜色组里找到浅色 #fef3c7", bool(pos), blob(pos))
        if pos:
            pg.mouse.click(pos["x"], pos["y"])
            pg.wait_for_timeout(1500)
        s = st(pg, "fin", FR, FC)
        cl = (s["style"] or {}).get("cl") if isinstance(s["style"], dict) else None
        ok("浅色已用于字体色", isinstance(cl, dict) and str(cl.get("rgb", "")).lower() == "#fef3c7", blob(s["style"]))
        ok("字体上色 记一步", s["histFin"] == base["histFin"] + 1, "%s -> %s" % (base["histFin"], s["histFin"]))
        ok("面板点击后自动收起", not pg.evaluate(GRID)["visible"], "closed")

        # ---- 4. 用「深色」上填充色 → 记一步 ----
        pg.click('[data-std-color-btn="fin"]')
        pg.wait_for_timeout(500)
        pos = pg.evaluate(POS, {"mode": "bg", "hex": "#dc2626"})
        ok("填充颜色组里找到深色 #dc2626", bool(pos), blob(pos))
        if pos:
            pg.mouse.click(pos["x"], pos["y"])
            pg.wait_for_timeout(1500)
        s = st(pg, "fin", FR, FC)
        bg = (s["style"] or {}).get("bg") if isinstance(s["style"], dict) else None
        ok("深色已用于填充色", isinstance(bg, dict) and str(bg.get("rgb", "")).lower() == "#dc2626", blob(s["style"]))
        ok("填充上色 记一步", s["histFin"] == base["histFin"] + 2, "%s -> %s" % (base["histFin"], s["histFin"]))

        # ---- 5. Ctrl+Z 两次回基线 ----
        pg.evaluate("""() => { var c=document.querySelector('#univer_container canvas'); if(c){ c.focus(); } }""")
        pg.keyboard.press("Control+z"); pg.wait_for_timeout(1400)
        s = st(pg, "fin", FR, FC)
        ok("Ctrl+Z 撤掉填充色",
           not (isinstance(s["style"], dict) and (s["style"].get("bg") or {}).get("rgb")), blob(s["style"]))
        pg.keyboard.press("Control+z"); pg.wait_for_timeout(1400)
        s = st(pg, "fin", FR, FC)
        ok("再 Ctrl+Z 撤掉字体色",
           not (isinstance(s["style"], dict) and (s["style"].get("cl") or {}).get("rgb")), blob(s["style"]))
        ok("两次撤销后账本归零", s["histFin"] == base["histFin"], s["histFin"])

        # ---- 6. 权益表：按钮隐藏 + 面板 24 色 ----
        pg.evaluate("() => switchView('equity')")
        pg.wait_for_function("() => !!document.querySelector('#equity_container canvas')", timeout=60000)
        pg.wait_for_timeout(4000)
        btns2 = pg.evaluate(BTN, "#equity_container")
        say("权益原生按钮状态:", blob(btns2))
        pb2 = btns2.get("paint-bucket")
        ok("权益 填充颜色按钮已隐藏",
           isinstance(pb2, dict) and pb2.get("display") == "none" and pb2.get("w", 0) == 0, blob(pb2))
        pg.click('[data-std-color-btn="eq"]')
        pg.wait_for_timeout(500)
        g2 = pg.evaluate(GRID)
        ok("权益 面板字体颜色 24 色", (g2.get("grids") or {}).get("text") == exp_text,
           "%s 个" % len(((g2.get("grids") or {}).get("text")) or []))
        ok("权益 面板填充颜色 24 色", (g2.get("grids") or {}).get("bg") == exp_bg,
           "%s 个" % len(((g2.get("grids") or {}).get("bg")) or []))

        say("---- 结果：%d 项失败 ----" % len(FAILS))
        if FAILS:
            say("FAILED:", "; ".join(FAILS))
        b.close()
    return 1 if FAILS else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        traceback.print_exc()
        sys.exit(2)
