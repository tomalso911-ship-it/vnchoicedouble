import io, sys, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    pg = b.new_page(viewport={'width':1280,'height':900})
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('http://localhost:5050/lite', wait_until='load', timeout=20000)
    pg.wait_for_timeout(1500)
    pg.fill('#loginUser', 'tom'); pg.fill('#loginPwd', '66668888'); pg.click('#loginBtn')
    pg.wait_for_timeout(2000)
    pg.evaluate("if(window.switchView) switchView('worklog')")
    pg.wait_for_selector('#wl-cards .prod-card', timeout=20000)
    pg.click('#wl-cards .prod-card:first-child')
    pg.wait_for_selector('#wl-tabs .wl-tab', timeout=20000)
    pg.click('#wl-tabs .wl-tab[data-key="mywork"]')
    pg.wait_for_selector('.wl-flow-card', timeout=20000)
    res = pg.evaluate("""
      (function(){
        var cards = document.querySelectorAll('.wl-flow-card');
        return [].map.call(cards, function(c){
          var img = c.querySelector('img.wl-flow-svg');
          return { title: c.querySelector('.wl-flow-title').textContent, num: c.querySelector('.wl-flow-num').textContent, src: img?img.getAttribute('src'):null };
        });
      })();
    """)
    print(json.dumps(res, ensure_ascii=False))
    # verify svg route serves
    r = pg.goto('http://localhost:5050/flow_svg/01_purchase.svg')
    print('svg status:', r.status, 'ctype:', r.headers.get('content-type'))
    print('errors:', errs)
    b.close()
    print('OK')
