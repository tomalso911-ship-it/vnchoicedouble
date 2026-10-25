# -*- coding: utf-8 -*-
"""真实控制台 + 真实 DOM 验证：「合并财务总报表」标签现在能显示合并后的表格。

覆盖：
  A 首次进入财务页 → 点「合并财务总报表」
  B 点「中国财务报表」→ 再切回「合并财务总报表」（验证 cn→vn 换源重载）
  C 全程 console error / pageerror 计数
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_verify_merge_tab_out.txt")
L = []


def log(s):
    L.append(str(s))
    io.open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(s)


log("start")

from playwright.sync_api import sync_playwright  # noqa: E402

ERRS = []
PAGES = []

PROBE = r"""() => {
  var out = {};
  var pm = document.getElementById('fin_panel_merge');
  out.panelMergeActive = pm ? pm.classList.contains('active') : null;
  out.panelMergeText = pm ? (pm.innerText || '').replace(/\s+/g, ' ').trim().slice(0, 100) : null;
  out.hasUnderConstruction = !!(pm && /建设中|敬请期待|under construction|đang xây dựng/i.test(pm.innerText || ''));
  var ws = document.getElementById('fin_workspace');
  out.wsDisplay = ws ? (ws.style.display || '(empty)') : null;
  out.wsRects = ws ? ws.getClientRects().length : null;
  var uc = document.getElementById('univer_container');
  out.ucW = uc ? uc.clientWidth : null;
  out.ucH = uc ? uc.clientHeight : null;
  out.finKind = (typeof FIN_KIND !== 'undefined') ? FIN_KIND : null;
  out.activeTab = (typeof FIN_ACTIVE_TAB !== 'undefined') ? FIN_ACTIVE_TAB : null;
  try {
    var wb = finUniverAPI.getActiveWorkbook();
    var shs = wb.getSheets();
    out.sheetCount = shs.length;
    out.sheetNames = shs.map(function (s) { return s.getName(); }).join(' | ');
    out.activeSheet = wb.getActiveSheet().getName();
  } catch (e) { out.sheetErr = String(e).slice(0, 140); }
  return out;
}"""


def show(tag, pg):
    info = pg.evaluate(PROBE)
    log("── %s" % tag)
    for k in ("panelMergeActive", "hasUnderConstruction", "wsDisplay", "wsRects",
              "ucW", "ucH", "finKind", "activeTab", "sheetCount", "activeSheet", "sheetErr",
              "panelMergeText", "sheetNames"):
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

    pg.evaluate("() => { try { switchView('finance'); } catch(e){} }")
    pg.wait_for_timeout(15000)          # 等引擎 + 快照
    show("A0 进入财务页（默认标签）", pg)

    pg.evaluate("() => { try { fin_switchTab('merge'); } catch(e){} }")
    pg.wait_for_timeout(3500)
    show("A1 点「合并财务总报表」", pg)

    pg.evaluate("() => { try { fin_switchTab('cn'); } catch(e){} }")
    pg.wait_for_timeout(6000)
    show("B1 点「中国财务报表」", pg)

    pg.evaluate("() => { try { fin_switchTab('merge'); } catch(e){} }")
    pg.wait_for_timeout(8000)
    show("B2 从中国报表切回「合并财务总报表」", pg)

    # 表格里是否真有数据（读合并表活动单元的几格）
    cells = pg.evaluate(r"""() => {
      try {
        var sh = finUniverAPI.getActiveWorkbook().getActiveSheet();
        var rows = [];
        for (var r = 17; r <= 24; r++) {
          rows.push(r + ': ' + [1,2,5].map(function (c) {
            var v = sh.getRange(r - 1, c - 1).getValue();
            return (v === null || v === undefined) ? '' : String(v);
          }).join(' | '));
        }
        return rows;
      } catch (e) { return ['ERR ' + String(e).slice(0, 120)]; }
    }""")
    log("── 抽样数据行（列 A | 凭证 B | Chi E）")
    for x in cells:
        log("   " + x)

    log("console error 合计 = %d" % len(ERRS))
    for x in ERRS[:6]:
        log("   ERR " + x)
    log("pageerror = %s" % PAGES[:4])
    b.close()
log("done")
