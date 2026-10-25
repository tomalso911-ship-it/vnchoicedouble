import io, subprocess, tempfile, os
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
    if not body.strip():
        continue
    f = tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8")
    f.write(body); f.close()
    try:
        r = subprocess.run(["node", "--check", f.name], capture_output=True, text=True, timeout=120)
        out.append(("OK %d" if r.returncode == 0 else "FAIL %d -> %s") % (s + 1, (r.stderr or "")[:200].replace("\n", " ")))
    finally:
        os.unlink(f.name)
io.open("_chk_node_out.txt", "w", encoding="utf-8").write("\n".join(out) + "\nDONE")
