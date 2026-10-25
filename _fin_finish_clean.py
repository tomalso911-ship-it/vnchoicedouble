# -*- coding: utf-8 -*-
"""收尾：① 作废旧快照缓存并按新键重建（快照→指纹→键）；② 删掉两份旧污染 .bak_before_*。"""
import io, sys, os, glob, json, hashlib, zipfile
sys.path.insert(0, r'C:\vnchoicedouble')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

XLSX = r'C:\vnchoicedouble\finance_data\vn_report.xlsx'
FIN = r'C:\vnchoicedouble\finance_data'

print('=== 1) 作废旧快照缓存 ===')
rm = []
for p in [os.path.join(FIN, 'vn_report.snapshot.key'), os.path.join(FIN, 'vn_report.snapshot.fp')] + \
         glob.glob(os.path.join(FIN, 'vn_report.snapshot.*.json')):
    try:
        os.remove(p); rm.append(os.path.basename(p))
    except OSError:
        pass
print('   已删:', rm)

print('\n=== 2) 按新键重建（快照→指纹→键，与 app.py 同序）===')
import univer_convert
st = os.stat(XLSX)
key = "%d:%d:%s" % (st.st_mtime_ns, st.st_size, XLSX)
path = os.path.join(FIN, 'vn_report.snapshot.%s.json' % hashlib.sha1(key.encode('utf-8')).hexdigest()[:16])
snap = univer_convert.xlsx_to_univer(XLSX)
with open(path + '.part', 'w', encoding='utf-8') as fh:
    json.dump(snap, fh, ensure_ascii=False, separators=(",", ":"))
# 直接复制 xl/worksheets/sheet2.xml 之外的字节校验（复用 zip 对比结论，这里只报大小）
os.replace(path + '.part', path)
h = hashlib.sha256()
with open(path, 'rb') as fh:
    for c in iter(lambda: fh.read(1 << 20), b''):
        h.update(c)
with open(os.path.join(FIN, 'vn_report.snapshot.fp') + '.tmp', 'w', encoding='utf-8') as fh:
    fh.write(h.hexdigest())
os.replace(os.path.join(FIN, 'vn_report.snapshot.fp') + '.tmp', os.path.join(FIN, 'vn_report.snapshot.fp'))
with open(os.path.join(FIN, 'vn_report.snapshot.key') + '.tmp', 'w', encoding='utf-8') as fh:
    fh.write(key)
os.replace(os.path.join(FIN, 'vn_report.snapshot.key') + '.tmp', os.path.join(FIN, 'vn_report.snapshot.key'))
print('   新快照 =', os.path.basename(path), ' %.2fMB' % (os.path.getsize(path) / 1048576.0))
print('   指纹文件存在 =', os.path.isfile(os.path.join(FIN, 'vn_report.snapshot.fp')))
print('   键文件内容 =', open(os.path.join(FIN, 'vn_report.snapshot.key'), encoding='utf-8').read().strip())

print('\n=== 3) 清理旧污染快照 .bak_before_* ===')
old = sorted(glob.glob(os.path.join(FIN, 'vn_report.snapshot.*.json.bak_before_*')))
print('   找到:', [os.path.basename(p) for p in old])
for p in old:
    os.remove(p)
print('   已删 %d 个' % len(old))
print('   finance_data 里剩余 snapshot 相关:', sorted(os.path.basename(p) for p in glob.glob(os.path.join(FIN, '*snapshot*'))))
print('   仍留作证据:', [os.path.basename(p) for p in glob.glob(os.path.join(FIN, '_polluted_cache_backup', '*'))])
