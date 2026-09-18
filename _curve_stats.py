# -*- coding: utf-8 -*-
import json, re, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

labels = []
y, m = 2021, 1
while (y, m) <= (2026, 9):
    labels.append('%04d-%02d' % (y, m))
    m += 1
    if m > 12:
        m, y = 1, y + 1

def extrema(vals):
    peaks, valleys = [], []
    for i in range(1, len(vals) - 1):
        if vals[i] > vals[i-1] and vals[i] > vals[i+1]:
            peaks.append((labels[i], vals[i]))
        if vals[i] < vals[i-1] and vals[i] < vals[i+1]:
            valleys.append((labels[i], vals[i]))
    return peaks, valleys

def parse_js_var(path, varname):
    with io.open(path, encoding='utf-8') as f:
        txt = f.read()
    m = re.search(r'window\.' + varname + r'\s*=\s*([\s\S]*?);', txt)
    return json.loads(m.group(1))

fx = parse_js_var('vendor/fx_history.js', 'FX_HISTORY')
mat = parse_js_var('vendor/material_prices.js', 'MATERIAL_PRICES')

print("=== 汇率 ===")
for k, unit in [('rmbVnd', ''), ('usdVnd', ''), ('usdRmb', '')]:
    vals = [r[k] for r in fx]
    p, v = extrema(vals)
    print(f"\n{k}:")
    print(f"  起点 2021-01: {vals[0]}")
    print(f"  终点 2026-09: {vals[-1]}")
    print(f"  全局最高 {max(vals)} @ {labels[vals.index(max(vals))]}")
    print(f"  全局最低 {min(vals)} @ {labels[vals.index(min(vals))]}")
    print("  波峰:")
    for d, val in p:
        print(f"    {d}: {val}")
    print("  波谷:")
    for d, val in v:
        print(f"    {d}: {val}")

print("\n=== 建材 ===")
for k, unit in [('rebar', 'VND/kg'), ('cement', 'VND/t'), ('sand', 'VND/m3'), ('gravel', 'VND/m3')]:
    vals = mat['series'][k]
    p, v = extrema(vals)
    print(f"\n{k} ({unit}):")
    print(f"  起点 2021-01: {vals[0]:,}")
    print(f"  终点 2026-09: {vals[-1]:,}")
    print(f"  全局最高 {max(vals):,} @ {labels[vals.index(max(vals))]}")
    print(f"  全局最低 {min(vals):,} @ {labels[vals.index(min(vals))]}")
    print("  波峰:")
    for d, val in p:
        print(f"    {d}: {val:,}")
    print("  波谷:")
    for d, val in v:
        print(f"    {d}: {val:,}")
