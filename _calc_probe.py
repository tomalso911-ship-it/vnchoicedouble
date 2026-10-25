# -*- coding: utf-8 -*-
import io

L = io.open('choice_lite.html', encoding='utf-8', errors='replace').read().split('\n')
keys = ['\u8ba1\u7b97', 'eq_statCompute', 'eq_statBind', 'eqStatSel', 'eqStatPend', 'eq_statScan']
for i in range(24370, min(26700, len(L))):
    s = L[i]
    if any(k in s for k in keys):
        print(i + 1, s.strip().encode('ascii', 'backslashreplace').decode('ascii')[:165])
