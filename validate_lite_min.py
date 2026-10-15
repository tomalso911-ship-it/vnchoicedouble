# -*- coding: utf-8 -*-
"""校验 choice_lite.min.html 与源文件功能等价（无语法错误、全局符号一致）。"""
from playwright.sync_api import sync_playwright
import json
import os

BASE = 'file:///c:/vnchoicedouble/'
SRC = BASE + 'choice_lite.html'
MIN = BASE + 'choice_lite.min.html'

GLOBALS = [
    'switchView', 'renderWonData', 'openProjectReport', 'setLangDebug', 'applyLangFit',
    'fitOne', 'measureW', 'loadWon', 'prod_get', 'prod_mergeFactory', 'inst_bldgSpecInstalled',
    'fmtMoney', 'fmtThousands', 'syncWonColVisibility', 'applyRowPerms', '__deferInit',
    'RPT_I18N', 'PROJECT_REPORT_CSS', 'startFitObserver', 'initStickyHScrollbars',
    'initFitScreen', 'loadUsers', 'startPendBadgePolling', 'curHiddenForSel', 'curColSel',
    'prod_slatsMatrix', 'wonGroupState', 'fitTopbarFonts', 'buildWonColGroup', 'injectWonToggleBtns',
]

PROBE = """
(function(){
  var L = %s, r = {};
  for (var i=0;i<L.length;i++){ r[L[i]] = (typeof window[L[i]]); }
  return r;
})()
"""


def run(pg, url, errs):
    pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
    pg.goto(url, wait_until='domcontentloaded', timeout=60000)
    pg.wait_for_timeout(2500)
    return pg.evaluate(PROBE % json.dumps(GLOBALS))


def main():
    L = []

    def log(s):
        L.append(s)

    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)

        pg1 = b.new_page(); e1 = []
        g1 = run(pg1, SRC, e1)

        pg2 = b.new_page(); e2 = []
        g2 = run(pg2, MIN, e2)

        b.close()

    log('src pageerrors: %d' % len(e1))
    for x in e1[:8]:
        log('    ' + x)
    log('min pageerrors: %d' % len(e2))
    for x in e2[:8]:
        log('    ' + x)

    diff = {k: (g1.get(k), g2.get(k)) for k in GLOBALS if g1.get(k) != g2.get(k)}
    log('global type diffs: %d' % len(diff))
    for k, v in diff.items():
        log('    %-26s src=%s min=%s' % (k, v[0], v[1]))

    ok = (len(diff) == 0) and (len(e2) <= len(e1))
    log('RESULT: ' + ('PASS' if ok else 'FAIL'))

    with open('_val_result.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')


if __name__ == '__main__':
    main()
