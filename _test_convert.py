import sys, urllib.request, json
if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')
req = urllib.request.Request('http://127.0.0.1:5050/api/finance/convert-currency', data=json.dumps({"target":"USD"}).encode('utf-8'), headers={"Content-Type":"application/json"}, method='POST')
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read().decode('utf-8'))
    print('ok=', data.get('ok'))
    print('target=', data.get('target'))
    sheets = list(data.get('values', {}).keys())
    print('sheet_count=', len(sheets), 'names=', sheets)
    for s in sheets:
        rows = data['values'][s]
        first = next(iter(rows.items()))
        print('sheet', s, 'row_count', len(rows), 'first row', first)
except Exception as e:
    print('ERR', e)
