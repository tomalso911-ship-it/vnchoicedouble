# -*- coding: utf-8 -*-
"""一次性补齐全部项目里缺失/旧版(v!=2)的上午(09点)/下午(14点)天气。
走运行中的服务端 API（GET 取服务端最新副本 → 只在副本上补天气 → 原样 PUT 回），
不直接改数据库、不改动任何其它字段与日期键格式、不动业务数据。

用法:  python _wx_fix_all.py            # 试运行（只报告，不写）
       python _wx_fix_all.py --apply    # 真正写入
"""
import sqlite3, json, sys, os, re, datetime, unicodedata
import urllib.request, urllib.parse

sys.stdout.reconfigure(encoding="utf-8")
BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, "agi_pm.db")
SRV = "http://127.0.0.1:5050"
ME = "tom"
APPLY = "--apply" in sys.argv

BEAUFORT = [(1, 0), (5, 1), (11, 2), (19, 3), (28, 4), (38, 5), (49, 6), (61, 7), (74, 8), (88, 9), (102, 10), (117, 11), (10**9, 12)]


def beaufort(kmh):
    if kmh is None:
        return None
    for lim, lv in BEAUFORT:
        if kmh <= lim:
            return lv
    return 12


def wx_from_hourly(hr, i):
    if not hr or i < 0 or i >= len(hr["time"]):
        return None
    t = hr["temperature_2m"][i]
    if t is None:
        return None
    code = hr["weather_code"][i]
    h = hr["relative_humidity_2m"][i]
    ws = hr["wind_speed_10m"][i]
    lv = beaufort(ws) if ws is not None else None
    return {"temp": "%d°C" % round(t), "code": code,
            "hum": ("%d%%" % round(h)) if h is not None else "—",
            "wind": ("%d级" % lv) if lv is not None else "—", "v": 2}


def hour_idx(hr, ymd, hh):
    if not hr:
        return -1
    exact = "%sT%s:00" % (ymd, hh)
    if exact in hr["time"]:
        return hr["time"].index(exact)
    for i, t in enumerate(hr["time"]):
        if t.startswith("%sT%s" % (ymd, hh)):
            return i
    return -1


def prov_norm(s):
    s = str(s or "").lower()
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.replace("đ", "d")
    return re.sub(r"[^a-z0-9]", "", s)


def load_prov():
    """从 vn_provinces.js 读取 VN_PROVINCES + VN_PROV_ALIAS，等价实现前端 vnProvinceByKey。"""
    js = open(os.path.join(BASE, "vn_provinces.js"), encoding="utf-8").read()
    table = {}
    for vi, lat, lng in re.findall(r"vi:\s*'([^']+)'[^}]*?lat:\s*([\d.]+)\s*,\s*lng:\s*([\d.]+)", js):
        table[prov_norm(vi)] = {"vi": vi, "lat": float(lat), "lng": float(lng)}
    alias = {}
    for k, v in re.findall(r"([a-z]+):'([a-z]+)'", js[js.find("VN_PROV_ALIAS"):]):
        alias[k] = v
    return table, alias


VN_TABLE, VN_ALIAS = load_prov()


def vn_prov(name):
    k = prov_norm(name)
    if k in VN_TABLE:
        return VN_TABLE[k]
    a = VN_ALIAS.get(k)
    if a and a in VN_TABLE:
        return VN_TABLE[a]
    return None


def dmy_to_ymd(d):
    if not d:
        return ""
    p = re.split(r"[-/.]", str(d))
    if len(p) != 3 or len(p[2]) != 4:
        return ""
    return "%s-%s-%s" % (p[2], p[1], p[0])


def fetch_json(url, timeout=30):
    r = urllib.request.urlopen(url, timeout=timeout)
    return json.loads(r.read().decode())


def http_get_factory(pid):
    u = "%s/api/prod-factory/%s?me=%s" % (SRV, urllib.parse.quote(str(pid)), urllib.parse.quote(ME))
    return fetch_json(u).get("data")


def http_put_factory(pid, data):
    u = "%s/api/prod-factory/%s" % (SRV, urllib.parse.quote(str(pid)))
    body = json.dumps({"requester": ME, "data": data}, ensure_ascii=False).encode()
    req = urllib.request.Request(u, data=body, headers={"Content-Type": "application/json"}, method="PUT")
    return json.loads(urllib.request.urlopen(req, timeout=90).read().decode())


def fetch_hourly(pr, start, end):
    """与前端一致：近 92 天用 forecast，更早走 archive，跨 92 天时分段合并。"""
    q = ("?latitude=%s&longitude=%s&hourly=temperature_2m,relative_humidity_2m,"
         "wind_speed_10m,weather_code&timezone=Asia%%2FHo_Chi_Minh"
         % (pr["lat"], pr["lng"]))

    def url_for(base, s, e):
        return base + q + "&start_date=" + s + "&end_date=" + e

    def get(url):
        try:
            return fetch_json(url)
        except Exception as e:
            print("    请求失败:", e)
            return None

    def near(s, e):
        d = get(url_for("https://api.open-meteo.com/v1/forecast", s, e))
        if d and (d.get("hourly") or {}).get("time"):
            return d["hourly"]
        d = get(url_for("https://archive-api.open-meteo.com/v1/archive", s, e))
        return (d or {}).get("hourly") if d else None

    def arch(s, e):
        d = get(url_for("https://archive-api.open-meteo.com/v1/archive", s, e))
        return (d or {}).get("hourly") if d else None

    cut = (datetime.date.today() - datetime.timedelta(days=91)).strftime("%Y-%m-%d")
    if start >= cut:
        return near(start, end)
    old_end = (datetime.datetime.strptime(cut, "%Y-%m-%d") - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    a = arch(start, old_end)
    b = near(max(start, cut), end)
    if not a:
        return b
    if not b:
        return a
    idx = {t: i for i, t in enumerate(a["time"])}
    for i, t in enumerate(b["time"]):
        if t in idx:
            j = idx[t]
            for f in ("temperature_2m", "relative_humidity_2m", "wind_speed_10m", "weather_code"):
                a[f][j] = b[f][i]
        else:
            idx[t] = len(a["time"])
            a["time"].append(t)
            for f in ("temperature_2m", "relative_humidity_2m", "wind_speed_10m", "weather_code"):
                a[f].append(b[f][i])
    return a


def main():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    prov_by_id = {str(r["id"]): (r["province"] or "").strip() for r in con.execute("SELECT id, province FROM won_projects")}
    pids = [r["project_id"] for r in con.execute("SELECT project_id FROM prod_factory ORDER BY project_id")]
    con.close()

    today = datetime.date.today().strftime("%Y-%m-%d")
    hh_now = datetime.datetime.now().hour
    print("今天参数: %s  当前小时: %d  模式: %s" % (today, hh_now, "APPLY(写入)" if APPLY else "DRY-RUN(只报告)"))
    print("省份表条目: %d  别名: %d" % (len(VN_TABLE), len(VN_ALIAS)))

    total_slots = total_changed = total_projects = 0
    for pid in pids:
        data = http_get_factory(pid)
        if not data:
            print("[%s] 服务端无数据，跳过" % pid)
            continue
        prov = prov_by_id.get(str(pid)) or ((data.get("profile") or {}).get("province") or "")
        slots = []

        def scan(mapobj):
            if not isinstance(mapobj, dict):
                return
            for k, o in mapobj.items():
                if not isinstance(o, dict) or o.get("_deleted"):
                    continue
                ymd = dmy_to_ymd(k) or str(k)
                if not ymd or len(ymd) != 10:
                    continue
                na = (not o.get("weatherAm")) or (o["weatherAm"] or {}).get("v") != 2
                np_ = (not o.get("weatherPm")) or (o["weatherPm"] or {}).get("v") != 2
                if na or np_:
                    slots.append({"ymd": ymd, "o": o, "am": na, "pm": np_, "key": k})

        scan(data.get("workers"))
        scan(data.get("production"))
        scan((data.get("installation") or {}).get("workers"))
        for _hk, rec in (data.get("houseOut") or {}).items():
            if isinstance(rec, dict):
                scan(rec.get("outDaily"))
                scan(rec.get("inDaily"))

        if not slots:
            print("[%s] 无缺口  province=%r" % (pid, prov))
            continue
        total_slots += len(slots)
        print("\n[%s] province=%r 缺口 %d 条 -> %s" % (pid, prov, len(slots),
              "; ".join("%s(AM%s,PM%s)" % (s["key"], "缺" if s["am"] else "有", "缺" if s["pm"] else "有") for s in slots)))
        pr = vn_prov(prov)
        if not pr:
            print("    ✗ 省份坐标找不到（%r），跳过" % prov)
            continue
        hr = fetch_hourly(pr, min(s["ymd"] for s in slots), max(s["ymd"] for s in slots))
        if not hr:
            print("    ✗ 天气接口无数据，跳过")
            continue
        changed = 0
        for s in slots:
            is_today = (s["ymd"] == today)
            if s["am"] and (not is_today or hh_now >= 9):
                w = wx_from_hourly(hr, hour_idx(hr, s["ymd"], "09"))
                if w:
                    s["o"]["weatherAm"] = w
                    changed += 1
            if s["pm"] and (not is_today or hh_now >= 14):
                w = wx_from_hourly(hr, hour_idx(hr, s["ymd"], "14"))
                if w:
                    s["o"]["weatherPm"] = w
                    changed += 1
        if not changed:
            print("    ✗ 无可写入（未到时间点或接口缺该时段）")
            continue
        total_changed += changed
        total_projects += 1
        if APPLY:
            res = http_put_factory(pid, data)
            print("    ✓ 写入 %d 个时段  PUT ok=%s stale=%s" % (changed, res.get("ok"), res.get("stale")))
        else:
            print("    · 将写入 %d 个时段（试运行未落库）" % changed)

    print("\n===== 汇总 =====\n涉及项目 %d 个，缺口时段 %d 个，实际可写 %d 个" % (total_projects, total_slots, total_changed))
    if not APPLY:
        print("（试运行；确认无误后加 --apply 真正写入）")


if __name__ == "__main__":
    main()
