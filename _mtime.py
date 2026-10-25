# -*- coding: utf-8 -*-
import os
import time

for p in ['choice_lite.html', 'choice_lite.min.html']:
    print(p, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(p))), os.path.getsize(p))
