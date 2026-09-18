# -*- coding: utf-8 -*-
# 生成建材价格历史曲线数据（月度 2021-01 ~ 2026-09）
# 【示例数据】：按越南市场各年大致价位锚定 + 季节性波动生成，可整体替换为真实数据；
# 替换后前端零改动（读 window.MATERIAL_PRICES）
import json, io, math

# 各年锚点（年初价位），中间按月线性插值 + 小幅季节/噪声波动
ANCHOR = {
    # 钢筋 VND/kg
    'rebar':  [15500, 17800, 15500, 14300, 13600, 13900],
    # 水泥 VND/t
    'cement': [1550000, 1740000, 1700000, 1610000, 1575000, 1610000],
    # 黄砂 VND/m3
    'sand':   [380000, 445000, 495000, 482000, 468000, 488000],
    # 石子 VND/m3
    'gravel': [320000, 358000, 398000, 389000, 382000, 398000],
}
YEARS = [2021, 2022, 2023, 2024, 2025, 2026]

def series(key):
    a = ANCHOR[key]
    vals = []
    for yi in range(len(YEARS)):
        y0 = a[yi]
        y1 = a[yi + 1] if yi + 1 < len(a) else a[yi]
        for m in range(1, 13):
            if YEARS[yi] == 2026 and m > 9:
                break
            base = y0 + (y1 - y0) * (m - 1) / 12.0
            # 季节波动：年中需求淡季略低、年末略高；外加小幅确定性噪声
            season = math.sin((m / 12.0) * 2 * math.pi) * (base * 0.012)
            noise = math.sin((yi * 12 + m) * 2.399963) * (base * 0.008)
            vals.append(round(base + season + noise))
    return vals

labels = []
y, m = 2021, 1
while (y, m) <= (2026, 9):
    labels.append('%04d-%02d' % (y, m))
    m += 1
    if m > 12:
        m, y = 1, y + 1

data = {
    'labels': labels,
    'units': {'rebar': 'VND/kg', 'cement': 'VND/t', 'sand': 'VND/m3', 'gravel': 'VND/m3'},
    'series': {k: series(k) for k in ['rebar', 'cement', 'sand', 'gravel']}
}

js = ('// 建材价格历史曲线（月度 2021-01 ~ 2026-09），X=年/月 Y=价格\n'
      '// 【示例数据】按越南市场各年大致价位生成，可直接整体替换为真实采集数据，前端零改动\n'
      'window.MATERIAL_PRICES = ' + json.dumps(data, ensure_ascii=False, indent=1) + ';\n')
io.open('vendor/material_prices.js', 'w', encoding='utf-8').write(js)

import sys
sys.stdout.write('months=%d labels=%s..%s\n' % (len(labels), labels[0], labels[-1]))
for k in data['series']:
    sys.stdout.write('%s: %s .. %s (%s)\n' % (k, data['series'][k][0], data['series'][k][-1], data['units'][k]))
