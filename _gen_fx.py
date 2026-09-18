# -*- coding: utf-8 -*-
# 从真实API（Yahoo Finance 月K线）采集 2021-01 ~ 2026-09 汇率（取每月1号/首交易日开盘价），
# 生成 vendor/fx_history.js 固化进系统：历史数据一次生成，之后前端不再请求任何接口
import json, datetime, urllib.request, io

P1 = int(datetime.datetime(2021, 1, 1).timestamp())
P2 = int(datetime.datetime(2026, 10, 1).timestamp())

def fetch_monthly(pair):
    url = ('https://query1.finance.yahoo.com/v8/finance/chart/%s?interval=1mo&period1=%d&period2=%d'
           % (pair, P1, P2))
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=25) as r:
        j = json.loads(r.read().decode('utf-8'))
    res = j['chart']['result'][0]
    stamps = res.get('timestamp') or []
    q = (res.get('indicators', {}).get('quote') or [{}])[0]
    opens = q.get('open') or []
    closes = q.get('close') or []
    out = {}
    for t, o, cl in zip(stamps, opens, closes):
        d = datetime.datetime.fromtimestamp(t, datetime.timezone.utc)
        ym = '%04d-%02d' % (d.year, d.month)
        val = o if o is not None else cl   # 1号无开盘数据时退用收盘
        if ym not in out and val is not None:
            out[ym] = round(float(val), 4)
    return out

vnd = fetch_monthly('USDVND=X')
cny = fetch_monthly('USDCNY=X')

# 2021-01 ~ 2026-09 全月展开，缺失月份用上月值前向填充（真实序列的标准处理）
yms = []
y, m = 2021, 1
while (y, m) <= (2026, 9):
    yms.append('%04d-%02d' % (y, m))
    m += 1
    if m > 12: m, y = 1, y + 1

def ffill(series):
    out = {}; prev = None
    for ym in yms:
        if ym in series: prev = series[ym]
        if prev is not None: out[ym] = prev
    return out

vnd = ffill(vnd); cny = ffill(cny)
recs = []
for ym in yms:
    v = vnd.get(ym); c = cny.get(ym)
    if not v or not c: continue
    recs.append({'ym': ym, 'rmbVnd': round(v / c, 1), 'usdVnd': round(v, 1), 'usdRmb': round(c, 4)})

js = ('// 汇率历史（月度，每月1号数据）：由真实API采集于 2026-09-16 生成，已历史化固化，\n'
      '// 前端直接读取 window.FX_HISTORY，不再请求接口；新月份由懒采集追加到 localStorage\n'
      'window.FX_HISTORY = ' + json.dumps(recs, ensure_ascii=False, indent=1) + ';\n')
io.open('vendor/fx_history.js', 'w', encoding='utf-8').write(js)
sysline = 'months=%d first=%s last=%s' % (len(recs), json.dumps(recs[0], ensure_ascii=True), json.dumps(recs[-1], ensure_ascii=True))
sys.stdout.write(sysline + '\n')
