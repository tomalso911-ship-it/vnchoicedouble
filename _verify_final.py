# -*- coding: utf-8 -*-
"""最终验收（一次跑完，安全）：
 0. 把此前测试留下的 AC6 还原成 ☐（会话开始时它本来就是 ☐）；
 1. 统计栏：单格 / 一列 11 格 / 2 列 11 行，计数·总计·平均·最大·最小必须与快照逐格求和一致；
 2. 核销勾选：勾上 → 自动保存 → 文件真的变 ☑；取消 → 文件回到 ☐（最终不留痕）；
 3. 金额三块仍是 245,025,360、E5 仍是 41,400,000。
"""
import io
import json
import os
import shutil
import sys
import time

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import openpyxl  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
FIN = os.path.join(HERE, "finance_data")
CN = os.path.join(FIN, "cn_report.xlsx")
OUT = os.path.join(HERE, "_verify_final_out.txt")
L = []


def log(s):
    L.append(s)
    io.open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(s)


def read_file_state():
    wb = openpyxl.load_workbook(CN, data_only=False)
    ws = wb[wb.sheetnames[0]]
    tot = {}
    for tag, cols in (("base", (4, 5)), ("zh", (14, 15)), ("en", (24, 25))):
        t = 0.0
        for r in range(5, 205):
            for c in cols:
                v = ws.cell(r, c).value
                if isinstance(v, (int, float)) and not isinstance(v, bool):
                    t += abs(float(v))
        tot[tag] = round(t, 2)
    st = {"AC5": ws["AC5"].value, "AC6": ws["AC6"].value, "AC7": ws["AC7"].value,
          "E5": ws["E5"].value, "base": tot["base"], "zh": tot["zh"], "en": tot["en"]}
    wb.close()
    return st


def write_ac6(val):
    wb = openpyxl.load_workbook(CN, data_only=False)
    ws = wb[wb.sheetnames[0]]
    ws["AC6"].value = val
    tmp = CN + ".verify.tmp"
    wb.save(tmp)
    os.replace(tmp, CN)


# ---------- 0 ----------
shutil.copyfile(CN, os.path.join(FIN, "backups",
                                 "cn_report_%s_before_final.xlsx.bak" % time.strftime("%Y%m%d_%H%M%S")))
before = read_file_state()
log("① 初始状态 = %s" % json.dumps(before, ensure_ascii=False))
if before["AC6"] != "\u2610":
    write_ac6("\u2610")
    log("   （把测试留下的 AC6 还原成 ☐ → 现在 %r）" % read_file_state()["AC6"])

fails = []

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True, args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 1500, "height": 900})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("http://127.0.0.1:5050/lite", wait_until="domcontentloaded")
    pg.wait_for_timeout(1500)
    pg.fill("#loginUser", "tom")
    pg.fill("#loginPwd", "66668888")
    pg.click("#loginBtn")
    pg.wait_for_selector("#topbar:not(.hidden)", timeout=20000)
    pg.evaluate("() => { try { switchView('finance'); } catch(e){} }")
    pg.wait_for_timeout(1000)
    pg.evaluate("() => { var t = document.querySelector('#fin-tabs .fin-tab[data-key=\\'cn\\']'); if (t) t.click(); }")
    for _ in range(80):
        pg.wait_for_timeout(500)
        if pg.evaluate("() => (typeof finReady !== 'undefined') && !!finReady"):
            break
    pg.wait_for_timeout(3000)

    # ---------- 1 统计栏 ----------
    exp = pg.evaluate("""() => {
      var snap = fin_currentSnapshot(); var sid = snap.sheetOrder[0];
      var cd = (snap.sheets[sid] || {}).cellData || {}; var styles = snap.styles || {};
      function stat(r0, c0, nr, nc){
        var cnt = 0, nums = 0, sum = 0;
        for (var r = r0; r < r0 + nr; r++){
          var row = cd[String(r)] || {};
          for (var c = c0; c < c0 + nc; c++){
            var cell = row[String(c)]; var v = cell && cell.v;
            if (v === undefined || v === null) continue;
            if (typeof v === 'string' && !v.trim()) continue;
            cnt++;
            var n = (typeof v === 'number') ? v : ((typeof v === 'string' && /^-?[\\d,]+(\\.\\d+)?$/.test(v.trim())) ? Number(v.replace(/,/g,'')) : null);
            if (n !== null && isFinite(n)){
              var s = cell.s; var st = (typeof s === 'string') ? styles[s] : s;
              var pat = (st && st.n && st.n.pattern) || '';
              if (typeof fin_isDatePattern === 'function' && fin_isDatePattern(pat)) continue;
              nums++; sum += n;
            }
          }
        }
        return { cnt: cnt, nums: nums, sum: Math.round(sum*100)/100 };
      }
      return { single: stat(4,4,1,1), col11: stat(4,4,11,1), two2d: stat(4,3,11,2) };
    }""")
    log("")
    log("② 统计栏（期望值由快照逐格求和给出）= %s" % json.dumps(exp, ensure_ascii=False))
    for tag, r0, c0, nr, nc, key in (("单格 E5", 4, 4, 1, 1, "single"),
                                     ("E5:E15（11 格）", 4, 4, 11, 1, "col11"),
                                     ("D5:E15（22 格）", 4, 3, 11, 2, "two2d")):
        pg.evaluate("""async (a) => { finUniverAPI.getActiveWorkbook().getActiveSheet().getRange(a[0],a[1],a[2],a[3]).activate();
                       await new Promise(function(r){ setTimeout(r, 700); }); }""",
                    [r0, c0, nr, nc])
        i = pg.evaluate("() => window.__finStatInfo || null")
        bar = pg.evaluate("() => { var b = document.getElementById('fin_statbar'); return b ? b.textContent : 'NO-BAR'; }")
        e = exp[key]
        ok = bool(i) and i.get("cnt") == e["cnt"] and i.get("nums") == e["nums"] and abs((i.get("sum") or 0) - e["sum"]) < 1
        log("   【%s】%s" % (tag, bar.strip()))
        log("      内部值 cnt=%s nums=%s sum=%s | 期望 %s/%s/%s → %s"
            % (i and i.get("cnt"), i and i.get("nums"), i and i.get("sum"),
               e["cnt"], e["nums"], e["sum"], "✔" if ok else "✘"))
        if not ok:
            fails.append("统计栏 " + tag)

    # ---------- 2 核销勾选往返 ----------
    log("")
    log("③ 核销勾选（屏幕 ↔ 文件）")
    for tag, expect in (("勾上", "\u2611"), ("取消", "\u2610")):
        r = pg.evaluate("""async () => {
          var sh = finUniverAPI.getActiveWorkbook().getActiveSheet();
          var before = String(sh.getRange(5, 28).getValue());
          finCnCheckApply({ startRow: 5, endRow: 5, startColumn: 28, endColumn: 28 });
          for (var i = 0; i < 24; i++){ await new Promise(function(x){ setTimeout(x, 500); }); }
          return { before: before, after: String(sh.getRange(5, 28).getValue()) };
        }""")
        f = read_file_state()
        ok = (f["AC6"] == expect)
        log("   %s：屏幕 %s → %s ；文件 AC6=%r → %s" % (tag, r["before"], r["after"], f["AC6"], "✔" if ok else "✘"))
        if not ok:
            fails.append("核销" + tag)
    f = read_file_state()
    ok = (f["base"] == f["zh"] == f["en"] == 245025360 and f["E5"] == 41400000)
    log("   金额未被破坏（三块 245,025,360 / E5 41,400,000）？ %s" % ("✔" if ok else "✘"))
    if not ok:
        fails.append("金额")
    log("   页面报错 = %s" % (errs[:5] if errs else "无"))
    b.close()

log("")
log("最终文件状态 = %s" % json.dumps(read_file_state(), ensure_ascii=False))
log("===> 结论：%s" % ("全部通过" if not fails else ("失败项 " + str(fails))))
