# -*- coding: utf-8 -*-
"""严格核验：xlsx_to_univer 出来的快照里，'Chi tiết thu-chi' F 列到底是什么。
   直接调用服务端转换器（不读任何缓存文件），并顺带核对缓存键哈希。"""
import io, sys, os, json, hashlib, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, 'c:/vnchoicedouble')
import univer_convert

FIN_DIR = 'c:/vnchoicedouble/finance_data'
REPORT = os.path.join(FIN_DIR, 'vn_report.xlsx')
st = os.stat(REPORT)
key = "%d:%d:%s" % (st.st_mtime_ns, st.st_size, REPORT)
print('绝对路径缓存键 =', key)
print('哈希 ->       =', hashlib.sha1(key.encode('utf-8')).hexdigest()[:16])
print('xlsx mtime    =', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(st.st_mtime)))
print()

snap = univer_convert.xlsx_to_univer(REPORT)
sid = [k for k, v in snap['sheets'].items() if v.get('name') == 'Chi tiết thu-chi'][0]
cd = snap['sheets'][sid]['cellData']
print('★ 转换器【实时】产出的 Chi tiết thu-chi F 列（0 基 r / 1 基行）：')
for r in [3, 4, 5, 6, 7, 8, 78, 79, 292, 293, 299, 300, 301, 302]:
    c = cd.get(str(r), {}).get('5')
    a = cd.get(str(r), {}).get('0')
    print('   0基r%-4d(1基%-4d) A=%-28r F=%r' % (r, r + 1, (a or {}).get('v'), c))
