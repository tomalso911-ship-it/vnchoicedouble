# -*- coding: utf-8 -*-
import io
import re

L = io.open('choice_lite.html', encoding='utf-8', errors='replace').read().split('\n')
pat = re.compile(r'lastIndex|while\s*\(|for\s*\(;;\)|setInterval|setTimeout\(.*render|render\(\)')
for i in range(24370, min(26700, len(L))):
    if pat.search(L[i]):
        print(i + 1, L[i].strip().encode('ascii', 'backslashreplace').decode('ascii')[:150])
