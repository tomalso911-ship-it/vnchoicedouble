# -*- coding: utf-8 -*-
"""探针 2：拉 Univer 0.5.5 sheets-ui 的三语 locale，找出「选择全部」这条菜单/快捷键文案的
真实 key 与中/英/越三种写法（用于右键菜单项精准匹配）。只读，不改仓库文件。"""
import re
import sys
import urllib.request

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

LANGS = ["zh-CN", "en-US", "vi-VN"]
BASES = [
    "https://esm.sh/@univerjs/sheets-ui@0.5.5/locales/%s",
    "https://esm.sh/@univerjs/presets@0.5.5/preset-sheets-core/locales/%s",
]

KEYS = re.compile(r"select", re.I)


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", "replace")


def main():
    for base in BASES:
        for lg in LANGS:
            url = base % lg
            try:
                t = fetch(url)
            except Exception as e:
                print("!! %s -> %s" % (url, e))
                continue
            print("=" * 90)
            print("%s (%d chars)" % (url, len(t)))
            # 抓 "key":"value" 里 key 或 value 含 select / 全选 的条目
            for m in re.finditer(r'"([^"]{0,80})"\s*:\s*"([^"]{0,80})"', t):
                k, v = m.group(1), m.group(2)
                if KEYS.search(k) or "全选" in v or "选择全部" in v:
                    print("   %-46s = %s" % (k, v))
            # 非 JSON 模块时退化成整段里搜「全选」
            for m in re.finditer("全选|选择全部|Select all|Chọn tất cả", t):
                s = max(0, m.start() - 120)
                print("   ~ %s" % t[s:m.end() + 120].replace("\n", " "))


if __name__ == "__main__":
    main()
