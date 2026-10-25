from playwright.sync_api import sync_playwright
import os, time

URL = 'https://choice-vn-crm.duckdns.org/lite?v=7c719566190d'
OUT = r'C:\vnchoicedouble\training_shots\tri'
os.makedirs(OUT, exist_ok=True)
LANGS = [('vi','VI'), ('zh','中'), ('en','EN')]

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

def shot(pg, path):
    pg.screenshot(path=path, full_page=False)

cap_log=[]
with sync_playwright() as p:
    b = p.chromium.launch(args=['--ignore-certificate-errors'])
    pg = b.new_page(viewport={'width':1000,'height':760}, device_scale_factor=1)
    pg.goto(URL, wait_until='networkidle', timeout=60000)
    pg.wait_for_timeout(1500)
    shot(pg, os.path.join(OUT,'login_default.png')); cap_log.append('login_default OK')
    pg.fill('#loginUser','tom'); pg.fill('#loginPwd','66668888'); pg.click('#loginBtn')
    pg.wait_for_timeout(2500)

    for name in ORDER:
        steps = STEPS[name]
        for code,_ in LANGS:
            try:
                set_lang(pg, code)
                for i,s in enumerate(steps):
                    pg.evaluate(s)
                    pg.wait_for_timeout(1400 if i==len(steps)-1 else 900)
                fn = os.path.join(OUT, f'{name}_{code}.png')
                shot(pg, fn); cap_log.append(f'{name}_{code} OK')
            except Exception as e:
                cap_log.append(f'{name}_{code} ERR {e}')
    b.close()

open(os.path.join(OUT,'_capture_log.txt'),'w',encoding='utf-8').write('\n'.join(cap_log))

# ---- PDF ----
FOOTER = (
    '<div style="width:100%;font-family:Times New Roman,Microsoft YaHei,serif;'
    'font-size:8px;color:#667;padding:0 9mm;display:flex;justify-content:space-between;">'
    '<span>CHOICE SLATS VIET NAM · Sổ tay ảnh /lite · 图文手册 · Picture Manual</span>'
    '<span><span class="pageNumber"></span> / <span class="totalPages"></span></span>'
    '</div>'
)
with sync_playwright() as p:
    b = p.chromium.launch(args=['--ignore-certificate-errors'])
    pg = b.new_page()
    pg.goto('file:///C:/vnchoicedouble/training_manual.html', wait_until='load', timeout=60000)
    pg.wait_for_timeout(2500)
    pg.emulate_media(media='print')
    pg.wait_for_timeout(600)
    pg.pdf(path=r'C:\vnchoicedouble\training_manual.pdf', format='A4', print_background=True,
            display_header_footer=True, header_template='<div></div>', footer_template=FOOTER,
            margin={'top':'10mm','bottom':'13mm','left':'9mm','right':'9mm'})
    b.close()

print('ALL DONE capture=%d pdf=%d KB' % (len(cap_log), os.path.getsize(r'C:\vnchoicedouble\training_manual.pdf')//1024))
