# -*- coding: utf-8 -*-
"""探针 38：带格式复制/粘贴（CLIP-RICH-20261018）验收。

要求（用户 2026-10-18）：「复制粘贴的时候，单元格的格式、颜色、字号、对齐方式，
等等一切都要 100% 和被复制的内容一样！」

做法：真实 Ctrl+C 触发复制（产生镜像），再通过引擎 paste 通道粘贴（避开 headless
剪贴板读限制），逐项比较源格与目标格的【值 + 完整样式对象】。
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

URL = "http://127.0.0.1:5050/lite?v=rich38"
SRC_R, SRC_C = 6, 6
DST_R, DST_C = 9, 3
FAILS = []

SRC_STYLE_1 = {"bl": 1, "fs": 14, "ff": "Arial", "cl": {"rgb": "#dc2626"},
               "bg": {"rgb": "#fef3c7"}, "ht": 2, "vt": 2, "n": {"pattern": "#,##0.00"}}
SRC_STYLE_2 = {"it": 1, "ul": {"s": 1}, "fs": 11, "cl": {"rgb": "#2563eb"},
               "bg": {"rgb": "#dcfce7"}, "ht": 1, "vt": 1}
DIRTY_STYLE = {"bg": {"rgb": "#000000"}, "it": 1, "fs": 20, "ht": 3}


def say(*a):
    print(*a, flush=True)


def ok(name, cond, extra=""):
    say(("PASS  " if cond else "FAIL  ") + name + (("  |  " + str(extra)) if extra else ""))
    if not cond:
        FAILS.append(name)


def blob(s):
    try:
        return json.dumps(s, ensure_ascii=False, sort_keys=True)[:300]
    except Exception:
        return str(s)[:300]


def norm_style(s):
    if not isinstance(s, dict):
        return None
    clean = {k: v for k, v in s.items() if v is not None}
    if "n" in clean and isinstance(clean["n"], dict) and not clean["n"].get("pattern"):
        clean.pop("n")
    return clean


# 财务：往源区域写「值 + 花式样式」，给目标区域先塞干扰样式
FIN_PREP = """(arg) => {
  var api = window.finUniverAPI;
  var wb = api.getActiveWorkbook();
  var sh = wb.getActiveSheet();
  var uid = wb.getId();
  var sid = sh.getSheetId();
  var cs = window.__finCmdSvc;
  if (!cs) return { err: 'no-cmdsvc' };
  function setVal(r, c, v){
    sh.getRange(r, c, 1, 1).setValue(v);
  }
  function setStyle(r, c, s){
    cs.executeCommand('sheet.command.set-range-values', {
      unitId: uid, subUnitId: sid,
      range: { startRow: r, startColumn: c, endRow: r, endColumn: c },
      value: [[{ s: s }]]
    });
  }
  setVal(arg.sr, arg.sc, 1234.5);
  setStyle(arg.sr, arg.sc, arg.s1);
  setVal(arg.sr, arg.sc + 1, 'ABC');
  setStyle(arg.sr, arg.sc + 1, arg.s2);
  /* 目标区先放「干扰样式」，用来验证粘贴会把目标原有样式清干净 */
  setVal(arg.dr, arg.dc, 'zzz');
  setStyle(arg.dr, arg.dc, arg.dirty);
  setVal(arg.dr, arg.dc + 1, 'yyy');
  setStyle(arg.dr, arg.dc + 1, arg.dirty);
  return { ok: true, uid: uid, sid: sid };
}"""

FIN_SELECT = """(arg) => {
  var sh = window.finUniverAPI.getActiveWorkbook().getActiveSheet();
  sh.getRange(arg.r, arg.c, arg.nr, arg.nc).activate();
  var c = document.querySelector('#univer_container canvas');
  if (c) { c.setAttribute('tabindex','0'); c.focus(); }
  return true;
}"""

# 读某区域 值 + 样式（样式 id 解析成内联对象）
READ = """(arg) => {
  var isEq = !!arg.eq;
  var sn, sid;
  if (isEq){
    var api = window.__eqAPI();
    sn = api.getActiveWorkbook().getSnapshot();
    sid = api.getActiveWorkbook().getActiveSheet().getSheetId();
  } else {
    sn = window.fin_currentSnapshot();
    var sh = window.finSheetObj();
    sid = sh && sh.getSheetId ? sh.getSheetId() : null;
  }
  var sheet = (sid && sn.sheets[sid]) ? sn.sheets[sid] : sn.sheets[Object.keys(sn.sheets)[0]];
  var out = [];
  for (var r = arg.r; r < arg.r + arg.nr; r++){
    var row = [];
    for (var c = arg.c; c < arg.c + arg.nc; c++){
      var cell = sheet && sheet.cellData && sheet.cellData[r] ? sheet.cellData[r][c] : null;
      var s = cell ? cell.s : null;
      if (typeof s === 'string') s = (sn.styles || {})[s];
      row.push({ v: cell ? (cell.v === undefined ? null : cell.v) : null,
                 f: cell ? (cell.f || null) : null,
                 s: s || null });
    }
    out.push(row);
  }
  return out;
}"""


def rows_to_cmp(rows):
    return [[{"v": c["v"], "f": c["f"], "s": norm_style(c["s"])} for c in r] for r in rows]


def main():
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True, args=["--no-sandbox"])
        ctx = b.new_context(viewport={"width": 1600, "height": 950})
        pg = ctx.new_page()
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
        say("ENGINE:", pg.evaluate("() => window.__clipEngine && window.__clipEngine.ver"))

        # ---- 准备源/目标 ----
        prep = pg.evaluate(FIN_PREP, {"sr": SRC_R, "sc": SRC_C, "dr": DST_R, "dc": DST_C,
                                      "s1": SRC_STYLE_1, "s2": SRC_STYLE_2, "dirty": DIRTY_STYLE})
        say("prep:", blob(prep))
        pg.wait_for_timeout(1200)
        src_before = pg.evaluate(READ, {"eq": False, "r": SRC_R, "c": SRC_C, "nr": 1, "nc": 2})
        say("源格:", blob(rows_to_cmp(src_before)))

        # ---- 真实 Ctrl+C（产生镜像）----
        pg.evaluate(FIN_SELECT, {"r": SRC_R, "c": SRC_C, "nr": 1, "nc": 2})
        pg.wait_for_timeout(500)
        pg.keyboard.press("Control+c")
        pg.wait_for_timeout(900)
        mir = pg.evaluate("() => window.__finClipMirror ? { text: window.__finClipMirror.text, n: window.__finClipMirror.mat.length } : null")
        say("镜像:", blob(mir))
        ok("复制后产生了带格式镜像", bool(mir) and mir.get("n") == 1, blob(mir))
        if not mir:
            say("---- 结果：%d 项失败 (无镜像，后续跳过) ----" % len(FAILS))
            b.close()
            return 1
        clip_text = mir["text"]
        say("剪贴板文本:", repr(clip_text))

        # ---- 粘贴到目标格（走引擎 paste → rich）----
        pg.evaluate(FIN_SELECT, {"r": DST_R, "c": DST_C, "nr": 1, "nc": 1})
        pg.wait_for_timeout(400)
        okp = pg.evaluate("(t) => window.__clipEngine.paste(t, 'fin')", clip_text)
        pg.wait_for_timeout(1800)
        ok("rich 通道粘贴成功", bool(okp), okp)
        last = pg.evaluate("() => window.__finClipLast || null")
        say("__finClipLast:", blob(last))
        ok("引擎走的是 rich 分支", isinstance(last, dict) and bool(last.get("rich")), blob(last))

        dst_after = pg.evaluate(READ, {"eq": False, "r": DST_R, "c": DST_C, "nr": 1, "nc": 2})
        say("目标格(粘贴后):", blob(rows_to_cmp(dst_after)))

        # ---- 逐项断言 ----
        ok("值 100% 一致：1234.5", abs((dst_after[0][0]["v"] or 0) - 1234.5) < 1e-9, dst_after[0][0]["v"])
        ok("值 100% 一致：ABC", dst_after[0][1]["v"] == "ABC", dst_after[0][1]["v"])
        ok("样式 100% 一致：数字格", norm_style(dst_after[0][0]["s"]) == norm_style(src_before[0][0]["s"]),
           blob(norm_style(dst_after[0][0]["s"])))
        ok("样式 100% 一致：文本格", norm_style(dst_after[0][1]["s"]) == norm_style(src_before[0][1]["s"]),
           blob(norm_style(dst_after[0][1]["s"])))
        s1 = norm_style(dst_after[0][0]["s"]) or {}
        ok("加粗 bl=1", s1.get("bl") == 1, s1.get("bl"))
        ok("字号 fs=14", s1.get("fs") == 14, s1.get("fs"))
        ok("字体 ff=Arial", s1.get("ff") == "Arial", s1.get("ff"))
        ok("字色 #dc2626", (s1.get("cl") or {}).get("rgb") == "#dc2626", s1.get("cl"))
        ok("底色 #fef3c7（覆盖目标原黑底）", (s1.get("bg") or {}).get("rgb") == "#fef3c7", s1.get("bg"))
        ok("水平居中 ht=2", s1.get("ht") == 2, s1.get("ht"))
        ok("垂直居中 vt=2", s1.get("vt") == 2, s1.get("vt"))
        ok("数字格式 #,##0.00", (s1.get("n") or {}).get("pattern") == "#,##0.00", s1.get("n"))
        s2 = norm_style(dst_after[0][1]["s"]) or {}
        ok("目标原有斜体未被带过来（源是斜体，干扰也是斜体）", s2.get("it") == 1, s2.get("it"))
        ok("干扰样式 fs=20 已被清掉", s2.get("fs") == 11, s2.get("fs"))

        # ---- 权益表：同一套流程（值 + 样式）----
        pg.evaluate("() => switchView('equity')")
        pg.wait_for_function("() => !!document.querySelector('#equity_container canvas')", timeout=60000)
        pg.wait_for_timeout(4000)
        eq_prep = """(arg) => {
          var api = window.__eqAPI();
          var wb = api.getActiveWorkbook();
          var sh = wb.getActiveSheet();
          var sid = sh.getSheetId();
          sh.getRange(arg.sr, arg.sc, 1, 1).setValue(9876.5);
          var p1 = api.executeCommand('sheet.command.set-range-values', {
            unitId: 'equity-report', subUnitId: sid,
            range: { startRow: arg.sr, startColumn: arg.sc, endRow: arg.sr, endColumn: arg.sc },
            value: [[{ s: arg.s1 }]]
          });
          if (p1 && p1.then) p1.catch(function(){});
          sh.getRange(arg.dr, arg.dc, 1, 1).setValue('zzz');
          var p2 = api.executeCommand('sheet.command.set-range-values', {
            unitId: 'equity-report', subUnitId: sid,
            range: { startRow: arg.dr, startColumn: arg.dc, endRow: arg.dr, endColumn: arg.dc },
            value: [[{ s: arg.dirty }]]
          });
          if (p2 && p2.then) p2.catch(function(){});
          return true;
        }"""
        pg.evaluate(eq_prep, {"sr": SRC_R, "sc": SRC_C, "dr": DST_R, "dc": DST_C,
                              "s1": SRC_STYLE_1, "dirty": DIRTY_STYLE})
        pg.wait_for_timeout(1500)
        eq_src = pg.evaluate(READ, {"eq": True, "r": SRC_R, "c": SRC_C, "nr": 1, "nc": 1})
        say("权益源格:", blob(rows_to_cmp(eq_src)))
        pg.evaluate("""(arg) => {
          var sh = window.__eqAPI().getActiveWorkbook().getActiveSheet();
          sh.getRange(arg.r, arg.c, 1, 1).activate();
          var c = document.querySelector('#equity_container canvas');
          if (c) { c.setAttribute('tabindex','0'); c.focus(); }
        }""", {"r": SRC_R, "c": SRC_C})
        pg.wait_for_timeout(500)
        pg.keyboard.press("Control+c")
        pg.wait_for_timeout(900)
        mir2 = pg.evaluate("() => window.__eqClipMirror ? { text: window.__eqClipMirror.text } : null")
        say("权益镜像:", blob(mir2))
        ok("权益 复制后产生带格式镜像", bool(mir2), blob(mir2))
        if mir2:
            pg.evaluate("""(arg) => {
              var sh = window.__eqAPI().getActiveWorkbook().getActiveSheet();
              sh.getRange(arg.r, arg.c, 1, 1).activate();
              var c = document.querySelector('#equity_container canvas');
              if (c) { c.focus(); }
            }""", {"r": DST_R, "c": DST_C})
            pg.wait_for_timeout(400)
            okp2 = pg.evaluate("(t) => window.__clipEngine.paste(t, 'eq')", mir2["text"])
            pg.wait_for_timeout(1800)
            ok("权益 rich 通道粘贴成功", bool(okp2), okp2)
            eq_dst = pg.evaluate(READ, {"eq": True, "r": DST_R, "c": DST_C, "nr": 1, "nc": 1})
            say("权益目标格:", blob(rows_to_cmp(eq_dst)))
            ok("权益 值一致 9876.5", abs((eq_dst[0][0]["v"] or 0) - 9876.5) < 1e-9, eq_dst[0][0]["v"])
            ok("权益 样式 100% 一致",
               norm_style(eq_dst[0][0]["s"]) == norm_style(eq_src[0][0]["s"]),
               blob(norm_style(eq_dst[0][0]["s"])))

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
