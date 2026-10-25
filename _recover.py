# -*- coding: utf-8 -*-
"""尝试把被反复乘爆的数值还原成原始录入值（按汇率幂次反推）。"""
import itertools

vals = {4: 7.407352404817838e+18, 5: 2.753822365133669e+18, 7: 8775150930648999.0}
rates = {'rmb3850': 3850, 'rmb3500': 3500, 'usd26100': 26100, 'usd25000': 25000,
         'usd_cny': 26100 / 3850.0}

for row, v in vals.items():
    print('==== R%dC5  value=%r' % (row, v))
    best = []
    # 逐个因子穷举：最多 8 步
    names = list(rates.keys())

    def walk(rest, path, depth):
        if depth > 0:
            # 记录当前状态
            if abs(rest - round(rest)) < 1e-6 * max(1, abs(rest)):
                best.append((abs(rest - round(rest)), list(path), rest))
        if depth >= 8:
            return
        for n in names:
            walk(rest / rates[n], path + [n], depth + 1)

    walk(v, [], 0)
    best.sort(key=lambda x: (abs(x[2] - round(x[2])), len(x[1])))
    for d, path, rest in best[:12]:
        print('   diff=%.3g  %-6d  <- %s' % (d, round(rest), ' / '.join(path)))
