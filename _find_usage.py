import io, re

path = r"c:/vnchoicedouble/choice_lite.html"
lines = io.open(path, encoding="utf-8").read().split("\n")

pats = ["lbl_for_house2", "lbl_floor_spec", "slats_pig_house_", "prod_slatsMatrix", "houseOrder"]

rep = []
for p in pats:
    rep.append("=" * 70)
    rep.append("PATTERN: " + p)
    for i, ln in enumerate(lines, 1):
        if p in ln:
            rep.append("  L%d: %s" % (i, ln.strip()[:230]))

io.open(r"c:/vnchoicedouble/_find_usage_out.txt", "w", encoding="utf-8").write("\n".join(rep))
print("lines:", len(rep))
