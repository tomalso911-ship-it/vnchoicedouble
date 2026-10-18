# -*- coding: utf-8 -*-
"""探针 43：Ctrl+C / Ctrl+X / Ctrl+V 三键回归（含「复制空白」修复）。

断言：
  1) 财务空白格 Ctrl+C：必须被接管（__clipLast.ok=true, len=0），不能"静默无反应"；
  2) 财务全选 Ctrl+C：正常产出大量文本；
  3) 权益 Ctrl+C → Ctrl+V（带格式镜像）→ Ctrl+X 清空源格；
  4) 自检状态：__CLIP_LOCK_FAILED=false 且打印过 OK。
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

URL = "http://127.0.0.1:5050/lite?v=clip43"
SRC = (20, 2)
DST = (20, 5)
FAILS = []


def say(*a):
    print(*a, flush=True)


def ok(name, cond, extra=""):
    say(("PASS  " if cond else "FAIL  ") + name + (("  |  " + str(extra)) if extra else ""))
    if not cond:
        FAILS.append(name)


def blob(s):
    try:
        return json.dumps(s, ensure_ascii=False)[:200]
    except Exception:
        return str(s)[:200]


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
        pg.evaluate("() => switchView('finance')")
        pg.wait_for_function("() => !!(window.finReady && document.querySelector('#univer_container canvas'))", timeout=60000)
        pg.wait_for_timeout(4000)

        say("自检:", pg.evaluate("() => ({ failed: !!window.__CLIP_LOCK_FAILED, okLogged: !!window.__clipLockOkLogged })"))

        # ---- 1. 财务：空白格 Ctrl+C ----
        blank = pg.evaluate("""() => {
          var sh = window.finUniverAPI.getActiveWorkbook().getActiveSheet();
          for (var r = 30; r < 60; r++){
            for (var c = 24; c < 30; c++){
              var v = null;
              try { v = sh.getRange(r, c, 1, 1).getValues()[0][0]; } catch(e){ continue; }
              if (v === null || v === '' || v === undefined) return { r: r, c: c };
            }
          }
          return null;
        }""")
        say("空白格:", blank)
        ok("找到空白格用于测试", bool(blank), blob(blank))
        if blank:
            pg.evaluate("""(arg) => {
              window.finUniverAPI.getActiveWorkbook().getActiveSheet().getRange(arg.r, arg.c).activate();
              var c = document.querySelector('#univer_container canvas');
              if (c) { c.setAttribute('tabindex','0'); c.focus(); }
            }""", blank)
            pg.wait_for_timeout(700)
            pg.keyboard.press("Control+c")
            pg.wait_for_timeout(900)
            last = pg.evaluate("() => window.__clipLast || null")
            mir = pg.evaluate("() => window.__finClipMirror ? { text: window.__finClipMirror.text, rows: window.__finClipMirror.mat.length } : null")
            say("空复制 __clipLast:", blob(last), "镜像:", blob(mir))
            ok("财务 空复制被接管（不是静默无反应）",
               isinstance(last, dict) and last.get("kind") == "copy" and last.get("len") == 0 and last.get("ok") is True,
               blob(last))
            try:
                clip = pg.evaluate("() => navigator.clipboard.readText()")
            except Exception as e:
                clip = "READ-FAIL:" + str(e)
            ok("财务 空复制把剪贴板清空（不再残留旧文本）", clip == "", repr(clip)[:80])

        # ---- 2. 财务：全选 Ctrl+C ----
        pg.keyboard.press("Control+a")
        pg.wait_for_timeout(400)
        pg.keyboard.press("Control+c")
        pg.wait_for_timeout(1500)
        last2 = pg.evaluate("() => window.__clipLast || null")
        say("全选复制:", blob(last2))
        ok("财务 全选复制有内容", isinstance(last2, dict) and (last2.get("len") or 0) > 100, blob(last2))

        # ---- 3. 权益：C → V → X ----
        pg.evaluate("() => switchView('equity')")
        pg.wait_for_function("() => !!document.querySelector('#equity_container canvas')", timeout=60000)
        pg.wait_for_timeout(4500)
        pg.evaluate("""(arg) => {
          var api = window.__eqAPI();
          var sh = api.getActiveWorkbook().getActiveSheet();
          var sid = sh.getSheetId();
          sh.getRange(arg.r, arg.c, 1, 1).setValue('CLIPTEST');
          var pr = api.executeCommand('sheet.command.set-range-values', {
            unitId: 'equity-report', subUnitId: sid,
            range: { startRow: arg.r, startColumn: arg.c, endRow: arg.r, endColumn: arg.c },
            value: [[{ s: { bl: 1, cl: { rgb: '#dc2626' } } }]]
          });
          if (pr && pr.then) pr.catch(function(){});
          sh.getRange(arg.r, arg.c, 1, 1).activate();
          var c = document.querySelector('#equity_container canvas');
          if (c) { c.setAttribute('tabindex','0'); c.focus(); }
        }""", {"r": SRC[0], "c": SRC[1]})
        pg.wait_for_timeout(1200)
        pg.keyboard.press("Control+c")
        pg.wait_for_timeout(900)
        l3 = pg.evaluate("() => window.__clipLast || null")
        m3 = pg.evaluate("() => window.__eqClipMirror ? window.__eqClipMirror.text : null")
        ok("权益 Ctrl+C 成功", isinstance(l3, dict) and l3.get("kind") == "copy" and l3.get("ok") is True and l3.get("len") == 8, blob(l3))
        ok("权益 复制内容 = 屏幕文本", m3 == "CLIPTEST", repr(m3))

        # 粘贴到目标格
        pg.evaluate("""(arg) => {
          var sh = window.__eqAPI().getActiveWorkbook().getActiveSheet();
          sh.getRange(arg.r, arg.c, 1, 1).activate();
          var c = document.querySelector('#equity_container canvas');
          if (c) { c.focus(); }
        }""", {"r": DST[0], "c": DST[1]})
        pg.wait_for_timeout(500)
        pg.keyboard.press("Control+v")
        pg.wait_for_timeout(1800)
        l4 = pg.evaluate("() => window.__clipLast || null")
        dst = pg.evaluate("""(arg) => {
          var sn = window.__eqAPI().getActiveWorkbook().getSnapshot();
          var sid = window.__eqAPI().getActiveWorkbook().getActiveSheet().getSheetId();
          var cell = sn.sheets[sid].cellData && sn.sheets[sid].cellData[arg.r] ? sn.sheets[sid].cellData[arg.r][arg.c] : null;
          return cell ? { v: cell.v } : null;
        }""", {"r": DST[0], "c": DST[1]})
        ok("权益 Ctrl+V 写入成功", bool(l4) and l4.get("kind") == "paste" and l4.get("ok") is True, blob(l4))
        ok("权益 粘贴值正确", bool(dst) and dst.get("v") == "CLIPTEST", blob(dst))

        # 剪切源格
        pg.evaluate("""(arg) => {
          var sh = window.__eqAPI().getActiveWorkbook().getActiveSheet();
          sh.getRange(arg.r, arg.c, 1, 1).activate();
          var c = document.querySelector('#equity_container canvas');
          if (c) { c.focus(); }
        }""", {"r": SRC[0], "c": SRC[1]})
        pg.wait_for_timeout(500)
        pg.keyboard.press("Control+x")
        pg.wait_for_timeout(1400)
        l5 = pg.evaluate("() => window.__clipLast || null")
        srcCell = pg.evaluate("""(arg) => {
          var sn = window.__eqAPI().getActiveWorkbook().getSnapshot();
          var sid = window.__eqAPI().getActiveWorkbook().getActiveSheet().getSheetId();
          var cell = sn.sheets[sid].cellData && sn.sheets[sid].cellData[arg.r] ? sn.sheets[sid].cellData[arg.r][arg.c] : null;
          return cell ? { v: cell.v } : null;
        }""", {"r": SRC[0], "c": SRC[1]})
        ok("权益 Ctrl+X 成功", bool(l5) and l5.get("kind") == "cut", blob(l5))
        ok("权益 剪切清空源格", not srcCell or srcCell.get("v") in (None, ""), blob(srcCell))

        ok("自检未报错（不再误报红字）", pg.evaluate("() => !window.__CLIP_LOCK_FAILED"))
        ok("无页面异常", not errs, "; ".join(errs[:3]))

        # ---- 清理测试格子 ----
        pg.evaluate("""(cells) => {
          var api = window.__eqAPI();
          var sh = api.getActiveWorkbook().getActiveSheet();
          for (var i = 0; i < cells.length; i++){
            sh.getRange(cells[i][0], cells[i][1], 1, 1).activate();
            var pr = api.executeCommand('sheet.command.clear-selection-content', {});
            if (pr && pr.then) pr.catch(function(){});
          }
        }""", [[SRC[0], SRC[1]], [DST[0], DST[1]]])
        pg.wait_for_timeout(2500)
        left = pg.evaluate("""(cells) => {
          var sn = window.__eqAPI().getActiveWorkbook().getSnapshot();
          var sid = window.__eqAPI().getActiveWorkbook().getActiveSheet().getSheetId();
          var out = [];
          for (var i = 0; i < cells.length; i++){
            var cell = sn.sheets[sid].cellData && sn.sheets[sid].cellData[cells[i][0]] ? sn.sheets[sid].cellData[cells[i][0]][cells[i][1]] : null;
            out.push(cell ? { v: cell.v } : null);
          }
          return out;
        }""", [[SRC[0], SRC[1]], [DST[0], DST[1]]])
        say("清理后:", blob(left))

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
