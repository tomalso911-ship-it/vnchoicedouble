from pypdf import PdfReader
out=[]
r = PdfReader(r'C:\vnchoicedouble\training_manual_final.pdf')
full = '\n'.join((p.extract_text() or '') for p in r.pages)
for kw in ['SỔ TAY ẢNH','PICTURE MANUAL','MỤC LỤC','CÁCH ĐỌC','Báo cáo ghi chép','Công việc của tôi','Tab A — Tổng quan','Đăng nhập','Sản xuất']:
    out.append('%-22s %s' % (kw, 'YES' if kw in full else 'no'))
out.append('PAGES %d' % len(r.pages))
out.append('--- page1 head ---')
out.append((r.pages[0].extract_text() or '')[:260])
open(r'C:\vnchoicedouble\_which_pdf.txt','w',encoding='utf-8').write('\n'.join(out))
print('written')
