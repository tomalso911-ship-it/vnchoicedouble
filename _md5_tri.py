import hashlib, os, glob
files = sorted(glob.glob(r'C:\vnchoicedouble\training_shots\tri\*.png'))
base = {}
for f in files:
    h = hashlib.md5(open(f,'rb').read()).hexdigest()[:8]
    name = os.path.basename(f)
    print(f'{h}  {name}')
# 按前缀分组看同组是否雷同
from collections import defaultdict
g = defaultdict(list)
for f in files:
    n = os.path.basename(f)
    pre = n.rsplit('_',1)[0]
    g[pre].append(hashlib.md5(open(f,'rb').read()).hexdigest()[:8])
print('\n-- groups --')
for k,v in g.items():
    print(k, 'SAME' if len(set(v))==1 else 'diff', v)
