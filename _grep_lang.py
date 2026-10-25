import re
src = open(r'C:\vnchoicedouble\choice_lite.html', encoding='utf-8', errors='ignore').read()
pats = [r'setLang', r'switchLang', r'langchange', r'function .{0,20}[Ll]ang',
        r"onclick=\"[^\"]*[Ll]ang", r'data-lang', r'__lang', r'setLangDebug']
seen = set()
for pat in pats:
    for m in re.finditer(pat, src):
        s = max(0, m.start()-60); e = min(len(src), m.end()+90)
        snip = src[s:e].replace('\n',' ')
        # 转义以防打印出错
        print('PAT', pat)
        print('  ...'+snip+'...')
        print()
