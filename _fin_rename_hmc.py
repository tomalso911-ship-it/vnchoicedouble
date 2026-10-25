"""把财务报表里的中文名「河明强」统一改为「何明强」。
覆盖：翻译缓存(真值来源) fin_trans_cache.json、当前 JSON 快照、xlsx 导出件。
仅做精确子串替换，不改越南语原文 Hà Minh Cường。改前对每个文件做 .bak_before_hmc 备份。
"""
import os, zipfile

BASE = 'finance_data'
OLD, NEW = '河明强', '何明强'

JSON_FILES = [
    'fin_trans_cache.json',
    'vn_report.snapshot.53de90780c95c7e1.json',
    'merge_report.snapshot.4656dda10233c9cc.json',
]
XLSX_FILES = ['vn_report.xlsx', 'merge_report.xlsx', 'cn_report.xlsx']


def backup(p):
    b = p + '.bak_before_hmc'
    if not os.path.exists(b):
        with open(p, 'rb') as f:
            data = f.read()
        with open(b, 'wb') as f:
            f.write(data)
    return b


def fix_json(p):
    with open(p, encoding='utf-8') as f:
        t = f.read()
    n = t.count(OLD)
    if n:
        backup(p)
        with open(p, 'w', encoding='utf-8') as f:
            f.write(t.replace(OLD, NEW))
    return n


def fix_xlsx(p):
    if not os.path.exists(p):
        return -1
    z = zipfile.ZipFile(p, 'r')
    names = z.namelist()
    data = {n: z.read(n) for n in names}
    z.close()
    total = 0
    changed = False
    for n in names:
        if not (n.endswith('.xml') or n.endswith('.rels')):
            continue
        try:
            s = data[n].decode('utf-8')
        except Exception:
            continue
        c = s.count(OLD)
        if c:
            data[n] = s.replace(OLD, NEW).encode('utf-8')
            changed = True
            total += c
    if changed:
        backup(p)
        base, ext = os.path.splitext(p)
        tmp = base + '.tmp' + ext
        with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zo:
            for n in names:
                zo.writestr(n, data[n])
        os.replace(tmp, p)
    return total


if __name__ == '__main__':
    for f in JSON_FILES:
        p = os.path.join(BASE, f)
        print('JSON', f, '->', fix_json(p) if os.path.exists(p) else 'MISSING')
    for f in XLSX_FILES:
        p = os.path.join(BASE, f)
        r = fix_xlsx(p)
        print('XLSX', f, '->', ('replaced %d' % r) if r >= 0 else 'MISSING')
