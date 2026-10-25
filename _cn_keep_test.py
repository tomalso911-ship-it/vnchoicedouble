#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FIN-KEEP-20261016 端到端验证（只读 + 一次「应被拒绝」的保存尝试）。

验证三件事：
  A) 乐观锁：带错误版本号保存 → 必须被拒（stale），且 cn_report.xlsx 一动不动。
  B) 数据量守卫：带正确版本号、但内容被削掉 90% 的快照 → 必须被拒（guard=data-loss），
     且 cn_report.xlsx 一动不动；若守卫失效把文件写坏，脚本会自动从手工备份还原并报 FAIL。
  C) 写盘前历史备份：被拒的这次尝试也必须留下 backups/cn_history/ 里的一份可回滚点。
"""
import json
import os
import sys
import glob
import urllib.request
import urllib.error

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = "http://127.0.0.1:5050"
ROOT = os.path.dirname(os.path.abspath(__file__))
CN = os.path.join(ROOT, "finance_data", "cn_report.xlsx")
SAFE = os.path.join(ROOT, "finance_data", "backups", "cn_report_before_finkeep_20261016.xlsx.bak")
HIST = os.path.join(ROOT, "finance_data", "backups", "cn_history")
SNAP_URL = BASE + "/api/finance/cn-report/snapshot"
SAVE_URL = BASE + "/api/finance/cn-report/save"

fails = []


def sig(path=CN):
    st = os.stat(path)
    return (int(st.st_size), int(st.st_mtime_ns))


def http(url, method="GET", obj=None, timeout=180):
    data = None
    headers = {}
    if obj is not None:
        data = json.dumps(obj).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, dict(r.headers), r.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers or {}), e.read()


def hist_files():
    if not os.path.isdir(HIST):
        return []
    return sorted(glob.glob(os.path.join(HIST, "cn_*.xlsx.bak")))


print("=" * 72)
print("初始 cn_report.xlsx =", sig())
print("历史目录:", HIST, "已有", len(hist_files()), "份")

# ---------- 取当前快照与版本号 ----------
st, hdr, raw = http(SNAP_URL)
rev = hdr.get("X-Fin-Rev") or hdr.get("x-fin-rev")
print("GET /snapshot  HTTP", st, " rev =", rev, " 快照 %d 字节" % len(raw))
if st != 200 or not rev:
    print("✗ 拿不到快照/版本号，测试中止")
    sys.exit(1)

# ---------- A) 错误版本号必须被拒 ----------
s0 = sig()
st_a, _, body_a = http(SAVE_URL, "POST", {"__rev": "bogus-rev-for-test", "sheetOrder": [], "sheets": {}})
try:
    ja = json.loads(body_a.decode("utf-8"))
except Exception:
    ja = {}
print("-" * 72)
print("A) 错误版本号保存 → HTTP", st_a, ja)
ok_a = bool(ja.get("stale")) and sig() == s0
print("   文件未被改动:", sig() == s0, " 结论:", "PASS" if ok_a else "FAIL")
if not ok_a:
    fails.append("A 乐观锁未拦住错误版本号的保存")

# ---------- B) 内容被削掉 90% 的快照必须被拒 ----------
snap = json.loads(raw.decode("utf-8"))
sids = snap.get("sheetOrder") or list((snap.get("sheets") or {}).keys())
sid = sids[0] if sids else None
cells_before = 0
for s in (snap.get("sheets") or {}).values():
    cells_before += sum(len(row) for row in (s.get("cellData") or {}).values())
print("-" * 72)
print("B) 快照原始非空格数 ≈", cells_before, " 工作表", sid)
shrink = json.loads(raw.decode("utf-8"))
sh = (shrink.get("sheets") or {}).get(sid)
sh["cellData"] = {"4": {"0": {"v": "SHRINK-TEST"}, "1": {"v": "1"}}}
s1 = sig()
n_hist_before = len(hist_files())
st_b, _, body_b = http(SAVE_URL, "POST", dict(shrink, __rev=rev))
try:
    jb = json.loads(body_b.decode("utf-8"))
except Exception:
    jb = {}
print("   削顶保存 → HTTP", st_b, jb)
unchanged = (sig() == s1)
print("   文件未被改动:", unchanged)
if not unchanged:
    print("   ✗✗ 守卫失效、文件已被写坏 → 立刻从手工备份还原！")
    if os.path.isfile(SAFE):
        import shutil
        shutil.copyfile(SAFE, CN)
        print("   已还原:", sig())
    fails.append("B 数据量守卫失效（文件被削顶快照覆盖，已从备份还原）")
else:
    ok_b = bool(jb.get("stale")) and jb.get("guard") == "data-loss"
    print("   结论:", "PASS" if ok_b else "FAIL（stale=%s guard=%s）" % (jb.get("stale"), jb.get("guard")))
    if not ok_b:
        fails.append("B 守卫没按 data-loss 拒绝（stale/guard 不符）")

# ---------- C) 被拒的这次也必须有历史备份 ----------
n_hist_after = len(hist_files())
print("-" * 72)
print("C) 历史备份 %d → %d 份" % (n_hist_before, n_hist_after))
if n_hist_after > n_hist_before:
    for f in hist_files()[-3:]:
        print("   +", os.path.basename(f), os.stat(f).st_size, "B")
    print("   结论: PASS")
else:
    print("   结论: FAIL（写盘前没有留下历史备份）")
    fails.append("C 写盘前历史备份未生成")

print("=" * 72)
if fails:
    print("✗ 测试失败：")
    for f in fails:
        print("   -", f)
    sys.exit(1)
print("✓ 全部通过：错误版本号被拒 / 削顶快照被拒 / 写盘前留有可回滚备份")
print("最终 cn_report.xlsx =", sig())
