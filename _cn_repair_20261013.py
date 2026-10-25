# -*- coding: utf-8 -*-
"""中国报表一次性修复（FIN-CN-REPAIR-20261013）。

修两处【数据】问题（代码根因已在 app.py / choice_lite.html 修掉）：
  ① 英文块（U–AB）里装的是中文 → 英文视图永远显示中文。按「中文块(=用户原始数据)」为源，
     重新翻出英文写回英文块；顺带补全空缺的语言块。语言无关内容（单号/数字）三块同步复制。
  ② 金额列是【文本】('41,400,000\xa0') → 数字格式对它不生效，¥ 永远显示不出来。
     交给 app._cn_normalize_money_fmt 转成数字并套 "¥"#,##0。

★先备份再改；只动文字块的值与金额格式，不动任何结构。
用法：
    python _cn_repair_20261013.py            # 演练（只统计，不写盘）
    python _cn_repair_20261013.py --apply    # 真正修复（先备份）
"""
import io
import json
import os
import re
import shutil
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import openpyxl  # noqa: E402

OUT = io.open(os.path.join(HERE, "_cn_repair_out.txt"), "w", encoding="utf-8", newline="\n")


def log(s):
    OUT.write(str(s) + "\n")
    print(s)


APPLY = "--apply" in sys.argv
ZH_OFF, EN_OFF = 10, 20
SCAN_COLS = 8
CACHE_PATH = os.path.join(HERE, "finance_data", "fin_trans_cache.json")

_CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
_NUMLIKE_RE = re.compile(r"^[\d\s.,%\-+()/:]+$")
_CODE_RE = re.compile(r"^[A-Z0-9][A-Z0-9\-_./]*$")


def has_cjk(s):
    return bool(_CJK_RE.search(str(s or "")))


def is_code_like(s):
    """单号/代号/纯数字：语言无关，不翻译，三块原样复制（与前端 fin_isCodeLike 同口径）。"""
    t = str(s or "").strip()
    if not t:
        return True
    if _NUMLIKE_RE.match(t):
        return True
    if " " not in t and re.search(r"\d", t) and re.search(r"[A-Za-zÀ-ỹ]", t):
        return True
    if _CODE_RE.match(t):
        return True
    return False


def looks_like(cand, lang, src):
    """与前端 fin_transLooksLike 完全同规则（改一处必须同时改另一处）。"""
    c = str(cand or "")
    if not c.strip():
        return False
    if c == src:
        return False
    if lang == "en":
        return not has_cjk(c)
    if lang == "zh":
        return has_cjk(c)
    return True


def main():
    import app
    path = app.CN_REPORT
    log("目标文件: %s" % path)
    if not os.path.isfile(path):
        log("文件不存在，结束")
        return

    # 持久译文缓存：能命中就不联网（与 fin_trilingual 共用同一个文件）
    cache = {}
    try:
        cache = json.load(io.open(CACHE_PATH, encoding="utf-8")) or {}
    except Exception:
        cache = {}
    log("持久译文缓存条目 = %d" % len(cache))

    def gtrans(text, target):
        key = text + "|" + target
        if key in cache and cache[key]:
            return cache[key]
        t = app.fin_translate(text, target)
        if t:
            cache[key] = t
        return t or ""

    wb = openpyxl.load_workbook(path)
    ws = wb[app.CN_SHEET_NAME] if app.CN_SHEET_NAME in wb.sheetnames else wb[wb.sheetnames[0]]
    log("工作表 = %s  尺寸 = %s  max_row = %d" % (ws.title, ws.dimensions, ws.max_row))

    plan = []   # (r, c, kind, old, new)
    for r in range(1, ws.max_row + 1):
        for c in range(1, SCAN_COLS + 1):
            vi = ws.cell(r, c).value
            zh = ws.cell(r, c + ZH_OFF).value
            en = ws.cell(r, c + EN_OFF).value
            texts = [x for x in (vi, zh, en) if isinstance(x, str) and x.strip()]
            if not texts:
                continue
            # 源文字：优先"看起来是中文"的块（用户原始数据），否则越南文块
            src = None
            if isinstance(zh, str) and has_cjk(zh):
                src = zh.strip()
            elif isinstance(vi, str) and vi.strip():
                src = vi.strip()
            elif isinstance(zh, str) and zh.strip():
                src = zh.strip()
            if not src:
                continue
            if is_code_like(src):
                for off, cur in ((0, vi), (ZH_OFF, zh), (EN_OFF, en)):
                    if cur is None or (isinstance(cur, str) and not cur.strip()):
                        plan.append((r, c + off, "copy", cur, src))
                continue
            # 英文块不合适 → 重翻英文
            if not looks_like(en, "en", src):
                new_en = gtrans(src, "en") or ""
                # ★中文块里夹着少量汉字时（如 'Pay Spring 和 HT LLC'），翻译链会认为"已经是英文"
                #   原样返回 → 英文块继续带汉字。这时改用【越南文块】为源再翻一次（'và'→'and'）。
                if has_cjk(new_en) and isinstance(vi, str) and vi.strip() and not has_cjk(vi):
                    alt = gtrans(vi.strip(), "en") or ""
                    if alt and not has_cjk(alt):
                        new_en = alt
                plan.append((r, c + EN_OFF, "en", en, new_en))
            # 中文块不合适 → 重翻中文
            if not looks_like(zh, "zh", src):
                plan.append((r, c + ZH_OFF, "zh", zh, gtrans(src, "zh") or ""))
            # 越南语块空 → 从源补越南文
            if vi is None or (isinstance(vi, str) and not vi.strip()):
                plan.append((r, c, "vi", vi, gtrans(src, "vi") or ""))

    plan = [p for p in plan if p[4] and str(p[4]).strip() and str(p[4]) != str(p[3])]
    log("-" * 60)
    log("计划修复格数 = %d" % len(plan))
    by_kind = {}
    for p in plan:
        by_kind[p[2]] = by_kind.get(p[2], 0) + 1
    log("按类型: %r" % by_kind)
    for p in plan[:12]:
        log("   r%-4d c%-3d %-4s %r -> %r" % p)

    if not APPLY:
        log("\n（演练模式，未写盘。加 --apply 才真正修复）")
        return

    bak = os.path.join(HERE, "finance_data", "backups",
                       "cn_report_%s_before_repair.xlsx.bak" % time.strftime("%Y%m%d_%H%M%S"))
    shutil.copy2(path, bak)
    log("已备份 -> %s" % bak)

    for (r, c, kind, old, new) in plan:
        ws.cell(r, c).value = new
    wb.save(path)
    log("已写回译文修复：%d 格" % len(plan))

    if cache:
        try:
            tmp = CACHE_PATH + ".tmp"
            json.dump(cache, io.open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            os.replace(tmp, CACHE_PATH)
            log("持久译文缓存已更新 -> %d 条" % len(cache))
        except Exception as e:
            log("缓存写盘失败: %r" % e)

    # ★金额（文本→数字 + ¥#,##0）与黑色网格线、数据区蓝字、核销列居中
    log("-" * 60)
    log("执行中国报表外观归一化（金额/网格线/蓝字/居中）…")
    changed = app._cn_normalize_style()
    log("_cn_normalize_style() = %s" % changed)
    try:
        app._cn_cache_invalidate()
        log("旧快照缓存已失效")
    except Exception as e:
        log("快照缓存失效失败: %r" % e)


main()
OUT.close()
