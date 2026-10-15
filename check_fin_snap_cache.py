#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
财务 Univer 快照缓存「锁死」检查（lint / CI / git pre-commit 均可用）。

契约编号：FIN-SNAP-CACHE-20261011（见 app.py 中「快照缓存」区块注释）

为什么需要这个硬锁：
  财务表刷新慢的根因是 GET /api/finance/vn-report/snapshot 每次都拿 openpyxl
  把整本 xlsx 重新转成 Univer 快照（实测 4~5 s）。修法是按「源 xlsx 的 mtime+大小」
  缓存转换结果，命中就直接发缓存文件；浏览器带 If-None-Match/If-Modified-Since 时
  直接 304，连 JSON 都不用再传。以下每一条都对应一次实测踩到的坑，缺一条就会
  「读到旧数据」或「白缓存」，两者都比慢更糟：

  ① 缓存键必须同时包含源文件的 mtime 与 size（只按文件名/只按 mtime 都会误命中）。
  ② 任何改写 FIN_REPORT 的地方都必须调用 _fin_cache_invalidate()，且失效必须删键文件：
     fin_save_report / fin_init_report / fin_save_snapshot。漏一处 → 用户看到旧表。
  ③ 落盘必须原子、且【先快照、后键文件】：
     · 快照文件名必须由缓存键派生（_fin_cache_name）——重建写的是新文件名，
       绝不覆盖可能正被上一次响应读着的旧文件；
       ★ Windows 实测：固定文件名 + os.replace 覆盖会因目标正被读而
         WinError 5 Access denied → 500（_fin_snap_test.py 第 4 步抓到）。
     · 快照用 .part + os.replace 就位；键文件也要 .tmp + os.replace。
     · 顺序不可颠倒，否则可能「有键但无完整快照」。
  ④ GET 必须走缓存判定（_fin_cache_current / _fin_cache_build），不得再直接调用
     univer_convert.xlsx_to_univer（那就是「每次刷新都重新加载」的原始 BUG）。
  ⑤ 出缓存必须带 conditional=True，让重复加载退化为 304。
  ⑥ 缓存【必须带内容指纹】（FIN-SNAP-FP-20261015）：快照落盘后把 sha256 写进 .fp，
     判定缓存时重新比对；缺指纹/对不上（被手改、半截、损坏）一律判未命中、从 xlsx 重转。
     ★血案：2026-10-15 一次性脚本直接把 off-by-one 的余额公式烘焙进快照 JSON，
       缓存键只比 xlsx 的 mtime+size → 手改内容照样命中下发，
       前端 #VALUE! 怎么改 choice_lite.html 都修不掉。

用法：
  python3 check_fin_snap_cache.py [path/to/app.py]
  python3 check_fin_snap_cache.py --selftest     # 反向测试：篡改临时副本，必须全被拦下
退出码：0 = 通过；1 = 契约被破坏（CI 失败 / pre-commit 拦截）。
"""
import os
import re
import shutil
import sys
import tempfile

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

DOC_ID = "FIN-SNAP-CACHE-20261011"
WRITE_POINTS = ("fin_save_report", "fin_init_report", "fin_save_snapshot")
CACHE_FNS = ("_fin_report_key", "_fin_cache_name", "_fin_cache_current",
             "_fin_cache_valid", "_fin_cache_invalidate", "_fin_cache_build")


def strip_py_comments(s):
    """去掉 `#` 注释（不碰字符串里的 #）。代码判定一律在剥完注释的文本上做。"""
    out = []
    for ln in s.split("\n"):
        q = None
        for i, ch in enumerate(ln):
            if q:
                if ch == q:
                    q = None
            elif ch in "\"'":
                q = ch
            elif ch == "#":
                ln = ln[:i]
                break
        out.append(ln)
    return "\n".join(out)


def py_body(text, name):
    """按缩进取出 `def <name>(...)` 的函数体，找不到返回 None。"""
    m = re.search(r"^(?P<ind>[ \t]*)def\s+" + re.escape(name) + r"\s*\(", text, re.M)
    if not m:
        return None
    ind = len(m.group("ind"))
    lines = text[m.start():].split("\n")
    out = [lines[0]]
    for ln in lines[1:]:
        if not ln.strip():
            out.append(ln)
            continue
        if len(ln) - len(ln.lstrip(" \t")) <= ind:
            break
        out.append(ln)
    return "\n".join(out)


def check_app(path):
    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()
    code = strip_py_comments(text)
    errors = []
    warnings = []

    # ---- 标记与常量 ----
    if DOC_ID not in text:
        errors.append("找不到锁标记 %s（快照缓存区块被删除？）" % DOC_ID)
    for nm in ("FIN_SNAP_KEY", "FIN_SNAP_PREFIX", "_FIN_SNAP_LOCK"):
        if not re.search(r"^%s\s*=" % re.escape(nm), code, re.M):
            errors.append("找不到 %s 定义（缓存区块被删除？）" % nm)

    # ---- ① 缓存键 = mtime + size ----
    key = py_body(code, "_fin_report_key")
    if key is None:
        errors.append("不变量①被破坏：找不到 _fin_report_key()")
    else:
        if "st_mtime_ns" not in key:
            errors.append("不变量①被破坏：缓存键不再包含源文件的 mtime（st_mtime_ns）")
        if "st_size" not in key:
            errors.append("不变量①被破坏：缓存键不再包含源文件大小（st_size）"
                          "（只按 mtime 会在同秒改写时误命中）")

    # ---- ③ 落盘：键派生命名 + 原子 + 先快照后键 ----
    namef = py_body(code, "_fin_cache_name")
    if namef is None:
        errors.append("不变量③被破坏：找不到 _fin_cache_name()"
                      "（快照文件名必须由缓存键派生，否则重建会覆盖正被读的文件 → WinError 5）")
    elif "FIN_SNAP_PREFIX" not in namef:
        errors.append("不变量③被破坏：_fin_cache_name 不再基于 FIN_SNAP_PREFIX 派生文件名")

    build = py_body(code, "_fin_cache_build")
    if build is None:
        errors.append("找不到 _fin_cache_build()（缓存构建入口被删除？）")
    else:
        if not re.search(r"path\s*=\s*os\.path\.join\(\s*FIN_DIR\s*,\s*_fin_cache_name\s*\(", build):
            errors.append("不变量③被破坏：快照文件路径不再由 _fin_cache_name(key) 派生"
                          "（回到固定文件名就会在重建时 WinError 5）")
        if not re.search(r"os\.replace\(\s*part\s*,\s*path\s*\)", build):
            errors.append("不变量③被破坏：快照不再原子就位（缺 os.replace(part, path)）")
        if "json.dump" not in build:
            errors.append("不变量③被破坏：_fin_cache_build 不再序列化快照（json.dump）")
        i_snap = build.find("os.replace(part, path)")
        m_key = re.search(r"os\.replace\(\s*tmp_key\s*,\s*FIN_SNAP_KEY\s*\)", build)
        if m_key is None:
            errors.append("不变量③被破坏：键文件不再原子替换（缺 os.replace(tmp_key, FIN_SNAP_KEY)）")
        elif i_snap >= 0 and m_key.start() < i_snap:
            errors.append("不变量③被破坏：键文件写在快照【之前】"
                          "（必须先快照后键，否则可能「有键但无完整快照」）")

    for nm in CACHE_FNS:
        if py_body(code, nm) is None:
            errors.append("找不到缓存函数 %s（被删除？）" % nm)

    # ---- ② 失效必须删键文件 ----
    inv = py_body(code, "_fin_cache_invalidate")
    if inv is None:
        errors.append("找不到 _fin_cache_invalidate()（失效入口被删除？）")
    elif not re.search(r"os\.remove\(\s*FIN_SNAP_KEY\s*\)", inv):
        errors.append("不变量②被破坏：_fin_cache_invalidate 不再删键文件"
                      "（键还在 → 旧快照仍被判为有效 → 读到旧表）")

    # ---- ④⑤ GET 必须走缓存 ----
    get = py_body(code, "fin_get_snapshot")
    if get is None:
        errors.append("找不到 fin_get_snapshot（快照接口被删除？）")
    else:
        if "xlsx_to_univer" in get:
            errors.append("不变量④被破坏：fin_get_snapshot 又直接调用 univer_convert.xlsx_to_univer"
                          "（这正是「每次刷新都重新解析 xlsx」的原始 BUG）")
        if "_fin_cache_current" not in get:
            errors.append("不变量④被破坏：fin_get_snapshot 不再判定缓存（缺 _fin_cache_current()）")
        if "_fin_cache_build" not in get:
            errors.append("不变量④被破坏：fin_get_snapshot 未命中时不再构建缓存（缺 _fin_cache_build()）")
        if not re.search(r"conditional\s*=\s*True", get):
            errors.append("不变量⑤被破坏：快照不再以 conditional=True 发出"
                          "（浏览器无法 304，每次都要重传整份 JSON）")
        if not re.search(r"send_from_directory\(\s*FIN_DIR\s*,", get):
            errors.append("不变量⑤被破坏：fin_get_snapshot 不再发送缓存文件")

    # ---- ⑥ 内容指纹（FIN-SNAP-FP-20261015）:防"绕过转换器手改缓存"再被下发 ----
    if not re.search(r"^FIN_SNAP_FP\s*=", code, re.M):
        errors.append("不变量⑥被破坏：找不到 FIN_SNAP_FP 定义"
                      "（快照必须带内容指纹，否则手改过的缓存会被当成有效数据下发）")
    cur = py_body(code, "_fin_cache_current")
    if cur is None:
        errors.append("不变量⑥被破坏：找不到 _fin_cache_current()")
    elif "_fin_snap_fp_ok(" not in cur:
        errors.append("不变量⑥被破坏：_fin_cache_current 不再校验快照内容指纹（缺 _fin_snap_fp_ok()）"
                      "→ 手改/损坏的快照会被判为命中并下发")
    if py_body(code, "_fin_snap_fp_ok") is None:
        errors.append("不变量⑥被破坏：找不到 _fin_snap_fp_ok()")
    if py_body(code, "_fin_snap_sha256") is None:
        errors.append("不变量⑥被破坏：找不到 _fin_snap_sha256()")
    if build is not None:
        if "_fin_snap_sha256(" not in build:
            errors.append("不变量⑥被破坏：_fin_cache_build 不再计算快照指纹（缺 _fin_snap_sha256()）")
        m_fp = re.search(r"os\.replace\(\s*tmp_fp\s*,\s*FIN_SNAP_FP\s*\)", build)
        if m_fp is None:
            errors.append("不变量⑥被破坏：指纹文件不再原子就位（缺 os.replace(tmp_fp, FIN_SNAP_FP)）")
        elif i_snap >= 0 and m_fp.start() < i_snap:
            errors.append("不变量⑥被破坏：指纹写在快照【之前】（必须先快照、再指纹、最后切键）")
        elif m_key is not None and m_fp.start() > m_key.start():
            errors.append("不变量⑥被破坏：指纹写在键文件【之后】"
                          "（否则可能「有键但没对得上的指纹」→ 每次 GET 都白重建）")
    if inv is not None and "os.remove(FIN_SNAP_FP)" not in inv:
        errors.append("不变量⑥被破坏：_fin_cache_invalidate 不再删除指纹文件"
                      "（源文件改了、指纹还在，会误判有效）")

    # ---- ② 三个写入点 ----
    for nm in WRITE_POINTS:
        body = py_body(code, nm)
        if body is None:
            errors.append("找不到写入函数 %s（被改名/删除？）" % nm)
            continue
        if "_fin_cache_invalidate()" not in body:
            errors.append("不变量②被破坏：%s 改写 FIN_REPORT 后没有调用 _fin_cache_invalidate()"
                          "（刷新会读到旧快照）" % nm)

    # 兜底提醒：别处是否还有直接写 FIN_REPORT 而没失效缓存的代码
    spans = []
    for nm in WRITE_POINTS:
        body = py_body(code, nm)
        if body:
            i = code.find(body)
            if i >= 0:
                spans.append((i, i + len(body)))
    for m in re.finditer(r"open\(\s*FIN_REPORT\s*,\s*['\"](?:wb|w)['\"]", code):
        w = m.start()
        if not any(a <= w <= b for a, b in spans):
            warnings.append("第 %d 行有直接写 FIN_REPORT 的代码，确认它属于已知写入点之一"
                            % (code.count("\n", 0, w) + 1))

    return errors, warnings


# ======================= 反向测试 =======================
def _rep(old, new):
    def _f(t):
        assert old in t, "篡改目标不存在: %r" % old
        return t.replace(old, new)
    return _f


CASES = [
    ("① 缓存键丢掉 mtime", _rep('"%d:%d:%s" % (st.st_mtime_ns, st.st_size, FIN_REPORT)',
                               '"%d:%s" % (st.st_size, FIN_REPORT)')),
    ("① 缓存键丢掉 size", _rep('"%d:%d:%s" % (st.st_mtime_ns, st.st_size, FIN_REPORT)',
                              '"%d:%s" % (st.st_mtime_ns, FIN_REPORT)')),

    ("② fin_save_report 不再失效缓存", _rep(
        '    _fin_daily_backup()\n    _fin_cache_invalidate()   # ★源文件已改写：必须丢掉旧快照缓存\n',
        '    _fin_daily_backup()\n')),
    ("② fin_init_report 不再失效缓存", _rep(
        '    _fin_cache_invalidate()   # ★新种子：丢掉旧快照缓存\n', '')),
    ("② fin_save_snapshot 不再失效缓存", _rep(
        '        _fin_cache_invalidate()   # ★快照已写回 xlsx：丢掉旧快照缓存\n', '')),
    ("② 失效不再删键文件", _rep("        os.remove(FIN_SNAP_KEY)\n",
                                "        pass\n")),

    ("③ 快照文件名不再由缓存键派生（回到固定名）", _rep(
        "        path = os.path.join(FIN_DIR, _fin_cache_name(key))\n",
        "        path = os.path.join(FIN_DIR, FIN_SNAP_PREFIX + \"cur.json\")\n")),
    ("③ 快照不再原子就位", _rep("            os.replace(part, path)",
                               "            shutil.copyfile(part, path)")),
    ("③ 键文件写在快照之前", _rep(
        "            os.replace(part, path)          # 新文件名，不可能撞上正被读的旧文件\n"
        "            # ★写内容指纹（FIN-SNAP-FP-20261015）：键切换前落好，保证「有键必有对得上的指纹」\n"
        "            with open(tmp_fp, \"w\", encoding=\"utf-8\") as fh:\n"
        "                fh.write(_fin_snap_sha256(path))\n"
        "            os.replace(tmp_fp, FIN_SNAP_FP)\n"
        "            with open(tmp_key, \"w\", encoding=\"utf-8\") as fh:\n"
        "                fh.write(key)\n"
        "            os.replace(tmp_key, FIN_SNAP_KEY)   # 键文件最后才切（它从不对外发送）\n",
        "            with open(tmp_fp, \"w\", encoding=\"utf-8\") as fh:\n"
        "                fh.write(_fin_snap_sha256(path))\n"
        "            os.replace(tmp_fp, FIN_SNAP_FP)\n"
        "            with open(tmp_key, \"w\", encoding=\"utf-8\") as fh:\n"
        "                fh.write(key)\n"
        "            os.replace(tmp_key, FIN_SNAP_KEY)   # 键文件最后才切（它从不对外发送）\n"
        "            os.replace(part, path)          # 新文件名，不可能撞上正被读的旧文件\n")),

    ("④ fin_get_snapshot 又直接解析 xlsx", _rep(
        "    _snap_key, _snap_path = _fin_cache_current()\n",
        "    snap = univer_convert.xlsx_to_univer(FIN_REPORT)\n    return jsonify(snap)\n"
        "    _snap_key, _snap_path = None, None\n")),
    ("④ fin_get_snapshot 不再判定缓存", _rep(
        "    _snap_key, _snap_path = _fin_cache_current()\n",
        "    _snap_key, _snap_path = None, None\n")),
    ("⑤ 出缓存不再 conditional（无法 304）", _rep(
        'mimetype="application/json", conditional=True)',
        'mimetype="application/json")')),
    ("⑤ 不再发送缓存文件", _rep(
        "    resp = send_from_directory(FIN_DIR, os.path.basename(_snap_path),\n",
        "    resp = jsonify({})\n    return resp\n")),

    ("⑥ 判定缓存不再校验内容指纹（手改的缓存会被下发）", _rep(
        "    if not _fin_snap_fp_ok(path):\n        return key, None          # ★被手改/半截/损坏 → 判未命中，重新转换\n",
        "")),
    ("⑥ 构建时不再写指纹", _rep(
        "            with open(tmp_fp, \"w\", encoding=\"utf-8\") as fh:\n"
        "                fh.write(_fin_snap_sha256(path))\n"
        "            os.replace(tmp_fp, FIN_SNAP_FP)\n",
        "")),
    ("⑥ 失效时不再删指纹", _rep(
        "    try:\n        os.remove(FIN_SNAP_FP)      # ★内容指纹一并作废（FIN-SNAP-FP-20261015）\n"
        "    except OSError:\n        pass\n",
        "")),
]


def selftest(app_path):
    tmp = tempfile.mkdtemp(prefix="fin_snap_negtest_")
    try:
        dst = os.path.join(tmp, "app.py")
        base = open(app_path, encoding="utf-8").read()

        open(dst, "wb").write(base.encode("utf-8"))
        errs, _ = check_app(dst)
        if errs:
            print("✗ 对照组失败：未改动的 app.py 竟然报错：")
            for e in errs:
                print("   ", e)
            return 2
        print("对照组（未改动）→ 通过 ✔")
        print("-" * 78)

        leaked = []
        for name, fn in CASES:
            t = fn(base)
            open(dst, "wb").write(t.encode("utf-8"))
            errs, _ = check_app(dst)
            if errs:
                print("拦截 ✔  %s" % name)
                print("        → %s" % errs[0])
            else:
                print("漏过 ✗  %s" % name)
                leaked.append(name)
        print("-" * 78)
        if leaked:
            print("✗ 反向测试失败：%d/%d 种篡改没被拦住 → %s" % (len(leaked), len(CASES), leaked))
            return 1
        print("✓ 反向测试通过：%d 种篡改全部被硬锁拦截。" % len(CASES))
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    args = [a for a in sys.argv[1:] if a != "--selftest"]
    app_path = args[0] if args else os.path.join(here, "app.py")
    if not os.path.exists(app_path):
        print("✗ 找不到文件: %s" % app_path)
        return 1
    if "--selftest" in sys.argv[1:]:
        return selftest(app_path)
    errors, warnings = check_app(app_path)
    print("检查目标: %s" % app_path)
    for w in warnings:
        print("  ! 警告: %s" % w)
    if not errors:
        print("✓ 通过：财务快照缓存锁定契约未被破坏（%s 六条不变量全在）" % DOC_ID)
        return 0
    for e in errors:
        print("  ✗ 违规: %s" % e)
    print("✗ 失败：共 %d 处违规。这是「锁死」契约，禁止篡改；"
          "请恢复 %s 的不变量后再提交。" % (len(errors), DOC_ID))
    return 1


if __name__ == "__main__":
    sys.exit(main())
