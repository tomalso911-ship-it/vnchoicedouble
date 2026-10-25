# -*- coding: utf-8 -*-
"""确认 App 当前【真正会下发】的快照文件是哪一个（缓存键 = xlsx 的 mtime_ns+size+路径）。"""
import io, sys, os, glob, hashlib, time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
FIN_DIR = 'finance_data'
REPORT = os.path.join(FIN_DIR, 'vn_report.xlsx')
st = os.stat(REPORT)
key = "%d:%d:%s" % (st.st_mtime_ns, st.st_size, REPORT)
want = 'vn_report.snapshot.%s.json' % hashlib.sha1(key.encode('utf-8')).hexdigest()[:16]
print('xlsx key      =', key)
print('应当下发的文件 =', want)
try:
    got = open(os.path.join(FIN_DIR, 'vn_report.snapshot.key'), encoding='utf-8').read().strip()
except OSError as e:
    got = '<读不到: %s>' % e
print('key 文件内容   =', got)
print('键是否一致     =', got == key)
print()
print('目录下所有快照文件（mtime 从新到旧）：')
files = glob.glob(os.path.join(FIN_DIR, 'vn_report.snapshot.*.json'))
files += glob.glob(os.path.join(FIN_DIR, 'cn_report.snapshot.*.json'))
files += glob.glob(os.path.join(FIN_DIR, 'merge_report.snapshot.*.json'))
for p in sorted(files, key=os.path.getmtime, reverse=True):
    print('   %-56s %s  %s' % (os.path.basename(p), time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(p))) if False else time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(p))), '★当前' if os.path.basename(p) == want else ''))
