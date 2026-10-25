# -*- coding: utf-8 -*-
"""清掉被手改污染的快照缓存（等价于 app.py 的 _fin_cache_invalidate()），
   下次 GET /api/finance/vn-report/snapshot 会从【干净的 xlsx】重新转换并落盘。
   同时把罪魁脚本 _fin_bake_formulas.py 改名停用（不再可被误跑）。"""
import io, sys, os, glob, time, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

FIN_DIR = r'C:\vnchoicedouble\finance_data'
KEY = os.path.join(FIN_DIR, 'vn_report.snapshot.key')
PREFIXES = ('vn_report.snapshot.', 'cn_report.snapshot.', 'merge_report.snapshot.')

print('--- 1) 删除缓存键与全部快照文件（先确认备份已存在）---')
bakdir = os.path.join(FIN_DIR, '_polluted_cache_backup')
n_bak = len(glob.glob(os.path.join(bakdir, '*'))) if os.path.isdir(bakdir) else 0
print('   备份目录里的文件数 =', n_bak, bakdir)
if n_bak == 0:
    print('   !! 没有备份，拒绝删除'); sys.exit(1)

removed = []
for p in [KEY] + [q for pre in PREFIXES
                  for q in glob.glob(os.path.join(FIN_DIR, pre + '*.json'))]:
    try:
        os.remove(p)
        removed.append(os.path.basename(p))
    except OSError as e:
        print('   删不掉（可能正被服务进程读着，下次会覆盖）:', os.path.basename(p), e)
print('   已删除:', removed)

print('\n--- 2) 停用罪魁脚本 _fin_bake_formulas.py ---')
src = r'C:\vnchoicedouble\_fin_bake_formulas.py'
if os.path.isfile(src):
    dst = src + '.disabled_polluted_cache_' + time.strftime('%Y%m%d')
    shutil.move(src, dst)
    print('   已改名停用 ->', os.path.basename(dst))
else:
    print('   已不存在')

print('\n--- 3) 现状 ---')
print('   key 存在?', os.path.isfile(KEY))
left = [os.path.basename(p) for pre in PREFIXES for p in glob.glob(os.path.join(FIN_DIR, pre + '*.json'))]
print('   残留快照:', left if left else '（无，下次 GET 会重建）')
print('   备份(留证):', [os.path.basename(p) for p in glob.glob(os.path.join(bakdir, '*'))])
