# backup_src.py - choice-project source snapshot (git-free rollback)
# Reliable on Windows: Chinese description is read from a UTF-8 file backup_desc.txt
# (created by the assistant before running), so no codepage loss.
#
# Usage:
#   (assistant) write backup_desc.txt with one-line description (UTF-8), then:
#   python backup_src.py
#   (manual)   python backup_src.py "english description here"
#
# Effect: copies key sources into backups\<YYYYMMDD-HHMMSS>_<desc>\,
#         appends backups\MANIFEST.txt  (time | desc | files)
#         and writes backups\<folder>\NOTE.txt (same line, UTF-8).
# Restore: copy backups\<folder>\<file> back to project root.

import os, shutil, sys, datetime

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

root = os.path.dirname(os.path.abspath(__file__))
bak = os.path.join(root, 'backups')
os.makedirs(bak, exist_ok=True)

desc = None
if len(sys.argv) > 1:
    desc = sys.argv[1].strip()
if not desc:
    desc_path = os.path.join(root, 'backup_desc.txt')
    if os.path.exists(desc_path):
        with open(desc_path, encoding='utf-8') as f:
            desc = f.read().strip()
        os.remove(desc_path)  # consume one-shot description
if not desc:
    desc = 'manual'

ts = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
allowed = set('-_')
slug = ''.join(ch if (ch.isalnum() or '\u4e00' <= ch <= '\u9fff' or ch in allowed) else '_' for ch in desc)
slug = slug[:60]
target = os.path.join(bak, ts + '_' + slug)
os.makedirs(target, exist_ok=True)

files = ['index.html', 'crm_table.js', 'lost_table.js', 'app.py', 'manifest.json']
copied = []
for f in files:
    s = os.path.join(root, f)
    if os.path.exists(s):
        shutil.copy2(s, os.path.join(target, f))
        copied.append(f)

line = ts + ' | ' + desc + ' | ' + ' '.join(copied)
with open(os.path.join(bak, 'MANIFEST.txt'), 'a', encoding='utf-8') as fp:
    fp.write(line + '\n')
with open(os.path.join(target, 'NOTE.txt'), 'w', encoding='utf-8') as fp:
    fp.write(line + '\n')

print('Snapshot:', target)
print('Files:', ', '.join(copied))
print('Logged: backups/MANIFEST.txt')
print('Restore: copy backups/<folder>/<file> back to project root.')
