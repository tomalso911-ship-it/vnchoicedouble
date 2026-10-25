# -*- coding: utf-8 -*-
"""① 核实「被污染的快照文件」是否就是当前缓存键对应的文件；② 备份它；③ 打印 xlsx 的 D95/E95/F95 佐证。"""
import io, sys, os, glob, json, hashlib, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

FIN_DIR = r'C:\vnchoicedouble\finance_data'
REPORT = os.path.join(FIN_DIR, 'vn_report.xlsx')
st = os.stat(REPORT)
key = "%d:%d:%s" % (st.st_mtime_ns, st.st_size, REPORT)
want = 'vn_report.snapshot.%s.json' % hashlib.sha1(key.encode('utf-8')).hexdigest()[:16]
print('当前缓存键   =', key)
print('算出的文件名 =', want)
print('磁盘上实际有 =', [os.path.basename(p) for p in glob.glob(os.path.join(FIN_DIR, 'vn_report.snapshot.*.json'))])
print('★两者一致吗 =', os.path.isfile(os.path.join(FIN_DIR, want)))
print()

bad = os.path.join(FIN_DIR, want)
if os.path.isfile(bad):
    d = json.load(open(bad, encoding='utf-8'))
    sid = [k for k, v in d['sheets'].items() if v.get('name') == 'Chi tiết thu-chi'][0]
    cd = d['sheets'][sid]['cellData']
    for r in [4, 5, 6, 7]:
        c = cd.get(str(r), {}).get('5')
        print('  污染缓存 0基r%-3d F = %r' % (r, c))
    print()
    bakdir = os.path.join(FIN_DIR, '_polluted_cache_backup')
    os.makedirs(bakdir, exist_ok=True)
    dst = os.path.join(bakdir, os.path.basename(bad) + '.%s' % time.strftime('%Y%m%d_%H%M%S'))
    with open(dst, 'wb') as fh:
        fh.write(open(bad, 'rb').read())
    print('已备份污染缓存 ->', dst)

from openpyxl import load_workbook
wb = load_workbook(REPORT, data_only=False)
ws = wb['Chi tiết thu-chi']
print()
print('xlsx 佐证（1基行 95/96/97，列 A/B/C/D/E/F）：')
for r in (94, 95, 96, 97):
    print('  row%-4d' % r, [ws.cell(row=r, column=c).value for c in (1, 2, 3, 4, 5, 6)])
