import sys
import urllib.request

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
h = urllib.request.urlopen('http://127.0.0.1:5050/lite', timeout=20).read().decode('utf-8', 'replace')
print('len =', len(h))
for name, key in [
    ('FIN-EDIT-SCOPE', 'FIN-EDIT-SCOPE-20261017'),
    ('EQ-EDIT-SCOPE', 'EQ-EDIT-SCOPE-20261017'),
    ('EQ-CLIP-EDITSAFE', 'EQ-CLIP-EDITSAFE-20261017'),
    ('win_clipWrite', 'window.win_clipWrite = function'),
    ('eq 接线', 'window.win_clipWrite(eq_clipMatrixText())'),
    ('fin 接线', 'fin_clipWrite(fin_clipMatrixText())'),
    ('clip-lock 自检', '[clip-lock] OK'),
]:
    print('%-18s = %s' % (name, key in h))
