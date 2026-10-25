# -*- coding: utf-8 -*-
"""诊断：合并报表的中国记录到底在不在？在哪张工作表？前端为什么看不到？

做法：登录后在页面上下文里 fetch /api/finance/merge-report/snapshot，
直接解析快照 JSON：逐工作表数 "CN:" 标记、列出对应行号/凭证/字色，
再对照 UI 里的活动工作表名与底部标签。
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_diag_merge_rows_out.txt")
L = []


def log(s):
    L.append(str(s))
    io.open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(s)


log("start")

from playwright.sync_api import sync_playwright  # noqa: E402

JS = r"""async () => {
  var out = {};
  var r = await fetch('/api/finance/merge-report/snapshot');
  out.status = r.status;
  if (!r.ok) { return out; }
  var j = await r.json();
  out.sheetOrder = j.sheetOrder;
  out.sheetNames = j.sheetOrder.map(function (sid) { return j.sheets[sid].name; });
  out.cnBySheet = {};
  out.cnRows = [];
  j.sheetOrder.forEach(function (sid) {
    var sh = j.sheets[sid];
    var cd = sh.cellData || {};
    var n = 0;
    Object.keys(cd).forEach(function (rr) {
      Object.keys(cd[rr]).forEach(function (cc) {
        var cell = cd[rr][cc];
        var v = cell ? cell.v : null;
        if (typeof v === 'string' && v.indexOf('CN:') === 0) {
          n++;
          out.cnRows.push({
            sheet: sh.name,
            row: parseInt(rr, 10) + 1,        // 1 基
            col: parseInt(cc, 10) + 1,
            mark: v,
            voucher: (cd[rr] && cd[ '1' ] && cd[rr]['1']) ? cd[rr]['1'].v : null,
            date: (cd[rr] && cd[rr]['0']) ? cd[rr]['0'].v : null,
            amount: (cd[rr] && cd[rr]['4']) ? cd[rr]['4'].v : null,
            styleOfA: (cd[rr] && cd[rr]['0']) ? cd[rr]['0'].s : null
          });
        }
      });
    });
    if (n) out.cnBySheet[sh.name] = n;
  });
  // 顺带看看「Chi thực tế」表里有没有 UNC00009 这条
  var target = null;
  j.sheetOrder.forEach(function (sid) {
    if (j.sheets[sid].name === 'Chi th\u1ef1c t\u1ebf') { target = j.sheets[sid]; }
  });
  out.hasChiSheet = !!target;
  if (target) {
    var hits = [];
    var cd = target.cellData || {};
    Object.keys(cd).forEach(function (rr) {
      var row = cd[rr] || {};
      Object.keys(row).forEach(function (cc) {
        var v = row[cc] ? row[cc].v : null;
        if (typeof v === 'string' && v.indexOf('UNC00009') === 0) {
          hits.push({ row: parseInt(rr, 10) + 1, col: parseInt(cc, 10) + 1, v: v });
        }
      });
    });
    out.unc00009Hits = hits;
    out.chiRowCount = Object.keys(cd).length;
  }
  return out;
}"""

UI = r"""() => {
  var out = {};
  out.finKind = (typeof FIN_KIND !== 'undefined') ? FIN_KIND : null;
  out.unitId = (typeof finLastView !== 'undefined' && finLastView) ? finLastView.id : null;
  out.viewMaxCol = (typeof FIN_VIEW_MAXCOL !== 'undefined') ? FIN_VIEW_MAXCOL : null;
  try {
    var wb = finUniverAPI.getActiveWorkbook();
    var act = wb.getActiveSheet();
    out.activeSheet = (typeof act.getSheetName === 'function') ? act.getSheetName()
                    : (typeof act.getName === 'function') ? act.getName() : String(act);
    var shs = wb.getSheets();
    out.sheetCount = shs.length;
    out.sheetNames = shs.map(function (s) {
      return (typeof s.getSheetName === 'function') ? s.getSheetName()
           : (typeof s.getName === 'function') ? s.getName() : String(s);
    }).join(' | ');
  } catch (e) { out.err = String(e).slice(0, 140); }
  // 底部工作表标签（Univer 渲染出来的 DOM）
  try {
    var tabs = document.querySelectorAll('#univer_container [class*="sheet-bar"] [class*="tab"], #univer_container [class*="sheet-tab"]');
    out.sheetTabCount = tabs.length;
  } catch (e) {}
  return out;
}"""

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True, args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 1500, "height": 900})
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

    log("── UI 状态")
    ui = pg.evaluate(UI)
    for k, v in ui.items():
        log("   %-16s = %s" % (k, v))

    log("")
    log("── 合并快照解析（直接看后端 JSON）")
    info = pg.evaluate(JS)
    log("   HTTP 状态 = %s" % info.get("status"))
    log("   工作表顺序 = %s" % info.get("sheetNames"))
    log("   含 CN: 标记的工作表 = %s" % info.get("cnBySheet"))
    log("   有「Chi thực tế」表 = %s，快照里该表行数 = %s"
        % (info.get("hasChiSheet"), info.get("chiRowCount")))
    log("   快照里 UNC00009 出现位置 = %s" % info.get("unc00009Hits"))
    log("")
    log("   CN 标记行明细（快照内，1 基行号）：")
    for x in (info.get("cnRows") or []):
        log("      [%s] 行%-4s 列%-3s %-24s 日期=%-12s 凭证=%-10s 金额=%s"
            % (x.get("sheet"), x.get("row"), x.get("col"), x.get("mark"),
               str(x.get("date"))[:12], x.get("voucher"), x.get("amount")))
    b.close()
log("done")
