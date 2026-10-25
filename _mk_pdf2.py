from playwright.sync_api import sync_playwright
import os
st=[]
HTML='file:///C:/vnchoicedouble/training_manual.html'
OUT=r'C:\vnchoicedouble\training_manual_final.pdf'
FOOTER=('<div style="width:100%;font-family:Times New Roman,Microsoft YaHei,serif;'
 'font-size:8px;color:#667;padding:0 9mm;display:flex;justify-content:space-between;">'
 '<span>CHOICE SLATS VIET NAM · Sổ tay ảnh /lite · 图文手册 · Picture Manual</span>'
 '<span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>')
with sync_playwright() as p:
    b=p.chromium.launch(args=['--ignore-certificate-errors'])
    pg=b.new_page()
    pg.goto(HTML, wait_until='load', timeout=60000)
    pg.wait_for_timeout(3000)
    imgs=pg.evaluate("[...document.images].map(i=>({s:i.getAttribute('src'),ok:i.complete&&i.naturalWidth>0}))")
    bad=[x['s'] for x in imgs if not x['ok']]
    st.append('IMAGES %d BROKEN %d %s'%(len(imgs),len(bad),bad[:3]))
    pg.emulate_media(media='print')
    pg.wait_for_timeout(800)
    pg.pdf(path=OUT, format='A4', print_background=True,
            display_header_footer=True, header_template='<div></div>', footer_template=FOOTER,
            margin={'top':'10mm','bottom':'13mm','left':'9mm','right':'9mm'})
    b.close()
st.append('PDF %d KB'%(os.path.getsize(OUT)//1024))
open(r'C:\vnchoicedouble\_pdf_status.txt','w',encoding='utf-8').write('\n'.join(st))
print('done')
