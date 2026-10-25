# -*- coding: utf-8 -*-
import io

L = io.open('choice_lite.html', encoding='utf-8', errors='replace').read().split('\n')
keys = ['switchView', 'ensure(', 'pub.ensure', '__eqRateWired', 'eqFxFetch', 'load()', 'pub.load',
        'refresh', 'eq_statHideBuiltinBar', 'eq_statEnsureBar', 'innerHTML']
for i in range(24370, min(26700, len(L))):
    s = L[i]
    if any(k in s for k in keys):
        print(i + 1, s.strip().encode('ascii', 'backslashreplace').decode('ascii')[:150])
