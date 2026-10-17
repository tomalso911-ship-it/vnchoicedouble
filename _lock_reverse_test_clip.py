# -*- coding: utf-8 -*-
"""反向测试：验证「剪贴板三键放行」与「拖拽自愈」两组锁真的能拦住篡改。"""
import os
import shutil
import subprocess
import sys
import tempfile

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'choice_lite.html')
base = open(SRC, encoding='utf-8', errors='replace').read()

CASES = [
    ('删掉剪贴板放行段', 'check_fin_excel_keys_lock.py',
     'var finClipKey = (k === \'c\' || k === \'C\' || k === \'x\' || k === \'X\' || k === \'v\' || k === \'V\');\n'
     '          if (e.ctrlKey && !e.shiftKey && !e.altKey && finClipKey) return;',
     ''),
    ('放行改成 preventDefault', 'check_fin_excel_keys_lock.py',
     'if (e.ctrlKey && !e.shiftKey && !e.altKey && finClipKey) return;',
     'if (e.ctrlKey && !e.shiftKey && !e.altKey && finClipKey) { e.preventDefault(); return; }'),
    ('删掉拖拽自愈（buttons===0）', 'check_hscroll_lock.py',
     'if (e.buttons === 0){ if (bar.__hsEndDrag) bar.__hsEndDrag(); return; }',
     ''),
    ('pointerup 改回冒泡阶段', 'check_hscroll_lock.py',
     "window.addEventListener('pointerup', endDrag, true);",
     "window.addEventListener('pointerup', endDrag);"),
    ('去掉焦点归还', 'check_hscroll_lock.py',
     'cvf.focus({ preventScroll: true })',
     'cvf.focus()'),
]

caught, missed = [], []
tmp = tempfile.mkdtemp(prefix='cliplock_')
# check_fin_excel_keys_lock.py 默认按【脚本所在目录】找文件、不跟随 cwd，
# 所以必须显式传副本路径；同时把未篡改的验证床放进去，让不变量⑥ 保持通过，
# 这样失败就只可能来自不变量⑧。
shutil.copyfile(os.path.join(ROOT, '_univer_kb_fix.html'),
                os.path.join(tmp, '_univer_kb_fix.html'))
try:
    for name, lock, old, new in CASES:
        if old not in base:
            print('  ⚠ 模式未匹配：%s' % name)
            missed.append(name)
            continue
        text = base.replace(old, new, 1)
        tgt = os.path.join(tmp, 'choice_lite.html')
        with open(tgt, 'w', encoding='utf-8') as f:
            f.write(text)
        env = dict(os.environ, PYTHONIOENCODING='utf-8')
        r = subprocess.run([sys.executable, os.path.join(ROOT, lock), tgt], cwd=tmp,
                           capture_output=True, text=True, encoding='utf-8',
                           errors='replace', env=env)
        if r.returncode != 0:
            caught.append(name)
            print('  ✓ 已拦截：%s (%s)' % (name, lock))
        else:
            missed.append(name)
            print('  ✗ 漏过：%s (%s)' % (name, lock))
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print()
print('拦截 %d/%d' % (len(caught), len(CASES)))
if missed:
    print('漏过：', '、'.join(missed))
sys.exit(0 if not missed else 1)
