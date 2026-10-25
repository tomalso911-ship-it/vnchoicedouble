# -*- coding: utf-8 -*-
"""快速探查：服务端真正吐出来的 choice_lite.html 是不是当前文件？财务脚本块完整吗？
（结果写 _cn_html_probe_out.txt，不起浏览器）"""
import io
import os
import re
import socket
import sys
import threading
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.join(HERE, "_cn_html_probe_out.txt")
L = []


def log(s):
    L.append(str(s))
    io.open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")


def port_open(port):
    s = socket.socket()
    s.settimeout(0.6)
    try:
        s.connect(("127.0.0.1", port))
        return True
    except Exception:
        return False
    finally:
        s.close()


import app  # noqa: E402

PORT = 5153
if not port_open(PORT):
    threading.Thread(target=lambda: app.app.run(host="127.0.0.1", port=PORT, debug=False,
                                                use_reloader=False, threaded=True),
                     daemon=True).start()
    for _ in range(60):
        if port_open(PORT):
            break
        time.sleep(0.3)

log("BASE_DIR = %s" % app.BASE_DIR)
r = urllib.request.urlopen("http://127.0.0.1:%d/" % PORT, timeout=30)
html = r.read().decode("utf-8", "replace")
log("服务端吐出的 HTML 长度 = %d" % len(html))

disk = io.open(os.path.join(HERE, "choice_lite.html"), encoding="utf-8").read()
log("磁盘上 choice_lite.html 长度 = %d" % len(disk))
log("两者一致 = %s" % (html == disk))

for key in ('id="fin_workspace"', "FIN-CN-REPORT-20261013", "var FIN_KIND", "function finCnAdaptView",
            "function finCnCheckApply", "id=\"fin_status\"", "id='fin_status'"):
    log("  contains %-32r = %s (disk=%s)" % (key, key in html, key in disk))

log("script 开标签数 = %d, 闭标签数 = %d" % (html.count("<script"), html.count("</script>")))

# 找财务脚本块，检查关键语句顺序
i = html.find("财务管理三语标签页：状态与切换")
log("财务脚本块起点 = %d" % i)
if i > 0:
    seg = html[i:i + 4000]
    log("块开头 300 字:")
    log(seg[:300].replace("\n", " | "))
    # 找 <script> 前 200 字
    j = html.rfind("<script>", 0, i)
    log("紧邻的 <script> 位置 = %d (距块 %d 字符)" % (j, i - j))

# 检查是否在某个未闭合的字符串/注释里：统计块内单引号数量是否平衡
if i > 0:
    end = html.find("<!----", i)
    log("sample around FIN_KINDS:")
    k = html.find("var FIN_KINDS", i)
    log("  FIN_KINDS 位置 = %s" % k)
    if k > 0:
        log("  " + html[k - 60:k + 200].replace("\n", " | "))

# 用 node/esprima 无关的粗略检查：把财务块单独抠出来，数一下花括号是否平衡
m = html.find("<script>", i - 200)
if m > 0:
    e = html.find("</script>", i)
    block = html[m + len("<script>"):e]
    log("财务块长度 = %d, 花括号 {%d  }%d" % (len(block), block.count("{"), block.count("}")))
    log("块尾 200 字: " + block[-200:].replace("\n", " | "))

print("done")
