# -*- coding: utf-8 -*-
"""反向测试：对 check_perf_idle_lock.py 做篡改验证——每种「退回空转」的改法都必须被拦住。

用法：python _lock_reverse_test_perf_idle.py
输出：每条篡改 → 期望 FAIL；最后打印 x/y 拦截成功。
"""
import os
import re
import subprocess
import sys
import tempfile

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "choice_lite.html")
CHECK = os.path.join(BASE, "check_perf_idle_lock.py")


def wsflex(old):
    """把片段变成「空白数量无关」的正则，方便篡改时不必抠缩进。"""
    parts = re.split(r"\s+", old.strip())
    return re.compile(r"\s+".join(re.escape(p) for p in parts))


def tamper_fin_remember(s):
    """只删掉 finRememberCur 那个 interval 里的门控（其它同名片段不动）。"""
    i = s.find("finLastKeyAt < 400) return;")
    if i <= 0:
        return None
    head, tail = s[:i], s[i:]
    win = head[-400:]
    pat = wsflex("try { if (!__viewActive('finance')) return; } catch(e){}")
    if not pat.search(win):
        return None
    return head[:-400] + pat.sub("", win, count=1) + tail


def tamper_sheetlock(s):
    """只删掉 sheetLockHideDeleteMenus 函数体内的门控。"""
    j = s.find("function sheetLockHideDeleteMenus(){")
    if j < 0:
        return None
    seg = s[j:j + 900]
    pat = wsflex("if (!__viewActive('finance') && !__viewActive('equity')) return;")
    if not pat.search(seg):
        return None
    return s[:j] + pat.sub("if (false) return;", seg, count=1) + s[j + 900:]


CASES = [
    ("① 去掉 updateNavLock 对 #univer_container 的排除",
     "if(tgt.id==='univer_container' || (tgt.closest && tgt.closest('#univer_container'))) continue;",
     ""),
    ("① 去掉 updateNavLock 对 #equity_container 的排除",
     "if(tgt.id==='equity_container' || (tgt.closest && tgt.closest('#equity_container'))) continue;",
     ""),
    ("② 把「合并定时器」改回「每次变动先查 DOM」",
     "if (tm) return; tm = setTimeout(function () { tm = null; if (!hasMoveBtn()) return;",
     "if (!hasMoveBtn()) return; tm = setTimeout(function () { tm = null;"),
    ("② hasMoveBtn 改回整页 document.querySelector",
     "var v = document.getElementById('view-won');",
     "var v = null;"),
    ("③ 800ms 重试退回无条件（永久空转）",
     "if (++tries <= 6) setTimeout(start, 800 * tries);",
     "setTimeout(start, 800);"),
    ("④ 工具栏门控丢掉 stale 标记（纯 return）",
     "if (!_act) { window.__finToolbarStale = true; return; }",
     "if (!_act) return;"),
    ("⑤ 权益权限门控丢掉 stale 标记（纯 return）",
     "if (!_act) { window.__eqPermsStale = true; return; }",
     "if (!_act) return;"),
    ("⑥ 删掉 700ms 兜底轮询里的工具栏补挂",
     "if (window.__finToolbarStale && typeof __viewActive === 'function' && __viewActive('finance')) {",
     "if (false) {"),
    ("⑥ switchView 钩子不接线",
     "window.switchView = _svWrapped;",
     "window.switchView = _sv;"),
    ("⑦ 帧泵判定放宽（不再限定 renderEvenInBackground）",
     "ok = s.indexOf('_beginFrame') >= 0 && s.indexOf('renderEvenInBackground') >= 0;",
     "ok = s.indexOf('_beginFrame') >= 0;"),
    ("⑦ 去掉「视图激活就不延迟」的判断（前台也降频）",
     "if (typeof cb === 'function' && _isRenderPump(cb) && !window.__univerAnyActive()) {",
     "if (typeof cb === 'function' && _isRenderPump(cb)) {"),
    ("⑧ 去掉 finRememberCur 的视图门控（只删那一处）", tamper_fin_remember, None),
    ("⑧ 去掉 sheetLockHideDeleteMenus 的视图门控（只删那一处）", tamper_sheetlock, None),
    ("⑨ 偷偷新增一个 body 级 MutationObserver",
     "window.__perfIdle4 = true;",
     "window.__perfIdle4 = true; new MutationObserver(function(){}).observe(document.body, {childList:true});"),
    ("⑨ 偷偷新增一个无条件 setInterval",
     "window.__perfIdle4 = true;",
     "window.__perfIdle4 = true; setInterval(function(){ /* sneak */ }, 500);"),
    ("⑨ 新增 documentElement 级观察器",
     "window.__perfIdle4 = true;",
     "window.__perfIdle4 = true; new MutationObserver(function(){}).observe(document.documentElement, {childList:true});"),
]


def main():
    src = open(SRC, encoding="utf-8", errors="replace").read()
    ok_n = 0
    tmpdir = tempfile.mkdtemp(prefix="idle_lock_rt_")
    for i, (name, old, new) in enumerate(CASES, 1):
        if callable(old):
            mutated = old(src)
            if mutated is None:
                print("  ?  %-46s 篡改锚点没找到（脚本可能已更新，请修反向测试）" % name)
                continue
        else:
            pat = wsflex(old)
            if not pat.search(src):
                print("  ?  %-46s 篡改锚点没找到（脚本可能已更新，请修反向测试）" % name)
                continue
            mutated = pat.sub(new, src, count=1)
        path = os.path.join(tmpdir, "mutant_%02d.html" % i)
        with open(path, "w", encoding="utf-8") as f:
            f.write(mutated)
        r = subprocess.run([sys.executable, CHECK, path], capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=300)
        caught = (r.returncode != 0)
        if caught:
            ok_n += 1
        print("  %s %-46s rc=%d" % ("✓ 拦住" if caught else "✗ 漏过", name, r.returncode))
    print("\n反向测试结果：%d/%d 种篡改被拦截" % (ok_n, len(CASES)))
    return 0 if ok_n == len(CASES) else 1


sys.exit(main())
