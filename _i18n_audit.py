import io, re

path = r"c:/vnchoicedouble/choice_lite.html"
html = io.open(path, encoding="utf-8").read()
lines = html.split("\n")

def skeleton(s):
    out = list(s)
    i, n = 0, len(s)
    while i < n:
        c = s[i]
        nxt = s[i+1] if i+1 < n else ""
        if c == "/" and nxt == "/":
            j = i
            while j < n and s[j] != "\n":
                j += 1
            for k in range(i, j):
                out[k] = " "
            i = j
            continue
        if c == "/" and nxt == "*":
            j = i + 2
            while j < n and not (s[j] == "*" and j+1 < n and s[j+1] == "/"):
                j += 1
            j = min(n, j + 2)
            for k in range(i, j):
                if out[k] != "\n":
                    out[k] = " "
            i = j
            continue
        if c in ("'", '"', "`"):
            q = c
            j = i + 1
            while j < n:
                if s[j] == "\\":
                    j += 2
                    continue
                if s[j] == q:
                    j += 1
                    break
                j += 1
            for k in range(i + 1, max(i + 1, j - 1)):
                if out[k] != "\n":
                    out[k] = " "
            i = j
            continue
        i += 1
    return "".join(out)

skel = skeleton(html)

BLOCK_RE = re.compile(r"(?<![A-Za-z0-9_$])(zh|en|vi)\s*:\s*\{")
blocks = []
for m in BLOCK_RE.finditer(skel):
    # 花括号配对
    depth = 0
    j = skel.index("{", m.start())
    k = j
    while k < len(skel):
        if skel[k] == "{":
            depth += 1
        elif skel[k] == "}":
            depth -= 1
            if depth == 0:
                break
        k += 1
    blocks.append((m.group(1), j, k + 1))

# 分组：连续且语言不重复
groups, cur = [], []
for b in blocks:
    if b[0] in [x[0] for x in cur]:
        if cur:
            groups.append(cur)
        cur = [b]
    else:
        cur.append(b)
if cur:
    groups.append(cur)

VAL_RE = re.compile(r"([A-Za-z_$][A-Za-z0-9_$]*)\s*:\s*")
VN_DIA = "ăâđêôơưáàảãạấầẩẫậắằẳẵặéèẻẽẹếềểễệíìỉĩịóòỏõọốồổỗộớờởỡợúùủũụứừửữựýỳỷỹỵ"

def block_data(b):
    lang, s, e = b
    seg_s, seg_k = skel[s:e], html[s:e]
    out = {}
    for m in VAL_RE.finditer(seg_s):
        key = m.group(1)
        rest = seg_k[m.end():].lstrip()
        if rest.startswith('"') or rest.startswith("'"):
            q = rest[0]
            i = 1
            buf = []
            while i < len(rest):
                if rest[i] == "\\":
                    buf.append(rest[i:i+2]); i += 2; continue
                if rest[i] == q:
                    break
                buf.append(rest[i]); i += 1
            val = "".join(buf).replace('\\"', '"').replace("\\'", "'")
        else:
            val = ""
        out.setdefault(key, val)
    return out

rep = []
rep.append("total grouped dict-groups: %d" % len(groups))
for gi, g in enumerate(groups):
    if len(g) < 2:
        continue
    langs = [x[0] for x in g]
    startline = html[:g[0][1]].count("\n") + 1
    data = {b[0]: block_data(b) for b in g}
    rep.append("")
    rep.append("### GROUP %d  langs=%s  ~line %d  sizes=%s" % (
        gi, langs, startline, {k: len(v) for k, v in data.items()}))
    if "zh" in data and "en" in data:
        miss = sorted(set(data["zh"]) - set(data["en"]))
        if miss:
            rep.append("  zh-only keys (%d): %s" % (len(miss), ", ".join(miss[:60])))
    if "zh" in data and "vi" in data:
        miss = sorted(set(data["zh"]) - set(data["vi"]))
        if miss:
            rep.append("  ** vi MISSING keys (%d): %s" % (len(miss), ", ".join(miss[:80])))
    if "en" in data and "vi" in data:
        miss = sorted(set(data["en"]) - set(data["vi"]))
        if miss:
            rep.append("  en-only keys (%d): %s" % (len(miss), ", ".join(miss[:60])))
        # vi 与 en 完全相同的值（疑似漏译）
        same = []
        for k in sorted(set(data["en"]) & set(data["vi"])):
            a, b = data["en"][k], data["vi"][k]
            if a and a == b and len(a) >= 4 and any(ch.isalpha() for ch in a):
                if len(a.split()) >= 2 or len(a) >= 8:
                    has_vn = any(ch in VN_DIA for ch in a.lower())
                    if not has_vn:
                        same.append((k, a))
        if same:
            rep.append("  ** vi == en (%d) 疑似漏译:" % len(same))
            for k, v in same[:40]:
                rep.append("       %s = %r" % (k, v[:70]))

io.open(r"c:/vnchoicedouble/_i18n_audit_out.txt", "w", encoding="utf-8").write("\n".join(rep))
print("groups:", len(groups), "written:", len(rep))
