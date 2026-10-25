# -*- coding: utf-8 -*-
"""为「月度筛选能否同步汇总表」做技术评估：dump 汇总表(TỔNG HỢP)与一张明细表的公式/列结构。"""
import json, glob, os, sys, datetime, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 取最新的快照文件
cands = sorted(glob.glob('finance_data/vn_report.snapshot.*.json'), key=os.path.getmtime)
path = cands[-1]
print('snapshot:', path, datetime.datetime.fromtimestamp(os.path.getmtime(path)))
snap = json.load(open(path, encoding='utf-8'))
sheets = snap['sheets']


def cell_str(c):
    if not c:
        return ''
    v = c.get('v')
    f = c.get('f')
    t = c.get('t')
    s = ''
    if f:
        s += 'f=%s ' % f
    if v is not None:
        s += 'v=%r ' % v
    if t is not None:
        s += 't=%s ' % t
    st = c.get('s')
    if isinstance(st, dict) and st.get('n'):
        s += 'n=%s' % st['n']
    return s.strip()


def dump(sid, rows, cols, title):
    sh = sheets[sid]
    cd = sh.get('cellData') or {}
    print('\n===== %s | %s | %s =====' % (title, sid, sh.get('name')))
    for r in rows:
        row = cd.get(str(r)) or {}
        parts = []
        for c in cols:
            cell = row.get(str(c))
            if cell is None:
                continue
            parts.append('[%d] %s' % (c, cell_str(cell)))
        print(' r%-4d %s' % (r, ' || '.join(parts)))
    print(' merges:', [(m.get('startRow'), m.get('startColumn'), m.get('endRow'), m.get('endColumn'))
                       for m in (sh.get('mergeData') or [])][:12])
    print(' columnData:', {k: v for k, v in (sh.get('columnData') or {}).items() if k in [str(c) for c in cols]})


# 汇总表：全表前 24 行，只看显示块 0..9
dump('sheet_1', list(range(0, 24)), list(range(0, 10)), '汇总表')
# 明细表：表头与第一段数据（先找前 8 行 + 第 4..8 行）
dump('sheet_2', list(range(3, 12)), list(range(0, 10)), '收支明细 表头+前几行')
# 明细表某一行的完整列（看有没有余额列/公式）
sh2 = sheets['sheet_2']
cd2 = sh2.get('cellData') or {}
for r in (4, 5, 6, 77, 78, 79, 291, 292, 299, 300):
    row = cd2.get(str(r)) or {}
    print('\n sheet_2 r%d:' % r)
    for c in sorted(row.keys(), key=lambda x: int(x)):
        print('    [%s] %s' % (c, cell_str(row[c])))
