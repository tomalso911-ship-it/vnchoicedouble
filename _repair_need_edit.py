# -*- coding: utf-8 -*-
"""一次性数据修复：审批已「返回重新填写」，但收货单状态还停在 pending 的记录。

背景（APPR-RETURN-LOCK-20261026）：
  审批人在「审批中心」点「返回重新填写」时，前端 prod_save() 被
  prod_pushToServer 的首次同步门禁(__PROD_SYNCED)静默拦掉，服务端收货单
  状态没被改成 need_edit → 申请人列表里永远看不到「✎ 重新填写」按钮，
  流程无法闭环。代码已修好；本脚本把【已经卡住的历史记录】补回正确状态。

用法：
  python _repair_need_edit.py <db路径>            # 预演（只打印，不写）
  python _repair_need_edit.py <db路径> --apply    # 真正写入（写前自动备份 db）
"""
import json
import os
import shutil
import sqlite3
import sys
import time

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
APPLY = "--apply" in sys.argv
DB = ARGS[0] if ARGS else "agi_pm.db"

if not os.path.isfile(DB):
    print("找不到数据库：" + DB)
    sys.exit(1)

if APPLY:
    bak = DB + ".bak_before_need_edit_%s" % time.strftime("%Y%m%d_%H%M%S")
    shutil.copyfile(DB, bak)
    print("已备份 -> " + bak)

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

rows = con.execute(
    "select id,requester,status,target_id,resolver,resolved_at,payload "
    "from approval_requests where block_id='PROD-RECEIPT' and status='returned' "
    "order by id"
).fetchall()

print("待检查的「返回重新填写」审批：%d 条" % len(rows))
fixed = 0
for r in rows:
    pl = {}
    try:
        pl = json.loads(r["payload"] or "{}")
    except Exception:
        pass
    pid, rid = pl.get("project"), pl.get("receiptId")
    if not pid or not rid:
        print("  审批 %s：payload 缺 project/receiptId，跳过" % r["id"])
        continue
    fr = con.execute("select rowid,data,updated_at from prod_factory where project_id=?",
                     (str(pid),)).fetchone()
    if not fr:
        print("  审批 %s：prod_factory 无 project=%s，跳过" % (r["id"], pid))
        continue
    try:
        data = json.loads(fr["data"])
    except Exception as e:
        print("  审批 %s：工厂数据解析失败 %s" % (r["id"], e))
        continue
    mats = data.get("materials") or {}
    recs = mats.get("receipts") or []
    hit = [x for x in recs if x.get("id") == rid]
    if not hit:
        print("  审批 %s：收货单 %s 不在列表（可能已被重新填写/删除），跳过" % (r["id"], rid))
        continue
    cur = hit[0].get("status")
    if cur == "need_edit":
        print("  审批 %s：收货单 %s 已是 need_edit ✓" % (r["id"], rid))
        continue
    if cur != "pending":
        print("  审批 %s：收货单 %s 当前=%s（非 pending），保守跳过" % (r["id"], rid, cur))
        continue
    print("  审批 %s：收货单 %s pending -> need_edit%s"
          % (r["id"], rid, "" if APPLY else "  【预演】"))
    if APPLY:
        hit[0]["status"] = "need_edit"
        data["materials"] = mats
        con.execute("update prod_factory set data=?, updated_at=? where rowid=?",
                    (json.dumps(data, ensure_ascii=False),
                     time.strftime("%Y-%m-%d %H:%M:%S"), fr["rowid"]))
        fixed += 1

if APPLY:
    con.commit()
    print("完成：修复 %d 条" % fixed)
else:
    print("预演结束（未写入）。确认无误后加 --apply 执行。")
con.close()
