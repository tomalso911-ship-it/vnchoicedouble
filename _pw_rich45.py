# -*- coding: utf-8 -*-
"""探针 45：真实键盘「多行」复制粘贴，验证格式 100% 过去（CLIP-TEXT-NORM-20261018）。

单格测不出 \r\n 问题，必须多行。权益表空表，测后清理。
"""
import json
import sys
import traceback

from playwright.sync_api import sync_playwright

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

URL = "http://127.0.0.1:5050/lite?v=rich45"
SR = SC = 20      # C21
DR = DC = 25      # C26
NR, NC = 2, 2
FAILS = []

STY = [
    {"bl": 1, "cl": {"rgb": "#dc2626"}, "bg": {"rgb": "#fef3c7"}, "fs": 14},
    {"it": 1, "cl": {"rgb": "#2563eb"}, "bg": {"rgb": "#dcfce7"}, "fs": 11, "ht": 2},
    {"ul": {"s": 1}, "cl": {"rgb": "#16a34a"}, "ht": 1, "vt": 1, "n": {"pattern": "#,##0.00"}},
    {"bl": 1, "it": 1, "bg": {"rgb": "#dbeafe"}, "fs": 18, "ht": 3},
]
VALS = [[11.5, "AAA"], ["BBB", 2222.25]]


def say(*a):
    print(*a, flush=True)


def ok(name, cond, extra=""):
    say(("PASS  " if cond else "FAIL  ") + name + (("  |  " + str(extra)) if extra else ""))
    if not cond:
        FAILS.append(name)


def blob(s):
    try:
        return json.dumps(s, ensure_ascii=False, sort_keys=True)[:400]
    except Exception:
        return str(s)[:400]


def norm_style(s):
    if not isinstance(s, dict):
        return None
    return {k: v for k, v in s.items() if v is not None}


READ = """(arg) => {
  var sn = window.__eqAPI().getActiveWorkbook().getSnapshot();
  var sid = window.__eqAPI().getActiveWorkbook().getActiveSheet().getSheetId();
  var sh = sn.sheets[sid];
  var out = [];
  for (var r = arg.r; r < arg.r + arg.nr; r++){
    var row = [];
    for (var c = arg.c; c < arg.c + arg.nc; c++){
      var cell = sh.cellData && sh.cellData[r] ? sh.cellData[r][c] : null;
      var s = cell ? cell.s : null;
      if (typeof s === 'string') s = (sn.styles || {})[s];
      row.push({ v: cell ? (cell.v === undefined ? null : cell.v) : null, s: s || null });
    }
    out.push(row);
  }
  return out;
}"""


def cmp(rows):
    return [[{"v": c["v"], "s": norm_style(c["s"])} for c in r] for r in rows]


def main():
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True, args=["--no-sandbox"])
        ctx = b.new_context(viewport={"width": 1600, "height": 950})
        try:
            ctx.grant_permissions(["clipboard-read", "clipboard-write"], origin="http://127.0.0.1:5050")
        except Exception:
            pass
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
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
        pg.wait_for_timeout(5000)

        # 准备 2x2 源区域（值 + 各异样式）
        pg.evaluate("""(arg) => {
          var api = window.__eqAPI();
          var sh = api.getActiveWorkbook().getActiveSheet();
          var sid = sh.getSheetId();
          sh.getRange(arg.r, arg.c, arg.nr, arg.nc).setValues(arg.vals);
          for (var r = 0; r < arg.nr; r++){
            for (var c = 0; c < arg.nc; c++){
              var pr = api.executeCommand('sheet.command.set-range-values', {
                unitId: 'equity-report', subUnitId: sid,
                range: { startRow: arg.r + r, startColumn: arg.c + c, endRow: arg.r + r, endColumn: arg.c + c },
                value: [[{ s: arg.sty[r * arg.nc + c] }]]
              });
              if (pr && pr.then) pr.catch(function(){});
            }
          }
        }""", {"r": SR, "c": SC, "nr": NR, "nc": NC, "vals": VALS, "sty": STY})
        pg.wait_for_timeout(1500)

        src = pg.evaluate(READ, {"r": SR, "c": SC, "nr": NR, "nc": NC})
        say("源区域:", blob(cmp(src)))

        # 真实 Ctrl+C
        pg.evaluate("""(arg) => {
          var sh = window.__eqAPI().getActiveWorkbook().getActiveSheet();
          sh.getRange(arg.r, arg.c, arg.nr, arg.nc).activate();
          var c = document.querySelector('#equity_container canvas');
          if (c) { c.setAttribute('tabindex','0'); c.focus(); }
        }""", {"r": SR, "c": SC, "nr": NR, "nc": NC})
        pg.wait_for_timeout(700)
        pg.keyboard.press("Control+c")
        pg.wait_for_timeout(1000)
        mir = pg.evaluate("() => window.__eqClipMirror ? { text: window.__eqClipMirror.text, rows: window.__eqClipMirror.mat.length } : null")
        say("镜像:", repr(mir))
        try:
            clip = pg.evaluate("() => navigator.clipboard.readText()")
        except Exception as e:
            clip = "READ-FAIL"
        say("系统剪贴板:", repr(clip))
        if isinstance(clip, str) and isinstance(mir, dict):
            ok("剪贴板文本与镜像一致（含换行归一化）",
               clip.replace("\r\n", "\n") == mir["text"].replace("\r\n", "\n"), "raw_has_CR=%s" % ("\r" in clip))

        # 真实 Ctrl+V 到目标区
        pg.evaluate("""(arg) => {
          var sh = window.__eqAPI().getActiveWorkbook().getActiveSheet();
          sh.getRange(arg.r, arg.c, 1, 1).activate();
          var c = document.querySelector('#equity_container canvas');
          if (c) { c.focus(); }
        }""", {"r": DR, "c": DC})
        pg.wait_for_timeout(600)
        pg.keyboard.press("Control+v")
        pg.wait_for_timeout(2200)

        last = pg.evaluate("() => window.__clipLast || null")
        say("粘贴 __clipLast:", blob(last))
        ok("真实 Ctrl+V 走 rich 通道（不是纯文本）", isinstance(last, dict) and bool(last.get("rich")), blob(last))

        dst = pg.evaluate(READ, {"r": DR, "c": DC, "nr": NR, "nc": NC})
        say("目标区域:", blob(cmp(dst)))
        ok("2x2 值全部一致", [c["v"] for r in dst for c in r] == [c["v"] for r in src for c in r],
           str([c["v"] for r in dst for c in r]))
        ok("2x2 格式全部一致（逐格）",
           norm_style(dst[0][0]["s"]) == norm_style(src[0][0]["s"]) and
           norm_style(dst[0][1]["s"]) == norm_style(src[0][1]["s"]) and
           norm_style(dst[1][0]["s"]) == norm_style(src[1][0]["s"]) and
           norm_style(dst[1][1]["s"]) == norm_style(src[1][1]["s"]),
           blob([norm_style(dst[0][0]["s"]), norm_style(dst[1][1]["s"])]))
        s00 = norm_style(dst[0][0]["s"]) or {}
        ok("加粗/字色/底色/字号 都在", s00.get("bl") == 1 and (s00.get("cl") or {}).get("rgb") == "#dc2626"
           and (s00.get("bg") or {}).get("rgb") == "#fef3c7" and s00.get("fs") == 14, blob(s00))
        s11 = norm_style(dst[1][1]["s"]) or {}
        ok("斜体/底色/字号/对齐 都在", s11.get("it") == 1 and (s11.get("bg") or {}).get("rgb") == "#dbeafe"
           and s11.get("fs") == 18 and s11.get("ht") == 3, blob(s11))
        s10 = norm_style(dst[1][0]["s"]) or {}
        ok("下划线/数字格式 都在", (s10.get("ul") or {}).get("s") == 1
           and (s10.get("n") or {}).get("pattern") == "#,##0.00", blob(s10))

        ok("无页面异常", not errs, "; ".join(errs[:2]))

        # 清理
        pg.evaluate("""(arg) => {
          var api = window.__eqAPI();
          var sh = api.getActiveWorkbook().getActiveSheet();
          var cells = [[arg.sr, arg.sc], [arg.dr, arg.dc]];
          var spans = [arg.nr, arg.nc];
          for (var i = 0; i < 2; i++){
            sh.getRange(cells[i][0], cells[i][1], arg.nr, arg.nc).activate();
            var pr = api.executeCommand('sheet.command.clear-selection-content', {});
            if (pr && pr.then) pr.catch(function(){});
          }
        }""", {"sr": SR, "sc": SC, "dr": DR, "dc": DC, "nr": NR, "nc": NC})
        pg.wait_for_timeout(2500)

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
