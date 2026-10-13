#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""财务 Univer「sheets-formula bufferWhen 爆栈防护」锁死检查（lint / CI / git pre-commit 均可用）。

契约编号：FIN-FORMULA-STACK-20261013（见 choice_lite.html 中 fin_patchFormulaService 区块注释）

为什么需要这个硬锁：
  上游 @univerjs/sheets-formula@0.5.5 的 RegisterOtherFormulaService 构造函数里这样组合：

      this._formulaChangeWithRange$.pipe(
        bufferWhen(() => this.calculateStarted$.pipe(filter(v => v)))
      ).subscribe(...)

  而 calculateStarted$ 是 new BehaviorSubject(false)，并且 TriggerCalculationController 的
  构造函数末尾【无条件】执行 calculateStarted$.next(true)。rxjs 的 BehaviorSubject 在【每一次订阅】
  时都会同步回放当前值，bufferWhen 的关闭通知器又会在每次关缓冲后【重新订阅】——于是值已经是 true
  时：投递 true → 关缓冲 → 重新订阅 → 同步回放 true → 又关缓冲 → … 同步无限递归直到爆栈，
  rxjs 再把 RangeError 经 reportUnhandledError 异步抛出 → 控制台红字
  「Uncaught RangeError: Maximum call stack size exceeded ... bufferWhen.mjs」。
  修法是运行时给 calculateStarted$ 套一个「无回放转发外壳」（pipe 前插 skip(1)），使关闭通知器
  恢复成边沿触发。下面每一条都对应「去掉就复发」的关键点：

  ① importmap 必须把 @univerjs/sheets-formula 指到 preset-sheets-core 内部引用的【同一个文件 URL】
     （/@univerjs/sheets-formula@0.5.5/es2022/sheets-formula.mjs）。指到别处 → 浏览器加载到第二个
     模块实例 → DI token 不是同一个对象 → 补丁打在错误的类上（表格照跑，但控制台依旧爆栈）。
  ② importmap 必须有 "rxjs" → /rxjs@>=7.0.0?target=es2022（同一个 rxjs 实例，skip 必须来自同一份 rxjs）。
  ③ fin_patchFormulaService 必须：包住 _initFormulaRegister、把 calculateStarted$ 换成转发外壳、
     外壳的 pipe 前面插 skip(1)（★核心一行，删掉即复发）、原实现必须用 orig.call(self) 调回、幂等标记。
  ④ 打补丁【必须早于】presets.createUniver(...)：服务的构造函数在 createUniver 内部跑，晚一步就拦不住。
  ⑤ 自检 fin_formulaSafeCheck 只允许在【原型】上查标记，绝不可在 createUniver 之后立刻 injector.get()
     ——那个时机单元还没建、服务还没注册进 DI，redi 会抛
     "[redi]: Expect required dependency items for id ... but get 0"（实测踩到）。

用法：
  python3 check_fin_formula_lock.py [path/to/choice_lite.html]
  python3 check_fin_formula_lock.py --selftest     # 反向测试：篡改临时副本，必须全被拦下
退出码：0 = 通过；1 = 契约被破坏（CI 失败 / pre-commit 拦截）。
"""
import io
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

DOC_ID = "FIN-FORMULA-STACK-20261013"
HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_HTML = os.path.join(HERE, "choice_lite.html")

# (编号, 说明, 正则)  —— 正则在「空白折叠后」的文本上匹配，容忍重新缩进
REQ = [
    ("①a", "importmap：@univerjs/sheets-formula 必须指到 preset 内部引用的同一个文件 URL",
     r'"@univerjs/sheets-formula":\s*"https://esm\.sh/@univerjs/sheets-formula@0\.5\.5/es2022/sheets-formula\.mjs"'),
    ("①b", "importmap：@univerjs/sheets-formula 入口必须被 import 进来（_impOpt）",
     r"_impOpt\('@univerjs/sheets-formula'\)"),
    ("②a", 'importmap：必须有 "rxjs" → /rxjs@>=7.0.0?target=es2022（同一份 rxjs）',
     r'"rxjs":\s*"https://esm\.sh/rxjs@>=7\.0\.0\?target=es2022"'),
    ("②b", "rxjs 入口必须被 import 进来（_impOpt）",
     r"_impOpt\('rxjs'\)"),
    ("③a", "fin_patchFormulaService 必须存在（原型级补丁）",
     r"function fin_patchFormulaService\(formulaMod, rxMod\)"),
    ("③b", "必须先判 rxMod.skip 可用（拿不到 skip 就整体跳过，别硬装）",
     r"typeof rxMod\.skip !== 'function'\) return false;"),
    ("③c", "必须包住 RegisterOtherFormulaService.prototype._initFormulaRegister",
     r"proto\._initFormulaRegister = function\(\)"),
    ("③d", "★核心：外壳 pipe 前必须插 skip(1)（丢掉 BehaviorSubject 订阅时的同步回放）",
     r"\[rxMod\.skip\(1\)\]\.concat\(Array\.prototype\.slice\.call\(arguments\)\)"),
    ("③e", "必须把 calculateStarted$ 换成外壳（否则原 BehaviorSubject 仍会被重入订阅）",
     r"self\.calculateStarted\$ = guarded;"),
    ("③f", "原实现必须用 orig.call(self) 调回（不得丢掉原有注册逻辑）",
     r"return orig\.call\(self\);"),
    ("③g", "幂等标记 proto.__finFormulaSafe = true 必须保留",
     r"proto\.__finFormulaSafe = true;"),
    ("④a", "打补丁的调用必须存在（fin_patchFormulaService(_mods[21], _mods[22])）",
     r"try \{ fin_patchFormulaService\(_mods\[21\], _mods\[22\]\); \}"),
    ("④b", "自检的调用必须存在（fin_formulaSafeCheck(_mods[21])）",
     r"try \{ fin_formulaSafeCheck\(_mods\[21\]\); \} catch\(e\)\{\}"),
    ("⑤a", "fin_formulaSafeCheck 必须存在",
     r"function fin_formulaSafeCheck\(formulaMod\)"),
    ("⑤b", "自检必须只看原型标记 proto.__finFormulaSafe",
     r"var guardedOk = !!\(proto && proto\.__finFormulaSafe\);"),
    ("⑤c", "自检必须给排障留可观测标记 window.__FIN_FORMULA_SAFE = true",
     r"window\.__FIN_FORMULA_SAFE = true;"),
]


def norm(s):
    """折叠空白（换行/缩进统一成单空格），使契约匹配容忍重新缩进。"""
    return re.sub(r"\s+", " ", s)


def strip_js_comments(s):
    """去掉 // 行注释与 /* */ 块注释。
    ★注意：`//` 必须不是紧跟在 `:` 后面 —— 否则会把 importmap 里的 https://esm.sh/... 一起切掉。"""
    s = re.sub(r"/\*.*?\*/", " ", s, flags=re.S)
    out = []
    for ln in s.split("\n"):
        m = re.search(r"(?<!:)//", ln)
        out.append(ln if not m else ln[:m.start()])
    return "\n".join(out)


def fn_body(html, header):
    """按花括号配对，取出函数体（用于「函数内部不得出现某写法」这类检查）。"""
    i = html.find(header)
    if i < 0:
        return ""
    j = html.find("{", i)
    if j < 0:
        return ""
    depth = 0
    for k in range(j, len(html)):
        c = html[k]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return html[j:k + 1]
    return html[j:]


def import_entries(html):
    """取出 Promise.all([...]) 里的逐个 import 项（顺序即 _mods 下标）。"""
    head = "var _mods = await Promise.all(["
    i = html.find(head)
    if i < 0:
        return []
    j = html.find("]);", i)
    if j < 0:
        return []
    body = strip_js_comments(html[i + len(head):j])
    return [x.strip() for x in body.split(",") if x.strip()]


def check(html):
    """返回违规说明列表（空 = 通过）。"""
    bad = []
    text = norm(strip_js_comments(html))

    for _no, desc, pat in REQ:
        if not re.search(pat, text):
            bad.append("缺失/被改动：" + desc)

    # 模块下标漂移：_mods[21]/_mods[22] 必须还是 sheets-formula / rxjs（插一项就错位）
    items = import_entries(html)
    if len(items) < 23:
        bad.append("模块下标：Promise.all 里只有 %d 项，_mods[21]/_mods[22] 已越界" % len(items))
    else:
        if "@univerjs/sheets-formula" not in items[21]:
            bad.append("模块下标漂移：_mods[21] 应为 @univerjs/sheets-formula，实际为 %s" % items[21][:60])
        if "rxjs" not in items[22]:
            bad.append("模块下标漂移：_mods[22] 应为 rxjs，实际为 %s" % items[22][:60])

    # ④ 顺序：打补丁必须在 presets.createUniver( 之前
    i_patch = text.find("try { fin_patchFormulaService(_mods[21], _mods[22]); }")
    i_create = text.find("var createResult = presets.createUniver({")
    if i_patch < 0 or i_create < 0:
        bad.append("缺失/被改动：patch 调用或 presets.createUniver( 找不到，无法校验先后顺序")
    elif i_patch > i_create:
        bad.append("顺序错误：fin_patchFormulaService 必须在 presets.createUniver 之前调用"
                   "（服务构造函数在 createUniver 内部跑，晚了拦不住）")

    # ⑤ 自检里不得调 injector.get（早期取 DI 会让 redi 抛 "required dependency items"）
    body = strip_js_comments(fn_body(html, "function fin_formulaSafeCheck(formulaMod)"))
    if body:
        if "__getInjector" in body or ".get(" in body:
            bad.append("自检污染：fin_formulaSafeCheck 里不得调用 injector.get()"
                       "（单元未建/服务未注册，redi 会抛 Expect required dependency items）")
    return bad


MUTATIONS = [
    ("去掉 skip(1)（核心一行）", "[rxMod.skip(1)]", "[]"),
    ("自检里偷偷注入 injector.get()",
     "var cls = formulaMod && formulaMod.RegisterOtherFormulaService;",
     "var cls = formulaMod && formulaMod.RegisterOtherFormulaService; var _s = finUniver.__getInjector().get(cls);"),
    ("删掉 importmap 的 sheets-formula 条目",
     '"@univerjs/sheets-formula": "https://esm.sh/@univerjs/sheets-formula@0.5.5/es2022/sheets-formula.mjs",', ""),
    ("删掉 importmap 的 rxjs 条目", '"rxjs": "https://esm.sh/rxjs@>=7.0.0?target=es2022"', ""),
    ("删掉 _impOpt('rxjs') 那一行", "_impOpt('rxjs')", ""),
    ("在 Promise.all 里插一项造成下标漂移",
     "var _mods = await Promise.all([",
     "var _mods = await Promise.all([\n          _impOpt('@univerjs/sheets-sort-ui'),"),
    ("删掉幂等标记 proto.__finFormulaSafe = true;", "proto.__finFormulaSafe = true;", ""),
    ("不再替换 calculateStarted$（只留空外壳）", "self.calculateStarted$ = guarded;", ""),
    ("把补丁调用挪到 createUniver 之后",
     "        try { fin_patchFormulaService(_mods[21], _mods[22]); } catch(e){ console.warn('[fin-formula]', e); }\n\n        var createResult = presets.createUniver({",
     "        var createResult = presets.createUniver({"),
    ("原实现被丢掉（不调回 orig）", "return orig.call(self);", "return undefined;"),
    ("自检不再看原型标记", "var guardedOk = !!(proto && proto.__finFormulaSafe);", "var guardedOk = true;"),
]


def selftest(html):
    print("— 反向测试（篡改临时副本，必须全部被拦下）")
    ok = True
    for desc, old, new in MUTATIONS:
        if old not in html:
            print("  ⚠ 跳过（模板串已变，请同步更新 MUTATIONS）：%s" % desc)
            ok = False
            continue
        bad = check(html.replace(old, new, 1))
        if bad:
            print("  ✓ 拦下：%s → %s" % (desc, bad[0][:60]))
        else:
            print("  ✗ 漏过！！ %s（契约检查没抓到这次篡改）" % desc)
            ok = False
    # 原文件必须通过
    if check(html):
        print("  ✗ 未篡改的原文件竟然不通过：%s" % check(html)[0][:80])
        ok = False
    else:
        print("  ✓ 未篡改的原文件通过")
    print("— 反向测试结果：%s" % ("全部拦下 ✓" if ok else "存在漏网/模板过期 ✗"))
    return 0 if ok else 1


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    path = args[0] if args else DEFAULT_HTML
    try:
        html = io.open(path, encoding="utf-8", errors="replace").read()
    except Exception as e:
        print("✗ 读不到 %s：%s" % (path, e))
        return 1

    if "--selftest" in sys.argv[1:]:
        return selftest(html)

    bad = check(html)
    if bad:
        print("✗ %s 契约被破坏（%s）：" % (os.path.basename(path), DOC_ID))
        for b in bad:
            print("   - " + b)
        print("   说明见 choice_lite.html 里 fin_patchFormulaService 上方注释。")
        return 1
    print("✓ %s 通过（%s：sheets-formula bufferWhen 无回放外壳 + skip(1) + createUniver 之前装配）"
          % (os.path.basename(path), DOC_ID))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
