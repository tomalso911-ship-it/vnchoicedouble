# -*- coding: utf-8 -*-
"""清掉「旧污染快照备份」这一族的残留（含合并报表那份）。
   做法与上次一致：先复制到 finance_data/_polluted_cache_backup/ 留证，再从工作目录删除。
   只动【快照缓存】家族的 *.bak_before_*，绝不碰 xlsx 数据文件与正式备份。"""
import io, sys, os, glob, shutil, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

FIN = r'C:\vnchoicedouble\finance_data'
EVID = os.path.join(FIN, '_polluted_cache_backup')
os.makedirs(EVID, exist_ok=True)

print('=== 1) finance_data 下所有含 snapshot 的文件 ===')
for p in sorted(glob.glob(os.path.join(FIN, '*snapshot*'))):
    print('   %-62s %9d 字节' % (os.path.basename(p), os.path.getsize(p)))

targets = sorted(glob.glob(os.path.join(FIN, '*snapshot*.bak_before_*')))
print('\n=== 2) 命中「旧污染快照备份」家族 %d 个 ===' % len(targets))
for p in targets:
    print('   ', os.path.basename(p))

print('\n=== 3) 复制留证 -> 再删除 ===')
for p in targets:
    dst = os.path.join(EVID, os.path.basename(p) + '.%s' % time.strftime('%Y%m%d_%H%M%S'))
    shutil.copy2(p, dst)
    os.remove(p)
    print('   已清 %-58s （留证 %s）' % (os.path.basename(p), os.path.basename(dst)))

print('\n=== 4) 顺手清掉半截的 .part / .tmp（只限快照家族）===')
for p in sorted(glob.glob(os.path.join(FIN, '*snapshot*.part')) + glob.glob(os.path.join(FIN, '*snapshot*.tmp'))):
    try:
        os.remove(p)
        print('   已删', os.path.basename(p))
    except OSError as e:
        print('   删不掉', os.path.basename(p), e)

print('\n=== 5) 现状 ===')
print('   finance_data 下剩余含 snapshot 的文件：')
for p in sorted(glob.glob(os.path.join(FIN, '*snapshot*'))):
    print('      %-62s %9d 字节' % (os.path.basename(p), os.path.getsize(p)))
print('\n   留证目录 %s：' % EVID)
for p in sorted(glob.glob(os.path.join(EVID, '*'))):
    print('      %-62s %9d 字节' % (os.path.basename(p), os.path.getsize(p)))

print('\n=== 6) 仓库里其它 *.bak_before_*（只报告，不动）===')
others = [p for p in glob.glob(r'C:\vnchoicedouble\**\*.bak_before_*', recursive=True)]
for p in sorted(set(others)):
    if 'snapshot' not in os.path.basename(p):
        print('   ', os.path.relpath(p, r'C:\vnchoicedouble'))
if not [p for p in others if 'snapshot' not in os.path.basename(p)]:
    print('   （无）')
