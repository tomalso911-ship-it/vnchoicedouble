from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 794, 'height': 1050})
    pg.goto('file:///C:/vnchoicedouble/training_manual.html', wait_until='load')
    pg.wait_for_timeout(1500)
    pg.emulate_media(media='print')

    # Ch3 开头
    y = pg.evaluate("document.querySelectorAll('h1.chap')[2].getBoundingClientRect().top + window.scrollY")
    pg.evaluate("window.scrollTo(0, %f)" % (y - 10))
    pg.wait_for_timeout(400)
    pg.screenshot(path='training_shots/_prev_ch3.png')

    # 附录 A 术语表
    y2 = pg.evaluate("(function(){var a=document.querySelectorAll('h1.chap'); return a[a.length-3].getBoundingClientRect().top + window.scrollY;})()")
    pg.evaluate("window.scrollTo(0, %f)" % (y2 - 10))
    pg.wait_for_timeout(400)
    pg.screenshot(path='training_shots/_prev_appA.png')
    b.close()
print('ok')
