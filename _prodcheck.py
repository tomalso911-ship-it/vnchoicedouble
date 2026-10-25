import sqlite3, json
c = sqlite3.connect('agi_pm.db')
d = json.loads(c.execute('select data from prod_factory where project_id=19').fetchone()[0])
out = {}
prod = d.get('production') or {}
out['production_days'] = len(prod)
sample = {}
for i, k in enumerate(list(prod.keys())[:3]):
    sample[k] = prod[k]
out['production_sample'] = sample
fin = d.get('finished') or {}
out['finished_keys'] = list(fin.keys())
out['finished_sample'] = {k: fin[k] for k in list(fin.keys())[:3]}
open('_prodcheck.json', 'w', encoding='utf-8').write(json.dumps(out, ensure_ascii=False, indent=2))
print('ok')
