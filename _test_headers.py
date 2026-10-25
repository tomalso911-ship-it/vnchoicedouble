import sys, openpyxl
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
wb = openpyxl.load_workbook('finance_data/vn_report.xlsx', data_only=True)

def norm(v):
    if not v:
        return ""
    s = str(v).lower()
    for a, b in (("à","a"),("á","a"),("ạ","a"),("ả","a"),("ã","a"),("ă","a"),("ắ","a"),("ằ","a"),("ẳ","a"),("ẵ","a"),("ặ","a"),("â","a"),("ấ","a"),("ầ","a"),("ẩ","a"),("ẫ","a"),("ậ","a"),
                 ("đ","d"),("é","e"),("è","e"),("ẻ","e"),("ẽ","e"),("ẹ","e"),("ê","e"),("ế","e"),("ề","e"),("ể","e"),("ễ","e"),("ệ","e"),
                 ("í","i"),("ì","i"),("ỉ","i"),("ĩ","i"),("ị","i"),
                 ("ó","o"),("ò","o"),("ỏ","o"),("õ","o"),("ọ","o"),("ô","o"),("ố","o"),("ồ","o"),("ổ","o"),("ỗ","o"),("ộ","o"),("ơ","o"),("ớ","o"),("ờ","o"),("ở","o"),("ỡ","o"),("ợ","o"),
                 ("ú","u"),("ù","u"),("ủ","u"),("ũ","u"),("ụ","u"),("ư","u"),("ứ","u"),("ừ","u"),("ử","u"),("ữ","u"),("ự","u"),
                 ("ý","y"),("ỳ","y"),("ỷ","y"),("ỹ","y"),("ỵ","y")):
        s = s.replace(a, b)
    return s

for ws in wb.worksheets:
    print('---', ws.title, 'max_row=', ws.max_row, 'max_col=', ws.max_column)
    found_header = None
    for r in range(1, min(ws.max_row, 20) + 1):
        found = {}
        for c in range(1, min(ws.max_column, 15) + 1):
            h = norm(ws.cell(r, c).value)
            if "ngay" in h or "date" in h or "hach toan" in h:
                found["date"] = c
            if "thu" in h:
                found["thu"] = c
            if "chi" in h:
                found["chi"] = c
            if "ton" in h or "con" in h or "lai" in h:
                found["ton"] = c
        if "thu" in found or "chi" in found:
            found_header = r
            print('FOUND header row', r, 'date=', found.get('date'), 'amount=', [found.get(k) for k in ('thu','chi','ton')])
            break
    if not found_header:
        print('NO header found')

