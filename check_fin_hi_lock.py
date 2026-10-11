#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
财务表「屏幕高亮」锁死检查（lint / CI / git pre-commit 均可用）。

契约编号：FIN-HI-LOCK-20261011（见 choice_lite.html 中的 ★锁死区★ 注释）

为什么需要这个硬锁：
  曾经出现「红字高亮打上去后莫名其妙消失」。根因不是写样式失败，而是
  「保存动作本身把屏幕上的红抹掉」，而 finHiRecompute 只看行号、行号没变就 return，
  于是抹掉后再也不会补回。以下四条不变量是修复的全部内容，缺一条 BUG 就会复发：

  ① 高亮写样式必须开静默窗口：finHiExecStyle 末尾设置 finHiQuietUntil = Date.now() + FIN_HI_LOCK.quietMs；
     fin_bindChange 的 listener 必须写成 `if (finHiApplying || Date.now() < finHiQuietUntil) return;`
     （onCommandExecuted 回调是异步的，进来时 finHiApplying 已复位为 false，只靠它必然漏判
      → 高亮写入被误判成用户编辑 → fin_markDirty() → 自动保存 → 触发 ②）。
  ② fin_inlineStyles 绝不把实时样式库的对象塞进副本的 cell.s：
     必须用 fin_cloneStyleObj() 克隆；剥离红色高亮只能 delete 克隆副本，禁止 delete 原对象；
     深拷贝失败（或 out.sheets/out.styles 缺失）必须直接 return snapshot。
  ③ 必须存在 finHiCellHasHi/finHiRowHasHi，且 finHiRecompute 在「行号相同」时仍要抽查
     红+粗是否真的还在，不在就走"只重写、不撤回"的自愈通道（受 finHiHealAt 节流）。
  ④ 高亮是纯屏幕效果：保存副本里必须已剥离红+粗（不得把红色写进 xlsx）。

用法：
  python3 check_fin_hi_lock.py [path/to/choice_lite.html]
  不传路径时默认检查同目录下的 choice_lite.html。
退出码：0 = 通过；1 = 契约被破坏（CI 失败 / pre-commit 拦截）。
"""
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

DOC_ID = "FIN-HI-LOCK-20261011"


def fn_body(text, name):
    """取出 `function <name>(...)` 的函数体（含花括号配对），找不到返回 None。"""
    m = re.search(r"function\s+" + re.escape(name) + r"\s*\(", text)
    if not m:
        return None
    fb = text.find("{", m.end())
    if fb < 0:
        return None
    depth = 0
    i = fb
    while i < len(text):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[fb:i + 1]
        i += 1
    return text[fb:]


def line_of(text, idx):
    return text.count("\n", 0, idx) + 1


def check_html(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    errors = []
    warnings = []

    # ---- 0) 锁标记与常量必须都在 ----
    if DOC_ID not in text:
        errors.append("找不到锁标记 %s（锁死区注释被删除？）" % DOC_ID)
    if not re.search(r"var\s+FIN_HI_LOCK\s*=\s*\{", text):
        errors.append("找不到 FIN_HI_LOCK 常量定义（锁死区被删除？）")
    for key, val in (("quietMs", 600), ("healMs", 4000)):
        if not re.search(r"%s\s*:\s*%d" % (key, val), text):
            errors.append("FIN_HI_LOCK.%s 不再是 %d（静默/节流时长被改动？）" % (key, val))

    # ---- ① 静默窗口：高亮写入不得触发自动保存 ----
    body = fn_body(text, "finHiExecStyle")
    if body is None:
        errors.append("找不到 finHiExecStyle（高亮写样式入口被删除？）")
    elif not re.search(r"finHiQuietUntil\s*=\s*Date\.now\(\)\s*\+\s*FIN_HI_LOCK\.quietMs", body):
        errors.append("不变量①被破坏：finHiExecStyle 末尾没有设置 finHiQuietUntil（高亮写入会被误判成编辑→触发自动保存）")

    bind = fn_body(text, "fin_bindChange")
    if bind is None:
        errors.append("找不到 fin_bindChange（命令监听被删除？）")
    else:
        if not re.search(r"finHiApplying\s*\|\|\s*Date\.now\(\)\s*<\s*finHiQuietUntil\s*\)\s*return", bind):
            errors.append("不变量①被破坏：fin_bindChange 的 listener 未同时检查静默窗口 "
                          "(应为 `if (finHiApplying || Date.now() < finHiQuietUntil) return;`)")
        if not re.search(r"finHiLockVerify\s*\(\s*\)\s*;", bind):
            errors.append("启动自检被移除：fin_bindChange 内找不到 finHiLockVerify() 调用")

    # ---- ② 保存路径：只能在副本上剥离样式 ----
    if fn_body(text, "fin_cloneStyleObj") is None:
        errors.append("不变量②被破坏：找不到 fin_cloneStyleObj（样式克隆函数被删除）")

    inline = fn_body(text, "fin_inlineStyles")
    if inline is None:
        errors.append("找不到 fin_inlineStyles（保存前样式内联入口被删除？）")
    else:
        if not re.search(r"if\s*\(\s*!out\s*\|\|\s*!out\.sheets\s*\|\|\s*!out\.styles\s*\)", inline):
            errors.append("不变量②被破坏：fin_inlineStyles 缺少【深拷贝失败就放弃剥离】的保护")
        if not re.search(r"cell\.s\s*=\s*fin_cloneStyleObj\s*\(\s*st\s*\)", inline):
            errors.append("不变量②被破坏：把 styles[id] 灌进 cell.s 时没有克隆"
                          "（会与实时样式库共享引用）")
        if not re.search(r"fin_cloneStyleObj\s*\(\s*_s4\s*\)", inline):
            errors.append("不变量②被破坏：剥离红色高亮时没有先克隆样式对象")
        if not re.search(r"_cell4\.s\s*=\s*_cp4\s*;", inline):
            errors.append("不变量②被破坏：剥离后的样式没有写回克隆副本 _cp4")
        # 旧 BUG 写法：直接 delete 原对象
        for mm in re.finditer(r"delete\s+_s4\s*\.\s*(cl|bl)", inline):
            errors.append("第 %d 行出现旧 BUG 写法 `delete _s4.%s`：直接删实时样式库的对象，"
                          "保存会把屏幕上的红色高亮抹掉" % (line_of(text, text.find(inline) + mm.start()),
                                                     mm.group(1)))

    # ---- ③ 自愈：行号没变也要确认红+粗还在 ----
    for nm in ("finHiCellHasHi", "finHiRowHasHi"):
        if fn_body(text, nm) is None:
            errors.append("不变量③被破坏：找不到 %s（高亮自愈能力被删除）" % nm)

    rec = fn_body(text, "finHiRecompute")
    if rec is None:
        errors.append("找不到 finHiRecompute（高亮重算入口被删除？）")
    else:
        if not re.search(r"if\s*\(\s*rowsSame\s*&&\s*styleOk\s*\)\s*return", rec):
            errors.append("不变量③被破坏：finHiRecompute 的【无变化】判定不再检查 styleOk"
                          "（只看行号→样式被洗掉后再也不会补回）")
        if not re.search(r"finHiRowHasHi\s*\(", rec):
            errors.append("不变量③被破坏：finHiRecompute 没有调用 finHiRowHasHi 做样式抽查")
        if not re.search(r"finHiHealAt\s*=\s*Date\.now\(\)\s*\+\s*FIN_HI_LOCK\.healMs", rec):
            errors.append("不变量③被破坏：自愈通道缺少 finHiHealAt 节流")
        if not re.search(r"if\s*\(\s*!rowsSame\s*\)\s*prev\.forEach", rec):
            errors.append("不变量③被破坏：撤回旧高亮不再是【仅当行号真的变了】才执行"
                          "（样式被洗掉时应直接重写，不撤回）")
        if len(re.findall(r"prev\.forEach\s*\(\s*function", rec)) != 1:
            errors.append("finHiRecompute 中 prev.forEach 出现次数不为 1，撤回逻辑可能被改坏")

    # ---- ④ 自检函数本身必须存在（行为级回归测试） ----
    for nm in ("finHiLockCheck", "finHiLockVerify"):
        if fn_body(text, nm) is None:
            errors.append("找不到 %s（锁死区行为级自检被删除）" % nm)

    lockchk = fn_body(text, "finHiLockCheck")
    if lockchk is not None and "fin_inlineStyles" not in lockchk:
        warnings.append("finHiLockCheck 未调用 fin_inlineStyles，自检可能不再覆盖保存路径")

    return errors, warnings


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "choice_lite.html")
    if not os.path.exists(path):
        print("✗ 找不到文件: %s" % path)
        sys.exit(1)

    errors, warnings = check_html(path)

    print("检查目标: %s" % path)
    for w in warnings:
        print("  ! 警告: %s" % w)
    if not errors:
        print("✓ 通过：财务屏幕高亮锁定契约未被破坏（%s 四条不变量全在）" % DOC_ID)
        sys.exit(0)
    for e in errors:
        print("  ✗ 违规: %s" % e)
    print("✗ 失败：共 %d 处违规。这是「锁死」契约，禁止篡改；"
          "请恢复 %s 的四条不变量后再提交。" % (len(errors), DOC_ID))
    sys.exit(1)


if __name__ == "__main__":
    main()
