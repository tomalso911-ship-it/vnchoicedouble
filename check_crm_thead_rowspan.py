# -*- coding: utf-8 -*-
"""CRM-THEAD-ROWSPAN-20261114 静态不变量检查（不启动浏览器，秒级完成）

背景：CRM 表两级表头已从「tbody 伪表头行」改为「thead 内真两级合并」：
  一级 <tr class="won-thead">   无子列的格子 rowspan="2"，分组格子 colspan="N"
  二级 <tr class="won-subthead"> 只含分组子列（汇率 2 / Q1-Q7 各 3 / PDF 3）

检查项：
  1. renderCrmThead 尾部拼接 renderCrmFakeSubHeaderRow()（二级行在 thead 内）
  2. renderCrmData 不再把二级行渲染进 tbody
  3. hdr() 对 colspan==1 的格子输出 rowspan="2"
  4. 一级表头 colspan 之和 == 48
  5. 二级行只渲染 _crmHasSubCell 为真的列，且列数 == 26
  6. 22 个 rowspan 列 + 26 个二级列 == 48（守恒，缺一列整表错位）
  7. patchCrmFakeHeaderRowTextOnly 改的是 #crmThead 里的 tr.won-subthead
  8. syncCrmColVisibility 只放过一级行 th，二级行 th 必须随数据列隐藏
  9. index.html 有 #crmTable thead tr.won-subthead th 的 sticky 规则（top 用 --crm-th1-h）
"""
import io
import os
import re
import sys

try:                      # Windows 控制台默认 cp1252，中文输出会 UnicodeEncodeError
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = os.path.dirname(os.path.abspath(__file__))
JS = os.path.join(ROOT, "crm_table.js")
HTML = os.path.join(ROOT, "index.html")

fails = []


def ok(cond, msg):
    if cond:
        print("  [OK] " + msg)
    else:
        fails.append(msg)
        print("  [FAIL] " + msg)


def read(path):
    with io.open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def main():
    js = read(JS)
    html = read(HTML)

    print("== 1. 二级行属于 thead ==")
    m = re.search(r"function renderCrmThead\(\)[\s\S]*?\n\}\n", js)
    ok(bool(m), "找到 renderCrmThead")
    body = m.group(0) if m else ""
    ok("renderCrmFakeSubHeaderRow()" in body, "renderCrmThead 末尾拼接二级表头行")
    ok("won-subthead" in js, "二级行 class 为 won-subthead")

    print("== 2. tbody 不再含伪表头行 ==")
    rd = re.search(r"function renderCrmData\(list\)[\s\S]*?\n  list\.forEach", js)
    ok(bool(rd) and "renderCrmFakeSubHeaderRow()" not in (rd.group(0) if rd else ""),
       "renderCrmData 不再渲染二级表头")
    ok('html = \'\'' in js, "renderCrmData 以空字符串起头")

    print("== 3. rowspan 输出 ==")
    ok('rowspan="2"' in body, "hdr() 输出 rowspan=\"2\"")
    ok("(cs === 1) ? ' rowspan=\"2\"'" in js, "仅 colspan==1 的格子加 rowspan")

    print("== 4/6. 列数守恒 ==")
    cols = re.findall(r"hdr\(\s*(\d+)\s*,[^,]*,\s*'[^']*'\s*,\s*(\d+)\s*,", body)
    total, rowspan_cols, group_cols = 0, 0, 0
    for c, cs in cols:
        cs = int(cs)
        total += cs
        if cs == 1:
            rowspan_cols += 1
        else:
            group_cols += 1
    ok(total == 48, "一级表头 colspan 之和 = %d（应为 48）" % total)
    ok(rowspan_cols == 22, "一级 rowspan 格数 = %d（应为 22）" % rowspan_cols)
    ok(group_cols == 9, "一级分组格数 = %d（应为 9：汇率 1 + Q1-Q7 共 7 + PDF 1）" % group_cols)
    sub_cols = total - rowspan_cols
    ok(sub_cols == 26, "二级列数（由一级推得）= %d（应为 26）" % sub_cols)
    ok(rowspan_cols + sub_cols == 48, "22 + 26 = 48 列守恒")

    print("== 5. _crmHasSubCell 覆盖范围 ==")
    hs = re.search(r"function _crmHasSubCell\(i\)\s*\{([\s\S]*?)\}", js)
    ok(bool(hs), "找到 _crmHasSubCell")
    hsbody = hs.group(1) if hs else ""
    expect = set([17, 18]) | set(range(20, 41)) | set([42, 43, 44])
    covered = set()
    for a, b in re.findall(r"i >= (\d+) && i <= (\d+)", hsbody):
        covered |= set(range(int(a), int(b) + 1))
    covered |= set(int(x) for x in re.findall(r"i === (\d+)", hsbody))
    ok(covered == expect,
       "_crmHasSubCell 覆盖 17/18/20-40/42-44（差集 %s）" % (sorted(covered ^ expect),))
    ok(len(covered) == 26, "二级子列集合 = 26 列")

    print("== 7. 二级行文本补丁 ==")
    p = re.search(r"function patchCrmFakeHeaderRowTextOnly\(\)[\s\S]*?\n\}\n", js)
    pb = p.group(0) if p else ""
    ok("crmThead" in pb, "补丁作用于 #crmThead")
    ok("tr.won-subthead" in pb, "补丁定位 tr.won-subthead")
    ok("_crmParseFragment" not in pb, "补丁不再解析 HTML（<tr> 在 template 里会被丢弃）")

    print("== 8. 列隐藏：二级行必须同步 ==")
    s = re.search(r"function syncCrmColVisibility\(\)[\s\S]*?\n\}\n", js)
    sb = s.group(0) if s else ""
    ok("won-thead" in sb, "只放过一级行 th（won-thead）")
    ok("tr.won-thead > th[data-col=" in sb, "组头按 tr.won-thead 精确定位")

    print("== 9. index.html 样式规则 ==")
    ok("#crmTable thead tr.won-subthead th" in html, "存在二级行 sticky 规则")
    ok("top: var(--crm-th1-h, 22px)" in html, "二级行 top 使用实测变量 --crm-th1-h")
    ok("#crmTable thead tr.won-thead th[rowspan]" in html, "rowspan 格 2px 收口线")
    ok("_crmSyncTheadHeight" in js, "存在 _crmSyncTheadHeight 实测函数")
    ok('build 2026-11-14-Z124' in html, "PERM_BUILD 已递增（crm_table.js 缓存破坏）")

    print("")
    if fails:
        print("RESULT: FAIL (%d)" % len(fails))
        for f in fails:
            print("   - " + f)
        return 1
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
