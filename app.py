# ⛔ FROZEN (2026-09-06) V2026.09.06.20：本文件逻辑已锁定，未经用户明确同意禁止修改。本地后端逻辑均正确，仅 CRM/LOST/WON/个人佣金 数据可为演示数据。
# -*- coding: utf-8 -*-
"""
AGI-CRM · Won（签约项目）后端
- 仅保留与 index.html（签约项目页）相关的 won_projects 一张表
- 无认证、无用户体系、无 CRM/Lost/报价单/审批/汇率历史/省份等无关内容
- 提供 4 个纯数据 API：GET/POST/PUT/DELETE /api/won-projects
- 附件上传/删除、补充协议摘要保存
- 静态托管 index.html（端口 5050，与前端 fetch 地址一致）
"""

import os
import io
import sys
import json
import hashlib
import sqlite3
import time
import shutil
import mimetypes
import subprocess
import struct
from datetime import datetime, timedelta
import re
import copy
import openpyxl
from flask import Flask, request, jsonify, send_from_directory, Response, redirect
from flask_cors import CORS

# Windows 控制台默认 cp1252 无法打印中文，统一改用 UTF-8，避免中文 print 崩溃
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# ===================== 配置 =====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = BASE_DIR
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
VAULT_DIR = os.path.join(UPLOAD_DIR, "vault")  # 私密空间（tom 专属）独立子目录
DB_PATH = os.path.join(DATA_DIR, "agi_pm.db")

# ⛔ 锁死注释之外：桌面版（PyInstaller 打包）专用分支，仅 sys.frozen 时生效，
# 不影响 `python app.py` 本地开发模式。数据落到用户可写目录，前端从解包目录读取。
if getattr(sys, "frozen", False):
    _appdata = os.environ.get("APPDATA") or os.path.expanduser("~")
    _data = os.path.join(_appdata, "AGI-PM")
    os.makedirs(_data, exist_ok=True)
    BASE_DIR = sys._MEIPASS
    DATA_DIR = _data
    UPLOAD_DIR = os.path.join(DATA_DIR, "uploads")
    VAULT_DIR = os.path.join(UPLOAD_DIR, "vault")
    DB_PATH = os.path.join(DATA_DIR, "agi_pm.db")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(VAULT_DIR, exist_ok=True)
LIB_DIR = os.path.join(UPLOAD_DIR, "library")
os.makedirs(LIB_DIR, exist_ok=True)

# ===================== 私密空间（Vault）配置 =====================
# 仅 tom 一人可使用；PIN 为 4 位密码，输对后服务端签发有时效的 token。
VAULT_OWNER = "tom"
VAULT_PIN = "1116"
VAULT_TOKEN_TTL = 30 * 60  # token 有效期（秒）：30 分钟
VAULT_TOKEN_BYTES = 24
# 防爆破：同一窗口连续错误次数限制（错误 5 次锁 60 秒）
VAULT_MAX_FAIL = 5
VAULT_LOCK_SECONDS = 60
# 私密空间：仅拦截真正危险的可执行文件，其余任意类型均可上传
VAULT_BLOCKED_EXT = {".exe", ".bat", ".cmd", ".com", ".scr", ".msi", ".sh", ".js", ".vbs", ".ps1", ".jar", ".dll"}
_vault_fail = {"count": 0, "lock_until": 0.0}
_vault_tokens = {}  # {token: expiry_ts}
# 私密空间上传容量：刻意不做任何限制（不设 MAX_CONTENT_LENGTH），任意大小文件均可上传。
# 如需限制请显式设置 app.config['MAX_CONTENT_LENGTH']，默认保持无限制。

# ============================================================================
# 演示模式开关（★ 培训结束后上线前必须改为 False ★）
# ----------------------------------------------------------------------------
# True  = 开发/培训/演示模式：三张业务表（crm_projects / won_projects /
#         approval_requests）为空时，自动注入示例数据，方便演示与教学。
# False = 生产模式：表为空时不注入任何示例数据。
#
# 【为什么要这个开关】
# init_db() 在表为空时会自动播种，如果不关掉，清空测试记录后只要重启服务，
# 示例数据就会"复活"（CRM 30 条 + 签约项目 + 审批 6 条），导致永远清不干净。
#
# 【当前状态】
#   默认 False：系统启动后 CRM/LOST/WON/审批 均为空，只保留真实用户。
#   需要演示时，在「用户与授权」页点黑色【DEMO】按钮即可一键还原全部示例数据。
#   （DEMO 按钮走 /api/demo/load，不依赖本开关）
#
# 【培训结束上线步骤】
#   1. 备份数据库：copy agi_pm.db agi_pm_backup_日期.db
#   2. 运行清理脚本：python reset_demo_data.py   （清空示例数据 + 移除 DEMO 按钮）
#   3. 重启服务：python app.py
# 详见 reset_demo_data.py 顶部说明。
# ============================================================================
DEMO_SEED = False

# ============================================================================
# 真实用户 vs 示例用户（DEMO 按钮机制的基础）
# ----------------------------------------------------------------------------
# 【需求背景】
#  系统需要两套状态：
#    · 日常/生产态 —— 只有真实用户 + 真实业务数据（学员录入的），示例数据全无
#    · 演示/培训态 —— 一键还原完整的示例数据（含示例用户、示例项目、示例审批）
#  培训结束后，再一键清空所有示例数据，正式投入使用。
#
# 【定义】
#  REAL_USERS      ：团队真实账号。永远保留，DEMO 不影响他们，
#                    清理脚本也绝不删除。
#  DEMO_USERNAMES  ：演示用假账号。由 DEMO 按钮从 demo_snapshot.json 还原，
#                    由「重置/清理」按名单精确删除。
# ============================================================================
REAL_USERS = ["tom", "alice", "admin", "cuong", "james", "travis", "ali", "linh", "khoa"]
DEMO_USERNAMES = [
    "minh", "salesdir1", "salesdir2", "gm1", "gm2", "dgm1", "dgm2",
    "obs1", "obs2", "fin1", "fin2", "asst1", "hr1",
]
# 业务表：DEMO 清空/还原的范围
DEMO_TABLES = ["crm_projects", "lost_projects", "won_projects", "approval_requests"]
# 快照文件：由 export_demo_snapshot.py 生成（对当前演示状态拍照）
DEMO_SNAPSHOT = os.path.join(DATA_DIR, "demo_snapshot.json")

app = Flask(__name__)
CORS(app)

# ===================== 权限变更实时推送（轻量级版本号机制）=====================
# 每个用户的权限/角色/状态发生变更时，bump 其版本号。
# 前端轮询 /api/perm-version?username= 检测版本变化，变化时立即刷新本地会话缓存，
# 实现「审批通过立即回写前端缓存（无需重新登录）」与「被改权限用户页面实时更新」。
PERM_VERSION = {}   # {username: int}
_PERM_VERSION_LOCK = None

def bump_perm_version(username):
    """刷新某用户的权限版本号（线程安全）。"""
    if not username:
        return
    import threading
    global _PERM_VERSION_LOCK
    if _PERM_VERSION_LOCK is None:
        _PERM_VERSION_LOCK = threading.Lock()
    with _PERM_VERSION_LOCK:
        PERM_VERSION[username] = PERM_VERSION.get(username, 0) + 1

def get_perm_version(username):
    return PERM_VERSION.get(username, 0)

def _norm_approver_list(approvers, conn):
    """把审批人列表统一规范为用户名。兼容前端旧 bug 中存的数字 ID。
    返回：去重后的用户名列表（只保留能解析到有效用户的）。"""
    if not isinstance(approvers, list):
        return []
    by_id = {}
    by_name_lower = {}
    for r in conn.execute("SELECT id, username, status FROM users").fetchall():
        by_id[r["id"]] = r["username"]
        by_name_lower[r["username"].lower()] = r["username"]
    seen = set()
    out = []
    for v in approvers:
        if v is None:
            continue
        s = str(v).strip()
        if not s:
            continue
        # 纯数字 -> 按 id 解析
        if s.isdigit():
            uname = by_id.get(int(s))
        else:
            uname = by_name_lower.get(s.lower())
        if not uname:
            continue
        if uname not in seen:
            seen.add(uname)
            out.append(uname)
    return out

def _norm_user_perms(perms, conn):
    """规范化 users.perms JSON 中所有区块的 approvers（数字 ID -> 用户名）。"""
    if not isinstance(perms, dict):
        return perms
    for bid, p in list(perms.items()):
        if not isinstance(p, dict):
            continue
        arr = p.get("approvers")
        if isinstance(arr, list):
            p["approvers"] = _norm_approver_list(arr, conn)
    return perms

def _migrate_approver_ids_to_usernames(c):
    """一次性迁移：users.perms 与 approval_requests.approvers 中的数字 ID -> 用户名。"""
    import json as _json
    by_id = {r["id"]: r["username"] for r in c.execute("SELECT id, username FROM users").fetchall()}
    # 修复 users.perms
    for row in c.execute("SELECT id, perms FROM users WHERE perms IS NOT NULL AND perms <> ''").fetchall():
        try:
            perms = _json.loads(row["perms"])
        except Exception:
            continue
        if not isinstance(perms, dict):
            continue
        changed = False
        for bid, p in list(perms.items()):
            if not isinstance(p, dict):
                continue
            arr = p.get("approvers")
            if isinstance(arr, list):
                new_arr = []
                seen = set()
                for v in arr:
                    s = str(v).strip()
                    if s.isdigit():
                        uname = by_id.get(int(s))
                        if uname and uname not in seen:
                            new_arr.append(uname); seen.add(uname)
                    elif s and s not in seen:
                        new_arr.append(s); seen.add(s)
                if new_arr != arr:
                    p["approvers"] = new_arr
                    changed = True
        if changed:
            c.execute("UPDATE users SET perms=? WHERE id=?", (_json.dumps(perms, ensure_ascii=False), row["id"]))
            print(f"[migrate] users.id={row['id']} perms 审批人已规范化为用户名")
    # 修复 approval_requests.approvers
    for row in c.execute("SELECT id, approvers FROM approval_requests WHERE approvers IS NOT NULL AND approvers <> ''").fetchall():
        try:
            arr = _json.loads(row["approvers"])
        except Exception:
            continue
        if not isinstance(arr, list):
            continue
        new_arr = []
        seen = set()
        for v in arr:
            s = str(v).strip()
            if s.isdigit():
                uname = by_id.get(int(s))
                if uname and uname not in seen:
                    new_arr.append(uname); seen.add(uname)
            elif s and s not in seen:
                new_arr.append(s); seen.add(s)
        if new_arr != arr:
            c.execute("UPDATE approval_requests SET approvers=? WHERE id=?", (_json.dumps(new_arr, ensure_ascii=False), row["id"]))
            print(f"[migrate] approval_requests.id={row['id']} 审批人已规范化为用户名")

# ===================== 数据库 =====================
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ===================== 自动备份（防数据丢失） =====================
# 用 SQLite 在线备份 API 生成一致性快照，滚动保留最近 N 份。
# 触发时机：服务启动、每次生产工厂保存后（节流）、手动点击。
AUTO_BACKUP_DIR = os.path.join(BASE_DIR, "backups", "auto")
_AUTO_BACKUP_STATE = {"ts": 0.0}


def _auto_backup_db(reason="auto", keep=80, min_interval=0):
    """生成 agi_pm.db 的一致性备份到 backups/auto/，返回备份文件路径（失败返回 None）。"""
    try:
        now = time.time()
        if min_interval and (now - _AUTO_BACKUP_STATE["ts"]) < min_interval:
            return None
        os.makedirs(AUTO_BACKUP_DIR, exist_ok=True)
        stamp = time.strftime("%Y%m%d_%H%M%S")
        safe = re.sub(r"[^0-9A-Za-z_\-]", "_", str(reason))[:40]
        fn = os.path.join(AUTO_BACKUP_DIR, "agi_pm_%s_%s.db" % (stamp, safe))
        src = sqlite3.connect(DB_PATH)
        dst = sqlite3.connect(fn)
        try:
            with dst:
                src.backup(dst)
        finally:
            dst.close()
            src.close()
        _AUTO_BACKUP_STATE["ts"] = now
        # 滚动删除最旧的备份，避免无限增长
        try:
            files = [f for f in os.listdir(AUTO_BACKUP_DIR)
                     if f.startswith("agi_pm_") and f.endswith(".db")]
            files.sort(key=lambda x: os.path.getmtime(os.path.join(AUTO_BACKUP_DIR, x)))
            for old in files[:-keep]:
                try:
                    os.remove(os.path.join(AUTO_BACKUP_DIR, old))
                except Exception:
                    pass
        except Exception:
            pass
        print("[auto_backup] %s -> %s" % (reason, fn))
        return fn
    except Exception as e:
        try:
            print("[auto_backup] failed(%s): %s" % (reason, e))
        except Exception:
            pass
        return None


def row_to_dict(row):
    d = dict(row)
    for k, v in list(d.items()):
        if isinstance(v, str):
            # JSON 字段尝试解析
            if k in ("attachments", "supp_summary", "cust_view_detail", "gs_view_detail"):
                try:
                    d[k] = json.loads(v) if v else []
                except:
                    # 解析失败时回退为空数组，避免把损坏的字符串（如 "[object Object]"）暴露给前端
                    d[k] = []
    return d

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.executescript("""
    CREATE TABLE IF NOT EXISTS won_projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT DEFAULT (datetime('now','localtime')),
        updated_at TEXT DEFAULT (datetime('now','localtime')),
        contract_no TEXT DEFAULT '',
        customer TEXT DEFAULT '',
        province TEXT DEFAULT '',
        contract_date TEXT DEFAULT '',
        signing_parties TEXT DEFAULT '',
        contract_currency TEXT DEFAULT '',
        rate_rmb_vnd TEXT DEFAULT '',
        rate_usd_vnd TEXT DEFAULT '',
        incoterm TEXT DEFAULT '',
        include_install TEXT DEFAULT '',
        payment_terms TEXT DEFAULT '',
        payment_terms_zh TEXT DEFAULT '',
        payment_terms_en TEXT DEFAULT '',
        payment_terms_vi TEXT DEFAULT '',
        salesperson TEXT DEFAULT '',

        equip_rmb INTEGER DEFAULT 0,
        equip_usd INTEGER DEFAULT 0,
        equip_vnd INTEGER DEFAULT 0,
        superv_rmb INTEGER DEFAULT 0,
        superv_usd INTEGER DEFAULT 0,
        superv_vnd INTEGER DEFAULT 0,
        fb_budget_rmb INTEGER DEFAULT 0,
        fb_budget_usd INTEGER DEFAULT 0,
        fb_budget_vnd INTEGER DEFAULT 0,
        fb_actual_rmb INTEGER DEFAULT 0,
        fb_actual_usd INTEGER DEFAULT 0,
        fb_actual_vnd INTEGER DEFAULT 0,
        cc_budget_rmb INTEGER DEFAULT 0,
        cc_budget_usd INTEGER DEFAULT 0,
        cc_budget_vnd INTEGER DEFAULT 0,
        cc_actual_rmb INTEGER DEFAULT 0,
        cc_actual_usd INTEGER DEFAULT 0,
        cc_actual_vnd INTEGER DEFAULT 0,
        total_equip_rmb INTEGER DEFAULT 0,
        total_equip_usd INTEGER DEFAULT 0,
        total_equip_vnd INTEGER DEFAULT 0,
        inst_budget_rmb INTEGER DEFAULT 0,
        inst_budget_usd INTEGER DEFAULT 0,
        inst_budget_vnd INTEGER DEFAULT 0,
        inst_actual_rmb INTEGER DEFAULT 0,
        inst_actual_usd INTEGER DEFAULT 0,
        inst_actual_vnd INTEGER DEFAULT 0,
        total_ei_rmb INTEGER DEFAULT 0,
        total_ei_usd INTEGER DEFAULT 0,
        total_ei_vnd INTEGER DEFAULT 0,

        -- ★ 新增：增值税&关税&其他费用调节平衡输入
        vat_rmb INTEGER DEFAULT 0,
        vat_usd INTEGER DEFAULT 0,
        vat_vnd INTEGER DEFAULT 0,

        -- ★ 新增：质保金信息
        warranty_rmb INTEGER DEFAULT 0,
        warranty_usd INTEGER DEFAULT 0,
        warranty_vnd INTEGER DEFAULT 0,
        warranty_start TEXT DEFAULT '',
        warranty_end TEXT DEFAULT '',

        cust_pay_count INTEGER DEFAULT 0,
        cust_paid_rmb INTEGER DEFAULT 0,
        cust_paid_usd INTEGER DEFAULT 0,
        cust_paid_vnd INTEGER DEFAULT 0,
        cust_unpaid_rmb INTEGER DEFAULT 0,
        cust_unpaid_usd INTEGER DEFAULT 0,
        cust_unpaid_vnd INTEGER DEFAULT 0,
        cust_view_detail TEXT DEFAULT '[]',
        cust_remark TEXT DEFAULT '',

        gs_comm_pct TEXT DEFAULT '',
        gs_comm_rmb INTEGER DEFAULT 0,
        gs_comm_usd INTEGER DEFAULT 0,
        gs_comm_vnd INTEGER DEFAULT 0,
        gs_pay_count INTEGER DEFAULT 0,
        gs_paid_rmb INTEGER DEFAULT 0,
        gs_paid_usd INTEGER DEFAULT 0,
        gs_paid_vnd INTEGER DEFAULT 0,
        gs_unpaid_rmb INTEGER DEFAULT 0,
        gs_unpaid_usd INTEGER DEFAULT 0,
        gs_unpaid_vnd INTEGER DEFAULT 0,
        gs_view_detail TEXT DEFAULT '[]',
        gs_remark TEXT DEFAULT '',

        agi_payable_rmb INTEGER DEFAULT 0,
        agi_payable_usd INTEGER DEFAULT 0,
        agi_payable_vnd INTEGER DEFAULT 0,

        agi_remark TEXT DEFAULT '',

        doc_equip TEXT DEFAULT '',
        doc_install TEXT DEFAULT '',
        doc_both TEXT DEFAULT '',
        doc_addendum_cnt INTEGER DEFAULT 0,
        doc_view_addendum TEXT DEFAULT '',
        doc_remark TEXT DEFAULT '',
        concrete_floor_spec TEXT DEFAULT '',

        attachments TEXT DEFAULT '[]',
        supp_summary TEXT DEFAULT '[]'
    );
    """)

    # ★ 迁移：为已有数据库添加新列（如果不存在）
    try:
        c.execute("ALTER TABLE won_projects ADD COLUMN agi_remark TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass
    try:
        c.execute("ALTER TABLE won_projects ADD COLUMN doc_equip TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass
    try:
        c.execute("ALTER TABLE won_projects ADD COLUMN doc_install TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass
    try:
        c.execute("ALTER TABLE won_projects ADD COLUMN doc_both TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass
    try:
        c.execute("ALTER TABLE won_projects ADD COLUMN doc_addendum_cnt INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass
    try:
        c.execute("ALTER TABLE won_projects ADD COLUMN doc_view_addendum TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass
    try:
        c.execute("ALTER TABLE won_projects ADD COLUMN doc_remark TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass
    # ★ 三语付款方式列
    try:
        c.execute("ALTER TABLE won_projects ADD COLUMN payment_terms_zh TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass
    try:
        c.execute("ALTER TABLE won_projects ADD COLUMN payment_terms_en TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass
    try:
        c.execute("ALTER TABLE won_projects ADD COLUMN payment_terms_vi TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass
    # ★ 历史数据迁移：旧单语 payment_terms → 默认视为当前语言，回填三列（幂等）
    c.execute(
        "UPDATE won_projects SET payment_terms_zh = payment_terms, payment_terms_en = payment_terms, payment_terms_vi = payment_terms "
        "WHERE (payment_terms_zh IS NULL OR payment_terms_zh = '') AND (payment_terms_en IS NULL OR payment_terms_en = '') AND (payment_terms_vi IS NULL OR payment_terms_vi = '') "
        "AND payment_terms IS NOT NULL AND payment_terms != ''"
    )
    # ★ 三语备注列：cust/gs/agi remark 各拆 zh/en/vi 三列（方案A）
    for _base in ("cust_remark", "gs_remark", "agi_remark"):
        for _suf in ("zh", "en", "vi"):
            try:
                c.execute(f"ALTER TABLE won_projects ADD COLUMN {_base}_{_suf} TEXT DEFAULT ''")
            except sqlite3.OperationalError:
                pass
    try:
        c.execute("ALTER TABLE crm_projects ADD COLUMN remark_zh TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass
    try:
        c.execute("ALTER TABLE crm_projects ADD COLUMN remark_en TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass
    try:
        c.execute("ALTER TABLE crm_projects ADD COLUMN remark_vi TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass
    # ★ 历史数据迁移：旧单语备注 → 默认视为中文，回填 _zh（仅当 _zh 为空且原列非空，幂等）
    for _base in ("cust_remark", "gs_remark", "agi_remark"):
        c.execute(
            f"UPDATE won_projects SET {_base}_zh = {_base} "
            f"WHERE ({_base}_zh IS NULL OR {_base}_zh = '') AND {_base} IS NOT NULL AND {_base} != ''"
        )
    # ★ 全新库时 crm_projects 还没创建（CREATE TABLE 在本函数稍后），必须跳过；
    #   否则 init_db 抛 "no such table: crm_projects"，导致全新库永远初始化失败
    #   （旧库已存在该表，回填照常执行，行为不变）。
    if c.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='crm_projects'").fetchone():
        c.execute(
            "UPDATE crm_projects SET remark_zh = remark "
            "WHERE (remark_zh IS NULL OR remark_zh = '') AND remark IS NOT NULL AND remark != ''"
        )
    conn.commit()
    try:
        c.execute("ALTER TABLE won_projects ADD COLUMN vat_rmb INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass
    try:
        c.execute("ALTER TABLE won_projects ADD COLUMN vat_usd INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass
    try:
        c.execute("ALTER TABLE won_projects ADD COLUMN vat_vnd INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass
    try:
        c.execute("ALTER TABLE won_projects ADD COLUMN warranty_rmb INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass
    try:
        c.execute("ALTER TABLE won_projects ADD COLUMN warranty_usd INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass
    try:
        c.execute("ALTER TABLE won_projects ADD COLUMN warranty_vnd INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass
    try:
        c.execute("ALTER TABLE won_projects ADD COLUMN warranty_start TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass
    try:
        c.execute("ALTER TABLE won_projects ADD COLUMN warranty_end TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass

    # ★ 迁移：为历史数据库补上缺失的 attachments / supp_summary / created_at / updated_at 列
    try:
        c.execute("ALTER TABLE won_projects ADD COLUMN attachments TEXT DEFAULT '[]'")
    except sqlite3.OperationalError:
        pass
    try:
        c.execute("ALTER TABLE won_projects ADD COLUMN supp_summary TEXT DEFAULT '[]'")
    except sqlite3.OperationalError:
        pass
    try:
        c.execute("ALTER TABLE won_projects ADD COLUMN created_at TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass
    try:
        c.execute("ALTER TABLE won_projects ADD COLUMN updated_at TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass
    # ★ 独立记录：为 won_projects 添加 owner_user_id（记录归属账号）
    try:
        c.execute("ALTER TABLE won_projects ADD COLUMN owner_user_id TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass
    # ★ V40：won_projects 省份列（本地 SQLite 无 100 列限制，直接加列；云端走映射表）
    try:
        c.execute("ALTER TABLE won_projects ADD COLUMN province TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass
    # ★ 水泥漏缝地板规格 JSON
    try:
        c.execute("ALTER TABLE won_projects ADD COLUMN concrete_floor_spec TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass
    # ★ V40：WON 省份自动填充（与云端 wonlost.js 的 WON_PROV_FILL 列表一致）：
    #   空省份行按列表循环分配，让案例数据有合理分布
    _won_prov_fill = [
        "Đồng Nai", "Tây Ninh", "Bắc Ninh", "Vĩnh Long", "Thái Nguyên",
        "An Giang", "Cần Thơ", "Quảng Ninh", "Đắk Lắk", "Thanh Hóa",
        "Khánh Hòa", "Gia Lai", "Lâm Đồng", "TP. Hồ Chí Minh", "Hà Nội",
        "Hải Phòng", "Đà Nẵng", "Nghệ An", "Hưng Yên", "Lạng Sơn",
    ]
    _won_rows_no_prov = c.execute(
        "SELECT id FROM won_projects WHERE province IS NULL OR province='' ORDER BY id"
    ).fetchall()
    for _i, _r in enumerate(_won_rows_no_prov):
        c.execute(
            "UPDATE won_projects SET province=? WHERE id=?",
            (_won_prov_fill[_i % len(_won_prov_fill)], _r[0]),
        )

    # ★ CRM（报价/跟进）表 —— 与 Won 同机制，三语支持
    c.executescript("""
    CREATE TABLE IF NOT EXISTS crm_projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT DEFAULT (datetime('now','localtime')),
        updated_at TEXT DEFAULT (datetime('now','localtime')),

        quote_no TEXT DEFAULT '',
        project_name TEXT DEFAULT '',
        province TEXT DEFAULT '',
        customer TEXT DEFAULT '',
        bu TEXT DEFAULT '',
        construction TEXT DEFAULT '',
        startup_pct TEXT DEFAULT '',
        sign_pct TEXT DEFAULT '',
        manager TEXT DEFAULT '',
        manager_phone TEXT DEFAULT '',
        company_info TEXT DEFAULT '',
        initial_quote_date TEXT DEFAULT '',
        est_purchase_date TEXT DEFAULT '',
        est_ship_date TEXT DEFAULT '',
        quote_version TEXT DEFAULT '',
        last_quote_date TEXT DEFAULT '',
        rate_rmb_vnd TEXT DEFAULT '',
        rate_usd_vnd TEXT DEFAULT '',
        incoterm TEXT DEFAULT '',
        install_quoted TEXT DEFAULT '',
        salesperson TEXT DEFAULT '',
        remark TEXT DEFAULT '',
        pdf_equip TEXT DEFAULT '',
        pdf_install TEXT DEFAULT '',
        pdf_both TEXT DEFAULT '',

        q1_rmb INTEGER DEFAULT 0, q1_usd INTEGER DEFAULT 0, q1_vnd INTEGER DEFAULT 0,
        q2_rmb INTEGER DEFAULT 0, q2_usd INTEGER DEFAULT 0, q2_vnd INTEGER DEFAULT 0,
        q3_rmb INTEGER DEFAULT 0, q3_usd INTEGER DEFAULT 0, q3_vnd INTEGER DEFAULT 0,
        q4_rmb INTEGER DEFAULT 0, q4_usd INTEGER DEFAULT 0, q4_vnd INTEGER DEFAULT 0,
        q5_rmb INTEGER DEFAULT 0, q5_usd INTEGER DEFAULT 0, q5_vnd INTEGER DEFAULT 0,
        q6_rmb INTEGER DEFAULT 0, q6_usd INTEGER DEFAULT 0, q6_vnd INTEGER DEFAULT 0,
        q7_rmb INTEGER DEFAULT 0, q7_usd INTEGER DEFAULT 0, q7_vnd INTEGER DEFAULT 0,
        status TEXT DEFAULT 'active'
    );
    """)
    # 兼容已存在的库：补充 status 列
    try:
        c.execute("ALTER TABLE crm_projects ADD COLUMN status TEXT DEFAULT 'active'")
    except sqlite3.OperationalError:
        pass
    # ★ 独立记录：为 crm_projects 添加 owner_user_id（记录归属账号）
    try:
        c.execute("ALTER TABLE crm_projects ADD COLUMN owner_user_id TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass

    # ★ 失败项目表（lost_projects）—— 与 CRM 同机制、三语支持，完全独立存储
    c.executescript("""
    CREATE TABLE IF NOT EXISTS lost_projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT DEFAULT (datetime('now','localtime')),
        updated_at TEXT DEFAULT (datetime('now','localtime')),

        quote_no TEXT DEFAULT '',
        project_name TEXT DEFAULT '',
        province TEXT DEFAULT '',
        customer TEXT DEFAULT '',
        bu TEXT DEFAULT '',
        construction TEXT DEFAULT '',
        startup_pct TEXT DEFAULT '',
        sign_pct TEXT DEFAULT '',
        manager TEXT DEFAULT '',
        manager_phone TEXT DEFAULT '',
        company_info TEXT DEFAULT '',
        initial_quote_date TEXT DEFAULT '',
        est_purchase_date TEXT DEFAULT '',
        est_ship_date TEXT DEFAULT '',
        quote_version TEXT DEFAULT '',
        last_quote_date TEXT DEFAULT '',
        rate_rmb_vnd TEXT DEFAULT '',
        rate_usd_vnd TEXT DEFAULT '',
        incoterm TEXT DEFAULT '',
        install_quoted TEXT DEFAULT '',
        salesperson TEXT DEFAULT '',
        remark TEXT DEFAULT '',
        pdf_equip TEXT DEFAULT '',
        pdf_install TEXT DEFAULT '',
        pdf_both TEXT DEFAULT '',
        fail_reason TEXT DEFAULT '',
        fail_date TEXT DEFAULT '',

        q1_rmb INTEGER DEFAULT 0, q1_usd INTEGER DEFAULT 0, q1_vnd INTEGER DEFAULT 0,
        q2_rmb INTEGER DEFAULT 0, q2_usd INTEGER DEFAULT 0, q2_vnd INTEGER DEFAULT 0,
        q3_rmb INTEGER DEFAULT 0, q3_usd INTEGER DEFAULT 0, q3_vnd INTEGER DEFAULT 0,
        q4_rmb INTEGER DEFAULT 0, q4_usd INTEGER DEFAULT 0, q4_vnd INTEGER DEFAULT 0,
        q5_rmb INTEGER DEFAULT 0, q5_usd INTEGER DEFAULT 0, q5_vnd INTEGER DEFAULT 0,
        q6_rmb INTEGER DEFAULT 0, q6_usd INTEGER DEFAULT 0, q6_vnd INTEGER DEFAULT 0,
        q7_rmb INTEGER DEFAULT 0, q7_usd INTEGER DEFAULT 0, q7_vnd INTEGER DEFAULT 0
    );
    """)
    # ★ 独立记录：为 lost_projects 添加 owner_user_id（记录归属账号，从 crm 转失败时自动继承）
    try:
        c.execute("ALTER TABLE lost_projects ADD COLUMN owner_user_id TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass

    # ===================== 用户表（登录 / 权限） =====================
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            real_name TEXT DEFAULT '',
            role TEXT DEFAULT 'user',
            status TEXT DEFAULT 'active',
            created_at TEXT DEFAULT ''
        )
    """)
    # ===== 审批请求表（权限“发起审批”类型的真实拦截存储） =====
    c.executescript("""
    CREATE TABLE IF NOT EXISTS approval_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        requester TEXT NOT NULL,
        requester_name TEXT DEFAULT '',
        block_id TEXT NOT NULL,
        block_name TEXT DEFAULT '',
        action_name TEXT DEFAULT '',
        approvers TEXT DEFAULT '[]',
        status TEXT DEFAULT 'pending',      -- pending / approved / rejected
        created_at TEXT DEFAULT '',
        resolved_at TEXT DEFAULT '',
        resolver TEXT DEFAULT '',
        resolver_name TEXT DEFAULT ''
    );
    """)
    # ===== 生产现场工厂共享数据表（全员可见，服务端存储，取代仅浏览器 localStorage） =====
    c.execute("""
    CREATE TABLE IF NOT EXISTS prod_factory (
        project_id TEXT PRIMARY KEY,
        data TEXT,
        updated_by TEXT DEFAULT '',
        updated_at TEXT DEFAULT ''
    );
    """)
    # ===== 生产模块通用键值表（材料规格等全局配置，服务端共享） =====
    c.execute("""
    CREATE TABLE IF NOT EXISTS prod_kv (
        k TEXT PRIMARY KEY,
        data TEXT,
        updated_by TEXT DEFAULT '',
        updated_at TEXT DEFAULT ''
    );
    """)
    # 审批模块扩展字段：标题 / 审批内容说明 / 审批结果意见
    for col in ["title", "content", "result_note"]:
        try:
            c.execute(f"ALTER TABLE approval_requests ADD COLUMN {col} TEXT DEFAULT ''")
        except sqlite3.OperationalError:
            pass

    # 单次生效审批字段：persist='single-use' 不写入用户权限，仅单次放行；target_id 区分同一区块不同操作对象
    for col, ddl in [("persist", "TEXT DEFAULT 'persistent'"), ("target_id", "TEXT DEFAULT ''")]:
        try:
            c.execute(f"ALTER TABLE approval_requests ADD COLUMN {col} {ddl}")
        except sqlite3.OperationalError:
            pass
    # 已消耗标记：服务端权限闸门放行单次审批时置 1，防止同一审批被重复用于多次操作
    try:
        c.execute("ALTER TABLE approval_requests ADD COLUMN consumed INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass
    # 用户与权限管理审批：payload 暂存（USR-D1 权限变更 / USR-D2 新增用户 / USR-D3 删除用户），
    # 审批通过后由服务端按 payload 执行（新增账号通过前不入 users 表=不可登录、不出现在用户列表）
    try:
        c.execute("ALTER TABLE approval_requests ADD COLUMN payload TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass

    # 种子审批数据：便于测试“审批”模块（生产模式下跳过，避免清空后复活）
    if DEMO_SEED:
        seed_approval_requests(c)
    try:
        c.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user'")
    except sqlite3.OperationalError:
        pass
    try:
        c.execute("ALTER TABLE users ADD COLUMN status TEXT DEFAULT 'active'")
    except sqlite3.OperationalError:
        pass
    # 离职代理：离职用户的业务数据/待办自动并给代理人（存被代理人的 username）
    try:
        c.execute("ALTER TABLE users ADD COLUMN delegate_to TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass
    # DEMO 标记（仅信息用途）：1=演示账号、0=真实账号。供 reset_demo_data.py
    # 清理脚本按标记删演示账号。★ DEMO 按钮（load/clear）已与用户表彻底解耦，
    # 不会读写此标记，也不会增删任何用户。
    _is_demo_added = False
    try:
        c.execute("ALTER TABLE users ADD COLUMN is_demo INTEGER DEFAULT 0")
        _is_demo_added = True
    except sqlite3.OperationalError:
        pass
    if _is_demo_added:
        # 仅在首次加列时做一次存量标注：演示账号标 1，真实账号标 0。
        # 之后 is_demo 完全由数据流维护（DEMO 还原=1、正常建号=0），
        # 不在每次启动时重标 —— 否则用户用演示名建的真实号会在重启后被误标。
        try:
            for _u in DEMO_USERNAMES:
                c.execute("UPDATE users SET is_demo=1 WHERE lower(username)=lower(?)", (_u,))
            for _u in REAL_USERS:
                c.execute("UPDATE users SET is_demo=0 WHERE lower(username)=lower(?)", (_u,))
        except Exception:
            pass

    # ★ 业务表 DEMO 标记（is_demo）：1=演示数据、0=真实数据。
    #   用于「清空 DEMO」时精确删除（DELETE WHERE is_demo=1），绝不误删真实录入的数据。
    #   每次还原/加载 DEMO 时由 load_demo_data 打 1；学员在演示期间录入的真实业务数据保持 0。
    #   注：DEMO 按钮（load/clear）仍与 users 表彻底解耦，这里只标记业务数据行。
    for _bt in DEMO_TABLES:
        try:
            c.execute("ALTER TABLE %s ADD COLUMN is_demo INTEGER DEFAULT 0" % _bt)
        except sqlite3.OperationalError:
            pass

    # 个人佣金 · 佣金记录主表（案例数据打 is_demo=1，便于最后一条命令精确清除，不误伤真实数据）
    try:
        c.execute("""
            CREATE TABLE IF NOT EXISTS commission_records (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              contract TEXT NOT NULL,
              parties TEXT DEFAULT '',
              group_name TEXT DEFAULT '',
              sign_date TEXT DEFAULT '',
              deposit_date TEXT DEFAULT '',
              currency TEXT DEFAULT '',
              equip_rmb TEXT DEFAULT '',
              equip_usd TEXT DEFAULT '',
              equip_vnd TEXT DEFAULT '',
              rate_rmb TEXT DEFAULT '',
              rate_usd TEXT DEFAULT '',
              remark TEXT DEFAULT '',
              is_demo INTEGER DEFAULT 0,
              created_at TEXT DEFAULT (datetime('now','localtime')),
              updated_at TEXT DEFAULT (datetime('now','localtime'))
            )
        """)
        c.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_comm_rec_contract ON commission_records(contract)")
    except Exception:
        pass
    # 个人佣金 · 受益人表（payments 为 JSON 字符串，存 1~N 期支付明细）
    try:
        c.execute("""
            CREATE TABLE IF NOT EXISTS commission_beneficiaries (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              record_id INTEGER NOT NULL,
              ben_index INTEGER DEFAULT 0,
              name TEXT DEFAULT '',
              currency TEXT DEFAULT '',
              total_rmb TEXT DEFAULT '',
              total_usd TEXT DEFAULT '',
              total_vnd TEXT DEFAULT '',
              sign_date TEXT DEFAULT '',
              deposit_date TEXT DEFAULT '',
              paid_rmb TEXT DEFAULT '',
              paid_usd TEXT DEFAULT '',
              paid_vnd TEXT DEFAULT '',
              pay_count INTEGER DEFAULT 0,
              unpaid_rmb TEXT DEFAULT '',
              unpaid_usd TEXT DEFAULT '',
              unpaid_vnd TEXT DEFAULT '',
              pay_nature TEXT DEFAULT '',
              note TEXT DEFAULT '',
              payments TEXT DEFAULT '[]',
              updated_at TEXT DEFAULT (datetime('now','localtime'))
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_comm_ben_rec ON commission_beneficiaries(record_id)")
    except Exception:
        pass
    # 个人佣金 · 修改金额审批表（后门三人组 tom/cuong/travis 专用）
    try:
        c.execute("""
            CREATE TABLE IF NOT EXISTS comm_amt_requests (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              req_key TEXT NOT NULL,
              contract_no TEXT DEFAULT '',
              beneficiary TEXT DEFAULT '',
              pay_no TEXT DEFAULT '',
              currency TEXT DEFAULT '',
              old_amount TEXT DEFAULT '',
              new_amount TEXT DEFAULT '',
              reason TEXT DEFAULT '',
              requester TEXT NOT NULL,
              approver1 TEXT NOT NULL,
              approver2 TEXT NOT NULL,
              dec1 TEXT DEFAULT '',
              dec2 TEXT DEFAULT '',
              status TEXT DEFAULT 'pending',
              created_at TEXT,
              resolved_at TEXT
            )
        """)
    except Exception:
        pass
    # 权限相关字段
    for col, ddl in [
        ("position", "TEXT DEFAULT ''"),
        ("vis_can_see_me", "TEXT DEFAULT '[]'"),   # 可看该用户数据的人 id 列表（反向授权）
        ("vis_he_can_see", "TEXT DEFAULT '[]'"),   # 该用户可看的人 id 列表（正向授权）
        ("perms", "TEXT DEFAULT '{}'"),            # 区块权限决策 {bid: {decision, approvers}}
        ("forgot_approvers", "TEXT DEFAULT '[]'"), # 忘记密码审批人（tom 默认，可追加；通过后密码重置为初始密码）
        ("sort_order", "INTEGER DEFAULT 0"),       # 用户列表排序权重（越小越靠前）
    ]:
        try:
            c.execute(f"ALTER TABLE users ADD COLUMN {col} {ddl}")
        except sqlite3.OperationalError:
            pass

    # 登录记录表
    c.execute("""
        CREATE TABLE IF NOT EXISTS login_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            login_time TEXT DEFAULT (datetime('now','localtime')),
            ip_address TEXT DEFAULT '',
            user_agent TEXT DEFAULT ''
        )
    """)

    # 自由任命管理人员表：与职位解耦，单独维护 2-4 名管理员
    c.execute("""
        CREATE TABLE IF NOT EXISTS managers (
            username TEXT PRIMARY KEY NOT NULL,
            updated_at TEXT DEFAULT (datetime('now','localtime'))
        )
    """)

    # 忘记密码申请表
    c.execute("""
        CREATE TABLE IF NOT EXISTS password_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            requested_at TEXT DEFAULT '',
            processed_at TEXT DEFAULT '',
            note TEXT DEFAULT ''
        )
    """)
    seed = c.execute("SELECT COUNT(*) FROM users WHERE username='tom'").fetchone()[0]
    if seed == 0:
        c.execute("INSERT INTO users (username, password, real_name, role, status, created_at) VALUES (?,?,?,?,?,?)",
                  ("tom", "66668888", "Tom", "admin", "active", time.strftime("%Y-%m-%d %H:%M:%S")))
        print("[init_db] 已创建种子用户 tom / 66668888")

    # 确保 tom 始终在管理员名单中
    c.execute("INSERT OR IGNORE INTO managers (username) VALUES (?)", ("tom",))
    # 迁移旧逻辑中的 gm1/gm2（若存在）到管理员表，保证平滑过渡
    for old_mgr in ("gm1", "gm2"):
        exists = c.execute("SELECT 1 FROM users WHERE username=?", (old_mgr,)).fetchone()
        if exists:
            c.execute("INSERT OR IGNORE INTO managers (username) VALUES (?)", (old_mgr,))

    # ★ 种子数据：CRM（潜在项目）没有有效数据时自动注入 30 组示例数据
    # 若存在空占位行（quote_no 为空），先清理，再判断是否为空。
    c.execute("DELETE FROM crm_projects WHERE quote_no IS NULL OR quote_no = ''")
    cnt = c.execute("SELECT COUNT(*) FROM crm_projects").fetchone()[0]
    # ★ 种子数据：签约项目（won_projects）没有有效数据时自动注入示例数据
    # 如果表为空或没有 AGI-Customer/GS-Customer 数据（看板图表需要这些数据），插入种子数据
    won_cnt = c.execute("SELECT COUNT(*) FROM won_projects WHERE customer IS NOT NULL AND customer != ''").fetchone()[0]
    bu_cnt = c.execute("SELECT COUNT(*) FROM won_projects WHERE signing_parties IN ('AGI-Customer', 'GS-Customer')").fetchone()[0]
    if not DEMO_SEED:
        # 生产模式：不注入任何示例数据，表可保持为空
        print("[init_db] 生产模式(DEMO_SEED=False)：跳过示例数据注入")
    elif won_cnt == 0 or bu_cnt == 0:
        seed_won_projects(c)
        if won_cnt == 0:
            print("[init_db] won_projects 无有效数据，已自动注入示例签约项目数据")
        else:
            print("[init_db] won_projects 缺少 AGI-Customer/GS-Customer 数据，已补充示例数据")
    else:
        pass  # 已有数据，不做修改

    if DEMO_SEED and cnt == 0:
        seed_crm_projects(c)
        print("[init_db] crm_projects 无有效数据，已自动注入 30 组示例数据")
    elif not DEMO_SEED:
        pass   # 生产模式：保持为空，不注入
    else:
        # 已存在数据：修正旧版种子数据（省份/BU/建设情况 需与模态框下拉选项值一致；
        # 启动概率/签约概率 不得超过 100%）
        migrate_crm_seed(c)
        # 三币联动/电话/公司信息/概率 多样化修正
        migrate_crm_seed_v2(c)

    # 迁移：把旧权限数据里存的审批人数字 ID 全部转换为用户名
    _migrate_approver_ids_to_usernames(c)

    # ===================== 资料库文件索引表 =====================
    c.execute("""
        CREATE TABLE IF NOT EXISTS library_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER DEFAULT NULL,
            filename TEXT NOT NULL,
            original_name TEXT NOT NULL,
            uploader TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now','localtime')),
            size INTEGER DEFAULT 0
        )
    """)
    try:
        c.execute("CREATE INDEX IF NOT EXISTS idx_library_project ON library_files(project_id)")
    except Exception:
        pass

    conn.commit()
    conn.close()


def seed_crm_projects(c):
    """在 crm_projects 为空时注入 30 组示例数据（供测试/演示用）。"""
    # 省份 / BU / 建设情况：取值必须与前端下拉框的 <option value> 完全一致，
    # 否则模态框打开时下拉框无法匹配，会停留在"未选择"并导致必填校验失败。
    provinces = ["Bắc Ninh", "Đà Nẵng", "Hải Phòng", "TP. Hồ Chí Minh", "Hà Nội",
                 "Tây Ninh", "Đồng Nai", "Vĩnh Long", "Quảng Ninh", "Thái Nguyên"]
    bus = ["pig_farm", "broiler_farm", "chicken_egg_farm", "duck_farm",
           "duck_egg_farm", "others"]
    constructions = ["land", "license", "design", "bidding", "supplier_sel",
                     "nearing", "signed_no_deposit", "signed_deposit", "failed", "cancelled"]
    incoterms = ["EXW", "FOB", "CIF", "DDP", "CIP"]
    # 负责人（客户方联系人）：必须是越南人名，不含中文
    managers = [
        "Nguyen Van An", "Tran Thi Binh", "Le Quang Huy", "Pham Minh Duc",
        "Hoang Van Long", "Vu Thi Mai", "Do Cong Thanh", "Bui Tuan Kiet",
        "Ngo Thanh Trung", "Dang Xuan Phuc", "Vo Van Tam", "Ly Thi Hoa",
        "Phan Ngoc Son", "Duong Minh Tri", "Trinh Van Hai", "Nguyen Thi Lan",
        "Huynh Phuoc Thanh", "Thai Van Dung", "Cao Tuan Anh", "Dinh Van Phuoc",
    ]
    # 销售（内部员工）
    sales = ["Tom", "Travis", "Ali", "Cuong", "Khoa", "James"]
    customers = [
        "越南富光电子", "GreenTech Solar", "Long An Steel", "Hai Phong Logistics",
        "河内精密制造", "Dong Nai Auto Parts", "Binh Duong Electric", "Quang Ninh Cement",
        "Thai Nguyen Machinery", "Vinfast Components", "Samsung Display VN", "LG Innotek VN",
    ]
    zones = ["A区", "B区", "二期", "一期", "扩建"]
    rmb_bases = [850000, 920000, 1000000, 760000, 1150000, 680000, 1290000, 540000, 980000,
                 1430000, 610000, 880000, 1220000, 730000, 1350000, 990000, 470000, 1120000,
                 1500000, 1050000]
    # 启动概率 / 签约概率：多样化，避免全部为 100%（签约概率不高于启动概率）
    startup_pcts = [30, 45, 60, 75, 80, 90, 55, 70, 85, 95, 40, 65, 50, 88, 72,
                    35, 58, 68, 92, 48, 62, 38, 82, 52, 78, 42, 96, 25, 64, 74]
    sign_pcts =    [15, 30, 45, 60, 70, 80, 40, 55, 70, 85, 25, 50, 35, 72, 55,
                    20, 42, 52, 80, 32, 46, 22, 68, 36, 60, 28, 85, 15, 50, 62]
    # 负责人电话：越南手机号（10位，以 03/05/07/08/09 开头），多样化
    phone_pref = ["09", "03", "07", "08", "05"]
    # 公司信息：结合客户名 + 越南不同省份/地址，多样化
    addr_cities = ["胡志明市", "河内", "海防", "岘港", "同奈", "北宁", "太原", "广宁", "西宁", "永隆"]
    addr_zone = ["工业园区", "高新技术区", "出口加工区", "经济开发区", "商贸中心"]
    company_extra = ["越南分公司", "驻越办事处", "制造基地", "项目工程部", "区域服务中心"]

    def fdate(month, day):
        return "2026-{:02d}-{:02d}".format(month, max(1, min(28, day)))

    def rmb_to_q(rmb_amount, rate_rmb_vnd, rate_usd_vnd):
        """按项目自身汇率，将 RMB 换算为一致的 USD 与 VND（与模态框 crmQuoteLink 的 RMB 换算一致）。"""
        vnd = round(rmb_amount * rate_rmb_vnd)
        usd = round(vnd / rate_usd_vnd)
        return vnd, usd

    rows = []
    for i in range(30):
        base = rmb_bases[i % len(rmb_bases)]
        q1 = round(base * 0.20); q2 = round(base * 0.15); q3 = round(base * 0.25)
        q4 = round(base * 0.12); q5 = round(base * 0.08); q6 = round(base * 0.10)
        q7 = round(base * 0.10)
        cust = customers[i % len(customers)]
        rate_rmb_vnd = 3000 + i * 11
        rate_usd_vnd = (20 + i % 5) * 1000
        # 三币联动：以 RMB 为基准，按本项目汇率换算 USD / VND
        qa = rmb_to_q(q1, rate_rmb_vnd, rate_usd_vnd)
        qb = rmb_to_q(q2, rate_rmb_vnd, rate_usd_vnd)
        qc = rmb_to_q(q3, rate_rmb_vnd, rate_usd_vnd)
        qd = rmb_to_q(q4, rate_rmb_vnd, rate_usd_vnd)
        qe = rmb_to_q(q5, rate_rmb_vnd, rate_usd_vnd)
        qf = rmb_to_q(q6, rate_rmb_vnd, rate_usd_vnd)
        qg = rmb_to_q(q7, rate_rmb_vnd, rate_usd_vnd)
        phone = phone_pref[i % len(phone_pref)] + "{:08d}".format((i * 137) % 100000000)
        company = "{}·{}·{} · {}".format(cust, addr_cities[i % len(addr_cities)],
                                         addr_zone[i % len(addr_zone)],
                                         company_extra[i % len(company_extra)])
        rows.append((
            "QT-2026-{:03d}".format(i + 1),
            cust + " " + zones[i % len(zones)],
            provinces[i % len(provinces)],
            cust,
            bus[i % len(bus)],
            constructions[i % len(constructions)],
            str(startup_pcts[i % len(startup_pcts)]),
            str(sign_pcts[i % len(sign_pcts)]),
            managers[i % len(managers)],
            phone,
            company,
            fdate(1 + i % 12, 1 + i % 9),
            fdate(1 + (i + 2) % 12, 11 + (i + 3) % 10),
            fdate(1 + (i + 4) % 12, 21 + (i + 5) % 8),
            "V{}".format(1 + i % 3),
            fdate(1 + (i + 1) % 12, 12 + (i + 2) % 10),
            "{}".format(rate_rmb_vnd),
            "{}".format(rate_usd_vnd),
            incoterms[i % len(incoterms)],
            "是" if i % 3 != 2 else "否",
            sales[i % len(sales)],
            ["", "重点跟进", "客户要求年前报价", "已提交技术方案", "等待审批"][i % 5],
            "", "", "",
            q1, qa[1], qa[0],
            q2, qb[1], qb[0],
            q3, qc[1], qc[0],
            q4, qd[1], qd[0],
            q5, qe[1], qe[0],
            q6, qf[1], qf[0],
            q7, qg[1], qg[0],
            (sales[i % len(sales)]).strip().lower(),   # owner_user_id（独立记录归属）
        ))

    cols = ("quote_no,project_name,province,customer,bu,construction,startup_pct,sign_pct,"
            "manager,manager_phone,company_info,initial_quote_date,est_purchase_date,"
            "est_ship_date,quote_version,last_quote_date,rate_rmb_vnd,rate_usd_vnd,incoterm,"
            "install_quoted,salesperson,remark,pdf_equip,pdf_install,pdf_both,"
            "q1_rmb,q1_usd,q1_vnd,q2_rmb,q2_usd,q2_vnd,q3_rmb,q3_usd,q3_vnd,"
            "q4_rmb,q4_usd,q4_vnd,q5_rmb,q5_usd,q5_vnd,q6_rmb,q6_usd,q6_vnd,"
            "q7_rmb,q7_usd,q7_vnd,owner_user_id")
    placeholders = ",".join(["?"] * 47)
    c.executemany(
        "INSERT INTO crm_projects ({}) VALUES ({})".format(cols, placeholders),
        rows
    )


def seed_won_projects(c):
    """在 won_projects 为空时注入示例签约项目数据（供看板图表测试/演示用）。
    
    这些数据用于渲染签约项目看板中的三个图表：
    1. 各BU累计销售 vs 当年 - 需要 AGI-Customer 和 GS-Customer 的项目
    2. 各BU历年销售占比 - 需要按年份分组的数据
    3. 各BU当年销售占比 - 需要当年按签约方分组的数据
    
    注意：前端看板使用 total_equip_usd 字段计算销售金额，所以种子数据必须包含此字段
    """
    import datetime
    now = datetime.datetime.now()
    current_year = now.year
    
    # 示例签约项目数据：混合不同年份和签约方
    # total_equip_* 是前端图表使用的关键字段（签单金额）
    won_data = [
        # AGI-Customer 项目 (历年)
        {"contract_no": "AGI-2024-001", "customer": "河内养猪场A", "contract_date": f"{current_year-2}-03-15",
         "signing_parties": "AGI-Customer", "contract_currency": "USD", "rate_rmb_vnd": 4800, "rate_usd_vnd": 25000,
         "incoterm": "CIF", "salesperson": "Tom", 
         "total_equip_rmb": 2200000, "total_equip_usd": 75000, "total_equip_vnd": 1875000000,
         "total_ei_rmb": 2800000, "total_ei_usd": 95000, "total_ei_vnd": 2375000000},
        {"contract_no": "AGI-2024-002", "customer": "海防蛋鸡场B", "contract_date": f"{current_year-2}-06-20",
         "signing_parties": "AGI-Customer", "contract_currency": "USD", "rate_rmb_vnd": 4800, "rate_usd_vnd": 25000,
         "incoterm": "DDP", "salesperson": "Travis",
         "total_equip_rmb": 2500000, "total_equip_usd": 85000, "total_equip_vnd": 2125000000,
         "total_ei_rmb": 3200000, "total_ei_usd": 108000, "total_ei_vnd": 2700000000},
        {"contract_no": "AGI-2024-003", "customer": "同奈肉鸡场C", "contract_date": f"{current_year-2}-09-10",
         "signing_parties": "AGI-Customer", "contract_currency": "USD", "rate_rmb_vnd": 4800, "rate_usd_vnd": 25000,
         "incoterm": "CIF", "salesperson": "Tom",
         "total_equip_rmb": 1500000, "total_equip_usd": 51000, "total_equip_vnd": 1275000000,
         "total_ei_rmb": 1950000, "total_ei_usd": 66000, "total_ei_vnd": 1650000000},
        {"contract_no": "AGI-2025-001", "customer": "北宁养猪场D", "contract_date": f"{current_year-1}-02-28",
         "signing_parties": "AGI-Customer", "contract_currency": "USD", "rate_rmb_vnd": 4800, "rate_usd_vnd": 25500,
         "incoterm": "CIF", "salesperson": "Ali",
         "total_equip_rmb": 3200000, "total_equip_usd": 105000, "total_equip_vnd": 2677500000,
         "total_ei_rmb": 4100000, "total_ei_usd": 135000, "total_ei_vnd": 3442500000},
        {"contract_no": "AGI-2025-002", "customer": "胡志明饲料厂E", "contract_date": f"{current_year-1}-05-15",
         "signing_parties": "AGI-Customer", "contract_currency": "USD", "rate_rmb_vnd": 4800, "rate_usd_vnd": 25500,
         "incoterm": "DDP", "salesperson": "Tom",
         "total_equip_rmb": 4400000, "total_equip_usd": 145000, "total_equip_vnd": 3697500000,
         "total_ei_rmb": 5600000, "total_ei_usd": 184000, "total_ei_vnd": 4692000000},
        {"contract_no": "AGI-2025-003", "customer": "岘港禽蛋场F", "contract_date": f"{current_year-1}-08-22",
         "signing_parties": "AGI-Customer", "contract_currency": "USD", "rate_rmb_vnd": 4800, "rate_usd_vnd": 25500,
         "incoterm": "CIF", "salesperson": "Travis",
         "total_equip_rmb": 1800000, "total_equip_usd": 59000, "total_equip_vnd": 1504500000,
         "total_ei_rmb": 2350000, "total_ei_usd": 77000, "total_ei_vnd": 1963500000},
        {"contract_no": "AGI-2026-001", "customer": "太原养猪场G", "contract_date": f"{current_year}-01-10",
         "signing_parties": "AGI-Customer", "contract_currency": "USD", "rate_rmb_vnd": 4800, "rate_usd_vnd": 25800,
         "incoterm": "CIF", "salesperson": "Tom",
         "total_equip_rmb": 3800000, "total_equip_usd": 123000, "total_equip_vnd": 3173400000,
         "total_ei_rmb": 4800000, "total_ei_usd": 155000, "total_ei_vnd": 3999000000},
        {"contract_no": "AGI-2026-002", "customer": "广宁鸭场H", "contract_date": f"{current_year}-03-18",
         "signing_parties": "AGI-Customer", "contract_currency": "USD", "rate_rmb_vnd": 4800, "rate_usd_vnd": 25800,
         "incoterm": "DDP", "salesperson": "Ali",
         "total_equip_rmb": 1650000, "total_equip_usd": 53000, "total_equip_vnd": 1367400000,
         "total_ei_rmb": 2100000, "total_ei_usd": 68000, "total_ei_vnd": 1754400000},
        {"contract_no": "AGI-2026-003", "customer": "西宁禽类场I", "contract_date": f"{current_year}-06-05",
         "signing_parties": "AGI-Customer", "contract_currency": "USD", "rate_rmb_vnd": 4800, "rate_usd_vnd": 25800,
         "incoterm": "CIF", "salesperson": "Travis",
         "total_equip_rmb": 3000000, "total_equip_usd": 97000, "total_equip_vnd": 2502600000,
         "total_ei_rmb": 3800000, "total_ei_usd": 123000, "total_ei_vnd": 3173400000},
        # GS-Customer 项目 (历年)
        {"contract_no": "GS-2024-001", "customer": "河内养鸡场J", "contract_date": f"{current_year-2}-04-12",
         "signing_parties": "GS-Customer", "contract_currency": "USD", "rate_rmb_vnd": 4800, "rate_usd_vnd": 25000,
         "incoterm": "CIF", "salesperson": "Cuong",
         "total_equip_rmb": 1200000, "total_equip_usd": 41000, "total_equip_vnd": 1025000000,
         "total_ei_rmb": 1500000, "total_ei_usd": 51000, "total_ei_vnd": 1275000000},
        {"contract_no": "GS-2024-002", "customer": "海防养鸭场K", "contract_date": f"{current_year-2}-07-25",
         "signing_parties": "GS-Customer", "contract_currency": "USD", "rate_rmb_vnd": 4800, "rate_usd_vnd": 25000,
         "incoterm": "DDP", "salesperson": "Khoa",
         "total_equip_rmb": 1750000, "total_equip_usd": 59500, "total_equip_vnd": 1487500000,
         "total_ei_rmb": 2200000, "total_ei_usd": 74500, "total_ei_vnd": 1862500000},
        {"contract_no": "GS-2024-003", "customer": "同奈养猪场L", "contract_date": f"{current_year-2}-10-08",
         "signing_parties": "GS-Customer", "contract_currency": "USD", "rate_rmb_vnd": 4800, "rate_usd_vnd": 25000,
         "incoterm": "CIF", "salesperson": "Cuong",
         "total_equip_rmb": 1400000, "total_equip_usd": 47500, "total_equip_vnd": 1187500000,
         "total_ei_rmb": 1800000, "total_ei_usd": 61000, "total_ei_vnd": 1525000000},
        {"contract_no": "GS-2025-001", "customer": "北宁禽蛋场M", "contract_date": f"{current_year-1}-03-30",
         "signing_parties": "GS-Customer", "contract_currency": "USD", "rate_rmb_vnd": 4800, "rate_usd_vnd": 25500,
         "incoterm": "CIF", "salesperson": "James",
         "total_equip_rmb": 2300000, "total_equip_usd": 76000, "total_equip_vnd": 1938000000,
         "total_ei_rmb": 2900000, "total_ei_usd": 95500, "total_ei_vnd": 2435250000},
        {"contract_no": "GS-2025-002", "customer": "胡志明养鸡场N", "contract_date": f"{current_year-1}-07-18",
         "signing_parties": "GS-Customer", "contract_currency": "USD", "rate_rmb_vnd": 4800, "rate_usd_vnd": 25500,
         "incoterm": "DDP", "salesperson": "Cuong",
         "total_equip_rmb": 3250000, "total_equip_usd": 107000, "total_equip_vnd": 2728500000,
         "total_ei_rmb": 4100000, "total_ei_usd": 135000, "total_ei_vnd": 3442500000},
        {"contract_no": "GS-2025-003", "customer": "岘港饲料厂O", "contract_date": f"{current_year-1}-11-05",
         "signing_parties": "GS-Customer", "contract_currency": "USD", "rate_rmb_vnd": 4800, "rate_usd_vnd": 25500,
         "incoterm": "CIF", "salesperson": "Khoa",
         "total_equip_rmb": 1300000, "total_equip_usd": 42800, "total_equip_vnd": 1091400000,
         "total_ei_rmb": 1650000, "total_ei_usd": 54300, "total_ei_vnd": 1384650000},
        {"contract_no": "GS-2026-001", "customer": "太原禽类场P", "contract_date": f"{current_year}-02-14",
         "signing_parties": "GS-Customer", "contract_currency": "USD", "rate_rmb_vnd": 4800, "rate_usd_vnd": 25800,
         "incoterm": "CIF", "salesperson": "Cuong",
         "total_equip_rmb": 2750000, "total_equip_usd": 89000, "total_equip_vnd": 2296200000,
         "total_ei_rmb": 3500000, "total_ei_usd": 113000, "total_ei_vnd": 2915400000},
        {"contract_no": "GS-2026-002", "customer": "广宁养猪场Q", "contract_date": f"{current_year}-04-22",
         "signing_parties": "GS-Customer", "contract_currency": "USD", "rate_rmb_vnd": 4800, "rate_usd_vnd": 25800,
         "incoterm": "DDP", "salesperson": "James",
         "total_equip_rmb": 2150000, "total_equip_usd": 69500, "total_equip_vnd": 1793100000,
         "total_ei_rmb": 2700000, "total_ei_usd": 87500, "total_ei_vnd": 2257500000},
        {"contract_no": "GS-2026-003", "customer": "西宁养鸡场R", "contract_date": f"{current_year}-07-12",
         "signing_parties": "GS-Customer", "contract_currency": "USD", "rate_rmb_vnd": 4800, "rate_usd_vnd": 25800,
         "incoterm": "CIF", "salesperson": "Khoa",
         "total_equip_rmb": 2450000, "total_equip_usd": 79000, "total_equip_vnd": 2038200000,
         "total_ei_rmb": 3100000, "total_ei_usd": 100000, "total_ei_vnd": 2580000000},
    ]
    
    # 插入数据库
    for proj in won_data:
        c.execute("""
            INSERT INTO won_projects (
                contract_no, customer, contract_date, signing_parties, contract_currency,
                rate_rmb_vnd, rate_usd_vnd, incoterm, salesperson, owner_user_id,
                total_equip_rmb, total_equip_usd, total_equip_vnd,
                total_ei_rmb, total_ei_usd, total_ei_vnd
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            proj["contract_no"], proj["customer"], proj["contract_date"],
            proj["signing_parties"], proj["contract_currency"],
            proj["rate_rmb_vnd"], proj["rate_usd_vnd"], proj["incoterm"], proj["salesperson"],
            (proj.get("salesperson") or "").strip().lower(),
            proj["total_equip_rmb"], proj["total_equip_usd"], proj["total_equip_vnd"],
            proj["total_ei_rmb"], proj["total_ei_usd"], proj["total_ei_vnd"]
        ))


def seed_approval_requests(c):
    """注入示例审批数据，所有审批均来自「界面/操作权限」中勾选了"发起审批"的区块。

    字段说明（对应实际表结构）：
      - title：审批事项标题 = 权限区块名称
      - requester：发起人（用户名）
      - approvers：审批人（多人 JSON 数组）
      - created_at：发起日期
      - resolved_at：审批日期
      - status：pending / approved / rejected
      - result_note：审批结果/意见
      - content：审批内容 = 该区块"默认保留信息"列的说明文字
      - block_id / block_name：对应权限区块
    """
    cnt = c.execute("SELECT COUNT(*) FROM approval_requests").fetchone()[0]
    if cnt > 0:
        return
    now = time.strftime("%Y-%m-%d %H:%M:%S")

    # 与前端 i18n 中 user_block_<bid>_info 保持一致的说明文字（审批内容）
    INFO = {
        "DB-P1": "保留默认=不显示此图（C类全公司聚合，需「特别授权看全公司」才显示按省份柱图） · 默认不显示",
        "DB-B1": "保留默认=不显示此图（C类全公司聚合，需「特别授权看全公司」才显示按BU柱图） · 默认不显示",
        "DB-C1": "保留默认=不显示此图（C类全公司聚合，需「特别授权看全公司」才显示按建设阶段柱图） · 默认不显示",
        "CRM-D2": "保留默认=列表/详情显示「编辑」按钮，可编辑数据范围内的CRM项目 · 默认显示",
        "CRM-D3": "保留默认=列表/详情显示「删除」按钮，可删除数据范围内的CRM项目 · 默认显示",
        "CRM-E1": "保留默认=列表顶部显示「导出」按钮，导出数据范围内的项目 · 默认显示",
        "WON-D2": "保留默认=列表/详情显示「编辑」按钮，可编辑数据范围内的Won项目 · 默认显示",
        "WON-D4": "保留默认=详情显示「查看CPR报告」按钮，可打开数据范围内项目的智能报告 · 默认显示",
        "APP-L3": "保留默认=不显示此入口（C类全公司记录，需「特别授权看全公司」才显示） · 默认不显示",
        "USR-D1": "保留默认=不显示此入口（S类敏感操作，仅管理员可见） · 默认不显示",
    }
    # (block_id, block_name, 发起人, 审批人, 发起日期, 审批日期, 状态, 审批意见)
    samples = [
        ("DB-P1", "按省份统计双轴柱图", "cuong", ["tom", "dgm1"], "2026-08-10 09:12", "2026-08-11 15:40", "approved", "已阅，同意开放该图表。"),
        ("DB-B1", "按BU统计双轴柱图", "james", ["tom", "travis"], "2026-08-12 14:03", "2026-08-13 10:25", "approved", "BU 聚合信息可开放。"),
        ("DB-C1", "按建设情况统计双轴柱图", "khoa", ["tom", "salesdir1"], "2026-08-14 11:20", "", "pending", ""),
        ("CRM-E1", "导出Excel", "ali", ["travis", "fin1"], "2026-08-18 16:45", "", "pending", ""),
        ("WON-D4", "查看CPR报告", "linh", ["tom", "gm2"], "2026-08-19 08:50", "2026-08-20 17:10", "rejected", "权限过高，暂不同意。"),
        ("APP-L3", "全公司审批记录", "minh", ["tom", "dgm1"], "2026-08-21 13:30", "2026-08-22 09:15", "approved", "已确认可查看。"),
    ]
    for bid, bname, requester, approvers, created, resolved, status, note in samples:
        c.execute("""
            INSERT INTO approval_requests
            (title, requester, approvers, created_at, resolved_at, status, result_note, content, block_id, block_name)
            VALUES (?,?,?,?,?,?,?,?,?,?)
        """, (bname, requester, json.dumps(approvers, ensure_ascii=False), created, resolved,
              status, note, INFO.get(bid, ""), bid, bname))
    print("[init_db] approval_requests 已自动注入示例审批数据")


def migrate_crm_seed(c):
    """修正旧版种子数据，使其与模态框下拉选项值一致。

    旧版种子将省份存为中文、BU 存为 "GS/AGI/BOD"、建设情况存为中文，
    而前端下拉框的 <option value> 分别为越南语省名、BU 代码、建设情况代码，
    导致模态框下拉框无法匹配、必填校验失败（表现为按钮无反应）。
    本函数仅处理种子数据（quote_no 形如 QT-2026-xxx），不改动用户录入的数据。
    """
    # 旧中文省名 -> 越南语省名（对应前端 provinceOptionsHtml 的 value）
    province_map = {
        "北江": "Bắc Ninh", "北宁": "Bắc Ninh", "海防": "Hải Phòng",
        "胡志明市": "TP. Hồ Chí Minh", "河内": "Hà Nội", "隆安": "Tây Ninh",
        "同奈": "Đồng Nai", "平阳": "Vĩnh Long", "广宁": "Quảng Ninh",
        "太原": "Thái Nguyên",
    }
    # 旧 "GS/AGI/BOD" -> BU 代码
    bu_map = {"GS": "pig_farm", "AGI": "broiler_farm", "BOD": "chicken_egg_farm"}
    # 旧中文建设情况 -> 建设情况代码
    cons_map = {
        "钢结构": "land", "土建": "license", "机电": "design", "消防": "bidding",
        "给排水": "supplier_sel", "装修": "nearing",
    }

    rows = c.execute(
        "SELECT id, province, bu, construction, startup_pct, sign_pct "
        "FROM crm_projects WHERE quote_no LIKE 'QT-2026-%'"
    ).fetchall()
    changed = 0
    for rid, province, bu, cons, startup_pct, sign_pct in rows:
        new_prov = province_map.get(province, province)
        new_bu = bu_map.get(bu, bu)
        new_cons = cons_map.get(cons, cons)

        def clamp_pct(v):
            try:
                n = int(str(v).replace("%", ""))
            except (TypeError, ValueError):
                return v
            return str(max(0, min(100, n)))

        new_startup = clamp_pct(startup_pct)
        new_sign = clamp_pct(sign_pct)

        if (new_prov != province or new_bu != bu or new_cons != cons
                or new_startup != startup_pct or new_sign != sign_pct):
            c.execute(
                "UPDATE crm_projects SET province=?, bu=?, construction=?, "
                "startup_pct=?, sign_pct=? WHERE id=?",
                (new_prov, new_bu, new_cons, new_startup, new_sign, rid)
            )
            changed += 1
    if changed:
        print("[init_db] 已修正 {} 条 CRM 种子数据（省份/BU/建设情况/概率）".format(changed))


def migrate_crm_seed_v2(c):
    """修正 CRM 种子数据的展示一致性与多样性：

    1. 三币联动：将 q1~q7 的 USD/VND 按各项目自身的汇率换算，使 RMB/USD/VND 三币一致；
    2. 负责人电话：多样化越南手机号，避免千篇一律；
    3. 公司信息：结合客户名 + 越南不同地址，避免全部相同；
    4. 启动概率/签约概率：多样化，避免全部为 100%（签约概率不高于启动概率）。
    仅处理种子数据（quote_no 形如 QT-2026-xxx），不改动用户录入的数据。
    """
    startup_pcts = [30, 45, 60, 75, 80, 90, 55, 70, 85, 95, 40, 65, 50, 88, 72,
                    35, 58, 68, 92, 48, 62, 38, 82, 52, 78, 42, 96, 25, 64, 74]
    sign_pcts =    [15, 30, 45, 60, 70, 80, 40, 55, 70, 85, 25, 50, 35, 72, 55,
                    20, 42, 52, 80, 32, 46, 22, 68, 36, 60, 28, 85, 15, 50, 62]
    phone_pref = ["09", "03", "07", "08", "05"]
    addr_cities = ["胡志明市", "河内", "海防", "岘港", "同奈", "北宁", "太原", "广宁", "西宁", "永隆"]
    addr_zone = ["工业园区", "高新技术区", "出口加工区", "经济开发区", "商贸中心"]
    company_extra = ["越南分公司", "驻越办事处", "制造基地", "项目工程部", "区域服务中心"]

    def to_num(v):
        try:
            return float(v)
        except (TypeError, ValueError):
            return 0.0

    rows = c.execute(
        "SELECT id, customer, rate_rmb_vnd, rate_usd_vnd, "
        "q1_rmb,q1_usd,q1_vnd,q2_rmb,q2_usd,q2_vnd,q3_rmb,q3_usd,q3_vnd,"
        "q4_rmb,q4_usd,q4_vnd,q5_rmb,q5_usd,q5_vnd,q6_rmb,q6_usd,q6_vnd,"
        "q7_rmb,q7_usd,q7_vnd "
        "FROM crm_projects WHERE quote_no LIKE 'QT-2026-%' ORDER BY id"
    ).fetchall()
    changed = 0
    for idx, row in enumerate(rows):
        rid = row["id"]
        customer = row["customer"] or ""
        rate_rmb_vnd = to_num(row["rate_rmb_vnd"])
        rate_usd_vnd = to_num(row["rate_usd_vnd"])
        # 三币联动：以 RMB 为基准，按项目汇率换算 USD / VND（与模态框 crmQuoteLink 一致）
        q_vals = []
        for qn in range(1, 8):
            rmb = to_num(row["q{}_rmb".format(qn)])
            vnd = round(rmb * rate_rmb_vnd) if rate_rmb_vnd > 0 else to_num(row["q{}_vnd".format(qn)])
            usd = round(vnd / rate_usd_vnd) if rate_usd_vnd > 0 else to_num(row["q{}_usd".format(qn)])
            q_vals.extend([round(rmb), usd, vnd])
        # 电话 / 公司信息 / 概率 多样化
        phone = phone_pref[idx % len(phone_pref)] + "{:08d}".format((idx * 137) % 100000000)
        company = "{}·{}·{} · {}".format(customer, addr_cities[idx % len(addr_cities)],
                                         addr_zone[idx % len(addr_zone)],
                                         company_extra[idx % len(company_extra)])
        startup = startup_pcts[idx % len(startup_pcts)]
        sign = sign_pcts[idx % len(sign_pcts)]
        c.execute(
            "UPDATE crm_projects SET "
            "q1_rmb=?,q1_usd=?,q1_vnd=?,q2_rmb=?,q2_usd=?,q2_vnd=?,"
            "q3_rmb=?,q3_usd=?,q3_vnd=?,q4_rmb=?,q4_usd=?,q4_vnd=?,"
            "q5_rmb=?,q5_usd=?,q5_vnd=?,q6_rmb=?,q6_usd=?,q6_vnd=?,"
            "q7_rmb=?,q7_usd=?,q7_vnd=?,manager_phone=?,company_info=?,"
            "startup_pct=?,sign_pct=? WHERE id=?",
            q_vals + [phone, company, str(startup), str(sign), rid]
        )
        changed += 1
    if changed:
        print("[init_db] 已修正 {} 条 CRM 种子数据（三币联动/电话/公司信息/概率 多样化）".format(changed))


init_db()


# ===================== 工具 =====================
def safe_name(s):
    s = os.path.basename(s or "")
    s = re.sub(r"[^A-Za-z0-9_.-]", "_", s) if False else s.replace("\\", "_").replace("/", "_")
    return s or "file"

ALLOWED_EXT = {".pdf", ".jpg", ".jpeg", ".png", ".gif", ".webp", ".xls", ".xlsx", ".doc", ".docx", ".txt"}

# ===================== API：登录 / 密码 =====================
def _verify_cloud_password(stored, password):
    """校验云端 Worker 同款密码：pbkdf2$迭代$盐hex$哈希hex（PBKDF2-SHA256/256位）。
    历史明文（无前缀）直接比对。"""
    try:
        stored = str(stored or "")
        if not stored.startswith("pbkdf2$"):
            return stored == password
        parts = stored.split("$")
        it = int(parts[1]) if parts[1].isdigit() else 100000
        salt = bytes.fromhex(parts[2])
        expected = parts[3]
        dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, it, dklen=32)
        return dk.hex() == expected
    except Exception:
        return False


def _cloud_mirror_login(conn, username, password):
    """桌面版离线登录兜底：用同步下来的云端用户镜像（_cloud_users）校验。

    返回 (user_dict, None) 或 (None, 错误消息)。镜像不存在时返回 (None, '')，
    由调用方回退到「用户名不存在」。"""
    try:
        cols = [r[1] for r in conn.execute("PRAGMA table_info(_cloud_users)").fetchall()]
        if "username" not in cols:
            return None, ''
        row = conn.execute("SELECT * FROM _cloud_users WHERE username=?", (username,)).fetchone()
        if not row:
            return None, ''
        if str(row["status"] or "active") != "active":
            return None, "该账号已被禁用"
        if not _verify_cloud_password(row["password"], password):
            return None, "密码错误"
        try:
            perms = json.loads(row["perms"]) if row["perms"] else {}
        except Exception:
            perms = {}
        is_admin = False
        try:
            is_admin = bool(conn.execute(
                "SELECT 1 FROM _cloud_managers WHERE username=?", (username,)).fetchone())
        except Exception:
            pass
        if not is_admin and (row["role"] or "") == "管理员":
            is_admin = True
        def _ids(raw):
            try:
                v = json.loads(raw or "[]")
                return v if isinstance(v, list) else []
            except Exception:
                return []
        return {
            "username": row["username"],
            "real_name": row["real_name"] or "",
            "role": row["role"] or "",
            "position": row["position"] or "",
            "is_admin": bool(is_admin),
            "status": "active",
            "vis_he_can_see": _ids(row["vis_he_can_see"]),
            "vis_can_see_me": _ids(row["vis_can_see_me"]),
            "perms": perms,
            "offline": True,
        }, None
    except Exception:
        return None, ''


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json(force=True, silent=True) or {}
    # 统一转小写：手机键盘首字母自动大写会输入 "Tom"，而库存的是 "tom"，
    # SQLite 的 = 比较大小写敏感会导致登录失败。这里归一化，任何大小写都能登录。
    username = (data.get("username") or "").strip().lower()
    password = data.get("password") or ""
    if not username or not password:
        return jsonify({"ok": False, "error": "请输入用户名和密码"})
    conn = get_db()
    row = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
    if not row:
        # 本机 users 表没有该账号 → 尝试【云端用户目录镜像】离线登录（桌面版）。
        # 镜像由 sync_client.sync_users() 随每次同步从云端单向拉下来，
        # 密码是云端同款 PBKDF2 哈希，本机离线也能校验，效果与联网登录一致。
        cuser, cerr = _cloud_mirror_login(conn, username, password)
        if cuser is None:
            conn.close()
            return jsonify({"ok": False, "error": cerr or "用户名不存在"})
        try:
            conn.execute("INSERT INTO login_history (username, ip_address, user_agent) VALUES (?, ?, ?)",
                         (username, request.remote_addr or '', (request.headers.get('User-Agent') or '')[:200]))
            conn.commit()
        except Exception:
            pass
        conn.close()
        return jsonify({"ok": True, "user": cuser})
    if row["status"] != "active":
        conn.close()
        return jsonify({"ok": False, "error": "该账号已被禁用"})
    if row["password"] != password:
        conn.close()
        return jsonify({"ok": False, "error": "密码错误"})
    # 记录登录（成功才记录）
    try:
        ip = request.remote_addr or ''
        ua = request.headers.get('User-Agent', '')[:200]
        conn.execute("INSERT INTO login_history (username, ip_address, user_agent) VALUES (?, ?, ?)",
                     (username, ip, ua))
        conn.commit()
    except Exception as e:
        print(f"[Login] Failed to record login history: {e}")
    def _col(k, d=""):
        try:
            v = row[k]
            return v if v is not None else d
        except Exception:
            return d
    role_val = _col("role")
    role_l = (role_val or "").lower()
    is_admin = _is_manager(conn, _col("username"))
    perms_raw = _col("perms", "{}")
    try:
        perms = json.loads(perms_raw) if perms_raw else {}
    except Exception:
        perms = {}
    perms = _norm_user_perms(perms, conn)
    def _ids(raw):
        try:
            v = json.loads(raw or "[]")
            return v if isinstance(v, list) else []
        except Exception:
            return []
    conn.close()
    return jsonify({"ok": True, "user": {
        "username": _col("username"),
        "real_name": _col("real_name"),
        "role": role_val,
        "position": _col("position"),
        "is_admin": bool(is_admin),
        "status": _col("status", "active"),
        "vis_he_can_see": _ids(_col("vis_he_can_see", "[]")),
        "vis_can_see_me": _ids(_col("vis_can_see_me", "[]")),
        # 操作权限决策：{bid: {decision, approvers}}，前端据此做界面拦截
        "perms": perms
    }})


def _is_manager(conn, username):
    """判断用户是否为管理员：在自由任命的管理员表中，或角色为“管理员”。"""
    if not username:
        return False
    row = conn.execute("SELECT 1 FROM managers WHERE username=?", (username,)).fetchone()
    if row:
        return True
    u = conn.execute("SELECT role FROM users WHERE username=?", (username,)).fetchone()
    return bool(u) and (u["role"] or "") == "管理员"


def _manager_usernames(conn):
    """返回当前所有管理员账号列表（只保留 users 表里真实存在的账号，自动清理残留）。"""
    rows = conn.execute(
        "SELECT m.username FROM managers m "
        "INNER JOIN users u ON lower(u.username) = lower(m.username) "
        "ORDER BY m.username"
    ).fetchall()
    return [r["username"] for r in rows]


@app.route("/api/me", methods=["GET"])
def api_me():
    """前端恢复 sessionStorage 中的 authUser 后，用 username 刷新最新 role/is_admin/perms，
    避免旧缓存（没有 is_admin 字段）导致管理员入口/图表被隐藏。"""
    username = (request.args.get("username") or "").strip()
    if not username:
        return jsonify({"ok": False, "error": "missing username"})
    conn = get_db()
    row = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
    if not row:
        conn.close()
        return jsonify({"ok": False, "error": "user not found"})
    def _col(k, d=""):
        try:
            v = row[k]
            return v if v is not None else d
        except Exception:
            return d
    is_admin = _is_manager(conn, _col("username"))
    perms_raw = _col("perms", "{}")
    try:
        perms = json.loads(perms_raw) if perms_raw else {}
    except Exception:
        perms = {}
    perms = _norm_user_perms(perms, conn)
    def _ids(raw):
        try:
            v = json.loads(raw or "[]")
            return v if isinstance(v, list) else []
        except Exception:
            return []
    conn.close()
    return jsonify({"ok": True, "user": {
        "username": _col("username"),
        "real_name": _col("real_name"),
        "role": _col("role"),
        "position": _col("position"),
        "is_admin": bool(is_admin),
        "status": _col("status", "active"),
        "vis_he_can_see": _ids(_col("vis_he_can_see", "[]")),
        "vis_can_see_me": _ids(_col("vis_can_see_me", "[]")),
        "perms": perms
    }})

# ============================================================
# 看板聚合统计：复刻云端 /api/dashboard-stats，供桌面版使用
# ============================================================
def _dash_sum_with_fallback(primary, fallback, suffix):
    p = primary + "_" + suffix
    # fallback 传 '0' 表示「没有备用列，按 0 计」；直接拼成 0_rmb 会被 SQLite
    # 解析成非法 token（unrecognized token: "0_rmb"）导致 /api/dashboard-stats 500。
    if not fallback or fallback == "0":
        f = "0"
    else:
        f = fallback + "_" + suffix
    return (f"SUM(CASE WHEN {p} IS NULL THEN COALESCE(CAST({f} AS REAL),0) "
            f"ELSE CAST({p} AS REAL) END)")


@app.route("/api/dashboard-stats", methods=["GET"])
def api_dashboard_stats():
    """返回 CRM/WON/LOST 的计数与三币汇总，降低前端全量拉表开销。"""
    username = (request.headers.get("X-User-Name") or "").strip()

    def _stats_for(table, block_id, primary, fallback, status_where=None):
        vs_clause, vs_params = _visible_scope(username, block_id)
        where = ["lower(salesperson) <> 'agi-gs internal'"]
        params = []
        if status_where:
            where.append(status_where)
        if vs_clause:
            where.append("(" + vs_clause + ")")
            params.extend(vs_params)
        where_sql = " WHERE " + " AND ".join(where)
        sql = (f"SELECT COUNT(*) AS cnt, "
               f"{_dash_sum_with_fallback(primary, fallback, 'rmb')} AS rmb, "
               f"{_dash_sum_with_fallback(primary, fallback, 'usd')} AS usd, "
               f"{_dash_sum_with_fallback(primary, fallback, 'vnd')} AS vnd "
               f"FROM {table}{where_sql}")
        conn = get_db()
        try:
            row = conn.execute(sql, params).fetchone()
            return {
                "count": row["cnt"] or 0,
                "rmb": round(row["rmb"] or 0),
                "usd": round(row["usd"] or 0),
                "vnd": round(row["vnd"] or 0),
            }
        finally:
            conn.close()

    try:
        # 看板顶部统计卡统一受 DB-S1 数据范围控制，与三模块列表权限独立
        crm = _stats_for(
            "crm_projects", "DB-S1", "q1", "0",
            status_where="(status='active' OR status IS NULL OR status='')"
        )
        won = _stats_for("won_projects", "DB-S1", "total_ei", "equip")
        lost = _stats_for("lost_projects", "DB-S1", "q1", "0")
        return jsonify({"ok": True, "crm": crm, "won": won, "lost": lost})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


# ==================== 汇率看板 ====================
# 汇率数据统一由系统既有的 /api/fx-rates（见下方 api_fx_rates）提供：
#   读库缓存 + 当月缺失后台补抓，返回 {ok, labels:[YYYY-MM], series:{usd_cny,usd_vnd,cny_vnd}}。
# 此处不再重复定义路由，避免 Flask 端点名冲突导致应用无法启动。


# ==================== 个人佣金 · 修改金额审批 ====================
# 规则（后门三人组专用）：
#   1. 仅 tom / cuong / travis 可发起佣金金额修改；
#   2. 审批发给【除请求者外的另外两人】；
#   3. 两人都同意 → 通过，系统自动把金额改成新值；任一拒绝 → 作废；
#   4. 只支持改金额，不支持改付款日期；
#   5. 只在「个人佣金 → 查看与审批」展示，不混入全局审批页。
COMMISSION_APPROVERS = ["tom", "cuong", "travis"]


def _comm_now():
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _comm_approvers_for(requester):
    r = str(requester or "").strip().lower()
    return [u for u in COMMISSION_APPROVERS if u != r]


# ==================== 个人佣金 · 佣金记录持久化（SQLite） ====================
#   设计要点：
#     · 案例数据（DEMO2 灌入）写库时打 is_demo=1；真实录入的数据 is_demo=0
#     · 最后「清空 DEMO」只需 DELETE ... WHERE is_demo=1，绝不会误伤真实数据
#     · 主记录按 contract 唯一索引 upsert；受益人按 record_id 整组替换（明细 payments 存 JSON）

def _comm_rec_to_dict(row, conn):
    """把主记录行 + 其受益人（含 payments 明细）组装成前端 COMM_RECORDS 的元素结构"""
    d = dict(row)
    item = {
        "contract": d.get("contract") or "",
        "parties": d.get("parties") or "",
        "group": d.get("group_name") or "",
        "date": d.get("sign_date") or "",
        "depositDate": d.get("deposit_date") or "",
        "currency": d.get("currency") or "",
        "equipRMB": d.get("equip_rmb") or "",
        "equipUSD": d.get("equip_usd") or "",
        "equipVND": d.get("equip_vnd") or "",
        "rateRMB": d.get("rate_rmb") or "",
        "rateUSD": d.get("rate_usd") or "",
        "remark": d.get("remark") or "",
        "isDemo": int(d.get("is_demo") or 0),
        "beneficiaries": [],
    }
    bens = conn.execute(
        "SELECT * FROM commission_beneficiaries WHERE record_id=? ORDER BY ben_index",
        (d.get("id"),)).fetchall()
    for b in bens:
        bd = dict(b)
        try:
            payments = json.loads(bd.get("payments") or "[]")
        except Exception:
            payments = []
        # 明细里的空字符串统一还原为 ''（前端 parseMoney 兼容）
        for p in payments:
            for k, v in list(p.items()):
                if v is None:
                    p[k] = ""
        item["beneficiaries"].append({
            "name": bd.get("name") or "",
            "currency": bd.get("currency") or "",
            "totalRMB": bd.get("total_rmb") or "",
            "totalUSD": bd.get("total_usd") or "",
            "totalVND": bd.get("total_vnd") or "",
            "signDate": bd.get("sign_date") or "",
            "depositDate": bd.get("deposit_date") or "",
            "paidRMB": bd.get("paid_rmb") or "",
            "paidUSD": bd.get("paid_usd") or "",
            "paidVND": bd.get("paid_vnd") or "",
            "payCount": bd.get("pay_count") or 0,
            "unpaidRMB": bd.get("unpaid_rmb") or "",
            "unpaidUSD": bd.get("unpaid_usd") or "",
            "unpaidVND": bd.get("unpaid_vnd") or "",
            "payNature": bd.get("pay_nature") or "",
            "note": bd.get("note") or "",
            "payments": payments,
        })
    return item


@app.route("/api/commission/records", methods=["GET"])
def api_comm_records_get():
    conn = get_db()
    try:
        rows = conn.execute(
            "SELECT * FROM commission_records ORDER BY id").fetchall()
        items = [_comm_rec_to_dict(r, conn) for r in rows]
        return jsonify({"ok": True, "items": items})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()


@app.route("/api/commission/records", methods=["POST"])
def api_comm_records_save():
    """保存一条佣金记录（按 contract upsert），payload 形如：
       { record: {...前端 COMM_RECORDS 元素...}, isDemo: 0|1 }"""
    body = request.get_json(force=True, silent=True) or {}
    rec = body.get("record") or {}
    contract = str(rec.get("contract") or "").strip()
    if not contract:
        return jsonify({"error": "缺少合同编号"}), 400

    is_demo = 1 if (body.get("isDemo") or rec.get("isDemo")) else 0
    bens = rec.get("beneficiaries") or []
    conn = get_db()
    try:
        row = conn.execute(
            "SELECT id FROM commission_records WHERE contract=?", (contract,)).fetchone()
        if row:
            rid = row["id"]
            conn.execute(
                "UPDATE commission_records SET parties=?, group_name=?, sign_date=?,"
                " deposit_date=?, currency=?, equip_rmb=?, equip_usd=?, equip_vnd=?,"
                " rate_rmb=?, rate_usd=?, remark=?, is_demo=?,"
                " updated_at=datetime('now','localtime') WHERE id=?",
                (str(rec.get("parties") or ""), str(rec.get("group") or ""),
                 str(rec.get("date") or ""), str(rec.get("depositDate") or ""),
                 str(rec.get("currency") or ""), str(rec.get("equipRMB") or ""),
                 str(rec.get("equipUSD") or ""), str(rec.get("equipVND") or ""),
                 str(rec.get("rateRMB") or ""), str(rec.get("rateUSD") or ""),
                 str(rec.get("remark") or ""), is_demo, rid))
        else:
            cur = conn.execute(
                "INSERT INTO commission_records (contract, parties, group_name,"
                " sign_date, deposit_date, currency, equip_rmb, equip_usd, equip_vnd,"
                " rate_rmb, rate_usd, remark, is_demo)"
                " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (contract, str(rec.get("parties") or ""), str(rec.get("group") or ""),
                 str(rec.get("date") or ""), str(rec.get("depositDate") or ""),
                 str(rec.get("currency") or ""), str(rec.get("equipRMB") or ""),
                 str(rec.get("equipUSD") or ""), str(rec.get("equipVND") or ""),
                 str(rec.get("rateRMB") or ""), str(rec.get("rateUSD") or ""),
                 str(rec.get("remark") or ""), is_demo))
            rid = cur.lastrowid

        # 受益人整组替换（明细 payments 序列化为 JSON）
        conn.execute("DELETE FROM commission_beneficiaries WHERE record_id=?", (rid,))
        for i, b in enumerate(bens):
            if not isinstance(b, dict):
                continue
            conn.execute(
                "INSERT INTO commission_beneficiaries (record_id, ben_index, name,"
                " currency, total_rmb, total_usd, total_vnd, sign_date, deposit_date,"
                " paid_rmb, paid_usd, paid_vnd, pay_count, unpaid_rmb, unpaid_usd,"
                " unpaid_vnd, pay_nature, note, payments)"
                " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (rid, i, str(b.get("name") or ""), str(b.get("currency") or ""),
                 str(b.get("totalRMB") or ""), str(b.get("totalUSD") or ""),
                 str(b.get("totalVND") or ""), str(b.get("signDate") or ""),
                 str(b.get("depositDate") or ""), str(b.get("paidRMB") or ""),
                 str(b.get("paidUSD") or ""), str(b.get("paidVND") or ""),
                 int(b.get("payCount") or 0), str(b.get("unpaidRMB") or ""),
                 str(b.get("unpaidUSD") or ""), str(b.get("unpaidVND") or ""),
                 str(b.get("payNature") or ""), str(b.get("note") or ""),
                 json.dumps(b.get("payments") or [], ensure_ascii=False)))
        conn.commit()
        return jsonify({"ok": True, "id": rid, "saved": len(bens)})
    except Exception as e:
        try:
            conn.rollback()
        except Exception:
            pass
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()


@app.route("/api/commission/records/demo", methods=["DELETE"])
def api_comm_records_clear_demo():
    """清除全部 DEMO 案例（is_demo=1），真实录入的数据（is_demo=0）一律保留"""
    conn = get_db()
    try:
        ids = [r["id"] for r in conn.execute(
            "SELECT id FROM commission_records WHERE is_demo=1").fetchall()]
        n = 0
        if ids:
            ph = ",".join("?" * len(ids))
            conn.execute(
                "DELETE FROM commission_beneficiaries WHERE record_id IN (%s)" % ph, ids)
            n = conn.execute(
                "DELETE FROM commission_records WHERE id IN (%s)" % ph, ids).rowcount
        conn.commit()
        return jsonify({"ok": True, "cleared": (n if n and n > 0 else len(ids))})
    except Exception as e:
        try:
            conn.rollback()
        except Exception:
            pass
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()


@app.route("/api/commission/records/<contract>", methods=["DELETE"])
def api_comm_records_delete(contract):
    """删除指定合同编号的记录（用于前端删除单条）"""
    conn = get_db()
    try:
        row = conn.execute(
            "SELECT id FROM commission_records WHERE contract=?", (contract,)).fetchone()
        if not row:
            return jsonify({"error": "记录不存在"}), 404
        rid = row["id"]
        conn.execute("DELETE FROM commission_beneficiaries WHERE record_id=?", (rid,))
        conn.execute("DELETE FROM commission_records WHERE id=?", (rid,))
        conn.commit()
        return jsonify({"ok": True})
    except Exception as e:
        try:
            conn.rollback()
        except Exception:
            pass
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()


@app.route("/api/commission/amount-requests", methods=["GET", "POST"])
def api_comm_amt_requests():
    conn = get_db()
    if request.method == "GET":
        rows = conn.execute(
            "SELECT * FROM comm_amt_requests ORDER BY id DESC").fetchall()
        conn.close()
        items = []
        for r in rows:
            d = dict(r)
            # 重新激活类申请（req_key 以 REACTIVATE 开头）→ 前端据此外挂解锁而非改金额
            d["reactivate"] = str(d.get("req_key") or "").startswith("REACTIVATE")
            items.append(d)
        return jsonify({"ok": True, "items": items})

    body = request.get_json(force=True, silent=True) or {}
    requester = str(body.get("requester") or "").strip().lower()
    if requester not in COMMISSION_APPROVERS:
        conn.close()
        return jsonify({"error": "只有授权人员可以发起佣金金额修改"}), 403

    is_react = bool(body.get("reactivate"))
    old_amount = str(body.get("old_amount") or "").strip()
    new_amount = str(body.get("new_amount") or "").strip()
    # 重新激活类申请：不携带新旧金额，跳过金额校验（req_key 加 REACTIVATE 前缀防重）
    if not is_react and (not new_amount or new_amount == old_amount):
        conn.close()
        return jsonify({"error": "请填写与原来不同的新金额"}), 400

    a1, a2 = _comm_approvers_for(requester)
    req_key = "||".join([
        "REACTIVATE" if is_react else str(body.get("contract_no") or ""),
        str(body.get("beneficiary") or ""),
        str(body.get("pay_no") or ""),
    ])
    dup = conn.execute(
        "SELECT id FROM comm_amt_requests WHERE req_key=? AND status='pending'",
        (req_key,)).fetchone()
    if dup:
        conn.close()
        return jsonify({"error": "该笔金额已有待审批的修改申请"}), 409

    conn.execute(
        "INSERT INTO comm_amt_requests (req_key, contract_no, beneficiary, pay_no,"
        " currency, old_amount, new_amount, reason, requester, approver1, approver2,"
        " status, created_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,'pending',?)",
        (req_key, str(body.get("contract_no") or ""),
         str(body.get("beneficiary") or ""), str(body.get("pay_no") or ""),
         str(body.get("currency") or ""), old_amount, new_amount,
         str(body.get("reason") or ""), requester, a1, a2, _comm_now()))
    conn.commit()
    conn.close()
    return jsonify({"ok": True, "approvers": [a1, a2]})


@app.route("/api/commission/amount-requests/<int:rid>/resolve", methods=["POST"])
def api_comm_amt_resolve(rid):
    body = request.get_json(force=True, silent=True) or {}
    action = str(body.get("action") or "").strip().lower()
    resolver = str(body.get("resolver") or "").strip().lower()
    if action not in ("approve", "reject"):
        return jsonify({"error": "操作无效"}), 400

    conn = get_db()
    row = conn.execute(
        "SELECT * FROM comm_amt_requests WHERE id=?", (rid,)).fetchone()
    if not row:
        conn.close()
        return jsonify({"error": "审批不存在"}), 404
    if row["status"] != "pending":
        conn.close()
        return jsonify({"error": "该审批已结束"}), 409
    if resolver not in (row["approver1"], row["approver2"]):
        conn.close()
        return jsonify({"error": "你不是该笔审批的审批人"}), 403

    dec_field = "dec1" if resolver == row["approver1"] else "dec2"
    conn.execute(
        "UPDATE comm_amt_requests SET %s=? WHERE id=?" % dec_field, (action, rid))
    conn.commit()

    cur = conn.execute(
        "SELECT * FROM comm_amt_requests WHERE id=?", (rid,)).fetchone()
    status = "pending"
    decs = [cur["dec1"], cur["dec2"]]
    if "reject" in decs:
        status = "rejected"
    elif cur["dec1"] == "approve" and cur["dec2"] == "approve":
        status = "approved"   # 两人都同意 → 通过，前端据此外挂新金额

    if status != "pending":
        conn.execute(
            "UPDATE comm_amt_requests SET status=?, resolved_at=? WHERE id=?",
            (status, _comm_now(), rid))
        conn.commit()
    conn.close()
    return jsonify({
        "ok": True,
        "status": status,
        "new_amount": cur["new_amount"] if status == "approved" else None,
    })


@app.route("/api/perm-version", methods=["GET"])
def api_perm_version():
    """前端轮询：返回某用户权限版本号。版本变化即代表其 perms/role/status 已变更，
    前端据此立即刷新本地会话缓存（无需重新登录）。"""
    username = (request.args.get("username") or "").strip()
    if not username:
        return jsonify({"ok": False, "error": "missing username"})
    return jsonify({"ok": True, "username": username, "version": get_perm_version(username)})


@app.route("/api/login-history", methods=["GET"])
def get_login_history():
    """获取登录记录统计数据"""
    conn = get_db()
    # 获取每月每用户的登录次数
    monthly = conn.execute("""
        SELECT strftime('%Y-%m', login_time) as month,
               username,
               COUNT(*) as count
        FROM login_history
        GROUP BY month, username
        ORDER BY month DESC, username
    """).fetchall()
    # 获取每年每用户的登录次数
    yearly = conn.execute("""
        SELECT strftime('%Y', login_time) as year,
               username,
               COUNT(*) as count
        FROM login_history
        GROUP BY year, username
        ORDER BY year DESC, username
    """).fetchall()
    # 获取当月每用户的登录次数
    current_month = conn.execute("""
        SELECT username,
               COUNT(*) as count
        FROM login_history
        WHERE strftime('%Y-%m', login_time) = strftime('%Y-%m', 'now', 'localtime')
        GROUP BY username
        ORDER BY count DESC, username
    """).fetchall()
    # 获取当年每用户的登录次数
    current_year = conn.execute("""
        SELECT username,
               COUNT(*) as count
        FROM login_history
        WHERE strftime('%Y', login_time) = strftime('%Y', 'now', 'localtime')
        GROUP BY username
        ORDER BY count DESC, username
    """).fetchall()
    conn.close()
    return jsonify({
        "ok": True,
        "monthly": [dict(r) for r in monthly],
        "yearly": [dict(r) for r in yearly],
        "userMonthly": [dict(r) for r in current_month],
        "userYearly": [dict(r) for r in current_year]
    })

@app.route("/api/change-password", methods=["POST"])
def change_password():
    """Reset Password：校验旧密码，设置新密码"""
    data = request.get_json(force=True, silent=True) or {}
    username = (data.get("username") or "").strip()
    old_pw = data.get("old_password") or ""
    new_pw = data.get("new_password") or ""
    if not username:
        return jsonify({"ok": False, "error": "缺少用户名"})
    if len(new_pw) < 6:
        return jsonify({"ok": False, "error": "新密码长度至少 6 位"})
    conn = get_db()
    row = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
    if not row:
        conn.close()
        return jsonify({"ok": False, "error": "用户名不存在"})
    if row["password"] != old_pw:
        conn.close()
        return jsonify({"ok": False, "error": "旧密码错误"})
    conn.execute("UPDATE users SET password=? WHERE username=?", (new_pw, username))
    conn.commit()
    conn.close()
    return jsonify({"ok": True, "message": "密码修改成功"})

@app.route("/api/forget-password", methods=["POST"])
def forget_password():
    """忘记密码：不再直接重置/返回临时密码。
    流程：根据该用户配置的 forgot_approvers（忘记密码审批人，tom 默认）创建一条
    PWD-FORGET 审批请求 → 审批人待办角标 +1 → 任一审批人"通过"后，
    密码自动重置为初始密码 66668888（DEFAULT_INIT_PASSWORD）。"""
    data = request.get_json(force=True, silent=True) or {}
    username = (data.get("username") or "").strip()
    if not username:
        return jsonify({"ok": False, "error": "请输入用户名"})
    conn = get_db()
    row = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
    if not row:
        conn.close()
        return jsonify({"ok": False, "error": "用户名不存在"})
    # 该用户的忘记密码审批人（默认 tom；空则兜底 tom + 全体管理员）
    try:
        approvers = json.loads(row["forgot_approvers"] or "[]")
    except Exception:
        approvers = []
    approvers = [a for a in approvers if a]
    if not approvers:
        approvers = ["tom"]
        try:
            for m in conn.execute("SELECT username FROM managers"):
                if m["username"] not in approvers:
                    approvers.append(m["username"])
        except Exception:
            pass
    # 防重复：同一用户已有待处理的忘记密码审批则不再新建
    dup = conn.execute(
        "SELECT id FROM approval_requests WHERE block_id='PWD-FORGET' AND target_id=? AND status='pending'",
        (username,)).fetchone()
    if dup:
        conn.close()
        return jsonify({"ok": True, "message": "already_pending", "approvers": approvers})
    real_name = row["real_name"] or username
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    conn.execute(
        "INSERT INTO approval_requests (requester, requester_name, block_id, block_name, action_name, "
        "approvers, status, created_at, persist, target_id, title, content) "
        "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
        (username, real_name, "PWD-FORGET", "Password Reset", "忘记密码重置",
         json.dumps(approvers, ensure_ascii=False), "pending", now, "single-use", username,
         "忘记密码重置", f"{real_name}({username}) 申请重置登录密码"))
    conn.execute("INSERT INTO password_requests (username, status, requested_at, note) VALUES (?,?,?,?)",
                 (username, "pending", now, "sent_to_approvers"))
    conn.commit()
    conn.close()
    return jsonify({"ok": True, "message": "sent_to_approvers", "approvers": approvers})

# ===================== API：项目 CRUD =====================
# ★ 调试路由：查看 API 返回的签约项目数据结构（用于诊断图表问题）
@app.route("/api/won-projects/debug", methods=["GET"])
def debug_won_projects():
    """返回签约项目数据的诊断信息：字段列表、前几条数据样本"""
    conn = get_db()
    c = conn.cursor()
    try:
        # 获取表结构
        cols = c.execute("PRAGMA table_info(won_projects)").fetchall()
        col_names = [col[1] for col in cols]
        
        # 获取数据样本
        rows = c.execute("SELECT * FROM won_projects LIMIT 3").fetchall()
        sample_data = [dict(zip(col_names, r)) for r in rows]
        
        # 签约方分布
        party_dist = {}
        for row in c.execute("SELECT signing_parties, COUNT(*) FROM won_projects GROUP BY signing_parties"):
            party_dist[row[0] or '空'] = row[1]
        
        return jsonify({
            "columns": col_names,
            "sample": sample_data,
            "signing_parties_distribution": party_dist
        })
    finally:
        conn.close()

# ★ 调试路由：强制重新生成签约项目种子数据（用于修复看板图表空白问题）
# 访问方式：GET /api/won-projects/reseed
@app.route("/api/won-projects/reseed", methods=["GET"])
def reseed_won_projects():
    """强制清除并重新插入签约项目示例数据（看板图表演示用）"""
    import os
    # 只允许本地访问
    if request.remote_addr not in ('127.0.0.1', 'localhost', '::1') and os.environ.get('FLASK_ENV') != 'development':
        return jsonify({"error": "仅允许本地访问"}), 403
    
    conn = get_db()
    c = conn.cursor()
    try:
        # 清空现有数据（谨慎操作，仅清空签约项目表）
        c.execute("DELETE FROM won_projects")
        conn.commit()
        
        # 重新插入种子数据
        seed_won_projects(c)
        conn.commit()
        
        # 验证插入结果
        count = c.execute("SELECT COUNT(*) FROM won_projects").fetchone()[0]
        bu_count = c.execute("SELECT COUNT(*) FROM won_projects WHERE signing_parties IN ('AGI-Customer', 'GS-Customer')").fetchone()[0]
        
        return jsonify({
            "ok": True,
            "message": f"已重新生成签约项目种子数据（共 {count} 条，含 AGI/GS 签约方数据 {bu_count} 条）",
            "total": count,
            "bu_projects": bu_count
        })
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

def _norm_decision(decision):
    """把任意语言的权限决策规范化为统一 key。"""
    if not decision:
        return ""
    d = str(decision).strip()
    if d in ("特别授权看全公司", "Grant Company-wide", "Cấp toàn công ty", "all", "company"):
        return "all"
    if d in ("隐藏该项", "Hide", "Ẩn mục này", "hide"):
        return "hide"
    if d in ("发起审批", "Submit approval", "Gửi phê duyệt", "Khởi tạo phê duyệt", "approve"):
        return "approve"
    return "default"


def _user_has_full_company(conn, username, block_id):
    """判断 username 是否对 block_id 拥有“特别授权看全公司”（decision=='all'）。"""
    if not username or not block_id:
        return False
    row = conn.execute("SELECT perms FROM users WHERE username=?", (username,)).fetchone()
    if not row:
        return False
    try:
        perms = json.loads(row["perms"]) if row["perms"] else {}
    except Exception:
        return False
    if not isinstance(perms, dict):
        return False
    blk = perms.get(block_id)
    if not isinstance(blk, dict):
        return False
    return _norm_decision(blk.get("decision")) == "all"


def _visible_scope(username, block_id=None):
    """返回 (where_clause, params) 用于限制某用户可见的项目记录（独立记录）。

    - 未登录 / 管理员 / 总经理 / 副总经理：返回 ('', []) 表示看全部（向后兼容）。
    - 普通用户：若对 block_id 拥有“特别授权看全公司”(decision='all')，也看全部。
    - 其他：仅看 owner_user_id 属于“自己 + vis_he_can_see 指定人员”的记录；
      兼容旧数据（owner_user_id 为空）：退而按 salesperson 文本匹配同一组人。
    """
    if not username:
        return ("", [])
    conn = get_db()
    user = conn.execute("SELECT role, vis_he_can_see FROM users WHERE username=?", (username,)).fetchone()
    if not user:
        conn.close()
        return ("", [])
    # 看全部：自由任命的管理员
    if _is_manager(conn, username):
        conn.close()
        return ("", [])
    # 看全部：对该区块拥有“特别授权看全公司”
    if block_id and _user_has_full_company(conn, username, block_id):
        conn.close()
        return ("", [])
    visible = [username.lower()]
    try:
        vs = json.loads(user["vis_he_can_see"]) if user["vis_he_can_see"] else []
    except Exception:
        vs = []
    # vis_he_can_see 兼容两种存储格式：
    #   1) 数字/数字串 → 用户 ID（管理界面保存），需先解析为用户名
    #   2) 用户名字符串 → 旧种子数据，直接使用
    id_list = []
    name_list = []
    for v in vs:
        s = str(v).strip()
        if not s:
            continue
        if s.isdigit():
            id_list.append(int(s))
        else:
            name_list.append(s.lower())
    if id_list:
        try:
            ph = ",".join("?" * len(id_list))
            for r in conn.execute(f"SELECT username FROM users WHERE id IN ({ph})", id_list).fetchall():
                name_list.append(str(r["username"]).strip().lower())
        except Exception:
            pass
    for n in name_list:
        if n and n not in visible:
            visible.append(n)
    # 反向授权：其他用户的 vis_can_see_me 中包含当前用户（按 ID 或用户名）→ 其数据对当前用户可见
    try:
        me = conn.execute("SELECT id FROM users WHERE username=?", (username,)).fetchone()
        my_id = me["id"] if me else None
        for r in conn.execute(
            "SELECT username, vis_can_see_me FROM users WHERE username<>? AND vis_can_see_me IS NOT NULL AND vis_can_see_me<>'' AND vis_can_see_me<>'[]'",
            (username,)
        ).fetchall():
            try:
                arr = json.loads(r["vis_can_see_me"]) if r["vis_can_see_me"] else []
            except Exception:
                arr = []
            hit = False
            for v in arr:
                s = str(v).strip()
                if not s:
                    continue
                if s.isdigit():
                    if my_id is not None and int(s) == my_id:
                        hit = True
                        break
                elif s.lower() == username.lower():
                    hit = True
                    break
            if hit:
                u2 = str(r["username"]).strip().lower()
                if u2 and u2 not in visible:
                    visible.append(u2)
    except Exception:
        pass
    # 离职代理：当前用户是被代理人的 delegate_to 时，自动可见离职/停用人员名下的数据
    try:
        delegated = conn.execute(
            "SELECT username FROM users WHERE delegate_to=? AND status<>'active' AND username<>?",
            (username, username)
        ).fetchall()
        for d in delegated:
            visible.append(str(d["username"]).strip().lower())
    except Exception:
        pass
    conn.close()
    ph = ",".join("?" * len(visible))
    # owner_user_id（录入人）或 salesperson（实际销售）任一命中可见集合即可见，
    # 这样正向/反向授权看某人数据时，其作为销售员的记录也能被正确纳入。
    # 两个分支都必须 lower：owner_user_id / salesperson 实际存的是用户名字符串，
    # 存量数据大小写混杂（如 'Khoa'），不 lower 会导致“自己的行不可见”
    clause = f"lower(owner_user_id) IN ({ph}) OR lower(salesperson) IN ({ph})"
    return (clause, visible + visible)


def _owns_row(table, pid, username):
    """后端写操作真实拦截：写权限仅限行归属者本人（防止通过数据范围授权越权修改他人数据）。

    - 数据范围授权（vis_he_can_see / vis_can_see_me）只授予“查看”权，不授予“写”权；
      被授权人只能读，不能修改/删除他人数据，他人数据也不会被其修改。
    - 管理员（总经理/副总经理/自由任命管理员）豁免，可写全部。
    - 未带 X-User-Name（如自动化/老调用）视为有权，向后兼容。
    返回 True 表示允许写。
    """
    if not username:
        return True
    conn = get_db()
    try:
        if _is_manager(conn, username):
            return True
        row = conn.execute(f"SELECT owner_user_id, salesperson FROM {table} WHERE id=?", (pid,)).fetchone()
        if not row:
            return False
        me = username.strip().lower()
        owner = (row["owner_user_id"] or "").strip().lower()
        if owner:
            return owner == me
        # 兼容旧数据：owner 为空时按 salesperson 文本匹配本人
        sp = (row["salesperson"] or "").strip().lower()
        return sp == me
    finally:
        conn.close()


def _perm_gate(conn, username, bid, target_id=None):
    """服务端权限闸门（无条件强制）：所有写操作按该用户权限决策在服务端校验。

    规则（对任意用户无条件生效，与浏览器状态/前端代码无关）：
    - hide（隐藏该项）          → 403 拒绝
    - approve（发起审批）       → 必须存在"该用户对该 bid+target 的已通过单次审批"（未消耗）；
                                  放行同时标记 consumed=1（一次审批只能执行一次操作）
    - default/company（保留默认/特别授权）→ 放行
    - 管理员豁免；未带 X-User-Name 放行（向后兼容自动化/脚本）
    返回 None=放行；返回 (jsonify元组)=拒绝响应。
    """
    if not username:
        return None
    try:
        if _is_manager(conn, username):
            return None
    except Exception:
        pass
    try:
        row = conn.execute("SELECT perms FROM users WHERE username=?", (username,)).fetchone()
    except Exception:
        return None
    if not row or not row["perms"]:
        return None
    try:
        p = json.loads(row["perms"])
        dec = ((p.get(bid) or {}).get("decision") or "").strip().lower()
    except Exception:
        return None
    if not dec or dec in ("default", "company"):
        return None
    if dec == "hide":
        return (jsonify({"error": "forbidden_hidden", "message": "无权限：该模块已被隐藏"}), 403)
    if dec == "approve":
        tid = str(target_id if target_id is not None else "")
        g = conn.execute(
            "SELECT id FROM approval_requests WHERE requester=? AND block_id=? AND target_id=? "
            "AND status='approved' AND persist='single-use' AND COALESCE(consumed,0)=0 "
            "ORDER BY id DESC LIMIT 1",
            (username, bid, tid)).fetchone()
        if not g:
            return (jsonify({"error": "approval_required",
                             "message": "该操作需审批人通过后才能执行"}), 403)
        conn.execute("UPDATE approval_requests SET consumed=1 WHERE id=?", (g["id"],))
        return None
    return None


# ===================== WON-P345：签约项目 P3/P4/P5 列权限 =====================
# 隐藏时服务端直接剥离这些字段（列表+详情），任何客户端手段都拿不到
WON_P345_KEYS = (
    "gs_comm_pct", "gs_comm_rmb", "gs_comm_usd", "gs_comm_vnd",
    "gs_pay_count", "gs_paid_rmb", "gs_paid_usd", "gs_paid_vnd",
    "gs_unpaid_rmb", "gs_unpaid_usd", "gs_unpaid_vnd", "gs_remark",
    "agi_payable_rmb", "agi_payable_usd", "agi_payable_vnd",
    "agi_pay_count", "agi_paid_rmb", "agi_paid_usd", "agi_paid_vnd",
    "agi_unpaid_rmb", "agi_unpaid_usd", "agi_unpaid_vnd", "agi_remark",
    "doc_equip", "doc_install", "doc_both", "doc_addendum_cnt", "doc_remark",
    # ★ 三语备注列同步纳入 P345 剥离
    "gs_remark_zh", "gs_remark_en", "gs_remark_vi",
    "agi_remark_zh", "agi_remark_en", "agi_remark_vi",
)

def _won_p345_hidden(conn, username):
    """P3/P4/P5 列隐藏判定：显式决策优先；未配置时销售/销售总监职位默认隐藏。"""
    if not username:
        return False
    try:
        row = conn.execute("SELECT perms, position FROM users WHERE username=?", (username,)).fetchone()
        if not row:
            return False
        try:
            p = json.loads(row["perms"] or "{}")
            dec = ((p.get("WON-P345") or {}).get("decision") or "").strip().lower()
        except Exception:
            dec = ""
        if dec:
            return dec == "hide"
        pos = (row["position"] or "").strip()
        return pos in ("销售", "销售总监", "观察者")   # 观察者职位缺省隐藏（预设值，配置后按配置）
    except Exception:
        return False

def _strip_won_p345(rows):
    for d in rows:
        for k in WON_P345_KEYS:
            d.pop(k, None)
    return rows


# ★ 三语备注 / 付款方式 JSON 展开：本机后端复刻云端 wonlost.js 行为，
# 让桌面版也能像网页版一样正确显示中文/英文/越南文。
_WON_RM_BASES = ["cust_remark", "gs_remark", "agi_remark"]

def _expand_won_remarks(row):
    if not row:
        return row
    for b in _WON_RM_BASES:
        obj = None
        try:
            obj = json.loads(row[b]) if row.get(b) else None
        except Exception:
            obj = None
        if obj and isinstance(obj, dict):
            row[b + "_zh"] = obj.get("zh") or ""
            row[b + "_en"] = obj.get("en") or ""
            row[b + "_vi"] = obj.get("vi") or ""
        else:
            old = str(row[b]) if row.get(b) is not None else ""
            row[b + "_zh"] = old
            row[b + "_en"] = ""
            row[b + "_vi"] = ""
    return row

def _expand_payment_terms(row):
    if not row:
        return row
    raw = str(row.get("payment_terms") or "")
    obj = None
    if raw.strip().startswith("{"):
        try:
            obj = json.loads(raw)
        except Exception:
            obj = None
    if obj and isinstance(obj, dict):
        row["payment_terms_zh"] = obj.get("zh") or ""
        row["payment_terms_en"] = obj.get("en") or ""
        row["payment_terms_vi"] = obj.get("vi") or ""
    else:
        row["payment_terms_zh"] = raw
        row["payment_terms_en"] = raw
        row["payment_terms_vi"] = raw
    return row


def _expand_won_row(row):
    _expand_won_remarks(row)
    _expand_payment_terms(row)
    return row


@app.route("/api/won-projects", methods=["GET"])
def list_projects():
    conn = get_db()
    uname = request.headers.get("X-User-Name")
    clause, params = _visible_scope(uname, "WON-L1")
    sql = "SELECT * FROM won_projects WHERE lower(salesperson) <> 'agi-gs internal'"
    if clause:
        sql += " AND (" + clause + ")"
    sql += " ORDER BY id DESC"
    rows = conn.execute(sql, params).fetchall()
    out = [row_to_dict(r) for r in rows]
    for d in out:
        _expand_won_row(d)
    # WON-P345 权限闸门（服务端硬剥离）：隐藏决策/销售缺省 → 剥掉 P3/P4/P5 全部字段，
    # 浏览器、接口直调、任何客户端手段都拿不到这些数据
    if _won_p345_hidden(conn, uname):
        _strip_won_p345(out)
    conn.close()
    return jsonify(out)

@app.route("/api/won-projects", methods=["POST"])
def create_project():
    data = request.get_json(force=True, silent=True) or {}
    fields = [
        "contract_no","customer","province","contract_date","signing_parties","contract_currency",
        "rate_rmb_vnd","rate_usd_vnd","incoterm","include_install","payment_terms","payment_terms_zh","payment_terms_en","payment_terms_vi","salesperson",
        "equip_rmb","equip_usd","equip_vnd","superv_rmb","superv_usd","superv_vnd",
        "fb_budget_rmb","fb_budget_usd","fb_budget_vnd","fb_actual_rmb","fb_actual_usd","fb_actual_vnd",
        "cc_budget_rmb","cc_budget_usd","cc_budget_vnd","cc_actual_rmb","cc_actual_usd","cc_actual_vnd",
        "total_equip_rmb","total_equip_usd","total_equip_vnd",
        "inst_budget_rmb","inst_budget_usd","inst_budget_vnd","inst_actual_rmb","inst_actual_usd","inst_actual_vnd",
        "total_ei_rmb","total_ei_usd","total_ei_vnd",
        # ★ 新增：增值税&关税&其他费用调节平衡输入
        "vat_rmb","vat_usd","vat_vnd",
        # ★ 新增：质保金信息
        "warranty_rmb","warranty_usd","warranty_vnd","warranty_start","warranty_end",
        "cust_pay_count","cust_paid_rmb","cust_paid_usd","cust_paid_vnd",
        "cust_unpaid_rmb","cust_unpaid_usd","cust_unpaid_vnd","cust_remark",
        "gs_comm_pct","gs_comm_rmb","gs_comm_usd","gs_comm_vnd",
        "gs_pay_count","gs_paid_rmb","gs_paid_usd","gs_paid_vnd",
        "gs_unpaid_rmb","gs_unpaid_usd","gs_unpaid_vnd","gs_remark",
        "agi_payable_rmb","agi_payable_usd","agi_payable_vnd",
        "agi_pay_count","agi_paid_rmb","agi_paid_usd","agi_paid_vnd",
        "agi_unpaid_rmb","agi_unpaid_usd","agi_unpaid_vnd","agi_remark",
        "doc_equip","doc_install","doc_both","doc_addendum_cnt","doc_remark","concrete_floor_spec",
        # ★ 三语备注列
        "cust_remark_zh","cust_remark_en","cust_remark_vi",
        "gs_remark_zh","gs_remark_en","gs_remark_vi",
        "agi_remark_zh","agi_remark_en","agi_remark_vi"
    ]
    cols = []
    vals = []
    for f in fields:
        if f in data:
            cols.append(f)
            v = data[f]
            if f.startswith(("equip_","superv_","fb_","cc_","inst_","total_","cust_","gs_","agi_","vat_","doc_")) and f not in ("cust_remark","gs_remark","gs_comm_pct","agi_remark","doc_remark","doc_equip","doc_install","doc_both","concrete_floor_spec","cust_remark_zh","cust_remark_en","cust_remark_vi","gs_remark_zh","gs_remark_en","gs_remark_vi","agi_remark_zh","agi_remark_en","agi_remark_vi"):
                try:
                    v = int(v or 0)
                except:
                    v = 0
            vals.append(v)
    cols += ["attachments","supp_summary","cust_view_detail","gs_view_detail"]
    vals += [
        json.dumps(data.get("attachments") or [], ensure_ascii=False),
        json.dumps(data.get("supp_summary") or [], ensure_ascii=False),
        json.dumps(data.get("cust_view_detail") or [], ensure_ascii=False),
        json.dumps(data.get("gs_view_detail") or [], ensure_ascii=False)
    ]
    # 独立记录：记录归属人 = 当前登录用户（前端通过 X-User-Name 头传递）
    cols.append("owner_user_id")
    vals.append((request.headers.get("X-User-Name") or "").strip().lower())
    # AGI 明细 & 补充协议：字符串原样存储（与前端文本框值一致）
    for k in ("agi_view_detail", "doc_view_addendum"):
        if data.get(k) is not None:
            cols.append(k)
            vals.append(data.get(k))
    sql = f"INSERT INTO won_projects ({','.join(cols)}) VALUES ({','.join(['?']*len(vals))})"
    conn = get_db()
    cur = conn.execute(sql, vals)
    new_id = cur.lastrowid
    conn.execute("UPDATE won_projects SET updated_at=datetime('now','localtime') WHERE id=?", (new_id,))
    row = conn.execute("SELECT * FROM won_projects WHERE id=?", (new_id,)).fetchone()
    conn.commit()
    conn.close()
    return jsonify(row_to_dict(row)), 201

@app.route("/api/won-projects/<int:pid>", methods=["GET"])
def get_project(pid):
    conn = get_db()
    uname = request.headers.get("X-User-Name")
    row = conn.execute("SELECT * FROM won_projects WHERE id=?", (pid,)).fetchone()
    if not row:
        conn.close()
        return jsonify({"error":"not found"}), 404
    d = row_to_dict(row)
    _expand_won_row(d)
    if _won_p345_hidden(conn, uname):
        _strip_won_p345([d])
    conn.close()
    return jsonify(d)

@app.route("/api/won-projects/<int:pid>", methods=["PUT"])
def update_project(pid):
    data = request.get_json(force=True, silent=True) or {}
    conn = get_db()
    row = conn.execute("SELECT id FROM won_projects WHERE id=?", (pid,)).fetchone()
    if not row:
        conn.close()
        return jsonify({"error":"not found"}),404
    # 后端真实拦截：仅记录所有者/被授权可见者可读写
    if not _owns_row("won_projects", pid, request.headers.get("X-User-Name")):
        conn.close()
        return jsonify({"error":"forbidden"}), 403
    fields = [
        "contract_no","customer","province","contract_date","signing_parties","contract_currency",
        "rate_rmb_vnd","rate_usd_vnd","incoterm","include_install","payment_terms","payment_terms_zh","payment_terms_en","payment_terms_vi","salesperson",
        "equip_rmb","equip_usd","equip_vnd","superv_rmb","superv_usd","superv_vnd",
        "fb_budget_rmb","fb_budget_usd","fb_budget_vnd","fb_actual_rmb","fb_actual_usd","fb_actual_vnd",
        "cc_budget_rmb","cc_budget_usd","cc_budget_vnd","cc_actual_rmb","cc_actual_usd","cc_actual_vnd",
        "total_equip_rmb","total_equip_usd","total_equip_vnd",
        "inst_budget_rmb","inst_budget_usd","inst_budget_vnd","inst_actual_rmb","inst_actual_usd","inst_actual_vnd",
        "total_ei_rmb","total_ei_usd","total_ei_vnd",
        # ★ 新增：增值税&关税&其他费用调节平衡输入
        "vat_rmb","vat_usd","vat_vnd",
        # ★ 新增：质保金信息
        "warranty_rmb","warranty_usd","warranty_vnd","warranty_start","warranty_end",
        "cust_pay_count","cust_paid_rmb","cust_paid_usd","cust_paid_vnd",
        "cust_unpaid_rmb","cust_unpaid_usd","cust_unpaid_vnd","cust_remark",
        "gs_comm_pct","gs_comm_rmb","gs_comm_usd","gs_comm_vnd",
        "gs_pay_count","gs_paid_rmb","gs_paid_usd","gs_paid_vnd",
        "gs_unpaid_rmb","gs_unpaid_usd","gs_unpaid_vnd","gs_remark",
        "agi_payable_rmb","agi_payable_usd","agi_payable_vnd",
        "agi_pay_count","agi_paid_rmb","agi_paid_usd","agi_paid_vnd",
        "agi_unpaid_rmb","agi_unpaid_usd","agi_unpaid_vnd","agi_remark",
        "doc_equip","doc_install","doc_both","doc_addendum_cnt","doc_remark","concrete_floor_spec",
        # ★ 三语备注列
        "cust_remark_zh","cust_remark_en","cust_remark_vi",
        "gs_remark_zh","gs_remark_en","gs_remark_vi",
        "agi_remark_zh","agi_remark_en","agi_remark_vi"
    ]
    sets = []
    vals = []
    for f in fields:
        if f in data:
            sets.append(f"{f}=?")
            v = data[f]
            if f.startswith(("equip_","superv_","fb_","cc_","inst_","total_","cust_","gs_","agi_","vat_","doc_")) and f not in ("cust_remark","gs_remark","gs_comm_pct","agi_remark","doc_remark","doc_equip","doc_install","doc_both","concrete_floor_spec","cust_remark_zh","cust_remark_en","cust_remark_vi","gs_remark_zh","gs_remark_en","gs_remark_vi","agi_remark_zh","agi_remark_en","agi_remark_vi"):
                try:
                    v = int(v or 0)
                except:
                    v = 0
            vals.append(v)
    for k in ("attachments","supp_summary","cust_view_detail","gs_view_detail","agi_view_detail","doc_view_addendum"):
        if k in data:
            sets.append(f"{k}=?")
            vals.append(json.dumps(data[k], ensure_ascii=False) if isinstance(data[k], (list,dict)) else (data[k] or ""))
    if sets:
        sets.append("updated_at=datetime('now','localtime')")
        vals.append(pid)
        conn.execute(f"UPDATE won_projects SET {', '.join(sets)} WHERE id=?", vals)
    row = conn.execute("SELECT * FROM won_projects WHERE id=?", (pid,)).fetchone()
    conn.commit()
    conn.close()
    return jsonify(row_to_dict(row))

def _rm_upload_file(name):
    """安全删除 uploads/ 目录下的一个文件（删记录时捆绑清理，维护磁盘空间）。

    兼容三种取值：纯文件名 / 含 uploads/ 的 URL / 空值。
    只按 basename 处理且仅作用于 UPLOAD_DIR 内，绝不误删目录外的文件；文件不存在时静默跳过。
    """
    if not name:
        return
    s = str(name).strip()
    if "uploads/" in s:
        s = s.split("uploads/")[-1]
    s = os.path.basename(s.strip())
    if not s:
        return
    try:
        os.remove(os.path.join(UPLOAD_DIR, s))
    except OSError:
        pass


def _rm_upload_files(*names):
    """批量安全删除 uploads/ 文件（值可为空/URL/文件名，逐个容错）。"""
    for n in names:
        _rm_upload_file(n)


# ===================== 彻底删除（Purge）工具 =====================
# 与云端 cloudflare/src/purge.js 对称：
# 本地数据库同样没有外键、没开 PRAGMA foreign_keys，删记录时
# 必须手写级联，否则审批单 / 佣金记录 / 磁盘文件都会残留。
#
# 设计原则：
#   1) 引用计数安全删除：同一个文件若仍被其它记录引用则不删
#      （"CRM 转失败"后 CRM 与 LOST 共享同一批 pdf 值，删一边不能弄坏另一边）
#   2) 全级联：磁盘文件 + 审批单 + 佣金记录，一次删干净
# =====================

def _norm_file_ref(v):
    """把 文件名 / uploads/xxx URL / 空值 统一成纯文件名，无法解析返回 ''。"""
    s = str(v or "").strip()
    if not s:
        return ""
    if "uploads/" in s:
        s = s.split("uploads/")[-1]
    return os.path.basename(s.strip())


def _row_file_refs(table, row):
    """从一条记录里取出它引用的所有文件名。"""
    out = []
    if not row:
        return out
    try:
        if table == "won_projects":
            atts = json.loads(row["attachments"]) if row["attachments"] else []
            for a in atts or []:
                n = _norm_file_ref((a or {}).get("filename") or (a or {}).get("url"))
                if n:
                    out.append(n)
            # ★ V45/V52：WON 合同/安装合同 PDF 也存成 uploads/ 下的纯文件名，
            # 必须纳入引用集，否则 purge-orphans 会误删真实合同附件。
            for f in ("doc_equip", "doc_install", "doc_both"):
                n = _norm_file_ref(row[f])
                if n:
                    out.append(n)
            return out
        for f in ("pdf_equip", "pdf_install", "pdf_both"):
            n = _norm_file_ref(row[f])
            if n:
                out.append(n)
    except Exception:
        pass
    return out


def _collect_referenced_files(conn):
    """收集整个数据库里被引用的所有文件名（用于孤儿扫描 + 安全删除）。"""
    refs = set()
    for t in ("crm_projects", "lost_projects", "won_projects"):
        try:
            if t == "won_projects":
                rows = conn.execute(
                    "SELECT attachments, doc_equip, doc_install, doc_both FROM won_projects"
                ).fetchall()
                for r in rows:
                    refs.update(_row_file_refs("won_projects", r))
            else:
                rows = conn.execute(
                    "SELECT pdf_equip, pdf_install, pdf_both FROM %s" % t
                ).fetchall()
                for r in rows:
                    refs.update(_row_file_refs(t, r))
        except Exception:
            continue
    return refs


def _rm_files_if_orphan(conn, names, exclude_table=None, exclude_id=None):
    """引用计数安全删除：只删没有任何其它记录引用的文件。

    返回 (deleted, kept) 数量。
    """
    refs = _collect_referenced_files(conn)
    # 排除"正在被删除的这条记录"自身的引用
    if exclude_table and exclude_id is not None:
        try:
            row = conn.execute(
                "SELECT * FROM %s WHERE id=?" % exclude_table, (exclude_id,)
            ).fetchone()
            for k in _row_file_refs(exclude_table, row):
                refs.discard(k)
        except Exception:
            pass
    deleted = kept = 0
    for n in names or []:
        fn = _norm_file_ref(n)
        if not fn:
            continue
        if fn in refs:
            kept += 1
            continue
        try:
            os.remove(os.path.join(UPLOAD_DIR, fn))
            deleted += 1
        except OSError:
            pass
    return deleted, kept


def _purge_approvals(conn, block_prefix, pid):
    """删除指向该记录的审批单（target_id 存记录 id，block_id 形如 CRM-D3）。"""
    try:
        cur = conn.execute(
            "DELETE FROM approval_requests WHERE block_id LIKE ? AND target_id=?",
            (block_prefix + "%", str(pid)),
        )
        return cur.rowcount or 0
    except Exception:
        return 0


def _purge_commission(conn, contract_no):
    """按合同号删除佣金记录（主表 + 受益人表）。"""
    if not contract_no:
        return 0, 0
    try:
        ids = [
            r["id"]
            for r in conn.execute(
                "SELECT id FROM commission_records WHERE contract=?", (contract_no,)
            ).fetchall()
        ]
        if not ids:
            return 0, 0
        ph = ",".join("?" * len(ids))
        b = conn.execute(
            "DELETE FROM commission_beneficiaries WHERE record_id IN (%s)" % ph, ids
        ).rowcount or 0
        r = conn.execute(
            "DELETE FROM commission_records WHERE id IN (%s)" % ph, ids
        ).rowcount or 0
        return r, b
    except Exception:
        return 0, 0


def _cleanup_replaced_pdf(old_val, new_name):
    """替换上传后删除旧文件：old_val 为该槽位原文件名/URL，与新文件同名则跳过。"""
    if not old_val:
        return
    old = str(old_val).strip()
    if "uploads/" in old:
        old = old.split("uploads/")[-1].strip()
    old = os.path.basename(old)
    if old and old != new_name:
        _rm_upload_file(old)


@app.route("/api/won-projects/<int:pid>", methods=["DELETE"])
def delete_project(pid):
    conn = get_db()
    row = conn.execute("SELECT attachments FROM won_projects WHERE id=?", (pid,)).fetchone()
    if not row:
        conn.close()
        return jsonify({"error":"not found"}),404
    # 后端真实拦截
    if not _owns_row("won_projects", pid, request.headers.get("X-User-Name")):
        conn.close()
        return jsonify({"error":"forbidden"}), 403
    # 彻底删除：磁盘附件 + 审批单(WON-*) + 佣金记录(按合同号) → 主记录
    full = conn.execute(
        "SELECT attachments, contract_no FROM won_projects WHERE id=?", (pid,)
    ).fetchone()
    try:
        atts = json.loads(full["attachments"]) if full and full["attachments"] else []
    except Exception:
        atts = []
    contract_no = (full["contract_no"] if full else "") or ""
    deleted, kept = _rm_files_if_orphan(
        conn, [a.get("filename") for a in atts],
        exclude_table="won_projects", exclude_id=pid,
    )
    approvals = _purge_approvals(conn, "WON-", pid)
    comm_rec, comm_ben = _purge_commission(conn, contract_no)
    conn.execute("DELETE FROM won_projects WHERE id=?", (pid,))
    conn.commit()
    conn.close()
    return jsonify({"ok": True, "purge": {
        "files_deleted": deleted, "files_kept": kept,
        "approvals_deleted": approvals,
        "commission_records": comm_rec, "commission_beneficiaries": comm_ben,
    }})

# ===================== API：CRM（报价/跟进） CRUD =====================
CRM_FIELDS = [
    "quote_no","project_name","province","customer","bu","construction",
    "startup_pct","sign_pct","manager","manager_phone","company_info",
    "initial_quote_date","est_purchase_date","est_ship_date","quote_version",
    "last_quote_date","rate_rmb_vnd","rate_usd_vnd","incoterm",
    "install_quoted","salesperson","remark","pdf_equip","pdf_install","pdf_both",
    "remark_zh","remark_en","remark_vi",
    "q1_rmb","q1_usd","q1_vnd",
    "q2_rmb","q2_usd","q2_vnd",
    "q3_rmb","q3_usd","q3_vnd",
    "q4_rmb","q4_usd","q4_vnd",
    "q5_rmb","q5_usd","q5_vnd",
    "q6_rmb","q6_usd","q6_vnd",
    "q7_rmb","q7_usd","q7_vnd",
]
CRM_NUM_FIELDS = set([
    "q1_rmb","q1_usd","q1_vnd","q2_rmb","q2_usd","q2_vnd",
    "q3_rmb","q3_usd","q3_vnd","q4_rmb","q4_usd","q4_vnd",
    "q5_rmb","q5_usd","q5_vnd","q6_rmb","q6_usd","q6_vnd",
    "q7_rmb","q7_usd","q7_vnd",
])

@app.route("/api/crm-projects", methods=["GET"])
def list_crm_projects():
    conn = get_db()
    # 只返回潜在项目（active），已转到“失败项目”的不再展示
    base = "status='active' OR status IS NULL OR status=''"
    scope = (request.args.get("scope") or "").strip()
    username = request.headers.get("X-User-Name")
    # scope=all 表示前端显式请求“全公司”数据（看板图表/概况弹窗使用）；
    # 否则按用户可见范围，若该用户拥有 CRM-L1 “特别授权看全公司”也看全部
    if scope == "all":
        clause, params = ("", [])
    else:
        clause, params = _visible_scope(username, "CRM-L1")
    sql = ("SELECT * FROM crm_projects WHERE (%s) AND lower(salesperson) <> 'agi-gs internal'" % base)
    if clause:
        sql += " AND (%s)" % clause
    sql += " ORDER BY id ASC"
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return jsonify([row_to_dict(r) for r in rows])

@app.route("/api/crm-projects", methods=["POST"])
def create_crm_project():
    data = request.get_json(force=True, silent=True) or {}
    cols = []
    vals = []
    for f in CRM_FIELDS:
        if f in data:
            cols.append(f)
            v = data[f]
            if f in CRM_NUM_FIELDS:
                try:
                    v = int(v or 0)
                except:
                    v = 0
            vals.append(v)
    # 独立记录：记录归属人 = 当前登录用户（前端通过 X-User-Name 头传递）
    cols.append("owner_user_id")
    vals.append((request.headers.get("X-User-Name") or "").strip().lower())
    sql = f"INSERT INTO crm_projects ({','.join(cols)}) VALUES ({','.join(['?']*len(vals))})"
    conn = get_db()
    cur = conn.execute(sql, vals)
    new_id = cur.lastrowid
    conn.execute("UPDATE crm_projects SET updated_at=datetime('now','localtime') WHERE id=?", (new_id,))
    row = conn.execute("SELECT * FROM crm_projects WHERE id=?", (new_id,)).fetchone()
    conn.commit()
    conn.close()
    return jsonify(row_to_dict(row)), 201

@app.route("/api/crm-projects/<int:pid>", methods=["GET"])
def get_crm_project(pid):
    conn = get_db()
    row = conn.execute("SELECT * FROM crm_projects WHERE id=?", (pid,)).fetchone()
    conn.close()
    if not row:
        return jsonify({"error":"not found"}), 404
    return jsonify(row_to_dict(row))

@app.route("/api/crm-projects/<int:pid>", methods=["PUT"])
def update_crm_project(pid):
    data = request.get_json(force=True, silent=True) or {}
    conn = get_db()
    row = conn.execute("SELECT id FROM crm_projects WHERE id=?", (pid,)).fetchone()
    if not row:
        conn.close()
        return jsonify({"error":"not found"}),404
    if not _owns_row("crm_projects", pid, request.headers.get("X-User-Name")):
        conn.close()
        return jsonify({"error":"forbidden"}), 403
    gerr = _perm_gate(conn, request.headers.get("X-User-Name"), "CRM-D2", str(pid))
    if gerr:
        conn.commit(); conn.close()
        return gerr
    sets = []
    vals = []
    for f in CRM_FIELDS:
        if f in data:
            sets.append(f"{f}=?")
            v = data[f]
            if f in CRM_NUM_FIELDS:
                try:
                    v = int(v or 0)
                except:
                    v = 0
            vals.append(v)
    if sets:
        sets.append("updated_at=datetime('now','localtime')")
        vals.append(pid)
        conn.execute(f"UPDATE crm_projects SET {', '.join(sets)} WHERE id=?", vals)
    row = conn.execute("SELECT * FROM crm_projects WHERE id=?", (pid,)).fetchone()
    conn.commit()
    conn.close()
    return jsonify(row_to_dict(row))

@app.route("/api/crm-projects/<int:pid>", methods=["DELETE"])
def delete_crm_project(pid):
    conn = get_db()
    # 先取出文件引用（pdf_* 存的是 uploads/ 里的文件名），删记录时捆绑清理磁盘文件
    row = conn.execute("SELECT id, pdf_equip, pdf_install, pdf_both FROM crm_projects WHERE id=?", (pid,)).fetchone()
    if not row:
        conn.close()
        return jsonify({"error":"not found"}),404
    if not _owns_row("crm_projects", pid, request.headers.get("X-User-Name")):
        conn.close()
        return jsonify({"error":"forbidden"}), 403
    gerr = _perm_gate(conn, request.headers.get("X-User-Name"), "CRM-D3", str(pid))
    if gerr:
        conn.commit(); conn.close()
        return gerr
    # 彻底删除：磁盘附件 + 审批单(CRM-*) → 主记录
    # 引用计数安全删除：CRM 转失败后 CRM 与 LOST 共享同一批 pdf 值，
    # 只要 LOST 那边还在引用，文件就不能删，否则 LOST 的附件会变死链。
    deleted, kept = _rm_files_if_orphan(
        conn,
        [row["pdf_equip"], row["pdf_install"], row["pdf_both"]],
        exclude_table="crm_projects", exclude_id=pid,
    )
    approvals = _purge_approvals(conn, "CRM-", pid)
    conn.execute("DELETE FROM crm_projects WHERE id=?", (pid,))
    conn.commit()
    conn.close()
    return jsonify({"ok": True, "purge": {
        "files_deleted": deleted, "files_kept": kept, "approvals_deleted": approvals,
    }})

@app.route("/api/crm-projects/<int:pid>/failed", methods=["POST"])
def move_crm_project_to_failed(pid):
    """将潜在项目转到失败项目（状态置为 failed，同时在 lost_projects 创建记录）。"""
    conn = get_db()
    row = conn.execute("SELECT id FROM crm_projects WHERE id=?", (pid,)).fetchone()
    if not row:
        conn.close()
        return jsonify({"error":"not found"}),404
    if not _owns_row("crm_projects", pid, request.headers.get("X-User-Name")):
        conn.close()
        return jsonify({"error":"forbidden"}), 403
    gerr = _perm_gate(conn, request.headers.get("X-User-Name"), "CRM-F1", str(pid))
    if gerr:
        conn.commit(); conn.close()
        return gerr
    # 获取 CRM 完整记录，按列名映射（避免两张表列顺序不同导致错位）
    crm_row = conn.execute("SELECT * FROM crm_projects WHERE id=?", (pid,)).fetchone()
    crm_cols = [d[1] for d in conn.execute("PRAGMA table_info(crm_projects)").fetchall()]
    crm_dict = dict(zip(crm_cols, crm_row))
    # 获取 lost_projects 表的列顺序
    lost_cols = [d[1] for d in conn.execute("PRAGMA table_info(lost_projects)").fetchall()]
    fail_reason = request.json.get("fail_reason","") if request.is_json else ""
    insert_vals = []
    for col in lost_cols:
        if col in ("id", "created_at", "updated_at"):   # DB 自动生成
            insert_vals.append(None)
        elif col == "fail_reason":                      # 用户选择的失败原因
            insert_vals.append(fail_reason)
        elif col == "fail_date":                        # 当前日期
            insert_vals.append(datetime.now().strftime("%Y-%m-%d"))
        elif col == "status":                           # 状态置为 failed
            insert_vals.append("failed")
        else:                                           # 其余字段按列名一一对应
            insert_vals.append(crm_dict.get(col, None))
    conn.execute(f"INSERT INTO lost_projects ({','.join(lost_cols)}) VALUES ({','.join(['?']*len(lost_cols))})", insert_vals)
    conn.execute("UPDATE crm_projects SET status='failed', updated_at=datetime('now','localtime') WHERE id=?", (pid,))
    conn.commit()
    conn.close()
    return jsonify({"ok":True})

# ===================== API：失败项目（Lost） CRUD =====================
LOST_FIELDS = CRM_FIELDS + ["fail_reason", "fail_date"]
LOST_NUM_FIELDS = set(CRM_NUM_FIELDS)

@app.route("/api/lost-projects", methods=["GET"])
def list_lost_projects():
    conn = get_db()
    clause, params = _visible_scope(request.headers.get("X-User-Name"), "LOST-L1")
    sql = "SELECT * FROM lost_projects WHERE lower(salesperson) <> 'agi-gs internal'"
    if clause:
        sql += " AND (" + clause + ")"
    sql += " ORDER BY id ASC"
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return jsonify([row_to_dict(r) for r in rows])

@app.route("/api/lost-projects", methods=["POST"])
def create_lost_project():
    data = request.get_json(force=True, silent=True) or {}
    cols = []
    vals = []
    for f in LOST_FIELDS:
        if f in data:
            cols.append(f)
            v = data[f]
            if f in LOST_NUM_FIELDS:
                try:
                    v = int(v or 0)
                except:
                    v = 0
            vals.append(v)
    sql = f"INSERT INTO lost_projects ({','.join(cols)}) VALUES ({','.join(['?']*len(vals))})"
    conn = get_db()
    cur = conn.execute(sql, vals)
    new_id = cur.lastrowid
    conn.execute("UPDATE lost_projects SET updated_at=datetime('now','localtime') WHERE id=?", (new_id,))
    row = conn.execute("SELECT * FROM lost_projects WHERE id=?", (new_id,)).fetchone()
    conn.commit()
    conn.close()
    return jsonify(row_to_dict(row)), 201

@app.route("/api/lost-projects/<int:pid>", methods=["GET"])
def get_lost_project(pid):
    conn = get_db()
    row = conn.execute("SELECT * FROM lost_projects WHERE id=?", (pid,)).fetchone()
    conn.close()
    if not row:
        return jsonify({"error":"not found"}), 404
    return jsonify(row_to_dict(row))

@app.route("/api/lost-projects/<int:pid>", methods=["PUT"])
def update_lost_project(pid):
    data = request.get_json(force=True, silent=True) or {}
    conn = get_db()
    row = conn.execute("SELECT id FROM lost_projects WHERE id=?", (pid,)).fetchone()
    if not row:
        conn.close()
        return jsonify({"error":"not found"}),404
    if not _owns_row("lost_projects", pid, request.headers.get("X-User-Name")):
        conn.close()
        return jsonify({"error":"forbidden"}), 403
    gerr = _perm_gate(conn, request.headers.get("X-User-Name"), "LOST-D2", str(pid))
    if gerr:
        conn.commit(); conn.close()
        return gerr
    sets = []
    vals = []
    for f in LOST_FIELDS:
        if f in data:
            sets.append(f"{f}=?")
            v = data[f]
            if f in LOST_NUM_FIELDS:
                try:
                    v = int(v or 0)
                except:
                    v = 0
            vals.append(v)
    if sets:
        sets.append("updated_at=datetime('now','localtime')")
        vals.append(pid)
        conn.execute(f"UPDATE lost_projects SET {', '.join(sets)} WHERE id=?", vals)
    row = conn.execute("SELECT * FROM lost_projects WHERE id=?", (pid,)).fetchone()
    conn.commit()
    conn.close()
    return jsonify(row_to_dict(row))

@app.route("/api/lost-projects/<int:pid>", methods=["DELETE"])
def delete_lost_project(pid):
    conn = get_db()
    # 先取出文件引用（pdf_* 存的是 uploads/ 里的文件名），删记录时捆绑清理磁盘文件
    row = conn.execute("SELECT id, pdf_equip, pdf_install, pdf_both FROM lost_projects WHERE id=?", (pid,)).fetchone()
    if not row:
        conn.close()
        return jsonify({"error":"not found"}),404
    if not _owns_row("lost_projects", pid, request.headers.get("X-User-Name")):
        conn.close()
        return jsonify({"error":"forbidden"}), 403
    gerr = _perm_gate(conn, request.headers.get("X-User-Name"), "LOST-D3", str(pid))
    if gerr:
        conn.commit(); conn.close()
        return gerr
    # 彻底删除：磁盘附件 + 审批单(LOST-*) → 主记录（同样用引用计数安全删除）
    deleted, kept = _rm_files_if_orphan(
        conn,
        [row["pdf_equip"], row["pdf_install"], row["pdf_both"]],
        exclude_table="lost_projects", exclude_id=pid,
    )
    approvals = _purge_approvals(conn, "LOST-", pid)
    conn.execute("DELETE FROM lost_projects WHERE id=?", (pid,))
    conn.commit()
    conn.close()
    return jsonify({"ok": True, "purge": {
        "files_deleted": deleted, "files_kept": kept, "approvals_deleted": approvals,
    }})

@app.route("/api/lost-projects/<int:pid>/restore", methods=["POST"])
def restore_lost_project(pid):
    """将失败项目转回为潜在项目：从 lost_projects 移回 crm_projects(status='active')。"""
    conn = get_db()
    row = conn.execute("SELECT * FROM lost_projects WHERE id=?", (pid,)).fetchone()
    if not row:
        conn.close()
        return jsonify({"error":"not found"}),404
    if not _owns_row("lost_projects", pid, request.headers.get("X-User-Name")):
        conn.close()
        return jsonify({"error":"forbidden"}), 403
    gerr = _perm_gate(conn, request.headers.get("X-User-Name"), "LOST-R1", str(pid))
    if gerr:
        conn.commit(); conn.close()
        return gerr
    d = row_to_dict(row)
    cols = list(CRM_FIELDS)  # 业务字段，不含 status / fail_reason / fail_date
    # ★ 归属人随流转保留：LOST 行 owner 来自当初 CRM 转失败时保留的归属，
    #   转回潜在必须延续同一归属人，不得留空（否则退化为按 salesperson 匹配，
    #   三模块数据授权链在 LOST→CRM 处断裂）。
    _owner = (row["owner_user_id"] or "").strip().lower() if row["owner_user_id"] else ""
    if not _owner:
        _owner = (request.headers.get("X-User-Name") or "").strip().lower()
    cols.append("owner_user_id")
    vals = [d.get(c, "") if c not in CRM_NUM_FIELDS else int(d.get(c) or 0) for c in CRM_FIELDS]
    vals.append(_owner)
    placeholders = ",".join(["?"] * len(cols))
    conn.execute(
        f"INSERT INTO crm_projects ({','.join(cols)}, status) VALUES ({placeholders}, 'active')",
        vals,
    )
    conn.execute("DELETE FROM lost_projects WHERE id=?", (pid,))
    conn.commit()
    conn.close()
    return jsonify({"ok": True})

# 失败项目报价单 PDF 上传（与 CRM 报价单文档同机制）
@app.route("/api/lost-projects/<int:pid>/documents", methods=["POST"])
def upload_lost_pdf(pid):
    if "file" not in request.files:
        return jsonify({"error":"no file"}),400
    f = request.files["file"]
    if not f.filename:
        return jsonify({"error":"empty filename"}),400
    ext = os.path.splitext(f.filename)[1].lower()
    if ext != ".pdf":
        return jsonify({"error":"invalid pdf"}),415
    # 槽位（pdf_equip/pdf_install/pdf_both）：带槽位才能找到被替换的旧文件
    slot = (request.form.get("slot") or request.args.get("slot") or "").strip()
    if slot not in ("pdf_equip", "pdf_install", "pdf_both"):
        slot = ""
    conn = get_db()
    row = conn.execute("SELECT id, pdf_equip, pdf_install, pdf_both FROM lost_projects WHERE id=?", (pid,)).fetchone()
    conn.close()
    if not row:
        return jsonify({"error":"not found"}),404
    base = safe_name(f.filename)
    fname = f"{int(time.time()*1000)}_{base}"
    fpath = os.path.join(UPLOAD_DIR, fname)
    f.save(fpath)
    with open(fpath,"rb") as fh:
        data = fh.read(1024)
    i = 0
    while i < len(data) and (data[i] in (0x20, 0x09, 0x0A, 0x0D) or
                             (data[i:i+3] == b"\xef\xbb\xbf")):
        if data[i:i+3] == b"\xef\xbb\xbf":
            i += 3
        else:
            i += 1
    is_pdf = data[i:i+5] == b"%PDF-"
    if not is_pdf:
        try:
            os.remove(fpath)
        except Exception:
            pass
        return jsonify({"error":"invalid pdf"}),415
    # ★ 替换上传：新文件已验证合法，删除该槽位被替换的旧文件（维护磁盘空间）
    if slot:
        _cleanup_replaced_pdf(row[slot], fname)
    return jsonify({"ok":True, "filename": fname, "url": f"/uploads/{fname}"})

# ===================== API：附件 =====================
@app.route("/api/won-projects/<int:pid>/attachments", methods=["POST"])
def upload_attachment(pid):
    if "file" not in request.files:
        return jsonify({"error":"no file"}),400
    f = request.files["file"]
    if not f.filename:
        return jsonify({"error":"empty filename"}),400
    ext = os.path.splitext(f.filename)[1].lower()
    if ext not in ALLOWED_EXT:
        return jsonify({"error":"ext not allowed"}),400

    conn = get_db()
    row = conn.execute("SELECT id, attachments FROM won_projects WHERE id=?", (pid,)).fetchone()
    if not row:
        conn.close()
        return jsonify({"error":"not found"}),404

    base = safe_name(f.filename)
    fname = f"{int(time.time()*1000)}_{base}"
    fpath = os.path.join(UPLOAD_DIR, fname)
    f.save(fpath)

    if ext == ".pdf":
        with open(fpath,"rb") as fh:
            head = fh.read(5)
        if head != b"%PDF-":
            os.remove(fpath)
            conn.close()
            return jsonify({"error":"invalid pdf"}),400

    try:
        atts = json.loads(row["attachments"]) if row["attachments"] else []
    except:
        atts = []
    item = {
        "filename": fname,
        "original": f.filename,
        "ext": ext,
        "uploaded_at": time.strftime("%Y-%m-%d %H:%M"),
        "url": f"/uploads/{fname}"
    }
    atts.append(item)
    conn.execute("UPDATE won_projects SET attachments=?, updated_at=datetime('now','localtime') WHERE id=?",
                 (json.dumps(atts, ensure_ascii=False), pid))
    conn.commit()
    new_row = conn.execute("SELECT * FROM won_projects WHERE id=?", (pid,)).fetchone()
    conn.close()
    return jsonify(row_to_dict(new_row))


# ===================== 生产模块：收货单照片上传 =====================
# 与合同附件机制一致：文件存 uploads/，返回 文件名 + URL；不污染 won_projects.attachments 列。
@app.route("/api/won-projects/<int:pid>/prod-receipt-photos", methods=["POST"])
def upload_prod_receipt_photo(pid):
    if "file" not in request.files:
        return jsonify({"error": "no file"}), 400
    f = request.files["file"]
    if not f.filename:
        return jsonify({"error": "empty filename"}), 400
    ext = os.path.splitext(f.filename)[1].lower()
    if ext not in ALLOWED_EXT:
        return jsonify({"error": "ext not allowed"}), 400
    conn = get_db()
    row = conn.execute("SELECT id FROM won_projects WHERE id=?", (pid,)).fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "not found"}), 404
    stamp = time.strftime("%Y%m%d%H%M%S")
    rand = os.urandom(3).hex()
    fname = "prec_%d_%s_%s%s" % (pid, stamp, rand, ext)
    f.save(os.path.join(UPLOAD_DIR, fname))
    return jsonify({"ok": True, "filename": fname, "url": "/uploads/" + fname})


# 安装区域收货照片上传（与原料库存收货照片机制一致，保存为 inzone_ 前缀）
@app.route("/api/won-projects/<int:pid>/inst-zone-photos", methods=["POST"])
def upload_inst_zone_photo(pid):
    if "file" not in request.files:
        return jsonify({"error": "no file"}), 400
    f = request.files["file"]
    if not f.filename:
        return jsonify({"error": "empty filename"}), 400
    ext = os.path.splitext(f.filename)[1].lower()
    if ext not in ALLOWED_EXT:
        return jsonify({"error": "ext not allowed"}), 400
    conn = get_db()
    row = conn.execute("SELECT id FROM won_projects WHERE id=?", (pid,)).fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "not found"}), 404
    stamp = time.strftime("%Y%m%d%H%M%S")
    rand = os.urandom(3).hex()
    fname = "inzone_%d_%s_%s%s" % (pid, stamp, rand, ext)
    f.save(os.path.join(UPLOAD_DIR, fname))
    return jsonify({"ok": True, "filename": fname, "url": "/uploads/" + fname})


# 删除安装区域收货照片文件（仅 tom/cuong/james 可操作；前端逐张调用）
@app.route("/api/inst-zone-photos/<path:filename>", methods=["DELETE"])
def delete_inst_zone_photo(filename):
    filename = os.path.basename(filename)
    me = (request.args.get("me") or "").strip()
    if me not in ("tom", "cuong", "james"):
        return jsonify({"ok": False, "error": "no permission"}), 403
    if not filename.startswith("inzone_"):
        return jsonify({"ok": False, "error": "not a zone photo"}), 400
    path = os.path.join(UPLOAD_DIR, filename)
    try:
        if os.path.exists(path):
            os.remove(path)
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


# 删除收货单照片文件（仅 tom/cuong/james 可操作；删除收货单时前端逐张调用）
@app.route("/api/prod-receipt-photos/<path:filename>", methods=["DELETE"])
def delete_prod_receipt_photo(filename):
    filename = os.path.basename(filename)
    me = (request.args.get("me") or "").strip()
    if me not in ("tom", "cuong", "james"):
        return jsonify({"ok": False, "error": "no permission"}), 403
    if not filename.startswith("prec_"):
        return jsonify({"ok": False, "error": "not a receipt photo"}), 400
    path = os.path.join(UPLOAD_DIR, filename)
    try:
        if os.path.exists(path):
            os.remove(path)
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/api/won-projects/<int:pid>/attachments/<path:filename>", methods=["DELETE"])
def delete_attachment(pid, filename):
    filename = os.path.basename(filename)
    conn = get_db()
    row = conn.execute("SELECT attachments FROM won_projects WHERE id=?", (pid,)).fetchone()
    if not row:
        conn.close()
        return jsonify({"error":"not found"}),404
    try:
        atts = json.loads(row["attachments"]) if row["attachments"] else []
    except:
        atts = []
    atts = [a for a in atts if a.get("filename") != filename]
    conn.execute("UPDATE won_projects SET attachments=?, updated_at=datetime('now','localtime') WHERE id=?",
                 (json.dumps(atts, ensure_ascii=False), pid))
    conn.commit()
    try:
        os.remove(os.path.join(UPLOAD_DIR, filename))
    except:
        pass
    new_row = conn.execute("SELECT * FROM won_projects WHERE id=?", (pid,)).fetchone()
    conn.close()
    return jsonify(row_to_dict(new_row))

# ===================== 禁用前端缓存（根治"改了代码看不到效果"） =====================
# 原理：给 HTML/JS 响应加 Cache-Control: no-cache，浏览器每次都会向服务器校验
# 文件是否变化（ETag/Last-Modified 未变则返回 304，开销极小；变了立刻拿到新代码）。
# 此前 Flask 默认不带该头，Windows 浏览器会凭"启发式缓存"直接用本地旧副本，
# 导致改了 index.html / crm_table.js 后用户强刷也可能拿到旧版。
@app.after_request
def add_no_cache_headers(resp):
    try:
        mt = (resp.mimetype or '')
        if mt == 'text/html' or mt.startswith('application/javascript') or mt.startswith('text/javascript'):
            resp.headers['Cache-Control'] = 'no-cache'
    except Exception:
        pass
    return resp

# ===================== 桌面版：附件"按需取回" =====================
# 场景：用户刚装好、还没同步，或换了一台电脑 —— 界面里有附件引用，
#       但本机 uploads/ 里还没有文件。以前只能干等下一次同步，
#       现在点"查看/下载"时临时从云端取回并缓存到本机，之后离线也能打开。
CLOUD_BASE = "https://agi-gs.tomalso911.workers.dev"
# 云端 R2 的目录前缀（与 cloudflare/src 写入时保持一致）
_CLOUD_DIRS = ("crm-docs", "won-docs", "lost-docs", "crm", "won", "lost")


def _cloud_headers():
    """读取桌面版保存的云端令牌（sync.json）。未登录返回 None。"""
    try:
        with io.open(os.path.join(DATA_DIR, "sync.json"), "r", encoding="utf-8") as f:
            tok = (json.load(f) or {}).get("token", "")
        if not tok:
            return None
        return {"Authorization": "Bearer " + tok,
                "User-Agent": "AGI-PM-Desktop"}
    except Exception:
        return None


def _fetch_cloud_file(path):
    """从云端取回附件并缓存到 uploads/。成功返回本机文件名，失败返回 ''。

    path 可以是云端形态（/api/files/crm-docs/xxx.pdf）或纯文件名；
    纯文件名时依次尝试各业务目录（crm-docs / won-docs / lost-docs …）。
    """
    if not _cloud_headers():
        return ""
    import urllib.request

    name = os.path.basename(path or "")
    if not name:
        return ""
    s = (path or "").strip()
    cands = []
    if s.startswith("/api/files/"):
        cands.append(s)
    if "/" in s.strip("/"):
        cands.append("/api/files/" + s.lstrip("/"))
    cands += ["/api/files/%s/%s" % (d, name) for d in _CLOUD_DIRS]
    cands.append("/api/files/" + name)

    import urllib.error

    headers = _cloud_headers()
    for c in cands:
        try:
            req = urllib.request.Request(CLOUD_BASE + c, headers=headers)
            with urllib.request.urlopen(req, timeout=12) as r:
                data = r.read()
            if not data:
                continue
            with open(os.path.join(UPLOAD_DIR, name), "wb") as f:
                f.write(data)
            return name
        except urllib.error.HTTPError as e:
            # 401/403 = 令牌失效或未登录：再试其它目录也没用，立即放弃，
            # 避免每个缺失文件都空转 7 次网络请求（界面会卡住）。
            if e.code in (401, 403):
                return ""
            continue
        except Exception:
            continue
    return ""


@app.route("/uploads/<path:filename>")
def serve_upload(filename):
    filename = os.path.basename(filename)
    # 本机没有且已登录云端 → 临时取回一次（离线或云端也没有则 404）
    if not os.path.isfile(os.path.join(UPLOAD_DIR, filename)):
        got = _fetch_cloud_file(filename)
        if got:
            filename = got
    return send_from_directory(UPLOAD_DIR, filename)


@app.route("/api/files/<path:filename>")
def serve_api_file(filename):
    """桌面版专用：兼容【云端形态】的附件路径 /api/files/<目录>/<文件名>。

    为什么必须有这条路由（V2026.09.05.29 修复）：
      云端把附件引用存成 "/api/files/crm-docs/xxx.pdf"，网页端由 Worker
      从 R2 取回，一切正常；但桌面版跑的是本机 Flask，以前没有这条路由，
      于是界面里"查看/下载 PDF"发出的 /api/files/... 请求一律 404 ——
      表现就是"桌面版不能预览、也不能下载 PDF"，而网页端同样的按钮是好的。

    处理：按【文件名】从本机 uploads/ 提供（同步已把文件下载到该目录）。
    带 ?dl=1 时按附件下载，否则内联预览（与云端 files.js 行为一致）。
    """
    name = os.path.basename(filename or "")
    if not name:
        return jsonify({"error": "file not found"}), 404
    if not os.path.isfile(os.path.join(UPLOAD_DIR, name)):
        # 本机还没这个文件（未同步 / 换电脑）→ 已登录则临时从云端取回
        got = _fetch_cloud_file(filename)
        if not got:
            return jsonify({"error": "file not found", "missing": name}), 404
        name = got
    as_att = (request.args.get("dl") or "").strip() not in ("", "0", "false")
    return send_from_directory(UPLOAD_DIR, name, as_attachment=as_att)


# 离线桌面版：把第三方前端库（html2canvas / jsPDF / chart.js 等）随 exe 打包在
# BASE_DIR/vendor 下，前端用 /vendor/xxx 同源加载，断网也能用打印 PDF / 容量饼图。
@app.route("/vendor/<path:filename>")
def serve_vendor(filename):
    vendor_dir = os.path.join(BASE_DIR, "vendor")
    return send_from_directory(vendor_dir, filename)


# ===================== 财务管理：越南报表（Univer）本地落盘 =====================
# 前端用 Univer 打开并可编辑；保存时把整本 xlsx 写回服务器文件。
# 历史行不会被删除（财务只在末尾插行），实现“数据单向递增”。
# 每日自动一份备份（滚动保留 30 天）；支持按月/按年生成快照存档。
import datetime as _fdt

FIN_DIR = os.path.join(BASE_DIR, "finance_data")
FIN_REPORT = os.path.join(FIN_DIR, "vn_report.xlsx")
FIN_BACKUP_DIR = os.path.join(FIN_DIR, "backups")
FIN_ARCHIVE_DIR = os.path.join(FIN_DIR, "archive")
for _d in (FIN_DIR, FIN_BACKUP_DIR, FIN_ARCHIVE_DIR):
    os.makedirs(_d, exist_ok=True)

# ---- 快照缓存（FIN-SNAP-CACHE-20261011）----------------------------------------
# 为什么需要：GET /api/finance/vn-report/snapshot 原先【每次】都用 openpyxl 把整本
# xlsx 重新转成 Univer 快照，一次要好几秒；上传（或每次自动保存）之后，每刷新一次
# 就再来一遍，用户体感就是「又慢又总是在加载」。
# 做法：以【源 xlsx 的 mtime(ns) + 文件大小 + 路径】为缓存键，把转换结果落盘为
# finance_data/vn_report.snapshot.<键哈希>.json；命中就直接把这个文件发出去
# （send_from_directory + conditional=True → 浏览器带 If-None-Match/If-Modified-Since
#  时直接 304，连 JSON 都不用传）。
#
# ★★ Windows 关键点：快照文件【按缓存键命名】，重建时写的是新文件名，绝不去覆盖
#    可能正被上一次响应读着的旧文件。最初写成「固定文件名 + os.replace 覆盖」，
#    实测（_fin_snap_test.py 第 4 步）会因目标文件正被读而报
#    WinError 5 Access denied → 500。切换缓存靠那个【从不对外发送】的小键文件，
#    它自身写入则是原子的（.tmp + os.replace）。
#
# ★ 契约：任何改写 FIN_REPORT 的地方都必须调用 _fin_cache_invalidate()，
#   否则会读到旧快照。硬锁脚本 check_fin_snap_cache.py 会静态检查这三处。
import threading as _fthreading

FIN_SNAP_KEY = os.path.join(FIN_DIR, "vn_report.snapshot.key")
FIN_SNAP_PREFIX = "vn_report.snapshot."
_FIN_SNAP_LOCK = _fthreading.Lock()


def _fin_report_key():
    """缓存键 = 源 xlsx 的 mtime(ns) + 大小 + 路径；文件不存在返回 None。"""
    try:
        st = os.stat(FIN_REPORT)
    except OSError:
        return None
    return "%d:%d:%s" % (st.st_mtime_ns, st.st_size, FIN_REPORT)


def _fin_cache_name(key):
    """快照文件名由【缓存键】派生：源文件一变名字就变，旧文件永远不会被覆盖。"""
    return "%s%s.json" % (FIN_SNAP_PREFIX, hashlib.sha1(key.encode("utf-8")).hexdigest()[:16])


def _fin_cache_files():
    """当前目录下所有快照文件（含旧键遗留的，用于清理）。"""
    try:
        return [fn for fn in os.listdir(FIN_DIR)
                if fn.startswith(FIN_SNAP_PREFIX) and fn.endswith(".json")]
    except OSError:
        return []


def _fin_cache_current():
    """返回 (当前键, 当前可用的快照绝对路径或 None)。"""
    key = _fin_report_key()
    if key is None:
        return None, None
    try:
        with open(FIN_SNAP_KEY, "r", encoding="utf-8") as fh:
            got = fh.read().strip()
    except OSError:
        return key, None
    if got != key:
        return key, None
    path = os.path.join(FIN_DIR, _fin_cache_name(key))
    return key, (path if os.path.isfile(path) else None)


def _fin_cache_valid():
    """键文件 = 当前源文件的键，且对应快照文件在 → 缓存可用。"""
    return _fin_cache_current()[1] is not None


def _fin_cache_invalidate():
    """源 xlsx 被改写后必须调用：丢掉键与所有快照（下次 GET 重新转换并缓存）。
    删不掉的（正被某个响应读着）留到下次 _fin_cache_build 里再清，不影响正确性。"""
    try:
        os.remove(FIN_SNAP_KEY)
    except OSError:
        pass
    for fn in _fin_cache_files():
        try:
            os.remove(os.path.join(FIN_DIR, fn))
        except OSError:
            pass


def _fin_cache_build(force=False):
    """把 xlsx 转成快照并落盘。返回 (ok, detail)；detail ∈ hit/built/错误原因。
    ★顺序不可颠倒：先把快照写成【新文件名】并原子就位，最后才切键文件 ——
      保证「有键必有完整快照」，绝不会把半截 JSON 发出去。"""
    key = _fin_report_key()
    if key is None:
        return False, "not initialized"
    with _FIN_SNAP_LOCK:
        if not force and _fin_cache_valid():
            return True, "hit"
        try:
            sys.path.insert(0, BASE_DIR)
            import univer_convert
            snap = univer_convert.xlsx_to_univer(FIN_REPORT)
        except Exception as e:
            return False, "convert failed: %s" % e
        path = os.path.join(FIN_DIR, _fin_cache_name(key))
        part = path + ".part"
        tmp_key = FIN_SNAP_KEY + ".tmp"
        try:
            with open(part, "w", encoding="utf-8") as fh:
                json.dump(snap, fh, ensure_ascii=False, separators=(",", ":"))
            os.replace(part, path)          # 新文件名，不可能撞上正被读的旧文件
            with open(tmp_key, "w", encoding="utf-8") as fh:
                fh.write(key)
            os.replace(tmp_key, FIN_SNAP_KEY)   # 键文件最后才切（它从不对外发送）
        except OSError as e:
            for p in (part, tmp_key):
                try:
                    os.remove(p)
                except OSError:
                    pass
            return False, "cache write failed: %s" % e
        # 清掉旧键遗留下来的快照（删不掉的留到下次，不影响正确性）
        keep = os.path.basename(path)
        for fn in _fin_cache_files():
            if fn != keep:
                try:
                    os.remove(os.path.join(FIN_DIR, fn))
                except OSError:
                    pass
        return True, "built"


def _fin_daily_backup():
    """每日一份备份；删除超过 30 天的旧备份，磁盘占用封顶约 30 份。"""
    today = _fdt.date.today().strftime("%Y-%m-%d")
    bpath = os.path.join(FIN_BACKUP_DIR, "vn_report_%s.xlsx.bak" % today)
    if not os.path.isfile(bpath) and os.path.isfile(FIN_REPORT):
        try:
            shutil.copyfile(FIN_REPORT, bpath)
        except OSError:
            pass
    cutoff = _fdt.date.today() - _fdt.timedelta(days=30)
    for fn in os.listdir(FIN_BACKUP_DIR):
        if not (fn.startswith("vn_report_") and fn.endswith(".xlsx.bak")):
            continue
        try:
            d = _fdt.datetime.strptime(fn[len("vn_report_"):-len(".xlsx.bak")], "%Y-%m-%d").date()
        except Exception:
            continue
        if d < cutoff:
            try:
                os.remove(os.path.join(FIN_BACKUP_DIR, fn))
            except OSError:
                pass


@app.route("/api/finance/vn-report", methods=["GET"])
def fin_get_report():
    # 尚未初始化（无种子文件）时返回 404，前端提示先导入
    if not os.path.isfile(FIN_REPORT):
        return jsonify({"error": "not initialized"}), 404
    return send_from_directory(
        FIN_DIR, "vn_report.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=False,
    )


@app.route("/api/finance/vn-report", methods=["POST"])
def fin_save_report():
    data = request.get_data()
    if not data:
        return jsonify({"error": "empty"}), 400
    tmp = FIN_REPORT + ".tmp"
    with open(tmp, "wb") as fh:
        fh.write(data)
    try:
        os.replace(tmp, FIN_REPORT)  # 原子替换，避免半写损坏
    except OSError:
        # Windows 下目标文件偶被占用，退回直接覆盖写
        with open(FIN_REPORT, "wb") as fh:
            fh.write(data)
        try:
            os.remove(tmp)
        except OSError:
            pass
    _fin_daily_backup()
    _fin_cache_invalidate()   # ★源文件已改写：必须丢掉旧快照缓存
    return jsonify({
        "ok": True,
        "bytes": len(data),
        "saved_at": _fdt.datetime.now().isoformat(timespec="seconds"),
    })


@app.route("/api/finance/vn-report/snapshot", methods=["POST"])
def fin_snapshot_report():
    period = (request.args.get("period") or "").strip()
    if not period:
        return jsonify({"error": "period required"}), 400
    m = re.match(r"^(\d{4})(?:-(\d{1,2}))?$", period)
    if not m:
        return jsonify({"error": "period format YYYY or YYYY-MM"}), 400
    if m.group(2) and not (1 <= int(m.group(2)) <= 12):
        return jsonify({"error": "month out of range"}), 400
    # 归一化月份为两位：2026-5 -> 2026-05
    period = m.group(1) if not m.group(2) else ("%s-%02d" % (m.group(1), int(m.group(2))))
    if not os.path.isfile(FIN_REPORT):
        return jsonify({"error": "not initialized"}), 404
    os.makedirs(FIN_ARCHIVE_DIR, exist_ok=True)
    dest = os.path.join(FIN_ARCHIVE_DIR, "vn_%s.xlsx" % period)
    shutil.copyfile(FIN_REPORT, dest)
    return jsonify({"ok": True, "file": "vn_%s.xlsx" % period})


@app.route("/api/finance/vn-report/init", methods=["POST"])
def fin_init_report():
    # 仅用于“重新初始化/换表”：上传一份 xlsx 作为新种子（覆盖旧文件与备份）。
    if "file" not in request.files:
        return jsonify({"error": "no file"}), 400
    f = request.files["file"]
    if not f.filename:
        return jsonify({"error": "empty filename"}), 400
    data = f.read()
    if not data:
        return jsonify({"error": "empty"}), 400
    tmp = FIN_REPORT + ".tmp"
    with open(tmp, "wb") as fh:
        fh.write(data)
    os.replace(tmp, FIN_REPORT)
    _fin_daily_backup()
    # ★三语自动补全（FIN-TRI-AUTO-20261013）：上传的若是普通"单块"报表
    #   （ZH 块 K–R / EN 块 U–AB 为空），前端 fin_isTrilingualSheet 会把它判成
    #   "非三语表"并【完全不翻译】——这就是"换了新报表却不会自动翻译"的根因。
    #   这里就地补出两块 + 重写表名三语映射，前端刷新后即可三语切换。
    #   ★译文优先取持久缓存 finance_data/fin_trans_cache.json：已翻过的绝不重复请求，
    #     只翻【新增条目】；译文写回 xlsx 即"离线版本"，固定住。
    #   ★翻译 API 不可达时 fin_trilingual 不碰文件（绝不把源文当译文灌进 K/U）。
    _tri = {"ok": False, "reason": "skipped"}
    try:
        sys.path.insert(0, BASE_DIR)
        import fin_trilingual
        _tri = fin_trilingual.ensure_report(FIN_REPORT)
        sys.stderr.write("[fin_init_report] trilingual: %s\n" % _tri)
        sys.stderr.flush()
    except Exception as _te:
        sys.stderr.write("[fin_init_report] trilingual failed: %s\n" % _te)
        sys.stderr.flush()
    _fin_cache_invalidate()   # ★新种子：丢掉旧快照缓存
    # 上传是一次明确的用户动作（本来就在等），这里顺手把快照转换一次并缓存，
    # 于是上传后那一次自动刷新也能直接命中缓存，不再重新解析 xlsx。
    _warm_ok, _warm_detail = _fin_cache_build(force=True)
    if not _warm_ok:
        # 预热失败不影响上传结果：留着缓存不写，下次 GET 再惰性转换
        sys.stderr.write("[fin_init_report] snapshot warm failed: %s\n" % _warm_detail)
        sys.stderr.flush()
    return jsonify({"ok": True, "bytes": len(data),
                    "snapshot": "built" if _warm_ok else "lazy",
                    "trilingual": _tri})


@app.route("/api/finance/vn-report/snapshot", methods=["GET"])
def fin_get_snapshot():
    # 返回 Univer 快照（JSON），前端 createUniverSheet 加载（xlsx->快照在后端用 openpyxl 完成）。
    # ★ 命中缓存（源 xlsx 未变）就直接发缓存文件，不再重新解析 xlsx：
    #   conditional=True → 浏览器已存有同一份时回 304，连 JSON 都不必再传一遍。
    if not os.path.isfile(FIN_REPORT):
        return jsonify({"error": "not initialized"}), 404
    _snap_key, _snap_path = _fin_cache_current()
    if _snap_path is None:
        ok, detail = _fin_cache_build(force=True)
        if not ok:
            return jsonify({"error": detail}), 500
        _snap_key, _snap_path = _fin_cache_current()
        if _snap_path is None:
            return jsonify({"error": "cache unavailable"}), 500
    resp = send_from_directory(FIN_DIR, os.path.basename(_snap_path),
                               mimetype="application/json", conditional=True)
    resp.headers["Content-Type"] = "application/json; charset=utf-8"
    resp.headers["X-Fin-Snap-Cache"] = "hit"
    return resp


@app.route("/api/finance/sheet-titles", methods=["GET"])
def fin_sheet_titles():
    """各 sheet 的三语标签名（供前端语言切换时改工作表标签）。
    ?kind=vn（默认）→ finance_data/fin_sheet_titles.json
    ?kind=cn        → finance_data/fin_sheet_titles_cn.json（中国报表，只有「实际支出」一张表）
    ★两份文件分开存放，中国报表绝不会覆盖越南那份（DABACO 保护词就在越南那份里）。"""
    kind = (request.args.get("kind") or "vn").strip().lower()
    fname = "fin_sheet_titles_cn.json" if kind == "cn" else "fin_sheet_titles.json"
    p = os.path.join(FIN_DIR, fname)
    titles = {}
    if os.path.isfile(p):
        try:
            with open(p, encoding="utf-8") as fh:
                titles = json.load(fh) or {}
        except Exception:
            titles = {}
    return jsonify({"ok": True, "kind": kind, "titles": titles})


@app.route("/api/finance/convert-currency", methods=["POST"])
def fin_convert_currency():
    """整张报表用【同一个汇率】（报表截至日 = "As of <date>" 或报表内最大日期）折算。
       因为只是"全表乘同一常数"，D-E=F、小计、滚动余额、跨表汇总(TỔNG HỢP)等恒等式全部守恒，
       不会出现"逐行汇率不同→毛额误差淹没净额→正数变负数"的问题。
       - values：只给【静态数字格】的换算值；公式格不写值，交给表格自身重算（同一汇率 → 结果一致）。
       - fmt   ：所有金额格（含公式格、汇总表 TỔNG HỢP）的 0 基 row/col，供前端统一套货币格式。

       ★kind=cn（中国报表，FIN-CN-CURRENCY-20261013）：中国报表的金额【基准币种是人民币】，
         所以换算方向与越南报表相反：目标 RMB=原值；USD=num÷USDCNY；VND=num×CNYVND。
         表头与越南那张「Chi thực tế」完全一致（A=Ngày hạch toán、D=Thu、E=Chi），
         所以下面的列识别逻辑【一个字都不用改】，只是把源文件换成 cn_report.xlsx。"""
    data = request.get_json(force=False, silent=True) or {}
    kind = (data.get("kind") or "vn").strip().lower()
    if kind not in ("vn", "cn"):
        kind = "vn"
    target = (data.get("target") or "").upper().replace("CNY", "RMB").replace("¥", "RMB")
    if target not in ("VND", "USD", "RMB"):
        return jsonify({"ok": False, "error": "target must be VND/USD/RMB"}), 400
    report = CN_REPORT if kind == "cn" else FIN_REPORT
    if not os.path.isfile(report):
        return jsonify({"ok": False, "error": "report not initialized"}), 404

    # 读历史汇率缓存（USD→VND、USD→CNY），推导 CNY→VND（保留精度）
    conn = get_db()
    try:
        fx = _fx_load_cache(conn)
    finally:
        conn.close()
    usdvnd = fx.get("USDVND", {})
    usdcny = fx.get("USDCNY", {})
    cnyvnd = {}
    for d, u in usdvnd.items():
        c = usdcny.get(d)
        if c:
            cnyvnd[d] = u / c

    def nearest_rate(date_str, rate_map):
        if not rate_map or not date_str:
            return None
        if date_str in rate_map:
            return rate_map[date_str]
        earlier = [d for d in rate_map if d <= date_str]
        if earlier:
            return rate_map[max(earlier)]
        later = [d for d in rate_map if d >= date_str]
        if later:
            return rate_map[min(later)]
        return None

    def norm_header(v):
        if not v:
            return ""
        s = str(v).lower()
        for a, b in (("à","a"),("á","a"),("ạ","a"),("ả","a"),("ã","a"),("ă","a"),("ắ","a"),("ằ","a"),("ẳ","a"),("ẵ","a"),("ặ","a"),("â","a"),("ấ","a"),("ầ","a"),("ẩ","a"),("ẫ","a"),("ậ","a"),
                     ("đ","d"),("é","e"),("è","e"),("ẻ","e"),("ẽ","e"),("ẹ","e"),("ê","e"),("ế","e"),("ề","e"),("ể","e"),("ễ","e"),("ệ","e"),
                     ("í","i"),("ì","i"),("ỉ","i"),("ĩ","i"),("ị","i"),
                     ("ó","o"),("ò","o"),("ỏ","o"),("õ","o"),("ọ","o"),("ô","o"),("ố","o"),("ồ","o"),("ổ","o"),("ỗ","o"),("ộ","o"),("ơ","o"),("ớ","o"),("ờ","o"),("ở","o"),("ỡ","o"),("ợ","o"),
                     ("ú","u"),("ù","u"),("ủ","u"),("ũ","u"),("ụ","u"),("ư","u"),("ứ","u"),("ừ","u"),("ử","u"),("ữ","u"),("ự","u"),
                     ("ý","y"),("ỳ","y"),("ỷ","y"),("ỹ","y"),("ỵ","y")):
            s = s.replace(a, b)
        return s

    wbD = openpyxl.load_workbook(report, data_only=True)     # 缓存值
    wbF = openpyxl.load_workbook(report, data_only=False)    # 公式

    ASOF_RE = re.compile(r"as of\s+([A-Za-z]{3,9})\s+(\d{1,2}),\s*(\d{4})", re.I)
    asof_text = None
    max_date = None
    sheets = []   # (title, header_row, amount_cols)
    for ws in wbD.worksheets:
        wsF = wbF[ws.title]
        # (a) 抓 "As of <date>" 文本（前 8 行 × 前 6 列）
        for r in range(1, min(ws.max_row, 8) + 1):
            for c in range(1, min(ws.max_column, 6) + 1):
                v = ws.cell(r, c).value
                if isinstance(v, str) and "as of" in v.lower():
                    m = ASOF_RE.search(v)
                    if m:
                        raw = "%s %s, %s" % (m.group(1), m.group(2), m.group(3))
                        for fmt in ("%b %d, %Y", "%B %d, %Y"):
                            try:
                                asof_text = datetime.strptime(raw, fmt).strftime("%Y-%m-%d")
                                break
                            except Exception:
                                pass
        # (b) 明细表：A 列表头为 Ngày hạch toán，且含精确 thu/chi/ton → VI+10+20 三块金额列
        header_row = None
        amount_cols = []
        for r in range(1, min(ws.max_row, 20) + 1):
            first10 = [norm_header(ws.cell(r, c).value) for c in range(1, min(ws.max_column, 10) + 1)]
            if not (first10 and ("ngay" in first10[0] or "hach toan" in first10[0])):
                continue
            found = [i + 1 for i, h in enumerate(first10) if h in ("thu", "chi", "ton")]
            if found:
                header_row = r
                cols = []
                for c in found:
                    for cc in (c, c + 10, c + 20):
                        if cc <= ws.max_column:
                            cols.append(cc)
                amount_cols = sorted(set(cols))
                break
        # (c) 汇总表（如 TỔNG HỢP）：列头含 amount / số tiền
        if not amount_cols:
            for r in range(1, min(ws.max_row, 20) + 1):
                hits = []
                for c in range(1, min(ws.max_column, 30) + 1):
                    h = norm_header(ws.cell(r, c).value)
                    if ("amount" in h) or ("so tien" in h):
                        hits.append(c)
                if hits:
                    header_row = r
                    amount_cols = sorted(set(hits))
                    break
        # (d) 该表最大日期（用于兜底"截至日"）
        for r in range(1, ws.max_row + 1):
            v = ws.cell(r, 1).value
            if isinstance(v, datetime):
                ds = v.strftime("%Y-%m-%d")
                if max_date is None or ds > max_date:
                    max_date = ds
        if amount_cols:
            sheets.append((ws.title, header_row, amount_cols))

    asof = asof_text or max_date
    usd_rate = nearest_rate(asof, usdvnd)      # 1 USD = ? VND
    cny_rate = nearest_rate(asof, cnyvnd)      # 1 CNY = ? VND
    usdcny_rate = nearest_rate(asof, usdcny)   # 1 USD = ? CNY
    # ★基准币种 = VND（越南报表与中国报表一样）。
    #   中国报表里的金额同样是【越南盾】口径（用户 2026-10-13 实测：7560000 ÷ 3882.17 = 1947.36
    #   就是他屏幕上看到的 ¥1,947），用户明确要求「参考越南财务报表里面的逻辑」做换算，
    #   所以两张报表共用同一套 VND 基准的算法；kind 只用来选【哪份文件/哪张表】。
    base = "VND"

    def _convert(num):
        """按【VND 基准】换算到目标币种（越/中两张报表共用；同一汇率 → 恒等式守恒）。"""
        if target == "VND":
            return num
        if target == "USD":
            return round(num / usd_rate, 2) if usd_rate else num
        return round(num / cny_rate, 2) if cny_rate else num               # RMB

    values = {}
    fmt = {}
    for (title, header_row, amount_cols) in sheets:
        wsD = wbD[title]
        wsF = wbF[title]
        vmap = {}
        flist = []
        for r in range(header_row + 1, wsD.max_row + 1):
            for c in amount_cols:
                cached = wsD.cell(r, c).value
                frm = wsF.cell(r, c).value
                is_formula = isinstance(frm, str) and frm.startswith("=")
                num = None
                if is_formula:
                    # 纯数字常量公式（如 "=150000000"）其实是硬编码金额 → 当静态值换算；
                    # 只有真正的计算式（=SUM(...)、=D5-E5、=+F..+D..-E..）才交给表格重算。
                    lit = frm[1:].strip().lstrip("+").strip()
                    try:
                        num = float(lit)
                    except Exception:
                        num = None
                elif cached is not None:
                    try:
                        num = float(cached)
                    except Exception:
                        num = None

                is_real_formula = is_formula and num is None
                if num is None and not is_real_formula:
                    continue                     # 空格：不写值也不套格式
                flist.append([r - 1, c - 1])     # 套货币格式（含真公式格）
                if is_real_formula:
                    continue                     # 真公式格：交给表格自身重算，不覆盖
                vmap.setdefault(r - 1, {})[c - 1] = _convert(num)
        if vmap:
            values[title] = vmap
        if flist:
            fmt[title] = flist

    if target == "USD":
        rate = usd_rate
    elif target == "RMB":
        rate = cny_rate
    else:
        rate = 1
    # ★factor = 「换算值 = 原值 × factor」的那个因子（前端在"外币显示下用户改了金额"时
    #   用它把输入值【换回基准币】再落盘，避免把外币数字当人民币写进文件）。
    factor = 1.0
    if target == "USD" and usd_rate:
        factor = 1.0 / usd_rate
    elif target == "RMB" and cny_rate:
        factor = 1.0 / cny_rate
    return jsonify({"ok": True, "kind": kind, "base": base, "target": target,
                    "asof": asof, "rate": rate, "factor": factor,
                    "values": values, "fmt": fmt})


@app.route("/api/finance/vn-report/save", methods=["POST"])
def fin_save_snapshot():
    # 接收 Univer 快照（JSON），写回 xlsx 落盘（快照->xlsx 在后端用 openpyxl 完成）
    data = request.get_json(force=False, silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "invalid json"}), 400
    try:
        sys.path.insert(0, BASE_DIR)
        import univer_convert
        tmp = FIN_REPORT + ".tmp.xlsx"
        univer_convert.univer_to_xlsx(data, tmp)
        try:
            os.replace(tmp, FIN_REPORT)
        except OSError:
            import shutil
            with open(FIN_REPORT, "wb") as fh:
                fh.write(open(tmp, "rb").read())
            try:
                os.remove(tmp)
            except OSError:
                pass
        _fin_daily_backup()
        _fin_cache_invalidate()   # ★快照已写回 xlsx：丢掉旧快照缓存
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        sys.stderr.write("[fin_save_snapshot] ERROR: %s\n%s\n" % (e, tb))
        sys.stderr.flush()
        return jsonify({"error": "convert failed: %s" % e}), 500
    return jsonify({"ok": True, "saved_at": _fdt.datetime.now().isoformat(timespec="seconds")})


# ===================== 财务管理：中国报表（Univer）本地落盘 =====================
# 用户要求（2026-10-13）：把越南财务报表的【整套表格逻辑】原样复制到中国财务报表，
# 差别只有一个——中国报表的 Excel 里【只有一张工作表「实际支出」】，其它 7 张表不需要。
#   · 文件      ：finance_data/cn_report.xlsx（工作表名「实际支出」）
#   · 快照缓存  ：cn_report.snapshot.<键哈希>.json + cn_report.snapshot.key（与越南同构）
#   · 每日备份  ：finance_data/backups/cn_report_<YYYY-MM-DD>.xlsx.bak（滚动 30 份）
#   · 接口      ：/api/finance/cn-report[/snapshot|/init|/save]
#   · 表名三语  ：finance_data/fin_sheet_titles_cn.json（与越南那份分开，互不覆盖）
#   · 核销列    ：工作表 AC 列（第 29 列）表头「核销」，下面是每行的勾选框
#   ★★「自动翻译」逻辑一个字都没改：仍然走前端那套 finTransCache + /api/translate +
#      fin_translate（FIN-TRANS-CHAIN）。这里只是把【数据源】从 vn_report.xlsx 换成
#      cn_report.xlsx，翻译链/缓存/保护词判定全部复用，不新增也不改写。
CN_REPORT = os.path.join(FIN_DIR, "cn_report.xlsx")
CN_SNAP_KEY = os.path.join(FIN_DIR, "cn_report.snapshot.key")
CN_SNAP_PREFIX = "cn_report.snapshot."
CN_TITLES_PATH = os.path.join(FIN_DIR, "fin_sheet_titles_cn.json")
_CN_SNAP_LOCK = _fthreading.Lock()

CN_SHEET_NAME = "实际支出"      # 中国报表唯一的工作表
CN_TITLE_ROW = 4                # 表头行（1 基）
CN_FIRST_DATA_ROW = 5           # 第一条数据行
CN_SEED_ROWS = 200              # 种子文件预留的空数据行数
CN_CHECK_COL = 29               # AC 列（1 基）＝核销勾选框列
CN_CHECK_HEAD = "核销"
CN_CHECK_ON = "☑"
CN_CHECK_OFF = "☐"
# 中国报表【数据区】字体颜色（用户要求：除"屏幕高亮的红色加粗行"外，其余行都是蓝色）。
# 纯蓝；想换成柔和的 Office 蓝就改成 "FF0070C0"。
CN_TEXT_BLUE = "FF0000FF"

# ============ 中国报表：默认人民币符号 + 黑色网格线（FIN-CN-MONEY-20261013）============
# 用户要求：① 中国财务报表里金额显示【人民币符号】，默认货币就是 RMB（越南报表仍是越南盾）；
#           ② 中国财务报表加上【黑色网格线】。
# ★为什么改 xlsx 文件而不是只改屏幕：保存链路（前端 finCnBuildSavePayload）是
#   「保留文件原样式、只更新值」，屏幕上现加的格式根本不会写回文件；反过来，文件里的格式会成为
#   单元格"基样式"，用户在 App 或 Excel 里新录入的内容会自动继承 → 一次到位、以后不用管。
#   （与 _cn_normalize_text_color 的蓝化、_cn_normalize_ac_align 的居中同一套理由。）
CN_MONEY_FMT = '"¥"#,##0'            # ★与前端 choice_lite.html 的 finCnMoneyFmt 必须完全一致
CN_MONEY_COLS = ("D", "E", "N", "O", "X", "Y")   # 三语块的「收入 / 支出」列
CN_BORDER_RGB = "FF000000"           # 黑色网格线
# 黑色网格线覆盖范围（1 基列区间）：A–AB；核销列 AC 由 _cn_border_cols() 追加 → 实际 A–AC 整行。
# ★用户 2026-10-13 报「网格线没完全做好」的根因：原来只刷三语块 A-E / K-O / U-Y，
#   而中国报表视图是「A–J + AC」（K–AB 被隐藏）—— F–J 这 5 列正好露在屏幕上却没有线。
#   现在整行都刷（隐藏的块也刷，逻辑上与语言无关、且改版隐藏范围时不会再漏）。
CN_BORDER_BLOCKS = ((1, 28),)


def _cn_make_seed_xlsx(path):
    """生成中国报表种子文件：只含一张「实际支出」表，三语表头与越南那张完全一致，
    并预留 AC 核销列（每行一个空勾选框 ☐）+ 末尾合计行。
    ★金额列带人民币符号（CN_MONEY_FMT）+ 整块黑色网格线（CN_BORDER_RGB），见上方区块说明。"""
    import openpyxl
    from openpyxl.styles import Font, Alignment
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = CN_SHEET_NAME
    bold = Font(bold=True)
    center = Alignment(horizontal="center", vertical="center")
    ws["A1"] = "SỔ CHI TIẾT CHI TIỀN"
    ws["K1"] = "付款明细账簿"
    ws["U1"] = "PAYMENTS DETAIL"
    ws["A2"] = "Tiền mặt + Tiền gửi ngân hàng"
    ws["K2"] = "现金 + 银行存款"
    ws["U2"] = "Cash + Bank deposits"
    ws.merge_cells("A1:E1")
    ws.merge_cells("A2:E2")
    for col, txt in (("A", "Ngày hạch toán"), ("B", "Số chứng từ"), ("C", "Diễn giải"),
                     ("D", "Thu"), ("E", "Chi"),
                     ("K", "记账日期"), ("L", "凭证号"), ("M", "摘要"),
                     ("N", "收入"), ("O", "支出"),
                     ("U", "Accounting date"), ("V", "Document No."), ("W", "Description"),
                     ("X", "Receipts"), ("Y", "Payments"),
                     ("AC", CN_CHECK_HEAD)):
        c = ws["%s%d" % (col, CN_TITLE_ROW)]
        c.value = txt
        c.font = bold
        c.alignment = center
    last = CN_FIRST_DATA_ROW + CN_SEED_ROWS - 1
    for r in range(CN_FIRST_DATA_ROW, last + 1):
        for col in ("A", "K", "U"):
            ws["%s%d" % (col, r)].number_format = "dd-mm-yyyy"
        for col in CN_MONEY_COLS:
            ws["%s%d" % (col, r)].number_format = CN_MONEY_FMT      # ★人民币符号
        ac = ws["AC%d" % r]
        ac.value = CN_CHECK_OFF
        ac.alignment = center          # ★勾选框水平+垂直居中（用户要求"选择框左右居中"）
    tot = last + 1
    _sum = "=SUM(E%d:E%d)" % (CN_FIRST_DATA_ROW, last)
    ws["C%d" % tot] = "TỔNG CỘNG"
    ws["E%d" % tot] = _sum
    ws["M%d" % tot] = "全部的"
    ws["O%d" % tot] = _sum
    ws["W%d" % tot] = "TOTAL"
    ws["Y%d" % tot] = _sum
    for col in CN_MONEY_COLS:
        ws["%s%d" % (col, tot)].number_format = CN_MONEY_FMT       # 合计行也带 ¥
    _cn_apply_borders(ws, 1, tot)      # ★黑色网格线（标题行 ~ 合计行）
    for col, w in (("A", 11.7), ("B", 11.3), ("C", 34.8), ("D", 11.7), ("E", 20.3), ("AC", 10)):
        ws.column_dimensions[col].width = w
    wb.save(path)


def _cn_border_cols():
    """要加黑色网格线的列号（1 基）：三语块 A-E / K-O / U-Y + 核销列 AC。"""
    cols = []
    for a, b in CN_BORDER_BLOCKS:
        cols.extend(range(a, b + 1))
    cols.append(CN_CHECK_COL)
    return cols


def _cn_has_thin_border(bd):
    """四边都已是细边框（thin）→ True（幂等判定用）。
    ★只比线型、不比颜色：Excel/主题色/ARGB 三种写法都可能是"黑"，比颜色容易误判成"要改"。"""
    for name in ("left", "right", "top", "bottom"):
        s = getattr(bd, name, None) if bd is not None else None
        if s is None or (s.style or "") != "thin":
            return False
    return True


def _cn_apply_borders(ws, first_row, last_row):
    """给中国报表的三语块 + 核销列刷黑色细边框，返回改动的格子数
    （0 = 本来就已经有网格线 → 调用方不必重写文件、也不会白动 mtime）。

    ★必须跳过【合并区域里除左上角以外】的格子：Excel 只保留合并区左上角的边框，
      其它格子存盘后边框会被丢掉 —— 不跳过的话每次启动都会"发现少 8 个边框"→ 重写文件 →
      白动 mtime → 白重建一次快照缓存（实测就是合并的 A1:E1 / A2:E2 那 8 个格子）。"""
    from openpyxl.styles import Border, Side
    side = Side(style="thin", color=CN_BORDER_RGB)
    border = Border(left=side, right=side, top=side, bottom=side)
    skip = set()
    try:
        for rng in ws.merged_cells.ranges:
            for row in ws.iter_rows(min_row=rng.min_row, max_row=rng.max_row,
                                    min_col=rng.min_col, max_col=rng.max_col):
                for cell in row:
                    if (cell.row, cell.column) != (rng.min_row, rng.min_col):
                        skip.add((cell.row, cell.column))
    except Exception:
        pass
    changed = 0
    cols = _cn_border_cols()
    for r in range(first_row, last_row + 1):
        for c in cols:
            if (r, c) in skip:
                continue
            cell = ws.cell(row=r, column=c)
            if _cn_has_thin_border(cell.border):
                continue
            cell.border = border
            changed += 1
    return changed


def _cn_ws_save_atomic(wb, path=None):
    """★原子落盘（FIN-CN-ATOMIC-SAVE-20261013）：先写同目录临时文件，再 os.replace 顶替。
    为什么必须这样：归一化那几步（核销列居中 / 数据区蓝字 / 金额 ¥ 符号 / 黑色网格线）
    原来直接用 openpyxl 的 save 就地重写线上文件 ——
    实测就在这一瞬间读 cn_report.xlsx 会拿到坏 zip（BadZipFile: File is not a zip file），
    并发读快照拿到的内容会不完整；万一进程/断电中断，报表文件直接被写坏。"""
    p = path or CN_REPORT
    tmp = p + ".norm.tmp"
    wb.save(tmp)
    try:
        os.replace(tmp, p)
    except Exception:
        try:
            os.remove(tmp)
        except OSError:
            pass
        raise


def _cn_normalize_ac_align():
    """把中国报表 AC 列（核销）单元格设成【水平 + 垂直居中】——用户要求"选择框左右居中"。
    为什么必须改文件：保存链路（前端 finCnBuildSavePayload）写回时是【保留文件原样式、只更新值】，
       前端视图上的对齐不会被写进文件，所以只能落在 xlsx 里。
    幂等：已经居中的文件不会被重写（否则每次启动都动 mtime → 白重建一次快照缓存）。
    返回 True 表示改过文件（调用方据此让快照缓存失效）。"""
    if not os.path.isfile(CN_REPORT):
        return False
    try:
        import openpyxl
        from openpyxl.styles import Alignment
        wb = openpyxl.load_workbook(CN_REPORT)
        ws = wb[CN_SHEET_NAME] if CN_SHEET_NAME in wb.sheetnames else wb[wb.sheetnames[0]]
        col = openpyxl.utils.get_column_letter(CN_CHECK_COL)     # 29 -> 'AC'
        center = Alignment(horizontal="center", vertical="center")
        changed = 0
        for r in range(1, ws.max_row + 1):
            cell = ws["%s%d" % (col, r)]
            if cell.value is None or str(cell.value).strip() == "":
                continue
            a = cell.alignment
            if a and a.horizontal == "center" and a.vertical == "center":
                continue
            cell.alignment = center
            changed += 1
        if changed:
            _cn_ws_save_atomic(wb)
            sys.stderr.write("[fin-cn] 核销列 %d 个单元格已设为居中\n" % changed)
        return changed > 0
    except Exception as e:
        sys.stderr.write("[fin-cn] 核销列居中处理失败: %s\n" % e)
        return False


# 合计行标签（蓝化时跳过这些行）：三语块各自的合计文字
CN_TOTAL_LABELS = frozenset(["TỔNG CỘNG", "全部的", "TOTAL", "合计", "总计"])


def _cn_is_total_row(row_cells):
    """判定"合计行"：本行内只要有一个单元格的值正好是合计标签，就认为整行是合计行（不蓝化）。"""
    for c in row_cells:
        v = c.value
        if isinstance(v, str) and v.strip().upper() in CN_TOTAL_LABELS:
            return True
    return False


def _cn_normalize_text_color():
    """把中国报表【数据区】的字体设成蓝色 —— 用户要求：「除了红色加粗这一行以外的行，都改成蓝色」。

    ★为什么必须落进文件、而不是只改屏幕：
      保存链路（前端 finCnBuildSavePayload 里的 put()）是「保留文件原样式、只更新值」，
      屏幕上现加的颜色根本不会写回 xlsx；反过来，文件里的蓝色会成为单元格的"基样式"，
      用户在 App 或 Excel 里新录入的内容会自动继承蓝色 → 一次到位、以后不用管。
    ★与屏幕高亮的关系：高亮（红 + 粗）是【只显示在屏幕上】的，覆盖在蓝色之上，两者不冲突；
      FIN-HI-LOCK-20261011 的保存剥离只针对红（rgb 含 FF0000）+ 粗，蓝色不受影响。
    ★范围：第 CN_FIRST_DATA_ROW..CN_FIRST_DATA_ROW+CN_SEED_ROWS-1 行 × A..AB 列
      （AC 核销列保持黑色；表头行、合计行不动。
        要连表头/合计行一起变蓝，把下面的 first/last 调一下即可。）
    幂等：已经蓝色的格子跳过；没改动就完全不重写文件（避免白动 mtime）。"""
    if not os.path.isfile(CN_REPORT):
        return False
    try:
        import openpyxl
        from openpyxl.styles import Color
        from copy import copy as _cp
        wb = openpyxl.load_workbook(CN_REPORT)
        ws = wb[CN_SHEET_NAME] if CN_SHEET_NAME in wb.sheetnames else wb[wb.sheetnames[0]]
        first = CN_FIRST_DATA_ROW
        # ★行范围必须跟着【实际内容】走，不能只认种子预留的那 200 行：
        #   用户往里录/粘贴数据后行数可能超过 204；种子末尾的那一行是合计行，必须排除。
        last = max(CN_FIRST_DATA_ROW + CN_SEED_ROWS - 1, ws.max_row)
        max_col = CN_CHECK_COL - 1        # A..AB（AC 核销列不动）
        want = CN_TEXT_BLUE.lstrip('#').upper()[-6:]
        changed = 0
        for row in ws.iter_rows(min_row=first, max_row=last, min_col=1, max_col=max_col):
            if _cn_is_total_row(row):
                continue                  # ★合计行不蓝化（表头行/标题行本来就不在这个范围内）
            for cell in row:
                cur = getattr(getattr(cell.font, 'color', None), 'rgb', None)
                if isinstance(cur, str) and cur.lstrip('#').upper()[-6:] == want:
                    continue
                nf = _cp(cell.font)
                nf.color = Color(rgb=CN_TEXT_BLUE)
                cell.font = nf
                changed += 1
        if changed:
            _cn_ws_save_atomic(wb)
            sys.stderr.write("[fin-cn] 数据区 %d 个单元格字体已设为蓝色\n" % changed)
        return changed > 0
    except Exception as e:
        sys.stderr.write("[fin-cn] 数据区蓝色处理失败: %s\n" % e)
        return False


_CN_MONEY_TEXT_RE = re.compile(r"^\d{1,3}(?:,\d{3})+(?:\.\d+)?$|^\d+(?:\.\d+)?$")


def _cn_money_to_number(cell):
    """★把「文本型金额」转成真正的数字 —— 用户 2026-10-13 报「货币符号没体现」的真正原因。

    原始导出里金额常常是【文本】：'41,400,000\\xa0'（末尾还带一个不间断空格）。
    Excel/Univer 的数字格式对【文本】格一律不生效 —— 数字格式就算写成 "¥"#,##0，
    屏幕上照样只显示原文 '41,400,000'，永远看不到 ¥。所以必须先变成数字。
    ★只转「纯数字 / 千分位数字」字符串（'41,400,000'、'0'、'1,234.5'）；
      '41,400,000 VND'、含货币符号或文字的格子一律不碰（不猜、不丢信息）。
    已经是数字的格原样返回 False（幂等：第二次调用不会再改文件）。"""
    v = cell.value
    if not isinstance(v, str):
        return False
    raw = v.replace("\u00a0", " ").strip()
    if not raw or not _CN_MONEY_TEXT_RE.match(raw):
        return False
    try:
        n = float(raw.replace(",", ""))
    except ValueError:
        return False
    cell.value = int(n) if n == int(n) else n
    return True


def _cn_normalize_money_fmt():
    """中国报表【金额列】统一成人民币符号 —— 用户要求「中国财务报表里默认货币是 RMB」。

    ★为什么落进文件：见上方「默认人民币符号 + 黑色网格线」区块（保存链路只更新值、保留文件原样式）。
    ★范围：数据区 + 合计行（合计行也要带 ¥，否则最后一行光秃秃的）；
      行数按【实际内容】走（max(种子预留行, ws.max_row)），用户录到第 300 行也照样覆盖。
    ★与"币种下拉"的关系：这张报表的金额本来就是人民币，右下角下拉只做显示符号、不做换算。
    ★文本型金额先转数字（_cn_money_to_number）—— 否则数字格式对文本格不生效，永远看不到 ¥。
    幂等：已经等于 CN_MONEY_FMT 的格子跳过；完全没改动就不重写文件（避免白动 mtime）。
    返回 True 表示改过文件（调用方据此让快照缓存失效）。"""
    if not os.path.isfile(CN_REPORT):
        return False
    try:
        import openpyxl
        wb = openpyxl.load_workbook(CN_REPORT)
        ws = wb[CN_SHEET_NAME] if CN_SHEET_NAME in wb.sheetnames else wb[wb.sheetnames[0]]
        last = max(CN_FIRST_DATA_ROW + CN_SEED_ROWS, ws.max_row)   # 含合计行
        changed = 0
        num_fixed = 0
        for r in range(CN_FIRST_DATA_ROW, last + 1):
            for col in CN_MONEY_COLS:
                cell = ws["%s%d" % (col, r)]
                if _cn_money_to_number(cell):      # ★文本 → 数字
                    num_fixed += 1
                    changed += 1
                if (cell.number_format or "").strip() == CN_MONEY_FMT:
                    continue
                cell.number_format = CN_MONEY_FMT
                changed += 1
        if num_fixed:
            sys.stderr.write("[fin-cn] 金额列 %d 个「文本型金额」已转成数字（否则 ¥ 不显示）\n" % num_fixed)
        if changed:
            _cn_ws_save_atomic(wb)
            sys.stderr.write("[fin-cn] 金额列 %d 个单元格已套人民币符号 %s\n" % (changed, CN_MONEY_FMT))
        return changed > 0
    except Exception as e:
        sys.stderr.write("[fin-cn] 金额符号处理失败: %s\n" % e)
        return False


def _cn_normalize_border():
    """给中国报表加【黑色网格线】—— 用户要求「中国财务报表加上黑色网格线」。

    ★为什么落进文件：同上（屏幕上的边框不会被写回；文件里的边框会成为基样式被新录入的内容继承）。
    ★范围：A–AB 整行 + 核销列 AC（见 CN_BORDER_BLOCKS），行 1 ~ 最后一行（含标题行、表头行、合计行）。
    幂等：四边已是细边框的格子跳过（见 _cn_has_thin_border）；没改动就不重写文件。
    返回 True 表示改过文件（调用方据此让快照缓存失效）。"""
    if not os.path.isfile(CN_REPORT):
        return False
    try:
        import openpyxl
        wb = openpyxl.load_workbook(CN_REPORT)
        ws = wb[CN_SHEET_NAME] if CN_SHEET_NAME in wb.sheetnames else wb[wb.sheetnames[0]]
        last = max(CN_FIRST_DATA_ROW + CN_SEED_ROWS, ws.max_row)   # 含合计行
        changed = _cn_apply_borders(ws, 1, last)
        if changed:
            _cn_ws_save_atomic(wb)
            sys.stderr.write("[fin-cn] %d 个单元格已加黑色网格线\n" % changed)
        return changed > 0
    except Exception as e:
        sys.stderr.write("[fin-cn] 网格线处理失败: %s\n" % e)
        return False


def _cn_normalize_style():
    """中国报表外观归一化（幂等）：① AC 核销列居中；② 数据区字体蓝色；
    ③ 金额列人民币符号；④ 黑色网格线。
    返回 True 表示动过文件（调用方据此让快照缓存失效）。"""
    changed = False
    for fn, tag in ((_cn_normalize_ac_align, "核销列居中"),
                    (_cn_normalize_text_color, "数据区蓝色"),
                    (_cn_normalize_money_fmt, "金额人民币符号"),
                    (_cn_normalize_border, "黑色网格线")):
        try:
            if fn():
                changed = True
        except Exception as e:
            sys.stderr.write("[fin-cn] %s失败: %s\n" % (tag, e))
    return changed


def _cn_seed_if_missing():
    """中国报表文件/表名映射缺失时自动补一份（服务启动时调用，幂等）。"""
    try:
        if not os.path.isfile(CN_REPORT):
            _cn_make_seed_xlsx(CN_REPORT)
            sys.stderr.write("[fin-cn] 生成种子报表 %s\n" % CN_REPORT)
    except Exception as e:
        sys.stderr.write("[fin-cn] 生成种子报表失败: %s\n" % e)
    # 外观归一化：核销列居中 + 数据区字体蓝色（对"本次改动之前已生成"的旧文件也生效，
    # 用户不必手动删文件重生成）。动过文件就让快照缓存失效。
    try:
        if _cn_normalize_style():
            try:
                _cn_cache_invalidate()
            except Exception:
                pass
    except Exception:
        pass
    try:
        if not os.path.isfile(CN_TITLES_PATH):
            titles = {CN_SHEET_NAME: {"vi": "Chi thực tế", "zh": CN_SHEET_NAME,
                                      "en": "Actual Payments"}}
            with open(CN_TITLES_PATH, "w", encoding="utf-8") as fh:
                json.dump(titles, fh, ensure_ascii=False, indent=2)
    except Exception as e:
        sys.stderr.write("[fin-cn] 写表名映射失败: %s\n" % e)


# ---- 快照缓存（与越南同一套做法，只是源文件不同；FIN-SNAP-CACHE-20261011 同构）----
def _cn_report_key():
    """缓存键 = 中国报表 xlsx 的 mtime(ns) + 大小 + 路径；文件不存在返回 None。"""
    try:
        st = os.stat(CN_REPORT)
    except OSError:
        return None
    return "%d:%d:%s" % (st.st_mtime_ns, st.st_size, CN_REPORT)


def _cn_cache_name(key):
    """快照文件名由【缓存键】派生：源文件一变名字就变，旧文件永远不会被覆盖。"""
    return "%s%s.json" % (CN_SNAP_PREFIX, hashlib.sha1(key.encode("utf-8")).hexdigest()[:16])


def _cn_cache_files():
    try:
        return [fn for fn in os.listdir(FIN_DIR)
                if fn.startswith(CN_SNAP_PREFIX) and fn.endswith(".json")]
    except OSError:
        return []


def _cn_cache_current():
    """返回 (当前键, 当前可用的快照绝对路径或 None)。"""
    key = _cn_report_key()
    if key is None:
        return None, None
    try:
        with open(CN_SNAP_KEY, "r", encoding="utf-8") as fh:
            got = fh.read().strip()
    except OSError:
        return key, None
    if got != key:
        return key, None
    path = os.path.join(FIN_DIR, _cn_cache_name(key))
    return key, (path if os.path.isfile(path) else None)


def _cn_cache_valid():
    return _cn_cache_current()[1] is not None


def _cn_cache_invalidate():
    """中国报表 xlsx 被改写后必须调用：丢掉键与所有快照。"""
    try:
        os.remove(CN_SNAP_KEY)
    except OSError:
        pass
    for fn in _cn_cache_files():
        try:
            os.remove(os.path.join(FIN_DIR, fn))
        except OSError:
            pass


def _cn_cache_build(force=False):
    """把中国报表 xlsx 转成快照并落盘。返回 (ok, detail)；detail ∈ hit/built/错误原因。
    ★顺序与越南一致：先把快照写成【新文件名】原子就位，最后才切键文件。"""
    key = _cn_report_key()
    if key is None:
        return False, "not initialized"
    with _CN_SNAP_LOCK:
        if not force and _cn_cache_valid():
            return True, "hit"
        try:
            sys.path.insert(0, BASE_DIR)
            import univer_convert
            snap = univer_convert.xlsx_to_univer(CN_REPORT, snap_id="cn-report")
        except Exception as e:
            return False, "convert failed: %s" % e
        path = os.path.join(FIN_DIR, _cn_cache_name(key))
        part = path + ".part"
        tmp_key = CN_SNAP_KEY + ".tmp"
        try:
            with open(part, "w", encoding="utf-8") as fh:
                json.dump(snap, fh, ensure_ascii=False, separators=(",", ":"))
            os.replace(part, path)
            with open(tmp_key, "w", encoding="utf-8") as fh:
                fh.write(key)
            os.replace(tmp_key, CN_SNAP_KEY)
        except OSError as e:
            for p in (part, tmp_key):
                try:
                    os.remove(p)
                except OSError:
                    pass
            return False, "cache write failed: %s" % e
        keep = os.path.basename(path)
        for fn in _cn_cache_files():
            if fn != keep:
                try:
                    os.remove(os.path.join(FIN_DIR, fn))
                except OSError:
                    pass
        return True, "built"


def _cn_daily_backup():
    """每改一次中国报表就留一份当日备份（同一天只留一份，滚动 30 份）。"""
    try:
        if not os.path.isfile(CN_REPORT):
            return
        os.makedirs(FIN_BACKUP_DIR, exist_ok=True)
        stamp = _fdt.date.today().isoformat()
        dest = os.path.join(FIN_BACKUP_DIR, "cn_report_%s.xlsx.bak" % stamp)
        shutil.copyfile(CN_REPORT, dest)
        olds = sorted(fn for fn in os.listdir(FIN_BACKUP_DIR)
                      if fn.startswith("cn_report_") and fn.endswith(".xlsx.bak"))
        for fn in olds[:-30]:
            try:
                os.remove(os.path.join(FIN_BACKUP_DIR, fn))
            except OSError:
                pass
    except Exception as e:
        sys.stderr.write("[fin-cn] daily backup failed: %s\n" % e)


@app.route("/api/finance/cn-report", methods=["GET"])
def fin_cn_get_report():
    _cn_seed_if_missing()
    if not os.path.isfile(CN_REPORT):
        return jsonify({"error": "not initialized"}), 404
    return send_from_directory(FIN_DIR, "cn_report.xlsx", as_attachment=False,
                               mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


@app.route("/api/finance/cn-report", methods=["POST"])
def fin_cn_save_report():
    data = request.get_data() or b""
    if not data:
        return jsonify({"error": "empty body"}), 400
    tmp = CN_REPORT + ".tmp"
    with open(tmp, "wb") as fh:
        fh.write(data)
    os.replace(tmp, CN_REPORT)
    _cn_daily_backup()
    _cn_cache_invalidate()   # ★源文件已改写：必须丢掉旧快照缓存
    return jsonify({"ok": True, "bytes": len(data)})


@app.route("/api/finance/cn-report/snapshot", methods=["POST"])
def fin_cn_snapshot_report():
    """把当前中国报表按 period（YYYY / YYYY-MM）复制进 archive。"""
    period = (request.args.get("period") or "").strip()
    m = re.match(r"^(\d{4})(?:-(\d{1,2}))?$", period)
    if not m:
        return jsonify({"error": "period format YYYY or YYYY-MM"}), 400
    if m.group(2) and not (1 <= int(m.group(2)) <= 12):
        return jsonify({"error": "month out of range"}), 400
    period = m.group(1) if not m.group(2) else ("%s-%02d" % (m.group(1), int(m.group(2))))
    if not os.path.isfile(CN_REPORT):
        return jsonify({"error": "not initialized"}), 404
    os.makedirs(FIN_ARCHIVE_DIR, exist_ok=True)
    dest = os.path.join(FIN_ARCHIVE_DIR, "cn_%s.xlsx" % period)
    shutil.copyfile(CN_REPORT, dest)
    return jsonify({"ok": True, "file": "cn_%s.xlsx" % period})


@app.route("/api/finance/cn-report/init", methods=["POST"])
def fin_cn_init_report():
    """上传一份 xlsx 作为中国报表的新种子（覆盖旧文件与备份）。
    ★不调用 fin_trilingual：它写的是【越南】那份表名映射(fin_sheet_titles.json)，
      让中国报表去动它会把越南表名/保护词(DABACO)覆盖掉。中国报表的译文由前端
      那套完全相同的「跟翻 + 缓存」链路负责，逻辑不改。"""
    if "file" not in request.files:
        return jsonify({"error": "no file"}), 400
    f = request.files["file"]
    if not f.filename:
        return jsonify({"error": "empty filename"}), 400
    data = f.read()
    if not data:
        return jsonify({"error": "empty"}), 400
    tmp = CN_REPORT + ".tmp"
    with open(tmp, "wb") as fh:
        fh.write(data)
    os.replace(tmp, CN_REPORT)
    _cn_daily_backup()
    # ★新种子先做外观归一化（核销列居中 + 数据区蓝色），再重建快照
    try:
        _cn_normalize_style()
    except Exception as _ne:
        sys.stderr.write("[fin-cn] init normalize failed: %s\n" % _ne)
    _cn_cache_invalidate()   # ★新种子：丢掉旧快照缓存
    _warm_ok, _warm_detail = _cn_cache_build(force=True)
    if not _warm_ok:
        sys.stderr.write("[fin-cn] snapshot warm failed: %s\n" % _warm_detail)
    return jsonify({"ok": True, "bytes": len(data), "snapshot": "built" if _warm_ok else "lazy"})


def _cn_rev():
    """中国报表文件的版本号（mtime_ns + 字节数）—— 保存时的【乐观锁】。
    ★为什么需要（FIN-CN-REV-20261013，2026-10-13 实测事故）：
      用户在 A 标签页里录入金额 / 勾了核销，另一个【还开着旧数据的标签页】随后自动保存，
      把旧快照整份写回文件 → 新录入与勾选被静默回滚（文件金额变回 41,400,000、核销全变 ☐）。
      有了 rev：客户端只能提交"基于当前文件"的快照，版本对不上就拒收并让它重新加载。"""
    try:
        st = os.stat(CN_REPORT)
        return "%d-%d" % (int(st.st_mtime_ns), int(st.st_size))
    except OSError:
        return ""


def _cn_block_total(path, cols, r0=5, r1=205):
    """三语块里「某几个列」在数据区的绝对值合计 —— 用于判断落盘快照是否被"货币换算值"污染。
    ★为什么按列分组：三语块（A–E 越南文 / K–O 中文 / U–Y 英文）存的是【同一个越南盾数值】，
      所以基准块 D,E（第 4,5 列）与中文块 N,O（第 14,15 列）、英文块 X,Y（第 24,25 列）
      必须【同量级】。人民币换算污染的特征极其鲜明：基准块 ≈ 中文块 ÷ 3882.17。"""
    try:
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
        return t
    except Exception:
        return 0.0


@app.route("/api/finance/cn-report/snapshot", methods=["GET"])
def fin_cn_get_snapshot():
    """返回中国报表的 Univer 快照（命中缓存直发，conditional=True 支持 304）。"""
    _cn_seed_if_missing()
    if not os.path.isfile(CN_REPORT):
        return jsonify({"error": "not initialized"}), 404
    _snap_key, _snap_path = _cn_cache_current()
    if _snap_path is None:
        ok, detail = _cn_cache_build(force=True)
        if not ok:
            return jsonify({"error": detail}), 500
        _snap_key, _snap_path = _cn_cache_current()
        if _snap_path is None:
            return jsonify({"error": "cache unavailable"}), 500
    resp = send_from_directory(FIN_DIR, os.path.basename(_snap_path),
                               mimetype="application/json", conditional=True)
    resp.headers["Content-Type"] = "application/json; charset=utf-8"
    resp.headers["X-Fin-Snap-Cache"] = "hit"
    resp.headers["X-Fin-Rev"] = _cn_rev()      # ★版本号：前端保存时原样带回（乐观锁，见 _cn_rev）
    return resp


@app.route("/api/finance/cn-report/save", methods=["POST"])
def fin_cn_save_snapshot():
    """接收 Univer 快照（JSON），写回 cn_report.xlsx。
    ★中国报表是「手动保存」：前端不自动保存，用户点「保存」才走这里，
      所以刷新页面不会丢数据。"""
    data = request.get_json(force=False, silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "invalid json"}), 400
    # ★乐观锁（FIN-CN-REV-20261013）：前端带上它【加载时】的版本号（GET /snapshot 的 X-Fin-Rev）。
    #   版本对不上 ⇒ 期间有人（或另一个还开着旧数据的标签页）已经写过文件了。
    #   这时绝不能拿这份旧快照覆盖整份文件，否则别人刚录的金额/刚勾的核销会被静默回滚
    #   （2026-10-13 实测：文件被旧标签页从新数据覆盖回 41,400,000，核销全被抹成 ☐）。
    #   返回 HTTP 200 + stale:true（不是 4xx，避免浏览器控制台一片红），前端会重新加载后再让用户操作。
    _cli_rev = str(data.get("__rev") or "")
    _cur_rev = _cn_rev()
    if _cli_rev and _cur_rev and _cli_rev != _cur_rev:
        sys.stderr.write("[fin-cn] stale-blocked(rev %s != %s)\n" % (_cli_rev, _cur_rev))
        return jsonify({"ok": False, "stale": True, "rev": _cur_rev,
                        "error": "stale snapshot"}), 200
    _normalized = False        # ★数据区字色是否被本次保存修正过（返回值给前端决定要不要刷屏）
    try:
        sys.path.insert(0, BASE_DIR)
        import univer_convert
        tmp = CN_REPORT + ".tmp.xlsx"
        univer_convert.univer_to_xlsx(data, tmp)
        # ★★CN-BASIS-GUARD-20261013（服务端硬守卫，勿移除）★★
        #   为什么必须留在服务端：前端那套"把人民币显示值换回越南盾"的守卫依赖
        #     「当前下拉币种 + 汇率因子缓存 + 金额列登记」三个运行时状态，
        #     任何一个没就绪（切报表种类会把 finCnConvCur/finCnConvFactor 清零、缓存键丢失…）
        #     就会整段失效，而失效的表现是【静默】的：屏幕上的人民币数字被原样写进文件。
        #   2026-10-13 实测事故：基准块 D/E 被写成人民币换算值（41,400,000 → 10,664.14 → 再 ÷3882 → 2.75），
        #     每自动保存一次就再缩 3882 倍；而中文块 N/O、英文块 X/Y 还是真值 41,400,000，
        #     于是用户看到「中国报表的数据全变了」。
        #   本守卫用两个与前端状态无关的【文件级】判据把这种快照挡在落盘之前：
        #     ① 整表缩水：新基准块合计 / 旧基准块合计 < 0.02（≈÷3882 / ÷26292 的换算污染）；
        #     ② 三块不同量级：新基准块合计 / 新中文块合计 < 0.5（三语块必须同值，基准块被写成人民币了）。
        #   命中就【拒绝落盘】（删掉 tmp、保留服务器更正确的文件），
        #   返回 HTTP 200 + stale:true（不是 4xx，避免控制台一片红），前端收到 stale 会重新加载干净数据。
        try:
            _old_base = _cn_block_total(CN_REPORT, (4, 5))
            _new_base = _cn_block_total(tmp, (4, 5))
            _new_zh = _cn_block_total(tmp, (14, 15))
            _bad_total = bool(_old_base > 0 and _new_base > 0 and (_new_base / _old_base) < 0.02)
            _bad_ratio = bool(_new_zh > 0 and _new_base > 0 and (_new_base / _new_zh) < 0.5)
            if _bad_total or _bad_ratio:
                try:
                    os.remove(tmp)
                except OSError:
                    pass
                sys.stderr.write("[fin-cn] CN-BASIS-GUARD 拒绝落盘：%s (old_base=%.2f new_base=%.2f new_zh=%.2f ratio=%.8f)\n"
                                 % ("整表缩水" if _bad_total else "三块不同量级",
                                    _old_base, _new_base, _new_zh,
                                    (_new_base / _old_base) if _old_base else 0))
                sys.stderr.flush()
                return jsonify({"ok": True, "stale": True, "guard": "currency-regression",
                                "old_total": _old_base, "new_total": _new_base, "zh_total": _new_zh,
                                "rev": _cur_rev, "error": "amounts look like currency-converted values"}), 200
        except Exception as _ge:
            sys.stderr.write("[fin-cn] CN-BASIS-GUARD warning: %s\n" % _ge)
        try:
            os.replace(tmp, CN_REPORT)
        except OSError:
            with open(CN_REPORT, "wb") as fh:
                fh.write(open(tmp, "rb").read())
            try:
                os.remove(tmp)
            except OSError:
                pass
        _cn_daily_backup()
        _cn_cache_invalidate()   # ★快照已写回 xlsx：丢掉旧快照缓存
        # ★数据区字色归一化（用户要求：越/中/英三种语言块的数据区都必须是蓝字）：
        #   用户很可能是从别处【粘贴】进来（粘贴会带来源的黑色样式），所以每次保存后
        #   都在【文件层面】再刷一遍蓝色。幂等：已经蓝的格子不动，不会无谓重写文件。
        try:
            _normalized = bool(_cn_normalize_style())
        except Exception as _ne:
            sys.stderr.write("[fin-cn] save normalize failed: %s\n" % _ne)
        # ★重新生成快照：前端保存成功后会据此把屏幕也刷成蓝的
        try:
            _cn_cache_invalidate()
            _warm_ok, _warm_detail = _cn_cache_build(force=True)
            if not _warm_ok:
                sys.stderr.write("[fin-cn] snapshot warm failed: %s\n" % _warm_detail)
        except Exception as _we:
            sys.stderr.write("[fin-cn] snapshot rebuild failed: %s\n" % _we)
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        sys.stderr.write("[fin_cn_save_snapshot] ERROR: %s\n%s\n" % (e, tb))
        sys.stderr.flush()
        return jsonify({"error": "convert failed: %s" % e}), 500
    return jsonify({"ok": True, "saved_at": _fdt.datetime.now().isoformat(timespec="seconds"),
                    "normalized": bool(_normalized), "rev": _cn_rev()})


# ===================== API：合并财务总报表（FIN-MERGE-20261014）=====================
# 用户 2026-10-14 要求：「越南财务报表」里【不能】出现中国报表的数据，合并结果只体现于
# 「合并财务总报表」。因此合并结果落盘为【独立文件】merge_report.xlsx：
#   · vn_report.xlsx    = 干净版（只有越南记录）
#   · merge_report.xlsx = 合并版（越南 8 张表 + 中国「实际支出」记录，中国行蓝字）
# ★本接口【只读】该文件（前端也是只读模式）—— 绝不写回 vn_report.xlsx / cn_report.xlsx，
#   两个原文件与合并文件三者互不覆盖。
# 快照缓存机制与 vn / cn 完全一致：键 = mtime(ns)+size+路径，源文件一变缓存自动失效。
MERGE_REPORT = os.path.join(FIN_DIR, "merge_report.xlsx")
MERGE_SNAP_KEY = os.path.join(FIN_DIR, "merge_report.snapshot.key")
MERGE_SNAP_PREFIX = "merge_report.snapshot."
_MG_SNAP_LOCK = _fthreading.Lock()


def _mg_report_key():
    """缓存键 = 合并报表 xlsx 的 mtime(ns) + 大小 + 路径；文件不存在返回 None。"""
    try:
        st = os.stat(MERGE_REPORT)
    except OSError:
        return None
    return "%d:%d:%s" % (st.st_mtime_ns, st.st_size, MERGE_REPORT)


def _mg_cache_name(key):
    """快照文件名由【缓存键】派生：源文件一变名字就变，旧文件永远不会被覆盖。"""
    return "%s%s.json" % (MERGE_SNAP_PREFIX, hashlib.sha1(key.encode("utf-8")).hexdigest()[:16])


def _mg_cache_files():
    try:
        return [fn for fn in os.listdir(FIN_DIR)
                if fn.startswith(MERGE_SNAP_PREFIX) and fn.endswith(".json")]
    except OSError:
        return []


def _mg_cache_current():
    """返回 (当前键, 当前可用的快照绝对路径或 None)。"""
    key = _mg_report_key()
    if key is None:
        return None, None
    try:
        with open(MERGE_SNAP_KEY, "r", encoding="utf-8") as fh:
            got = fh.read().strip()
    except OSError:
        return key, None
    if got != key:
        return key, None
    path = os.path.join(FIN_DIR, _mg_cache_name(key))
    return key, (path if os.path.isfile(path) else None)


def _mg_cache_valid():
    return _mg_cache_current()[1] is not None


def _mg_cache_invalidate():
    """merge_report.xlsx 被改写后必须调用：丢掉键与所有快照。"""
    try:
        os.remove(MERGE_SNAP_KEY)
    except OSError:
        pass
    for fn in _mg_cache_files():
        try:
            os.remove(os.path.join(FIN_DIR, fn))
        except OSError:
            pass


def _mg_cache_build(force=False):
    """把合并报表 xlsx 转成快照并落盘。返回 (ok, detail)；detail ∈ hit/built/错误原因。
    ★顺序与越南/中国一致：先把快照写成【新文件名】原子就位，最后才切键文件。"""
    key = _mg_report_key()
    if key is None:
        return False, "not initialized"
    with _MG_SNAP_LOCK:
        if not force and _mg_cache_valid():
            return True, "hit"
        try:
            sys.path.insert(0, BASE_DIR)
            import univer_convert
            snap = univer_convert.xlsx_to_univer(MERGE_REPORT, snap_id="merge-report")
        except Exception as e:
            return False, "convert failed: %s" % e
        path = os.path.join(FIN_DIR, _mg_cache_name(key))
        part = path + ".part"
        tmp_key = MERGE_SNAP_KEY + ".tmp"
        try:
            with open(part, "w", encoding="utf-8") as fh:
                json.dump(snap, fh, ensure_ascii=False, separators=(",", ":"))
            os.replace(part, path)
            with open(tmp_key, "w", encoding="utf-8") as fh:
                fh.write(key)
            os.replace(tmp_key, MERGE_SNAP_KEY)
        except OSError as e:
            for p in (part, tmp_key):
                try:
                    os.remove(p)
                except OSError:
                    pass
            return False, "cache write failed: %s" % e
        keep = os.path.basename(path)
        for fn in _mg_cache_files():
            if fn != keep:
                try:
                    os.remove(os.path.join(FIN_DIR, fn))
                except OSError:
                    pass
        return True, "built"


@app.route("/api/finance/merge-report/snapshot", methods=["GET"])
def fin_mg_get_snapshot():
    """返回「合并财务总报表」的 Univer 快照（只读，命中缓存直发，conditional=True 支持 304）。
    文件不存在 → 404（前端提示未载入），绝不因此去改动 vn/cn 两个原文件。"""
    if not os.path.isfile(MERGE_REPORT):
        return jsonify({"error": "not initialized"}), 404
    _snap_key, _snap_path = _mg_cache_current()
    if _snap_path is None:
        ok, detail = _mg_cache_build(force=True)
        if not ok:
            return jsonify({"error": detail}), 500
        _snap_key, _snap_path = _mg_cache_current()
        if _snap_path is None:
            return jsonify({"error": "cache unavailable"}), 500
    resp = send_from_directory(FIN_DIR, os.path.basename(_snap_path),
                               mimetype="application/json", conditional=True)
    resp.headers["Content-Type"] = "application/json; charset=utf-8"
    resp.headers["X-Fin-Snap-Cache"] = "hit"
    return resp


# ===================== API：CRM 报价单 PDF 上传 =====================
@app.route("/api/crm-projects/<int:pid>/documents", methods=["POST"])
def upload_crm_pdf(pid):
    if "file" not in request.files:
        return jsonify({"error":"no file"}),400
    f = request.files["file"]
    if not f.filename:
        return jsonify({"error":"empty filename"}),400
    ext = os.path.splitext(f.filename)[1].lower()
    # 上传后二次校验：仅允许 PDF，且校验文件头 %PDF-
    if ext != ".pdf":
        return jsonify({"error":"invalid pdf"}),415
    # 槽位（pdf_equip/pdf_install/pdf_both）：带槽位才能找到被替换的旧文件
    slot = (request.form.get("slot") or request.args.get("slot") or "").strip()
    if slot not in ("pdf_equip", "pdf_install", "pdf_both"):
        slot = ""
    conn = get_db()
    row = conn.execute("SELECT id, pdf_equip, pdf_install, pdf_both FROM crm_projects WHERE id=?", (pid,)).fetchone()
    conn.close()
    if not row:
        return jsonify({"error":"not found"}),404
    base = safe_name(f.filename)
    fname = f"{int(time.time()*1000)}_{base}"
    fpath = os.path.join(UPLOAD_DIR, fname)
    f.save(fpath)
    # 上传后二次校验：跳过 UTF-8 BOM 与前导空白后，文件头必须为 %PDF-
    with open(fpath,"rb") as fh:
        data = fh.read(1024)
    i = 0
    while i < len(data) and (data[i] in (0x20, 0x09, 0x0A, 0x0D) or
                             (data[i:i+3] == b"\xef\xbb\xbf")):
        if data[i:i+3] == b"\xef\xbb\xbf":
            i += 3
        else:
            i += 1
    is_pdf = data[i:i+5] == b"%PDF-"
    if not is_pdf:
        try:
            os.remove(fpath)
        except Exception:
            pass
        return jsonify({"error":"invalid pdf"}),415
    # ★ 替换上传：新文件已验证合法，删除该槽位被替换的旧文件（维护磁盘空间）
    if slot:
        _cleanup_replaced_pdf(row[slot], fname)
    return jsonify({"ok":True, "filename": fname, "url": f"/uploads/{fname}"})

# ===================== API：WON 设备/安装合同 PDF 上传（V45） =====================
@app.route("/api/won-projects/<int:pid>/documents", methods=["POST"])
def upload_won_doc(pid):
    if "file" not in request.files:
        return jsonify({"error":"no file"}),400
    f = request.files["file"]
    if not f.filename:
        return jsonify({"error":"empty filename"}),400
    ext = os.path.splitext(f.filename)[1].lower()
    if ext != ".pdf":
        return jsonify({"error":"invalid pdf"}),415
    slot = (request.form.get("slot") or request.args.get("slot") or "").strip()
    if slot not in ("doc_equip", "doc_install", "doc_both"):
        slot = ""
    conn = get_db()
    row = conn.execute("SELECT id, doc_equip, doc_install, doc_both FROM won_projects WHERE id=?", (pid,)).fetchone()
    conn.close()
    if not row:
        return jsonify({"error":"not found"}),404
    base = safe_name(f.filename)
    fname = f"{int(time.time()*1000)}_{base}"
    fpath = os.path.join(UPLOAD_DIR, fname)
    f.save(fpath)
    with open(fpath,"rb") as fh:
        data = fh.read(1024 + 5)
    # ★ 二次校验（与前端/云端同标准）：前 1024 字节内查找 %PDF- 魔数
    if data.find(b"%PDF-", 0, 1024) < 0:
        try:
            os.remove(fpath)
        except Exception:
            pass
        return jsonify({"error":"invalid pdf"}),415
    # 替换上传：删除被替换的旧文件
    if slot:
        _cleanup_replaced_pdf(row[slot], fname)
    return jsonify({"ok":True, "filename": fname, "url": f"/uploads/{fname}"})

@app.route("/api/won-projects/<int:pid>/documents", methods=["DELETE"])
def delete_won_doc(pid):
    data = request.get_json(force=True, silent=True) or {}
    slot = (request.args.get("slot") or request.form.get("slot") or data.get("slot") or "").strip()
    if slot not in ("doc_equip", "doc_install", "doc_both"):
        return jsonify({"error": "invalid slot"}), 400
    conn = get_db()
    row = conn.execute(f"SELECT id, {slot} FROM won_projects WHERE id=?", (pid,)).fetchone()
    if not row:
        conn.close()
        return jsonify({"error": "not found"}), 404
    old_val = row[slot]
    conn.execute(
        f"UPDATE won_projects SET {slot}=?, updated_at=datetime('now','localtime') WHERE id=?",
        ("", pid),
    )
    conn.commit()
    conn.close()
    _rm_upload_file(old_val)
    return jsonify({"ok": True})

# ===================== API：资料库（Document Library） =====================
LIB_ALLOWED_EXT = {
    ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
    ".txt", ".csv", ".md", ".jpg", ".jpeg", ".png", ".gif", ".webp",
    ".zip", ".rar", ".7z", ".dwg", ".dxf"
}
LIB_BLOCKED_EXT = {".exe", ".bat", ".cmd", ".com", ".scr", ".msi", ".sh", ".js", ".vbs", ".ps1", ".jar", ".dll", ".app"}

def _lib_user():
    return (request.headers.get("X-User-Name") or "").strip().lower()

def _lib_can_edit():
    return _lib_user() in TRI_APPROVERS

def _lib_safe_ext(filename):
    ext = os.path.splitext(filename or "")[1].lower()
    if ext in LIB_BLOCKED_EXT:
        return False
    return True

@app.route("/api/library/projects", methods=["GET"])
def library_projects():
    conn = get_db()
    rows = conn.execute(
        "SELECT id, contract_no, customer, province FROM won_projects ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route("/api/library/files", methods=["GET"])
def library_files():
    project_id = request.args.get("project_id")
    conn = get_db()
    if project_id in (None, "", "null"):
        rows = conn.execute(
            "SELECT id, project_id, filename, original_name, uploader, created_at, size FROM library_files WHERE project_id IS NULL ORDER BY created_at DESC"
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT id, project_id, filename, original_name, uploader, created_at, size FROM library_files WHERE project_id=? ORDER BY created_at DESC",
            (int(project_id),),
        ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route("/api/library/upload", methods=["POST"])
def library_upload():
    if not _lib_can_edit():
        return jsonify({"error": "forbidden"}), 403
    files = request.files.getlist("file")
    if not files:
        return jsonify({"error": "no file"}), 400
    project_id = request.args.get("project_id") or request.form.get("project_id") or None
    if project_id in (None, "", "null"):
        project_id = None
    else:
        project_id = int(project_id)
    paths = request.form.getlist("paths") or []
    uploaded = []
    for idx, f in enumerate(files):
        rel = (paths[idx] if idx < len(paths) else "") or ""
        rel = rel.replace("\\", "/").strip()
        display = rel or f.filename
        if not display:
            continue
        if not _lib_safe_ext(display):
            uploaded.append({"ok": False, "error": "blocked", "original_name": display})
            continue
        base = safe_name(display)
        ext = os.path.splitext(base)[1].lower() or ".file"
        fname = f"lib_{int(time.time()*1000)}_{hashlib.md5((base + str(idx)).encode('utf-8')).hexdigest()[:8]}{ext}"
        fpath = os.path.join(LIB_DIR, fname)
        f.save(fpath)
        size = os.path.getsize(fpath) if os.path.isfile(fpath) else 0
        conn = get_db()
        cur = conn.execute(
            "INSERT INTO library_files (project_id, filename, original_name, uploader, size) VALUES (?, ?, ?, ?, ?)",
            (project_id, fname, display, _lib_user(), size),
        )
        fid = cur.lastrowid
        conn.commit()
        conn.close()
        uploaded.append({"ok": True, "id": fid, "filename": fname, "original_name": display, "size": size})
    ok_count = sum(1 for u in uploaded if u.get("ok"))
    return jsonify({"ok": ok_count > 0, "uploaded": uploaded, "count": ok_count})

@app.route("/api/library/files/<int:fid>", methods=["DELETE"])
def library_delete(fid):
    if not _lib_can_edit():
        return jsonify({"error": "forbidden"}), 403
    conn = get_db()
    row = conn.execute("SELECT filename FROM library_files WHERE id=?", (fid,)).fetchone()
    if not row:
        conn.close()
        return jsonify({"error": "not found"}), 404
    conn.execute("DELETE FROM library_files WHERE id=?", (fid,))
    conn.commit()
    conn.close()
    try:
        fp = os.path.join(LIB_DIR, row["filename"])
        if os.path.isfile(fp):
            os.remove(fp)
    except OSError:
        pass
    return jsonify({"ok": True})

@app.route("/api/library/files/<int:fid>/rename", methods=["PUT"])
def library_rename(fid):
    if not _lib_can_edit():
        return jsonify({"error": "forbidden"}), 403
    data = request.get_json(force=True, silent=True) or {}
    new_name = (data.get("original_name") or "").strip()
    if not new_name:
        return jsonify({"error": "empty name"}), 400
    conn = get_db()
    row = conn.execute("SELECT id FROM library_files WHERE id=?", (fid,)).fetchone()
    if not row:
        conn.close()
        return jsonify({"error": "not found"}), 404
    conn.execute("UPDATE library_files SET original_name=? WHERE id=?", (new_name, fid))
    conn.commit()
    conn.close()
    return jsonify({"ok": True})

@app.route("/api/library/files/<int:fid>/download")
def library_download(fid):
    conn = get_db()
    row = conn.execute("SELECT filename, original_name FROM library_files WHERE id=?", (fid,)).fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "not found"}), 404
    as_att = (request.args.get("dl") or "").strip() not in ("", "0", "false")
    dl_name = os.path.basename((row["original_name"] or row["filename"]).replace("\\", "/"))
    return send_from_directory(LIB_DIR, row["filename"], as_attachment=as_att, download_name=dl_name)

@app.route("/api/library/files/<int:fid>/preview")
def library_preview(fid):
    conn = get_db()
    row = conn.execute("SELECT filename, original_name FROM library_files WHERE id=?", (fid,)).fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "not found"}), 404
    ext = os.path.splitext(row["filename"])[1].lower()
    ct = mimetypes.guess_type(row["original_name"])[0] or "application/octet-stream"
    if ext not in (".pdf", ".jpg", ".jpeg", ".png", ".gif", ".webp"):
        return jsonify({"error": "not previewable"}), 415
    return send_from_directory(LIB_DIR, row["filename"], mimetype=ct)

@app.route("/api/library/files/<int:fid>/raw")
def library_raw(fid):
    """原始文件（内联），供前端在线阅览 PDF/Office 等（任意格式，不做类型限制）。"""
    conn = get_db()
    row = conn.execute("SELECT filename, original_name FROM library_files WHERE id=?", (fid,)).fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "not found"}), 404
    ct = mimetypes.guess_type(row["original_name"])[0] or "application/octet-stream"
    resp = send_from_directory(LIB_DIR, row["filename"], mimetype=ct, as_attachment=False,
                               download_name=row["original_name"])
    resp.headers["Cache-Control"] = "private, max-age=600"
    return resp

# ---- 高保真在线预览：用本机 Microsoft Office 把 Word/Excel/PPT 转成 PDF 后内联展示 ----
LIB_OFFICE_EXT = {".doc", ".docx", ".rtf", ".odt", ".txt",
                  ".xls", ".xlsx", ".xlsm", ".csv",
                  ".ppt", ".pptx", ".pptm"}
LIB_PDF_CACHE = os.path.join(LIB_DIR, "_pdfcache")

def _lib_office_to_pdf(src, dst):
    """调用本机 Office（PowerShell COM）把 Office 文档转成 PDF；成功返回 True。"""
    ps = shutil.which("powershell") or shutil.which("pwsh")
    script = os.path.join(BASE_DIR, "office2pdf.ps1")
    if not ps or not os.path.isfile(script):
        return False
    try:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if os.path.isfile(dst):
            try:
                os.remove(dst)
            except OSError:
                pass
        r = subprocess.run(
            [ps, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", script,
             "-In", src, "-Out", dst],
            capture_output=True, timeout=240,
        )
        ok = os.path.isfile(dst) and os.path.getsize(dst) > 0
        if not ok:
            print("[lib-pdf] convert failed rc=%s out=%s err=%s" % (
                r.returncode,
                (r.stdout or b"")[-300:].decode("utf-8", "replace"),
                (r.stderr or b"")[-300:].decode("utf-8", "replace")))
        return ok
    except Exception as e:
        print("[lib-pdf] convert error:", e)
        return False

@app.route("/api/library/files/<int:fid>/pdfview")
def library_pdfview(fid):
    """返回可内联预览的 PDF：原生 PDF 直接给；Word/Excel/PPT 由本机 Office 转 PDF（按 mtime 缓存）。
    ?check=1 时只返回 JSON {"ok":true} 或错误，用于前端先探测是否能高保真预览。"""
    conn = get_db()
    row = conn.execute(
        "SELECT filename, original_name FROM library_files WHERE id=?", (fid,)
    ).fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "not found"}), 404
    fname = row["filename"]
    ext = os.path.splitext(row["original_name"] or fname)[1].lower()
    src = os.path.join(LIB_DIR, fname)
    if not os.path.isfile(src):
        return jsonify({"error": "file missing"}), 404
    check = (request.args.get("check") or "").strip().lower() in ("1", "true", "yes")

    if ext == ".pdf":
        if check:
            return jsonify({"ok": True, "pdf": True})
        resp = send_from_directory(LIB_DIR, fname, mimetype="application/pdf", as_attachment=False)
        resp.headers["Cache-Control"] = "private, max-age=600"
        return resp

    if ext not in LIB_OFFICE_EXT:
        return jsonify({"ok": False, "error": "unsupported"}), 415

    try:
        st = os.stat(src)
        key = hashlib.md5(("%s|%d|%d" % (fname, st.st_size, int(st.st_mtime))).encode("utf-8")).hexdigest()
    except OSError:
        return jsonify({"ok": False, "error": "stat failed"}), 500
    pdf_name = key + ".pdf"
    pdf_path = os.path.join(LIB_PDF_CACHE, pdf_name)
    if not (os.path.isfile(pdf_path) and os.path.getsize(pdf_path) > 0):
        if not _lib_office_to_pdf(src, pdf_path):
            return jsonify({"ok": False, "error": "convert_failed"}), 501
    if check:
        return jsonify({"ok": True, "pdf": True})
    resp = send_from_directory(LIB_PDF_CACHE, pdf_name, mimetype="application/pdf", as_attachment=False)
    resp.headers["Cache-Control"] = "private, max-age=600"
    return resp

# ---- CAD(DWG/DXF) 在线预览：提取 DWG 内嵌的 PNG/BMP 缩略图（无需任何转换器） ----
LIB_CAD_EXT = {".dwg", ".dxf", ".dwf", ".dwfx"}

def _lib_cad_thumbnail(src):
    """从 CAD 文件中提取内嵌缩略图（AutoCAD 保存时写入的预览图）。
    优先 PNG；否则查找合法的 BMP。返回 (bytes, mime) 或 None。"""
    try:
        with open(src, "rb") as fh:
            head = fh.read(3 * 1024 * 1024)
    except OSError:
        return None
    png_sig = b"\x89PNG\r\n\x1a\n"
    pi = head.find(png_sig)
    if pi >= 0:
        end = pi + 8
        n = len(head)
        while end + 8 <= n:
            ln = struct.unpack_from(">I", head, end)[0]
            typ = head[end + 4:end + 8]
            if typ == b"IEND":
                blob = head[pi:end + 12]
                if len(blob) > 100:
                    return blob, "image/png"
                break
            end += 12 + ln
    i = 0
    while True:
        i = head.find(b"BM", i)
        if i < 0:
            break
        try:
            bf = struct.unpack_from("<I", head, i + 2)[0]
            off = struct.unpack_from("<I", head, i + 10)[0]
            hsz = struct.unpack_from("<I", head, i + 14)[0]
            w = struct.unpack_from("<i", head, i + 18)[0]
            h = struct.unpack_from("<i", head, i + 22)[0]
            bits = struct.unpack_from("<H", head, i + 28)[0]
            if (hsz == 40 and 0 < w <= 4096 and 0 < abs(h) <= 4096
                    and bits in (1, 4, 8, 24, 32) and off < 4096
                    and bf and i + bf <= len(head)):
                return head[i:i + bf], "image/bmp"
        except Exception:
            pass
        i += 2
    return None

@app.route("/api/library/files/<int:fid>/cadthumb")
def library_cadthumb(fid):
    """返回 CAD 文件内嵌的预览缩略图（PNG/BMP）。?check=1 只返回 JSON。"""
    conn = get_db()
    row = conn.execute("SELECT filename, original_name FROM library_files WHERE id=?", (fid,)).fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "not found"}), 404
    fname = row["filename"]
    src = os.path.join(LIB_DIR, fname)
    if not os.path.isfile(src):
        return jsonify({"error": "file missing"}), 404
    try:
        st = os.stat(src)
        key = hashlib.md5(("cad|%s|%d|%d" % (fname, st.st_size, int(st.st_mtime))).encode("utf-8")).hexdigest()
    except OSError:
        return jsonify({"ok": False, "error": "stat failed"}), 500
    os.makedirs(LIB_PDF_CACHE, exist_ok=True)
    cached = None
    for cand in (".png", ".bmp"):
        p = os.path.join(LIB_PDF_CACHE, key + cand)
        if os.path.isfile(p) and os.path.getsize(p) > 0:
            cached = key + cand
            break
    if not cached:
        thumb = _lib_cad_thumbnail(src)
        if not thumb:
            return jsonify({"ok": False, "error": "no_thumbnail"}), 404
        data, mime = thumb
        cached = key + (".png" if mime == "image/png" else ".bmp")
        with open(os.path.join(LIB_PDF_CACHE, cached), "wb") as fh:
            fh.write(data)
    if (request.args.get("check") or "").strip().lower() in ("1", "true", "yes"):
        return jsonify({"ok": True})
    resp = send_from_directory(LIB_PDF_CACHE, cached, as_attachment=False)
    resp.headers["Cache-Control"] = "private, max-age=600"
    return resp

# ===================== API：补充协议摘要 =====================
@app.route("/api/won-projects/<int:pid>/supp-summary", methods=["PUT"])
def update_supp_summary(pid):
    data = request.get_json(force=True, silent=True) or {}
    arr = data.get("supp_summary", [])
    if not isinstance(arr, list):
        return jsonify({"error":"supp_summary must be list"}),400
    conn = get_db()
    row = conn.execute("SELECT id FROM won_projects WHERE id=?", (pid,)).fetchone()
    if not row:
        conn.close()
        return jsonify({"error":"not found"}),404
    conn.execute("UPDATE won_projects SET supp_summary=?, updated_at=datetime('now','localtime') WHERE id=?",
                 (json.dumps(arr, ensure_ascii=False), pid))
    new_row = conn.execute("SELECT * FROM won_projects WHERE id=?", (pid,)).fetchone()
    conn.commit()
    conn.close()
    return jsonify(row_to_dict(new_row))

# ===================== 静态首页 =====================


@app.route("/")
def index():
    # 本机模式：把「已上云」的接口改回同源（本机），
    # 这样通过 http://localhost:5050 访问时，登录/会话/业务数据全部走本机后端 + 本机数据库，
    # 不受云端维护锁（LOGIN_ONLY_USERS）限制 —— 用于本地测试时释放全部用户。
    # 注意：只影响本机返回的这一份页面副本，磁盘上的 index.html 与线上 WEB 完全不变。
    try:
        src = os.path.join(BASE_DIR, "index.html")
        # 每次直接读盘并做 CLOUD_ONLY 替换，不依赖 mtime 内存缓存
        # （Windows 上同一秒内多次保存 st_mtime 不变，会导致缓存不刷新、
        #  前端一直看到旧版 HTML，表现为"改了代码却没效果"）。
        with io.open(src, encoding="utf-8") as f:
            html = f.read()
        # 把 var CLOUD_ONLY = [ ... ]; 整段替换为空数组
        html = re.sub(r"var CLOUD_ONLY\s*=\s*\[[\s\S]*?\];",
                      "var CLOUD_ONLY = [];  /* 本机模式：全部接口走 localhost */",
                      html, count=1)
        return Response(html, mimetype="text/html")
    except Exception:
        # 兜底：任何异常都退回原文件，保证页面一定能打开
        return send_from_directory(BASE_DIR, "index.html")

# ===== 精简版前端：仅 登录页 + 看板 + 签约项目（choice_lite.html） =====


@app.route("/lite")
def index_lite():
    """精简版页面：页签只保留「看板 / 签约项目」，表格样式与主站一致。
    与 index() 同机制：本机模式下把 CLOUD_ONLY 置空，所有接口走 localhost。

    缓存令牌：以 choice_lite.html 内容 MD5 作为版本号，URL 自动带 ?v=<hash>。
    文件内容一变 → hash 变 → URL 变 → 浏览器必然重新拉取并执行最新脚本，
    彻底避免「改了代码却看到旧版 / 旧 DOM」（含 bfcache 恢复旧页面的情况）。"""
    src = os.path.join(BASE_DIR, "choice_lite.html")
    try:
        with io.open(src, "rb") as fb:
            raw = fb.read()
        hv = hashlib.md5(raw).hexdigest()[:12]
        if request.args.get("v") != hv:
            r = redirect("/lite?v=" + hv)
            r.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
            r.headers["Pragma"] = "no-cache"
            return r
        html = raw.decode("utf-8")
        # 每次直接读盘并做 CLOUD_ONLY 替换，不依赖 mtime 内存缓存
        # （Windows 上同一秒内多次保存 st_mtime 不变，会导致缓存不刷新、
        #  前端一直看到旧版 HTML，表现为"改了代码却没效果"）。
        html = re.sub(r"var CLOUD_ONLY\s*=\s*\[[\s\S]*?\];",
                      "var CLOUD_ONLY = [];  /* 本机模式：全部接口走 localhost */",
                      html, count=1)
        return Response(html, mimetype="text/html",
                        headers={"Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
                                 "Pragma": "no-cache", "Expires": "0"})
    except Exception:
        return send_from_directory(BASE_DIR, "choice_lite.html")

@app.route("/crm_table.js")
def serve_crm_table():
    return send_from_directory(BASE_DIR, "crm_table.js", mimetype="application/javascript")

@app.route("/vault.html")
def serve_vault():
    return send_from_directory(BASE_DIR, "vault.html", mimetype="text/html")

@app.route("/lost_table.js")
def serve_lost_table():
    return send_from_directory(BASE_DIR, "lost_table.js", mimetype="application/javascript")

@app.route("/flow_svg/<fn>")
def serve_flow_svg(fn):
    import werkzeug.utils as _wu
    fn = _wu.secure_filename(fn)
    if not fn.endswith((".svg", ".webp", ".png")):
        return ("", 404)
    _ct = "image/svg+xml" if fn.endswith(".svg") else ("image/webp" if fn.endswith(".webp") else "image/png")
    return send_from_directory(os.path.join(BASE_DIR, "flow_svg"), fn, mimetype=_ct)

@app.route("/vn_provinces.js")
def serve_vn_provinces():
    return send_from_directory(BASE_DIR, "vn_provinces.js", mimetype="application/javascript")

# ===== PWA / 手机 APP 静态资源 =====
@app.route("/manifest.json")
def serve_manifest():
    return send_from_directory(BASE_DIR, "manifest.json",
                               mimetype="application/manifest+json")


@app.route("/icon-192.png")
def serve_icon_192():
    return send_from_directory(BASE_DIR, "icon-192.png", mimetype="image/png")


@app.route("/favicon.svg")
def serve_favicon_svg():
    return send_from_directory(BASE_DIR, "favicon.svg", mimetype="image/svg+xml")


@app.route("/icon-512.png")
def serve_icon_512():
    return send_from_directory(BASE_DIR, "icon-512.png", mimetype="image/png")


@app.route("/icon-512-maskable.png")
def serve_icon_maskable():
    return send_from_directory(BASE_DIR, "icon-512-maskable.png", mimetype="image/png")


# ===================== API：私密空间（Vault，tom 专属） =====================
def _vault_now():
    return time.time()

def _vault_check_lock():
    """返回 (locked, remain) ；locked=True 时 remain 为剩余锁定秒数。"""
    if _vault_fail["lock_until"] > _vault_now():
        return True, int(_vault_fail["lock_until"] - _vault_now())
    return False, 0

def _vault_owner_ok(req_user):
    """请求方是否为私密空间主人 tom（区分大小写归一）。"""
    return (req_user or "").strip().lower() == VAULT_OWNER

def _vault_auth_token():
    """从 header 或查询参数取出 token，校验有效性，返回 (ok, reason)。
    查询参数 ?vt= 兼容浏览器直接导航（<a>/<img> 带不了自定义头）。"""
    tok = (request.headers.get("X-Vault-Token") or request.args.get("vt") or "").strip()
    if not tok:
        return False, "missing token"
    exp = _vault_tokens.get(tok)
    if not exp:
        return False, "invalid token"
    if exp < _vault_now():
        _vault_tokens.pop(tok, None)
        return False, "expired token"
    return True, ""


def _vault_sanitize_rel(p):
    """清洗相对路径：逐段过滤 .. 与非法字符，返回 'a/b/c.ext' 形式（无首尾斜杠）。"""
    segs = []
    for s in re.split(r"[\\/]+", str(p or "")):
        s = re.sub(r'[\\/:*?"<>|]', "_", s)
        s = re.sub(r"\s+", "_", s).strip()
        if not s or s in (".", ".."):
            continue
        segs.append(s[:120])
    return "/".join(segs[:12])


def _vault_resolve_name(captured=""):
    """解析文件名：优先 ?n= 查询参数（完整相对路径），退化取 URL 路径捕获；拒绝 .. 穿越。"""
    name = (request.args.get("n") or captured or "").strip().lstrip("/")
    if not name or re.search(r"(^|/)\.\.(/|$)", name):
        return None
    return name


def _vault_unique_path(dirpath, filename):
    """重名自动加 (n)，与云端行为一致。"""
    base, ext = os.path.splitext(filename)
    cand = filename
    i = 1
    while os.path.exists(os.path.join(dirpath, cand)):
        cand = "%s (%d)%s" % (base, i, ext)
        i += 1
        if i > 99:
            cand = "%s (%d)%s" % (base, int(time.time()), ext)
            break
    return cand

import secrets as _secrets

@app.route("/api/vault/unlock", methods=["POST"])
def vault_unlock():
    """校验 PIN，成功后签发有时效的 token。仅 tom 可调用。"""
    data = request.get_json(force=True, silent=True) or {}
    req_user = (data.get("username") or "").strip()
    pin = (data.get("pin") or "").strip()
    locked, remain = _vault_check_lock()
    if locked:
        return jsonify({"ok": False, "error": "尝试过多，请 %d 秒后再试" % remain, "lock": remain}), 429
    if not _vault_owner_ok(req_user):
        return jsonify({"ok": False, "error": "无权限访问该空间"}), 403
    if pin != VAULT_PIN:
        _vault_fail["count"] += 1
        if _vault_fail["count"] >= VAULT_MAX_FAIL:
            _vault_fail["lock_until"] = _vault_now() + VAULT_LOCK_SECONDS
            _vault_fail["count"] = 0
            return jsonify({"ok": False, "error": "错误次数过多，已锁定 %d 秒" % VAULT_LOCK_SECONDS, "lock": VAULT_LOCK_SECONDS}), 429
        return jsonify({"ok": False, "error": "密码错误", "fail": _vault_fail["count"]}), 401
    # 成功：签发 token
    _vault_fail["count"] = 0
    tok = _secrets.token_hex(VAULT_TOKEN_BYTES)
    _vault_tokens[tok] = _vault_now() + VAULT_TOKEN_TTL
    return jsonify({"ok": True, "token": tok, "ttl": VAULT_TOKEN_TTL})

@app.route("/api/vault/files", methods=["GET"])
def vault_list():
    ok, reason = _vault_auth_token()
    if not ok:
        return jsonify({"ok": False, "error": reason}), 401
    items = []
    try:
        # 递归遍历：name 返回相对路径（含文件夹），前端渲染目录树
        for root, _dirs, files in os.walk(VAULT_DIR):
            for fn in files:
                fp = os.path.join(root, fn)
                rel = os.path.relpath(fp, VAULT_DIR).replace("\\", "/")
                st = os.stat(fp)
                items.append({
                    "name": rel,
                    "size": st.st_size,
                    "mtime": time.strftime("%Y-%m-%d %H:%M", time.localtime(st.st_mtime)),
                })
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500
    items.sort(key=lambda x: x["name"])
    return jsonify({"ok": True, "files": items})

@app.route("/api/vault/upload", methods=["POST"])
def vault_upload():
    ok, reason = _vault_auth_token()
    if not ok:
        return jsonify({"ok": False, "error": reason}), 401
    if "file" not in request.files:
        return jsonify({"ok": False, "error": "no file"}), 400
    f = request.files["file"]
    if not f.filename:
        return jsonify({"ok": False, "error": "empty filename"}), 400
    ext = os.path.splitext(f.filename)[1].lower()
    # 私密空间：仅拦截真正危险的可执行文件，其余任意类型均可上传
    if ext in VAULT_BLOCKED_EXT:
        return jsonify({"ok": False, "error": "不允许上传可执行文件：%s" % ext}), 400
    # 文件夹结构：path 字段为相对路径（a/b/c.ext），缺失时退化用文件名
    rel = _vault_sanitize_rel(request.form.get("path") or f.filename)
    if not rel:
        return jsonify({"ok": False, "error": "invalid path"}), 400
    parts = rel.split("/")
    dirpath = os.path.join(VAULT_DIR, *parts[:-1]) if len(parts) > 1 else VAULT_DIR
    os.makedirs(dirpath, exist_ok=True)
    fname = _vault_unique_path(dirpath, parts[-1])
    fpath = os.path.join(dirpath, fname)
    f.save(fpath)
    if ext == ".pdf":
        with open(fpath, "rb") as fh:
            head = fh.read(5)
        if head != b"%PDF-":
            os.remove(fpath)
            return jsonify({"ok": False, "error": "invalid pdf"}), 400
    rel_name = os.path.relpath(fpath, VAULT_DIR).replace("\\", "/")
    return jsonify({"ok": True, "name": rel_name, "original": f.filename})

@app.route("/api/vault/download/<path:name>", methods=["GET"])
def vault_download(name):
    ok, reason = _vault_auth_token()
    if not ok:
        return jsonify({"ok": False, "error": reason}), 401
    name = _vault_resolve_name(name)
    if not name:
        return jsonify({"ok": False, "error": "文件不存在"}), 404
    fp = os.path.join(VAULT_DIR, *name.split("/"))
    if not os.path.isfile(fp):
        return jsonify({"ok": False, "error": "文件不存在"}), 404
    return send_from_directory(VAULT_DIR, name, as_attachment=True)

@app.route("/api/vault/preview/<path:name>", methods=["GET"])
def vault_preview(name):
    ok, reason = _vault_auth_token()
    if not ok:
        return jsonify({"ok": False, "error": reason}), 401
    name = _vault_resolve_name(name)
    if not name:
        return jsonify({"ok": False, "error": "文件不存在"}), 404
    fp = os.path.join(VAULT_DIR, *name.split("/"))
    if not os.path.isfile(fp):
        return jsonify({"ok": False, "error": "文件不存在"}), 404
    return send_from_directory(VAULT_DIR, name)

@app.route("/api/vault/delete/<path:name>", methods=["DELETE"])
def vault_delete(name):
    ok, reason = _vault_auth_token()
    if not ok:
        return jsonify({"ok": False, "error": reason}), 401
    name = _vault_resolve_name(name)
    if not name:
        return jsonify({"ok": False, "error": "文件不存在"}), 404
    fp = os.path.join(VAULT_DIR, *name.split("/"))
    if not os.path.isfile(fp):
        return jsonify({"ok": False, "error": "文件不存在"}), 404
    os.remove(fp)
    _vault_cleanup_dirs(os.path.dirname(fp))
    return jsonify({"ok": True})


def _vault_cleanup_dirs(dirpath):
    """删除文件后顺手清掉空目录（根目录除外）。"""
    try:
        while os.path.abspath(dirpath) != os.path.abspath(VAULT_DIR):
            if os.path.isdir(dirpath) and not os.listdir(dirpath):
                os.rmdir(dirpath)
                dirpath = os.path.dirname(dirpath)
            else:
                break
    except Exception:
        pass

@app.route("/api/vault/delete", methods=["POST"])
def vault_delete_batch():
    """批量删除：body = {"names": [filename, ...]}"""
    ok, reason = _vault_auth_token()
    if not ok:
        return jsonify({"ok": False, "error": reason}), 401
    data = request.get_json(force=True, silent=True) or {}
    names = data.get("names") or []
    if not isinstance(names, list) or not names:
        return jsonify({"ok": False, "error": "没有选择文件"}), 400
    deleted, missing, blocked = [], [], []
    for n in names:
        n = str(n).strip().lstrip("/")
        if not n or re.search(r"(^|/)\.\.(/|$)", n):
            blocked.append(n); continue
        fp = os.path.join(VAULT_DIR, *n.split("/"))
        if not os.path.isfile(fp):
            missing.append(n); continue
        try:
            os.remove(fp)
            _vault_cleanup_dirs(os.path.dirname(fp))
            deleted.append(n)
        except Exception:
            missing.append(n)
    return jsonify({"ok": True, "deleted": deleted, "missing": missing, "blocked": blocked})


@app.route("/health")
def health():
    return jsonify({"ok": True, "db": DB_PATH, "upload_dir": UPLOAD_DIR})


# ===================== API：系统清理（仅 tom） =====================
# 与云端 /api/admin/purge-* 对称，用于清掉删记录后残留的孤儿文件。
@app.route("/api/admin/purge-report")
def admin_purge_report():
    """只读报告：磁盘文件总数、孤儿文件数与样例。"""
    if (request.headers.get("X-User-Name") or "").strip().lower() != "tom":
        return jsonify({"error": "forbidden: owner only"}), 403
    conn = get_db()
    refs = _collect_referenced_files(conn)
    conn.close()
    files, orphans = [], []
    for root, _dirs, names in os.walk(UPLOAD_DIR):
        for n in names:
            rel = os.path.relpath(os.path.join(root, n), UPLOAD_DIR).replace("\\", "/")
            files.append(rel)
            if not rel.startswith("vault/") and rel not in refs:
                orphans.append(rel)
    return jsonify({"ok": True, "report": {
        "upload_total": len(files),
        "upload_orphans": len(orphans),
        "orphan_sample": orphans[:30],
        "referenced_files": len(refs),
    }})


@app.route("/api/admin/purge-orphans", methods=["POST", "GET"])
def admin_purge_orphans():
    """清理 uploads/ 下没有任何数据库记录引用的孤儿文件（vault/ 不在此列）。"""
    if (request.headers.get("X-User-Name") or "").strip().lower() != "tom":
        return jsonify({"error": "forbidden: owner only"}), 403
    data = request.get_json(force=True, silent=True) or {}
    dry = bool(data.get("dryRun"))
    conn = get_db()
    refs = _collect_referenced_files(conn)
    conn.close()
    deleted, orphans = 0, []
    for root, _dirs, names in os.walk(UPLOAD_DIR):
        for n in names:
            rel = os.path.relpath(os.path.join(root, n), UPLOAD_DIR).replace("\\", "/")
            if rel.startswith("vault/") or rel in refs:
                continue
            orphans.append(rel)
            if not dry:
                try:
                    os.remove(os.path.join(UPLOAD_DIR, rel))
                    deleted += 1
                except OSError:
                    pass
    return jsonify({"ok": True, "result": {
        "orphan_found": len(orphans), "deleted": 0 if dry else deleted,
        "dryRun": dry, "sample": orphans[:50],
    }})


@app.route("/api/admin/storage-report")
def admin_storage_report():
    """本地 uploads/ 容量分布（与云端 /api/admin/storage-report 对称），离线桌面版也显示饼图。仅 tom 可用。"""
    if (request.headers.get("X-User-Name") or "").strip().lower() != "tom":
        return jsonify({"error": "forbidden: owner only"}), 403
    conn = get_db()
    # 按表收集被引用的文件名（用于把 uploads 文件归类到 won/crm/lost）
    refs = {"won": set(), "crm": set(), "lost": set()}
    try:
        rows = conn.execute("SELECT pdf_equip, pdf_install, pdf_both FROM crm_projects").fetchall()
        for r in rows:
            refs["crm"].update(_row_file_refs("crm_projects", r))
    except Exception:
        pass
    try:
        rows = conn.execute("SELECT pdf_equip, pdf_install, pdf_both FROM lost_projects").fetchall()
        for r in rows:
            refs["lost"].update(_row_file_refs("lost_projects", r))
    except Exception:
        pass
    try:
        rows = conn.execute("SELECT attachments FROM won_projects").fetchall()
        for r in rows:
            refs["won"].update(_row_file_refs("won_projects", r))
    except Exception:
        pass
    conn.close()

    areas = {k: 0 for k in ("won", "crm", "lost", "vault", "snapshots", "other")}
    for root, _dirs, names in os.walk(UPLOAD_DIR):
        for n in names:
            full = os.path.join(root, n)
            try:
                sz = os.path.getsize(full)
            except OSError:
                continue
            rel = os.path.relpath(full, UPLOAD_DIR).replace("\\", "/")
            if rel.startswith("vault/"):
                cat = "vault"
            elif n in refs["won"]:
                cat = "won"
            elif n in refs["crm"]:
                cat = "crm"
            elif n in refs["lost"]:
                cat = "lost"
            else:
                cat = "other"
            areas[cat] += sz
    # 数据快照（本地在 DATA_DIR）
    for snap in ("demo_snapshot.json", "price_snapshot.json"):
        try:
            p = os.path.join(DATA_DIR, snap)
            if os.path.isfile(p):
                areas["snapshots"] += os.path.getsize(p)
        except Exception:
            pass

    used = sum(areas.values())
    # 容量对齐云端 shape：用磁盘总空间 / 剩余空间（饼图除以 capacity_bytes）
    try:
        du = shutil.disk_usage(UPLOAD_DIR)
        capacity = du.total
        free = du.free
    except Exception:
        capacity = used or 1
        free = 0
    area_meta = {"won": "WON", "crm": "CRM", "lost": "LOST",
                 "vault": "Vault", "snapshots": "Snapshots", "other": "Other"}
    area_arr = [{"key": k, "name": area_meta[k], "bytes": areas[k],
                 "percent": (areas[k] / capacity * 100) if capacity else 0.0}
                for k in ("won", "crm", "lost", "vault", "snapshots", "other")
                if areas[k] > 0]
    area_arr.sort(key=lambda a: a["bytes"], reverse=True)
    return jsonify({"ok": True, "storage": {
        "capacity_bytes": capacity,
        "capacity_gb": round(capacity / 1e9, 2),
        "used_bytes": used,
        "used_gb": round(used / 1e9, 2),
        "used_percent": round(used / capacity * 100, 2) if capacity else 0.0,
        "free_bytes": free,
        "free_gb": round(free / 1e9, 2),
        "free_percent": round(free / capacity * 100, 2) if capacity else 0.0,
        "areas": area_arr,
    }})

# ===================== API：用户与授权（CRUD + 权限） =====================
DEFAULT_INIT_PASSWORD = "66668888"  # 新用户默认初始密码


def _row_to_user(row, manager_set=None):
    """将数据库行转换为前端需要的用户对象。"""
    import json as _json
    def rv(k, default=""):
        try:
            v = row[k]
            return v if v is not None else default
        except (IndexError, KeyError):
            return default
    try:
        vis_can_see_me = _json.loads(rv("vis_can_see_me", "[]")) if rv("vis_can_see_me") else []
    except Exception:
        vis_can_see_me = []
    try:
        vis_he_can_see = _json.loads(rv("vis_he_can_see", "[]")) if rv("vis_he_can_see") else []
    except Exception:
        vis_he_can_see = []
    try:
        perms = _json.loads(rv("perms", "{}")) if rv("perms") else {}
    except Exception:
        perms = {}
    try:
        forgot_approvers = _json.loads(rv("forgot_approvers", "[]")) if rv("forgot_approvers") else []
    except Exception:
        forgot_approvers = []
    username = rv("username")
    return {
        "id": rv("id"),
        "username": username,
        "real_name": rv("real_name"),
        "role": rv("role"),
        "position": rv("position"),
        "status": rv("status") or "active",
        "is_admin": (username in manager_set) if manager_set is not None else False,
        "vis_can_see_me": vis_can_see_me,
        "vis_he_can_see": vis_he_can_see,
        "perms": perms,
        "delegate_to": rv("delegate_to"),
        "forgot_approvers": forgot_approvers if isinstance(forgot_approvers, list) else [],
    }


# ===================== API：灌入各角色测试用户（用于测试） =====================
SEED_USERS = [
    # 销售（多个，作为 WON/LOST/CRM 销售人员下拉的主要来源）
    ("tom",    "Tom",    "销售",      False),
    ("cuong",  "Cuong",  "销售",      False),
    ("james",  "James",  "销售",      False),
    ("travis", "Travis", "销售",      False),
    ("ali",    "Ali",    "销售",      False),
    ("khoa",   "Khoa",   "销售",      False),
    ("minh",   "Minh",   "销售",      False),
    ("linh",   "Linh",   "销售",      False),
    # 销售总监
    ("salesdir1", "Henry",  "销售总监", False),
    ("salesdir2", "Wendy",  "销售总监", False),
    # 总经理
    ("gm1", "George", "总经理", True),
    ("gm2", "Grace",  "总经理", True),
    # 副总经理
    ("dgm1", "David", "副总经理", False),
    ("dgm2", "Diana", "副总经理", False),
    # 观察者
    ("obs1", "Olivia", "观察者", False),
    ("obs2", "Oscar",  "观察者", False),
    # 财务经理
    ("fin1", "Fiona", "财务经理", False),
    ("fin2", "Felix", "财务经理", False),
    # 总经理助理
    ("asst1", "Amy", "总经理助理", False),
    # 人事经理
    ("hr1", "Hannah", "人事经理", False),
]

@app.route("/api/seed-users", methods=["GET", "POST"])
def api_seed_users():
    """灌入各角色测试用户（upsert：username 已存在则跳过）。"""
    conn = get_db()
    inserted = 0
    for username, real_name, position, is_admin in SEED_USERS:
        exists = conn.execute("SELECT id FROM users WHERE username=?", (username,)).fetchone()
        if exists:
            continue
        pw_hash = DEFAULT_INIT_PASSWORD
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn.execute(
            """INSERT INTO users
               (username, password, real_name, role, position, status,
                vis_can_see_me, vis_he_can_see, perms, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (username, pw_hash, real_name,
             "admin" if is_admin else "user", position, "active",
             json.dumps([username], ensure_ascii=False),
             json.dumps([username], ensure_ascii=False),
             json.dumps({}, ensure_ascii=False),
             now)
        )
        # 种子数据里 is_admin=True 的旧标记同步迁移到 managers 表
        if is_admin:
            conn.execute("INSERT OR IGNORE INTO managers (username) VALUES (?)", (username,))
        inserted += 1
    # 保证 tom 始终为管理员
    conn.execute("INSERT OR IGNORE INTO managers (username) VALUES (?)", ("tom",))
    conn.commit()
    conn.close()
    return jsonify({"ok": True, "inserted": inserted, "total_defined": len(SEED_USERS)})


# ===== 审批请求 API（“发起审批”类型的真实拦截） =====
@app.route("/api/approval-requests", methods=["POST"])
def api_approval_create():
    data = request.get_json(force=True, silent=True) or {}
    requester = (data.get("requester") or "").strip()
    if not requester:
        return jsonify({"ok": False, "msg": "未登录"}), 401
    block_id = data.get("block_id") or ""
    block_name = data.get("block_name") or block_id
    # 审批标题 = 区块名称；审批内容 = 前端传来的权限说明文字（"默认保留信息"列）
    title = data.get("title") or block_name
    content = data.get("content") or ""
    approvers = data.get("approvers") or []
    conn = get_db()
    # ===== 审批人以数据库真源为准（核心修复）=====
    # 发起人浏览器里的权限快照可能已过期（管理员刚改完配置、发起人尚未刷新）。
    # 优先级：① 数据库中发起人当前配置的审批人 ② 前端提交的名单 ③ tom+管理员兜底。
    # 这样保证"当前配置的审批人"一定收到请求，业务流程永远不会因配置读取问题而中断。
    db_approvers = []
    try:
        _row = conn.execute("SELECT perms FROM users WHERE username=?", (requester,)).fetchone()
        if _row and _row["perms"]:
            _p = json.loads(_row["perms"])
            db_approvers = [str(a).strip() for a in ((_p.get(block_id) or {}).get("approvers") or []) if str(a).strip()]
    except Exception:
        db_approvers = []
    if db_approvers:
        approvers = db_approvers

    def _mgr_fallback():
        fb = ["tom"]
        try:
            for m in conn.execute("SELECT username FROM managers"):
                if m["username"] not in fb:
                    fb.append(m["username"])
        except Exception:
            pass
        return fb

    if not approvers:
        approvers = _mgr_fallback()
    # 单次生效审批按 target_id 区分同一区块不同操作对象；持续生效审批仍按区块去重
    persist = (data.get("persist") or "persistent").strip().lower()
    if persist not in ("persistent", "single-use"):
        persist = "persistent"
    target_id = (data.get("target_id") or "").strip()
    dup_sql = (
        "SELECT 1 FROM approval_requests WHERE requester=? AND block_id=? AND status='pending' AND persist=?"
        + (" AND target_id=?"
           if (persist == "single-use" or block_id == "PROD-RECEIPT")
           else "")
    )
    dup_params = (requester, block_id, persist)
    if persist == "single-use" or block_id == "PROD-RECEIPT":
        dup_params += (target_id,)
    dup = conn.execute(dup_sql, dup_params).fetchone()
    if dup:
        conn.close()
        return jsonify({"ok": False, "msg": "该操作已存在待审批请求"}), 409
    # 用户与权限管理审批（USR-L1/D1/D2/D3）：审批人锁死为固定三人组，任一人审批即结束；
    # payload 保存暂存数据（新增用户资料 / 权限变更前后对比 / 删除目标），通过后由服务端执行
    if block_id in ("USR-L1", "USR-D1", "USR-D2", "USR-D3"):
        approvers = list(TRI_APPROVERS)
    # 规范化审批人：兼容前端旧 bug 中存的数字 ID（保留停用/离职用户，以便其代理人能代为审批）
    approvers = _norm_approver_list(approvers, conn)
    # 过滤不存在的用户名（如配置残留的已删除账号），剩余为空则兜底 tom+管理员，
    # 保证业务审批请求永远能创建成功（宁可兜底送达，也不让发起人流程中断）
    existing_users = {r["username"] for r in conn.execute("SELECT username FROM users").fetchall()}
    approvers = [a for a in approvers if a in existing_users]
    if not approvers:
        approvers = _mgr_fallback()
        approvers = [a for a in approvers if a in existing_users]
    if not approvers:
        conn.close()
        return jsonify({"ok": False, "msg": "系统中没有可用的审批人（tom 不存在？）"}), 400
    # 全局规则：tom/cuong/james 对任何审批请求都具备审批权（含收货单 PROD-RECEIPT 等全部区块）；
    # 三人任一人点击通过/驳回即结束该申请（先到先得，效率同等）
    try:
        for _a in TRI_APPROVERS:
            if _a in existing_users and _a not in approvers:
                approvers.append(_a)
    except Exception:
        pass
    conn.execute("""INSERT INTO approval_requests
        (title, requester, requester_name, block_id, block_name, action_name, approvers, status, created_at, content, persist, target_id, payload)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
        title,
        requester,
        data.get("requester_name") or "",
        block_id,
        block_name,
        data.get("action_name") or "",
        json.dumps(approvers, ensure_ascii=False),
        "pending",
        time.strftime("%Y-%m-%d %H:%M:%S"),
        content,
        persist,
        target_id,
        data.get("payload") or ""
    ))
    conn.commit(); conn.close()
    return jsonify({"ok": True})


@app.route("/api/approval-requests", methods=["GET"])
def api_approval_list():
    # 支持按 ?scope=mine(我发起的) / ?scope=todo(待我审批) / ?scope=all(全部)
    scope = request.args.get("scope", "all")
    me = (request.args.get("me") or "").strip()
    conn = get_db()
    rows = conn.execute("SELECT * FROM approval_requests ORDER BY id DESC").fetchall()
    items = []
    for r in rows:
        x = row_to_dict(r)
        # 把审批人字段规范化用户名（兼容旧数字 ID 数据）
        try:
            arr = json.loads(x["approvers"]) if x["approvers"] else []
        except Exception:
            arr = []
        x["approvers"] = _norm_approver_list(arr, conn)
        items.append(x)
    conn.close()
    if scope == "mine":
        items = [x for x in items if x["requester"] == me]
    elif scope == "todo":
        # 待我审批：含直接指派给我，以及离职代理（我是某离职审批人的 delegate_to）的待办
        delegated_users = set()
        if me:
            try:
                conn2 = get_db()
                du = conn2.execute(
                    "SELECT username FROM users WHERE delegate_to=? AND status<>'active' AND username<>?",
                    (me, me)
                ).fetchall()
                delegated_users = {str(d["username"]) for d in du}
                conn2.close()
            except Exception:
                pass
        items = [x for x in items
                 if x["status"] == "pending"
                 and (me in x["approvers"]
                      or bool(delegated_users & set(x["approvers"])))]
    return jsonify({"ok": True, "items": items})


@app.route("/api/prod-factory/<pid>", methods=["GET"])
def api_prod_factory_get(pid):
    me = (request.args.get("me") or "").strip()
    if not me:
        return jsonify({"ok": False, "msg": "未登录"}), 401
    conn = get_db()
    row = conn.execute("SELECT data FROM prod_factory WHERE project_id=?", (str(pid),)).fetchone()
    conn.close()
    if row and row["data"]:
        try:
            return jsonify({"ok": True, "data": json.loads(row["data"])})
        except Exception:
            return jsonify({"ok": True, "data": None})
    return jsonify({"ok": True, "data": None})


def _prod_factory_weight(f):
    if not isinstance(f, dict): return 0
    w = 0
    try:
        ho = f.get('houseOut') or {}
        for rec in ho.values():
            if isinstance(rec, dict):
                od = rec.get('outDaily') or {}
                w += len(od)
        inst = f.get('installation') or {}
        ws = inst.get('workers') or {}
        for dw in ws.values():
            if not isinstance(dw, dict): continue
            if dw.get('_deleted'): continue
            zt = dw.get('zoneTeamWorkers') or {}
            for teams in zt.values():
                if not isinstance(teams, list): continue
                for t in teams:
                    if not isinstance(t, dict): continue
                    ti = t.get('todayInstall') or {}
                    w += len(ti)
                    if t.get('house'): w += 1
        if isinstance(f.get('plan'), list): w += len(f['plan'])
        if isinstance(f.get('workers'), dict): w += len(f['workers'])
        prof = f.get('profile')
        if isinstance(prof, dict) and prof: w += 1
        ip = f.get('inventoryPlan')
        if isinstance(ip, dict) and ip: w += 1
        if f.get('planStart'): w += 1
        if f.get('prepStart'): w += 1
        if f.get('priorityHouse'): w += 1
        prod = f.get('production')
        if isinstance(prod, dict): w += len(prod)
        m = f.get('materials') or {}
        for k in ['items','inbound','outbound','receipts']:
            if isinstance(m.get(k), list): w += len(m[k])
        eq = f.get('equipment')
        if isinstance(eq, dict):
            if isinstance(eq.get('list'), list): w += len(eq['list'])
            if isinstance(eq.get('faults'), list): w += len(eq['faults'])
        if isinstance(f.get('delivery'), list): w += len(f['delivery'])
        w += len(f.get('finished') or {})
    except Exception:
        pass
    return w

def _prod_factory_counts(f):
    """返回核心业务条目数：出库日明细总数、安装天数、安装记录行数、每日生产天数、人员快照天数。
       用于识别"信息量不少但关键业务数据缺失"的旧快照覆盖。

       ★ 每日生产 production / 人员快照 workers 此前不在统计里：只要客户端快照带够安装/出库数据，
       即使它的 production 少了好几天（旧快照），服务端也会照单全收 → 用户新录入的产出被整体覆盖丢失。
       这里把这两项纳入统计，供 PUT 回退闸识别。"""
    out_daily = 0
    install_days = 0
    install_rows = 0
    prod_days = 0
    worker_days = 0
    if not isinstance(f, dict):
        return (out_daily, install_days, install_rows, prod_days, worker_days)
    try:
        ho = f.get('houseOut') or {}
        for rec in ho.values():
            if isinstance(rec, dict):
                out_daily += len(rec.get('outDaily') or {})
        inst = f.get('installation') or {}
        ws = inst.get('workers') or {}
        install_days = 0
        for dw in ws.values():
            if not isinstance(dw, dict):
                continue
            if dw.get('_deleted'):
                continue
            install_days += 1
            zt = dw.get('zoneTeamWorkers') or {}
            for teams in zt.values():
                if not isinstance(teams, list):
                    continue
                for t in teams:
                    if not isinstance(t, dict):
                        continue
                    install_rows += len(t.get('todayInstall') or {})
        # 每日生产：按日期计数（只统计真正有内容的记录）
        pr = f.get('production')
        if isinstance(pr, dict):
            for rec in pr.values():
                if isinstance(rec, dict):
                    prod_days += 1
        wk = f.get('workers')
        if isinstance(wk, dict):
            worker_days = len(wk)
    except Exception:
        pass
    return (out_daily, install_days, install_rows, prod_days, worker_days)


def _merge_date_map(base, other):
    """按日期键做并集合并：base 优先，other 独有的日期补回来（两端都不丢）。"""
    res = copy.deepcopy(base) if isinstance(base, dict) else {}
    if isinstance(other, dict):
        for k, v in other.items():
            if k not in res or res.get(k) is None:
                res[k] = copy.deepcopy(v)
    return res


def _merge_factory_keep_install(payload, existing):
    """回退闸合并：以服务器现有完整数据(existing)为基底，保留用户本次的安装编辑(installation)，
    其余字段(出库/物料/设备等)一律采用服务器更完整的版本，从而避免“本地旧快照覆盖服务器新数据”，
    同时保证用户的安装编辑能够落库。

    ★ 每日生产 production / 人员快照 workers 同样按日期做并集：以服务器为基底，
    把客户端独有的日期补上，避免用户刚录入的产出被服务器旧快照冲掉。"""
    out = copy.deepcopy(existing)
    pinst = payload.get("installation") if isinstance(payload.get("installation"), dict) else {}
    oinst = existing.get("installation") if isinstance(existing.get("installation"), dict) else {}
    merged_inst = dict(oinst)        # 服务器安装数据为基底
    merged_inst.update(pinst)        # 用户本次编辑/新增的安装日期优先
    out["installation"] = merged_inst
    for key in ("production", "workers"):
        try:
            # 客户端本次编辑优先（与 installation 的处理保持一致），服务器独有的日期补回来
            merged_map = _merge_date_map(payload.get(key), existing.get(key))
            # 删除墓碑：任一端标记为删除的日期不再复活
            tomb = {}
            for side in (existing, payload):
                t = side.get(key + "Deleted") if isinstance(side, dict) else None
                if isinstance(t, dict):
                    for dk, dv in t.items():
                        if dv:
                            tomb[dk] = 1
            for dk in tomb:
                merged_map.pop(dk, None)
            if tomb:
                out[key + "Deleted"] = tomb
            if merged_map or existing.get(key) or payload.get(key):
                out[key] = merged_map
        except Exception:
            pass
    return out


def _normalize_out_daily(payload):
    """把旧版整数 outDaily 升级成对象格式，并尽量从 payload.installation 补填表人/天气/区域/猪舍号，
       防止旧页面把已补齐的字段又冲掉。"""
    if not isinstance(payload, dict):
        return
    ho = payload.get("houseOut") or {}
    if not isinstance(ho, dict):
        return
    inst = payload.get("installation") or {}
    workers = inst.get("workers") or {}
    assign = inst.get("assign") or {}

    def _ymd_to_dmy(ymd):
        try:
            return datetime.datetime.strptime(ymd, "%Y-%m-%d").strftime("%d/%m/%Y")
        except Exception:
            return ""

    def _weather_for(ymd):
        dmy = _ymd_to_dmy(ymd)
        w = workers.get(dmy)
        if isinstance(w, dict):
            return w.get("weatherAm"), w.get("weatherPm")
        return None, None

    def _recorder_for(ymd):
        dmy = _ymd_to_dmy(ymd)
        w = workers.get(dmy)
        if isinstance(w, dict) and w.get("recorder"):
            return w["recorder"]
        return ""

    for key, rec in ho.items():
        if not isinstance(rec, dict):
            continue
        od = rec.get("outDaily") or {}
        if not isinstance(od, dict):
            continue
        prefix = key.split("|")[0] if "|" in key else ""
        spec = "|".join(key.split("|")[1:]) if "|" in key else key
        changed = False
        for day, val in list(od.items()):
            if isinstance(val, dict):
                continue
            if not isinstance(val, (int, float)):
                continue
            am_wx, pm_wx = _weather_for(day)
            recorder = _recorder_for(day)
            dmy = _ymd_to_dmy(day)
            # 尝试从安装数据找目标猪舍#栋号/区域
            dest_house = prefix
            dest_bldg = "1"
            zone = ""
            w = workers.get(dmy)
            if isinstance(w, dict):
                zt = w.get("zoneTeamWorkers") or {}
                for z, teams in zt.items():
                    if not isinstance(teams, list):
                        continue
                    for t in teams:
                        if not isinstance(t, dict):
                            continue
                        ti = t.get("todayInstall") or {}
                        if spec in ti:
                            hs = str(t.get("house") or "")
                            hp = hs.split("#")
                            if hp[0]:
                                dest_house = hp[0]
                                dest_bldg = hp[1] if len(hp) > 1 else "1"
                                zone = z
                            break
                    if zone:
                        break
            if not zone:
                zone = assign.get(dest_house + "#" + dest_bldg) or ""
            od[day] = {
                "date": day,
                "qty": val,
                "recorder": recorder,
                "weatherAm": am_wx,
                "weatherPm": pm_wx,
                "destHouse": dest_house,
                "destBuildings": [dest_bldg],
                "zone": zone,
                "lines": [{"dest": dest_bldg, "qty": val, "seq": 1, "zone": zone}]
            }
            changed = True
        if changed:
            rec["outDaily"] = od
            rec["out"] = sum(
                (v.get("qty", 0) if isinstance(v, dict) else (float(v) if isinstance(v, (int, float)) else 0))
                for v in od.values()
            )


@app.route("/api/prod-factory/<pid>", methods=["PUT"])
def api_prod_factory_put(pid):
    data = request.get_json(force=True, silent=True) or {}
    me = (data.get("requester") or "").strip()
    if not me:
        return jsonify({"ok": False, "msg": "未登录"}), 401
    payload = data.get("data")
    if payload is None:
        return jsonify({"ok": False, "msg": "empty data"}), 400
    _normalize_out_daily(payload)
    try:
        blob = json.dumps(payload, ensure_ascii=False)
    except Exception:
        return jsonify({"ok": False, "msg": "bad data"}), 400
    conn = get_db()
    # ★★「永不丢」兜底（覆盖所有按日期键的业务数据）：无论回退闸是否触发，落库前都把服务器
    #    现有日期并集进来。客户端本次编辑优先（base），服务器独有的日期补回来；只有客户端显式
    #    写入 Deleted 墓碑的日期才移除。涵盖 production / workers / houseOut.outDaily / installation.workers。
    #    背景：10-07 16:01 一次旧快照 PUT 把 37 天生产整体覆盖成 23 天；20:05 又把出库日明细 12→6。
    _pre_row = conn.execute("SELECT data FROM prod_factory WHERE project_id=?", (str(pid),)).fetchone()
    if _pre_row and _pre_row["data"]:
        try:
            _pre = json.loads(_pre_row["data"])
            _dirty = False
            # 顶层按日期键的集合
            for _key in ("production", "workers"):
                _merged = _merge_date_map(payload.get(_key), _pre.get(_key))
                _tomb = payload.get(_key + "Deleted")
                if isinstance(_tomb, dict):
                    for _dk, _dv in _tomb.items():
                        if _dv:
                            _merged.pop(_dk, None)
                if _merged and _merged != payload.get(_key):
                    payload[_key] = _merged
                    _dirty = True
            # 出库日明细：houseOut[house].outDaily 按日期并集
            _ho = payload.get("houseOut") or {}
            _ho_pre = _pre.get("houseOut") or {}
            if isinstance(_ho, dict):
                for _h, _rec in _ho.items():
                    if not isinstance(_rec, dict):
                        continue
                    _od = _rec.get("outDaily") or {}
                    _od_pre = ((_ho_pre.get(_h) or {}).get("outDaily") or {})
                    _merged_od = _merge_date_map(_od, _od_pre)
                    if _merged_od and _merged_od != _od:
                        _rec["outDaily"] = _merged_od
                        _dirty = True
            # 安装每日记录：installation.workers 按日期并集（保留服务器侧 _deleted 逻辑删除）
            _inst = payload.get("installation") or {}
            _inst_pre = _pre.get("installation") or {}
            _iw = _inst.get("workers") if isinstance(_inst, dict) else None
            _iw_pre = _inst_pre.get("workers") if isinstance(_inst_pre, dict) else None
            if isinstance(_iw, dict):
                _merged_iw = _merge_date_map(_iw, _iw_pre)
                if isinstance(_iw_pre, dict):
                    for _dk, _dv in _iw_pre.items():
                        if isinstance(_dv, dict) and _dv.get("_deleted") and _dk not in _merged_iw:
                            _merged_iw[_dk] = _dv
                if _merged_iw != _iw:
                    _inst["workers"] = _merged_iw
                    payload["installation"] = _inst
                    _dirty = True
            if _dirty:
                blob = json.dumps(payload, ensure_ascii=False)
        except Exception as _me:
            print(f"[prod_factory PUT {pid}] data-merge guard warning: {_me}")
    # ★ 服务端防回退闸：禁止用信息量比现有服务器数据少得多的快照覆盖。
    # 背景：浏览器若打开着旧页面，本地只有 3 条出库，保存时会覆盖服务器已恢复的 8 条出库。
    existing_row = conn.execute("SELECT data FROM prod_factory WHERE project_id=?", (str(pid),)).fetchone()
    if existing_row and existing_row["data"]:
        try:
            existing = json.loads(existing_row["data"])
            ew = _prod_factory_weight(existing)
            iw = _prod_factory_weight(payload)
            ec = _prod_factory_counts(existing)
            ic = _prod_factory_counts(payload)
            # 任一核心指标低于阈值都视为回退
            reject_reason = None
            if ew > 0 and iw < ew * 0.6:
                reject_reason = f"overall weight too low (server:{ew} vs incoming:{iw})"
            elif ec[0] > 0 and ic[0] < ec[0] * 0.65:
                reject_reason = f"出库日明细过少 (server:{ec[0]} vs incoming:{ic[0]})"
            elif ec[1] > 0 and ic[1] < ec[1] * 0.65:
                reject_reason = f"安装天数过少 (server:{ec[1]} vs incoming:{ic[1]})"
            elif ec[2] > 0 and ic[2] < ec[2] * 0.65:
                reject_reason = f"安装记录过少 (server:{ec[2]} vs incoming:{ic[2]})"
            elif ec[3] > 0 and ic[3] < ec[3] * 0.65:
                reject_reason = f"每日生产天数过少 (server:{ec[3]} vs incoming:{ic[3]})"
            elif ec[4] > 0 and ic[4] < ec[4] * 0.65:
                reject_reason = f"人员快照天数过少 (server:{ec[4]} vs incoming:{ic[4]})"
            if reject_reason:
                # 仅当安装数据本身没有显著丢失时才“合并后接受”：保留用户本次安装编辑，
                # 并用服务器更完整的出库/物料等字段回填（避免本地旧快照覆盖服务器新数据）。
                # 若安装天数/记录数显著减少，则视为真正的旧快照回退，保留服务器版本。
                install_safe = (ic[1] >= ec[1] * 0.65) and (ic[2] >= ec[2] * 0.65)
                if install_safe:
                    try:
                        payload = _merge_factory_keep_install(payload, existing)
                    except Exception:
                        payload = existing
                    print(f"[prod_factory PUT {pid}] stale-merge(keep install edit, backfill server): {reject_reason}, requester={me}")
                    # 继续往下保存合并后的 payload
                else:
                    # ★ 真正的旧快照回退：保留服务器更完整的版本，原样回传前端合并，不丢任何数据。
                    print(f"[prod_factory PUT {pid}] stale-blocked(keep server): {reject_reason}, requester={me}")
                    try:
                        conn.close()
                    except Exception:
                        pass
                    return jsonify({
                        "ok": True,
                        "stale": True,
                        "msg": "服务器数据更完整，已保留服务器版本",
                        "data": existing,
                    })
        except Exception:
            pass
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    try:
        # 保存本次成功写入前的版本，便于回滚（只保留最近 10 个版本）
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS prod_factory_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id TEXT,
                    data TEXT,
                    updated_by TEXT,
                    updated_at TEXT
                )
            """)
            if existing_row and existing_row["data"]:
                conn.execute(
                    "INSERT INTO prod_factory_history (project_id, data, updated_by, updated_at) VALUES (?,?,?,?)",
                    (str(pid), existing_row["data"], (existing and existing.get('__updatedBy')) or '', now)
                )
                conn.execute(
                    "DELETE FROM prod_factory_history WHERE id NOT IN (SELECT id FROM prod_factory_history WHERE project_id=? ORDER BY updated_at DESC, id DESC LIMIT 10)",
                    (str(pid),)
                )
        except Exception as he:
            print(f"[prod_factory PUT {pid}] history backup warning: {he}")
        conn.execute("DELETE FROM prod_factory WHERE project_id=?", (str(pid),))
        conn.execute("INSERT INTO prod_factory (project_id, data, updated_by, updated_at) VALUES (?,?,?,?)",
                     (str(pid), blob, me, now))
        conn.commit()
    except Exception as e:
        try:
            conn.rollback()
        except Exception:
            pass
        conn.close()
        return jsonify({"ok": False, "msg": str(e)}), 500
    conn.close()
    _auto_backup_db("put_" + str(pid), min_interval=60)   # 每次保存后留一份整库快照（节流 60s）
    return jsonify({"ok": True})


def _ensure_history_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS prod_factory_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id TEXT,
            data TEXT,
            updated_by TEXT,
            updated_at TEXT
        )
    """)


@app.route("/api/prod-factory/<pid>/history", methods=["GET"])
def api_prod_factory_history(pid):
    """列出某项目的历史版本（含关键条目数，便于判断哪个版本数据更全）。"""
    me = (request.args.get("me") or "").strip()
    if not me:
        return jsonify({"ok": False, "msg": "未登录"}), 401
    conn = get_db()
    items = []
    try:
        _ensure_history_table(conn)
        rows = conn.execute(
            "SELECT id, data, updated_by, updated_at FROM prod_factory_history "
            "WHERE project_id=? ORDER BY id DESC LIMIT 50", (str(pid),)
        ).fetchall()
        for r in rows:
            try:
                d = json.loads(r["data"])
            except Exception:
                d = {}
            items.append({
                "id": r["id"],
                "updated_at": r["updated_at"],
                "updated_by": r["updated_by"],
                "houseOut": len((d.get("houseOut") or {})),
                "installDays": len(((d.get("installation") or {}).get("workers") or {})),
                "weight": _prod_factory_weight(d),
            })
    finally:
        conn.close()
    return jsonify({"ok": True, "items": items})


@app.route("/api/prod-factory/<pid>/restore", methods=["POST"])
def api_prod_factory_restore(pid):
    """把某个历史版本恢复为当前版本（恢复前先把当前版本也存一份，可再次反悔）。"""
    body = request.get_json(force=True, silent=True) or {}
    me = (body.get("requester") or "").strip()
    if not me:
        return jsonify({"ok": False, "msg": "未登录"}), 401
    try:
        hid = int(body.get("historyId"))
    except Exception:
        return jsonify({"ok": False, "msg": "缺少 historyId"}), 400
    conn = get_db()
    try:
        _ensure_history_table(conn)
        hrow = conn.execute(
            "SELECT data FROM prod_factory_history WHERE id=? AND project_id=?",
            (hid, str(pid))
        ).fetchone()
        if not hrow or not hrow["data"]:
            conn.close()
            return jsonify({"ok": False, "msg": "版本不存在"}), 404
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        cur = conn.execute("SELECT data FROM prod_factory WHERE project_id=?", (str(pid),)).fetchone()
        if cur and cur["data"]:
            _ensure_history_table(conn)
            conn.execute(
                "INSERT INTO prod_factory_history (project_id, data, updated_by, updated_at) VALUES (?,?,?,?)",
                (str(pid), cur["data"], "before-restore", now)
            )
        conn.execute("DELETE FROM prod_factory WHERE project_id=?", (str(pid),))
        conn.execute(
            "INSERT INTO prod_factory (project_id, data, updated_by, updated_at) VALUES (?,?,?,?)",
            (str(pid), hrow["data"], me + " (restore)", now)
        )
        conn.commit()
    except Exception as e:
        try:
            conn.rollback()
        except Exception:
            pass
        conn.close()
        return jsonify({"ok": False, "msg": str(e)}), 500
    conn.close()
    _auto_backup_db("restore_" + str(pid))
    return jsonify({"ok": True})


@app.route("/api/db-backup-now", methods=["POST"])
def api_db_backup_now():
    """手动生成一份整库快照（仅 tom）。"""
    body = request.get_json(force=True, silent=True) or {}
    me = (body.get("requester") or "").strip().lower()
    if me != "tom":
        return jsonify({"ok": False, "msg": "仅 tom 可操作"}), 403
    fn = _auto_backup_db("manual")
    return jsonify({"ok": bool(fn), "file": os.path.basename(fn) if fn else None})


@app.route("/api/db-backup", methods=["GET"])
def api_db_backup():
    """下载整库快照（仅 tom）。"""
    me = (request.args.get("me") or "").strip().lower()
    if me != "tom":
        return jsonify({"ok": False, "msg": "仅 tom 可操作"}), 403
    return send_from_directory(
        os.path.dirname(DB_PATH), os.path.basename(DB_PATH), as_attachment=True,
        download_name="agi_pm_%s.db" % time.strftime("%Y%m%d_%H%M%S")
    )


@app.route("/api/prod-kv/<path:key>", methods=["GET"])
def api_prod_kv_get(key):
    me = (request.args.get("me") or "").strip()
    if not me:
        return jsonify({"ok": False, "msg": "未登录"}), 401
    conn = get_db()
    row = conn.execute("SELECT data FROM prod_kv WHERE k=?", (str(key),)).fetchone()
    conn.close()
    if row and row["data"]:
        try:
            return jsonify({"ok": True, "data": json.loads(row["data"])})
        except Exception:
            return jsonify({"ok": True, "data": None})
    return jsonify({"ok": True, "data": None})


@app.route("/api/prod-kv/<path:key>", methods=["PUT"])
def api_prod_kv_put(key):
    data = request.get_json(force=True, silent=True) or {}
    me = (data.get("requester") or "").strip()
    if not me:
        return jsonify({"ok": False, "msg": "未登录"}), 401
    payload = data.get("data")
    if payload is None:
        return jsonify({"ok": False, "msg": "empty data"}), 400
    try:
        blob = json.dumps(payload, ensure_ascii=False)
    except Exception:
        return jsonify({"ok": False, "msg": "bad data"}), 400
    conn = get_db()
    try:
        conn.execute("DELETE FROM prod_kv WHERE k=?", (str(key),))
        conn.execute("INSERT INTO prod_kv (k, data, updated_by, updated_at) VALUES (?,?,?,?)",
                     (str(key), blob, me, time.strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
    except Exception as e:
        try:
            conn.rollback()
        except Exception:
            pass
        conn.close()
        return jsonify({"ok": False, "msg": str(e)}), 500
    conn.close()
    return jsonify({"ok": True})


# 版本号：用于确认运行中的服务进程加载的是哪一版 app.py
# （Python 进程启动后不会自动加载文件修改；改完代码必须重启服务）
APP_BUILD = "V2026.09.19-prod-receipt-3way"

@app.route("/api/version", methods=["GET"])
def api_version():
    return jsonify({"ok": True, "build": APP_BUILD})


@app.route("/api/approval-requests/<int:rid>/resolve", methods=["POST"])
def api_approval_resolve(rid):
    data = request.get_json(force=True, silent=True) or {}
    action = data.get("action")  # approve / reject / return（返回重新填写）
    resolver = (data.get("resolver") or "").strip()
    if action not in ("approve", "reject", "return"):
        return jsonify({"ok": False, "msg": "invalid action"}), 400
    conn = get_db()
    row = conn.execute("SELECT * FROM approval_requests WHERE id=?", (rid,)).fetchone()
    if not row:
        conn.close(); return jsonify({"ok": False, "msg": "not found"}), 404
    if row["status"] != "pending":
        conn.close(); return jsonify({"ok": False, "msg": "已处理"}), 409
    approvers = _norm_approver_list(json.loads(row["approvers"]) if row["approvers"] else [], conn)
    # 校验 resolver 是否是指定审批人，或审批人已离职且 resolver 是其代理人
    allowed = resolver in approvers
    if not allowed:
        delegated = {d["username"] for d in conn.execute(
            "SELECT username FROM users WHERE delegate_to=? AND status<>'active' AND username IN (%s)"
            % ",".join("?"*len(approvers)), (resolver, *approvers)).fetchall()}
        allowed = bool(delegated)
    if not allowed:
        conn.close()
        return jsonify({"ok": False, "msg": "您不是该审批单的指定审批人"}), 403
    # 三种结果：approve=同意 / reject=拒绝 / return=返回重新填写
    new_status = "approved" if action == "approve" else ("returned" if action == "return" else "rejected")
    result_note = data.get("note") or data.get("result_note") or ""
    if action == "return" and not result_note:
        result_note = "RETURN_FOR_EDIT"
    # 顺带把审批人字段持久化为规范的用户名（修复旧数字 ID 数据）
    conn.execute("""UPDATE approval_requests SET status=?, resolved_at=?, resolver=?, resolver_name=?, result_note=?, approvers=?
                    WHERE id=?""", (
        new_status, time.strftime("%Y-%m-%d %H:%M:%S"),
        resolver, data.get("resolver_name") or "",
        result_note, json.dumps(approvers, ensure_ascii=False), rid
    ))
    conn.commit(); conn.close()
    # 忘记密码审批（PWD-FORGET）：通过 → 密码自动重置为初始密码 66668888；拒绝 → 不做任何变更
    if row["block_id"] == "PWD-FORGET":
        if new_status == "approved":
            try:
                conn2 = get_db()
                conn2.execute("UPDATE users SET password=? WHERE username=?",
                              (DEFAULT_INIT_PASSWORD, row["target_id"] or row["requester"]))
                conn2.execute("UPDATE password_requests SET status='processed', processed_at=?, note='approved_reset' "
                              "WHERE username=? AND status='pending'",
                              (time.strftime("%Y-%m-%d %H:%M:%S"), row["target_id"] or row["requester"]))
                conn2.commit(); conn2.close()
            except Exception as e:
                print("[PWD-FORGET] 重置密码失败:", e)
        else:
            try:
                conn2 = get_db()
                conn2.execute("UPDATE password_requests SET status='rejected', processed_at=?, note='rejected' "
                              "WHERE username=? AND status='pending'",
                              (time.strftime("%Y-%m-%d %H:%M:%S"), row["target_id"] or row["requester"]))
                conn2.commit(); conn2.close()
            except Exception:
                pass
        bump_perm_version(row["requester"])
        return jsonify({"ok": True, "status": new_status})
    # 用户与权限管理审批（USR-D1 权限变更 / USR-D2 新增用户 / USR-D3 删除用户）：
    # 通过 → 按暂存 payload 执行；拒绝 → 丢弃。审批人已锁死三人组，任一人审批即结束。
    if row["block_id"] in ("USR-D1", "USR-D2", "USR-D3"):
        try:
            pl = json.loads(row["payload"] or "{}")
        except Exception:
            pl = {}
        conn2 = get_db()
        try:
            if new_status == "approved":
                if row["block_id"] == "USR-D1":
                    if pl.get("uid"):
                        conn2.execute("UPDATE users SET perms=? WHERE id=?",
                                      (json.dumps(pl.get("perms") or {}, ensure_ascii=False), pl["uid"]))
                elif row["block_id"] == "USR-D2":
                    # 账号一律小写（与登录名一致）：审批建号也必须归一化，
                    # 否则审批通过的账号会带大写，后续权限/数据范围/统计对不上。
                    _uname = (pl.get("username") or pl.get("login") or "").strip().lower()   # 前端 payload 用 login 字段
                    if _uname:
                        ex = conn2.execute("SELECT 1 FROM users WHERE lower(username)=lower(?)", (_uname,)).fetchone()
                        if not ex:
                            fa = pl.get("forgot_approvers") or ["tom"]
                            if isinstance(fa, list) and "tom" not in fa:
                                fa.insert(0, "tom")
                            conn2.execute("""INSERT INTO users
                               (username, password, real_name, role, position, status,
                                vis_can_see_me, vis_he_can_see, perms, forgot_approvers, created_at)
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
                                _uname, DEFAULT_INIT_PASSWORD, pl.get("name") or _uname,
                                "user", pl.get("position") or "", "active",
                                json.dumps(pl.get("vis_can_see_me") or []), json.dumps(pl.get("vis_he_can_see") or []),
                                json.dumps(pl.get("perms") or {}, ensure_ascii=False),
                                json.dumps(fa[:3], ensure_ascii=False), time.strftime("%Y-%m-%d %H:%M:%S")))
                            if pl.get("delegate_to"):
                                conn2.execute("UPDATE users SET delegate_to=? WHERE lower(username)=lower(?)",
                                              (pl["delegate_to"], _uname))
                elif row["block_id"] == "USR-D3":
                    if pl.get("uid"):
                        conn2.execute("DELETE FROM users WHERE id=?", (pl["uid"],))
                # 管理员名单同步（新增/编辑场景可能携带；tom 不可移除）
                if isinstance(pl.get("managers"), list) and pl["managers"]:
                    names = sorted({str(m).strip().lower() for m in pl["managers"] if str(m).strip()})
                    if "tom" not in names:
                        names.append("tom")
                    if 2 <= len(names) <= 4:
                        conn2.execute("DELETE FROM managers")
                        for n in names:
                            conn2.execute("INSERT OR IGNORE INTO managers (username) VALUES (?)", (n,))
                try:
                    bump_perm_version(pl.get("username") or "")
                except Exception:
                    pass
        except Exception as e:
            print("[USR-审批] 执行失败:", e)
        finally:
            try:
                conn2.commit()   # 关键：提交执行体写入（否则 close 时事务回滚丢弃）
            except Exception:
                pass
            try:
                conn2.close()
            except Exception:
                pass
        bump_perm_version(row["requester"])
        return jsonify({"ok": True, "status": new_status})
    # 审批通过：持续生效的审批才写入发起人 perms；单次生效审批仅做状态变更，不写入长期权限。
    # 同时刷新其版本号，触发其前端立即更新。
    is_persistent = (row["persist"] or "persistent").lower() == "persistent"
    if new_status == "approved" and is_persistent:
        try:
            conn2 = get_db()
            tgt = conn2.execute("SELECT id, perms FROM users WHERE username=?",
                                (row["requester"],)).fetchone()
            if tgt:
                import json as _json
                try:
                    p = _json.loads(tgt["perms"]) if tgt["perms"] else {}
                except Exception:
                    p = {}
                if not isinstance(p, dict):
                    p = {}
                # 通过后给予“特别授权看全公司”（与权限模态框的授权语义一致）
                blk = row["block_id"]
                if blk:
                    p[blk] = dict(p.get(blk, {}))
                    p[blk]["decision"] = "特别授权看全公司"
                    p[blk]["granted_by_approval"] = rid
                conn2.execute("UPDATE users SET perms=? WHERE id=?",
                              (_json.dumps(p, ensure_ascii=False), tgt["id"]))
                conn2.commit(); conn2.close()
        except Exception as e:
            print("[Approval] 写入授权失败:", e)
        bump_perm_version(row["requester"])
    elif new_status == "rejected" and is_persistent:
        # 拒绝：撤销因该审批产生的授权，恢复为“发起审批”以便用户再次申请
        try:
            conn2 = get_db()
            tgt = conn2.execute("SELECT id, perms FROM users WHERE username=?",
                                (row["requester"],)).fetchone()
            if tgt:
                import json as _json
                try:
                    p = _json.loads(tgt["perms"]) if tgt["perms"] else {}
                except Exception:
                    p = {}
                if isinstance(p, dict):
                    blk = row["block_id"]
                    if blk and blk in p and p[blk].get("granted_by_approval") == rid:
                        p[blk]["decision"] = "发起审批"
                        p[blk].pop("granted_by_approval", None)
                        conn2.execute("UPDATE users SET perms=? WHERE id=?",
                                      (_json.dumps(p, ensure_ascii=False), tgt["id"]))
                        conn2.commit()
                conn2.close()
        except Exception as e:
            print("[Approval] 撤销授权失败:", e)
        bump_perm_version(row["requester"])
    else:
        # 单次生效审批仅刷新版本号，不修改 perms
        bump_perm_version(row["requester"])
    return jsonify({"ok": True, "status": new_status})


def _can_delete_approval(conn, username):
    """是否有权限删除审批单。
    权限完全由「职位标签(role)」弹性决定，不绑定具体账号：
      - 职位标签含 管理员 / 总经理 / 副总经理 / 总裁 的人；
      - 以及固定人名 tom（真实且固定的个人）。
    role 由用户在用户列表里自由新增/修改，因此这里只按 role 文字匹配，
    不再硬编码任何具体账号（如 gm*/dgm*）。"""
    if not username:
        return False
    if username == "tom":
        return True
    u = conn.execute("SELECT role FROM users WHERE username=?", (username,)).fetchone()
    role = (u["role"] or "") if u else ""
    for kw in ("管理员", "总经理", "副总经理", "总裁"):
        if kw in role:
            return True
    return False


@app.route("/api/approval-requests/<int:rid>", methods=["DELETE"])
def api_approval_delete(rid):
    username = (request.args.get("username") or "").strip()
    conn = get_db()
    if not _can_delete_approval(conn, username):
        conn.close()
        return jsonify({"ok": False, "msg": "无删除权限"}), 403
    row = conn.execute("SELECT * FROM approval_requests WHERE id=?", (rid,)).fetchone()
    if not row:
        conn.close()
        return jsonify({"ok": False, "msg": "not found"}), 404
    conn.execute("DELETE FROM approval_requests WHERE id=?", (rid,))
    conn.commit(); conn.close()
    return jsonify({"ok": True})


@app.route("/api/users", methods=["GET"])
def api_users_list():
    conn = get_db()
    managers = set(_manager_usernames(conn))
    rows = conn.execute(
        "SELECT * FROM users ORDER BY sort_order ASC, id ASC"
    ).fetchall()
    users = [_row_to_user(r, managers) for r in rows]
    for u in users:
        u["perms"] = _norm_user_perms(u.get("perms", {}) or {}, conn)
    conn.close()
    return jsonify({"ok": True, "users": users, "managers": sorted(managers)})


# 销售/销售总监的 WON 锁死权限：这 5 项一律强制 decision=hide，
# UI 已锁死下拉，此处兜底所有保存路径（新建/更新），防止任何绕过
SALES_LOCKED_WON_PERMS = ("WON-D2", "WON-D3", "WON-N1", "WON-C1", "WON-P345")

# 用户与权限管理三人审批组（锁死）：任一人审批即结束该流程；三人自己操作免审批（与管理员同级直达）
TRI_APPROVERS = ("tom", "cuong", "james")


def _user_perm_dec(conn, username, bid):
    """读取用户 perms 中某区块的决策；未配置返回 ''。"""
    try:
        r = conn.execute("SELECT perms FROM users WHERE username=?", (username,)).fetchone()
        if not r or not r["perms"]:
            return ""
        p = json.loads(r["perms"])
        return ((p.get(bid) or {}).get("decision") or "")
    except Exception:
        return ""


def _usr_op_gate(conn, op, bid):
    """用户管理写操作闸门。
    返回 'direct'（三人组/管理员，直接执行）、'allow'（被授权，前端应走暂存审批）、'deny'（无权限）。
    未配置的 USR-D* 一律视为隐藏（deny）。"""
    if (op or "").strip().lower() in [x.lower() for x in TRI_APPROVERS]:
        return "direct"
    try:
        if _is_manager(conn, op):
            return "direct"
    except Exception:
        pass
    if _user_perm_dec(conn, op, bid) == "allow":
        return "allow"
    return "deny"

# 观察者固定权限模板：整套权限锁死为此值（审批人保留原有配置）；
# 未列入的区块（审批 APP-*、用户与权限管理 USR-* 等）对观察者一律禁止
OBSERVER_FIXED_PERMS = {
    "DB-S1": "default", "DB-P1": "default", "DB-B1": "default", "DB-C1": "default",
    "US-LH1": "default", "US-LH2": "default",
    "DB-MT1": "default", "DB-FD1": "default", "DB-LS1": "default", "DB-FX1": "default",
    "CRM-L1": "all", "CRM-D1": "default", "CRM-D2": "hide", "CRM-D3": "hide",
    "CRM-F1": "approve", "CRM-N1": "hide", "CRM-E1": "default",
    "WON-L1": "default", "WON-D1": "default", "WON-D2": "hide", "WON-D3": "hide",
    "WON-D4": "default", "WON-E1": "default", "WON-N1": "hide", "WON-C1": "hide",
    "WON-P345": "hide",
    "LOST-L1": "all", "LOST-D1": "default", "LOST-D2": "hide", "LOST-D3": "hide",
    "LOST-R1": "approve", "LOST-E1": "default",
}


def _is_observer_pos(position):
    return (position or "").strip() == "观察者"


def _force_observer_perms(perms, position):
    """观察者：仅作预设——完全未配置的区块按固定模板填初始值；已有配置（管理员改过）一律不动。"""
    try:
        if not _is_observer_pos(position):
            return perms
        if not isinstance(perms, dict):
            perms = {}
        for bid, dec in OBSERVER_FIXED_PERMS.items():
            if bid not in perms:
                perms[bid] = {"decision": dec, "approvers": []}
        return perms
    except Exception:
        return perms


def _force_sales_locked_perms(perms, position):
    try:
        if (position or "").strip() not in ("销售", "销售总监"):
            return perms
        if not isinstance(perms, dict):
            return perms
        for bid in SALES_LOCKED_WON_PERMS:
            blk = perms.get(bid)
            if isinstance(blk, dict):
                blk["decision"] = "hide"
                blk["approvers"] = []
            else:
                perms[bid] = {"decision": "hide", "approvers": []}
    except Exception:
        pass
    return perms


@app.route("/api/users", methods=["POST"])
def api_users_create():
    data = request.get_json(force=True, silent=True) or {}
    # 用户与权限管理闸门：三人组/管理员直达；被授权（USR-D2=允许新增）者由前端走暂存审批（不直达）；
    # 未授权一律拒绝（默认隐藏语义）
    _op = (request.headers.get("X-User-Name") or "").strip()
    _c0 = get_db()
    _gate = _usr_op_gate(_c0, _op, "USR-D2")
    _c0.close()
    # 三人组/管理员直达；allow 用户必须走页面审批流程（服务端拒绝直达，防止绕过审批）
    if _gate != "direct":
        return jsonify({"ok": False, "message": "无权限：新增用户未对你开放" if _gate == "deny" else "该操作需经审批流程，请在页面中提交申请"}), 403
    # 账号一律小写（与登录名一致）：同名不同大小写会导致权限、数据范围、
    # 销售归属统计错乱。前端已限制，这里做服务端兜底，直接调接口也逃不掉。
    username = (data.get("username") or "").strip().lower()
    real_name = (data.get("real_name") or "").strip()
    position = data.get("position") or ""
    status = data.get("status") or "active"
    vis_can_see_me = data.get("vis_can_see_me") or []
    vis_he_can_see = data.get("vis_he_can_see") or []
    perms = data.get("perms") or {}
    forgot_approvers = data.get("forgot_approvers") or ["tom"]
    if not username or not real_name:
        return jsonify({"ok": False, "message": "姓名和账号不能为空"})
    # 账号只允许小写字母和数字（与前端规则一致，接口层面再拦一次）
    if not re.match(r'^[a-z0-9]+$', username):
        return jsonify({"ok": False, "message": "登录账号只能使用小写字母和数字"})
    import json as _json
    conn = get_db()
    perms = _norm_user_perms(perms, conn)
    perms = _force_sales_locked_perms(perms, position)
    perms = _force_observer_perms(perms, position)
    conn = get_db()
    exists = conn.execute("SELECT id FROM users WHERE username=?", (username,)).fetchone()
    if exists:
        conn.close()
        return jsonify({"ok": False, "message": "账号已存在"})
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 忘记密码审批人：默认 tom，可追加（1~3 人）；tom 必在
    fa = [str(x).strip() for x in forgot_approvers if str(x).strip()]
    if "tom" not in fa:
        fa.insert(0, "tom")
    # 新建用户默认排在末尾：取当前最大 sort_order + 1000
    max_so = conn.execute("SELECT COALESCE(MAX(sort_order), 0) FROM users").fetchone()[0]
    sort_order = int(max_so or 0) + 1000
    cur = conn.execute(
        """INSERT INTO users
           (username, password, real_name, role, position, status,
            vis_can_see_me, vis_he_can_see, perms, forgot_approvers, created_at, sort_order)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (username, DEFAULT_INIT_PASSWORD, real_name, "user", position, status,
         _json.dumps(vis_can_see_me), _json.dumps(vis_he_can_see),
         _json.dumps(perms), _json.dumps(fa[:3], ensure_ascii=False), created_at, sort_order)
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return jsonify({"ok": True, "id": new_id, "message": "保存成功"})


@app.route("/api/managers", methods=["GET"])
def api_managers_list():
    conn = get_db()
    managers = sorted(_manager_usernames(conn))
    conn.close()
    return jsonify({"ok": True, "managers": managers})


@app.route("/api/managers", methods=["PUT"])
def api_managers_update():
    """自由任命/撤销管理员。约束：tom 不可被移除；总数 2-4 人。"""
    data = request.get_json(force=True, silent=True) or {}
    managers = [str(x).strip().lower() for x in (data.get("managers") or []) if str(x).strip()]
    managers = sorted(set(managers))
    if "tom" not in managers:
        return jsonify({"ok": False, "message": "tom 必须是管理员之一"}), 400
    if len(managers) < 2 or len(managers) > 4:
        return jsonify({"ok": False, "message": "管理人员数量必须在 2-4 人之间"}), 400
    conn = get_db()
    # 校验并自动过滤不存在的账号（历史残留/幽灵账号不阻断保存）
    placeholders = ",".join("?" * len(managers)) if managers else "''"
    existing = {r["username"] for r in conn.execute(f"SELECT username FROM users WHERE username IN ({placeholders})", managers).fetchall()} if managers else set()
    managers = sorted(set(managers) & existing)
    if "tom" not in managers:
        conn.close()
        return jsonify({"ok": False, "message": "tom 必须是管理员之一"}), 400
    if len(managers) < 2 or len(managers) > 4:
        conn.close()
        return jsonify({"ok": False, "message": "管理人员数量必须在 2-4 人之间"}), 400
    # 原子替换
    conn.execute("DELETE FROM managers")
    for username in managers:
        conn.execute("INSERT INTO managers (username) VALUES (?)", (username,))
    conn.commit()
    conn.close()
    return jsonify({"ok": True, "managers": managers})


@app.route("/api/users/<int:uid>", methods=["PUT"])
def api_users_update(uid):
    data = request.get_json(force=True, silent=True) or {}
    # 用户与权限管理闸门：三人组/管理员直达；被授权（USR-D1=允许编辑）者由前端走暂存审批（不直达）
    _op = (request.headers.get("X-User-Name") or "").strip()
    _c0 = get_db()
    _gate = _usr_op_gate(_c0, _op, "USR-D1")
    _c0.close()
    if _gate != "direct":
        return jsonify({"ok": False, "message": "无权限：编辑用户权限未对你开放" if _gate == "deny" else "该操作需经审批流程，请在页面中提交申请"}), 403
    real_name = (data.get("real_name") or "").strip()
    position = data.get("position") or ""
    status = data.get("status") or "active"
    vis_can_see_me = data.get("vis_can_see_me") or []
    vis_he_can_see = data.get("vis_he_can_see") or []
    perms = data.get("perms") or {}
    forgot_approvers = data.get("forgot_approvers")
    delegate_to = (data.get("delegate_to") or "").strip()
    if not real_name:
        return jsonify({"ok": False, "message": "姓名不能为空"})
    import json as _json
    conn = get_db()
    perms = _norm_user_perms(perms, conn)
    perms = _force_sales_locked_perms(perms, position)
    perms = _force_observer_perms(perms, position)
    row = conn.execute("SELECT id, position, perms FROM users WHERE id=?", (uid,)).fetchone()
    if not row:
        conn.close()
        return jsonify({"ok": False, "message": "用户不存在"})
    # WON-L1 职位联动兜底：职位从 销售/销售总监 改为其他职位时，
    # 若 WON-L1 决策仍为销售缺省的 hide，则自动改回 default（不覆盖其他决策值）。
    try:
        _old_pos = (row["position"] or "").strip()
        _new_pos = (position or "").strip()
        if _old_pos in ("销售", "销售总监") and _new_pos not in ("销售", "销售总监"):
            blk = perms.get("WON-L1") if isinstance(perms, dict) else None
            if isinstance(blk, dict) and blk.get("decision") == "hide":
                blk["decision"] = "default"
    except Exception:
        pass
    # 不能把离职代理指向自己
    if delegate_to:
        tgt = conn.execute("SELECT username FROM users WHERE id=?", (uid,)).fetchone()
        if tgt and tgt["username"] == delegate_to:
            conn.close()
            return jsonify({"ok": False, "message": "离职代理不能设置为本人"})
    # 忘记密码审批人（可选保存；tom 必在，最多 3 人）
    fa_sql = None
    if forgot_approvers is not None:
        fa = [str(x).strip() for x in forgot_approvers if str(x).strip()]
        if "tom" not in fa:
            fa.insert(0, "tom")
        fa_sql = _json.dumps(fa[:3], ensure_ascii=False)
    conn.execute(
        """UPDATE users SET real_name=?, position=?, status=?,
           vis_can_see_me=?, vis_he_can_see=?, perms=?, delegate_to=? WHERE id=?""",
        (real_name, position, status,
         _json.dumps(vis_can_see_me), _json.dumps(vis_he_can_see),
         _json.dumps(perms), delegate_to, uid)
    )
    if fa_sql is not None:
        conn.execute("UPDATE users SET forgot_approvers=? WHERE id=?", (fa_sql, uid))
    conn.commit()
    # 权限/角色/状态变更：刷新目标用户版本号，触发其前端实时刷新
    try:
        tgt = conn.execute("SELECT username FROM users WHERE id=?", (uid,)).fetchone()
        if tgt:
            bump_perm_version(tgt["username"])
    except Exception:
        pass
    conn.close()
    return jsonify({"ok": True, "message": "保存成功"})


@app.route("/api/users/<int:uid>", methods=["DELETE"])
def api_users_delete(uid):
    # 用户与权限管理闸门：三人组/管理员直达；被授权（USR-D3=允许删除/停用）者由前端走暂存审批（不直达）
    _op = (request.headers.get("X-User-Name") or "").strip()
    _c0 = get_db()
    _gate = _usr_op_gate(_c0, _op, "USR-D3")
    _c0.close()
    if _gate != "direct":
        return jsonify({"ok": False, "message": "无权限：删除/停用用户未对你开放" if _gate == "deny" else "该操作需经审批流程，请在页面中提交申请"}), 403
    conn = get_db()
    conn.execute("DELETE FROM users WHERE id=?", (uid,))
    conn.commit()
    conn.close()
    return jsonify({"ok": True, "message": "删除成功"})


@app.route("/api/users/reorder", methods=["PUT"])
def api_users_reorder():
    """调整用户列表顺序：仅 tom/cuong/james 或管理员可执行。"""
    data = request.get_json(force=True, silent=True) or {}
    _op = (request.headers.get("X-User-Name") or "").strip()
    conn = get_db()
    if _op.lower() not in [x.lower() for x in TRI_APPROVERS] and not _is_manager(conn, _op):
        conn.close()
        return jsonify({"ok": False, "message": "无权限：仅管理员或指定审批人可调整顺序"}), 403
    orders = data.get("orders") or []
    for o in orders:
        uid = o.get("id")
        so = o.get("sort_order")
        if uid is None or so is None:
            continue
        conn.execute("UPDATE users SET sort_order=? WHERE id=?", (int(so), int(uid)))
    conn.commit()
    conn.close()
    return jsonify({"ok": True, "message": "顺序已保存"})


# ===================== 启动 =====================
@app.after_request
def _no_cache(resp):
    # 禁用浏览器强缓存，确保每次刷新都拿到最新 index.html / JS，避免改了代码却看不到
    resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    return resp

# ===================== 服务端翻译中转（ptTranslateViaGoogle 优先走此端点）=====================
# 目的：翻译请求与系统其它功能走同一条同源通道，绕开浏览器端扩展/证书/网络
#      对 translate.googleapis.com 直连的干扰。
# GET /api/translate?q=<text>&target=<zh|en|vi>  →  {ok:true, text:"..."}
@app.route("/api/translate", methods=["GET"])
def api_translate():
    q = (request.args.get("q") or "")[:1000]
    target = (request.args.get("target") or "en").lower()
    if not q:
        return jsonify({"ok": False, "error": "empty q"}), 400
    if target not in ("zh", "en", "vi"):
        return jsonify({"ok": False, "error": "bad target"}), 400
    t = fin_translate(q, target)
    if t:
        return jsonify({"ok": True, "text": t})
    return jsonify({"ok": False, "error": "translation failed (all providers)"}), 502

# ===================== 服务端备注三语补翻（复刻云端 M13）=====================
# 触发：前端列表加载后 fire 调用 /api/translate-remarks?table=...&limit=N
# 作用：扫描表内缺失的 remark_zh/en/vi，用 Google 翻译补齐并写回 SQLite。
# 表结构差异：
#   crm_projects / lost_projects：remark_zh/en/vi 独立列（缺列时自动 ALTER）
#   won_projects：三语 JSON 打包在 cust/gs/agi_remark 列
# ==========================================================================
_TRANSLATE_CACHE = {}  # "text|target" -> translation

# ★不翻译保护词（FIN-NO-TRANS-20261013）：品牌名「DABACO」在 zh/vi/en 三语里都必须
#   保留拉丁写法，绝不能被译成中文（如「达巴科」）或越南文。规则：原文含保护词而译文把它
#   弄丢了 → 直接退回原文（与前端 fin_transChecked 同一套判定）。要加保护词，往这里加小写词。
_FIN_NO_TRANS = ("dabaco",)


def _fin_has_no_trans(s):
    s = (s or "").lower()
    return any(w in s for w in _FIN_NO_TRANS)


# ---- 统一翻译链（FIN-TRANS-CHAIN）：Google(主) -> DeepL(备) -> MyMemory(末) ----
# DeepL key：优先环境变量 DEEPL_API_KEY，否则读 finance_data/.deepl_key（已 gitignore）
_DEEPL_KEY = os.environ.get("DEEPL_API_KEY") or ""
if not _DEEPL_KEY:
    try:
        _kf = os.path.join(os.path.dirname(os.path.abspath(__file__)), "finance_data", ".deepl_key")
        if os.path.isfile(_kf):
            _DEEPL_KEY = open(_kf, encoding="utf-8").read().strip()
    except Exception:
        _DEEPL_KEY = ""
_DEEPL_ENDPOINT = "https://api-free.deepl.com/v2/translate"
_DEEPL_LANG = {"zh": "ZH", "en": "EN", "vi": "VI"}


def _gtrans_google(text, target):
    try:
        u = ("https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl="
             + urllib.parse.quote(target) + "&dt=t&q=" + urllib.parse.quote(text))
        req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            d = json.loads(resp.read().decode("utf-8"))
        return "".join(seg[0] for seg in (d[0] or []) if seg and seg[0])
    except Exception:
        return ""


def _gtrans_deepl(text, target):
    if not _DEEPL_KEY:
        return ""
    try:
        body = urllib.parse.urlencode({"text": text, "target_lang": _DEEPL_LANG[target]}).encode("utf-8")
        req = urllib.request.Request(_DEEPL_ENDPOINT, data=body, method="POST")
        req.add_header("Authorization", "DeepL-Auth-Key " + _DEEPL_KEY)
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
        req.add_header("User-Agent", "Mozilla/5.0")
        with urllib.request.urlopen(req, timeout=12) as resp:
            j = json.loads(resp.read().decode("utf-8"))
        return (j.get("translations") or [{}])[0].get("text") or ""
    except Exception:
        return ""


def _gtrans_mymemory(text, target):
    try:
        u = ("https://api.mymemory.translated.net/get?q=" + urllib.parse.quote(text)
             + "&langpair=vi|" + urllib.parse.quote(target))
        req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=12) as resp:
            d = json.loads(resp.read().decode("utf-8"))
        t = (d.get("responseData") or {}).get("translatedText") or ""
        if "MYMEMORY WARNING" in t:
            return ""
        return t
    except Exception:
        return ""


def fin_translate(text, target):
    """三档翻译链，返回译文；全失败返回 ''。结果经 _TRANSLATE_CACHE 缓存。"""
    text = (text or "").strip()
    if not text or target not in ("zh", "en", "vi"):
        return ""
    ck = text + "|" + target
    if ck in _TRANSLATE_CACHE:
        return _TRANSLATE_CACHE[ck]
    res = ""
    for fn in (_gtrans_google, _gtrans_deepl, _gtrans_mymemory):
        try:
            r = fn(text, target)
        except Exception:
            r = ""
        if r:
            res = r
            break
    if res and _fin_has_no_trans(text) and not _fin_has_no_trans(res):
        res = text   # ★保护词被译掉（如 DABACO→达巴科）→ 退回原文（FIN-NO-TRANS-20261013）
    if res:
        _TRANSLATE_CACHE[ck] = res
    return res


def _google_translate_single(text, target):
    # 复用统一翻译链（Google->DeepL->MyMemory），保持历史调用方兼容
    return fin_translate(text, target)


def _parse_tri(v):
    if v and isinstance(v, dict):
        return {"zh": v.get("zh") or "", "en": v.get("en") or "", "vi": v.get("vi") or ""}
    s = "" if v is None else str(v)
    try:
        o = json.loads(s)
        if o and isinstance(o, dict) and not isinstance(o, list):
            return {"zh": o.get("zh") or "", "en": o.get("en") or "", "vi": o.get("vi") or ""}
    except Exception:
        pass
    return {"zh": s, "en": "", "vi": ""}


@app.route("/api/translate-remarks", methods=["GET"])
def api_translate_remarks():
    table = (request.args.get("table") or "").strip()
    limit = min(int(request.args.get("limit") or "40"), 80)

    TABLES = {
        "crm_projects":  {"cols": ["remark"], "json": False},
        "lost_projects": {"cols": ["remark"], "json": False},
        "won_projects":  {"cols": ["cust_remark", "gs_remark", "agi_remark"], "json": True},
    }
    conf = TABLES.get(table)
    if not conf:
        return jsonify({"ok": False, "error": "bad table"}), 400

    conn = get_db()
    try:
        c = conn.cursor()
        # 独立列表缺列时幂等补齐
        if not conf["json"]:
            for s in ("zh", "en", "vi"):
                try:
                    c.execute(f"ALTER TABLE {table} ADD COLUMN remark_{s} TEXT DEFAULT ''")
                except sqlite3.OperationalError:
                    pass

        rows = [dict(r) for r in c.execute(f"SELECT * FROM {table}").fetchall()]

        jobs = []
        for row in rows:
            for col in conf["cols"]:
                tri = _parse_tri(row.get(col))
                has = {
                    "zh": bool(tri["zh"].strip()),
                    "en": bool(tri["en"].strip()),
                    "vi": bool(tri["vi"].strip()),
                }
                if not has["zh"] and not has["en"] and not has["vi"]:
                    continue
                missing = [l for l in ("en", "vi", "zh") if not has[l]]
                if not missing:
                    continue
                src_lang = "zh" if has["zh"] else ("en" if has["en"] else "vi")
                src_text = tri[src_lang]
                for lang in missing:
                    jobs.append({
                        "row": row,
                        "col": col,
                        "tri": tri,
                        "lang": lang,
                        "src_text": src_text,
                    })

        if not jobs:
            return jsonify({"ok": True, "filled": 0, "remaining": 0})

        # 只翻译未缓存的任务，并受 limit 限制
        todo = [j for j in jobs if (j["src_text"] + "|" + j["lang"]) not in _TRANSLATE_CACHE][:limit]
        for j in todo:
            try:
                j["trans"] = _google_translate_single(j["src_text"], j["lang"])
            except Exception:
                j["trans"] = ""

        for j in todo:
            if j.get("trans"):
                j["tri"][j["lang"]] = j["trans"]

        filled = 0
        applied = set()
        updates_by_col = {col: [] for col in conf["cols"]}
        for j in todo:
            if not j.get("trans"):
                continue
            rk = str(j["row"]["id"]) + "|" + j["col"]
            if rk in applied:
                continue
            applied.add(rk)
            if conf["json"]:
                updates_by_col[j["col"]].append((
                    json.dumps({"zh": j["tri"]["zh"], "en": j["tri"]["en"], "vi": j["tri"]["vi"]}, ensure_ascii=False),
                    j["row"]["id"],
                ))
            else:
                updates_by_col[j["col"]].append((
                    j["tri"]["zh"], j["tri"]["en"], j["tri"]["vi"],
                    j["row"]["id"],
                ))

        for col, vals in updates_by_col.items():
            if not vals:
                continue
            if conf["json"]:
                c.executemany(f"UPDATE {table} SET {col}=? WHERE id=?", vals)
            else:
                c.executemany(f"UPDATE {table} SET remark_zh=?, remark_en=?, remark_vi=? WHERE id=?", vals)
            filled += len(vals)

        conn.commit()

        remaining = 0
        for j in jobs:
            key = j["src_text"] + "|" + j["lang"]
            if not (j.get("trans") or key in _TRANSLATE_CACHE):
                remaining += 1

        return jsonify({"ok": True, "filled": filled, "remaining": remaining})
    except Exception as e:
        conn.rollback()
        return jsonify({"ok": False, "error": str(e)}), 502
    finally:
        conn.close()


# ===================== 金属价格走势 + 历史汇率（免费数据源：雅虎财经，无需 API Key）=====================
# 4 个品种：中国铁(铁矿石) / 不锈钢(热轧卷板) / 锌锭 / 塑料(石化原料)，均为国际真实基准价（USD/吨）。
# 价格以 USD 为基准，按【真实的每日历史汇率】换算为 RMB / VND，使走势与同期汇率对应。
# 历史汇率：USDCNY=X（USD→人民币）、USDVND=X（USD→越南盾），CNY→VND 由二者推导。
# 数据每日缓存到 SQLite(metal_cache / fx_cache)，避免频繁外网请求；外网不可达时回退缓存。
# ⛔⛔⛔ 2026-09-04 整体冻结声明（锁死）：金属/汇率这条价格管线的采集、换算、离群点守卫逻辑
# 已校验通过，四个品种（铁/不锈钢/锌/塑料）走势单位对齐(USD/吨)、数值正确。
# 严禁在未取得用户明确同意前对以下任一处做"优化/重构/简化"：METAL_SYMBOLS、
# METAL_OFFICIAL_CODES、METAL_TO_TON_FACTOR、_metal_clean_outliers 及其两处调用点。
# 任何改动都可能重新引入单位错位或脏数据，导致图表再次失真。
import urllib.request
import urllib.error
import urllib.parse

METAL_SYMBOLS = {
    "iron": "HRC=F",      # 热轧卷板（代表钢铁/钢材成品基准价，USD/吨）
    "stainless": "HRC=F", # 热轧卷板（作为不锈钢上游替代指标，USD/吨）
    "zinc": "ZNC=F",      # LME 锌锭（USD/吨）
    "plastic": "BZ=F",    # 布伦特原油（代表塑料原料，原始 USD/桶，需换算为 USD/吨）
}
# 官方月度数据源（IMF Primary Commodity Price System，免费、无需 API Key）
# 前缀 P 表示 actual market price（美元实际价）。若 IMF 返回为空，自动回退 Yahoo。
# 注：stainless 与 plastic 在 IMF PCPS 中暂无公认独立代码，暂用 Yahoo 期货，后续可按需求换 World Bank。
METAL_OFFICIAL_CODES = {
    "iron": "PIORECR",    # 铁矿石，美元/吨
    "zinc": "PZINC",      # 锌，美元/吨
}
# 各品种原始 Yahoo 单位 -> 标准化 USD/吨 的换算系数（缓存中存原始值，渲染时换算）
# iron/stainless/zinc 原始已是 USD/吨，系数 1.0
# plastic(BZ=F 布伦特原油) 原始是 USD/桶，1 吨 ≈ 7.33 桶（原油密度折算），系数 7.33
METAL_TO_TON_FACTOR = {
    "iron": 1.0,
    "stainless": 1.0,
    "zinc": 1.0,
    "plastic": 7.33,   # 桶 -> 吨：1 吨原油 ≈ 7.33 桶
}
# 各品种原始单位说明（用于前端展示）
METAL_RAW_UNIT = {
    "iron": "USD/ton",
    "stainless": "USD/ton",
    "zinc": "USD/ton",
    "plastic": "USD/barrel",
}
FX_SYMBOLS = {
    "USDCNY": "USDCNY=X",  # 1 USD = ? CNY（真实历史）
    "USDVND": "USDVND=X",  # 1 USD = ? VND（真实历史）
    "USDPHP": "USDPHP=X",  # 1 USD = ? PHP（真实历史；菲律宾用）
}

# 当 Yahoo 无某月历史汇率时的本地回退（近似值，仅用于菲律宾 PHP 等少数缺数情形）
FX_LCU_PER_USD_FALLBACK = {
    "USDPHP": {
        "2021": 50.3, "2022": 54.4, "2023": 55.8, "2024": 57.2,
        "2025": 57.8, "2026": 58.5,   # 2026 全年用 58.5 近似（含 2026-08）
    },
}

# ===================== 大宗饲料原料价格 =====================
# 国际市场数据源：CBOT 期货（雅虎财经免费源）。
# 重要单位修正：
#   - 玉米 ZC=F / 大豆 ZS=F 报价单位为「美分/蒲式耳」(currency=USX)，需 ×39.37/100 换算为 USD/吨
#   - 豆粕 ZM=F 报价单位为「美元/短吨」(currency=USD)，需 ×1.102 换算为 USD/吨（1 短吨≈0.907 公吨）
# 中国/越南价格 = 国际 USD/吨基准 × 区域升贴水(basis，小幅 ±5~10%) 后按真实历史汇率换算到本币。
# DDGS 无液态期货，以豆粕 × 0.9 近似（DDGS 历史价约为豆粕的 90%）。
FEED_ITEMS = {
    # 2026-08-25 按用户提供的 CNF 到岸价重新校准：
    #   CBOT 玉米 ≈203 USD/吨，大豆 ≈446 USD/吨，豆粕 SM≈390 USD/吨，DDGS 美湾锚点 300 USD/吨。
    #   系数 = 目标到岸价 ÷ CBOT 基准，用于把实时 CBOT 裸价映射到各国 CNF 到岸价。
    "corn":     {"sym": "ZC=F", "unit_factor": 0.3937, "china_basis": 1.424, "vn_basis": 1.365, "unit": "USD/ton"},
    "soybean":  {"sym": "ZS=F", "unit_factor": 0.3937, "china_basis": 1.359, "vn_basis": 1.332, "unit": "USD/ton"},
    "soymeal":  {"sym": "ZM=F", "unit_factor": 1.102,  "china_basis": 1.205, "vn_basis": 1.174, "unit": "USD/ton"},
    "ddgs":     {"sym": "ZM=F", "ddgs_ratio": 0.9, "unit_factor": 1.102, "china_basis": 1.083, "vn_basis": 1.083, "unit": "USD/ton"},
}
# 各曲线原生货币：国际=USD，中国=RMB，越南=VND
FEED_CURVE_NATIVE = {"intl": "USD", "china": "RMB", "vietnam": "VND"}

# 13/14 国当地 DDP 采购价：用 CBOT 国际基准 × 到岸升贴水系数模拟。
# 因 Yahoo 免费源无法提供各国现货 DDP，此处使用行业经验系数（海运+关税+内陆物流）。
# key 为国家代码；name 为三语名称；basis 为对国际 USD/吨的升贴水倍数。
FEED_COUNTRY_BASIS = {
    # 2026-08-25 按用户提供的 CNF 到岸价重新校准。
    # 系数 = 目标到岸价 ÷ CBOT 基准；基准：corn=203, soybean=446, soymeal=390, ddgs=300。
    "TH": {"name": {"zh": "泰国", "en": "Thailand", "vi": "Thái Lan"}, "basis": {"corn": 1.374, "soybean": 1.336, "soymeal": 1.179, "ddgs": 1.083}},
    "MM": {"name": {"zh": "缅甸", "en": "Myanmar", "vi": "Myanmar"}, "basis": {"corn": 1.384, "soybean": 1.341, "soymeal": 1.185, "ddgs": 1.083}},
    "LA": {"name": {"zh": "老挝", "en": "Laos", "vi": "Lào"}, "basis": {"corn": 1.399, "soybean": 1.348, "soymeal": 1.192, "ddgs": 1.083}},
    "KH": {"name": {"zh": "柬埔寨", "en": "Cambodia", "vi": "Campuchia"}, "basis": {"corn": 1.379, "soybean": 1.339, "soymeal": 1.182, "ddgs": 1.083}},
    "IN": {"name": {"zh": "印度", "en": "India", "vi": "Ấn Độ"}, "basis": {"corn": 1.394, "soybean": 1.345, "soymeal": 1.190, "ddgs": 1.083}},
    "BD": {"name": {"zh": "孟加拉", "en": "Bangladesh", "vi": "Bangladesh"}, "basis": {"corn": 1.389, "soybean": 1.343, "soymeal": 1.187, "ddgs": 1.083}},
    "ID": {"name": {"zh": "印尼", "en": "Indonesia", "vi": "Indonesia"}, "basis": {"corn": 1.369, "soybean": 1.334, "soymeal": 1.177, "ddgs": 1.083}},
    "MY": {"name": {"zh": "马来西亚", "en": "Malaysia", "vi": "Malaysia"}, "basis": {"corn": 1.360, "soybean": 1.330, "soymeal": 1.172, "ddgs": 1.083}},
    "PH": {"name": {"zh": "菲律宾", "en": "Philippines", "vi": "Philippines"}, "basis": {"corn": 1.384, "soybean": 1.341, "soymeal": 1.185, "ddgs": 1.083}},
    "NP": {"name": {"zh": "尼泊尔", "en": "Nepal", "vi": "Nepal"}, "basis": {"corn": 1.414, "soybean": 1.354, "soymeal": 1.200, "ddgs": 1.083}},
    "LK": {"name": {"zh": "斯里兰卡", "en": "Sri Lanka", "vi": "Sri Lanka"}, "basis": {"corn": 1.394, "soybean": 1.345, "soymeal": 1.190, "ddgs": 1.083}},
    "KR": {"name": {"zh": "韩国", "en": "South Korea", "vi": "Hàn Quốc"}, "basis": {"corn": 1.404, "soybean": 1.350, "soymeal": 1.195, "ddgs": 1.083}},
    "JP": {"name": {"zh": "日本", "en": "Japan", "vi": "Nhật Bản"}, "basis": {"corn": 1.399, "soybean": 1.348, "soymeal": 1.197, "ddgs": 1.083}},
    "AU": {"name": {"zh": "澳大利亚", "en": "Australia", "vi": "Úc"}, "basis": {"corn": 1.448, "soybean": 1.370, "soymeal": 1.223, "ddgs": 1.083}},
}

# 短期内存缓存：避免货币/语言切换时重复拉外网（60s TTL）
_API_CACHE = {}

# 2026-08-25 用户校准锚点：玉米/大豆/豆粕/DDGS 的 USD/吨 目标裸价。
# 因 Yahoo 实时 CBOT 与用户给出的行业参考价存在偏差，此锚点仅用于覆盖当月（2026-08）
# 的最新价格，使看板在该时点显示与用户调研一致的价格；历史月份仍使用缓存数据。
FEED_ANCHOR_202608 = {"corn": 203.0, "soybean": 446.0, "soymeal": 390.0, "ddgs": 300.0}

# ===== 2026-08-25 用户提供的真实 CNF 到岸价锚点（USD/吨，各国当月绝对价格） =====
# 这是用户经市场调研确认的到岸价（含海运费、到港基准，不含目的国进口关税/增值税/内陆运）。
# 当月（2026-08）每个国家的价格直接取此表中的绝对价，不再用系数推导。
# 键为国家代码，值为 {玉米:价, 大豆:价, 豆粕:价, DDGS:价}。CN 为中国、VN 为越南。
# 取值口径：用户表为「美湾/巴西」两列，本锚点取两者中较高者（保守到岸价）。
FEED_CNF_ANCHOR = {
    "CN": {"corn": 289.0, "soybean": 606.0, "soymeal": 470.0, "ddgs": 325.0},
    "VN": {"corn": 277.0, "soybean": 594.0, "soymeal": 458.0, "ddgs": 325.0},
    "TH": {"corn": 279.0, "soybean": 596.0, "soymeal": 460.0, "ddgs": 325.0},
    "MM": {"corn": 281.0, "soybean": 598.0, "soymeal": 462.0, "ddgs": 325.0},
    "LA": {"corn": 284.0, "soybean": 601.0, "soymeal": 465.0, "ddgs": 325.0},
    "KH": {"corn": 280.0, "soybean": 597.0, "soymeal": 461.0, "ddgs": 325.0},
    "IN": {"corn": 283.0, "soybean": 600.0, "soymeal": 464.0, "ddgs": 325.0},
    "BD": {"corn": 282.0, "soybean": 599.0, "soymeal": 463.0, "ddgs": 325.0},
    "ID": {"corn": 278.0, "soybean": 595.0, "soymeal": 459.0, "ddgs": 325.0},
    "MY": {"corn": 276.0, "soybean": 593.0, "soymeal": 457.0, "ddgs": 325.0},
    "PH": {"corn": 281.0, "soybean": 598.0, "soymeal": 462.0, "ddgs": 325.0},
    "NP": {"corn": 287.0, "soybean": 604.0, "soymeal": 468.0, "ddgs": 325.0},
    "LK": {"corn": 283.0, "soybean": 600.0, "soymeal": 464.0, "ddgs": 325.0},
    "KR": {"corn": 285.0, "soybean": 602.0, "soymeal": 466.0, "ddgs": 325.0},
    "JP": {"corn": 284.0, "soybean": 601.0, "soymeal": 467.0, "ddgs": 325.0},
    "AU": {"corn": 294.0, "soybean": 611.0, "soymeal": 477.0, "ddgs": 325.0},
}

# ===== 2026-08-25 玉米本币现货价锚点（CNY/吨，用户提供） =====
# 玉米改用「本币现货价」口径（国内大宗批发/完税到岸），单位为 CNY/吨。
# 看板 RMB 模式直接显示此值；USD/VND 模式按实时汇率换算。
# 其他品种（大豆/豆粕/DDGS）仍用 FEED_CNF_ANCHOR（USD/吨）口径。
FEED_CNY_CORN_ANCHOR = {
    "CN": 2340.0, "VN": 2130.0, "TH": 2200.0, "MM": 1950.0, "LA": 2000.0,
    "KH": 2050.0, "IN": 1700.0, "BD": 1960.0, "ID": 1778.0, "MY": 1880.0,
    "PH": 1819.0, "NP": 2120.0, "LK": 2080.0, "KR": 2150.0, "JP": 2250.0,
    "AU": 2300.0,
}

# ===== 2026-08-25 大豆本币现货价锚点（CNY/吨，用户提供） =====
# 大豆改用「本币现货价」口径（进口分销/国内大宗批发），单位为 CNY/吨。
# 看板 RMB 模式直接显示此值；USD/VND 模式按实时汇率换算。
FEED_CNY_SOYBEAN_ANCHOR = {
    "CN": 4260.0, "VN": 4380.0, "TH": 4400.0, "MM": 4300.0, "LA": 4250.0,
    "KH": 4300.0, "IN": 5600.0, "BD": 5100.0, "ID": 4420.0, "MY": 4480.0,
    "PH": 4440.0, "NP": 5350.0, "LK": 5150.0, "KR": 4600.0, "JP": 4700.0,
    "AU": 4700.0,
}

# ===== 2026-08-25 豆粕(43%蛋白)本币现货价锚点（CNY/吨，用户提供） =====
# 豆粕改用「本币现货价」口径（进口分销/国内大宗批发），单位为 CNY/吨。
FEED_CNY_SOYMEAL_ANCHOR = {
    "CN": 3140.0, "VN": 3420.0, "TH": 3440.0, "MM": 3400.0, "LA": 3500.0,
    "KH": 3520.0, "IN": 3650.0, "BD": 3650.0, "ID": 3460.0, "MY": 3480.0,
    "PH": 3500.0, "NP": 3900.0, "LK": 3800.0, "KR": 3600.0, "JP": 3680.0,
    "AU": 3850.0,
}

# ===== 2026-08-25 DDGS 本币现货价锚点（CNY/吨，用户提供） =====
# DDGS 改用「本币现货价」口径（进口分销/国产酒精厂出厂），单位为 CNY/吨。
# ============================================================
# 畜禽出栏价格（生猪/鸡蛋/白羽肉鸡）
# 数据源策略：
#   1) 国际基准：CBOT 瘦肉猪期货 (HE=F)、鸡蛋期货 (DC=F)
#   2) 国别锚点：每月公开研报/行业网站给出的国别现货价（CNY/吨，本币口径）
#   3) 历史回填：CBOT × 国别系数 + 真实锚点一次性校准（与饲料原料一致）
# ============================================================

# 单位说明：
# - 生猪出栏价：CNY/头（典型体重 110-120kg，本币结算）
# - 鸡蛋出栏价：CNY/500克（盒装；本币结算）
# - 白羽肉鸡出栏价：CNY/只（出栏均重约2.5kg；本币结算）
# 价格级别：CN/越南/泰国按公开行情；其他国家以2026-08为锚点月度均价。

# ---- 生猪出栏价（CNY/公斤，元/kg，出栏均重约 120kg）----
LIVESTOCK_CNY_PIG_ANCHOR = {
    "CN": 15.42, "VN": 22.92, "TH": 20.00, "MM": 24.17, "LA": 25.83,
    "KH": 23.33, "IN": 18.33, "BD": 21.67, "ID": 20.83, "MY": 19.17,
    "PH": 22.50, "NP": 22.08, "LK": 23.75, "KR": 17.50, "JP": 15.83,
    "AU": 17.08,
}

# ---- 鸡蛋出栏价（CNY/公斤，÷2 换算自元/500g）----
LIVESTOCK_CNY_EGG_ANCHOR = {
    "CN": 9.60, "VN": 10.40, "TH": 11.00, "MM": 12.40, "LA": 13.60,
    "KH": 13.00, "IN": 11.60, "BD": 12.20, "ID": 11.80, "MY": 10.80,
    "PH": 12.60, "NP": 12.80, "LK": 13.20, "KR": 10.20, "JP": 10.60,
    "AU": 11.40,
}

# ---- 白羽肉鸡出栏价（CNY/公斤，出栏均重 2.5kg）----
LIVESTOCK_CNY_CHICKEN_ANCHOR = {
    "CN": 8.80, "VN": 11.20, "TH": 10.40, "MM": 12.80, "LA": 14.00,
    "KH": 12.00, "IN": 10.80, "BD": 12.40, "ID": 10.40, "MY": 9.60,
    "PH": 12.00, "NP": 13.20, "LK": 13.60, "KR": 9.20, "JP": 8.40,
    "AU": 10.00,
}

# Yahoo Finance 期货符号（瘦肉猪/鸡蛋），用于历史 CBOT 相对比例
LIVESTOCK_YAHOO_SYMBOLS = {
    "pig": "HE=F",       # Lean Hogs Futures
    "egg": "DC=F",       # Eggs Futures (CME)
}

# 畜禽品种元数据（统一口径：元/公斤 = CNY/kg）
LIVESTOCK_ITEMS = {
    "pig": {
        "name": {"zh": "生猪出栏价", "en": "Pig (Live)", "vi": "Heo (xuất chuồng)"},
        "unit": {"zh": "元/公斤", "en": "CNY/kg", "vi": "CNY/kg"},
        "yahoo": "HE=F",
        "anchor": LIVESTOCK_CNY_PIG_ANCHOR,
        "unit_factor": 1.0,
        "intl_floor_cny": 14.0,
    },
    "egg": {
        "name": {"zh": "鸡蛋出栏价", "en": "Egg (Carton)", "vi": "Trứng (xuất chuồng)"},
        "unit": {"zh": "元/公斤", "en": "CNY/kg", "vi": "CNY/kg"},
        "yahoo": "DC=F",
        "anchor": LIVESTOCK_CNY_EGG_ANCHOR,
        "unit_factor": 1.0,
        "intl_floor_cny": 9.0,
    },
    "chicken": {
        "name": {"zh": "白羽肉鸡出栏价", "en": "Broiler (Live)", "vi": "Gà trắng (xuất chuồng)"},
        "unit": {"zh": "元/公斤", "en": "CNY/kg", "vi": "CNY/kg"},
        "yahoo": None,  # 暂无统一期货代码，用 pig 比例近似 + 国别锚点
        "anchor": LIVESTOCK_CNY_CHICKEN_ANCHOR,
        "unit_factor": 1.0,
        "intl_floor_cny": 8.0,
    },
}

# 畜禽国家：与 collect_livestock.py 一致
LIVESTOCK_COUNTRY_CODES = ['CN','VN','TH','PH','ID','MY','BD','IN','RU','BR']

# 国家三语名称表（供畜禽 API 返回）
LIVESTOCK_COUNTRY_NAMES = {
    "CN": {"zh": "中国", "en": "China", "vi": "Trung Quốc"},
    "VN": {"zh": "越南", "en": "Vietnam", "vi": "Việt Nam"},
    "TH": {"zh": "泰国", "en": "Thailand", "vi": "Thái Lan"},
    "PH": {"zh": "菲律宾", "en": "Philippines", "vi": "Philippines"},
    "ID": {"zh": "印尼", "en": "Indonesia", "vi": "Indonesia"},
    "MY": {"zh": "马来西亚", "en": "Malaysia", "vi": "Malaysia"},
    "BD": {"zh": "孟加拉", "en": "Bangladesh", "vi": "Bangladesh"},
    "IN": {"zh": "印度", "en": "India", "vi": "India"},
    "RU": {"zh": "俄罗斯", "en": "Russia", "vi": "Nga"},
    "BR": {"zh": "巴西", "en": "Brazil", "vi": "Brazil"},
}

# 畜禽与饲料共享：pig ~ pig futures, egg ~ egg futures, chicken 用 pig 作近似波动源
LIVESTOCK_PROXY_SYMBOL = {
    "pig": "HE=F",
    "egg": "DC=F",
    "chicken": "HE=F",  # 肉鸡波动与瘦肉猪高相关；用 pig 比例近似
}

# ============================================================

# ============================================================
# 畜禽真实数据（仅中越两国）
# ------------------------------------------------------------
# 数据直接来自 collect_livestock.py 产出的真实表：
#   livestock_farmgate（出栏价 USD/kg）、livestock_retail（终端零售 USD/kg）
# 抓取源：CN=行情宝(生猪)/博亚和讯(鸡蛋·肉鸡)；VN=GREENFEED(每周)/agro.gov.vn 兜底。
# 其余国家（JP/KR/AU/TH/...）数据已移除，待新思路另行接入。
# ============================================================

# ---- DB 固化历史表 ----
# ---- 畜禽数据统一读取：直接复用 collect_livestock.py 产出的真实表 ----
# 仅中越两国（LIVESTOCK_COUNTRY_CODES=['CN','VN']），数据来自：
#   livestock_farmgate（出栏价 USD/kg，真实抓取：CN=行情宝/博亚和讯，VN=GREENFEED/agro.gov.vn）
#   livestock_retail（终端零售 USD/kg）
# 不再维护独立的 livestock_history / CBOT 形态 / FAOSTAT / NECC / MAFF / MLA 等重复体系。


def _livestock_write_month(conn, item, country, ym, price_usd, source="manual"):
    """手动补数：写入 livestock_retail 作为 collected 源，供 collect_livestock 后续纳入。"""
    conn.execute("""CREATE TABLE IF NOT EXISTS livestock_retail (
        item TEXT, country TEXT, ym TEXT,
        price_usd REAL, source_name TEXT, source_url TEXT,
        method TEXT, unit TEXT, note TEXT,
        PRIMARY KEY(item, country, ym))""")
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute("""INSERT OR REPLACE INTO livestock_retail
      (item,country,ym,price_usd,source_name,source_url,method,unit,note) VALUES(?,?,?,?,?,?,?,?,?)""",
      (item, country, ym, round(price_usd, 4), "manual:%s" % source, "", "manual", "kg", ts))
    conn.commit()


# ---- 主构建函数：直接读取真实表 ----
def _livestock_real_build_data(conn, cur):
    # 读取 collect_livestock.py 产出的真实表（USD/kg）。优先 farmgate，缺失回退 retail。
    fg = {}; rt = {}
    for item, cc, ym, usd in conn.execute(
        "SELECT item,country,ym,price_usd FROM livestock_farmgate WHERE price_usd IS NOT NULL").fetchall():
        fg.setdefault(item, {}).setdefault(cc, {})[ym] = float(usd)
    for item, cc, ym, usd in conn.execute(
        "SELECT item,country,ym,price_usd FROM livestock_retail WHERE price_usd IS NOT NULL").fetchall():
        rt.setdefault(item, {}).setdefault(cc, {})[ym] = float(usd)

    all_ym = set()
    for d in (fg, rt):
        for itd in d.values():
            for ccd in itd.values(): all_ym.update(ccd.keys())
    labels = sorted(all_ym) if all_ym else ["2026-08"]

    # 历史+当月 100% 读 SQLite 固化汇率缓存（秒开）；当月缺失后台补抓
    fx = _fx_load_cache(conn)
    now_ym = datetime.now().strftime("%Y-%m")
    if not _month_has_data(fx, FX_SYMBOLS.keys(), now_ym):
        _kick_market_warm()
    def _bidir_fill(src, labs):
        f = _forward_fill(src, labs); last = None
        for i in range(len(f)-1,-1,-1):
            if f[i] is not None: last = f[i]
            elif last is not None: f[i] = last
        return f
    usdcny = _bidir_fill(fx.get("USDCNY",{}), labels)
    usdvnd = _bidir_fill(fx.get("USDVND",{}), labels)

    # 真实数据已是 USD/kg；内部先换算为 CNY/kg 再按 cur 输出，复用既有转换逻辑
    def _usd_to_target(usd_v, idx):
        if usd_v is None: return None
        cf = usdcny[idx] if idx < len(usdcny) and usdcny[idx] else 7.1
        cny_v = usd_v * cf
        if cur == "RMB": return round(cny_v, 2)
        if cur == "USD": return round(usd_v, 2)
        if cur == "VND":
            vf = usdvnd[idx] if idx < len(usdvnd) and usdvnd[idx] else 23000.0
            return round(usd_v * vf, 2)
        return round(cny_v, 2)

    series = {}
    for item in LIVESTOCK_ITEMS:
        series[item] = {}
        for cc in LIVESTOCK_COUNTRY_CODES:
            idata = fg.get(item, {}).get(cc) or rt.get(item, {}).get(cc) or {}
            arr = [round(_usd_to_target(idata.get(ym), j), 2) if idata.get(ym) is not None else None
                   for j, ym in enumerate(labels)]
            series[item][cc] = arr
    return {"labels": labels, "series": series}



@app.route("/api/livestock-prices")
def api_livestock_prices():
    """畜禽出栏价 API：16国 × 3品种，月度，5年历史；按 cur 切换 RMB/USD/VND。"""
    cur = (request.args.get("cur") or "RMB").upper()
    if cur not in ("USD", "RMB", "VND"):
        cur = "RMB"
    cache_key = "livestock_" + cur
    cached = _API_CACHE.get(cache_key)
    if cached and (time.time() - cached[0] < 60):
        return jsonify(cached[1])
    conn = get_db()
    try:
        # 真实数据源：历史固化 + 自动更新（新数据优先，缺失月份用锚点+CBOT 补充）
        raw = _livestock_real_build_data(conn, cur)
    finally:
        conn.close()

    labels = raw["labels"]
    series = raw["series"]

    # 展平为 {_monthly_avg 期望的格式: {flat_key: [list]}}
    flat_series = {}
    key_map = []  # [(flat_key, item, ccode)]
    for item in series:
        for ccode in series[item]:
            fk = item + "|" + ccode
            flat_series[fk] = series[item][ccode]
            key_map.append((fk, item, ccode))

    # 月度聚合
    monthly_labels, monthly_flat = _monthly_avg(labels, flat_series)

    # 2026-08 校准：用当月最后一天的每日真实价直接覆盖月度均值
    # 这样保证"锚点月"显示 = 锚点真实价，避免月度聚合把中旬数据拉低
    if monthly_labels and monthly_labels[-1] == "2026-08" and raw.get("labels"):
        last_day_label = raw["labels"][-1]
        if last_day_label[:7] == "2026-08":
            for fk, item, ccode in key_map:
                daily_arr = raw["series"].get(item, {}).get(ccode, [])
                if daily_arr:
                    monthly_flat[fk][-1] = daily_arr[-1]

    # 跨品种统一波峰波谷降采样（与饲料一致）
    pv_labels, pv_flat = _peak_valley(monthly_labels, monthly_flat)

    pv_series = {it: {} for it in series}
    for fk, item, ccode in key_map:
        pv_series[item][ccode] = pv_flat.get(fk, [])

    resp = {
        "ok": True,
        "cur": cur,
        "labels": pv_labels,
        "series": pv_series,
        "data_source": "real_anchor_cbot_shape",  # 真实国别锚点 × 国际真实价格形态(CBOT)；非CPI推演
        "items": {
            k: {
                "name": v["name"],
                "unit": v["unit"],
                "anchor_month": "2026-08",
            }
            for k, v in LIVESTOCK_ITEMS.items()
        },
        "countries": {
            code: {"name": LIVESTOCK_COUNTRY_NAMES.get(code, {"zh": code, "en": code, "vi": code})}
            for code in LIVESTOCK_COUNTRY_CODES
        },
    }
    obj = jsonify(resp)
    obj.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    obj.headers["Pragma"] = "no-cache"
    _API_CACHE[cache_key] = (time.time(), resp)
    return obj


@app.route("/api/livestock-farmgate")
def api_livestock_farmgate():
    """畜禽出栏价（真实采集 + 断点补全）API。
    数据来自 collect_livestock.py 写入的 livestock_farmgate 表：
      - 单位 USD/kg（按 cur 可切 RMB/VND）
      - 每月第一天的值；method 标注 collected(真实/FAO/锚点种子)/gap_fill/anchor
      - formula 记录每个值的推算逻辑；source_url 记录数据源
    混合模式：英文API国家(CN/VN优先出栏价; JP/KR/AU/FAOSTAT)自动拉真实值，
              其余国家由用户手动补（见 livestock_retail_seed.csv）。
    """
    cur = (request.args.get("cur") or "USD").upper()
    if cur not in ("USD", "RMB", "VND"):
        cur = "USD"
    items = ["pig", "egg", "chicken"]
    countries = LIVESTOCK_COUNTRY_CODES
    conn = get_db()
    # FX 因子（USD -> target），按月首日
    fx = _fx_build_data(conn)
    # 直接用每日序列取每月首日的因子
    def factor_for(ym):
        # ym: YYYY-MM；取该月第一天对应因子
        day = ym + "-01"
        if cur == "USD":
            return 1.0
        src = fx.get("USDCNY" if cur == "RMB" else "USDVND", {})
        # 前向找最近因子
        import datetime as _dt
        y, m = int(ym[:4]), int(ym[5:7])
        for _ in range(0, 400):
            key = "%04d-%02d-%02d" % (y, m, 1)
            if key in src and src[key]:
                return float(src[key])
            # 前推一天
            d = _dt.date(y, m, 1)
            d = d - _dt.timedelta(days=1)
            y, m = d.year, d.month
        return 1.0

    labels = []
    # 取全量月份范围（2021-01 ~ 2026-08）
    rows = conn.execute("SELECT DISTINCT ym FROM livestock_farmgate ORDER BY ym").fetchall()
    labels = [r[0] for r in rows]

    series = {it: {} for it in items}
    meta = {it: {} for it in items}  # 记录每个 country 的 method 分布/来源
    for it in items:
        for cc in countries:
            fg = conn.execute(
                "SELECT ym,price_usd,method,formula,source_url FROM livestock_farmgate "
                "WHERE item=? AND country=? ORDER BY ym", (it, cc)).fetchall()
            arr = []
            for ym, usd, method, formula, surl in fg:
                if usd is None:
                    arr.append(None)
                    continue
                f = factor_for(ym)
                arr.append(round(usd * f, 4))
            series[it][cc] = arr
            # 来源与口径
            first = conn.execute(
                "SELECT source_url,method FROM livestock_farmgate "
                "WHERE item=? AND country=? AND price_usd IS NOT NULL ORDER BY ym LIMIT 1",
                (it, cc)).fetchone()
            meta[it][cc] = {
                "source_url": first[0] if first else "",
                "method": first[1] if first else "anchor",
                "unit": "USD/kg" if cur == "USD" else ("CNY/kg" if cur == "RMB" else "VND/kg"),
            }

    resp = {
        "ok": True,
        "cur": cur,
        "labels": labels,
        "series": series,
        "meta": meta,
        "markup": {"pig": 0.40, "egg": 0.30, "chicken": 0.35},
        "items": {
            k: {"name": v["name"], "unit": v["unit"], "anchor_month": "2026-08"}
            for k, v in LIVESTOCK_ITEMS.items()
        },
        "countries": {
            code: {"name": LIVESTOCK_COUNTRY_NAMES.get(code, {"zh": code, "en": code, "vi": code})}
            for code in countries
        },
        "data_source": "real_retail_backout_or_direct + gap_fill (collect_livestock.py)",
    }
    conn.close()
    return jsonify(resp)


@app.route("/api/livestock-retail-raw")
def api_livestock_retail_raw():
    """返回 collect_livestock 采集到的零售/市场原始价（含 manual_needed 待补）"""
    conn = get_db()
    rows = conn.execute(
        "SELECT item,country,ym,price_usd,unit,source_name,source_url,note "
        "FROM livestock_retail ORDER BY item,country,ym").fetchall()
    out = [dict(item=r[0], country=r[1], ym=r[2], price_usd=r[3], unit=r[4],
                source_name=r[5], source_url=r[6], note=r[7]) for r in rows]
    conn.close()
    return jsonify({"ok": True, "count": len(out), "rows": out})


@app.route('/api/livestock-ingest', methods=['POST'])
def api_livestock_ingest():
    """录入真实畜禽价格（手动数据优先于锚点+CBOT）。
    请求体 JSON：
      [{"item":"pig","country":"VN","year_month":"2026-08","price_cny":22.92,"source":"越南畜牧协会"},
       ...]
    或单次：
      {"item":"pig","country":"VN","year_month":"2026-08","price_cny":22.92,"source":"..."}
    价格单位固定：元/公斤 (CNY/kg)。"""
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"ok": False, "error": "invalid json"}), 400
    if isinstance(data, dict):
        data = [data]
    valid_items = set(LIVESTOCK_ITEMS.keys())
    valid_cc = set(LIVESTOCK_COUNTRY_CODES)
    conn = get_db()
    try:
        inserted = 0
        skipped = 0
        for row in data:
            item = str(row.get("item", "")).strip().lower()
            cc = str(row.get("country", "")).strip().upper()
            ym = str(row.get("year_month", "")).strip()
            pc = row.get("price_cny")
            src = str(row.get("source", "manual")).strip() or "manual"
            if item not in valid_items or cc not in valid_cc:
                skipped += 1
                continue
            if not (len(ym) == 7 and ym[4] == "-"):
                skipped += 1
                continue
            try:
                price = float(pc)
            except Exception:
                skipped += 1
                continue
            _livestock_write_month(conn, item, cc, ym, price, source="manual:%s" % src)
            inserted += 1
    finally:
        conn.close()
    # 清除缓存，让下次请求立即生效
    _API_CACHE.pop("livestock_RMB", None)
    _API_CACHE.pop("livestock_USD", None)
    _API_CACHE.pop("livestock_VND", None)
    return jsonify({"ok": True, "inserted": inserted, "skipped": skipped})

FEED_CNY_DDGS_ANCHOR = {
    "CN": 2200.0, "VN": 2480.0, "TH": 2500.0, "MM": 2450.0, "LA": 2550.0,
    "KH": 2580.0, "IN": 2400.0, "BD": 2500.0, "ID": 2500.0, "MY": 2520.0,
    "PH": 2540.0, "NP": 2850.0, "LK": 2750.0, "KR": 2620.0, "JP": 2680.0,
    "AU": 2800.0,
}

def _metal_cache_table(conn):
    conn.execute("""CREATE TABLE IF NOT EXISTS metal_cache (
        symbol TEXT, date TEXT, close REAL,
        PRIMARY KEY(symbol, date))""")
    conn.commit()

def _metal_load_cache(conn):
    """读取本地缓存：{symbol: {date: close_usd}}。"""
    _metal_cache_table(conn)
    cur = conn.execute("SELECT symbol, date, close FROM metal_cache")
    out = {}
    for sym, d, c in cur.fetchall():
        out.setdefault(sym, {})[d] = c
    return out

def _metal_save_cache(conn, data):
    """data: {symbol: {date: close_usd}}。"""
    _metal_cache_table(conn)
    rows = []
    for sym, m in data.items():
        for d, c in m.items():
            rows.append((sym, d, c))
    if rows:
        conn.executemany("INSERT OR REPLACE INTO metal_cache(symbol, date, close) VALUES(?,?,?)", rows)
        conn.commit()

def _fx_cache_table(conn):
    conn.execute("""CREATE TABLE IF NOT EXISTS fx_cache (
        pair TEXT, date TEXT, rate REAL,
        PRIMARY KEY(pair, date))""")
    conn.commit()

def _fx_load_cache(conn):
    _fx_cache_table(conn)
    cur = conn.execute("SELECT pair, date, rate FROM fx_cache")
    out = {}
    for pair, d, r in cur.fetchall():
        out.setdefault(pair, {})[d] = r
    return out

def _fx_save_cache(conn, data):
    _fx_cache_table(conn)
    rows = []
    for pair, m in data.items():
        for d, r in m.items():
            rows.append((pair, d, r))
    if rows:
        conn.executemany("INSERT OR REPLACE INTO fx_cache(pair, date, rate) VALUES(?,?,?)", rows)
        conn.commit()

def _month_period(ym):
    """返回某月(YYYY-MM)首日到次月首日前一秒的 unix 时间戳，用于雅虎按月拉取。"""
    y, m = int(ym[:4]), int(ym[5:7])
    first = datetime(y, m, 1)
    if m == 12:
        nxt = datetime(y + 1, 1, 1)
    else:
        nxt = datetime(y, m + 1, 1)
    period1 = int(first.timestamp())
    period2 = int(nxt.timestamp()) - 1
    return period1, period2

def _metal_fetch_yahoo(symbol, period1, period2):
    """从雅虎财经拉取日线收盘价，返回 {date: close_usd}。失败返回 {}。"""
    url = ("https://query1.finance.yahoo.com/v8/finance/chart/%s"
           "?period1=%d&period2=%d&interval=1d" % (urllib.parse.quote(symbol), period1, period2))
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            js = json.loads(resp.read().decode("utf-8"))
        res = js.get("chart", {}).get("result")
        if not res:
            return {}
        closes = res[0].get("indicators", {}).get("quote", [{}])[0].get("close", [])
        ts = res[0].get("timestamp", [])
        out = {}
        for t, c in zip(ts, closes):
            if c is None:
                continue
            d = datetime.utcfromtimestamp(t).strftime("%Y-%m-%d")
            out[d] = float(c)
        return out
    except Exception as e:
        print("[metal] fetch %s failed: %s" % (symbol, e))
        return {}

def _fx_fetch_yahoo(symbol, period1, period2):
    """从雅虎财经拉取日线汇率，返回 {date: rate}。失败返回 {}。"""
    return _metal_fetch_yahoo(symbol, period1, period2)

def _imf_extract_obs(obj):
    """递归提取 IMF SDMX JSON 中的 Obs {time, value} 列表。"""
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            key = k.lstrip("@").upper()
            if key in ("OBS", "OBSERVATIONS") and isinstance(v, list):
                for item in v:
                    if not isinstance(item, dict):
                        continue
                    tp = item.get("@TIME_PERIOD") or item.get("TIME_PERIOD")
                    ov = item.get("@OBS_VALUE") or item.get("OBS_VALUE")
                    if tp and ov is not None:
                        try:
                            out.append({"time": str(tp), "value": float(ov)})
                        except Exception:
                            pass
            else:
                out.extend(_imf_extract_obs(v))
    elif isinstance(obj, list):
        for v in obj:
            out.extend(_imf_extract_obs(v))
    return out

def _metal_fetch_imf_pcps(key, p1, p2):
    """从 IMF PCPS 拉取某商品的月度实际市场价格，返回 {YYYY-MM-DD: close_usd}。
    仅处理 METAL_OFFICIAL_CODES 中配置的品种；失败返回 {}。"""
    code = METAL_OFFICIAL_CODES.get(key)
    if not code:
        return {}
    start = datetime.utcfromtimestamp(p1).strftime("%Y-%m")
    end = datetime.utcfromtimestamp(p2).strftime("%Y-%m")
    url = ("https://dataservices.imf.org/REST/SDMX_JSON.svc/DataStream/PCPS/%s"
           "?startPeriod=%s&endPeriod=%s" % (urllib.parse.quote(code), start, end))
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            js = json.loads(resp.read().decode("utf-8"))
        obs = _imf_extract_obs(js)
        out = {}
        for ob in obs:
            ym = ob.get("time", "")
            if len(ym) >= 7 and ym[4] == "-":
                # 统一存为每月1号，与缓存中日线格式对齐
                out[ym[:7] + "-01"] = ob["value"]
        if out:
            print("[metal] IMF PCPS %s -> %s 条 (ex %s..%s)" % (key, len(out), start, end))
        return out
    except Exception as e:
        print("[metal] IMF PCPS %s failed: %s" % (key, e))
        return {}

# 历史固化状态：记录已处理过的"当前月"，用于跨月时对刚过去月做一次性补拉。
# 进程级变量；服务器重启后通过缓存中最新的月份推断，避免冷启动全量重拉。
_LAST_FILL_MONTH = None

def _prev_month_ym(ym):
    y, m = int(ym[:4]), int(ym[5:7])
    if m == 1:
        return "%04d-12" % (y - 1)
    return "%04d-%02d" % (y, m - 1)

def _ensure_prev_month_filled(conn, fetch_fn, keys, cache, cur_ym, save_fn):
    """跨月补拉：当当前月从 last_month 切换到 cur_ym 时，对刚过去的 last_month 整月补拉固化。
    历史月（非当前月）100% 读缓存，绝不外网；仅此处在跨月边界补拉一次。"""
    global _LAST_FILL_MONTH
    if _LAST_FILL_MONTH is None:
        # 冷启动：从缓存推断最近有数据的月份作为起点，不补拉历史
        latest = None
        for k in keys:
            m = cache.get(k, {})
            if m:
                cand = max(m.keys())[:7]
                if latest is None or cand > latest:
                    latest = cand
        _LAST_FILL_MONTH = latest or cur_ym
    if _LAST_FILL_MONTH != cur_ym:
        prev = _prev_month_ym(cur_ym)
        if _LAST_FILL_MONTH != prev and _LAST_FILL_MONTH < cur_ym:
            # 对刚过去的整月补拉并固化（仅此一次）
            p1, p2 = _month_period(prev)
            for key in keys:
                sym = keys[key]
                fresh = fetch_fn(sym, p1, p2)
                if fresh:
                    if key not in cache:
                        cache[key] = {}
                    cache[key].update(fresh)
            save_fn(conn, cache)
        _LAST_FILL_MONTH = cur_ym

def _month_has_data(cache, keys, cur_ym):
    """检查缓存中当前月(YYYY-MM)的数据是否完整。所有 key 都有当月数据才视为已采集；
    任一 key 缺失即触发补抓，避免某些币种已更新而另一些仍停留在上月。"""
    for k in keys:
        m = cache.get(k, {})
        if not any(d.startswith(cur_ym) for d in m.keys()):
            return False
    return True

# ⛔⛔⛔ 锁死：_metal_clean_outliers 是 2026-09-04 修复锌价脏数据（单日 ~108 而邻日真实价 ~2297/3950）
# 后新增的离群点守卫，是"防止脏数据再次进入金属图表"的唯一防线。禁止删除或弱化
# （如放宽 50% 阈值、或在调用点跳过它）。若数据源整体更换，必须保留等价守卫。
def _metal_clean_outliers(symbol, existing, fresh):
    """剔除数据源偶发离群点（如锌曾出现单日 ~108，而邻日真实价 ~2297/3950——
    疑为数据源返回了错误单位/拆分价）。规则：若某日值同时偏离其前后最近有效邻居
    >50%，则丢弃该点（不写入缓存，由前向填充沿用邻日真实值）。"""
    if not fresh:
        return fresh
    combined = dict(existing or {})
    combined.update(fresh)
    cdates = sorted(combined.keys())
    idx_of = {d: i for i, d in enumerate(cdates)}
    out = {}
    for d, v in fresh.items():
        if v is None:
            continue
        i = idx_of[d]
        prev_v = next((combined[cdates[j]] for j in range(i - 1, -1, -1)
                       if combined[cdates[j]] is not None), None)
        nxt_v = next((combined[cdates[j]] for j in range(i + 1, len(cdates))
                      if combined[cdates[j]] is not None), None)
        if prev_v and nxt_v and prev_v > 0 and nxt_v > 0:
            lo, hi = min(prev_v, nxt_v), max(prev_v, nxt_v)
            if v < lo * 0.5 or v > hi * 1.5:
                continue  # 离群，丢弃
        out[d] = v
    return out

def _metal_build_data(conn):
    """金属价格构建（USD 基准）：历史月 + 当月均只采集一次，采集后固化，本月内不再外网。
    每月第一天：当月缓存为空 → 自动拉取一次 → 固化 → 本月后续请求 100% 读缓存。
    跨月时：旧月已是上月底数据，自然成为历史；新月触发首次采集。
    2026-09-04 新增：优先使用 IMF PCPS 官方月度实际价（iron/zinc），回退 Yahoo。
    2026-09-04 新增：拉取后做离群点剔除（_metal_clean_outliers），避免脏数据入缓存。"""
    cache = _metal_load_cache(conn)
    now = datetime.now()
    cur_ym = now.strftime("%Y-%m")
    # 对官方数据源：若缓存完全为空，先一次性回填完整历史（2015-今）
    history_backfilled = False
    for key in METAL_OFFICIAL_CODES:
        if not cache.get(key):
            p1 = int(datetime(2015, 1, 1).timestamp())
            p2 = int(now.timestamp())
            fresh = _metal_fetch_imf_pcps(key, p1, p2)
            if fresh:
                fresh = _metal_clean_outliers(key, cache.get(key, {}), fresh)
                cache[key] = fresh
                history_backfilled = True
    if history_backfilled:
        _metal_save_cache(conn, cache)
    # 跨月补拉刚过去的月（固化，仅此一次）
    _ensure_prev_month_filled(conn, _metal_fetch_yahoo, METAL_SYMBOLS, cache, cur_ym, _metal_save_cache)
    # 当月：仅在缓存无当月数据时拉取一次（每月第一天 / 首次请求触发），采集后固化，本月不再拉外网
    if not _month_has_data(cache, METAL_SYMBOLS.keys(), cur_ym):
        p1, p2 = _month_period(cur_ym)
        p2 = int(now.timestamp())
        fresh_any = False
        for key, sym in METAL_SYMBOLS.items():
            fresh = _metal_fetch_imf_pcps(key, p1, p2)
            if not fresh:
                fresh = _metal_fetch_yahoo(sym, p1, p2)
            if fresh:
                fresh = _metal_clean_outliers(key, cache.get(key, {}), fresh)
                fresh_any = True
                if key not in cache:
                    cache[key] = {}
                cache[key].update(fresh)
        if fresh_any:
            _metal_save_cache(conn, cache)
    return cache

def _fx_build_data(conn):
    """真实历史汇率构建：历史月 + 当月均只采集一次，采集后固化，本月内不再外网。
    每月第一天自动拉取一次；跨月时旧月自然成为历史，新月触发首次采集。"""
    cache = _fx_load_cache(conn)
    now = datetime.now()
    cur_ym = now.strftime("%Y-%m")
    _ensure_prev_month_filled(conn, _fx_fetch_yahoo, FX_SYMBOLS, cache, cur_ym, _fx_save_cache)
    # 当月：仅在缓存无当月数据时拉取一次
    if not _month_has_data(cache, FX_SYMBOLS.keys(), cur_ym):
        p1, p2 = _month_period(cur_ym)
        p2 = int(now.timestamp())
        fresh_any = False
        for key, sym in FX_SYMBOLS.items():
            fresh = _fx_fetch_yahoo(sym, p1, p2)
            if fresh:
                fresh_any = True
                if key not in cache:
                    cache[key] = {}
                cache[key].update(fresh)
        if fresh_any:
            _fx_save_cache(conn, cache)
    return cache


# ---- 后台预热：当月数据缺失时异步补抓，接口请求不再阻塞等待外网 ----
import threading as _threading
_MARKET_WARM_LOCK = _threading.Lock()
_MARKET_WARM_RUNNING = False
_MARKET_LAST_WARM = 0.0

def _kick_market_warm():
    """feed/metal/fx 任一当月数据缺失时，后台线程补抓一次（固化进 SQLite）。
    请求路径 100% 读缓存 → 页面秒开；补抓完成清内存缓存，下次请求即含当月。"""
    global _MARKET_WARM_RUNNING, _MARKET_LAST_WARM
    now = time.time()
    if _MARKET_WARM_RUNNING or (now - _MARKET_LAST_WARM) < 120:
        return
    _MARKET_LAST_WARM = now
    with _MARKET_WARM_LOCK:
        if _MARKET_WARM_RUNNING:
            return
        _MARKET_WARM_RUNNING = True

    def _worker():
        global _MARKET_WARM_RUNNING
        try:
            conn = get_db()
            try:
                _fx_build_data(conn)
                _feed_build_data(conn)
                _metal_build_data(conn)
            finally:
                conn.close()
            # 抓到新数据后清 60s 内存缓存，让下次请求立刻带上当月
            for k in list(_API_CACHE.keys()):
                if k.startswith(("feed_", "metal_", "livestock_", "fx")):
                    _API_CACHE.pop(k, None)
            print("[warm] market current-month data refreshed in background")
        except Exception as e:
            print("[warm] background refresh failed:", e)
        finally:
            _MARKET_WARM_RUNNING = False

    _threading.Thread(target=_worker, daemon=True).start()

def _forward_fill(m, labels):
    """对缺失日期前向填充，返回与 labels 等长的数组。"""
    last = None
    arr = []
    for d in labels:
        v = m.get(d)
        if v is not None:
            last = v
        arr.append(last)
    return arr

def _monthly_avg(labels, series):
    """将日线数据按自然月聚合为月度平均值。
    labels: ['YYYY-MM-DD', ...]; series: {key: [值...]}
    返回 (month_labels, month_series)，month_labels 为 'YYYY-MM'。"""
    buckets = {}
    for i, d in enumerate(labels):
        if len(d) < 7:
            continue
        ym = d[:7]
        if ym not in buckets:
            buckets[ym] = {}
        for k, arr in series.items():
            if i < len(arr) and arr[i] is not None:
                buckets[ym].setdefault(k, []).append(arr[i])
    month_labels = sorted(buckets.keys())
    month_series = {}
    for k in series.keys():
        month_series[k] = []
    for ym in month_labels:
        for k in series.keys():
            vals = buckets[ym].get(k)
            if vals:
                month_series[k].append(round(sum(vals) / len(vals), 2))
            else:
                month_series[k].append(None)
    return month_labels, month_series

def _peak_valley(labels, series):
    """对已聚合的序列提取波峰+波谷关键点（含首尾），降低渲染密集度。
    关键修复：所有序列共享同一套索引(keep)，保证 labels 与每条 series 长度严格一致。
    labels: ['YYYY-MM', ...]; series: {key: [值或None...]}
    返回 (pv_labels, pv_series)，pv_labels 与每个 pv_series[key] 长度相同。"""
    n = len(labels)
    if n <= 12:
        return labels, series  # 点数少则不降采样
    keep = set([0, n - 1])  # 首尾必留
    # 跨所有序列收集极值点索引（取并集），确保所有序列使用同一套索引
    for k, arr in series.items():
        prev_val = None
        direction = 0  # 1=上升中, -1=下降中
        for i in range(1, n - 1):
            v = arr[i]
            if v is None:
                continue
            if prev_val is None:
                prev_val = v
                continue
            if v > prev_val:
                new_dir = 1
            elif v < prev_val:
                new_dir = -1
            else:
                new_dir = direction
            # 方向转变处 = 极值点（波峰或波谷）
            if direction != 0 and new_dir != 0 and new_dir != direction:
                keep.add(i)
            direction = new_dir
            prev_val = v
    idx = sorted(keep)
    pv_labels = [labels[i] for i in idx]
    pv_series = {}
    for k in series.keys():
        pv_series[k] = [series[k][i] for i in idx]
    # 安全检查：确保长度一致
    for k in pv_series:
        assert len(pv_series[k]) == len(pv_labels), f"pv_series[{k}] length {len(pv_series[k])} != pv_labels {len(pv_labels)}"
    return pv_labels, pv_series

# ===================== 锌锭历史冻结覆盖（2026-09-06）=====================
# 用户提供的 SMM 0# 锌锭月度均价（元/吨，2020-12~2026-08），套算 USD/VND 后锁死。
# 看板/价格走势对 zinc 的 <=cutoff 月份【直接读取 zinc_frozen.json】，不走实时换算管线；
# cutoff 之后（2026-09+）仍由实时管线（IMF/Yahoo + 真实汇率）续接，互不干扰。
# 此为历史数据锁死层，独立于下方⛔金属管线核心常量（METAL_SYMBOLS 等），不改动它们。
import json as _json
_ZINC_FROZEN = None
def _load_zinc_frozen():
    global _ZINC_FROZEN
    if _ZINC_FROZEN is not None:
        return _ZINC_FROZEN
    p = os.path.join(BASE_DIR, "zinc_frozen.json")
    if os.path.exists(p):
        try:
            with open(p, "r", encoding="utf-8") as f:
                _ZINC_FROZEN = _json.load(f)
        except Exception as e:
            print("[zinc_frozen] load failed:", e)
            _ZINC_FROZEN = False
    else:
        _ZINC_FROZEN = False
    return _ZINC_FROZEN

def _apply_zinc_frozen(month_labels, month_series, cur):
    """用冻结历史数据覆盖 zinc 的 <=cutoff 月份（按当前币种 cur）。"""
    frozen = _load_zinc_frozen()
    if not frozen or "zinc" not in month_series:
        return
    key = {"USD": "usd", "RMB": "rmb", "VND": "vnd"}.get(cur)
    if not key or key not in frozen:
        return
    cutoff = frozen.get("cutoff_month", "2026-08")
    mmap = {}
    for ym, v in zip(frozen.get("months", []), frozen.get(key, [])):
        mmap[ym] = v
    arr = month_series["zinc"]
    for i, ym in enumerate(month_labels):
        if ym <= cutoff and ym in mmap:
            arr[i] = mmap[ym]

@app.route("/api/metal-prices")
def api_metal_prices():
    cur = (request.args.get("cur") or "USD").upper()
    if cur not in ("USD", "RMB", "VND"):
        cur = "USD"
    # 短期内存缓存（60s）：货币切换时避免重复拉 Yahoo
    cache_key = "metal_" + cur
    cached = _API_CACHE.get(cache_key)
    if cached and (time.time() - cached[0] < 60):
        return jsonify(cached[1])
    conn = get_db()
    try:
        # 缓存直读（秒开）；当月缺失后台补抓
        raw = _metal_load_cache(conn)
        fx = _fx_load_cache(conn)
        now_ym = datetime.now().strftime("%Y-%m")
        if not (_month_has_data(raw, METAL_SYMBOLS.keys(), now_ym)
                and _month_has_data(fx, FX_SYMBOLS.keys(), now_ym)):
            _kick_market_warm()
    finally:
        conn.close()
    # 统一 labels（所有品种日期并集，升序）
    all_dates = set()
    for m in raw.values():
        all_dates.update(m.keys())
    labels = sorted(all_dates)
    # 真实历史汇率序列（前向填充）
    usdcny = _forward_fill(fx.get("USDCNY", {}), labels)
    usdvnd = _forward_fill(fx.get("USDVND", {}), labels)
    # 每日换算系数（USD -> 目标币种）
    if cur == "USD":
        conv = [1.0] * len(labels)
    elif cur == "RMB":
        conv = [r if r else 1.0 for r in usdcny]   # USD->CNY
    else:  # VND
        conv = [r if r else 1.0 for r in usdvnd]   # USD->VND
    series = {}
    for key, m in raw.items():
        factor = METAL_TO_TON_FACTOR.get(key, 1.0)
        base = _forward_fill(m, labels)
        arr = []
        for i, d in enumerate(labels):
            v = base[i]
            if v is None:
                arr.append(None)
            else:
                # 先按品种系数换算为 USD/吨（原始单位 -> 标准单位）
                usd_per_ton = v * factor
                # 再按真实历史汇率换算为目标币种 / 吨
                arr.append(round(usd_per_ton * (conv[i] or 1.0), 2))
        series[key] = arr
    # 聚合为月度平均，再提取波峰波谷关键点，降低渲染密集度
    month_labels, month_series = _monthly_avg(labels, series)
    # 锌锭历史冻结覆盖：<=cutoff 月份直接调用锁死数据（2026-09-06）
    _apply_zinc_frozen(month_labels, month_series, cur)
    pv_labels, pv_series = _peak_valley(month_labels, month_series)
    resp = {
        "ok": True,
        "cur": cur,
        "labels": pv_labels,
        "series": pv_series,
        "symbols": {k: METAL_SYMBOLS[k] for k in METAL_SYMBOLS},
        "raw_units": METAL_RAW_UNIT
    }
    _API_CACHE["metal_" + cur] = (time.time(), resp)
    return jsonify(resp)

# ===================== 饲料原料缓存与构建 =====================
def _feed_cache_table(conn):
    conn.execute("""CREATE TABLE IF NOT EXISTS feed_cache (
        symbol TEXT, date TEXT, close REAL,
        PRIMARY KEY(symbol, date))""")
    conn.commit()

def _feed_load_cache(conn):
    _feed_cache_table(conn)
    cur = conn.execute("SELECT symbol, date, close FROM feed_cache")
    out = {}
    for sym, d, c in cur.fetchall():
        out.setdefault(sym, {})[d] = c
    return out

def _feed_save_cache(conn, data):
    _feed_cache_table(conn)
    rows = []
    for sym, m in data.items():
        for d, c in m.items():
            rows.append((sym, d, c))
    if rows:
        conn.executemany("INSERT OR REPLACE INTO feed_cache(symbol, date, close) VALUES(?,?,?)", rows)
        conn.commit()

def _feed_build_data(conn):
    """饲料原料构建（USD 基准）：历史月 + 当月均只采集一次，采集后固化，本月内不再外网。
    每月第一天自动拉取一次；跨月时旧月自然成为历史，新月触发首次采集。"""
    cache = _feed_load_cache(conn)
    now = datetime.now()
    cur_ym = now.strftime("%Y-%m")
    feed_syms = {k: v["sym"] for k, v in FEED_ITEMS.items()}
    _ensure_prev_month_filled(conn, _metal_fetch_yahoo, feed_syms, cache, cur_ym, _feed_save_cache)
    # 当月：仅在缓存无当月数据时拉取一次
    if not _month_has_data(cache, feed_syms.keys(), cur_ym):
        p1, p2 = _month_period(cur_ym)
        p2 = int(now.timestamp())
        fresh_any = False
        for key, cfg in FEED_ITEMS.items():
            sym = cfg["sym"]
            fresh = _metal_fetch_yahoo(sym, p1, p2)
            if fresh:
                fresh_any = True
                if sym not in cache:
                    cache[sym] = {}
                cache[sym].update(fresh)
        if fresh_any:
            _feed_save_cache(conn, cache)
    return cache

@app.route("/api/feed-prices")
def api_feed_prices():
    """大宗饲料原料价格：每个品种含国际/中国/越南三条曲线，月度聚合 + 波峰波谷降采样。
    货币切换：三条曲线分别从各自原生货币换算到目标币种（真实汇率）。"""
    cur = (request.args.get("cur") or "USD").upper()
    if cur not in ("USD", "RMB", "VND"):
        cur = "USD"
    # 短期内存缓存（60s）：货币切换时避免重复拉 Yahoo
    cache_key = "feed_" + cur
    cached = _API_CACHE.get(cache_key)
    if cached and (time.time() - cached[0] < 60):
        return jsonify(cached[1])
    conn = get_db()
    try:
        # 历史+当月全部 100% 读 SQLite 固化缓存（秒开）；
        # 当月缺失时后台线程补抓，抓到后下次请求自动带上。
        raw = _feed_load_cache(conn)
        fx = _fx_load_cache(conn)
        now_ym = datetime.now().strftime("%Y-%m")
        if not (_month_has_data(raw, [v["sym"] for v in FEED_ITEMS.values()], now_ym)
                and _month_has_data(fx, FX_SYMBOLS.keys(), now_ym)):
            _kick_market_warm()
    finally:
        conn.close()
    # 统一 labels（所有品种日期并集，升序）
    all_dates = set()
    for cfg in FEED_ITEMS.values():
        all_dates.update(raw.get(cfg["sym"], {}).keys())
    labels = sorted(all_dates)
    # 真实历史汇率序列（双向填充：前向+后向，消除早期无数据缺口）
    def _bidir_fill(src, labs):
        f = _forward_fill(src, labs)
        # 后向填充开头 None
        last = None
        for i in range(len(f) - 1, -1, -1):
            if f[i] is not None:
                last = f[i]
            elif last is not None:
                f[i] = last
        return f
    usdcny = _bidir_fill(fx.get("USDCNY", {}), labels)
    usdvnd = _bidir_fill(fx.get("USDVND", {}), labels)
    # 目标币种换算因子（USD -> target），逐日。idx 为对应日期在 labels 中的下标。
    def usd_to_target(native_target, idx):
        if idx < 0:
            idx = 0
        if native_target == "USD":
            return 1.0
        if native_target == "RMB":
            return (usdcny[idx] if (idx < len(usdcny) and usdcny[idx]) else 1.0)
        if native_target == "VND":
            return (usdvnd[idx] if (idx < len(usdvnd) and usdvnd[idx]) else 1.0)
        return 1.0
    pv_result = {}
    _combined_curves = {}
    _combined_labels = []
    _cur_month = labels[-1][:7] if labels else None
    _anchor_month = "2026-08"
    last_idx = len(labels) - 1 if labels else -1
    # 锚点月(2026-08)在日序列中的索引：取最后一个落在 2026-08 的日点
    _anchor_idx = last_idx
    for _i in range(len(labels) - 1, -1, -1):
        if labels[_i][:7] == _anchor_month:
            _anchor_idx = _i
            break
    for item, cfg in FEED_ITEMS.items():
        sym = cfg["sym"]
        uf = cfg.get("unit_factor", 1.0)
        ratio = cfg.get("ddgs_ratio", 1.0)
        base = _forward_fill(raw.get(sym, {}), labels)
        # USD/吨基准序列（修正 CBOT 单位 + DDGS 比例）
        usd_series = [ (v * uf * ratio) if v is not None else None for v in base ]
        # 2026-08 校准：若最新日期落在 2026-08，直接用用户给出的 USD/吨 锚点价覆盖当月国际基准
        if _cur_month == _anchor_month and usd_series:
            usd_series[last_idx] = FEED_ANCHOR_202608.get(item, FEED_ANCHOR_202608["soybean"])
        is_anchor_month = (_cur_month == _anchor_month)
        def _f(factor):
            return round(factor, 2)
        # 当月锚点价换算到目标币种（用锚点月 2026-08 对应汇率）
        anchor_factor_cur = usd_to_target(cur, _anchor_idx)
        # 玉米用「本币现货价（CNY/吨）」锚点；其他品种用 USD/吨 CNF 锚点。
        # 玉米锚点换算：RMB 直接取值，USD=V/CNY汇率，VND=V*(VND/CNY)。
        def cny_to_target(cny_val, idx):
            if cny_val is None:
                return None
            cny_fx = usdcny[idx] if (idx < len(usdcny) and usdcny[idx]) else 1.0
            if cur == "RMB":
                return cny_val
            if cur == "USD":
                return cny_val / cny_fx
            if cur == "VND":
                vnd_fx = usdvnd[idx] if (idx < len(usdvnd) and usdvnd[idx]) else 1.0
                return cny_val * (vnd_fx / cny_fx)
            return cny_val
        # 本币锚点表：按品种选择（玉米/大豆用 CNY/吨，其余用 USD/吨 CNF）
        _CNY_ANCHOR_TABLE = {
            "corn": FEED_CNY_CORN_ANCHOR,
            "soybean": FEED_CNY_SOYBEAN_ANCHOR,
            "soymeal": FEED_CNY_SOYMEAL_ANCHOR,
            "ddgs": FEED_CNY_DDGS_ANCHOR,
        }
        cny_table = _CNY_ANCHOR_TABLE.get(item)
        # 真实口径公式：以 2026-08 真实现货锚点为基准，历史各月按 CBOT 相对比例回推
        #   某月真实价 = 锚点价 × (该月CBOT原始值 / 2026-08月CBOT原始值)
        # 这样整条曲线都是真实口径（终点=真实锚点，历史=相同波动形态），而非旧模拟值。
        base_ref = usd_series[_anchor_idx] if (_anchor_idx < len(usd_series) and usd_series[_anchor_idx]) else None
        curves = {}

        def _anchor_for(ckey):
            """返回该曲线在目标货币下的 2026-08 真实锚点价"""
            if cny_table is not None:
                # 本币现货锚点（CNY/吨）：中国用 CN，越南用 VN，国际用 CBOT 锚点
                if ckey == "intl":
                    a = FEED_ANCHOR_202608.get(item, FEED_ANCHOR_202608["soybean"])
                    return _f(a * anchor_factor_cur)
                elif ckey == "china":
                    return _f(cny_to_target(cny_table["CN"], _anchor_idx))
                elif ckey == "vietnam":
                    return _f(cny_to_target(cny_table["VN"], _anchor_idx))
                else:
                    return _f(cny_to_target(cny_table.get(ckey), _anchor_idx))
            else:
                if ckey == "intl":
                    a = FEED_ANCHOR_202608.get(item, FEED_ANCHOR_202608["soybean"])
                elif ckey == "china":
                    a = FEED_CNF_ANCHOR["CN"].get(item, 0)
                elif ckey == "vietnam":
                    a = FEED_CNF_ANCHOR["VN"].get(item, 0)
                else:
                    a = FEED_CNF_ANCHOR.get(ckey, {}).get(item, 0)
                return _f(a * anchor_factor_cur)

        # 基础曲线（国际/中国/越南）
        for ckey in FEED_CURVE_NATIVE:
            a_val = _anchor_for(ckey)
            arr = []
            for j in range(len(usd_series)):
                v = usd_series[j]
                if v is None or base_ref is None or base_ref == 0:
                    arr.append(None)
                elif j == last_idx:
                    arr.append(a_val)  # 锚点月直接用真实价
                else:
                    # 历史月：锚点价 × 当月CBOT相对比例
                    arr.append(_f(a_val * (v / base_ref)))
            curves[ckey] = arr
        # 国家曲线（含 CN 与各经验国家）
        all_ccodes = ["CN"] + list(FEED_COUNTRY_BASIS.keys())
        for ccode in all_ccodes:
            a_val = _anchor_for(ccode)
            arr = []
            for j in range(len(usd_series)):
                v = usd_series[j]
                if v is None or base_ref is None or base_ref == 0:
                    arr.append(None)
                elif j == last_idx:
                    arr.append(a_val)
                else:
                    arr.append(_f(a_val * (v / base_ref)))
            curves[ccode] = arr
        # 月度聚合
        month_labels, month_curves = _monthly_avg(labels, curves)
        # 2026-08 校准：用已覆盖的当日锚点值直接作为当月月度值，避免月中旧数据拉低平均
        if _cur_month == _anchor_month and month_labels and month_labels[-1] == _anchor_month:
            for ckey in curves:
                if curves[ckey] and curves[ckey][-1] is not None:
                    month_curves[ckey][-1] = curves[ckey][-1]
        # 暂存到统一容器，稍后统一做波峰波谷降采样（保证所有品种共享同一套 labels）
        for ckey in month_curves:
            _combined_curves[item + "|" + ckey] = month_curves[ckey]
        _combined_labels = month_labels
    # 统一波峰波谷降采样：所有品种/曲线共享同一套索引，确保 labels 与每条 series 一一对应
    pv_labels, _pv_combined = _peak_valley(_combined_labels, _combined_curves)
    # 拆分回每个品种
    pv_result = {}
    for item in FEED_ITEMS:
        pv_result[item] = {}
        for ckey in _combined_curves:
            if ckey.startswith(item + "|"):
                pv_result[item][ckey.split("|", 1)[1]] = _pv_combined[ckey]
    resp = {
        "ok": True,
        "cur": cur,
        "labels": pv_labels,
        "series": pv_result,
        "symbols": {k: v["sym"] for k, v in FEED_ITEMS.items()},
        "units": {k: v["unit"] for k, v in FEED_ITEMS.items()},
        "countries": {
            code: {"name": cfg["name"], "basis": cfg.get("basis", {})}
            for code, cfg in FEED_COUNTRY_BASIS.items()
        },
    }
    _API_CACHE["feed_" + cur] = (time.time(), resp)
    resp_obj = jsonify(resp)
    resp_obj.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    resp_obj.headers["Pragma"] = "no-cache"
    return resp_obj

@app.route("/api/feed-test")
def api_feed_test():
    """调试端点：检查 _monthly_avg 和 _peak_valley 的中间数据"""
    cur = (request.args.get("cur") or "RMB").upper()
    conn = get_db()
    try:
        raw = _feed_build_data(conn, cur)
        labels = raw["labels"]
        curves = raw["series"]
    finally:
        conn.close()
    
    # 测试 _monthly_avg
    month_labels, month_curves = _monthly_avg(labels, curves)
    
    # 测试 _peak_valley
    pv_labels, pv_curves = _peak_valley(month_labels, month_curves)
    
    result = {
        "raw_labels": len(labels),
        "raw_series_len": {k: len(v) for k, v in curves.items() if "corn" in k or k in ("vietnam","china","intl")},
        "month_labels": len(month_labels),
        "month_series_len": {k: len(v) for k, v in month_curves.items() if "corn" in k or k in ("vietnam","china","intl")},
        "pv_labels": len(pv_labels),
        "pv_series_len": {k: len(v) for k, v in pv_curves.items() if "corn" in k or k in ("vietnam","china","intl")},
        "match": len(pv_labels) == all(len(v) == len(pv_labels) for v in pv_curves.values()),
    }
    return jsonify(result)


@app.route("/api/material-prices")
def api_material_prices():
    """建材（钢筋/水泥/黄砂/石子）市场价格指数 API。

    优先拉取环境变量配置的真实数据源（VN_MAT_API_URL + 可选 VN_MAT_API_KEY），
    返回与前端 vendor/material_prices.js 完全一致的 {labels, units, series} 结构；
    未配置或拉取失败时回退到前端已内置的示例数据（use_bundled=true），前端零改动。

    期望的真实数据源响应格式（两种均可）：
      格式A（直接同构）:
        {"labels":["2021-01",...], "units":{"rebar":"VND/kg",...},
         "series":{"rebar":[...],"cement":[...],"sand":[...],"gravel":[...]}}
      格式B（按材料列点）:
        {"rebar":[{"ym":"2021-01","price":15677},...], "cement":[...], ...}
    越南可选数据源示例：Vật Giá Top（vatgia.top）Construction Material Price API。
    """
    cache_key = "material_prices"
    cached = _API_CACHE.get(cache_key)
    if cached and (time.time() - cached[0] < 3600):
        return jsonify(cached[1])

    url = os.environ.get("VN_MAT_API_URL")
    key = os.environ.get("VN_MAT_API_KEY")
    if url:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            if key:
                req.add_header("Authorization", "Bearer " + key)
            with urllib.request.urlopen(req, timeout=20) as resp:
                js = json.loads(resp.read().decode("utf-8"))
            data = _normalize_material_prices(js)
            if data:
                out = {"ok": True, "data_source": "live", "use_bundled": False,
                       "labels": data["labels"], "units": data["units"], "series": data["series"]}
                _API_CACHE[cache_key] = (time.time(), out)
                return jsonify(out)
        except Exception as e:
            app.logger.warning("material-prices live fetch failed: %s", e)
    # 回退：使用前端内置示例数据
    out = {"ok": True, "data_source": "demo", "use_bundled": True,
           "labels": [], "units": {}, "series": {}}
    _API_CACHE[cache_key] = (time.time(), out)
    return jsonify(out)


def _normalize_material_prices(js):
    """把外部响应规整成 {labels, units, series}，失败返回 None。"""
    if not isinstance(js, dict):
        return None
    keys = ("rebar", "cement", "sand", "gravel")
    # 格式A：直接同构
    if js.get("labels") and isinstance(js.get("series"), dict):
        series = {k: list(js["series"].get(k, []) or []) for k in keys}
        if any(series.values()):
            labels = list(js["labels"])
            for k in keys:
                if len(series[k]) > len(labels):
                    series[k] = series[k][:len(labels)]
            return {"labels": labels,
                    "units": {k: (js.get("units") or {}).get(k, "VND") for k in keys},
                    "series": series}
    # 格式B：每个材料是 [{ym, price}] 列表
    if all(isinstance(js.get(k), list) for k in keys):
        merged = {}
        for k in keys:
            for it in (js.get(k) or []):
                if not isinstance(it, dict):
                    continue
                ym = it.get("ym") or it.get("date")
                price = it.get("price", it.get("value"))
                if ym and price is not None:
                    merged.setdefault(k, {})[ym] = price
        if merged:
            labels = sorted({ym for k in merged for ym in merged[k]})
            series = {k: [merged.get(k, {}).get(ym) for ym in labels] for k in keys}
            return {"labels": labels,
                    "units": {k: "VND" for k in keys},
                    "series": series}
    return None


@app.route("/api/fx-rates")
def api_fx_rates():
    """返回三条真实历史汇率曲线：USD→CNY、USD→VND、CNY→VND，最近 5 年 + 当月。"""
    # 短期内存缓存（60s）
    cached = _API_CACHE.get("fx")
    if cached and (time.time() - cached[0] < 60):
        return jsonify(cached[1])
    conn = get_db()
    try:
        # 缓存直读（秒开）；当月缺失后台补抓
        fx = _fx_load_cache(conn)
        now_ym = datetime.now().strftime("%Y-%m")
        if not _month_has_data(fx, FX_SYMBOLS.keys(), now_ym):
            _kick_market_warm()
    finally:
        conn.close()
    all_dates = set()
    all_dates.update(fx.get("USDCNY", {}).keys())
    all_dates.update(fx.get("USDVND", {}).keys())
    labels = sorted(all_dates)
    usdcny = _forward_fill(fx.get("USDCNY", {}), labels)
    usdvnd = _forward_fill(fx.get("USDVND", {}), labels)
    # USD->CNY 保留 2 位小数；USD->VND 和 CNY->VND 取整（数值大无需小数）
    cny_vnd = []
    for i in range(len(labels)):
        a = usdcny[i]
        b = usdvnd[i]
        if a and b:
            cny_vnd.append(round(b / a))   # CNY→VND 取整
        else:
            cny_vnd.append(None)
    # usdvnd 也取整
    usdvnd_int = [round(v) if v is not None else None for v in usdvnd]
    # 聚合为月度平均，再提取波峰波谷关键点，降低渲染密集度
    daily_series = {
        "usd_cny": usdcny,       # 1 USD = ? CNY（2 位小数）
        "usd_vnd": usdvnd_int,   # 1 USD = ? VND（整数）
        "cny_vnd": cny_vnd       # 1 CNY = ? VND（整数）
    }
    month_labels, month_series = _monthly_avg(labels, daily_series)
    pv_labels, pv_series = _peak_valley(month_labels, month_series)
    # VND 类汇率数值大，取整显示
    for k in ("usd_vnd", "cny_vnd"):
        if k in pv_series:
            pv_series[k] = [round(v) if v is not None else None for v in pv_series[k]]
    resp = {
        "ok": True,
        "labels": pv_labels,
        "series": pv_series
    }
    _API_CACHE["fx"] = (time.time(), resp)
    return jsonify(resp)


# ============================================================================
# DEMO 演示数据机制（一键还原 / 一键清空）
# ============================================================================
# 设计要点：
#   · 示例数据从 demo_snapshot.json 还原（由 export_demo_snapshot.py 生成），
#     而不是调用 seed 函数重新生成 —— 这样能 100% 还原"当时"的演示状态，
#     包括 CRM 那 32 条被 migrate 修正过的数据。
#   · ★ DEMO 与用户列表彻底解耦（用户明确要求）：load/clear 只动 DEMO_TABLES
#     四张业务表，users 表 / managers 表一个字都不碰 —— 不管真实账号还是
#     演示账号（khoa/minh 等）。删用户只能走「用户与授权」页的删除审批流程。
#     demo_users 列表仅供 reset_demo_data.py 清理脚本使用。
# ============================================================================

def _demo_snapshot_exists():
    return os.path.exists(DEMO_SNAPSHOT)


def clear_demo_data(c, also_business=True):
    """清空演示业务数据（DEMO_TABLES 四张表）。

    ★ 与用户列表彻底解耦：本函数绝不碰 users / managers 表（真实账号和
    演示账号都不动）。删用户只能走用户管理页的删除审批流程。

    ★ is_demo 精确清除：只删 is_demo=1 的演示行，真实录入的业务数据（is_demo=0）
    一律保留 —— 培训结束点「清空 DEMO」即可把演示数据彻底清干净，绝不误伤真实数据。
    （早期未打标记的存量演示数据，由 init_db 后的一次性标注 / 或 reset_demo_data.py 兜底处理。）
    """
    removed = {}
    if also_business:
        for t in DEMO_TABLES:
            try:
                n = c.execute("SELECT COUNT(*) FROM %s WHERE is_demo=1" % t).fetchone()[0]
                c.execute("DELETE FROM %s WHERE is_demo=1" % t)
                try:
                    c.execute("DELETE FROM sqlite_sequence WHERE name=?", (t,))
                except Exception:
                    pass
                removed[t] = n
            except Exception as e:
                removed[t] = "失败: %s" % e
    # ★ 用户/管理员表完全不碰（DEMO 与用户列表彻底解耦）
    removed["_demo_users"] = 0
    removed["_demo_managers"] = 0
    return removed


def load_demo_data(c):
    """从快照还原演示数据。若快照不存在，则回退到调用 seed 函数生成。"""
    if not _demo_snapshot_exists():
        # 回退：用内置 seed 函数生成（数据会与快照略有差异）
        seed_crm_projects(c)
        seed_approval_requests(c)
        # seed 出来的也是演示数据，打 is_demo=1，便于「清空 DEMO」精确移除
        for _t in DEMO_TABLES:
            try:
                c.execute("UPDATE %s SET is_demo=1" % _t)
            except Exception:
                pass
        return {"mode": "seed_fallback", "note": "快照不存在，已用内置示例数据生成"}

    with open(DEMO_SNAPSHOT, "r", encoding="utf-8") as f:
        snap = json.load(f)

    restored = {}

    # ---- 业务表 ----
    # ★ 还原前只清【演示行】(is_demo=1)，真实录入的数据(is_demo=0)一律保留 ——
    #   这样培训期间你加的真实业务数据不会被「加载 DEMO」冲掉；DEMO 始终是同一批固定样本。
    for t in DEMO_TABLES:
        rows = (snap.get("tables") or {}).get(t) or []
        try:
            c.execute("DELETE FROM %s WHERE is_demo=1" % t)
        except Exception:
            pass
        n = 0
        for row in rows:
            if not isinstance(row, dict):
                continue
            # 去掉 id：避免 INSERT 覆盖真实行（真实行用自增 id，互不冲突）；
            # 末尾追加 is_demo=1 标记，供「清空 DEMO」精确删除、不误伤真实数据。
            cols = [k for k in row.keys() if k != "id"]
            cols.append("is_demo")
            if not cols:
                continue
            ph = ",".join("?" * len(cols))
            sql = "INSERT INTO %s (%s) VALUES (%s)" % (
                t, ",".join(cols), ph)
            try:
                vals = [row[k] for k in cols if k != "is_demo"] + [1]
                c.execute(sql, vals)
                n += 1
            except Exception:
                continue
        restored[t] = n

    # ★ 用户/管理员表完全不碰（DEMO 与用户列表彻底解耦）。
    # 快照里即使存有 demo_users / demo_managers 也一律忽略不写入。
    restored["_demo_users"] = 0
    restored["_demo_managers"] = 0
    restored["mode"] = "snapshot"
    return restored


# ⛔⛔⛔ 锁死（DEMO 策略，2026-09-04）：业务表的演示案例统一打 is_demo=1，作为「培训样本」固定保留，
# 培训结束前严禁任何路径删除/改动这批演示行（仅 /api/demo/clear 在培训后统一清空）。
# 真实录入数据一律 is_demo=0，绝不被 DEMO 还原或清空误伤。勿新增会自动清除 demo 的逻辑。
@app.route("/api/demo/load", methods=["POST"])
def api_demo_load():
    """一键还原演示数据（重置模式：先清空，再从快照还原）。"""
    try:
        conn = get_db()
        c = conn.cursor()
        clear_demo_data(c, also_business=True)
        restored = load_demo_data(c)
        conn.commit()
        conn.close()
        return jsonify({"ok": True, "restored": restored})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/api/demo/clear", methods=["POST"])
def api_demo_clear():
    """一键清空演示数据，回到只有真实用户的干净状态。"""
    try:
        conn = get_db()
        c = conn.cursor()
        removed = clear_demo_data(c, also_business=True)
        conn.commit()
        conn.close()
        return jsonify({"ok": True, "removed": removed})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


if __name__ == "__main__":
    import logging
    import socket
    # 默认只打印 WARNING 及以上，避免每个请求刷屏；开发需要时改成 INFO
    logging.basicConfig(level=logging.WARNING)
    # 关闭 Werkzeug 默认请求日志（只保留 ERROR 级别）
    werkzeug_log = logging.getLogger('werkzeug')
    werkzeug_log.setLevel(logging.ERROR)

    PORT = 5050

    # 每次启动先留一份整库快照（防数据丢失第一道保险）
    _auto_backup_db("startup")

    # 中国财务报表：文件/表名映射缺失时补一份种子（幂等；中国报表只有「实际支出」一张表）
    _cn_seed_if_missing()

    def _port_in_use(port, host="127.0.0.1", timeout=0.5):
        """端口占用预检（Windows 安全版）。

        注意：探测 socket 绝不能设置 SO_REUSEADDR，否则 Windows 下会与已监听的
        实例"共享"端口并 bind 成功，导致误判为"空闲"，预检形同虚设。
        这里改用 connect 探测：能连上说明确实已有服务在监听，判定为占用。
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        try:
            s.connect((host, port))
            return True          # 连得上 = 已有实例在监听
        except OSError:
            return False         # 连不上 = 端口空闲
        finally:
            s.close()

    if _port_in_use(PORT):
        # 端口已被占用：明确报错退出，避免多实例静默共存导致"改了代码看不到效果"
        # 提示用 ASCII，避免任何控制台编码环境下出现乱码
        sys.stderr.write(
            "\n[FATAL] Port %d is already in use. Service NOT started.\n"
            "        Another app.py instance may be running.\n"
            "        Fix: run start_server.bat (auto-kills old instances),\n"
            "             or: netstat -ano | findstr :%d\n\n" % (PORT, PORT)
        )
        sys.stderr.flush()
        sys.exit(1)

    # use_reloader=False：关闭 Flask 自动重载，避免每次启动产生 2 个进程（父 reloader + 子 worker）
    # threaded=True：多线程处理并发请求
    print("[OK] AGI-PM 服务启动：http://127.0.0.1:%d  (单实例/无 reloader)" % PORT)
    # 打印局域网 IP：手机/PWA 需用同一 WiFi 下的该地址访问（前端已改为同源相对路径，无需再改 IP）
    try:
        import socket as _sock
        _lan = None
        _s = _sock.socket(_sock.AF_INET, _sock.SOCK_DGRAM)
        _s.settimeout(0.5)
        # 不会真的发包，只是让系统选出去往公网的网卡，从而拿到本机局域网 IP
        _s.connect(("8.8.8.8", 80))
        _lan = _s.getsockname()[0]
        _s.close()
        if _lan and not _lan.startswith("127."):
            print("[INFO] 手机/PWA 访问（同一 WiFi）：http://%s:%d" % (_lan, PORT))
    except Exception:
        pass
    # 后台定时整库快照：服务长时间运行、无人手动保存时，仍每 30 分钟留一份
    try:
        import threading as _threading
        def _backup_loop():
            while True:
                time.sleep(1800)
                try:
                    _auto_backup_db("interval")
                except Exception:
                    pass
        _threading.Thread(target=_backup_loop, daemon=True).start()
        print("[INFO] 后台整库备份已启动（每 30 分钟一份，滚动保留最近 80 份）")
    except Exception as _be:
        print("[WARN] 后台备份线程启动失败：%s" % _be)
    app.run(host="0.0.0.0", port=PORT, debug=False, use_reloader=False, threaded=True)