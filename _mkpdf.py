from playwright.sync_api import sync_playwright
import os, datetime

HTML = 'file:///C:/vnchoicedouble/training_manual.html'
PDF = r'C:\vnchoicedouble\Choice_Slats_Ops_Manual.pdf'

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    pg = b.new_page()
    pg.goto(HTML, wait_until='networkidle', timeout=30000)
    pg.wait_for_timeout(800)
    pg.pdf(
        path=PDF,
        print_background=True,
        prefer_css_page_size=True,
        display_header_footer=True,
        header_template='<div></div>',
        footer_template='<div style="font-size:8px;width:100%;text-align:center;color:#888;font-family:Arial;">Choice Slats VN &middot; T&#224;i li&#7879;u &#273;&#224;o t&#7841;o &middot; <span class="pageNumber"></span> / <span class="totalPages"></span></div>',
    )
    b.close()

pgs = 0
try:
    import pypdf
    pgs = len(pypdf.PdfReader(PDF).pages)
except Exception as e:
    print('pgcount err', e)

print('PDF OK ->', PDF, os.path.getsize(PDF), 'bytes', '| PAGES:', pgs, '|', datetime.datetime.now().strftime('%H:%M:%S'))
