# -*- coding: utf-8 -*-
"""check_appr_need_edit_lock.py —— 「审批返回重新填写 → 收货单变 need_edit → 出现✎重新填写按钮」闭环锁

契约号：APPR-RETURN-LOCK-20261026（2026-10-26 用户报障后锁定）

事故原样：
  审批人在「审批中心」点「返回重新填写」，审批单变 returned，但收货单状态
  仍是 pending → 申请人的「已提交收货单」里永远不出现「✎ 重新填写」按钮，
  流程无法闭环。排查结论：审批回写走 prod_save()，而 prod_pushToServer 有
  「首次同步完成前不推送」门禁(__PROD_SYNCED)，审批人这次会话没打开过该项目
  → 整个 PUT 被静默丢弃，服务端根本没收到 need_edit。

四条不变量（缺一条即复发）：
  ① prodApprLoadFactory 取到服务端数据后必须置 window.__PROD_SYNCED[pid]=true
  ② 必须存在 prodApprSaveFactory(pid,f)：先强制置位同步门禁，再调 prod_save
  ③ prodApprApplyInbound / prodApprMarkReturned / prodApprMarkNeedEdit
     三个回写函数必须调用 prodApprSaveFactory，不得再直接 prod_save(f)
  ④ 收货单卡片仍要有 need_edit → prod_reeditReceipt 的「✎ 重新填写」按钮

运行：python check_appr_need_edit_lock.py   （0=通过，1=契约被破坏）
"""
import io
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = os.path.dirname(os.path.abspath(__file__))
# 默认检查本目录的 choice_lite.html；可显式传一个副本路径（反向测试用）
HTML = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(ROOT, "choice_lite.html")

FAILS = []


def fail(msg):
    FAILS.append(msg)
    print("  ✗ " + msg)


def ok(msg):
    print("  ✓ " + msg)


def func_body(src, name):
    """取 function name(...){ ... } 的函数体（按大括号配对，跳过字符串/注释里的括号足够用）。"""
    m = re.search(r"function\s+" + re.escape(name) + r"\s*\([^)]*\)\s*\{", src)
    if not m:
        return None
    i = m.end() - 1
    depth = 0
    in_s = None
    esc = False
    while i < len(src):
        c = src[i]
        if in_s:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == in_s:
                in_s = None
            i += 1
            continue
        if c in "\"'`":
            in_s = c
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return src[m.start():i + 1]
        i += 1
    return None


def main():
    if not os.path.isfile(HTML):
        print("找不到 choice_lite.html")
        return 1
    with io.open(HTML, "r", encoding="utf-8", errors="replace") as fh:
        src = fh.read()

    print("检查目标: " + HTML)

    # ① prodApprLoadFactory
    b = func_body(src, "prodApprLoadFactory")
    if b is None:
        fail("找不到 function prodApprLoadFactory")
    elif "__PROD_SYNCED" not in b or "window.__PROD_SYNCED[pid]=true" not in b.replace(" ", ""):
        fail("prodApprLoadFactory 未在拿到服务端数据后置 window.__PROD_SYNCED[pid]=true"
             "（门禁不放开 → 回写被静默丢弃）")
    else:
        ok("prodApprLoadFactory 取到服务端快照后置 __PROD_SYNCED[pid]=true")

    # ② prodApprSaveFactory
    b = func_body(src, "prodApprSaveFactory")
    if b is None:
        fail("找不到 function prodApprSaveFactory(pid, f) —— 审批回写绕开门禁的唯一通道")
    else:
        s = b.replace(" ", "")
        if "window.__PROD_SYNCED[pid]=true" not in s:
            fail("prodApprSaveFactory 内没有 window.__PROD_SYNCED[pid]=true")
        elif not re.search(r"return\s+prod_save\s*\(\s*f\s*\)", b):
            fail("prodApprSaveFactory 末尾必须 return prod_save(f)")
        else:
            ok("prodApprSaveFactory 强制置位同步门禁后再 prod_save(f)")

    # ③ 三个回写函数必须走 prodApprSaveFactory
    for fn in ("prodApprApplyInbound", "prodApprMarkReturned", "prodApprMarkNeedEdit"):
        b = func_body(src, fn)
        if b is None:
            fail("找不到 function " + fn)
            continue
        has_force = "prodApprSaveFactory(" in b
        has_raw = re.search(r"(?<![A-Za-z0-9_.$])prod_save\s*\(\s*f\s*\)", b) is not None
        if not has_force:
            fail("%s 必须调用 prodApprSaveFactory(pid, f)（直接 prod_save 会被门禁拦掉）" % fn)
        elif has_raw:
            fail("%s 里仍有裸 prod_save(f)，必须改成 prodApprSaveFactory(pid, f)" % fn)
        else:
            ok("%s 走 prodApprSaveFactory" % fn)

    # ④ need_edit → ✎ 重新填写按钮
    b = func_body(src, "prodReceiptCardHtml")
    if b is None:
        fail("找不到 function prodReceiptCardHtml")
    else:
        s = b.replace(" ", "")
        if "r.status==='need_edit'" not in s:
            fail("prodReceiptCardHtml 缺少 r.status==='need_edit' 判断（按钮不再出现）")
        elif "prod_reeditReceipt(" not in s:
            fail("prodReceiptCardHtml 的「✎ 重新填写」按钮不再调用 prod_reeditReceipt")
        elif "btn_reedit_receipt" not in s:
            fail("prodReceiptCardHtml 缺少 btn_reedit_receipt 三语文案")
        else:
            ok("收货单卡片的 need_edit → ✎ 重新填写 按钮完好")

    if func_body(src, "prod_reeditReceipt") is None:
        fail("找不到 function prod_reeditReceipt（载回表单的逻辑）")
    else:
        ok("prod_reeditReceipt 存在")

    # ⑤ 收货单兜底补建不得因 receipts 未初始化而抛错
    b = func_body(src, "prodApprEnsureReceipt")
    if b is None:
        fail("找不到 function prodApprEnsureReceipt")
    else:
        if "['items','inbound','outbound','receipts']" not in b.replace('"', "'").replace(" ", ""):
            fail("prodApprEnsureReceipt 未逐个补齐 materials 数组（receipts 缺失会 TypeError）")
        else:
            ok("prodApprEnsureReceipt 逐个补齐 materials 数组")

    if FAILS:
        print("\n✗ 失败 %d 项：APPR-RETURN-LOCK-20261026 契约被破坏。" % len(FAILS))
        return 1
    print("\n✓ 通过：审批「返回重新填写」闭环契约（APPR-RETURN-LOCK-20261026）完整。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
