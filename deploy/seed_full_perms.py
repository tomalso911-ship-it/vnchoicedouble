#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""一次性数据迁移：给 admin/cuong/james 落库「和 tom 一样」的全放开权限。

★OWNER-MATRIX-20261107：上一轮这三人是读时归一化（不落库），没有可修改的实体；
现在 tom/admin 必须能真实改他们的权限，所以把当前全放开结果写入各自的 perms。
只跑一次（标记文件），之后 tom/admin 的任何修改都不会被启动流程覆盖。

在服务器上执行：python3 /opt/choice-pm/deploy/seed_full_perms.py
"""
import json
import sqlite3
import time
import urllib.request
from pathlib import Path

BASE = Path("/opt/choice-pm")
DB = BASE / "agi_pm.db"
MARK = BASE / "backups" / ".full_perms_seeded_v2"
TARGETS = ("admin", "cuong", "james")


def main():
    (BASE / "backups").mkdir(exist_ok=True)
    if MARK.exists():
        print("SKIP: already seeded (", MARK, ")")
        return

    # 以服务端当前的归一化结果为准，避免模板写死走样
    with urllib.request.urlopen(
            urllib.request.Request("http://127.0.0.1:5060/api/me?username=tom",
                                   headers={"Accept-Encoding": "identity"}),
            timeout=20) as r:
        full = json.loads(r.read().decode("utf-8"))["user"]["perms"]
    if not full.get("common") or not full.get("projects"):
        raise SystemExit("ABORT: tom perms 不是全放开，先确认新代码已重启生效")
    packed = json.dumps(full, ensure_ascii=False)

    conn = sqlite3.connect(str(DB))
    conn.row_factory = sqlite3.Row
    before = {}
    for name in TARGETS:
        row = conn.execute("SELECT id, perms FROM users WHERE username=?", (name,)).fetchone()
        if not row:
            print("MISS:", name)
            continue
        before[name] = {"id": row["id"], "perms": row["perms"]}
        conn.execute("UPDATE users SET perms=? WHERE username=?", (packed, name))
    conn.commit()
    conn.close()

    ts = time.strftime("%Y%m%d_%H%M%S")
    bak = BASE / "backups" / ("perms_seed_%s.json" % ts)
    bak.write_text(json.dumps(before, ensure_ascii=False, indent=2), encoding="utf-8")
    MARK.write_text(ts, encoding="utf-8")
    print("SEEDED:", ", ".join(before.keys()))
    print("BACKUP:", bak)
    print("FULL_PERMS common=%d projects=%d" % (
        len(full.get("common", {})), len(full.get("projects", {}))))


if __name__ == "__main__":
    main()
