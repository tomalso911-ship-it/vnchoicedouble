# -*- coding: utf-8 -*-
"""反向测试：故意篡改 choice_lite.html 的副本，验证 check_fin_cn_hide_checked_lock.py 能拦住。"""
import os
import shutil
import subprocess
import sys
import tempfile

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'choice_lite.html')
LOCK = os.path.join(ROOT, 'check_fin_cn_hide_checked_lock.py')
base = open(SRC, encoding='utf-8', errors='replace').read()

def mutate(s):
    """返回 {名称: 篡改后的文案}"""
    out = {}
    out['去掉一个三语 key'] = s.replace('fin_btn_hide_checked:', '', 1)
    out['按钮移到导出之后'] = s.replace(
        '          <button class="fin-btn" id="fin_cn_hide_checked_btn" style="display:none"\n'
        '                  data-i18n="fin_btn_hide_checked" onclick="fin_cnToggleHideChecked()">隐藏核销记录</button>\n', '', 1
    ).replace('data-i18n="fin_btn_export" onclick="fin_exportLocal()">导出 xlsx</button>',
              'data-i18n="fin_btn_export" onclick="fin_exportLocal()">导出 xlsx</button>'
              '<button class="fin-btn" id="fin_cn_hide_checked_btn" data-i18n="fin_btn_hide_checked"'
              ' onclick="fin_cnToggleHideChecked()">隐藏</button>', 1)
    out['改掉 onclick'] = s.replace('onclick="fin_cnToggleHideChecked()"', 'onclick="fin_cnToggleHideChecked2()"', 1)
    out['删掉第二处调用'] = s.replace(
        'try { fin_cnHideCheckedInView(finLastView, snapshot); } catch(e){}', 'var _x = 1;', 1)
    out['颠倒调用顺序'] = s.replace(
        'try { fin_cnHideCheckedInView(snapshot, base); } catch(e){}\n'
        '        try { fin_rptHideInView(snapshot, base); } catch(e){}',
        'try { fin_rptHideInView(snapshot, base); } catch(e){}\n'
        '        try { fin_cnHideCheckedInView(snapshot, base); } catch(e){}', 1)
    out['不按 isCn 显隐'] = s.replace("if (hc) hc.style.display = isCn ? '' : 'none';", 'if (hc) hc.style.display = "";', 1)
    out['不再克隆 / 碰 cellData'] = s.replace(
        'var rd2 = fin_rptCloneRowData(src2);\n            var c3 = rd2[String(it2.r)];',
        'var rd2 = src2; sh2.cellData = sh2.cellData; var c3 = rd2[String(it2.r)];', 1)
    out['删掉 hd=1 标记'] = s.replace('c3.hd = 1;', 'c3.hd0 = 1;', 1)
    return out

cases = mutate(base)
caught, missed = [], []
tmp = tempfile.mkdtemp(prefix='hidelock_')
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
