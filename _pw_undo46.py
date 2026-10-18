# -*- coding: utf-8 -*-
"""探针 46：格式类动作是否可撤销（用户 2026-10-18「每一步动作都要能撤回」）。

只测样式，不动结构（不插行/不合并），避免改动真实报表。
步骤：加粗 / 字色 / 对齐 / 数字格式 → 每步按 Ctrl+Z，看是否回退。
"""
import json
import sys
import traceback

from playwright.sync_api import sync_playwright

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

URL = "http://127.0.0.1:5050/lite?v=undo46"
R, C = 6, 6
FAILS = []

ST = """(arg) => {
  var sn = window.fin_currentSnapshot();
  var sid = null;
  try { var sh = window.finSheetObj(); sid = sh && sh.getSheetId ? sh.getSheetId() : null; } catch(e){}
  var sheet = (sid && sn.sheets[sid]) ? sn.sheets[sid] : sn.sheets[Object.keys(sn.sheets)[0]];
  var cell = sheet && sheet.cellData && sheet.cellData[arg.r] ? sheet.cellData[arg.r][arg.c] : null;
  var s = cell ? cell.s : null;
  if (typeof s === 'string') s = (sn.styles || {})[s];
  var h = window.finUndoHist || [];
  return { style: s || null, hist: h.length, last: (h.length ? h[h.length-1] : null),
           v: cell ? cell.v : null };
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
        pg.wait_for_timeout(4000)

        # 工具栏图标清单（找加粗/对齐/字号/数字格式）
        icons = pg.evaluate("""() => {
          var out = [];
          document.querySelectorAll('#univer_container .univer-toolbar-container svg').forEach(function(sv){
            var host = sv.closest('.univer-toolbar-item-select-button') || sv.closest('button') || sv.parentElement;
            var r = host ? host.getBoundingClientRect() : {width:0};
            if (r.width > 1) out.push(sv.getAttribute('class') || '');
          });
          return out;
        }""")
        say("工具栏可见图标:", json.dumps(icons, ensure_ascii=False))

        def focus_cell():
            pg.evaluate("""(arg) => {
              window.finUniverAPI.getActiveWorkbook().getActiveSheet().getRange(arg.r, arg.c).activate();
              var c = document.querySelector('#univer_container canvas');
              if (c) { c.setAttribute('tabindex','0'); c.focus(); }
            }""", {"r": R, "c": C})
            pg.wait_for_timeout(600)

        def click_icon(keyword):
            el = pg.evaluate("""(kw) => {
              var best = null;
              document.querySelectorAll('#univer_container .univer-toolbar-container svg').forEach(function(sv){
                var cls = sv.getAttribute('class') || '';
                if (cls.indexOf(kw) < 0) return;
                var host = sv.closest('button') || sv.parentElement;
                var r = host.getBoundingClientRect();
                if (r.width < 2) return;
                if (!best) best = { x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2) };
              });
              return best;
            }""", keyword)
            if el:
                pg.mouse.click(el["x"], el["y"])
                pg.wait_for_timeout(1300)
            return el

        base = pg.evaluate(ST, {"r": R, "c": C})
        say("基线:", blob(base))

        # ---- A. 加粗 ----
        focus_cell()
        hit = click_icon("bold")
        ok("找到加粗按钮", bool(hit), blob(hit))
        a1 = pg.evaluate(ST, {"r": R, "c": C})
        say("加粗后:", blob(a1))
        ok("加粗生效", bool(a1["style"]) and a1["style"].get("bl") == 1, blob(a1["style"]))
        ok("加粗记一步", a1["hist"] == base["hist"] + 1, "%s -> %s" % (base["hist"], a1["hist"]))
        pg.evaluate("""() => { var c=document.querySelector('#univer_container canvas'); if(c){ c.focus(); } }""")
        pg.keyboard.press("Control+z"); pg.wait_for_timeout(1500)
        a2 = pg.evaluate(ST, {"r": R, "c": C})
        ok("Ctrl+Z 撤掉加粗", not (a2["style"] or {}).get("bl"), blob(a2["style"]))

        # ---- B. 字色（自建色板）----
        focus_cell()
        pg.click('[data-std-color-btn="fin"]')
        pg.wait_for_timeout(600)
        pos = pg.evaluate("""() => {
          var p = document.getElementById('stdColorPop');
          var g = p && p.querySelector('.scp-grid[data-mode="text"]');
          if (!g) return null;
          var sw = g.querySelectorAll('.scp-sw');
          var el = sw[3];
          var r = el.getBoundingClientRect();
          return { x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2), hex: el.getAttribute('data-hex') };
        }""")
        ok("找到色板色块", bool(pos), blob(pos))
        if pos:
            pg.mouse.click(pos["x"], pos["y"])
            pg.wait_for_timeout(1600)
        b1 = pg.evaluate(ST, {"r": R, "c": C})
        say("上色后:", blob(b1["style"]))
        ok("字色生效", bool(b1["style"]) and ((b1["style"].get("cl") or {}).get("rgb")), blob(b1["style"]))
        ok("字色记一步", b1["hist"] == base["hist"] + 1, "%s -> %s" % (base["hist"], b1["hist"]))
        pg.evaluate("""() => { var c=document.querySelector('#univer_container canvas'); if(c){ c.focus(); } }""")
        pg.keyboard.press("Control+z"); pg.wait_for_timeout(1500)
        b2 = pg.evaluate(ST, {"r": R, "c": C})
        ok("Ctrl+Z 撤掉字色", not ((b2["style"] or {}).get("cl") or {}).get("rgb"), blob(b2["style"]))

        # ---- C. 对齐（走 set-style {type:'ht'}，与工具栏对齐按钮同一类命令）----
        focus_cell()
        hit = pg.evaluate("""(arg) => {
          try {
            var api = window.finUniverAPI;
            var sh = api.getActiveWorkbook().getActiveSheet();
            api.executeCommand('sheet.command.set-style', { style: { type: 'ht', value: 2 } });
            return { ok: true };
          } catch(e){ return { err: String(e) }; }
        }""", {"r": R, "c": C})
        pg.wait_for_timeout(1400)
        say("对齐命令:", blob(hit))
        c1 = pg.evaluate(ST, {"r": R, "c": C})
        say("对齐后:", blob(c1["style"]))
        if hit:
            ok("对齐记一步", c1["hist"] == base["hist"] + 1, "%s -> %s" % (base["hist"], c1["hist"]))
            pg.evaluate("""() => { var c=document.querySelector('#univer_container canvas'); if(c){ c.focus(); } }""")
            pg.keyboard.press("Control+z"); pg.wait_for_timeout(1500)
            c2 = pg.evaluate(ST, {"r": R, "c": C})
            ok("Ctrl+Z 撤掉对齐", c2["hist"] == base["hist"], "%s -> %s" % (c1["hist"], c2["hist"]))

        # ---- D. 数字格式（numfmt 命令）----
        pg.evaluate("""(arg) => {
          try {
            var api = window.finUniverAPI;
            var sh = api.getActiveWorkbook().getActiveSheet();
            var sid = sh.getSheetId();
            var uid = api.getActiveWorkbook().getId();
            api.executeCommand('sheet.command.numfmt.set.numfmt', {
              values: [{ row: arg.r, col: arg.c, pattern: '#,##0.00' }]
            });
          } catch(e){ window.__fmtErr = String(e); }
        }""", {"r": R, "c": C})
        pg.wait_for_timeout(1600)
        d1 = pg.evaluate(ST, {"r": R, "c": C})
        say("数字格式后:", blob(d1["style"]))
        ok("数字格式生效", bool(((d1["style"] or {}).get("n") or {}).get("pattern")), blob(d1["style"]))
        ok("数字格式记一步", d1["hist"] == base["hist"] + 1, "%s -> %s" % (base["hist"], d1["hist"]))
        pg.evaluate("""() => { var c=document.querySelector('#univer_container canvas'); if(c){ c.focus(); } }""")
        pg.keyboard.press("Control+z"); pg.wait_for_timeout(1500)
        d2 = pg.evaluate(ST, {"r": R, "c": C})
        ok("Ctrl+Z 撤掉数字格式", not ((d2["style"] or {}).get("n") or {}).get("pattern"), blob(d2["style"]))

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
