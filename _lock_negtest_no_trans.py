# -*- coding: utf-8 -*-
"""反向测试：故意篡改「DABACO 不翻译」的四层保护，确认 check_fin_no_trans_lock.py 会拦截。"""
import io
import json
import os
import shutil
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
CHECK = os.path.join(HERE, "check_fin_no_trans_lock.py")
HTML = os.path.join(HERE, "choice_lite.html")
APP = os.path.join(HERE, "app.py")
FIN = os.path.join(HERE, "finance_data")

HTML_TAMPERS = [
    ("① 保护词表摘掉 dabaco", "var FIN_NO_TRANS = ['dabaco'];", "var FIN_NO_TRANS = [];"),
    ("① 判定改成大小写敏感", "var s = String(t == null ? '' : t).toLowerCase();",
     "var s = String(t == null ? '' : t);"),
    ("② 译文过滤不再退回原文", "return fin_hasNoTrans(trans) ? trans : null;",
     "return trans;"),
    ("② 标签翻译不再退回原名",
     "if (on && fin_hasNoTrans(on) && !fin_hasNoTrans(nm)) return on;   // \u2605\u522b\u628a DABACO \u8bd1\u6389",
     "if (false) return on;"),
    ("② 含保护词也照样联网翻译", "if (fin_hasNoTrans(text)) return;         // \u2605\u4fdd\u62a4\u8bcd\uff08DABACO\u2026\uff09\u4e0d\u7ffb\u8bd1",
     "if (false) return;"),
    ("④ 兜底表标签被译成中文", "'Thu Dabaco':           { vi:'Thu Dabaco',           zh:'\u6536\u6b3e Dabaco',   en:'Dabaco Receipts' },",
     "'Thu Dabaco':           { vi:'Thu Dabaco',           zh:'\u8fbe\u5df4\u79d1\u6536\u6b3e',   en:'Dabaco Receipts' },"),
]

APP_TAMPERS = [
    ("③ 服务端不再退回原文",
     "if res and _fin_has_no_trans(text) and not _fin_has_no_trans(res):\n        res = text",
     "if False:\n        res = text"),
    ("③ 服务端保护词表摘掉 dabaco", '_FIN_NO_TRANS = ("dabaco",)', '_FIN_NO_TRANS = ()'),
]


def run(html, app, fin_dir):
    r = subprocess.run([sys.executable, CHECK, html, app, fin_dir],
                       capture_output=True, text=True, encoding="utf-8", errors="replace",
                       env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    return r.returncode, (r.stdout or "")


def main():
    ok = True
    tmp_html = os.path.join(HERE, "_tamper_no_trans.html")
    tmp_app = os.path.join(HERE, "_tamper_no_trans_app.py")
    tmp_fin = os.path.join(HERE, "_tamper_no_trans_fin")

    src_html = io.open(HTML, encoding="utf-8").read()
    src_app = io.open(APP, encoding="utf-8").read()

    def report(name, rc, out):
        nonlocal ok
        caught = rc != 0
        print(("\u2713 \u5df2\u62e6\u622a  " if caught else "\u2717 \u6f0f\u68c0!!  ") + name + "  (exit=%d)" % rc)
        if caught:
            first = [l for l in out.splitlines() if "\u8fdd\u89c4" in l]
            if first:
                print("     ", first[0].strip())
        else:
            ok = False

    # ---- HTML 篡改 ----
    for name, old, new in HTML_TAMPERS:
        if old not in src_html:
            print("!! \u7be1\u6539\u70b9\u672a\u627e\u5230\uff08\u951a\u70b9\u53d8\u4e86\uff09:", name)
            ok = False
            continue
        io.open(tmp_html, "w", encoding="utf-8").write(src_html.replace(old, new, 1))
        rc, out = run(tmp_html, APP, FIN)
        report(name, rc, out)
    if os.path.exists(tmp_html):
        os.remove(tmp_html)

    # ---- app.py 篡改 ----
    for name, old, new in APP_TAMPERS:
        if old not in src_app:
            print("!! \u7be1\u6539\u70b9\u672a\u627e\u5230\uff08\u951a\u70b9\u53d8\u4e86\uff09:", name)
            ok = False
            continue
        io.open(tmp_app, "w", encoding="utf-8").write(src_app.replace(old, new, 1))
        rc, out = run(HTML, tmp_app, FIN)
        report(name, rc, out)
    if os.path.exists(tmp_app):
        os.remove(tmp_app)

    # ---- 数据篡改（fin_trans_cache.json 把品牌名译成中文）----
    if os.path.isdir(tmp_fin):
        shutil.rmtree(tmp_fin)
    os.makedirs(tmp_fin)
    for fn in ("fin_sheet_titles.json", "fin_trans_cache.json"):
        shutil.copyfile(os.path.join(FIN, fn), os.path.join(tmp_fin, fn))
    ct = os.path.join(tmp_fin, "fin_trans_cache.json")
    data = json.loads(io.open(ct, encoding="utf-8").read())
    data["Thu Dabaco|zh"] = "\u5468\u56db\u8fbe\u5df4\u79d1"
    io.open(ct, "w", encoding="utf-8").write(json.dumps(data, ensure_ascii=False, indent=1))
    rc, out = run(HTML, APP, tmp_fin)
    report("④ 译文缓存被打回「周四达巴科」", rc, out)

    st = os.path.join(tmp_fin, "fin_sheet_titles.json")
    t = json.loads(io.open(st, encoding="utf-8").read())
    t["Thu Dabaco"] = {"vi": "Thu Dabaco", "zh": "\u8fbe\u5df4\u79d1\u6536\u6b3e", "en": "Dabaco Receipts"}
    io.open(st, "w", encoding="utf-8").write(json.dumps(t, ensure_ascii=False, indent=1))
    rc, out = run(HTML, APP, tmp_fin)
    report("④ 表名映射被打回「达巴科收款」", rc, out)

    shutil.rmtree(tmp_fin, ignore_errors=True)

    print()
    print("\u53cd\u5411\u6d4b\u8bd5\u7ed3\u679c:", "\u5168\u90e8\u62e6\u622a \u2713" if ok else "\u5b58\u5728\u6f0f\u68c0 \u2717")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
