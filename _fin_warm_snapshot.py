# -*- coding: utf-8 -*-
"""按 app.py::_fin_cache_build 的同样方式，从【干净的 xlsx】重建快照缓存并落盘、落键。
   然后立刻回读校验：F 列不应再出现 '=F4+D5-E5' 这类错位公式。"""
import io, sys, os, json, hashlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, r'C:\vnchoicedouble')
import univer_convert

FIN_DIR = r'C:\vnchoicedouble\finance_data'
REPORT = os.path.join(FIN_DIR, 'vn_report.xlsx')
KEY = os.path.join(FIN_DIR, 'vn_report.snapshot.key')
PREFIX = 'vn_report.snapshot.'

st = os.stat(REPORT)
key = "%d:%d:%s" % (st.st_mtime_ns, st.st_size, REPORT)
path = os.path.join(FIN_DIR, '%s%s.json' % (PREFIX, hashlib.sha1(key.encode('utf-8')).hexdigest()[:16]))
FP = os.path.join(FIN_DIR, 'vn_report.snapshot.fp')

snap = univer_convert.xlsx_to_univer(REPORT)
part = path + '.part'
with open(part, 'w', encoding='utf-8') as fh:
    json.dump(snap, fh, ensure_ascii=False, separators=(",", ":"))
os.replace(part, path)
# ★与 app.py::_fin_cache_build 同序：快照 -> 指纹 -> 键（FIN-SNAP-FP-20261015）
_h = hashlib.sha256()
with open(path, 'rb') as fh:
    for chunk in iter(lambda: fh.read(1 << 20), b''):
        _h.update(chunk)
with open(FP + '.tmp', 'w', encoding='utf-8') as fh:
    fh.write(_h.hexdigest())
os.replace(FP + '.tmp', FP)
tmpk = KEY + '.tmp'
with open(tmpk, 'w', encoding='utf-8') as fh:
    fh.write(key)
os.replace(tmpk, KEY)
print('已重建快照 ->', os.path.basename(path))
print('大小 = %.2f MB' % (os.path.getsize(path) / 1048576.0))
print('键文件已写 ->', key)
print()

d = json.load(open(path, encoding='utf-8'))
sid = [k for k, v in d['sheets'].items() if v.get('name') == 'Chi tiết thu-chi'][0]
cd = d['sheets'][sid]['cellData']
print('★重建后 Chi tiết thu-chi F 列（0基r / 1基行）：')
ok = True
for r in [3, 4, 5, 6, 7, 8, 78, 79, 292, 293, 299, 300, 301, 302]:
    c = cd.get(str(r), {}).get('5') or {}
    f = c.get('f')
    print('   0基r%-4d(1基%-4d) F.f=%-22r F.v=%r' % (r, r + 1, f, c.get('v')))
    # 错位公式的特征：行号 = 自身 1 基行号 - 2（如 1基6 行出现 =F4+…）
    if isinstance(f, str) and ('F%d' % (r - 1)) in f:
        ok = False
print()
print('★是否还有错位公式:', '否 ✓' if ok else '是 ✗')
