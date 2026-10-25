# -*- coding: utf-8 -*-
"""验证「越南报表纯净 / 合并报表含中国记录」两条链路都正确。

分两层：
  ① 接口层：直接 POST 登录后 fetch 三份快照，统计 JSON 里 "CN:" 出现次数
     （vn-report 必须 0；merge-report 必须 >0；cn-report 也应为 0）。
  ② UI 层：切「越南财务报表」/「合并财务总报表」标签，读 FIN_KIND / 工作表数 / 工作区可见性，
     并统计真实控制台 error。
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_verify_merge_split_out.txt")
L = []


def log(s):
    L.append(str(s))
    io.open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(s)


log("start")

from playwright.sync_api import sync_playwright  # noqa: E402

ERRS = []
PAGES = []

FETCH_SNAP = r"""async () => {
  var out = {};
  var kinds = ['vn-report', 'merge-report', 'cn-report'];
  for (var i = 0; i < kinds.length; i++) {
    var k = kinds[i];
    try {
      var r = await fetch('/api/finance/' + k + '/snapshot');
      var t = await r.text();
      out[k] = {
        status: r.status,
        bytes: t.length,
        cnMarks: (t.match(/CN:/g) || []).length,
        sheets: (t.match(/sheet_\d+/g) || []).length
      };
    } catch (e) { out[k] = { err: String(e).slice(0, 120) }; }
  }
  return out;
}"""

UI_PROBE = r"""() => {
  var out = {};
  var pm = document.getElementById('fin_panel_merge');
  out.panelMergeActive = pm ? pm.classList.contains('active') : null;
  out.hasUnderConstruction = !!(pm && /建设中|敬请期待|under construction|đang xây dựng/i.test(pm.innerText || ''));
  var ws = document.getElementById('fin_workspace');
  out.wsRects = ws ? ws.getClientRects().length : null;
  var uc = document.getElementById('univer_container');
  out.ucW = uc ? uc.clientWidth : null;
  out.ucH = uc ? uc.clientHeight : null;
  out.finKind = (typeof FIN_KIND !== 'undefined') ? FIN_KIND : null;
  out.activeTab = (typeof FIN_ACTIVE_TAB !== 'undefined') ? FIN_ACTIVE_TAB : null;
  out.unitId = (typeof finLastView !== 'undefined' && finLastView) ? finLastView.id : null;
  try {
    var wb = finUniverAPI.getActiveWorkbook();
    out.sheetCount = wb.getSheets().length;
    out.sheetNames = wb.getSheets().map(function (s) {
      return (typeof s.getSheetName === 'function') ? s.getSheetName()
           : (typeof s.getName === 'function') ? s.getName() : String(s);
    }).join(' | ');
  } catch (e) { out.sheetErr = String(e).slice(0, 140); }
  return out;
}"""


def show(tag, pg):
    info = pg.evaluate(UI_PROBE)
    log("── %s" % tag)
    for k in ("finKind", "activeTab", "unitId", "panelMergeActive", "hasUnderConstruction",
              "wsRects", "ucW", "ucH", "sheetCount", "sheetErr", "sheetNames"):
        if k in info:
            log("   %-22s = %s" % (k, info[k]))
    return info


with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True, args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 1500, "height": 900})
    pg.on("console", lambda m: ERRS.append(m.text[:140]) if m.type == "error" else None)
    pg.on("pageerror", lambda e: PAGES.append(str(e)[:140]))

    pg.goto("http://127.0.0.1:5050/lite", wait_until="domcontentloaded")
    pg.wait_for_timeout(1200)
    pg.fill("#loginUser", "tom")
    pg.fill("#loginPwd", "66668888")
    pg.click("#loginBtn")
    pg.wait_for_selector("#topbar:not(.hidden)", timeout=25000)

    log("── ① 接口层：三份快照里的 CN: 标记数")
    snaps = pg.evaluate(FETCH_SNAP)
    for k in ("vn-report", "merge-report", "cn-report"):
        log("   %-14s %s" % (k, snaps.get(k)))

    pg.evaluate("() => { try { switchView('finance'); } catch(e){} }")
    pg.wait_for_timeout(15000)
    show("② 越南财务报表（应为 0 行中国记录）", pg)

    pg.evaluate("() => { try { fin_switchTab('merge'); } catch(e){} }")
    pg.wait_for_timeout(9000)
    show("③ 合并财务总报表（应含中国记录）", pg)

    pg.evaluate("() => { try { fin_switchTab('vn'); } catch(e){} }")
    pg.wait_for_timeout(9000)
    show("④ 切回越南财务报表", pg)

    log("console error 合计 = %d" % len(ERRS))
    for x in ERRS[:6]:
        log("   ERR " + x)
    log("pageerror = %s" % PAGES[:4])
    b.close()
log("done")
