# -*- coding: utf-8 -*-
"""把 Univer 0.5.5 的 esm.sh ESM 依赖图镜像到本地 vendor/univer/，并改写 import map。

为什么：财务页每次整页加载都要从 esm.sh 现场拉 320 个模块再装配，实测稳定吃掉
6.9~7.4 秒（会话内切标签页只要 0.02s）。本地化之后这些模块从本机/局域网取，
配合 immutable 长缓存，刷新时几乎不再有网络往返，而且彻底断网也能用。

做法：
  1) 从 choice_lite.html 的 importmap + 所有 import('@univerjs/...') 里收集入口
  2) 递归抓取（含 CSS），把每条 https://esm.sh/... 存成 vendor/univer/<名>__<哈希>.<ext>
  3) 把文件里所有 esm.sh 引用改写成 /vendor/univer/<名>
  4) 生成 vendor/univer/_map.json；--patch-html 时改写 choice_lite.html 的 importmap 与 5 个 CSS link

用法：
  python _vendor_univer.py                 # 只镜像，不改 HTML
  python _vendor_univer.py --patch-html    # 镜像 + 改写 choice_lite.html
"""
import hashlib
import json
import os
import re
import shutil
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(HERE, "choice_lite.html")
OUTDIR = os.path.join(HERE, "vendor", "univer")
OUTURL = "/vendor/univer/"
MAPFILE = os.path.join(OUTDIR, "_map.json")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

URL_RE = re.compile(r"https://esm\.sh/[^\s\"'`()<>\\]+")
SPEC_RE = re.compile(r"""import\s*\(\s*['"]([^'"]+)['"]\s*\)|from\s*['"]([^'"]+)['"]""")
IMPORTMAP_RE = re.compile(r"<script\s+type=\"importmap\">(.*?)</script>", re.S)


# ---------- 1) 从 HTML 收集入口 ----------
def load_importmap(html):
    m = IMPORTMAP_RE.search(html)
    if not m:
        raise SystemExit("✗ 找不到 importmap")
    return json.loads(m.group(1))["imports"]


def resolve(spec, imports):
    """按 importmap 规则解析裸模块名 → URL（支持末尾 / 前缀映射）。"""
    if spec in imports:
        return imports[spec]
    for k in sorted(imports, key=len, reverse=True):
        if k.endswith("/") and spec.startswith(k):
            return imports[k] + spec[len(k):]
    return None


def collect_entries(html, imports):
    specs = set()
    for m in SPEC_RE.finditer(html):
        s = m.group(1) or m.group(2)
        if s and s.startswith("@univerjs/"):
            specs.add(s)
    urls = []
    for s in sorted(specs):
        u = resolve(s, imports)
        if u:
            urls.append((s, u))
        else:
            print("  ! 无法解析（跳过）: %s" % s)
    # importmap 里显式列出的（可能没有对应 import() 调用）
    for k, v in imports.items():
        if k.startswith("@univerjs/") and not k.endswith("/"):
            if v not in [u for _, u in urls]:
                urls.append((k, v))
    return urls


def local_name(url):
    m = re.match(r"https://esm\.sh/(.*)$", url)
    tail = m.group(1) if m else url
    tail = tail.split("?")[0]
    ext = ".js"
    mm = re.search(r"\.(mjs|js|cjs|css|json)$", tail)
    if mm:
        ext = "." + mm.group(1)
        tail = tail[: -len(ext)]
    safe = re.sub(r"[^A-Za-z0-9._@-]", "_", tail)[:80]
    h = hashlib.sha1(url.encode("utf-8")).hexdigest()[:8]
    return "%s__%s%s" % (safe, h, ext)


# ---------- 2) 抓取 ----------
def fetch(url, retries=3):
    last = None
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            if e.code in (404, 410):
                return e.code, b""
            last = e
        except Exception as e:
            last = e
        time.sleep(0.4 * (i + 1))
    raise last if last else RuntimeError("fetch failed")


def main():
    patch_html = "--patch-html" in sys.argv
    html = open(HTML, encoding="utf-8").read()
    imports = load_importmap(html)

    os.makedirs(OUTDIR, exist_ok=True)
    entries = collect_entries(html, imports)
    print("入口 %d 个：" % len(entries))
    for s, u in entries:
        print("   %-50s → %s" % (s, u))

    # 待抓队列（URL）；已抓 = 本地已落盘
    todo = [u for _, u in entries]
    # 追加 5 个 CSS
    for m in re.finditer(r'<link rel="stylesheet" href="(https://esm\.sh/[^"]+)"', html):
        todo.append(m.group(1))

    seen, failed = {}, {}
    done_count = 0
    while todo:
        batch = []
        for u in todo:
            if u in seen or u in failed:
                continue
            seen[u] = local_name(u)
            batch.append(u)
        todo = []
        if not batch:
            break
        print("\n抓取 %d 个…" % len(batch))
        with ThreadPoolExecutor(max_workers=8) as ex:
            for url, res in zip(batch, ex.map(lambda u: (fetch(u) if not os.path.exists(
                    os.path.join(OUTDIR, seen[u])) or os.path.getsize(os.path.join(OUTDIR, seen[u])) == 0
                    else (200, None)), batch)):
                status, body = res
                path = os.path.join(OUTDIR, seen[url])
                if body is None:
                    body = open(path, "rb").read()
                if status != 200 or not body:
                    failed[url] = status
                    print("   ✗ %s (%s)" % (status, url[:90]))
                    continue
                open(path, "wb").write(body)
                done_count += 1
                # 找新依赖
                try:
                    text = body.decode("utf-8", "replace")
                except Exception:
                    text = ""
                for dep in set(URL_RE.findall(text)):
                    dep = dep.rstrip(".,;\\")
                    if dep not in seen and dep not in failed:
                        todo.append(dep)
        print("   已落盘 %d 个文件" % done_count)

    # ---------- 3) 改写引用 ----------
    print("\n改写引用…")
    rewritten = 0
    leftovers = 0
    for url, name in sorted(seen.items()):
        path = os.path.join(OUTDIR, name)
        if not os.path.exists(path):
            continue
        raw = open(path, "rb").read()
        text = raw.decode("utf-8", "replace")
        if "esm.sh" not in text:
            continue

        def sub(m):
            u = m.group(0).rstrip(".,;\\")
            suffix = m.group(0)[len(u):]
            if u in seen and os.path.exists(os.path.join(OUTDIR, seen[u])):
                return OUTURL + seen[u] + suffix
            return m.group(0)

        new = URL_RE.sub(sub, text)
        if new != text:
            open(path, "wb").write(new.encode("utf-8"))
            rewritten += 1
        left = len(URL_RE.findall(new))
        leftovers += left

    print("   改写文件 %d 个；残留 esm.sh 引用 %d 处" % (rewritten, leftovers))

    json.dump({"entries": {s: OUTURL + seen[u] for s, u in entries if u in seen and u not in failed},
               "css": {u: OUTURL + seen[u] for u in seen if seen[u].endswith(".css")},
               "all": seen, "failed": failed},
              open(MAPFILE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    total = 0
    n = 0
    for fn in os.listdir(OUTDIR):
        p = os.path.join(OUTDIR, fn)
        if os.path.isfile(p):
            total += os.path.getsize(p)
            n += 1
    print("\n本地化完成：%d 个文件 / %.1f MB → %s" % (n, total / 1048576.0, OUTDIR))
    print("清单：%s" % MAPFILE)
    if failed:
        print("失败 %d 个（可重跑会自动重试）：" % len(failed))
        for u, s in list(failed.items())[:10]:
            print("   %s %s" % (s, u[:100]))

    # ---------- 4) 改写 HTML ----------
    if patch_html:
        bak = HTML + ".bak_before_vendor_univer"
        if not os.path.exists(bak):
            shutil.copyfile(HTML, bak)
        h = html
        for s, u in entries:
            if u in failed or u not in seen:
                continue
            h = h.replace('"%s"' % u, '"%s"' % (OUTURL + seen[u]))
        for u, name in sorted(seen.items()):
            if name.endswith(".css") and u not in failed:
                h = h.replace('href="%s"' % u, 'href="%s"' % (OUTURL + name))
        open(HTML, "wb").write(h.encode("utf-8"))
        print("已改写 %s（备份 %s）" % (os.path.basename(HTML), os.path.basename(bak)))


if __name__ == "__main__":
    main()
