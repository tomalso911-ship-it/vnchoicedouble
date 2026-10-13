# -*- coding: utf-8 -*-
"""端到端验证（2026-10-13 事故修复）：
① 服务端快照里基准块 = 中文块 = 英文块（越南盾真值）；
② 用【被污染的快照】（基准块 ÷3882.17）POST /save → 必须被 CN-BASIS-GUARD 拒绝，且文件哈希不变；
③ 用【真实浏览器】打开中国报表（新代码）：finCnBuildSavePayload() 三块合计必须都是 245,025,360，
   再点一次保存，文件仍是 41,400,000 / AC 勾选不丢。

安全：任何一次写入前都先备份；若 ② 意外改动了文件，立刻从备份还原。"""
import datetime
import hashlib
import io
import json
import os
import shutil
import sys
import urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import openpyxl  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
FIN = os.path.join(HERE, "finance_data")
CN = os.path.join(FIN, "cn_report.xlsx")
BASE = "http://127.0.0.1:5050"
OUT = os.path.join(HERE, "_verify_cn_guard_out.txt")
L = []


def log(s):
    L.append(str(s))
    io.open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(s)


def sha(p):
    return hashlib.sha256(io.open(p, "rb").read()).hexdigest()


def block_total(path, cols, r0=5, r1=205):
    wb = openpyxl.load_workbook(path, data_only=False)
    ws = wb[wb.sheetnames[0]]
    t = 0.0
    for r in range(r0, r1 + 1):
        for c in cols:
            v = ws.cell(r, c).value
            if isinstance(v, bool):
                continue
            if isinstance(v, (int, float)):
                t += abs(float(v))
    wb.close()
    return round(t, 2)


# ---------- 备份 ----------
safety = os.path.join(FIN, "backups",
                      "cn_report_%s_before_guard_verify.xlsx.bak"
                      % datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
shutil.copyfile(CN, safety)
h0 = sha(CN)
log("① 备份完成 -> %s" % os.path.basename(safety))
log("   文件：基准块=%s  中文块=%s  英文块=%s"
    % (block_total(CN, (4, 5)), block_total(CN, (14, 15)), block_total(CN, (24, 25))))

# ---------- ② 服务端快照（GET）与 rev ----------
req = urllib.request.Request(BASE + "/api/finance/cn-report/snapshot")
with urllib.request.urlopen(req, timeout=120) as r:
    rev = r.headers.get("X-Fin-Rev")
    snap = json.loads(r.read().decode("utf-8"))
sid = snap["sheetOrder"][0]
cd = snap["sheets"][sid]["cellData"]


def sv(r, c):
    return (cd.get(str(r), {}).get(str(c), {}) or {}).get("v")


log("② 快照 X-Fin-Rev = %r" % rev)
log("   快照 E5(基准)=%r  O5(中文)=%r  Y5(英文)=%r" % (sv(4, 4), sv(4, 14), sv(4, 24)))
ok_snap = sv(4, 4) == sv(4, 14) == sv(4, 24) == 41400000
log("   三块同值(41,400,000)？ %s" % ("✔ 是" if ok_snap else "✘ 否"))

# ---------- ③ 故意提交"被污染"的快照（基准块 ÷3882.17）→ 必须被拒 ----------
bad = json.loads(json.dumps(snap))
bcd = bad["sheets"][sid]["cellData"]
n_bad = 0
for rk, row in bcd.items():
    for ck in ("3", "4"):
        cell = row.get(ck)
        if isinstance(cell, dict) and isinstance(cell.get("v"), (int, float)):
            cell["v"] = round(cell["v"] / 3882.170520768837, 2)
            n_bad += 1
bad["__rev"] = rev
log("③ 构造污染快照：%d 个金额格 ÷3882.17（模拟屏幕人民币换算值被写回）" % n_bad)
rq = urllib.request.Request(BASE + "/api/finance/cn-report/save",
                            data=json.dumps(bad).encode("utf-8"),
                            headers={"Content-Type": "application/json"})
resp = json.loads(urllib.request.urlopen(rq, timeout=300).read().decode("utf-8"))
log("   服务端返回 = %s" % json.dumps(resp, ensure_ascii=False))
h1 = sha(CN)
blocked = bool(resp.get("guard") == "currency-regression" or resp.get("stale"))
log("   是否被拒？ %s ；文件是否未被改动？ %s"
    % ("✔" if blocked else "✘", "✔" if h1 == h0 else "✘ 被改动了，立刻还原"))
if h1 != h0:
    shutil.copyfile(safety, CN)
    log("   ★已从备份还原：%s" % ("✔" if sha(CN) == h0 else "✘ 还原后仍不一致"))

# ---------- ④ 真实浏览器：新代码下 payload 三块必须一致 ----------
from playwright.sync_api import sync_playwright  # noqa: E402

JS_PAYLOAD = """() => {
  try {
    var p = finCnBuildSavePayload();
    if (!p) return { err: 'null' };
    var sid = (p.sheetOrder || [])[0];
    var cd = (p.sheets[sid] || {}).cellData || {};
    function tot(c1, c2){
      var t = 0;
      for (var r = 4; r <= 204; r++){
        [c1, c2].forEach(function(c){
          var x = (cd[String(r)] || {})[String(c)];
          var n = x ? Number(String(x.v === undefined || x.v === null ? '' : x.v).replace(/[,\\s\\u00a0]/g, '')) : NaN;
          if (isFinite(n)) t += Math.abs(n);
        });
      }
      return Math.round(t * 100) / 100;
    }
    function v(r, c){ var x = (cd[String(r)] || {})[String(c)]; return x ? x.v : null; }
    return { kind: (typeof FIN_KIND !== 'undefined') ? FIN_KIND : '?',
             cur: fin_curCurrencyCode(), base_E5: v(4, 4), zh_O5: v(4, 14), en_Y5: v(4, 24),
             tot_base: tot(3, 4), tot_zh: tot(13, 14), tot_en: tot(23, 24),
             ac4: v(3, 28), ac5: v(4, 28), ac7: v(6, 28) };
  } catch(e){ return { err: String(e) }; }
}"""

h2 = sha(CN)
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True, args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 1500, "height": 900})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append("console." + m.type + ": " + m.text) if m.type == "error" else None)
    pg.goto(BASE + "/lite", wait_until="domcontentloaded")
    pg.wait_for_timeout(1500)
    pg.fill("#loginUser", "tom")
    pg.fill("#loginPwd", "66668888")
    pg.click("#loginBtn")
    pg.wait_for_selector("#topbar:not(.hidden)", timeout=20000)
    pg.evaluate("() => { try { switchView('finance'); } catch(e){} }")
    pg.wait_for_timeout(1000)
    pg.evaluate("() => { var t = document.querySelector('#fin-tabs .fin-tab[data-key=\\'cn\\']'); if (t) t.click(); }")
    ready = False
    for _ in range(80):
        pg.wait_for_timeout(500)
        if pg.evaluate("() => (typeof finReady !== 'undefined') && !!finReady"):
            ready = True
            break
    log("④ 浏览器：Univer 就绪 = %s" % ready)
    pg.wait_for_timeout(2500)
    pl = pg.evaluate(JS_PAYLOAD)
    log("   payload 诊断 = %s" % json.dumps(pl, ensure_ascii=False))
    log("   三块合计一致？ %s"
        % ("✔" if abs((pl.get("tot_base") or 0) - 245025360) < 1
           and abs((pl.get("tot_zh") or 0) - 245025360) < 1 else "✘"))
    log("   点一次「保存」（幂等：内容与文件一致，应落盘同样的值）")
    st = pg.evaluate("""async () => {
      await fin_autoSave();
      await new Promise(function(res){ setTimeout(res, 2500); });
      var s = document.getElementById('fin_status');
      return s ? s.textContent : 'no-status';
    }""")
    log("   保存后状态 = %s" % st)
    pg.wait_for_timeout(500)
    b.close()

log("⑤ 保存后文件：基准块=%s  中文块=%s  英文块=%s"
    % (block_total(CN, (4, 5)), block_total(CN, (14, 15)), block_total(CN, (24, 25))))
wb = openpyxl.load_workbook(CN, data_only=False)
ws = wb[wb.sheetnames[0]]
log("   E5=%r  E8=%r  O5=%r  Y5=%r  AC4=%r  AC7=%r  AC8=%r  AC9=%r"
    % (ws["E5"].value, ws["E8"].value, ws["O5"].value, ws["Y5"].value,
       ws["AC4"].value, ws["AC7"].value, ws["AC8"].value, ws["AC9"].value))
log("⑥ 页面报错 = %s" % (errs[:6] if errs else "无"))
