from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    pg = b.new_page()
    weather_urls = []
    pg.on('request', lambda req: weather_urls.append(req.url) if 'open-meteo.com' in req.url else None)
    pg.goto('http://localhost:5050/lite', wait_until='load', timeout=20000)
    pg.wait_for_timeout(1500)
    pg.fill('#loginUser', 'tom')
    pg.fill('#loginPwd', '66668888')
    pg.click('#loginBtn')
    pg.wait_for_timeout(2000)
    t0 = time.time()
    pg.evaluate("if(window.switchView) switchView('dashboard')")
    pg.wait_for_selector('#bdTop10Body .bd-t10-row', timeout=20000)
    pg.wait_for_selector('#bdProdProg .bd-t10-row', timeout=20000)
    t1 = time.time()
    print('progress rows ready:', round(t1-t0,2), 's')
    pg.wait_for_selector('#bdWxBody .bd-wx-chip', timeout=20000)
    t2 = time.time()
    print('weather chips ready:', round(t2-t0,2), 's')
    print('weather urls:', weather_urls)
    print('hourly in url:', any('hourly' in u for u in weather_urls))
    b.close()
