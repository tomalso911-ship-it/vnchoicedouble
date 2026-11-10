# -*- coding: utf-8 -*-
"""硬锁自检：空闲期「不空转 + 视图门控 + 后台帧泵降频」契约
（PERF-IDLE-LOCK-20261108，用户 2026-11-08 明确要求「必须锁定这个逻辑，千万不能再出错」）。

为什么锁：
  2026-11-08 之前，页面空闲时每秒仍有 ~220 次调度唤醒（rAF 180/s + setTimeout 15/s + interval 27/s），
  全部来自「body 级 MutationObserver 被两套常驻 Univer 的 DOM 变动反复触发 → 各自 debounce 排空转定时器」。
  修完后：rAF 2151→174 / 12s，回调总耗时 169ms→61ms。这些都是**很脆的负向过滤**，
  任何重构只要把任意一条删掉或放宽，就会静默回退到原来的空转状态（用户无感，只是越来越卡）。

不变量（改坏即拦截提交）：
  ① updateNavLock 观察器必须忽略 #univer_container / #equity_container 内部的 class 变动
  ② 移动箭头观察器：★回调里绝不做 document.querySelector（必须合并进 200ms 定时器）
  ③ 移动箭头的 800ms 重试必须【退避 + 封顶】
  ④ 财务工具栏观察器必须视图门控（未激活只打 __finToolbarStale）
  ⑤ 权益权限观察器必须视图门控（未激活只打 __eqPermsStale）
  ⑥ ★门控必须有「补回」通路：__onViewShown 钩子 + 700ms 兜底轮询
     （2026-11-08 真实事故：纯 return 导致财务工具栏停在 .fin-workspace，宽 1322 而非 126）
  ⑦ Univer 帧泵降频只许针对「源码含 _beginFrame 且含 renderEvenInBackground」的回调，
     且任一表格视图激活时必须不延迟
  ⑧ 两处 250ms 常驻 interval 必须视图门控
  ⑨ ★基线漂移守门（用户 2026-11-08 追加要求）：
     body 级观察器 / documentElement 级观察器 / MutationObserver 总数 / 常驻 setInterval 总数
     全部钉死基线。后来新增（或删除）任何一处都拦提交，并在输出里列出各处行号，
     逼开发者显式确认「是否必要、有没有 document.hidden / __viewActive 门控」
     —— 防「以后又悄悄加一个 body 观察器或常驻轮询」绕过前 8 条（前 8 条只管已修好的那几处）。

失败即 exit 1（已登记进 .githooks/pre-commit 与 .git/hooks/pre-commit）。
反向测试：python _lock_reverse_test_perf_idle.py
"""
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

BASE = os.path.dirname(os.path.abspath(__file__))
TARGET = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE, "choice_lite.html")

try:
    src = open(TARGET, encoding="utf-8", errors="replace").read()
except OSError as e:
    print("✗ 读不到目标文件：%s (%r)" % (TARGET, e))
    sys.exit(1)

ok = True
NORM = re.sub(r"\s+", " ", src)


def chk(cond, msg):
    global ok
    print(("  ✓ " if cond else "  ✗ ") + msg)
    if not cond:
        ok = False


def has(snippet, msg):
    chk(re.sub(r"\s+", " ", snippet) in NORM, msg)


def hasnt(snippet, msg):
    chk(re.sub(r"\s+", " ", snippet) not in NORM, msg)


print("1) updateNavLock 观察器：忽略 Univer 内部的 class 变动")
has("if(tgt.id==='univer_container' || (tgt.closest && tgt.closest('#univer_container'))) continue;",
    "排除 #univer_container 内部变动")
has("if(tgt.id==='equity_container' || (tgt.closest && tgt.closest('#equity_container'))) continue;",
    "排除 #equity_container 内部变动")
has("if(tgt.id==='tbMenu' || (tgt.closest && tgt.closest('#tbMenu'))) continue;",
    "原有 #tbMenu 排除仍在（自激循环防护）")

print("2) 移动箭头观察器：合并在定时器里，回调内禁止整页 querySelector")
has("var mo = new MutationObserver(function () { if (tm) return; tm = setTimeout(function () { tm = null; if (!hasMoveBtn()) return;",
    "观察器只负责合并排一个 200ms 定时器，检查放在定时器里")
chk("function hasMoveBtn()" in src, "hasMoveBtn() 判定函数存在")
has("var v = document.getElementById('view-won');",
    "hasMoveBtn 先从 #view-won 取容器（不再整页扫）")
m = re.search(r"var mo = new MutationObserver\(function \(\) \{(.{0,160})", src, re.S)
chk(bool(m) and re.sub(r"\s+", " ", m.group(1)).lstrip().startswith("if (tm) return;"),
    "★观察器回调第一句必须是 if (tm) return;（不得先做 DOM 查询）")

print("3) 移动箭头 800ms 重试：退避 + 封顶")
has("if (++tries <= 6) setTimeout(start, 800 * tries);",
    "重试次数封顶（原来无上限 → 无按钮账号永久空转 ~1.25 次/秒）")
hasnt("setTimeout(start, 800);", "★不得回到无条件 setTimeout(start, 800)")

print("4) 财务工具栏观察器：视图门控 + stale 标记")
has("if (!_act) { window.__finToolbarStale = true; return; }", "未激活只打 __finToolbarStale，不排定时器")
has("try { _act = __viewActive('finance'); } catch(e) {}", "门控判据必须是 __viewActive('finance')")
has("finToolbarTimer = null; window.__finToolbarStale = false; try { fin_mountToolbar2(); } catch(e){}",
    "真正挂载时清掉 stale 标记")

print("5) 权益权限观察器：视图门控 + stale 标记")
has("if (!_act) { window.__eqPermsStale = true; return; }", "未激活只打 __eqPermsStale，不排定时器")
has("try { _act = __viewActive('equity'); } catch(e) {}", "门控判据必须是 __viewActive('equity')")
has("eqT = null; window.__eqPermsStale = false; try{ applyEqPerms(); }catch(e){}",
    "真正重贴时清掉 stale 标记")

print("6) ★门控必须有补回通路（2026-11-08 事故：纯 return 会让工具栏永远挂不上）")
chk("window.__onViewShown = function(v){" in NORM, "switchView 钩子 __onViewShown 存在")
has("if (v === 'finance' && typeof window.fin_mountToolbar2 === 'function')",
    "钩子在进入财务视图时补挂工具栏")
has("if (v === 'equity' && typeof window.applyEqPerms === 'function')",
    "钩子在进入权益视图时补跑权限")
has("window.switchView = _svWrapped;", "switchView 被包装（钩子真正接线）")
has("if (window.__finToolbarStale && typeof __viewActive === 'function' && __viewActive('finance')) {",
    "兜底轮询：财务工具栏")
has("if (window.__eqPermsStale && typeof __viewActive === 'function' && __viewActive('equity')) {",
    "兜底轮询：权益权限")
has("}, 700);", "兜底轮询间隔 700ms")

print("7) Univer 后台帧泵降频（只针对那一个渲染回调）")
chk("window.__univerAnyActive = function(){" in NORM, "__univerAnyActive 存在")
has("if (typeof __viewActive === 'function') return !!(__viewActive('finance') || __viewActive('equity'));",
    "活动判定 = 财务或权益视图")
has("if (typeof _raf === 'function' && !window.__rafIdlePatch) {", "rAF 包装幂等（只装一次）")
has("ok = s.indexOf('_beginFrame') >= 0 && s.indexOf('renderEvenInBackground') >= 0;",
    "只识别 Univer 渲染循环那一个回调（不误伤其它 rAF）")
has("if (typeof cb === 'function' && _isRenderPump(cb) && !window.__univerAnyActive()) {",
    "★只有「是渲染泵 且 两个表格视图都不在前台」时才延迟（激活时必须 60fps）")
has("return setTimeout(function(){ try { _raf(cb); } catch(e){} }, 200);", "后台降频到 ~5fps（200ms）")
has("return _raf(cb);", "非渲染泵 / 激活态 原样放行")

print("8) 两处 250ms 常驻 interval：视图门控")
# ★必须「就近」判定：同一个 __viewActive('finance') 片段在文件里出现很多次，
#   全局 count 查不出「刚好把 finRememberCur 那一处删掉」的篡改（反向测试实测漏过一次）。
_i = src.find("finLastKeyAt < 400) return;")
chk(_i > 0 and "__viewActive('finance')" in src[max(0, _i - 400):_i],
    "finRememberCur 轮询：同一个 interval 里、紧邻调用前必须有 __viewActive('finance') 门控")
_j = src.find("function sheetLockHideDeleteMenus(){")
chk(_j > 0 and "if (!__viewActive('finance') && !__viewActive('equity')) return;"
    in src[_j:_j + 900],
    "sheetLockHideDeleteMenus：同一个函数体内必须有 finance||equity 门控")

print("9) ★基线漂移守门：后来新增的 body 级观察器 / 常驻轮询必须被看见")
# 这一组的用意：前 8 条只守「已经修好的那几处」。将来谁再往页面里加一个
# body 级 MutationObserver 或一个无条件 setInterval，光靠前 8 条是发现不了的
# ——用户 2026-11-08 明确要求「后期增加了别的 body 级观察器或常驻轮询，这套锁也要能发现」。
# 做法：把当前基线钉死；数量一变就拦提交，并在输出里列出每一处的行号，
# 逼开发者显式确认「这门控是必要的吗、加了 document.hidden / __viewActive 门控吗」。
# 2026-11-08 追加 +1：SLATS-SOLID-BOX-20261108 的「实心板 YES 双线黑框」补框器
# （slatsSolidBoxBoot）。它只在 childList 变动时把新增子树丢进 150ms 合并队列，
# 回调首行有 document.hidden 门控 + visibilitychange 补扫，属确属必要的一处新增。
BASE_BODY_OBS = 11   # .observe(document.body ...)
BASE_MUT_OBS = 21    # new MutationObserver(...)
# 2026-11-10 追加 +1：WX-LIVE-SYNC-20261110「天气全员即时同步」的 15 秒轮询。
# 它带 document.hidden + window.currentView==='worklog' 双重门控（setInterval 回调首行判 hidden，
# wxLiveTick 再判视图），后台/其它视图一律不发请求；已按第⑨条显式确认必要性并登记基线。
BASE_IV = 40         # setInterval(...)

body_obs = len(re.findall(r"\.observe\(\s*document\.body", src))
mut_obs = len(re.findall(r"new MutationObserver\s*\(", src))
ivs = len(re.findall(r"\bsetInterval\s*\(", src))


def baseline(name, cur, base, hint):
    chk(cur == base, "%s：基线 %d，实际 %d%s" % (name, base, cur, "（一致）" if cur == base else " ★有变化"))
    if cur != base:
        print("      → %s" % hint)
        print("      → 若确属必要：先加门控（document.hidden / __viewActive），再把 check_perf_idle_lock.py 里对应基线改成 %d" % cur)


baseline("body 级观察器 .observe(document.body)", body_obs, BASE_BODY_OBS,
         "新增 body 观察器会被两套常驻 Univer 的 DOM 变动持续点亮 → 记得在回调里先判视图/元素来源")
BASE_DOCEL_OBS = 0
baseline("documentElement 级观察器", len(re.findall(r"\.observe\(\s*document\.documentElement", src)),
         BASE_DOCEL_OBS, "整文档级观察器极贵（每次变动都跨整棵树），一律不要新增")
baseline("MutationObserver 实例总数", mut_obs, BASE_MUT_OBS,
         "观察器总数变了（新增或删除），请确认没有引入新的「高频 debounce 空转」")
baseline("常驻 setInterval 总数", ivs, BASE_IV,
         "新增常驻轮询前请先想：能不能用事件/命令流代替？不能则必须带 document.hidden 或 __viewActive 门控")


def _lines(pat, limit=40):
    ls = []
    for m in re.finditer(pat, src):
        n = src.count("\n", 0, m.start()) + 1
        ls.append(n)
        if len(ls) >= limit:
            break
    return ls


if body_obs != BASE_BODY_OBS:
    print("      body observe 行号: %s" % _lines(r"\.observe\(\s*document\.body"))
if ivs != BASE_IV:
    print("      setInterval 行号: %s" % _lines(r"\bsetInterval\s*\("))
if mut_obs != BASE_MUT_OBS:
    print("      new MutationObserver 行号: %s" % _lines(r"new MutationObserver\s*\("))

print("")
if ok:
    print("总体: 全部通过 ✓（空闲不空转 / 视图门控 / 帧泵降频 契约完整）")
    sys.exit(0)
print("总体: 有违规 ✗")
sys.exit(1)
