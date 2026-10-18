# -*- coding: utf-8 -*-
"""探针 36：样式撤销/恢复【带断言】的验收回归。
覆盖：财务加粗/斜体/底色 + 按钮撤销恢复 + Ctrl+Z/Y 键盘通道 + 权益加粗 + 两表账本互不干扰。
退出码：全过 0，有失败 1。"""
import json
import sys
import traceback

from playwright.sync_api import sync_playwright

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

URL = "http://127.0.0.1:5050/lite?v=undo36"
FR, FC = 6, 6
ER, EC = 3, 3
FAILS = []


def say(*a):
    print(*a, flush=True)


def ok(name, cond, extra=""):
    say(("PASS  " if cond else "FAIL  ") + name + (("  |  " + str(extra)) if extra else ""))
    if not cond:
        FAILS.append(name)


ST = """(arg) => {
  var sel = arg.sel, R = arg.r, C = arg.c;
  var out = { hist: 0, redo: 0, histEq: 0, histFin: 0, redoEq: 0, redoFin: 0,
              last: window.__finUndoLastRec || null, style: null };
  function cnt(arr){
    var a = 0, b = 0;
    for (var i=0;i<arr.length;i++){ if (String(arr[i].unitId)==='equity-report') a++; else b++; }
    return [a,b];
  }
  try {
    var h = cnt(window.finUndoHist||[]), r = cnt(window.finUndoRedo||[]);
    out.hist = (window.finUndoHist||[]).length; out.redo = (window.finUndoRedo||[]).length;
    out.histEq = h[0]; out.histFin = h[1]; out.redoEq = r[0]; out.redoFin = r[1];
  } catch(e){}
  try {
    var sn, sid;
    if (sel === 'eq') {
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
    out.style = s ? s : null;
  } catch(e){ out.style = 'ERR:' + e; }
  return out;
}"""

FIND = """(arg) => {
  var root = document.querySelector(arg.root);
  if (!root) return null;
  var els = root.querySelectorAll('[class]');
  for (var i=0;i<els.length;i++){
    var cn = els[i].getAttribute('class') || '';
    if (cn.toLowerCase().indexOf(arg.needle) < 0) continue;
    var b = els[i].closest('button') || els[i];
    var r = b.getBoundingClientRect();
    if (r.width < 2 || r.height < 2) continue;
    return { x: Math.round(r.x+r.width/2), y: Math.round(r.y+r.height/2) };
  }
  return null;
}"""


def st(pg, sel, r, c):
    return pg.evaluate(ST, {"sel": sel, "r": r, "c": c})


def blob(s):
    try:
        return json.dumps(s, ensure_ascii=False)[:400]
    except Exception:
        return str(s)[:400]


def norm(s):
    """样式归一化：键序无关；值为 null 的键视同「没有这个样式」。

    这一版 Univer 清样式后会在样式库里留下 {bl: null} 残键（等价于不加粗），
    断言必须按语义比较，否则「撤销回到基线」永远不相等。
    """
    if not isinstance(s, dict):
        return None
    clean = {k: v for k, v in s.items() if v is not None}
    if not clean:
        return None
    try:
        return json.dumps(clean, sort_keys=True, ensure_ascii=False)
    except Exception:
        return str(clean)


def same(a, b):
    return norm(a) == norm(b)


def has_key(s, k):
    return isinstance(s, dict) and bool(s.get(k))


def click_icon(pg, root, needle):
    bx = pg.evaluate(FIND, {"root": root, "needle": needle})
    if not bx:
        say("  [miss] %s / %s" % (root, needle))
        return False
    pg.mouse.click(bx["x"], bx["y"])
    return True


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

        def focus_fin():
            pg.evaluate("""() => { var c=document.querySelector('#univer_container canvas'); if(c){ c.setAttribute('tabindex','0'); c.focus(); } }""")

        def act_fin():
            pg.evaluate("([r,c]) => { window.finUniverAPI.getActiveWorkbook().getActiveSheet().getRange(r,c).activate(); }", [FR, FC])

        focus_fin(); act_fin(); pg.wait_for_timeout(700)
        s0 = st(pg, "fin", FR, FC)
        baseFin = s0["style"]          # 基线样式（可能是 null，也可能带底纹/边框等默认样式）
        ok("财务 初始无样式", s0["style"] is None, blob(s0["style"]))

        # ---- 1. 加粗 → 撤销 → 恢复 → 撤销 ----
        click_icon(pg, "#univer_container", "bold-single"); pg.wait_for_timeout(1300)
        s = st(pg, "fin", FR, FC)
        ok("财务 加粗后 bl=1", isinstance(s["style"], dict) and (s["style"].get("bl") == 1), blob(s["style"]))
        ok("财务 加粗 记一步", s["histFin"] == s0["histFin"] + 1, "%s -> %s" % (s0["histFin"], s["histFin"]))

        click_icon(pg, "#univer_container", "undo-single"); pg.wait_for_timeout(1500)
        s = st(pg, "fin", FR, FC)
        ok("财务 撤销后回到基线", same(s["style"], baseFin) and not has_key(s["style"], "bl"), blob(s["style"]))
        ok("财务 撤销后 redo+1", s["redoFin"] == s0["redoFin"] + 1, s["redoFin"])

        click_icon(pg, "#univer_container", "redo-single"); pg.wait_for_timeout(1500)
        s = st(pg, "fin", FR, FC)
        ok("财务 恢复后 bl=1", isinstance(s["style"], dict) and (s["style"].get("bl") == 1), blob(s["style"]))

        click_icon(pg, "#univer_container", "undo-single"); pg.wait_for_timeout(1400)
        s = st(pg, "fin", FR, FC)
        ok("财务 再撤销后回到基线", same(s["style"], baseFin) and not has_key(s["style"], "bl"), blob(s["style"]))
        base = s

        # ---- 2. 斜体：按钮 + Ctrl+Z / Ctrl+Y 键盘通道 ----
        click_icon(pg, "#univer_container", "italic-single"); pg.wait_for_timeout(1300)
        s = st(pg, "fin", FR, FC)
        ok("财务 斜体后 it=1", isinstance(s["style"], dict) and (s["style"].get("it") == 1), blob(s["style"]))
        ok("财务 斜体 记一步", s["histFin"] == base["histFin"] + 1,
           "%s -> %s (last=%s)" % (base["histFin"], s["histFin"], blob(s["last"])))

        focus_fin(); act_fin(); pg.wait_for_timeout(400)
        pg.keyboard.press("Control+z"); pg.wait_for_timeout(1400)
        s = st(pg, "fin", FR, FC)
        ok("财务 Ctrl+Z 撤掉斜体", same(s["style"], baseFin) and not has_key(s["style"], "it"), blob(s["style"]))

        pg.keyboard.press("Control+y"); pg.wait_for_timeout(1400)
        s = st(pg, "fin", FR, FC)
        ok("财务 Ctrl+Y 恢复斜体", isinstance(s["style"], dict) and (s["style"].get("it") == 1), blob(s["style"]))

        click_icon(pg, "#univer_container", "undo-single"); pg.wait_for_timeout(1400)
        s = st(pg, "fin", FR, FC)
        ok("财务 斜体撤销回基线", same(s["style"], baseFin) and not has_key(s["style"], "it"), blob(s["style"]))
        base = s

        # ---- 3. 底色（走 __finApplyCellStyle 落色入口）→ 撤销 → 恢复 ----
        r = pg.evaluate("() => window.__finApplyCellStyle('bg', '#ffcc00')")
        pg.wait_for_timeout(1400)
        s = st(pg, "fin", FR, FC)
        hasbg = isinstance(s["style"], dict) and bool((s["style"].get("bg") or {}).get("rgb"))
        ok("财务 底色写入", bool(r) and hasbg, blob(s["style"]))
        ok("财务 底色 记一步", s["histFin"] == base["histFin"] + 1, s["histFin"])

        click_icon(pg, "#univer_container", "undo-single"); pg.wait_for_timeout(1500)
        s = st(pg, "fin", FR, FC)
        ok("财务 底色撤销后无 bg", not (isinstance(s["style"], dict) and bool((s["style"].get("bg") or {}).get("rgb"))), blob(s["style"]))

        click_icon(pg, "#univer_container", "redo-single"); pg.wait_for_timeout(1500)
        s = st(pg, "fin", FR, FC)
        ok("财务 底色恢复后有 bg", isinstance(s["style"], dict) and bool((s["style"].get("bg") or {}).get("rgb")), blob(s["style"]))

        # ---- 4. 权益表：加粗 → 撤销 → 恢复；账本与财务互不干扰 ----
        click_icon(pg, "#univer_container", "undo-single"); pg.wait_for_timeout(1200)
        finBefore = st(pg, "fin", FR, FC)
        pg.evaluate("() => switchView('equity')")
        pg.wait_for_function("() => !!document.querySelector('#equity_container canvas')", timeout=60000)
        pg.wait_for_timeout(4000)
        pg.evaluate("""() => { var c=document.querySelector('#equity_container canvas'); if(c){ c.setAttribute('tabindex','0'); c.focus(); } }""")
        pg.evaluate("([r,c]) => { window.__eqAPI().getActiveWorkbook().getActiveSheet().getRange(r,c).activate(); }", [ER, EC])
        pg.wait_for_timeout(800)
        e0 = st(pg, "eq", ER, EC)
        baseEq = e0["style"]           # 权益表每格自带默认样式(fs/ff/bd)，基线不为 null 属正常
        ok("权益 初始无显式样式", not has_key(baseEq, "bl") and not has_key(baseEq, "it") and not has_key(baseEq, "bg"), blob(baseEq))
        ok("权益 初始 财务账本保留", e0["histFin"] == finBefore["histFin"], "%s vs %s" % (e0["histFin"], finBefore["histFin"]))

        click_icon(pg, "#equity_container", "bold-single"); pg.wait_for_timeout(1400)
        e = st(pg, "eq", ER, EC)
        ok("权益 加粗后 bl=1", isinstance(e["style"], dict) and (e["style"].get("bl") == 1), blob(e["style"]))
        ok("权益 加粗 记一步(仅权益)", e["histEq"] == e0["histEq"] + 1, "%s -> %s" % (e0["histEq"], e["histEq"]))
        ok("权益 加粗不动财务账本", e["histFin"] == e0["histFin"], "%s vs %s" % (e["histFin"], e0["histFin"]))

        click_icon(pg, "#equity_container", "undo-single"); pg.wait_for_timeout(1600)
        e = st(pg, "eq", ER, EC)
        ok("权益 撤销后回到基线", same(e["style"], baseEq) and not has_key(e["style"], "bl"), blob(e["style"]))
        ok("权益 撤销只退权益一步", e["histEq"] == e0["histEq"], e["histEq"])
        ok("权益 撤销未误吃财务步骤", e["histFin"] == e0["histFin"], e["histFin"])

        click_icon(pg, "#equity_container", "redo-single"); pg.wait_for_timeout(1600)
        e = st(pg, "eq", ER, EC)
        ok("权益 恢复后 bl=1", isinstance(e["style"], dict) and (e["style"].get("bl") == 1), blob(e["style"]))

        click_icon(pg, "#equity_container", "undo-single"); pg.wait_for_timeout(1400)
        e = st(pg, "eq", ER, EC)
        ok("权益 收尾回到基线", same(e["style"], baseEq) and not has_key(e["style"], "bl"), blob(e["style"]))

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
