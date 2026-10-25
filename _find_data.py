import os, json, sqlite3, sys, copy
sys.stdout.reconfigure(encoding='utf-8')
ROOT = 'c:/vnchoicedouble'
PRE = ROOT + '/backups/auto/agi_pm_20261007_154224_interval.db'   # 丢失前最后一个快照
CUR = ROOT + '/agi_pm.db'

def load(path):
    con = sqlite3.connect(path); con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT data, updated_at FROM prod_factory WHERE project_id='19'")
    r = cur.fetchone(); con.close()
    return (json.loads(r['data']), r['updated_at']) if r else (None, None)

pre, pret = load(PRE)
cur, curt = load(CUR)
print('丢失前快照:', os.path.basename(PRE), pret)
print('当前库    : agi_pm.db', curt)

def ymd(d):
    try:
        a = str(d).split('/'); return '%s-%s-%s' % (a[2], a[1], a[0])
    except Exception: return ''

def day_total(rec):
    tot = 0
    for n, ln in ((rec or {}).get('lines') or {}).items():
        for s, v in ((ln or {}).get('qty') or {}).items(): tot += float(v or 0)
        for h, hv in ((ln or {}).get('matrix') or {}).items():
            for s, v in (hv or {}).items(): tot += float(v or 0)
    return tot

report = {'_pre_snapshot': os.path.basename(PRE), '_pre_updated_at': pret,
          '_cur_updated_at': curt, 'missing': {}}

# 1) production
pp, pc = pre.get('production') or {}, cur.get('production') or {}
miss_prod = {d: pp[d] for d in pp if d not in pc}
report['missing']['production'] = miss_prod
print('\n【每日生产】丢失 %d 天（当前 %d 天，恢复后 %d 天）:' % (len(miss_prod), len(pc), len(pp)))
for d in sorted(miss_prod, key=ymd):
    print('   %s  产量=%s  填表人=%s' % (d, day_total(miss_prod[d]), (miss_prod[d] or {}).get('recorder','')))

# 2) houseOut outDaily
hp, hc = pre.get('houseOut') or {}, cur.get('houseOut') or {}
miss_out = {}
for h, rec in hp.items():
    p_od = (rec or {}).get('outDaily') or {}
    c_od = ((hc.get(h) or {}).get('outDaily') or {})
    add = {d: v for d, v in p_od.items() if d not in c_od}
    if add: miss_out[h] = add
report['missing']['houseOut_outDaily'] = miss_out
print('\n【出库日明细】丢失 %d 栋:' % len(miss_out))
for h, add in miss_out.items():
    print('   %s -> 补回日期 %s' % (h, sorted(add, key=ymd)))

# 3) installation workers
ip = (pre.get('installation') or {}).get('workers') or {}
ic = (cur.get('installation') or {}).get('workers') or {}
miss_inst = {d: ip[d] for d in ip if d not in ic}
report['missing']['installation_workers'] = miss_inst
print('\n【安装每日记录】丢失 %d 天:' % len(miss_inst))
for d in sorted(miss_inst, key=ymd): print('   ', d)

# 4) workers 快照
wp, wc = pre.get('workers') or {}, cur.get('workers') or {}
miss_w = {d: wp[d] for d in wp if d not in wc}
report['missing']['workers'] = miss_w
print('\n【人员快照】丢失 %d 天:' % len(miss_w))
for d in sorted(miss_w, key=ymd)[:20]: print('   ', d)

with open(ROOT + '/recovery_plan_prod19.json', 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=1)
print('\n恢复包已生成: recovery_plan_prod19.json')
