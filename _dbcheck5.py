import sqlite3, json
c = sqlite3.connect('agi_pm.db'); cur = c.cursor()
cur.execute("PRAGMA table_info(won_projects)")
cols = [r[1] for r in cur.fetchall()]
print("remark/spec/cust cols:", [x for x in cols if any(k in x.lower() for k in ('remark','spec','cust'))])
c.close()
