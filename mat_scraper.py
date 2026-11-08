# -*- coding: utf-8 -*-
"""
mat_scraper.py —— 爬取清化省建材价格公示系统(giavlxd.thanhhoa.gov.vn)的真实砂/石价，
写入 price_snapshot.json 的最新月，覆盖种子参考价。水泥/钢筋该源没有，保留原值。
运行: python3 mat_scraper.py   （可放入 crontab 每月执行）
"""
import io, json, re, ssl, datetime, os, statistics, urllib.request
ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
BASE = "https://giavlxd.thanhhoa.gov.vn"
HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "price_snapshot.json")

# 材料 id -> 我们看板的 4 类映射（取自该站 /vat-lieu 的真实分类）
SAND_IDS = [5, 6, 7]            # Cát xây trát / Cát nghiền / Cát bê tông
GRAVEL_IDS = [3, 4, 10, 11, 12, 13, 14, 15]  # Cấp phối đá dăm / Đá các cỡ

def fetch_material(mid):
    url = BASE + "/vat-lieu/doanh-nghiep?material_id=%d" % mid
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30, context=ctx) as r:
        return json.loads(r.read().decode("utf-8", "replace"))

def collect(ids):
    vals = []
    for mid in ids:
        try:
            j = fetch_material(mid)
            for it in (j.get("data") or []):
                p = it.get("price")
                if not p or p.strip() in ("—", "-", ""):
                    continue
                m = re.search(r"[\d][\d\.,]*", p)
                if not m:
                    continue
                num = float(m.group(0).replace(".", "").replace(",", "."))
                if num > 0:
                    vals.append(num)
        except Exception as e:
            print("  warn material_id=%d: %s" % (mid, e))
    return vals

def median_or_none(vals):
    vals = [v for v in vals if v > 0]
    if not vals:
        return None
    return int(round(statistics.median(vals)))

def main():
    print("爬取清化省公示系统砂/石价 ...")
    sand = median_or_none(collect(SAND_IDS))
    gravel = median_or_none(collect(GRAVEL_IDS))
    print("  砂(中值) VND/m3 =", sand)
    print("  石(中值) VND/m3 =", gravel)
    if sand is None and gravel is None:
        print("未取到任何真实价格，跳过更新。")
        return

    snap = json.load(io.open(SNAP, encoding="utf-8"))
    labels = snap["labels"]
    series = snap["series"]

    # 公示价是"季度"粒度（publish_date=Quý X/YYYY）：
    # ① 若快照缺当前月，自动延展（各序列前向填充）；
    # ② 本季度内所有月份统一覆盖为同一条真实公示价，避免相邻月口径混用造成锯齿
    today = datetime.date.today()
    now_ym = "%04d-%02d" % (today.year, today.month)

    def next_ym(ym):
        y, m = int(ym[:4]), int(ym[5:7])
        m += 1
        if m > 12:
            m, y = 1, y + 1
        return "%04d-%02d" % (y, m)

    while labels[-1] < now_ym:
        nxt = next_ym(labels[-1])
        labels.append(nxt)
        for k in ("rebar", "cement", "sand", "gravel"):
            series[k].append(series[k][-1])

    q_start = "%04d-%02d" % (today.year, ((today.month - 1) // 3) * 3 + 1)
    idxs = [i for i, ym in enumerate(labels) if ym >= q_start]
    if sand is not None:
        for i in idxs:
            series["sand"][i] = sand
    if gravel is not None:
        for i in idxs:
            series["gravel"][i] = gravel

    today_s = today.isoformat()[:10]
    parts = []
    if sand is not None:
        parts.append("砂/石=清化省公示爬取(季度价)")
    if snap.get("_source", "").find("河内") >= 0:
        parts.append("钢/水泥=河内参考价种子")
    snap["_updated"] = today_s
    snap["_source"] = " · ".join(parts) if parts else "清化省建设厅公示系统爬取"
    io.open(SNAP, "w", encoding="utf-8").write(json.dumps(snap, ensure_ascii=False, indent=1))
    print("已更新 price_snapshot.json 本季度(%s~%s): sand=%s gravel=%s updated=%s" % (
        q_start, labels[-1], series["sand"][-1], series["gravel"][-1], today_s))

if __name__ == "__main__":
    main()
