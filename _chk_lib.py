import io, esprima
src = io.open("choice_lite.html", encoding="utf-8", errors="replace").read()
lines = src.split("\n")
starts = [i for i, l in enumerate(lines) if l.strip().startswith("<script") and "src=" not in l]
ends = [i for i, l in enumerate(lines) if "</script" in l]
out = []
for s in starts:
    if "importmap" in lines[s]:
        continue
    e = next((x for x in ends if x > s), None)
    if e is None:
        continue
    body = "\n".join(lines[s + 1:e])
    if "lib_scopeLvForKey" not in body and "lib_sales_contract" not in body:
        continue
    try:
        esprima.parseScript(body); out.append("OK %d" % (s + 1))
    except Exception:
        try:
            esprima.parseModule(body); out.append("OK(module) %d" % (s + 1))
        except Exception as ex:
            out.append("FAIL %d -> %s" % (s + 1, str(ex)[:300]))
io.open("_chk_lib_out.txt", "w", encoding="utf-8").write("\n".join(out) + "\nDONE")
