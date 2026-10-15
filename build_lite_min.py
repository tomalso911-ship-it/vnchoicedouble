# -*- coding: utf-8 -*-
"""构建步骤：由 choice_lite.html 生成 choice_lite.min.html（只压缩、不改逻辑）。
安全原则：
  - 源文件 choice_lite.html 原样保留（硬锁脚本都校验它）。
  - 仅移除注释：HTML 注释、<style> 内 CSS 注释、<script> 内 JS 注释。
  - JS 用状态机跳过字符串/模板串/正则，避免误删（注释替换为 1 个空格/换行，保证 token 不粘连）。
  - 生成后由 validate_lite_min.py 用无头浏览器实跑校验，失败可回退。
"""
import io
import os
import re
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'choice_lite.html')
DST = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'choice_lite.min.html')

# 正则之前允许出现的关键字（其后 / 视为正则起始而非除号）
KEYWORDS_BEFORE_RE = {
    'return', 'typeof', 'instanceof', 'in', 'of', 'new', 'delete', 'void',
    'do', 'else', 'yield', 'await', 'throw', 'case', 'default',
}

IDCHAR = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_$')

# 这些前导字符之后，/ 视为正则
REGEX_PRE_CHARS = set('(,=:[!&|?{};+-*%~^<>')


def _regex_allowed(prev):
    """prev: (char, word) 上一个有效字符/上一个标识符词。返回 / 是否可作为正则起始。"""
    ch, word = prev
    if word in KEYWORDS_BEFORE_RE:
        return True
    if ch == '' :
        return True
    if ch in REGEX_PRE_CHARS:
        return True
    return False


def strip_js_comments(src):
    out = []
    i = 0
    n = len(src)
    prev_ch = ''
    prev_word = ''
    word = []
    line_start = True

    def flush_word():
        nonlocal prev_word
        if word:
            prev_word = ''.join(word)
            del word[:]
        else:
            prev_word = ''

    def emit_space():
        # 折叠空白为单个空格；行首不输出
        if not line_start and out and out[-1] not in (' ', '\n'):
            out.append(' ')

    while i < n:
        c = src[i]

        # ---- 字符串 ----
        if c == "'" or c == '"':
            flush_word()
            j = i + 1
            while j < n:
                if src[j] == '\\':
                    j += 2
                    continue
                if src[j] == c:
                    j += 1
                    break
                if src[j] == '\n':
                    break
                j += 1
            out.append(src[i:j])
            prev_ch = c
            line_start = False
            i = j
            continue

        # ---- 模板串 ----
        if c == '`':
            flush_word()
            j = i + 1
            depth = 0
            while j < n:
                if src[j] == '\\':
                    j += 2
                    continue
                if depth == 0 and src[j] == '`':
                    j += 1
                    break
                if src[j] == '$' and j + 1 < n and src[j + 1] == '{':
                    depth += 1
                    j += 2
                    continue
                if depth > 0 and src[j] == '}':
                    depth -= 1
                    j += 1
                    continue
                j += 1
            out.append(src[i:j])
            prev_ch = '`'
            line_start = False
            i = j
            continue

        # ---- 注释 / 正则 / 除号 ----
        if c == '/' and i + 1 < n:
            nxt = src[i + 1]
            if nxt == '/':
                j = i
                while j < n and src[j] != '\n':
                    j += 1
                i = j
                continue
            if nxt == '*':
                j = src.find('*/', i + 2)
                j = n if j == -1 else j + 2
                emit_space()
                i = j
                continue
            if _regex_allowed((prev_ch, prev_word)):
                j = i + 1
                in_class = False
                while j < n:
                    ch = src[j]
                    if ch == '\\':
                        j += 2
                        continue
                    if ch == '\n':
                        break
                    if ch == '[':
                        in_class = True
                    elif ch == ']':
                        in_class = False
                    elif ch == '/' and not in_class:
                        j += 1
                        break
                    j += 1
                while j < n and src[j].isalpha():
                    j += 1
                out.append(src[i:j])
                prev_ch = '/'
                line_start = False
                i = j
                continue

        # ---- 空白 ----
        if c == ' ' or c == '\t' or c == '\r':
            emit_space()
            i += 1
            continue
        if c == '\n':
            if out and out[-1] == ' ':
                out.pop()
            out.append('\n')
            line_start = True
            i += 1
            continue

        # ---- 普通字符 ----
        out.append(c)
        line_start = False
        if c in IDCHAR:
            word.append(c)
        else:
            flush_word()
            prev_ch = c
        i += 1

    return ''.join(out)


def strip_css_comments(src):
    out = []
    i = 0
    n = len(src)
    while i < n:
        c = src[i]
        if c == '/' and i + 1 < n and src[i + 1] == '*':
            j = src.find('*/', i + 2)
            i = n if j == -1 else j + 2
            out.append(' ')
            continue
        if c == '"' or c == "'":
            j = i + 1
            while j < n:
                if src[j] == '\\':
                    j += 2
                    continue
                if src[j] == c:
                    j += 1
                    break
                j += 1
            out.append(src[i:j])
            i = j
            continue
        if c.isspace():
            if out and out[-1] != ' ':
                out.append(' ')
            i += 1
            continue
        out.append(c)
        i += 1
    return ''.join(out)


def strip_html_comments(src):
    return re.sub(r'<!--[\s\S]*?-->', '', src)


SCRIPT_RE = re.compile(r'(<script\b[^>]*>)([\s\S]*?)(</script\s*>)', re.IGNORECASE)
STYLE_RE = re.compile(r'(<style\b[^>]*>)([\s\S]*?)(</style\s*>)', re.IGNORECASE)


def _is_js(open_tag):
    m = re.search(r'type\s*=\s*["\']?([^"\'>\s]+)', open_tag, re.IGNORECASE)
    if not m:
        return True
    t = m.group(1).lower()
    return ('javascript' in t) or (t == 'module')


def _process_html_seg(seg):
    """处理 script 之外的 HTML 段：去 <style> 内 CSS 注释 + 去 HTML 注释。"""
    def _style_repl(m):
        return m.group(1) + strip_css_comments(m.group(2)) + m.group(3)
    seg = STYLE_RE.sub(_style_repl, seg)
    seg = re.sub(r'<!--[\s\S]*?-->', '', seg)
    return seg


def build():
    with io.open(SRC, 'r', encoding='utf-8') as f:
        src = f.read()

    # 先按 script 切分（script 内容单独处理，避免 HTML 注释规则误伤）
    out = []
    pos = 0
    for m in SCRIPT_RE.finditer(src):
        out.append(_process_html_seg(src[pos:m.start()]))
        open_tag, body, close_tag = m.group(1), m.group(2), m.group(3)
        if _is_js(open_tag):
            out.append(open_tag + strip_js_comments(body) + close_tag)
        else:
            out.append(open_tag + body + close_tag)
        pos = m.end()
    out.append(_process_html_seg(src[pos:]))

    result = ''.join(out)

    with io.open(DST, 'w', encoding='utf-8', newline='') as f:
        f.write(result)

    a = os.path.getsize(SRC)
    b = os.path.getsize(DST)
    print('src %.2f MB -> min %.2f MB  (%.1f%% of src)' % (a / 1048576.0, b / 1048576.0, 100.0 * b / a))
    return 0


if __name__ == '__main__':
    sys.exit(build())
