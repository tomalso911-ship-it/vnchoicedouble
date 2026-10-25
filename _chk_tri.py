# -*- coding: utf-8 -*-
import sys, openpyxl
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
wb=openpyxl.load_workbook('finance_data/vn_report.xlsx', data_only=True)
for name in ['TỔNG HỢP','Chi tiết thu-chi']:
    ws=wb[name]
    print('===== sheet', name, 'max_col=', ws.max_column)
    for r in range(1, 10):
        row=[]
        for c in range(1, min(ws.max_column, 32)+1):
            v=ws.cell(r,c).value
            if v is None: continue
            row.append('%s%d=%r' % (openpyxl.utils.get_column_letter(c), r, str(v)[:26]))
        if row: print(' ', ' | '.join(row))
