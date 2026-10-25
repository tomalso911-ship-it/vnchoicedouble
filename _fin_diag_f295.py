# -*- coding: utf-8 -*-
"""诊断：zip 条目级对比（备份 vs 现文件），并把 F295/F302/F303/F304 的原始 XML 并排打出来。"""
import io, sys, os, re, glob, shutil, zipfile, hashlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

XLSX = r'C:\vnchoicedouble\finance_data\vn_report.xlsx'
BAK = sorted(glob.glob(r'C:\vnchoicedouble\backups\vn_report_*_before_F295fix.xlsx.bak'))[0]
print('备份 =', os.path.basename(BAK))

with zipfile.ZipFile(BAK) as z:
    za = {i.filename: z.read(i.filename) for i in z.infolist()}
with zipfile.ZipFile(XLSX) as z:
    zb = {i.filename: z.read(i.filename) for i in z.infolist()}

print('\n=== zip 条目 ===')
print('  只在一侧存在的:', sorted(set(za) ^ set(zb)))
for k in sorted(set(za) & set(zb)):
    if za[k] != zb[k]:
        print('  ★内容变化: %-34s %d -> %d 字节' % (k, len(za[k]), len(zb[k])))
    else:
        print('   未变    : %-34s %d 字节' % (k, len(za[k])))

xmlA = za['xl/worksheets/sheet2.xml'].decode('utf-8')
xmlB = zb['xl/worksheets/sheet2.xml'].decode('utf-8')
print('\n=== sheet2.xml 里各格原始 XML ===')
for coord in ('F295', 'F302', 'F303', 'F304', 'F5', 'F293'):
    pa = re.search(r'<c r="%s".*?(?:</c>|/>)' % coord, xmlA, re.S)
    pb = re.search(r'<c r="%s".*?(?:</c>|/>)' % coord, xmlB, re.S)
    print('  %-5s 备份: %s' % (coord, pa.group(0) if pa else '(无)'))
    print('  %-5s 现在: %s' % ('', pb.group(0) if pb else '(无)'))

# 缓存值统计
print('\n=== <v> 数量对比（公式格是否还带缓存值）===')
for tag, x in (('备份', xmlA), ('现在', xmlB)):
    nf = len(re.findall(r'<f[ >]', x))
    nv = len(re.findall(r'<v[ >]', x))
    print('  %s: <f> %d 个, <v> %d 个' % (tag, nf, nv))
