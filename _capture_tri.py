from playwright.sync_api import sync_playwright
import os

URL = 'https://choice-vn-crm.duckdns.org/lite?v=7c719566190d'
OUT = r'C:\vnchoicedouble\training_shots\tri'
os.makedirs(OUT, exist_ok=True)
LANGS = [('vi','VI'), ('zh','中'), ('en','EN')]

# 每个视图 = 一组导航步骤(JS)
STEPS = {
 'board':   ["switchView('dashboard')"],
 'prod_list':["switchView('production')"],
 'tabA':    ["switchView('production')","prod_open('27')","prod_renderTab('A')"],
 'tabB':    ["switchView('production')","prod_open('27')","prod_renderTab('B')"],
 'tabC':    ["switchView('production')","prod_open('27')","prod_renderTab('C')"],
 'tabD':    ["switchView('production')","prod_open('27')","prod_renderTab('D')"],
 'tabE':    ["switchView('production')","prod_open('27')","prod_renderTab('E')"],
 'tabH':    ["switchView('production')","prod_open('27')","prod_renderTab('H')"],
 'tabF':    ["switchView('production')","prod_open('27')","prod_renderTab('F')"],
 'worklog': ["switchView('worklog')"],
 'worklog_detail':["switchView('worklog')","(function(){var c=document.querySelector(\"[data-pid],.wl-project,[onclick*=\\\"wl_open\\\"]\");if(c)c.click();})()"],
 'install': ["switchView('install')"],
 'approvals':["switchView('approvals')"],
 'library': ["switchView('library')"],
 'users':   ["switchView('users')"],
}
ORDER = ['board','prod_list','tabA','tabB','tabC','tabD','tabE','tabH','tabF',
         'worklog','worklog_detail','install','approvals','library','users']

def set_lang(pg, code):
    res = pg.evaluate("""(c)=>{
       const fns=[window.setLang, window.__app&&window.__app.setLang, window.switchLang];
       for(const f of fns){ if(typeof f==='function'){ try{ f(c); return 'ok'; }catch(e){} } }
       return 'nofn';
    }""", code)
    if res != 'ok':
        label = {'vi':'VI','zh':'中','en':'EN'}[code]
        try:
            pg.evaluate("""(lbl)=>{
               const els=[...document.querySelectorAll('button,span,a,div')];
               const el=els.find(e=>e.textContent.trim()===lbl && e.offsetParent!==null && e.children.length===0);
               if(el) el.click();
            }""", label)
        except Exception: pass
    pg.wait_for_timeout(900)

log=[]
with sync_playwright() as p:
    b = p.chromium.launch(args=['--ignore-certificate-errors'])
    pg = b.new_page(viewport={'width':480,'height':900}, device_scale_factor=1)
    pg.goto(URL, wait_until='networkidle', timeout=60000)
    pg.wait_for_timeout(1500)
    pg.screenshot(path=os.path.join(OUT,'login_default.png'), full_page=True)
    log.append('login_default OK')
    pg.fill('#loginUser','tom'); pg.fill('#loginPwd','66668888'); pg.click('#loginBtn')
    pg.wait_for_timeout(2500)

    for name in ORDER:
        steps = STEPS[name]
        for code,_ in LANGS:
            set_lang(pg, code)
            for i,s in enumerate(steps):
                pg.evaluate(s)
                pg.wait_for_timeout(1400 if i==len(steps)-1 else 900)
            fn = os.path.join(OUT, f'{name}_{code}.png')
            pg.screenshot(path=fn, full_page=True)
            log.append(f'{name}_{code} OK')
    b.close()

open(os.path.join(OUT,'_capture_log.txt'),'w',encoding='utf-8').write('\n'.join(log))
print('DONE', len(log))
