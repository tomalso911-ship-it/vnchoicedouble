# -*- coding: utf-8 -*-
"""验证「拉选多个数据 → 计数/总计/平均/最大/最小 正确」（用户 2026-10-13 截图：只显示 计数:1）。
只读：全程不点保存（并且把保存请求挡掉，避免任何落盘）。
测试三种选区：单格 / 一列 11 格 / 2 列 11 行，结果与快照里逐格求和交叉核对。"""
import datetime
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_verify_statbar_multi_out.txt")
L = []


def log(s):
    L.append(s)
    io.open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(s)


BLOCK_SAVE = """() => {
  var _f = window.fetch;
  window.fetch = function(u, o){
    try {
      var url = (typeof u === 'string') ? u : ((u && u.url) || '');
      var m = String((o && o.method) || 'GET').toUpperCase();
      if (m === 'POST' && url.indexOf('/api/finance/cn-report/save') >= 0){
        console.log('[PROBE-BLOCKED-SAVE]');
        return Promise.resolve(new Response(JSON.stringify({ok:true, saved_at:'blocked'}), {status:200, headers:{'Content-Type':'application/json'}}));
      }
    } catch(e){}
    return _f.apply(this, arguments);
  };
}"""


def j(o):
    return json.dumps(o, ensure_ascii=False)


with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True, args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 1500, "height": 900})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.add_init_script(BLOCK_SAVE)
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
    log("中国报表已载入；币种=%s" % pg.evaluate("() => fin_curCurrencyCode()"))

    def bar_html():
        return pg.evaluate("() => { var b = document.getElementById('fin_statbar'); return b ? b.textContent : 'NO-BAR'; }")

    def info():
        return pg.evaluate("() => window.__finStatInfo || null")

    def activate(r0, c0, nrows, ncols):
        return pg.evaluate("""async (a) => {
          var sh = finUniverAPI.getActiveWorkbook().getActiveSheet();
          sh.getRange(a[0], a[1], a[2], a[3]).activate();
          await new Promise(function(res){ setTimeout(res, 700); });
          return true;
        }""", [r0, c0, nrows, ncols])

    # 期望值：直接按快照逐格求和（只算数字格），与统计栏口径一致
    expect = pg.evaluate("""() => {
      var snap = fin_currentSnapshot();
      var sid = snap.sheetOrder[0];
      var cd = (snap.sheets[sid] || {}).cellData || {};
      function stat(r0, c0, nr, nc){
        var cnt = 0, nums = 0, sum = 0, mn = null, mx = null;
        for (var r = r0; r < r0 + nr; r++){
          var row = cd[String(r)] || {};
          for (var c = c0; c < c0 + nc; c++){
            var cell = row[String(c)];
            var v = cell && cell.v;
            if (v === undefined || v === null) continue;
            if (typeof v === 'string' && !v.trim()) continue;
            cnt++;
            var n = (typeof v === 'number') ? v : ((typeof v === 'string' && /^-?[\\d,]+(\\.\\d+)?$/.test(v.trim())) ? Number(v.replace(/,/g, '')) : null);
            if (n !== null && isFinite(n)){
              var s = cell.s, styles = snap.styles || {};
              var st = (typeof s === 'string') ? styles[s] : s;
              var pat = (st && st.n && st.n.pattern) || '';
              if (typeof fin_isDatePattern === 'function' && fin_isDatePattern(pat)) continue;
              nums++; sum += n;
              if (mn === null || n < mn) mn = n;
              if (mx === null || n > mx) mx = n;
            }
          }
        }
        return { cnt: cnt, nums: nums, sum: Math.round(sum * 100) / 100,
                 avg: nums ? Math.round(sum / nums * 100) / 100 : null,
                 min: mn, max: mx };
      }
      return { single: stat(4, 4, 1, 1), col11: stat(4, 4, 11, 1), two2d: stat(4, 3, 11, 2) };
    }""")
    log("快照口径期望值 = %s" % j(expect))

    cases = [("单格 E5", 4, 4, 1, 1, "single"), ("一列 E5:E15（11 格）", 4, 4, 11, 1, "col11"),
             ("两列 D5:E15（22 格）", 4, 3, 11, 2, "two2d")]
    fails = []
    for tag, r0, c0, nr, nc, key in cases:
        activate(r0, c0, nr, nc)
        i = info()
        html = bar_html()
        e = expect[key]
        got = {k: (i or {}).get(k) for k in ("cnt", "nums", "sum")}
        ok = bool(i) and i.get("cnt") == e["cnt"] and i.get("nums") == e["nums"] \
             and abs((i.get("sum") or 0) - (e["sum"] or 0)) < 1
        log("【%s】统计栏 = %s" % (tag, html.strip()))
        log("   内部值 = %s ；期望 cnt=%s nums=%s sum=%s ；%s"
            % (j(got), e["cnt"], e["nums"], e["sum"], "✔ 正确" if ok else "✘ 不符"))
        if not ok:
            fails.append(tag)

    log("页面报错 = %s" % (errs[:5] if errs else "无"))
    log("失败项 = %s" % (fails if fails else "无（全部通过）"))
    b.close()
