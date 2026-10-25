# -*- coding: utf-8 -*-
"""财务越南报表「三语并列」自动补全器（FIN-TRI-AUTO-20261013）

背景 / 为什么需要：
  前端只对「三语并列表」启用翻译视图 —— 判定规则（choice_lite.html
  fin_isTrilingualSheet）是：某张表在头 20 行内，至少有 3 处满足
  「第 c 列非空 且 第 c+10 列非空」(c = A..H)。
  只要上传的是普通单块报表（K/U 两块为空），所有表都被判为"非三语表"，
  前端就按设计原样显示、绝不翻译 —— 这就是"上传了新报表却不会自动翻译"的根因。

本模块做的事（上传后由 app.py 的 fin_init_report 自动调用）：
  1. 检测：逐表套用与前端完全相同的判定规则；
  2. 补全：把基础块 A–H 的文字按 ROLE 翻译/复制到 ZH(K–R) 与 EN(U–AB) 两块；
     —— 数值、日期、编号等"语言无关"内容按 ROLE=copy 原样复制，绝不翻译；
  3. 固定：译文来自持久缓存 finance_data/fin_trans_cache.json
     —— 缓存里已有的一律直接复用（不再调 API），只有【新增条目】才会真正请求翻译；
     译文同时固化进 xlsx 的 K/U 两块，即"离线版本"，下次换表无需重翻；
  4. 表名三语映射重写 finance_data/fin_sheet_titles.json。

★ 语言约定（与前端 fin_langOffset 硬绑定，不可改）：
    基础块 A–H = 越南语(vi) | K–R = 中文(zh) | U–AB = 英文(en)
  所以源报表必须是【越南语】版本；若上传中文/英文单块版，基础块会被当成 vi，
  届时「越南语」页签显示的是源语言本身，那属于数据侧问题，不是本模块的 bug。

★ 与本模块翻译链保持一致的另一份实现：_fin_build_trilingual.py（手工 CLI，
  已存在且保持可用；两者 ROLE / 偏移 / 缓存文件必须一致）。

CLI：
    python fin_trilingual.py            # 就地补全 finance_data/vn_report.xlsx
    python fin_trilingual.py --dry-run  # 只统计需要补多少格 / 要调多少次 API，不写文件
    python fin_trilingual.py 别的.xlsx  # 指定文件
"""
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
import urllib.parse
from copy import copy as _copy
from urllib.parse import quote
from urllib.request import Request, urlopen

import openpyxl
from openpyxl.styles import Color

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

BASE = os.path.dirname(os.path.abspath(__file__))
FIN_DIR = os.path.join(BASE, "finance_data")
FIN_REPORT_DEFAULT = os.path.join(FIN_DIR, "vn_report.xlsx")
CACHE_PATH = os.path.join(FIN_DIR, "fin_trans_cache.json")
TITLES_PATH = os.path.join(FIN_DIR, "fin_sheet_titles.json")
BACKUP_DIR = os.path.join(FIN_DIR, "backups")

# 源列 -> 角色（translate = 翻成 zh/en；copy = 原样复制）。
# ★必须与 _fin_build_trilingual.py 的 ROLE 完全一致：A(日期)/B(凭证号)/D-E-F(金额)/H(类别)
#   都是语言无关内容，只有 C(摘要) 与 G(备注) 需要翻译，A 列作为"序号"标题行偶有文字。
ROLE = {1: "translate", 2: "copy", 3: "translate", 4: "copy",
        5: "copy", 6: "copy", 7: "translate", 8: "copy"}
ZH_OFF, EN_OFF = 10, 20          # VI A–H | ZH K–R | EN U–AB
SCAN_COLS = 8                    # 基础块 = A..H
TRI_SHEET_ROWS = 20              # 判定只看前 20 行（与前端一致）
TRI_SHEET_NEED = 3               # 配对命中 >= 3 即判为三语并列表（与前端一致）
PRE_TRI_KEEP = 20                # 三语化前的备份最多保留 20 份

_DEEPL_ENDPOINT = "https://api-free.deepl.com/v2/translate"
_DEEPL_LANG = {"zh": "ZH", "en": "EN", "vi": "VI"}

_ENSURE_LOCK = threading.Lock()
_CACHE = None
_CACHE_DIRTY = False
_DEEPL_KEY = None


# ---------------------------------------------------------------- 翻译链
def _deepl_key():
    global _DEEPL_KEY
    if _DEEPL_KEY is None:
        _DEEPL_KEY = os.environ.get("DEEPL_API_KEY") or ""
        if not _DEEPL_KEY:
            try:
                kf = os.path.join(FIN_DIR, ".deepl_key")
                if os.path.isfile(kf):
                    with open(kf, encoding="utf-8") as fh:
                        _DEEPL_KEY = fh.read().strip()
            except Exception:
                _DEEPL_KEY = ""
    return _DEEPL_KEY


def _g_google(text, target):
    try:
        u = ("https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl="
             + quote(target) + "&dt=t&q=" + quote(text))
        req = Request(u, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode("utf-8"))
        return "".join(seg[0] for seg in (data[0] or []) if seg and seg[0])
    except Exception:
        return ""


def _g_deepl(text, target):
    key = _deepl_key()
    if not key:
        return ""
    try:
        body = urllib.parse.urlencode({"text": text, "target_lang": _DEEPL_LANG[target]}).encode("utf-8")
        req = Request(_DEEPL_ENDPOINT, data=body, method="POST")
        req.add_header("Authorization", "DeepL-Auth-Key " + key)
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
        req.add_header("User-Agent", "Mozilla/5.0")
        with urlopen(req, timeout=12) as r:
            j = json.loads(r.read().decode("utf-8"))
        return (j.get("translations") or [{}])[0].get("text") or ""
    except Exception:
        return ""


def _g_mymemory(text, target):
    """末备翻译源 MyMemory（免费、无 key、与 Google 不同服务）。源语言固定 vi。"""
    try:
        u = ("https://api.mymemory.translated.net/get?q=" + quote(text)
             + "&langpair=vi|" + quote(target))
        req = Request(u, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=12) as r:
            data = json.loads(r.read().decode("utf-8"))
        t = (data.get("responseData") or {}).get("translatedText") or ""
        if "MYMEMORY WARNING" in t or not t:
            return ""
        return t
    except Exception:
        return ""


def load_cache():
    global _CACHE
    if _CACHE is None:
        try:
            with open(CACHE_PATH, encoding="utf-8") as fh:
                _CACHE = json.load(fh) or {}
        except Exception:
            _CACHE = {}
    return _CACHE


def save_cache():
    global _CACHE_DIRTY
    if not _CACHE_DIRTY:
        return
    try:
        tmp = CACHE_PATH + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(_CACHE, fh, ensure_ascii=False, indent=1)
        os.replace(tmp, CACHE_PATH)
        _CACHE_DIRTY = False
    except Exception as e:
        sys.stderr.write("[fin_trilingual] cache save failed: %s\n" % e)


# ★★★ FIN-TOTAL-LABEL-LOCK-20261017（用户 2026-10-17：「全部的，改成：总计（锁定这个中文翻译）」）★★★
# 合计行标签的三语【写死】，绝不交给机器翻译：
#   谷歌词典把越南文 "TỔNG CỘNG" 译成「全部的」，于是越南报表 / 中国报表的 M 列（中文块）
#   全变成了「全部的」。这里在翻译链【最前面】直接返回锁定译文，并顺手把持久缓存里的旧值
#   改写过来 —— 以后无论重导、补译、增行，都不会再退回「全部的」。
# ★任何重构都不得移除这张表；要改合计行文案只能改这里。
TR_TOTAL_LOCK = {
    "zh": "总计",
    "en": "TOTAL",
    "vi": "TỔNG CỘNG",
}
# 视作「合计行标签」的原文（大小写不敏感；允许带一个结尾冒号）
TR_TOTAL_SRC = frozenset(x.upper() for x in (
    "TỔNG CỘNG", "Tổng cộng", "Tổng", "TOTAL", "TOTAL CỘNG",
    "全部的", "全部", "合计", "总计", "共計", "合計",
))


def _total_lock(text, target):
    """合计行标签 → 锁定的三语译文；不是合计标签则返回 None（照常走翻译链）。"""
    t = (text or "").strip()
    if not t:
        return None
    suffix = ""
    if t.endswith(":") or t.endswith("："):
        suffix = t[-1]
        t = t[:-1].strip()
    if t.upper() not in TR_TOTAL_SRC:
        return None
    base = TR_TOTAL_LOCK.get(target)
    return (base + suffix) if base else None


def gtrans(text, target, stats=None, dry_run=False):
    """三档翻译链 + 持久缓存。dry_run 时只统计不请求网络。"""
    global _CACHE_DIRTY
    text = (text or "").strip()
    if not text:
        return ""
    cache = load_cache()
    key = text + "|" + target
    # ★FIN-TOTAL-LABEL-LOCK-20261017：合计行标签必须在【缓存查询之前】就锁死，
    #   否则缓存里那条旧的「全部的」会一直被当成答案返回。
    _lk = _total_lock(text, target)
    if _lk:
        try:
            if cache.get(key) != _lk:
                cache[key] = _lk
                _CACHE_DIRTY = True
                save_cache()
        except Exception:
            pass
        if stats is not None:
            stats["cached"] += 1
        return _lk
    if key in cache:
        if stats is not None:
            stats["cached"] += 1
        return cache[key]
    if stats is not None:
        stats["new_text"] += 1
    if dry_run:
        if stats is not None:
            stats["api_calls"] += 1
        return ""
    t = ""
    for fn in (_g_google, _g_deepl, _g_mymemory):
        try:
            t = fn(text, target)
        except Exception:
            t = ""
        if t:
            break
    if stats is not None:
        stats["api_calls"] += 1
    if t:
        cache[key] = t
        _CACHE_DIRTY = True
    return t


# ---------------------------------------------------------------- 判定 / 补全
def is_trilingual_sheet(ws, rows=TRI_SHEET_ROWS, need=TRI_SHEET_NEED):
    """与前端 fin_isTrilingualSheet 完全同规则：
       头 rows 行内，c=A..H，第 c 列与第 c+10 列都非空 → 命中；命中共 need 次即为三语并列表。"""
    hits = 0
    last = min(rows, ws.max_row)
    for r in range(1, last + 1):
        for c in range(1, SCAN_COLS + 1):
            a = ws.cell(r, c).value
            b = ws.cell(r, c + ZH_OFF).value
            if a not in (None, "") and b not in (None, ""):
                hits += 1
                if hits >= need:
                    return True
    return False


def _load_titles():
    """读回现有的表名三语映射（用于保护人工校对过的名字）。"""
    try:
        with open(TITLES_PATH, encoding="utf-8") as fh:
            return json.load(fh) or {}
    except Exception:
        return {}


def report_is_trilingual(path):
    """整本是否已是"全表三语并列"。"""
    wb = openpyxl.load_workbook(path, read_only=True)
    try:
        return all(is_trilingual_sheet(ws) for ws in wb.worksheets)
    finally:
        try:
            wb.close()
        except Exception:
            pass


def _backup(path):
    try:
        os.makedirs(BACKUP_DIR, exist_ok=True)
        dst = os.path.join(BACKUP_DIR,
                           "vn_report_%s.pretri.xlsx" % time.strftime("%Y-%m-%d_%H%M%S"))
        if not os.path.isfile(dst):
            shutil.copyfile(path, dst)
        # 滚动保留最近 PRE_TRI_KEEP 份
        olds = sorted(f for f in os.listdir(BACKUP_DIR) if f.endswith(".pretri.xlsx"))
        for f in olds[:-PRE_TRI_KEEP]:
            try:
                os.remove(os.path.join(BACKUP_DIR, f))
            except OSError:
                pass
        return dst
    except Exception as e:
        sys.stderr.write("[fin_trilingual] backup failed: %s\n" % e)
        return None


# ---------------------------------------------------------------- 离线规范化
# ★为什么必须在"上传时就做"（FIN-DATE-NORM-20261013）：
#   前端财务页是只读的（choice_lite.html: FIN_READONLY = true），屏幕上做的任何
#   日期/样式规范化都不会落回文件。而"原始导出"里：
#     ① 日期数字格式是 en-US 的 mm-dd-yy（甚至还混杂 dd/mm/yyyy）；
#     ② 可能夹带历史遗留的「红+粗」高亮。
#   这两样会让前端的 finHiRecompute（每 2s 轮询 + 4s 自愈节流）与日期修正反复做
#   "内部写入"；而每次内部写入都会把 Univer 的 pushUndoRedo 静默最多 1.5s
#   （FIN-UNDO-CLEAN-20261012），于是表现为「撤销按钮按不动 / 撤掉的是看不见的格式」。
#   所以上传流水线里一次性做成"干净态"：与前端 finHiCleanup / finHiIsDateRow 同规则。
DDMMYYYY = "dd-mm-yyyy"
# 数字格式里出现日期特征才算"日期格式"（保守：避免把 #,##0 "m2" 之类误判）
_DATE_PAT_RE = re.compile(r"yy|dd|mmm|月|日", re.I)
# 文本日期： 2026-06-20 / 20-06-2026 / 20/06/2026（与前端 fin_parseDateText 覆盖面一致够用）
_TEXT_DATE_RE = re.compile(r"^\s*\d{1,4}[-/.]\d{1,2}[-/.]\d{1,4}")


def _is_date_value(v, numfmt):
    """这格是不是"日期"——与前端 finHiCellSerial 的口径保持一致（日期对象/日期格式数字/文本日期）。"""
    if isinstance(v, (datetime.datetime, datetime.date)):
        return True
    if isinstance(v, bool):
        return False
    if isinstance(v, (int, float)):
        return bool(_DATE_PAT_RE.search(str(numfmt or "")))
    if isinstance(v, str):
        return bool(_TEXT_DATE_RE.match(v))
    return False


def normalize_file(path, dry_run=False, logger=None):
    """① 所有日期格 → 数字格式 dd-mm-yyyy；② 清掉「日期行」里泄漏的红+粗。

    ★只动 A 列是日期的行（与前端 finHiCleanup 完全同规则）：
      "Ngân hàng VPbank / Tiền mặt 1 / Ngân hàng ACB Bank" 这类**银行小计/区域表头**行
      本身在原始报表里就是红+粗，它们不是日期行 → 绝不能被清掉（实测已确认）。
    只有确有改动才写盘，写盘前先在 backups/ 留一份 .pretri.xlsx。
    """
    log = logger if callable(logger) else (lambda *a: None)
    st = {"ok": False, "reason": "", "date_fmt": 0, "hl_clean": 0, "backup": None}
    try:
        wb = openpyxl.load_workbook(path)
    except Exception as e:
        st["reason"] = "load failed: %s" % e
        return st

    for ws in wb.worksheets:
        maxcol = min(max(ws.max_column, 1), SCAN_COLS + EN_OFF)      # 只扫 A..AB（三块）
        date_rows = []
        for r in range(1, ws.max_row + 1):
            a = ws.cell(r, 1)
            if _is_date_value(a.value, a.number_format):
                date_rows.append(r)
            for c in range(1, maxcol + 1):
                cc = ws.cell(r, c)
                if _is_date_value(cc.value, cc.number_format) and cc.number_format != DDMMYYYY:
                    if not dry_run:
                        cc.number_format = DDMMYYYY
                    st["date_fmt"] += 1
        for r in date_rows:
            for c in range(1, maxcol + 1):
                cc = ws.cell(r, c)
                f = cc.font
                try:
                    rgb = str(getattr(f.color, "rgb", "") or "").upper()
                except Exception:
                    rgb = ""
                if "FF0000" in rgb and f.bold:
                    if not dry_run:
                        nf = _copy(f)
                        try:
                            nf.color = Color(rgb="FF000000")
                        except Exception:
                            pass
                        nf.b = False
                        cc.font = nf
                    st["hl_clean"] += 1
                    log("    清泄漏高亮 %s r%d c%d" % (ws.title, r, c))

    if dry_run:
        st["ok"] = True
        st["reason"] = "dry-run"
        return st
    if not (st["date_fmt"] or st["hl_clean"]):
        st["ok"] = True
        st["reason"] = "already clean"
        return st
    st["backup"] = _backup(path)
    tmp = path + ".norm.tmp"
    try:
        wb.save(tmp)
        os.replace(tmp, path)
    except Exception as e:
        st["reason"] = "save failed: %s" % e
        try:
            os.remove(tmp)
        except OSError:
            pass
        return st
    st["ok"] = True
    st["reason"] = "normalized"
    return st


POSTFIX_SCRIPT = os.path.join(BASE, "_fin_fix_trilingual.py")


def run_postfix(src, logger=None):
    """★补齐「文字列」译文 —— 直接复用已经验证过的 _fin_fix_trilingual.py，不重写逻辑。

    为什么必须要有这一步：
      ROLE 是把「列角色」写死的（A/C/G 当文字列翻译，B/D/E/F 当"代号/数字"原样复制），
      但不同工作表列义不同 —— 汇总表 B 列是「内容说明」，应该是要翻译的，
      却被原样复制进 ZH/EN 块 → 前端把"译文＝原文"当成已有译文 → 主表格内容不翻译。
      _fin_fix_trilingual.py 换的是另一套判定：**任何字符串格都要有译文**
      （单号/代号如 NTTK00001 才原样复制），并同步刷新人工校对过的表名三语映射。
      它纯走持久缓存 fin_trans_cache.json → 已翻过的绝不重复联网，只翻真正的新文字。

    ★必须在 ROLE 补块【之后】调用：否则被 ROLE 复制成原文的格会反过来覆盖掉这一步的译文。
    """
    log = logger if callable(logger) else (lambda *a: None)
    st = {"ok": False, "reason": ""}
    if not os.path.isfile(POSTFIX_SCRIPT):
        st["reason"] = "postfix script missing"
        log("[fin_trilingual] 缺 %s，跳过文字列补翻" % POSTFIX_SCRIPT)
        return st
    try:
        r = subprocess.run([sys.executable, POSTFIX_SCRIPT, src, "--apply"],
                           cwd=BASE, capture_output=True, timeout=900)
        out = (r.stdout or b"").decode("utf-8", "replace")
        tail = [l.strip() for l in out.splitlines() if l.strip()][-3:]
        for l in tail:
            log("    " + l)
        st["ok"] = (r.returncode == 0)
        st["rc"] = r.returncode
        st["tail"] = tail
        if r.returncode != 0:
            st["reason"] = (r.stderr or b"").decode("utf-8", "replace")[-500:]
            log("[fin_trilingual] 文字列补翻失败: %s" % st["reason"])
    except Exception as e:
        st["reason"] = str(e)[:200]
        log("[fin_trilingual] 文字列补翻异常: %s" % st["reason"])
    return st


# ★脏值守卫（FIN-JUNK-GUARD-20261015）：源列里的 Excel 错误值(#NAME?/#VALUE!，含被机翻成
#   「＃姓名？」的残渣)绝不能被翻译、也不该镜像进 ZH/EN 块；纯数字(如摘要列里的 0)也不该
#   灌进文字列 —— 否则中文/英文块的「摘要」会显示成 0 或乱码。日期(datetime)仍按原样镜像。
_ERR_TEXT_RE = re.compile(r'^\s*[#＃].*[?!？!]\s*$')


def _is_junk_error_text(v):
    return isinstance(v, str) and bool(_ERR_TEXT_RE.match(v.strip()))


def ensure_report(path=None, dry_run=False, logger=None, probe=True):
    """就地补全三语两块。返回统计 dict（ok/reason/...），异常不外抛。

    · 已缓存译文不再调 API —— 「下次就不用再翻译了，只对新增条目翻译」靠这个实现；
    · 只有确有格子需要改动时才写盘（并先在 backups/ 留一份 .pretri.xlsx）；
    · 翻译 API 不可达时【不碰文件】，只返回 reason，避免把源文当译文灌进 K/U。
    """
    path = path or FIN_REPORT_DEFAULT
    log = logger if callable(logger) else (lambda *a: None)
    stats = {"ok": False, "path": path, "reason": "", "dry_run": bool(dry_run),
             "sheets": 0, "sheets_tri": 0, "cells_set": 0,
             "cached": 0, "new_text": 0, "api_calls": 0, "backup": None,
             "date_fmt": 0, "hl_clean": 0}

    if not os.path.isfile(path):
        stats["reason"] = "file not found"
        return stats

    def _merge_norm(nst):
        stats["date_fmt"] += nst.get("date_fmt", 0)
        stats["hl_clean"] += nst.get("hl_clean", 0)
        stats["normalize"] = nst.get("reason")
        if nst.get("date_fmt") or nst.get("hl_clean"):
            log("[fin_trilingual] 规范化：日期格式 %d 格 / 清泄漏高亮 %d 格"
                % (nst.get("date_fmt", 0), nst.get("hl_clean", 0)))

    with _ENSURE_LOCK:
        # ★三语补全的连通性预检：不通就只做离线规范化，绝不把源文当译文灌进 K/U
        if probe and not dry_run:
            if not gtrans("test", "en", None, False):
                _merge_norm(normalize_file(path, dry_run=dry_run, logger=logger))
                stats["reason"] = "translate api unreachable (normalize only)"
                stats["ok"] = bool(stats["date_fmt"] or stats["hl_clean"])
                log("[fin_trilingual] 翻译 API 不可达：只做离线规范化，不补三语")
                return stats

        try:
            wb = openpyxl.load_workbook(path)
        except Exception as e:
            stats["reason"] = "load failed: %s" % e
            return stats

        # ★保留已有人工校对过的表名（机器翻译绝不能覆盖它）——只对"映射里还没有"的表名做翻译。
        titles = dict(_load_titles())
        all_tri = True
        for ws in wb.worksheets:
            tri = is_trilingual_sheet(ws)
            if not tri:
                all_tri = False
            src_cols = [c for c in range(1, SCAN_COLS + 1)
                        if any(ws.cell(r, c).value not in (None, "")
                               for r in range(1, min(ws.max_row, 400) + 1))]
            if not src_cols:
                continue
            stats["sheets"] += 1
            max_r = ws.max_row
            for c in src_cols:
                role = ROLE.get(c, "copy")
                zc, ec = c + ZH_OFF, c + EN_OFF
                for r in range(1, max_r + 1):
                    v = ws.cell(r, c).value
                    if v is None or v == "":
                        continue
                    if role == "copy" or not isinstance(v, str):
                        # ★不把「纯数字」(摘要列里的 0 等)灌进 ZH/EN 文字列；日期/时间仍照镜像。
                        if role == "translate" and not isinstance(v, (datetime.datetime, datetime.date)):
                            continue
                        wz = we = v
                    else:
                        # ★Excel 错误值(#NAME?/#VALUE!/被机翻的 ＃姓名？)绝不翻译、也不镜像。
                        if _is_junk_error_text(v):
                            continue
                        wz = gtrans(v, "zh", stats, dry_run) or v
                        we = gtrans(v, "en", stats, dry_run) or v
                    cell = ws.cell(r, zc)
                    if cell.value != wz:
                        if not dry_run:
                            cell.value = wz
                        stats["cells_set"] += 1
                    cell = ws.cell(r, ec)
                    if cell.value != we:
                        if not dry_run:
                            cell.value = we
                        stats["cells_set"] += 1
            if not dry_run:
                old = titles.get(ws.title)
                if old and old.get("zh") and old.get("en"):
                    log("  表 %s -> 沿用已校对映射 zh=%s / en=%s"
                        % (ws.title, old.get("zh"), old.get("en")))
                else:
                    titles[ws.title] = {
                        "vi": ws.title,
                        "zh": gtrans(ws.title, "zh", stats, False) or ws.title,
                        "en": gtrans(ws.title, "en", stats, False) or ws.title,
                    }
                    log("  表 %s -> zh=%s / en=%s" % (ws.title,
                                                      titles[ws.title]["zh"], titles[ws.title]["en"]))

        stats["was_trilingual"] = all_tri
        stats["sheets_tri"] = sum(1 for ws in wb.worksheets if is_trilingual_sheet(ws))

        if dry_run:
            stats["ok"] = True
            stats["reason"] = "dry-run"
            return stats

        if stats["cells_set"]:
            stats["backup"] = _backup(path)
            tmp = path + ".tri.tmp"
            try:
                wb.save(tmp)
                os.replace(tmp, path)
            except Exception as e:
                stats["reason"] = "save failed: %s" % e
                try:
                    os.remove(tmp)
                except OSError:
                    pass
                return stats
        else:
            stats["reason"] = "nothing to fill"

        if titles:
            try:
                tmp = TITLES_PATH + ".tmp"
                with open(tmp, "w", encoding="utf-8") as fh:
                    json.dump(titles, fh, ensure_ascii=False, indent=1)
                os.replace(tmp, TITLES_PATH)
            except Exception as e:
                sys.stderr.write("[fin_trilingual] titles save failed: %s\n" % e)
        save_cache()

        # ★② 补齐「文字列」译文（汇总表内容说明列等）—— 必须在 ROLE 补块之后，见 run_postfix 说明
        stats["postfix"] = run_postfix(path, log)

        # ★① 离线规范化放在三语补全【之后】：补 K/U 时把 datetime 写进去，openpyxl 会给
        #   它们默认的 "yyyy-mm-dd h:mm:ss"；必须在这之后再统一成 dd-mm-yyyy，
        #   否则三个语言块里有两块的日期格式不一致（前端日期解析/比较会看不一致）。
        _merge_norm(normalize_file(path, dry_run=dry_run, logger=logger))

        stats["ok"] = True
        if not stats["reason"]:
            stats["reason"] = "filled"
        # 补全后再判定一次，作为"前端会不会认三语"的最终依据
        try:
            stats["sheets_tri"] = sum(1 for ws in openpyxl.load_workbook(path, read_only=True).worksheets
                                      if is_trilingual_sheet(ws))
        except Exception:
            pass
        log("[fin_trilingual] 完成：表=%d 补格=%d 新增文本=%d API=%d 缓存命中=%d 备份=%s"
            % (stats["sheets"], stats["cells_set"], stats["new_text"],
               stats["api_calls"], stats["cached"], stats["backup"]))
        return stats


def main():
    args = [a for a in sys.argv[1:]]
    dry = "--dry-run" in args
    no_probe = "--no-probe" in args
    rest = [a for a in args if not a.startswith("--")]
    path = rest[0] if rest else FIN_REPORT_DEFAULT

    def _p(*a):
        print(*a)

    st = ensure_report(path, dry_run=dry, logger=_p, probe=not no_probe)
    print("-" * 60)
    for k in ("ok", "path", "reason", "normalize", "date_fmt", "hl_clean",
              "sheets", "sheets_tri", "cells_set",
              "cached", "new_text", "api_calls", "backup"):
        if k in st:
            print("%-14s %s" % (k, st[k]))


if __name__ == "__main__":
    main()
