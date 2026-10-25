# -*- coding: utf-8 -*-
"""探针：确认 @univerjs/core 的 CommandService 里 beforeCommandExecuted 监听器
拿到的是【同一个 command 对象】、且在 handler 之前执行（这样才能改 params）。
只读，不改仓库文件。"""
import re
import sys
import urllib.request

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
URL = "https://esm.sh/@univerjs/core@0.5.5/es2022/core.mjs"


def main():
    req = urllib.request.Request(URL, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=120) as r:
        t = r.read().decode("utf-8", "replace")
    print("%s (%d chars)" % (URL, len(t)))
    for m in re.finditer(r"_beforeCommandExecutionListeners", t):
        s = max(0, m.start() - 500)
        e = min(len(t), m.end() + 700)
        print("-" * 90)
        print(t[s:e].replace("\n", " "))


if __name__ == "__main__":
    main()
