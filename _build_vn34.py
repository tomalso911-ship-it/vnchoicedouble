# -*- coding: utf-8 -*-
# 63 省真实边界 -> 按 2025 合并规则归组为 34 省市，并做几何合并（dissolve）：
# 组内共享边剔除，只保留外轮廓 => 34 省干净多边形 + 全部岛屿，可整体白色描边
import io, json, re, unicodedata

SRC = 'vendor/_vn_hc.geo.json'
OUT = 'vendor/vn34.geo.json'

M = {
 'angiang':'An Giang','kiengiang':'An Giang',
 'bacninh':'Bắc Ninh','bacgiang':'Bắc Ninh',
 'thainguyen':'Thái Nguyên','backan':'Thái Nguyên',
 'camau':'Cà Mau','baclieu':'Cà Mau',
 'hochiminh':'TP. Hồ Chí Minh','binhduong':'TP. Hồ Chí Minh','bariavungtau':'TP. Hồ Chí Minh',
 'vinhlong':'Vĩnh Long','bentre':'Vĩnh Long','travinh':'Vĩnh Long',
 'gialai':'Gia Lai','binhdinh':'Gia Lai',
 'dongnai':'Đồng Nai','binhphuoc':'Đồng Nai',
 'lamdong':'Lâm Đồng','binhthuan':'Lâm Đồng','daknong':'Lâm Đồng',
 'cantho':'Cần Thơ','haugiang':'Cần Thơ','soctrang':'Cần Thơ',
 'caobang':'Cao Bằng',
 'daklak':'Đắk Lắk','phuyen':'Đắk Lắk',
 'danang':'Đà Nẵng','quangnam':'Đà Nẵng',
 'dienbien':'Điện Biên',
 'dongthap':'Đồng Tháp','tiengiang':'Đồng Tháp',
 'tuyenquang':'Tuyên Quang','hagiang':'Tuyên Quang',
 'haiphong':'Hải Phòng','haiduong':'Hải Phòng',
 'ninhbinh':'Ninh Bình','hanam':'Ninh Bình','namdinh':'Ninh Bình',
 'hanoi':'Hà Nội','hatinh':'Hà Tĩnh',
 'phutho':'Phú Thọ','hoabinh':'Phú Thọ','vinhphuc':'Phú Thọ',
 'hungyen':'Hưng Yên','thaibinh':'Hưng Yên',
 'khanhhoa':'Khánh Hòa','ninhthuan':'Khánh Hòa',
 'quangngai':'Quảng Ngãi','kontum':'Quảng Ngãi',
 'laichau':'Lai Châu','langson':'Lạng Sơn','laocai':'Lào Cai','yenbai':'Lào Cai',
 'tayninh':'Tây Ninh','longan':'Tây Ninh',
 'nghean':'Nghệ An',
 'quangtri':'Quảng Trị','quangbinh':'Quảng Trị',
 'quangninh':'Quảng Ninh',
 'sonla':'Sơn La','thanhhoa':'Thanh Hóa',
 'hue':'Huế','thuathienhue':'Huế',
}

def norm(s):
    s = s or ''
    s = re.sub(r'\s*(province|city)\s*$', '', s, flags=re.I)
    s = re.sub(r'^\s*tỉnh\s+', '', s, flags=re.I)
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    s = s.replace('\u0111', 'd').replace('\u0110', 'D')
    s = re.sub(r'[^A-Za-z0-9]', '', s)
    return s.lower()

def ring_area(r):
    a = 0.0
    n = len(r)
    for i in range(n):
        x1, y1 = r[i][0], r[i][1]
        x2, y2 = r[(i + 1) % n][0], r[(i + 1) % n][1]
        a += x1 * y2 - x2 * y1
    return abs(a) / 2.0

def ring_centroid(r):
    cx = cy = a = 0.0
    n = len(r)
    for i in range(n):
        x1, y1 = r[i][0], r[i][1]
        x2, y2 = r[(i + 1) % n][0], r[(i + 1) % n][1]
        f = x1 * y2 - x2 * y1
        a += f
        cx += (x1 + x2) * f
        cy += (y1 + y2) * f
    a *= 0.5
    if abs(a) < 1e-9:
        xs = [p[0] for p in r]; ys = [p[1] for p in r]
        return sum(xs) / len(xs), sum(ys) / len(ys)
    return cx / (6 * a), cy / (6 * a)

def polys_of(geom):
    t = geom.get('type'); c = geom.get('coordinates') or []
    if t == 'Polygon': return [c]
    if t == 'MultiPolygon': return list(c)
    return []

def kp(p): return (round(p[0], 3), round(p[1], 3))

def dissolve(polys):
    """组内共享边剔除：und 计数==1 的有向边保留，按方向缝合回环"""
    und = {}
    directed = {}
    for poly in polys:
        for ring in poly:
            pts = list(ring)
            if len(pts) > 1 and pts[0] == pts[-1]:
                pts = pts[:-1]
            n = len(pts)
            for i in range(n):
                a, b = pts[i], pts[(i + 1) % n]
                ka, kb = kp(a), kp(b)
                if ka == kb: continue
                uk = tuple(sorted([ka, kb]))
                und[uk] = und.get(uk, 0) + 1
                directed[(ka, kb)] = (a, b)
    kept = {}
    for (ka, kb), (a, b) in directed.items():
        uk = tuple(sorted([ka, kb]))
        if und.get(uk, 0) == 1:
            kept[ka] = (kb, a, b)
    rings = []
    used = set()
    for start in list(kept.keys()):
        if start in used: continue
        ring = []
        cur = start
        while cur in kept and cur not in used:
            used.add(cur)
            kb, a, b = kept[cur]
            ring.append([a[0], a[1]])
            cur = kb
        if len(ring) >= 4:
            ring.append(list(ring[0]))
            rings.append(ring)
    return rings

def main():
    src = io.open(SRC, encoding='utf-8').read()
    data = json.loads(src)
    groups = {}
    for f in data.get('features', []):
        props = f.get('properties') or {}
        raw = props.get('name') or props.get('alt-name') or ''
        new = M.get(norm(raw))
        if not new: continue
        for poly in polys_of(f.get('geometry') or {}):
            if poly: groups.setdefault(new, []).append(poly)

    feats = []
    total_rings = 0
    for name in sorted(groups.keys()):
        rings = dissolve(groups[name])
        total_rings += len(rings)
        best = max(rings, key=ring_area)
        cx, cy = ring_centroid(best)
        feats.append({
            'type': 'Feature',
            'properties': {'name': name, 'cp': [round(cx, 3), round(cy, 3)]},
            'geometry': {'type': 'MultiPolygon', 'coordinates': [[r] for r in rings]}
        })

    io.open(OUT, 'w', encoding='utf-8').write(json.dumps({'type':'FeatureCollection','features':feats}, ensure_ascii=False))
    sys = 'features=%d rings=%d' % (len(feats), total_rings)
    print(sys)

    # 全国轮廓：所有省一起 dissolve => 海岸线 + 岛屿外边界（白色描边层用）
    allpolys = []
    bbox = [1e9, 1e9, -1e9, -1e9]
    for name in groups:
        for poly in groups[name]:
            allpolys.append(poly)
            for ring in poly:
                for p in ring:
                    bbox[0] = min(bbox[0], p[0]); bbox[1] = min(bbox[1], p[1])
                    bbox[2] = max(bbox[2], p[0]); bbox[3] = max(bbox[3], p[1])
    orings = dissolve(allpolys)
    ofeat = {'type':'Feature','properties':{'name':'Việt Nam'},
             'geometry':{'type':'MultiPolygon','coordinates':[[r] for r in orings]}}
    io.open('vendor/vn_outline.geo.json', 'w', encoding='utf-8').write(
        json.dumps({'type':'FeatureCollection','features':[ofeat]}, ensure_ascii=False))
    print('outline rings=%d' % len(orings))
    print('bbox lng/lat: %s' % json.dumps([round(x, 2) for x in bbox], ensure_ascii=True))

main()
