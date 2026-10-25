import subprocess, sqlite3, json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT='c:/vnchoicedouble'
def load(p):
    con=sqlite3.connect(p); cur=con.cursor()
    cur.execute("SELECT data FROM prod_factory WHERE project_id='19'"); r=cur.fetchone(); con.close()
    return json.loads(r[0]) if r else None
tmp=ROOT+'/_tmp_g.db'
open(tmp,'wb').write(subprocess.check_output(['git','show','4204e31c:agi_pm.db'],cwd=ROOT))
g=load(tmp); os.remove(tmp); c=load(ROOT+'/agi_pm.db')

def inst_rows(f):
    ws=(f.get('installation') or {}).get('workers') or {}
    days=0; rows=0
    for d,dw in ws.items():
        if not isinstance(dw,dict) or dw.get('_deleted'): continue
        days+=1
        for zn,teams in (dw.get('zoneTeamWorkers') or {}).items():
            for t in (teams or []):
                rows+=len((t or {}).get('todayInstall') or {})
    return days,rows
print('安装 天数/记录行:  完整版=%s   当前=%s' % (inst_rows(g), inst_rows(c)))

def od(f):
    ho=f.get('houseOut') or {}
    tot=0
    for h,r in ho.items():
        odd=(r or {}).get('outDaily') or {}
        q=0
        for d,v in odd.items(): q += float((v or {}).get('qty') or v or 0)
        tot+=q
    return sum(len((r or {}).get('outDaily') or {}) for r in ho.values()), tot
print('出库 日数/总量:    完整版=%s   当前=%s' % (od(g), od(c)))

def wdays(f): return len(f.get('workers') or {})
print('人员快照天数:      完整版=%d   当前=%d' % (wdays(g), wdays(c)))

def prodtot(f):
    t=0
    for d,r in (f.get('production') or {}).items():
        for n,ln in ((r or {}).get('lines') or {}).items():
            for s,v in (ln.get('qty') or {}).items(): t+=float(v or 0)
            for h,hv in (ln.get('matrix') or {}).items():
                for s,v in hv.items(): t+=float(v or 0)
    return t
print('生产总产量(片):    完整版=%s   当前=%s' % (prodtot(g), prodtot(c)))
