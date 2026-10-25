# -*- coding: utf-8 -*-
import io

L = io.open('choice_lite.html', encoding='utf-8', errors='replace').read().split('\n')
keys = ['\u5faa\u73af', 'NOLOOP', '\u91cd\u5165', 'loop', 'Loop', '\u6b7b\u5faa\u73af']
for i in range(24370, min(26700, len(L))):
    s = L[i]
    if any(k in s for k in keys):
        print(i + 1, s.strip().encode('ascii', 'backslashreplace').decode('ascii')[:180])
