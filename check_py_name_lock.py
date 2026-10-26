# -*- coding: utf-8 -*-
"""check_py_name_lock.py —— 后端 app.py 「函数名/调用名一致性」锁死区

背景（2026-10-26 线上事故）：
    app.py 里中国报表的「每日备份」函数被误改名成 `_fin_daily_backup`，
    与文件上方【越南报表】的同名函数撞车：
      ① 后定义的（中国版）把越南版顶掉 → 越南报表的每日备份失效；
      ② 三处调用 `_cn_daily_backup()` 变成 NameError →
         POST /api/finance/cn-report/save 恒返回 500（浏览器控制台一片红），
         用户以为"中国报表保存不了"。
    这类错误【语法检查抓不到】（compile 是过的），只有跑到那一行才炸，
    而且藏在保存路径的末尾，前面的 os.replace 已经执行 → 数据写进去了却报错。

本检查做两件事（纯静态 AST，不执行 app.py）：
    ① 同名函数被重复定义（def 重复）→ 直接判失败（顶掉的必定是前一个）。
    ② 调用了「文件里从未定义/赋值/导入」的私有函数名（以下划线开头）→ 判失败。

运行：python check_py_name_lock.py   （退出码 0 = 通过，1 = 契约被破坏）
"""
import ast
import builtins
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
# 默认检查本目录的 app.py；也可显式传一个文件路径（反向测试用：
#   python check_py_name_lock.py _bad_copy.py）
TARGET = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(ROOT, "app.py")

FAILS = []

# Windows 控制台默认 cp1252，中文/符号会直接 UnicodeEncodeError —— 统一成 utf-8。
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def fail(msg):
    FAILS.append(msg)
    print("✗ " + msg)


def collect_bound_names(tree):
    """文件里「任何位置被绑定过」的名字：def/class/赋值/for/with/import/except/参数/global。"""
    bound = set(dir(builtins))
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            bound.add(node.name)
        elif isinstance(node, ast.Name) and isinstance(node.ctx, (ast.Store, ast.Del)):
            bound.add(node.id)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            for a in node.names:
                bound.add(a.asname or a.name.split(".")[0])
        elif isinstance(node, ast.arg):
            bound.add(node.arg)
        elif isinstance(node, ast.ExceptHandler) and node.name:
            bound.add(node.name)
        elif isinstance(node, ast.Global):
            bound.update(node.names)
        elif isinstance(node, (ast.comprehension,)):
            for n in ast.walk(node.target):
                if isinstance(n, ast.Name):
                    bound.add(n.id)
    return bound


def main():
    if not os.path.isfile(TARGET):
        print("! 找不到 app.py，跳过")
        return 0
    src = open(TARGET, "r", encoding="utf-8").read()
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        print("✗ app.py 语法错误：第 %s 行 %s" % (e.lineno, e.msg))
        return 1

    # ① 【模块顶层】def 重名 —— 只有顶层才会真正互相顶掉（函数内部的局部小助手重名无害，
    #    例如两个函数各自定义了 _col/_ids，不能误报）
    seen = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name in seen:
                fail("顶层函数 %s 被重复定义（第 %d 行 与 第 %d 行）—— 后定义的会顶掉前一个，"
                     "请改名区分（例如 _cn_daily_backup / _fin_daily_backup）"
                     % (node.name, seen[node.name], node.lineno))
            else:
                seen[node.name] = node.lineno

    # ② 调用了从未绑定的私有名字
    bound = collect_bound_names(tree)
    reported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            name = node.func.id
            if not name.startswith("_"):
                continue
            if name in bound or name in reported:
                continue
            reported.add(name)
            fail("第 %d 行调用了 %s()，但 app.py 里从未定义/赋值过这个名字 → 运行到即 NameError"
                 "（例：/api/finance/cn-report/save 会 500）" % (node.lineno, name))

    if FAILS:
        print("\n check_py_name_lock: %d 处问题，提交被拦截。" % len(FAILS))
        return 1
    print("check_py_name_lock: OK（函数名唯一、无未定义私有调用）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
