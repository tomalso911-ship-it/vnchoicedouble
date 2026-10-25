from playwright.sync_api import sync_playwright
import os

URL = 'https://choice-vn-crm.duckdns.org/lite?v=7c719566190d'
OUT = r'C:\vnchoicedouble\training_shots\tri'
LANGS = [('vi','VI'), ('zh','中'), ('en','EN')]
TABS = ['A','B','C','D','E','H','F']

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
    pg = b.new_page(viewport={'width':414,'height':896}, device_scale_factor=2)
    pg.goto(URL, wait_until='networkidle', timeout=60000)
    pg.wait_for_timeout(1500)
    pg.fill('#loginUser','tom'); pg.fill('#loginPwd','66668888'); pg.click('#loginBtn')
    pg.wait_for_timeout(2500)

    for code, _ in LANGS:
        set_lang(pg, code)
        # 打开工厂（只一次），等数据加载
        pg.evaluate('prod_open("27")')
        pg.wait_for_timeout(1500)
        for t in TABS:
            pg.evaluate(f'prod_renderTab("{t}")')
            pg.wait_for_timeout(1500)
            fn = os.path.join(OUT, f'tab{t}_{code}.png')
            pg.screenshot(path=fn)
            log.append(f'tab{t}_{code} OK')
    b.close()

open(os.path.join(OUT,'_capture_tabsfix_log.txt'),'w',encoding='utf-8').write('\n'.join(log))
print('DONE', len(log))
