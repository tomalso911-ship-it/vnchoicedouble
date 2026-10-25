# -*- coding: utf-8 -*-
"""★FIN-TOTAL-LABEL-LOCK-20261017 数据修复：
把 finance_data/fin_trans_cache.json 里「合计行标签」的中文译文从「全部的」改成「总计」
（英文 TOTAL / 越南文 TỔNG CỘNG 一并对齐），并先备份原文件。
只改这一批 key，其它条目一个字都不动。"""
import io
import json
import os
import shutil
import sys
import time

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(ROOT, "finance_data", "fin_trans_cache.json")

LOCK = {"zh": "总计", "en": "TOTAL", "vi": "TỔNG CỘNG"}
SRC = {x.upper() for x in ("TỔNG CỘNG", "Tổng cộng", "Tổng", "TOTAL", "TOTAL CỘNG",
                           "全部的", "全部", "合计", "总计", "共計", "合計")}


def main():
    if not os.path.isfile(CACHE):
        print("!! 找不到 %s" % CACHE)
        return 1
    with io.open(CACHE, encoding="utf-8") as f:
        data = json.load(f)

    bak = CACHE + ".bak_total_label_" + time.strftime("%Y%m%d_%H%M%S")
    shutil.copy2(CACHE, bak)
    print("备份 → %s" % os.path.basename(bak))

    changed = []
    for k in list(data.keys()):
        if "|" not in k:
            continue
        src, lang = k.rsplit("|", 1)
        if lang not in LOCK:
            continue
        base = src.strip()
        if base.endswith(":") or base.endswith("："):
            base = base[:-1].strip()
        if base.upper() not in SRC:
            continue
        new = LOCK[lang]
        old = data.get(k)
        if old != new:
            data[k] = new
            changed.append((k, old, new))

    if not changed:
        print("无需改动（缓存里合计标签已经正确）")
        return 0

    tmp = CACHE + ".tmp"
    with io.open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=0, sort_keys=True)
    os.replace(tmp, CACHE)
    for k, o, n in changed:
        print("  %-24s : %r → %r" % (k, o, n))
    print("共修改 %d 条" % len(changed))
    return 0


if __name__ == "__main__":
    sys.exit(main())
