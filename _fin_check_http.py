# -*- coding: utf-8 -*-
"""端到端验证：直接向运行中的服务要 /api/finance/vn-report/snapshot，检查下发内容。"""
import io, sys, json, urllib.request, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
URL = 'http://127.0.0.1:5050/api/finance/vn-report/snapshot'
try:
    t0 = time.time()
    with urllib.request.urlopen(URL, timeout=60) as r:
        hdr = dict(r.getheaders())
        raw = r.read()
    print('HTTP OK  %.2fs  %.2f MB' % (time.time() - t0, len(raw) / 1048576.0))
    print('X-Fin-Snap-Cache 头 =', hdr.get('X-Fin-Snap-Cache'))
    d = json.loads(raw.decode('utf-8'))
    sid = [k for k, v in d['sheets'].items() if v.get('name') == 'Chi tiết thu-chi'][0]
    cd = d['sheets'][sid]['cellData']
    print()
    print('★服务端实际下发的 Chi tiết thu-chi F 列：')
    for r in [3, 4, 5, 6, 7, 78, 79, 292, 293, 294, 295, 299, 300, 301, 302]:
        c = cd.get(str(r), {}).get('5') or {}
        print('   0基r%-4d(1基%-4d) F.f=%-22r F.v=%r' % (r, r + 1, c.get('f'), c.get('v')))
    badf = []
    for rk, row in cd.items():
        c = row.get('5')
        if isinstance(c, dict) and isinstance(c.get('f'), str) and rk.isdigit():
            r = int(rk)
            if ('F%d' % (r - 1)) in c['f']:
                badf.append((r, c['f']))
    print()
    print('★错位公式（%s）: %s' % ('还有 = 仍会 #VALUE!' if badf else '= 无', badf[:6] if badf else '无 ✓'))
except Exception as e:
    print('请求失败:', type(e).__name__, e)
