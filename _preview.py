from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width':794,'height':1100})
    pg.goto('file:///C:/vnchoicedouble/training_manual.html', wait_until='load')
    pg.wait_for_timeout(1500)
    pg.emulate_media(media='print')
    # 截三段：登录区、看板区、TabA区
    for sel, name in [('.tri','_prev_first'), ('h2','_prev_h2')]:
        try:
            pg.locator(sel).first.screenshot(path=f'training_shots/{name}.png')
        except Exception as e:
            print('err', name, e)
    # 滚动到 TabA 再截
    pg.evaluate("document.querySelectorAll('h2')[5].scrollIntoView()")
    pg.wait_for_timeout(400)
    pg.screenshot(path='training_shots/_prev_tabA.png', clip={'x':0,'y':0,'width':794,'height':1000})
    b.close()
print('ok')
