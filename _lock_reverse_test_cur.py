#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""反向测试：故意篡改「货币代码不翻译」的四条不变量，确认 check_eq_cur_notrans_lock.py 会拦截。

8 种篡改（每一种都必须被拦下，否则锁是纸糊的）：
  1 删掉锁标记
  2 保护表里去掉 USD
  3 needTrans 里的豁免被删
  4 transOf 缓存防线被删
  5 requestTrans 的发请求豁免被删
  6 eqNoTransCur 的货币对拆分被删
  7 loadTrans 的脏缓存清理被删
  8 applyTrans 的显式跳过被删
"""
import os
import shutil
import subprocess
import sys
import tempfile

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "choice_lite.html")
LOCK = os.path.join(ROOT, "check_eq_cur_notrans_lock.py")
TMP = os.path.join(tempfile.gettempdir(), "_cur_notrans_reverse.html")

CASES = [
    ("1 删锁标记", "EQ-CURR-NOTRANS-LOCK-20261016", "EQ-CURR-NOTRANS-XXXX"),
    ("2 保护表去掉 USD", "['RMB', 'VND', 'USD']", "['RMB', 'VND']"),
    ("3 needTrans 豁免被删",
     "if (eqNoTransCur(t)) return false;      /* ★② 货币代码/货币对：永不翻译 */", ""),
    ("4 transOf 防线被删",
     "if (eqNoTransCur(text)) return null;    /* ★③ 货币代码/货币对：就算缓存里有译文也不用 */", ""),
    ("5 requestTrans 豁免被删",
     "if (eqNoTransCur(text)) { cb && cb(null); return; }   /* ★④ 货币代码/货币对：不发翻译请求 */", ""),
    ("6 货币对拆分被删", "var parts = s.split(/[-–—/", "var parts = s.split(/["),
    ("7 loadTrans 自愈被删",
     "if (eqNoTransCur(k) || eqNoTransWord(k)) { delete trans[k]; _purged = true; }", ""),
    ("8 applyTrans 跳过被删",
     "if (eqNoTransCur(cell.v)) return;   /* ★EQ-CURR-NOTRANS-LOCK-20261016：货币代码/货币对原样保留 */", ""),
    # ---- EQ-HEAD-LOCK-20261016：表头三语写死 ----
    ("9 删锁标记(表头)", "EQ-HEAD-LOCK-20261016", "EQ-HEAD-XXXX"),
    ("10 表头表被掏空", "{ zh: '序号', en: 'No.', vi: 'STT', alias: ['sự liên tiếp', 'số seri'] },", ""),
    ("11 英文被清空", "{ zh: '金额', en: 'Amount', vi: 'Số tiền', alias: ['Số lượng'] },",
     "{ zh: '金额', en: '', vi: 'Số tiền', alias: ['Số lượng'] },"),
    ("12 needTrans 表头豁免被删",
     "if (eqHeadRec(t)) return false;         /* ★EQ-HEAD-LOCK-20261016：表头三语已写死，不联网翻译 */", ""),
    ("13 transOf 表头写死被删",
     "    var _hr = eqHeadRec(text);\n    if (_hr) return _hr[target] || null;", ""),
    ("14 requestTrans 表头拦截被删",
     "if (eqHeadRec(text)) { cb && cb(null); return; }      /* ★EQ-HEAD-LOCK-20261016：表头三语已写死，不发请求 */", ""),
    ("15 applyTrans 表头闸门被删",
     "if (!eqHeadRec(cell.v) && !eqNeedTransLang(cell.v, L)) return;", ""),
    # ---- EQ-WORD-NOTRANS-LOCK-20261016：公司名 / 人名缩写不翻译 ----
    ("16 删锁标记(词)", "EQ-WORD-NOTRANS-LOCK-20261016", "EQ-WORD-XXXX"),
    ("17 保护表去掉 T.L", "['CHOICEVN', 'T.L', 'A.C', 'DABACO']", "['CHOICEVN', 'A.C', 'DABACO']"),
    ("18 needTrans 词豁免被删",
     "if (eqNoTransWord(t)) return false;     /* ★EQ-WORD-NOTRANS-LOCK-20261016：公司名/人名缩写永不翻译 */", ""),
    ("19 transOf 词防线被删",
     "if (eqNoTransWord(text)) return null;   /* ★EQ-WORD-NOTRANS-LOCK-20261016：公司名/人名缩写，缓存有译文也不用 */", ""),
    ("20 requestTrans 词拦截被删",
     "if (eqNoTransWord(text)) { cb && cb(null); return; }  /* ★EQ-WORD-NOTRANS-LOCK-20261016：公司名/人名缩写不发请求 */", ""),
    ("21 applyTrans 词跳过被删",
     "if (eqNoTransWord(cell.v)) return;  /* ★EQ-WORD-NOTRANS-LOCK-20261016：公司名/人名缩写原样保留 */", ""),
    ("22 loadTrans 词自愈被删",
     "if (eqNoTransCur(k) || eqNoTransWord(k)) { delete trans[k]; _purged = true; }",
     "if (eqNoTransCur(k)) { delete trans[k]; _purged = true; }"),
]


def run_lock(path):
    r = subprocess.run([sys.executable, LOCK, path], capture_output=True)
    return r.returncode


src = None
with open(SRC, encoding="utf-8") as f:
    src = f.read()

base_rc = run_lock(SRC)
print("原文件检查:", "通过(0)" if base_rc == 0 else "失败(%d) —— 先修好原文件再谈反向测试" % base_rc)
if base_rc != 0:
    sys.exit(1)

bad = 0
for name, old, new in CASES:
    if old not in src:
        print("  ? %-24s 锚点文本没找到，跳过（原文件结构可能已变）" % name)
        bad += 1
        continue
    with open(TMP, "w", encoding="utf-8") as f:
        # 锁标记在代码里出现多处（锁死区注释 + 各行内联注释），删标记这一项必须全删才算真删
        f.write(src.replace(old, new) if "删锁标记" in name else src.replace(old, new, 1))
    rc = run_lock(TMP)
    ok = (rc != 0)
    print("  %s %-24s 退出码=%d %s" % ("✓" if ok else "✗", name, rc,
                                       "已拦截" if ok else "★没拦住（锁有漏洞）"))
    if not ok:
        bad += 1
try:
    os.remove(TMP)
except OSError:
    pass

print("-" * 60)
if bad:
    print("✗ 反向测试有 %d 项未通过" % bad)
    sys.exit(1)
print("✓ 反向测试全部通过：%d 种篡改都被 check_eq_cur_notrans_lock.py 拦下" % len(CASES))
