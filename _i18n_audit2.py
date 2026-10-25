import io, re

path = r"c:/vnchoicedouble/choice_lite.html"
html = io.open(path, encoding="utf-8").read()
lines = html.split("\n")

def slice_lines(a, b):
    return "\n".join(lines[a-1:b])

zh, en, vi = slice_lines(18665, 19445), slice_lines(19446, 20229), slice_lines(20230, 21011)
PROD_zh, PROD_en, PROD_vi = slice_lines(5271, 5303), slice_lines(5304, 5335), slice_lines(5336, 5367)

def skeleton(s):
    out = list(s); i = 0; n = len(s)
    while i < n:
        c = s[i]; nx = s[i+1] if i+1 < n else ""
        if c == "/" and nx == "/":
            while i < n and s[i] != "\n": i += 1
            continue
        if c == "/" and nx == "*":
            i += 2
            while i < n and not (s[i] == "*" and i+1 < n and s[i+1] == "/"): i += 1
            i += 2
            continue
        if c in ("'", '"', "`"):
            q = c; j = i+1
            while j < n:
                if s[j] == "\\": j += 2; continue
                if s[j] == q: j += 1; break
                j += 1
            for k in range(i+1, max(i+1, j-1)):
                if out[k] != "\n": out[k] = " "
            i = j
            continue
        i += 1
    return "".join(out)

KEY_RE = re.compile(r"([A-Za-z_$][A-Za-z0-9_$]*)\s*:")
def kset(t):
    # 合并对象字面量 + 后续 xxx_I18N.zh.KEY = '...' 赋值 由单独正则处理
    return set(KEY_RE.findall(skeleton(t)))

main_keys = kset(zh) | kset(en) | kset(vi)
# 语言包里的 ['key'] 形式（含 zh.assign 之类）
for m in re.finditer(r"PROD_I18N\.(?:zh|en|vi)(?:\[['\"]([A-Za-z0-9_]+)['\"]\]|\.([A-Za-z0-9_]+))\s*=", html):
    pass
assigned = set()
for m in re.finditer(r"(?:PROD_I18N|I18N)\.(?:zh|en|vi)\.([A-Za-z0-9_]+)\s*=", html):
    assigned.add(m.group(1))
for m in re.finditer(r"(?:PROD_I18N|I18N)\.(?:zh|en|vi)\[['\"]([A-Za-z0-9_]+)['\"]\]\s*=", html):
    assigned.add(m.group(1))
assigned_main = set()
for m in re.finditer(r"\bI18N\.(?:zh|en|vi)\.([A-Za-z0-9_]+)\s*=", html):
    assigned_main.add(m.group(1))
main_keys |= assigned_main

prod_keys = kset(PROD_zh) | kset(PROD_en) | kset(PROD_vi) | assigned

rep = []
rep.append("main I18N keys: %d   PROD_I18N keys: %d" % (len(main_keys), len(prod_keys)))

# 1) data-i18n 引用
refs = []
for m in re.finditer(r'data-i18n="([^"]+)"', html):
    refs.append((m.group(1), html[:m.start()].count("\n") + 1))
rep.append("")
rep.append("=== 1) data-i18n 引用中，主 I18N 里【不存在】的键 ===")
bad = {}
for k, ln in refs:
    if k not in main_keys:
        bad.setdefault(k, []).append(ln)
for k in sorted(bad):
    rep.append("   %-28s 行 %s" % (k, bad[k][:12]))

rep.append("")
rep.append("=== 2) pt('key') 引用中，PROD_I18N 里【不存在】的键 ===")
bad2 = {}
for m in re.finditer(r"\bpt\(\s*'([A-Za-z0-9_]+)'\s*\)", html):
    k = m.group(1)
    if k not in prod_keys and k not in main_keys:
        bad2.setdefault(k, []).append(html[:m.start()].count("\n") + 1)
for k in sorted(bad2):
    rep.append("   %-28s 行 %s" % (k, bad2[k][:12]))

rep.append("")
rep.append("=== 3) 生产模块里直接用原始猪舍值渲染（未走 prod_phName）的可疑行 ===")
for i, ln in enumerate(lines, 1):
    if "houseOrder" in ln and "prod_phName" not in ln and ("join(" in ln or "textContent" in ln or "innerHTML" in ln):
        rep.append("   L%-6d %s" % (i, ln.strip()[:190]))

io.open(r"c:/vnchoicedouble/_i18n_audit2_out.txt", "w", encoding="utf-8").write("\n".join(rep))
print("written:", len(rep))
