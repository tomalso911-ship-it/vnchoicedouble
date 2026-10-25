import io

try:
    from pypdf import PdfReader
except Exception:
    from PyPDF2 import PdfReader

r = PdfReader('training_manual.pdf')
n = len(r.pages)
out = ['PAGES %d' % n]

all_text = []
for i, pg in enumerate(r.pages):
    try:
        all_text.append(pg.extract_text() or '')
    except Exception:
        all_text.append('')
blob = '\n'.join(all_text)

for kw in ['Nhật ký', '工作日志', 'Work Log', 'Mua hàng', '采购', 'Procurement',
           'Báo cáo ghi chép', '每日记录报告', 'Daily Record Report',
           'Công việc của tôi', '我的工作', 'My Work',
           'Tỉ lệ lắp', '安装率', 'Install rate', 'Trang']:
    out.append('%-24s %s' % (kw, 'YES' if kw in blob else 'NO'))

out.append('---- page5 sample ----')
out.append(all_text[5][:700] if len(all_text) > 5 else 'n/a')
out.append('---- page20 sample ----')
out.append(all_text[19][:700] if len(all_text) > 19 else 'n/a')

io.open('_chk_pdf.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('done', n)
