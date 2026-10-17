# -*- coding: utf-8 -*-
"""反向测试：故意篡改 choice_lite.html 的副本，验证 check_hscroll_lock.py 能拦住。"""
import os
import shutil
import subprocess
import sys
import tempfile

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'choice_lite.html')
LOCK = os.path.join(ROOT, 'check_hscroll_lock.py')
base = open(SRC, encoding='utf-8', errors='replace').read()


def mutate(s):
    out = {}
    out['滚动条挂回容器（会被 Univer 清空）'] = s.replace(
        'document.body.appendChild(bar);', 'c.appendChild(bar);', 1)
    out['恢复派发合成 WheelEvent'] = s.replace(
        "bar.style.display = 'flex';",
        "bar.style.display = 'flex';"
        "try { c.querySelectorAll('canvas')[0].dispatchEvent(new WheelEvent('wheel', {deltaX: 10})); } catch(e){}", 1)
    out['scrollToCell 纵向基准写 0（横滚会跳回第 1 行）'] = s.replace(
        'sh2.scrollToCell(curRow, target)', 'sh2.scrollToCell(0, target)', 1)
    out['可见列不用 getVisibleRange'] = s.replace(
        "if (sh && typeof sh.getVisibleRange === 'function'){", 'if (false){', 1)
    out['拖拽状态改回函数内局部变量'] = s.replace(
        'var st = bar.__hsState || (bar.__hsState = { dragging: false, startX: 0, startFrac: 0 });',
        'var st = { dragging: false, startX: 0, startFrac: 0 };', 1)
    out['去掉 rAF 合并（逐事件派发）'] = s.replace(
        'if (!hsRaf) hsRaf = requestAnimationFrame(hsFlush);',
        'if (bar.__hsScroll) bar.__hsScroll(hsPending);', 1)
    out['去掉同列去重（每帧重排）'] = s.replace(
        'if (bar.__hsLastCol === target) ok = true;', 'if (false) ok = true;', 1)
    out['去掉布局防抖（每轮无条件写样式）'] = s.replace(
        'if (bar.__hsLaidOnce && bar.__hsPX === nx && bar.__hsPY === ny) return;',
        'if (false) return;', 1)
    out['命令当主驱动（与像素/列定位互拉）'] = s.replace(
        "if (!ok && a && typeof a.executeCommand === 'function'){",
        "if (a && typeof a.executeCommand === 'function'){", 1)
    out['去掉 thumb 过渡（不再慢慢行走）'] = s.replace(
        'transition:left .12s linear,width .12s linear;', '', 1)
    out['去掉拖拽态 transition:none'] = s.replace(
        '.fin-hscroll.fin-hs-drag .fin-hscroll-thumb{transition:none;}', '', 1)
    out['去掉 resize 跟随'] = s.replace(
        "window.addEventListener('resize', relayout);", '', 1)
    return out


cases = mutate(base)
caught, missed = [], []
tmp = tempfile.mkdtemp(prefix='hscrolllock_')
try:
    for name, text in cases.items():
        if text == base:
            print('  ⚠ 篡改未生效（模式未匹配）：%s' % name)
            missed.append(name)
            continue
        with open(os.path.join(tmp, 'choice_lite.html'), 'w', encoding='utf-8') as f:
            f.write(text)
        env = dict(os.environ, PYTHONIOENCODING='utf-8')
        r = subprocess.run([sys.executable, LOCK], cwd=tmp, capture_output=True, text=True,
                           encoding='utf-8', errors='replace', env=env)
        if r.returncode != 0:
            caught.append(name)
            print('  ✓ 已拦截：%s' % name)
        else:
            missed.append(name)
            print('  ✗ 漏过：%s' % name)
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print()
print('拦截 %d/%d' % (len(caught), len(cases)))
if missed:
    print('漏过：', '、'.join(missed))
sys.exit(0 if not missed else 1)
