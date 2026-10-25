# -*- coding: utf-8 -*-
"""实测「中国成本独立显示」：
   ① 点按钮后必须【强行进入「实际支出」表】；
   ② 中国记录（蓝色）全部集中到数据区最下方；
   ③ 中间有分隔行（标题「中国成本记录」）。
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_verify_cn_group_out.txt")
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
  var btn = document.getElementById('fin_merge_group_btn');
  out.btnVisible = btn ? (btn.getClientRects().length > 0) : null;
  out.btnText = btn ? (btn.textContent || '').trim() : null;
  var re = document.getElementById('fin_reimport_btn');
  out.reimportVisible = re ? (re.getClientRects().length > 0) : null;
  out.groupFlag = (typeof FIN_MERGE_CN_GROUP !== 'undefined') ? FIN_MERGE_CN_GROUP : null;
  out.finKind = (typeof FIN_KIND !== 'undefined') ? FIN_KIND : null;
  out.sepRow = (typeof window.__FIN_MERGE_SEP_ROW === 'number') ? window.__FIN_MERGE_SEP_ROW : null;
  out.cnBase = (typeof window.__FIN_MERGE_CN_ROWBASE === 'number') ? window.__FIN_MERGE_CN_ROWBASE : null;
  out.cnRows = (typeof window.__FIN_MERGE_CN_ROWS === 'number') ? window.__FIN_MERGE_CN_ROWS : null;
  try {
    var idx = fin_mergeCnSheetIndex();
    out.chiIdx = idx;
    if (idx >= 0) {
      var vsh = finLastView.sheets[finLastView.sheetOrder[idx]];
      var keys = Object.keys(vsh.cellData).map(Number).sort(function (a, b) { return a - b; });
      out.totalRows = keys.length;
      function rowB(r) {
        var row = vsh.cellData[String(r)] || {};
        return row['1'] ? String(row['1'].v) : '';
      }
      function rowA(r) {
        var row = vsh.cellData[String(r)] || {};
        return row['0'] ? String(row['0'].v) : '';
      }
      if (out.sepRow !== null) {
        out.sepText = rowA(out.sepRow);
        out.rowBeforeSep = rowB(out.sepRow - 1);
        out.rowAfterSep = rowB(out.sepRow + 1);
      }
      out.tail10 = keys.slice(-10).map(function (r) { return (r + 1) + ':' + rowB(r); });
      out.head3 = keys.slice(0, 3).map(function (r) { return (r + 1) + ':' + rowB(r); });
    }
  } catch (e) { out.err = String(e).slice(0, 160); }
  try {
    var wb = finUniverAPI.getActiveWorkbook();
    var act = wb.getActiveSheet();
    out.activeSheet = (typeof act.getSheetName === 'function') ? act.getSheetName() : String(act);
  } catch (e) { out.activeSheetErr = String(e).slice(0, 100); }
  return out;
}"""


def show(tag, pg):
    info = pg.evaluate(PROBE)
    log("── %s" % tag)
    for k in ("finKind", "groupFlag", "btnVisible", "btnText", "reimportVisible",
              "chiIdx", "totalRows", "activeSheet", "sepRow", "sepText",
              "rowBeforeSep", "rowAfterSep", "cnBase", "cnRows", "err", "activeSheetErr"):
        if k in info:
            log("   %-16s = %s" % (k, info[k]))
    log("   head3          = %s" % (info.get("head3"),))
    log("   tail10         = %s" % (info.get("tail10"),))
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
    pg.wait_for_timeout(15000)
    pg.evaluate("() => { try { fin_switchTab('merge'); } catch(e){} }")
    pg.wait_for_timeout(10000)
    show("① 合并报表 · 点按钮之前", pg)

    pg.click("#fin_merge_group_btn")
    pg.wait_for_timeout(14000)
    show("② 点「中国成本独立显示」之后", pg)

    pg.click("#fin_merge_group_btn")
    pg.wait_for_timeout(14000)
    show("③ 再点一次（恢复原顺序）", pg)

    log("console error 合计 = %d" % len(ERRS))
    for x in ERRS[:6]:
        log("   ERR " + x)
    log("pageerror = %s" % PAGES[:4])
    b.close()
log("done")
