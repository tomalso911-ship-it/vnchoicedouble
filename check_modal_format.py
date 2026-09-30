#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模态框格式「锁死」检查（lint / CI / git pre-commit 均可用）。

契约（见 choice_lite.html 中 .mmax 的 [FROZEN 契约] 注释）：
  1) 放大态几何只能由唯一的 .mmax 规则定义，全文件必须恰好定义一次；
  2) 禁止为某个具体弹窗写 .xxx.mmax { position/top/left/... } 之类的“特例覆盖”；
  3) .mmax 类只能由 window.toggleMaximize 添加（唯一入口），不得别处 classList.add('mmax')。

用法：
  python3 check_modal_format.py [path/to/choice_lite.html]
不传路径时默认检查同目录下的 choice_lite.html。
退出码：0 = 通过；1 = 发现违规（可用于 CI 失败 / pre-commit 拦截）。
"""
import os
import re
import sys

# Windows 控制台默认 cp1252，重设 stdout/stderr 为 UTF-8，避免中文打印崩溃
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# 被 .mmax 锁死的几何属性（与 choice_lite.html 中 .mmax 规则一致）
GEOM_PROPS = {
    "position", "top", "left", "right", "bottom",
    "width", "height", "max-width", "max-height", "min-width", "min-height",
    "margin", "transform", "border-radius",
}

# 匹配一个“完整”的 .mmax 类 token（排除 .mmax-btn 这类伪命中）
MMAX_TOKEN = re.compile(r"\.mmax(?![-\w])")


def extract_rules(css):
    """剥离注释后，递归抽取所有非 at-rule 的 (selector, body) 规则。"""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)  # 去注释
    rules = []

    def parse(s):
        i, n = 0, len(s)
        buf = ""
        while i < n:
            c = s[i]
            if c == "{":
                depth = 1
                j = i + 1
                while j < n and depth > 0:
                    if s[j] == "{":
                        depth += 1
                    elif s[j] == "}":
                        depth -= 1
                    j += 1
                body = s[i + 1:j - 1]
                sel = buf.strip()
                if sel.startswith("@"):
                    parse(body)  # at-rule（@media/@keyframes…）内部继续递归
                else:
                    rules.append((sel, body))
                buf = ""
                i = j
            elif c == "}":
                buf = ""
                i += 1
            else:
                buf += c
                i += 1

    parse(css)
    return rules


def split_simple_selectors(part):
    """把选择器片段按组合符拆成简单选择器列表。"""
    return [s.strip() for s in re.split(r"[\s>~+]", part) if s.strip()]


def body_props(body):
    return set(re.findall(r"([a-zA-Z-]+)\s*:", body))


def check_html(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    # ---- 1) 抽取所有 <style> 块做 CSS 检查 ----
    style_blocks = re.findall(r"<style[^>]*>(.*?)</style>", text, flags=re.DOTALL)
    all_rules = []
    for sb in style_blocks:
        all_rules.extend(extract_rules(sb))

    errors = []
    warnings = []
    canonical_count = 0
    canonical_body = None

    for sel, body in all_rules:
        norm = sel.strip()
        props = body_props(body)
        has_geom = bool(props & GEOM_PROPS)

        # 该规则的选择器中是否“直接作用于带 .mmax 的盒子本身”
        # 注意：CSS 规则的“主体”是各片段的【最后一个】简单选择器；
        # 形如 .mmax #modalBody / .mmax .cm-body 是给后代元素设样式（合法），
        # 不算覆盖 .mmax 盒子，必须排除。
        targets_box = False
        is_canonical_sel = False
        for part in norm.split(","):
            simples = split_simple_selectors(part)
            if not simples:
                continue
            last = simples[-1]  # 主体简单选择器
            if last == ".mmax":
                targets_box = True
                is_canonical_sel = True
            elif MMAX_TOKEN.search(last):
                targets_box = True  # 形如 .modal.mmax / div.mmax 的复合选择器（作用于盒子本身）

        if not targets_box:
            continue

        if is_canonical_sel and norm == ".mmax":
            # 这是唯一的真相源规则
            canonical_count += 1
            canonical_body = body
        elif has_geom:
            # 非 .mmax 唯一规则、却给 .mmax 盒子设置了几何属性 → 特例覆盖，违规
            errors.append(
                "发现 .mmax 特例覆盖（禁止）：选择器 `%s` 设置了几何属性 %s"
                % (norm, sorted(props & GEOM_PROPS))
            )

    if canonical_count == 0:
        errors.append("未找到唯一的 .mmax 规则（放大态几何无定义）")
    elif canonical_count > 1:
        errors.append(".mmax 规则定义了 %d 次，必须恰好 1 次（单一真相源）" % canonical_count)

    if canonical_body is not None:
        cb_props = body_props(canonical_body)
        missing = {"position", "top", "left", "right", "bottom", "border-radius"} - cb_props
        if missing:
            errors.append("唯一 .mmax 规则缺少核心几何属性：%s" % sorted(missing))

    # ---- 2) JS 检查：.mmax 类只能由 window.toggleMaximize 添加 ----
    m = re.search(r"window\.toggleMaximize\s*=\s*function", text)
    if not m:
        warnings.append("未找到 window.toggleMaximize 定义（无法校验唯一添加入口）")
    else:
        # 从函数起点做括号匹配，得到函数结束位置（行号）
        start_idx = m.start()
        fb = text.find("{", start_idx)
        depth = 0
        end_idx = fb
        i = fb
        while i < len(text):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    end_idx = i
                    break
            i += 1
        fn_start_line = text.count("\n", 0, start_idx) + 1
        fn_end_line = text.count("\n", 0, end_idx) + 1

        add_re = re.compile(r"classList\.add\(['\"]mmax['\"]\)")
        for am in add_re.finditer(text):
            line = text.count("\n", 0, am.start()) + 1
            if not (fn_start_line <= line <= fn_end_line):
                errors.append(
                    "第 %d 行在 window.toggleMaximize 之外调用了 classList.add('mmax')，"
                    "违反唯一入口契约" % line
                )

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
    if not errors and not warnings:
        print("✓ 通过：模态框格式锁定契约未被破坏（.mmax 唯一、无特例覆盖、入口唯一）")
        sys.exit(0)
    for e in errors:
        print("  ✗ 违规: %s" % e)
    print("✗ 失败：共 %d 处违规，请修复后再提交。" % len(errors))
    sys.exit(1)


if __name__ == "__main__":
    main()
