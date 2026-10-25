import io, re, esprima

path = r"c:/vnchoicedouble/choice_lite.html"
html = io.open(path, encoding="utf-8").read()

# ---- 1) 语法检查 ----
blocks, pos = [], 0
while True:
    m = re.search(r"<script\b([^>]*)>(.*?)</script>", html[pos:], re.S | re.I)
    if not m:
        break
    attrs, body = m.group(1), m.group(2)
    start = pos + m.start(2)
    pos = pos + m.end()
    if "src=" in attrs.lower():
        continue
    blocks.append((start, body))
bad = 0
for idx, (start, body) in enumerate(blocks):
    try:
        esprima.parseScript(body)
    except Exception as e:
        print("SYNTAX ERROR block %d (line %d): %s" % (idx, html[:start].count("\n") + 1, e))
        bad += 1
print("script blocks=%d  syntax errors=%d" % (len(blocks), bad))

# ---- 2) data-i18n 悬挂键审计 ----
lines = html.split("\n")
def slice_lines(a, b):
    return "\n".join(lines[a-1:b])

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
    return set(KEY_RE.findall(skeleton(t)))

main_keys = kset(slice_lines(18665, 19445)) | kset(slice_lines(19446, 20229)) | kset(slice_lines(20230, 21011))
prod_keys = kset(slice_lines(5271, 5367)) | kset(slice_lines(5304, 5335)) | kset(slice_lines(5336, 5367))
for m in re.finditer(r"(?:PROD_I18N|I18N)\.(?:zh|en|vi)\.([A-Za-z0-9_]+)\s*=", html):
    prod_keys.add(m.group(1))
for m in re.finditer(r"(?:PROD_I18N|I18N)\.(?:zh|en|vi)\[['\"]([A-Za-z0-9_]+)['\"]\]\s*=", html):
    prod_keys.add(m.group(1))

known = main_keys | prod_keys
print("main keys=%d  prod keys=%d" % (len(main_keys), len(prod_keys)))

dangling = {}
n_ref = 0
for m in re.finditer(r'data-i18n="([^"]+)"', html):
    n_ref += 1
    k = m.group(1)
    if k not in known:
        dangling.setdefault(k, []).append(html[:m.start()].count("\n") + 1)
print("data-i18n refs=%d  dangling(任何语言包都没有的键)=%d" % (n_ref, len(dangling)))
for k in sorted(dangling):
    print("   %-30s lines=%s" % (k, dangling[k][:10]))

# ---- 3) 只用 data-i18n 而键仅在 PROD_I18N 中（修好之后已可被全局扫描覆盖）----
only_prod = {}
for m in re.finditer(r'data-i18n="([^"]+)"', html):
    k = m.group(1)
    if k in prod_keys and k not in main_keys:
        only_prod.setdefault(k, []).append(html[:m.start()].count("\n") + 1)
print("data-i18n keys living ONLY in PROD_I18N: %d" % len(only_prod))
for k in sorted(only_prod):
    print("   %-30s lines=%s" % (k, only_prod[k][:10]))
