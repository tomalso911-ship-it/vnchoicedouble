# -*- coding: utf-8 -*-
"""反向测试 check_prod_out_rule.py 的解析口径与守卫：
  A) dict-lines + qtyDetail 正常数据 → 0 违规（旧实现会误报）
  B) dict-lines + qty（无 qtyDetail），需求量基线可拆 → 0 违规
  C) 真正超出的数据 → 1（能抓到）
  D) 认不出的数据形状 → 2（形状守卫生效，不再静默误报）
  E) 缺需求量基线 + 无 qtyDetail → 不作判定（防误报），仍 0
在临时库上跑，绝不碰 agi_pm.db。"""
import io
import json
import os
import shutil
import sqlite3
import sys
import tempfile

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_prod_out_rule as R  # noqa: E402

SRC = os.path.join(HERE, "agi_pm.db")
SPEC = "A×B×C"          # 规格键必须是 L×W×H 形态，才会命中需求量基线


def case_a():
    """dict-lines + qtyDetail[规格][猪舍]：产量 30，出库 30 → 应 0 违规"""
    return {"production": {"01/01/2026": {"lines": {
        "1": {"houses": ["1"], "qty": {SPEC: 30}, "qtyDetail": {SPEC: {"1": 30}}}}}},
        "houseOut": {"1|" + SPEC: {"out": 30}}}


def case_b():
    """dict-lines + 只有 qty，靠需求量基线按比例拆分：
       猪舍1 需求 1、猪舍2 需求 3，qty=40 → 1:10、2:30；出库 10/30 → 0 违规"""
    return {"production": {"01/01/2026": {"lines": {
        "1": {"houses": ["1", "2"], "qty": {SPEC: 40}}}}},
        "houseOut": {"1|" + SPEC: {"out": 10}, "2|" + SPEC: {"out": 30}}}


def case_c():
    """真超出：qtyDetail 只给 5，出库 9 → 应报 1 处违规"""
    return {"production": {"01/01/2026": {"lines": {
        "1": {"houses": ["1"], "qty": {SPEC: 5}, "qtyDetail": {SPEC: {"1": 5}}}}}},
        "houseOut": {"1|" + SPEC: {"out": 9}}}


def case_d():
    """认不出的形状：数量既不是 qty/qtyDetail/matrix → 守卫应报运行错误"""
    return {"production": {"01/01/2026": {"lines": {"1": {"houses": ["1"], "weird": 999}}}},
            "houseOut": {"1|" + SPEC: {"out": 9}}}


def case_e():
    """old-shape 回归：lines 写成 list（旧数据可能出现）也应能解析"""
    return {"production": {"01/01/2026": {"lines": [
        {"houses": ["1"], "qty": {SPEC: 30}, "qtyDetail": {SPEC: {"1": 30}}}]}},
        "houseOut": {"1|" + SPEC: {"out": 30}}}


def run(cases, demand_rows):
    fd, p = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    shutil.copyfile(SRC, p)
    try:
        c = sqlite3.connect(p)
        c.execute("DELETE FROM prod_factory")
        c.execute("DELETE FROM won_projects")
        if demand_rows:
            c.execute("INSERT INTO won_projects(id, concrete_floor_spec) VALUES(?,?)",
                      ("1", json.dumps(demand_rows, ensure_ascii=False)))
        for pid, f in cases:
            c.execute("INSERT INTO prod_factory(project_id, data) VALUES(?,?)",
                      (str(pid), json.dumps(f, ensure_ascii=False)))
        c.commit()
        c.close()
        buf = io.StringIO()
        old = sys.stdout
        sys.stdout = buf
        try:
            rc = R.check_db(p)
        finally:
            sys.stdout = old
        return rc, buf.getvalue()
    finally:
        os.remove(p)


def demand_row(house, qty):
    return {"floor_len": "A", "floor_wid": "B", "floor_hgt": "C", "pig_house": house,
            "qty_unit": qty, "unit_per_building": 1, "building_count": 1}


DEMAND = [demand_row("1", 1), demand_row("2", 3)]
fails = 0


def expect(label, rc, out, want_rc, want_txt=None):
    global fails
    ok = (rc == want_rc) and (want_txt is None or want_txt in out)
    if not ok:
        fails += 1
    print("%-44s rc=%s (期望 %s) %s" % (label, rc, want_rc, "OK" if ok else "FAIL"))
    if not ok:
        print("     输出:", out.strip().replace("\n", " | ")[:300])


print("=== A) dict-lines + qtyDetail（旧实现会误报的关键形状）===")
rc, out = run([("A1", case_a())], DEMAND)
expect("dict-lines + qtyDetail → 通过", rc, out, 0, "✓ 通过")

print("=== B) dict-lines + qty 按需求量比例拆分 ===")
rc, out = run([("B1", case_b())], DEMAND)
expect("qty 拆分后不超 → 通过", rc, out, 0, "✓ 通过")

print("=== C) 真超出必须抓到 ===")
rc, out = run([("C1", case_c())], DEMAND)
expect("出库9>产量5 → 违规", rc, out, 1, "1 | " + SPEC)

print("=== D) 认不出的形状 → 守卫报运行错误(2) ===")
rc, out = run([("D1", case_d())], DEMAND)
expect("形状失效 → 退出码 2", rc, out, 2, "解析口径")

print("=== E) 缺需求量基线 + 无 qtyDetail → 不作判定（防误报）===")
rc, out = run([("E1", case_b())], [])
expect("无基线 → 跳过判定并说明，仍 0", rc, out, 0, "未作违规判定")

print("=== F) 旧形状 lines=list 回归 ===")
rc, out = run([("F1", case_e())], DEMAND)
expect("list 形态也能解析 → 通过", rc, out, 0, "✓ 通过")

print()
print("RESULT =", "全部通过" if fails == 0 else ("%d 项 FAIL" % fails))
sys.exit(1 if fails else 0)
