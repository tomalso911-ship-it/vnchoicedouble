from playwright.sync_api import sync_playwright
import os

SRC = 'file:///C:/vnchoicedouble/training_manual.html'
OUT = r'C:\vnchoicedouble\training_manual.pdf'

FOOTER = (
    '<div style="width:100%;font-family:Times New Roman,Microsoft YaHei,serif;'
    'font-size:8px;color:#667;padding:0 10mm;display:flex;justify-content:space-between;">'
    '<span>CHOICE SLATS VIET NAM · Sổ tay vận hành /lite · 操作说明书 · Operations Manual</span>'
    '<span><span class="pageNumber"></span> / <span class="totalPages"></span></span>'
    '</div>'
)

with sync_playwright() as p:
    b = p.chromium.launch(args=['--ignore-certificate-errors', '--font-render-hinting=none'])
    pg = b.new_page()
    pg.goto(SRC, wait_until='load', timeout=60000)
    pg.wait_for_timeout(2500)
    imgs = pg.evaluate("""[...document.images].map(i=>({s:i.getAttribute('src'),ok:i.complete&&i.naturalWidth>0}))""")
    bad = [x['s'] for x in imgs if not x['ok']]
    pg.emulate_media(media='print')
    pg.wait_for_timeout(600)
    pg.pdf(path=OUT, format='A4', print_background=True,
           display_header_footer=True, header_template='<div></div>', footer_template=FOOTER,
           margin={'top': '10mm', 'bottom': '13mm', 'left': '10mm', 'right': '10mm'})
    b.close()

size = os.path.getsize(OUT) if os.path.exists(OUT) else 0
print('IMGS', len(imgs), 'BROKEN', len(bad), bad[:5])
print('PDF_BYTES', size)
