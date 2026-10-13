#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
财务「品牌名不翻译」锁死检查（lint / CI / git pre-commit 均可用）。

契约编号：FIN-NO-TRANS-20261013
（见 choice_lite.html 中的 ★锁死区★ 注释、app.py 的 _FIN_NO_TRANS）

为什么需要这个硬锁：
  用户明确要求品牌名「DABACO」在 zh / vi / en 三语里都必须保留拉丁写法，
  绝不能被机器翻译成中文（曾出现「达巴科」）或越南文。历史上它被译错过两次：
    · 工作表标签：「Thu Dabaco」→ zh「达巴科收款」（把 Thu 当成了"周四"→「周四达巴科」）
    · 持久译文缓存：「Thu Dabaco|zh」→「周四达巴科」
  修好之后必须锁死：任何未来重构 / 重新生成译文 / 换报表，都不得把这三层保护拿走。

四层不变量（缺一层 BUG 就会复发）：
  ① 前端保护词表 + 判定函数：choice_lite.html 必须存在
       var FIN_NO_TRANS = [ ... 'dabaco' ... ];  function fin_hasNoTrans(t){...}
     判定必须大小写无关、按子串匹配（'DABACO'/'Dabaco'/'dabaco' 都要命中）。
  ② 前端三条使用点必须都在：
       · fin_transChecked  —— 译文把保护词弄丢了 → 返回 null（调用方退回原文）
       · fin_targetName    —— 标签译文把保护词弄丢了 → 退回原名
       · fin_requestTrans  —— 含保护词的文字【根本不发】翻译请求
  ③ 服务端兜底：app.py 必须存在 _FIN_NO_TRANS（含 "dabaco"）+ _fin_has_no_trans()，
     且 fin_translate 在「原文含保护词而译文弄丢了」时把结果退回原文（res = text）。
  ④ 落地数据（真正的译文来源，最容易被打回原形）：
       · finance_data/fin_sheet_titles.json ："Thu Dabaco" 的 zh/en 必须仍含 Dabaco
       · finance_data/fin_trans_cache.json  ："Thu Dabaco|zh" 必须仍含 Dabaco
       · 两个文件里都不允许再出现「达巴科」

用法：
  python3 check_fin_no_trans_lock.py [choice_lite.html] [app.py] [finance_data 目录]
  不传参数时按脚本同目录推断。退出码：0 = 通过；1 = 契约被破坏。
"""
import json
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

DOC_ID = "FIN-NO-TRANS-20261013"
BAD_ZH = "\u8fbe\u5df4\u79d1"          # 「达巴科」——被译错时的产物


def fn_body(text, name):
    """取出 `function <name>(...)` 的函数体（含花括号配对），找不到返回 None。"""
    m = re.search(r"function\s+" + re.escape(name) + r"\s*\(", text)
    if not m:
        return None
    fb = text.find("{", m.end())
    if fb < 0:
        return None
    depth = 0
    i = fb
    while i < len(text):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[fb:i + 1]
        i += 1
    return text[fb:]


def py_body(text, name):
    """取出 Python `def <name>(...)` 的函数体（按缩进配对），找不到返回 None。"""
    m = re.search(r"^([ \t]*)def\s+" + re.escape(name) + r"\s*\(", text, re.M)
    if not m:
        return None
    head_indent = m.group(1)
    start = text.find("\n", m.end())
    if start < 0:
        return None
    lines = text[start + 1:].split("\n")
    out = []
    for ln in lines:
        if not ln.strip():
            out.append(ln)
            continue
        indent = ln[:len(ln) - len(ln.lstrip())]
        if len(indent) <= len(head_indent):
            break
        out.append(ln)
    return "\n".join(out)


def check_html(path, errors, warnings):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    # ---- 0) 锁标记与保护词表 ----
    if DOC_ID not in text:
        errors.append("找不到锁标记 %s（锁死区注释被删除？）" % DOC_ID)

    m = re.search(r"var\s+FIN_NO_TRANS\s*=\s*\[([^\]]*)\]", text)
    if not m:
        errors.append("找不到 var FIN_NO_TRANS = [...]（品牌名保护词表被删除？）")
    elif "dabaco" not in m.group(1).lower():
        errors.append("FIN_NO_TRANS 里不再包含 'dabaco'（DABACO 保护被摘掉）")

    # ---- ① 判定函数必须存在且按 FIN_NO_TRANS 子串匹配 ----
    hnt = fn_body(text, "fin_hasNoTrans")
    if hnt is None:
        errors.append("找不到 fin_hasNoTrans（保护词判定函数被删除？）")
    else:
        if "FIN_NO_TRANS" not in hnt:
            errors.append("不变量①被破坏：fin_hasNoTrans 不再读取 FIN_NO_TRANS（保护词表被架空）")
        if "toLowerCase" not in hnt:
            errors.append("不变量①被破坏：fin_hasNoTrans 缺少 toLowerCase（大小写敏感→'DABACO' 漏判）")
        if "indexOf" not in hnt and "includes" not in hnt:
            errors.append("不变量①被破坏：fin_hasNoTrans 不再是子串匹配（整串相等会漏判长句里的品牌名）")

    # ---- ② 三条使用点 ----
    tc = fn_body(text, "fin_transChecked")
    if tc is None:
        errors.append("找不到 fin_transChecked（译文过滤函数被删除？）")
    else:
        if "fin_hasNoTrans(orig)" not in tc.replace(" ", ""):
            errors.append("不变量②被破坏：fin_transChecked 不再检查原文里的保护词")
        if not re.search(r"fin_hasNoTrans\s*\(\s*trans\s*\)\s*\?\s*trans\s*:\s*null", tc):
            errors.append("不变量②被破坏：fin_transChecked 在保护词被译掉时不再返回 null"
                          "（应写 `return fin_hasNoTrans(trans) ? trans : null;`）")

    tn = fn_body(text, "fin_targetName")
    if tn is None:
        errors.append("找不到 fin_targetName（工作表标签翻译入口被删除？）")
    else:
        if "fin_hasNoTrans(on)" not in tn.replace(" ", ""):
            errors.append("不变量②被破坏：fin_targetName 不再检查原名里的保护词")
        if not re.search(r"if\s*\(\s*on\s*&&\s*fin_hasNoTrans\s*\(\s*on\s*\)\s*&&\s*!fin_hasNoTrans\s*\(\s*nm\s*\)\s*\)\s*return\s+on\s*;", tn):
            errors.append("不变量②被破坏：fin_targetName 在标签译文弄丢保护词时不再退回原名"
                          "（应写 `if (on && fin_hasNoTrans(on) && !fin_hasNoTrans(nm)) return on;`）")

    rt = fn_body(text, "fin_requestTrans")
    if rt is None:
        errors.append("找不到 fin_requestTrans（按需翻译入口被删除？）")
    elif not re.search(r"if\s*\(\s*fin_hasNoTrans\s*\(\s*text\s*\)\s*\)\s*return\s*;", rt):
        errors.append("不变量②被破坏：fin_requestTrans 不再对含保护词的文字直接 return"
                      "（会联网把 DABACO 译成「达巴科」）")

    # ---- 表名兜底表：Thu Dabaco 的 zh/en 必须仍含 Dabaco ----
    m2 = re.search(r"FIN_SHEET_TITLES_FALLBACK\s*=\s*\{(.*?)\n\s*\};", text, re.S)
    if not m2:
        errors.append("找不到 FIN_SHEET_TITLES_FALLBACK（工作表标签三语兜底表被删除？）")
    else:
        blk = m2.group(1)
        mm = re.search(r"'Thu Dabaco'\s*:\s*\{([^}]*)\}", blk)
        if not mm:
            errors.append("兜底表里找不到 'Thu Dabaco' 条目（标签三语被删？）")
        else:
            one = mm.group(1)
            for lang in ("zh", "en"):
                lv = re.search(lang + r"\s*:\s*'([^']*)'", one)
                if not lv:
                    errors.append("兜底表 'Thu Dabaco' 缺少 %s 译文" % lang)
                elif "dabaco" not in lv.group(1).lower():
                    errors.append("兜底表 'Thu Dabaco'.%s = %r 已不含 Dabaco（品牌名被翻译了）"
                                  % (lang, lv.group(1)))
            if BAD_ZH in one:
                errors.append("兜底表 'Thu Dabaco' 里又出现了「达巴科」")


def check_app(path, errors):
    if not os.path.exists(path):
        errors.append("找不到 %s" % path)
        return
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    if DOC_ID not in text:
        errors.append("app.py 里找不到锁标记 %s" % DOC_ID)

    m = re.search(r"_FIN_NO_TRANS\s*=\s*\(([^)]*)\)", text)
    if not m:
        errors.append("app.py 找不到 _FIN_NO_TRANS 常量（服务端保护词表被删除？）")
    elif "dabaco" not in m.group(1).lower():
        errors.append("app.py 的 _FIN_NO_TRANS 里不再包含 'dabaco'")

    h = py_body(text, "_fin_has_no_trans")
    if h is None:
        errors.append("app.py 找不到 _fin_has_no_trans（服务端保护词判定被删除？）")
    else:
        if "_FIN_NO_TRANS" not in h:
            errors.append("不变量③被破坏：_fin_has_no_trans 不再读取 _FIN_NO_TRANS")
        if "lower()" not in h:
            errors.append("不变量③被破坏：_fin_has_no_trans 缺少 lower()（大小写漏判）")

    ft = py_body(text, "fin_translate")
    if ft is None:
        errors.append("app.py 找不到 fin_translate（统一翻译链被删除？）")
    elif not re.search(r"if\s+res\s+and\s+_fin_has_no_trans\s*\(\s*text\s*\)\s+and\s+not\s+_fin_has_no_trans\s*\(\s*res\s*\)\s*:\s*\n\s*res\s*=\s*text", ft):
        errors.append("不变量③被破坏：fin_translate 不再「保护词被译掉就退回原文」"
                      "（应写 `if res and _fin_has_no_trans(text) and not _fin_has_no_trans(res): res = text`）")


def check_data(fin_dir, errors):
    # ---- 工作表标签三语映射 ----
    p = os.path.join(fin_dir, "fin_sheet_titles.json")
    if not os.path.exists(p):
        errors.append("找不到 %s（工作表标签三语映射）" % p)
    else:
        raw = open(p, encoding="utf-8").read()
        if BAD_ZH in raw:
            errors.append("%s 里又出现了「达巴科」" % p)
        try:
            titles = json.loads(raw) or {}
        except Exception as e:
            errors.append("%s 不是合法 JSON：%s" % (p, e))
            titles = {}
        t = titles.get("Thu Dabaco")
        if not isinstance(t, dict):
            errors.append("fin_sheet_titles.json 里找不到 'Thu Dabaco' 表名条目")
        else:
            for lang in ("vi", "zh", "en"):
                v = t.get(lang) or ""
                if "dabaco" not in v.lower():
                    errors.append("表名 'Thu Dabaco'.%s = %r 已不含 Dabaco（品牌名被翻译）" % (lang, v))

    # ---- 持久译文缓存 ----
    p2 = os.path.join(fin_dir, "fin_trans_cache.json")
    if not os.path.exists(p2):
        errors.append("找不到 %s（持久译文缓存）" % p2)
    else:
        raw2 = open(p2, encoding="utf-8").read()
        if BAD_ZH in raw2:
            errors.append("%s 里又出现了「达巴科」（错译被写回缓存）" % p2)
        try:
            cache = json.loads(raw2) or {}
        except Exception as e:
            errors.append("%s 不是合法 JSON：%s" % (p2, e))
            cache = {}
        for key in ("Thu Dabaco|zh", "Thu Dabaco|en"):
            v = cache.get(key)
            if v is None:
                errors.append("fin_trans_cache.json 缺少条目 %r" % key)
            elif "dabaco" not in str(v).lower():
                errors.append("fin_trans_cache.json[%r] = %r 已不含 Dabaco（品牌名被翻译）" % (key, v))


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    args = sys.argv[1:]
    html = args[0] if len(args) > 0 else os.path.join(here, "choice_lite.html")
    app = args[1] if len(args) > 1 else os.path.join(here, "app.py")
    fin_dir = args[2] if len(args) > 2 else os.path.join(here, "finance_data")

    for must in (html, app):
        if not os.path.exists(must):
            print("✗ 找不到文件: %s" % must)
            sys.exit(1)

    errors = []
    check_html(html, errors, [])
    check_app(app, errors)
    check_data(fin_dir, errors)

    print("检查目标: %s | %s | %s" % (html, app, fin_dir))
    if not errors:
        print("✓ 通过：品牌名「DABACO」不翻译契约未被破坏（%s 四层保护全在）" % DOC_ID)
        sys.exit(0)
    for e in errors:
        print("  ✗ 违规: %s" % e)
    print("✗ 失败：共 %d 处违规。这是「锁死」契约，禁止篡改；"
          "请恢复 %s 的四层保护后再提交。" % (len(errors), DOC_ID))
    sys.exit(1)


if __name__ == "__main__":
    main()
