import sqlite3, json
con = sqlite3.connect('c:/vnchoicedouble/agi_pm.db'); con.row_factory = sqlite3.Row
cur = con.cursor()
cur.execute("SELECT id, project_id, updated_by, updated_at, length(data) AS len FROM prod_factory_history ORDER BY id")
for r in cur.fetchall():
    d = dict(r)
    print('HIST id=%s proj=%s by=%s at=%s len=%s' % (d['id'], d['project_id'], d['updated_by'], d['updated_at'], d['len']))
print('---- detail for project 19 ----')
cur.execute("SELECT id, updated_by, updated_at, data FROM prod_factory_history WHERE project_id='19' ORDER BY id")
for r in cur.fetchall():
    d = dict(r)
    try: obj = json.loads(d['data'])
    except Exception: obj = {}
    prod = obj.get('production') or {}
    days = sorted(prod.keys())
    print('HIST id=%s by=%s at=%s days=%d first=%s last=%s' % (d['id'], d['updated_by'], d['updated_at'], len(days), days[0] if days else '-', days[-1] if days else '-'))
con.close()
