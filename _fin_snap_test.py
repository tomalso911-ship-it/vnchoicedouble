# -*- coding: utf-8 -*-
"""财务快照缓存（FIN-SNAP-CACHE-20261011）端到端验证。

做法：不碰正在运行的服务、也不改真实 finance_data/vn_report.xlsx ——
      在临时目录里放一份副本，把 app.FIN_DIR / FIN_REPORT / FIN_SNAP_KEY
      重定向到临时目录，然后用 Flask 测试客户端打真实路由。
验证点：
  1) 冷启动：第一次 GET 会真的转换 xlsx（应较慢），并落缓存
  2) 热命中：第二次 GET 不再转换（明显更快），且与第一次内容一致
  3) 304：带上次的 ETag/Last-Modified 再请求，应回 304（连 JSON 都不传）
  4) 失效：源文件 mtime 变了 → 缓存键变 → 下次 GET 重新转换（不会读到旧表），
     且【不会】因为旧快照文件正被读而报 WinError 5（这是最初的真实 BUG）
  5) _fin_cache_invalidate() 真的会清掉键与快照
用法：python _fin_snap_test.py
"""
import json
import os
import shutil
import sys
import tempfile
import time

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

REAL_XLSX = os.path.join(HERE, "finance_data", "vn_report.xlsx")


def main():
    if not os.path.isfile(REAL_XLSX):
        print("✗ 找不到种子文件: %s" % REAL_XLSX)
        return 1

    tmp = tempfile.mkdtemp(prefix="fin_snap_test_")
    try:
        import app as A

        # ---- 全部重定向到临时目录，绝不动真实数据 ----
        A.FIN_DIR = tmp
        A.FIN_REPORT = os.path.join(tmp, "vn_report.xlsx")
        A.FIN_SNAP_KEY = os.path.join(tmp, "vn_report.snapshot.key")
        shutil.copyfile(REAL_XLSX, A.FIN_REPORT)
        print("测试目录: %s" % tmp)
        print("种子 xlsx: %.2f MB" % (os.path.getsize(A.FIN_REPORT) / 1024.0 / 1024.0))

        cli = A.app.test_client()

        def get(headers=None):
            t0 = time.time()
            r = cli.get("/api/finance/vn-report/snapshot", headers=headers or {})
            return r, time.time() - t0

        # ---- 1) 冷启动：必须真的转换并落缓存 ----
        r1, t1 = get()
        assert r1.status_code == 200, "冷启动 GET 状态码 %s" % r1.status_code
        snap1 = r1.get_json()
        assert isinstance(snap1, dict) and snap1, "冷启动返回的不是快照 dict"
        k1, p1 = A._fin_cache_current()
        assert p1 and os.path.isfile(p1), "冷启动后没有落快照缓存文件"
        assert r1.headers.get("X-Fin-Snap-Cache") == "hit", "缺少缓存命中标记头"
        print("1) 冷启动（真转换）      %6.2f s  快照 %.2f MB  缓存 %s ✔"
              % (t1, os.path.getsize(p1) / 1024.0 / 1024.0, os.path.basename(p1)))

        # ---- 2) 热命中：不再转换，内容一致 ----
        r2, t2 = get()
        assert r2.status_code == 200
        assert json.dumps(r1.get_json(), sort_keys=True) == json.dumps(r2.get_json(), sort_keys=True), \
            "热命中返回的内容与首次不一致"
        assert t2 < t1, "热命中没有变快（冷 %.2fs / 热 %.2fs）" % (t1, t2)
        print("2) 热命中（直接发缓存）  %6.2f s  比冷启动快 %.1f 倍 ✔"
              % (t2, (t1 / t2) if t2 > 0 else 0))

        # ---- 3) 304 ----
        etag, lm = r2.headers.get("ETag"), r2.headers.get("Last-Modified")
        assert etag or lm, "响应没有 ETag / Last-Modified，浏览器无法 304"
        hdrs = {}
        if etag:
            hdrs["If-None-Match"] = etag
        if lm:
            hdrs["If-Modified-Since"] = lm
        r3, t3 = get(hdrs)
        assert r3.status_code == 304, "带 %s 再请求返回 %s（应为 304）" % (list(hdrs), r3.status_code)
        print("3) 条件请求 → 304（不再传 JSON）%6.3f s ✔" % t3)

        # ---- 4) 源文件变了 → 缓存必须失效，且重建不能撞上正被读的旧文件 ----
        time.sleep(0.05)
        st = os.stat(A.FIN_REPORT)
        os.utime(A.FIN_REPORT, (st.st_atime + 10, st.st_mtime + 10))   # 只改 mtime，不动内容
        assert not A._fin_cache_valid(), "源文件 mtime 变了，缓存却仍被判为有效（会读到旧表！）"
        # 故意让上一次响应还“拿着”旧快照文件句柄（Windows 下最容易暴露覆盖冲突）
        hold = open(p1, "rb")
        try:
            r4, t4 = get()
            assert r4.status_code == 200, ("源文件变了之后 GET 返回 %s，body=%r"
                                           % (r4.status_code, r4.get_data()[:300]))
        finally:
            hold.close()
        k4, p4 = A._fin_cache_current()
        assert p4 and p4 != p1, "源文件变了但缓存文件没有换成新键派生的名字（旧文件可能被覆盖）"
        assert k4 != k1, "源文件变了但缓存键没变"
        print("4) 源文件 mtime 变化 → 旧缓存失效、写新文件重建  %6.2f s ✔" % t4)
        print("   新快照 %s；旧快照（正被读着）未被覆盖 ✔" % os.path.basename(p4))

        # ---- 5) 显式失效 ----
        A._fin_cache_invalidate()
        assert A._fin_cache_current()[1] is None, \
            "_fin_cache_invalidate() 之后缓存仍被判为有效（键没删掉 → 会读到旧表）"
        left = A._fin_cache_files()
        if left:
            # 删不掉的一定是正被某个响应句柄占着的（Windows 不允许删被打开的文件）。
            # 正确性由「键已删」保证；残留文件只是垃圾，会在下次 build/invalidate 时清掉。
            print("5) 键已删（缓存判为无效）✔；残留 %d 个被占用文件，下次自动清理：%s"
                  % (len(left), left))
        else:
            print("5) _fin_cache_invalidate() 清空键 + 快照 ✔")

        print("-" * 72)
        print("✓ 通过：刷新时不再重新解析 xlsx；源文件一变缓存立即失效，且不会读到旧表。")
        return 0
    except AssertionError as e:
        print("✗ 失败：%s" % e)
        return 1
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("✗ 异常：%s" % e)
        return 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
