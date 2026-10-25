# -*- coding: utf-8 -*-
"""直接调用 app._fin_dash_data 验证看板数据结构（不启动服务）。"""
import io, sys, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, r'C:\vnchoicedouble')
import app


def show(tag, d):
    print('\n===== %s =====' % tag)
    if not d:
        print('  !! None')
        return
    print('  title   :', d['title'])
    print('  asOf    : %r  ->  %s' % (d['asOf'], d['asOfIso']))
    print('  opening : %s' % d['opening'])
    print('  receipts: %s' % d['receipts']['total'])
    print('  payments: %s' % d['payments']['total'])
    print('  ending  : %s   (真实账面 C8 = %s)' % (d['ending'], d['balanceTotal']))
    print('  accounts:')
    for a in d['accounts']:
        print('     %-46s %s' % (a['zh'] + ' / ' + a['en'], a['v']))
    print('  收入明细:')
    for a in d['receipts']['items']:
        print('     %-46s %s' % (a['zh'] + ' / ' + a['en'], a['v']))
    print('  支出明细:')
    for a in d['payments']['items']:
        print('     %-46s %s' % (a['zh'] + ' / ' + a['en'], a['v']))
    print('  勾稽：')
    for c in d['checks']:
        print('     %-6s ok=%-5s expect=%s actual=%s' % (c['k'], c['ok'], c['expect'], c['actual']))
    print('  checksOk =', d['checksOk'])


show('越南 vn_report', app._fin_dash_data(app.FIN_REPORT))
show('合并 merge_report', app._fin_dash_data(app.MERGE_REPORT))
