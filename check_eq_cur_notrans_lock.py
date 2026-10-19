#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
股东权益报表「货币代码不翻译」锁死检查（lint / CI / git pre-commit 均可用）。

契约编号：EQ-CURR-NOTRANS-LOCK-20261016
（见 choice_lite.html 中的 ★★锁死区★★ 注释 EQ-CURR-NOTRANS-LOCK-20261016）

用户原话（2026-10-16）：
  「表格里面的 RMB, VND, USD. RMB-VND, USD-VND，这几个单元格里面的内容禁止被翻译，锁死！」

落点（已核对 equity_report.xlsx）：
  股东权益报表 · 工作表 Đầu tư Trung Quốc（中国投资数据）第 3 行
  H3=RMB  I3=VND  J3=USD  K3=RMB-VND  L3=USD-VND

为什么要锁（坏了会怎样）：
  这些是【货币代码 / 货币对】，不是自然语言。被译成「人民币」「Nhân dân tệ」后：
    · 表头与公式、对账口径全部对不上；
    · 更糟的是译文会被【写回 xlsx】（保存链把屏幕值落盘），下次打开文件里就是译文。

四条不变量（缺一条 BUG 就会复发）：
  ① 判定函数 eqNoTransCur()：整格归一化（去空白 + 转大写）后等于货币代码，
     或由货币代码用 - – — / \ | 组成的货币对（RMB-VND / USD/VND …）；
  ② needTrans()    —— 直接判「不需要翻译」（绝不发 /api/translate）；
  ③ transOf()      —— 直接返回 null（缓存里【已存过】译文也绝不套用 —— 历史脏数据防线）；
  ④ requestTrans() —— 直接回调 null 返回，不发请求。
  另外两处自愈/双保险：loadTrans() 载入时清掉缓存里货币代码的脏译文；
  applyTrans() 里显式跳过这些格子。

用法：
  python3 check_eq_cur_notrans_lock.py [choice_lite.html]
  不传路径时默认检查同目录下的 choice_lite.html。
退出码：0 = 通过；1 = 契约被破坏（CI 失败 / pre-commit 拦截）。
"""
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

DOC_ID = "EQ-CURR-NOTRANS-LOCK-20261016"
DOC2_ID = "EQ-HEAD-LOCK-20261016"
DOC3_ID = "EQ-WORD-NOTRANS-LOCK-20261016"
CODES = ("rmb", "vnd", "usd")
# 用户截图里锁定的中文表头（顺序也要一致）
HEAD_ZH = ['序号', '年份', '公司', '付款来自', '付款至', '金额', '汇率', '日期', '现金/转账', '备注']
# 用户截图里要求「不翻译」的公司名 / 人名缩写（须与 EQ_NO_TRANS_WORDS 里一字不差）
# ★2026-10-18 用户补充（EQ-NAME-NOTRANS-LOCK-20261018）：股东结构里的人名全部不翻译
#   —— 截图 A.L / A.C / A.J / A.T / A.R / A.M / A.Z
WORDS = ("CHOICEVN", "T.L", "A.C", "A.J", "A.L", "A.T", "A.R", "A.M", "A.Z", "DABACO")


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


def check(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    errors = []

    # ---- 0) 锁标记 ----
    if DOC_ID not in text:
        errors.append("找不到锁标记 %s（锁死区注释被删除？）" % DOC_ID)

    # ---- ① 货币代码表 + 判定函数 ----
    m = re.search(r"var\s+EQ_NO_TRANS_CUR\s*=\s*\[([^\]]*)\]", text)
    if not m:
        errors.append("找不到 var EQ_NO_TRANS_CUR = [...]（货币代码保护表被删除？）")
    else:
        body = m.group(1).lower()
        for c in CODES:
            if ("'" + c + "'") not in body and ('"' + c + '"') not in body:
                errors.append("EQ_NO_TRANS_CUR 里缺少 %r（货币代码保护被摘掉）" % c.upper())

    f_body = fn_body(text, "eqNoTransCur")
    if f_body is None:
        errors.append("找不到 eqNoTransCur（货币代码判定函数被删除？）")
    else:
        if "EQ_NO_TRANS_CUR" not in f_body:
            errors.append("①eqNoTransCur 不再读取 EQ_NO_TRANS_CUR（保护表被架空）")
        if "toUpperCase" not in f_body:
            errors.append("①eqNoTransCur 缺少 toUpperCase（小写 rmb/usd 会漏判）")
        if "indexOf" not in f_body:
            errors.append("①eqNoTransCur 不再是集合匹配（整串相等会漏判货币对）")
        if "split" not in f_body:
            errors.append("①eqNoTransCur 缺少货币对拆分（RMB-VND / USD/VND 会漏判）")
        elif "split(/" not in f_body.replace(" ", ""):
            errors.append("①eqNoTransCur 不再用正则拆分货币对（应写 s.split(/[-–—/\\\\|]+/)）")
        else:
            seg = f_body.replace(" ", "").split("split(/", 1)[1].split("]", 1)[0]
            for ch in ("-", "/", "|"):
                if ch not in seg:
                    errors.append("①eqNoTransCur 货币对分隔符集合缺少 %r（应含 - – — / \\ |）" % ch)

    # ---- ② needTrans 直接判「不需要翻译」 ----
    nt = fn_body(text, "needTrans")
    if nt is None:
        errors.append("找不到 needTrans（股东权益翻译入口被删除？）")
    elif not re.search(r"if\s*\(\s*eqNoTransCur\s*\(\s*t\s*\)\s*\)\s*return\s+false\s*;", nt):
        errors.append("②needTrans 不再对货币代码直接 return false"
                      "（会联网把 RMB 译成「人民币」）")

    # ---- ③ transOf 缓存防线 ----
    to = fn_body(text, "transOf")
    if to is None:
        errors.append("找不到 transOf（译文取值入口被删除？）")
    elif not re.search(r"if\s*\(\s*eqNoTransCur\s*\(\s*text\s*\)\s*\)\s*return\s+null\s*;", to):
        errors.append("③transOf 不再对货币代码返回 null"
                      "（缓存里的脏译文「人民币」会被套上去）")

    # ---- ④ requestTrans 不发请求 ----
    rt = fn_body(text, "requestTrans")
    if rt is None:
        errors.append("找不到 requestTrans（翻译请求入口被删除？）")
    elif not re.search(r"if\s*\(\s*eqNoTransCur\s*\(\s*text\s*\)\s*\)\s*\{\s*cb\s*&&\s*cb\s*\(\s*null\s*\)\s*;\s*return\s*;\s*\}", rt):
        errors.append("④requestTrans 不再对货币代码直接返回"
                      "（会把 RMB 发去翻译）")

    # ---- 自愈：loadTrans 清脏缓存 ----
    lt = fn_body(text, "loadTrans")
    if lt is None:
        errors.append("找不到 loadTrans（股东权益译文缓存载入被删除？）")
    else:
        if "eqNoTransCur(k)" not in lt:
            errors.append("loadTrans 不再清理缓存里的货币代码脏译文（历史错译会被复用）")
        if "delete trans[k]" not in lt:
            errors.append("loadTrans 缺少 delete trans[k]（脏译文没有被真正删掉）")

    # ---- 双保险：applyTrans 显式跳过 ----
    at = fn_body(text, "applyTrans")
    if at is None:
        errors.append("找不到 applyTrans（显示端翻译被删除？）")
    else:
        if not re.search(r"if\s*\(\s*eqNoTransCur\s*\(\s*cell\.v\s*\)\s*\)\s*return\s*;", at):
            errors.append("applyTrans 里缺少 eqNoTransCur(cell.v) 跳过（货币格子可能被换掉）")

    # ================= EQ-HEAD-LOCK-20261016：表头三语写死 =================
    # 用户 2026-10-16：「这个中文就不用改动了，请锁住；英文和越南文，也按照现在的意思锁住！」
    if DOC2_ID not in text:
        errors.append("找不到锁标记 %s（表头三语锁死区注释被删除？）" % DOC2_ID)

    m = re.search(r"var\s+EQ_HEAD_LOCK\s*=\s*\[(.*?)\n\s*\];", text, re.S)
    if not m:
        errors.append("找不到 var EQ_HEAD_LOCK = [...]（表头三语常量表被删除？）")
    else:
        block = m.group(1)
        rows = re.findall(r"\{\s*zh:\s*'([^']*)'\s*,\s*en:\s*'([^']*)'\s*,\s*vi:\s*'([^']*)'", block)
        zh_list = [r[0] for r in rows]
        if zh_list != HEAD_ZH:
            errors.append("EQ_HEAD_LOCK 的中文表头被改动或顺序变了：%s（应为 %s）"
                          % (zh_list, HEAD_ZH))
        for zh, en, vi in rows:
            if not en.strip():
                errors.append("EQ_HEAD_LOCK 里 %r 的英文被清空（英文界面会退回联网翻译）" % zh)
            if not vi.strip():
                errors.append("EQ_HEAD_LOCK 里 %r 的越南文被清空（越文界面会退回联网翻译）" % zh)

    hr = fn_body(text, "eqHeadRec")
    if hr is None:
        errors.append("找不到 eqHeadRec（表头识别函数被删除？）")
    else:
        if "EQ_HEAD_LOCK" not in hr:
            errors.append("eqHeadRec 不再读取 EQ_HEAD_LOCK（写死表被架空）")
        if "toLowerCase" not in hr:
            errors.append("eqHeadRec 缺少 toLowerCase（'năm' / 'Năm' 这类大小写差异会认不出）")
        if "alias" not in hr:
            errors.append("eqHeadRec 不再索引 alias（文件里历史漂移的写法会认不出）")

    nt = fn_body(text, "needTrans")
    if nt is not None and not re.search(r"if\s*\(\s*eqHeadRec\s*\(\s*t\s*\)\s*\)\s*return\s+false\s*;", nt):
        errors.append("needTrans 缺少 eqHeadRec 豁免（表头会被发去联网翻译）")

    to2 = fn_body(text, "transOf")
    if to2 is not None:
        if "eqHeadRec(text)" not in to2:
            errors.append("transOf 不再查 eqHeadRec（表头会被缓存里的说法覆盖）")
        if not re.search(r"return\s+_hr\[target\]", to2):
            errors.append("transOf 缺少 `return _hr[target]`（表头没有按写死值返回）")

    rt2 = fn_body(text, "requestTrans")
    if rt2 is not None and "eqHeadRec(text)" not in rt2:
        errors.append("requestTrans 缺少 eqHeadRec 拦截（表头仍会被发去翻译）")

    at2 = fn_body(text, "applyTrans")
    if at2 is not None and "eqHeadRec(cell.v)" not in at2:
        errors.append("applyTrans 缺少 eqHeadRec(cell.v)（越文界面下表头会被「只翻汉字格」的闸门挡掉）")

    # ================= EQ-WORD-NOTRANS-LOCK-20261016：公司名/人名缩写不翻译 =================
    # 用户 2026-10-16：「这个内容也不需要翻译！」（截图：Choice VN / T.L / A.C）
    # 用户 2026-10-17：「A.C / A.J / A.L 这三组名字不要翻译！」（补 A.J / A.L）
    # 落点：股东权益 ·「中国投资数据」E4:G6
    if DOC3_ID not in text:
        errors.append("找不到锁标记 %s（公司名/人名缩写不翻译的锁死区注释被删除？）" % DOC3_ID)

    m3 = re.search(r"var\s+EQ_NO_TRANS_WORDS\s*=\s*\[([^\]]*)\]", text)
    if not m3:
        errors.append("找不到 var EQ_NO_TRANS_WORDS = [...]（公司名/人名缩写保护表被删除？）")
    else:
        body3 = m3.group(1)
        for w in WORDS:
            if ("'" + w + "'") not in body3 and ('"' + w + '"') not in body3:
                errors.append("EQ_NO_TRANS_WORDS 里缺少 %r（该词会被翻译）" % w)

    wf = fn_body(text, "eqNoTransWord")
    if wf is None:
        errors.append("找不到 eqNoTransWord（公司名/人名缩写判定函数被删除？）")
    else:
        if "EQ_NO_TRANS_WORDS" not in wf:
            errors.append("eqNoTransWord 不再读取 EQ_NO_TRANS_WORDS（保护表被架空）")
        if "toUpperCase" not in wf:
            errors.append("eqNoTransWord 缺少 toUpperCase（大小写不同就漏判）")
        if "replace" not in wf:
            errors.append("eqNoTransWord 不再去掉空格（'Choice VN' 写成 'Choice  VN' 会漏判）")

    if nt is not None and "eqNoTransWord(t)" not in nt:
        errors.append("needTrans 缺少 eqNoTransWord(t) 豁免（Choice VN / T.L 会被发去联网翻译）")
    if to2 is not None and "eqNoTransWord(text)" not in to2:
        errors.append("transOf 缺少 eqNoTransWord(text) 防线（缓存里的译文会被套上去）")
    if rt2 is not None and "eqNoTransWord(text)" not in rt2:
        errors.append("requestTrans 缺少 eqNoTransWord(text) 拦截（仍会发翻译请求）")
    if at2 is not None and "eqNoTransWord(cell.v)" not in at2:
        errors.append("applyTrans 缺少 eqNoTransWord(cell.v) 跳过（显示端可能被换掉）")
    lt2 = fn_body(text, "loadTrans")
    if lt2 is not None and "eqNoTransWord(k)" not in lt2:
        errors.append("loadTrans 不再清理缓存里公司名/人名缩写的脏译文（历史错译会被复用）")

    return errors


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    html = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "choice_lite.html")
    if not os.path.exists(html):
        print("✗ 找不到文件: %s" % html)
        sys.exit(1)

    errors = check(html)
    print("检查目标: %s" % os.path.basename(html))
    if not errors:
        print("✓ 通过：股东权益报表「货币代码不翻译 + 表头三语写死 + 公司名人名不翻译」三条锁死契约未被破坏")
        print("   · %s：①②③④ + 自愈 + 双保险 全在" % DOC_ID)
        print("   · %s：中文表头 %s / 英文与越南文逐条非空 / eqHeadRec + 四处联动 全在"
              % (DOC2_ID, "、".join(HEAD_ZH)))
        print("   · %s：保护表 %s / eqNoTransWord + 四处联动 + 自愈 全在"
              % (DOC3_ID, " ".join(WORDS)))
        sys.exit(0)
    for e in errors:
        print("  ✗ 违规: %s" % e)
    print("✗ 失败：共 %d 处违规。这是「锁死」契约，禁止篡改；请恢复 %s 的四条不变量后再提交。"
          % (len(errors), DOC_ID))
    sys.exit(1)


if __name__ == "__main__":
    main()
