# -*- coding: utf-8 -*-
"""反向测试：故意篡改合并报表蓝字守卫（FIN-MERGE-CN-BLUE-GUARD-20261015），验证硬锁能拦住。"""
import os
import shutil
import subprocess
import sys
import tempfile

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.abspath(__file__))
base = open(os.path.join(ROOT, 'choice_lite.html'), encoding='utf-8', errors='replace').read()
LOCK = os.path.join(ROOT, 'check_fin_merge_cn_blue_lock.py')

guard_at = base.index('function finMergeCnBlueGuard(')
head, tail = base[:guard_at], base[guard_at:]


def in_guard(old, new):
    """只在守卫函数体内替换，避免误伤同名前缀的其他函数。"""
    return head + tail.replace(old, new, 1)


cases = {}
cases['删掉整个守卫函数'] = base.replace('function finMergeCnBlueGuard(){', 'function finMergeCnBlueGuardX(){', 1)
cases['不再限定合并+分组'] = in_guard(
    "if (FIN_KIND !== 'merge' || !FIN_MERGE_CN_GROUP) return 0;",
    "if (false) return 0;")
cases['不再跳过红高亮行'] = base.replace(
    "          if (hiRows.indexOf(r) >= 0) continue;            // ★红高亮行：整行不动\n", "", 1)
cases['不再跳过红字格'] = base.replace(
    "            if (rgb.indexOf('FF0000') >= 0) continue;      // 红（高亮残留/正在高亮）不覆盖\n", "", 1)
cases['不再静默写入'] = base.replace("        finHiApplying = true;                              // ★静默：与高亮/中国报表补蓝同一套机制\n", "", 1)
cases['把守卫挪到高亮之前'] = base.replace(
    "          var _cleaned = finHiCleanup();\n"
    "          finHiRecompute();\n"
    "          if (_cleaned > 0) fin_markDirty();\n"
    "          /* ★FIN-MERGE-CN-BLUE-GUARD-20261015：必须排在高亮之后（先拿到本轮的红色高亮行号，\n"
    "             才知道哪一行要跳过）→ 合并分组视图下把中国区块补回蓝字。 */\n"
    "          try { finMergeCnBlueGuard(); } catch(e){}\n",
    "          try { finMergeCnBlueGuard(); } catch(e){}\n"
    "          var _cleaned = finHiCleanup();\n"
    "          finHiRecompute();\n"
    "          if (_cleaned > 0) fin_markDirty();\n", 1)
cases['载入重建时不清高亮坐标'] = base.replace(
    "        finHiState = {};\n        var UNIT_SHEET", "        var UNIT_SHEET", 1)
cases['刷新重建时不清高亮坐标'] = base.replace(
    "      /* ★FIN-HI-STALE-STATE-20261015：同 fin_loadReport —— 旧单元已销毁，清空旧高亮坐标，\n"
    "         避免用「旧布局行号」去撤高亮时把（合并分组后）中国行写成黑色。 */\n"
    "      finHiState = {};\n", "", 1)
cases['不再只改字色'] = base.replace("ns.cl = { rgb: FIN_CN_BLUE };", "ns.cl = { rgb: '#000000' };", 1)

caught, missed = [], []
tmp = tempfile.mkdtemp(prefix='mergecn_')
try:
    env = dict(os.environ, PYTHONIOENCODING='utf-8')
    for name, text in cases.items():
        if text == base:
            print('  ⚠ 篡改未生效（模式未匹配）：%s' % name)
            missed.append(name)
            continue
        with open(os.path.join(tmp, 'choice_lite.html'), 'w', encoding='utf-8') as f:
            f.write(text)
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
