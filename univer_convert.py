"""
Univer 0.5.5 快照 <-> xlsx 双向转换（纯 Python / openpyxl）。
前端用 Univer OSS 编辑，xlsx 导入导出在本模块完成，后端落盘，规避 Pro 授权。

单元格/工作簿字段严格按 @univerjs/core@0.5.5 的 ICellData / IWorksheetData /
IWorkbookData / IStyleData / CellValueType 等类型定义。
"""
import openpyxl
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.styles.numbers import is_date_format
from openpyxl.utils.datetime import to_excel
import datetime
import sys

# ---- Univer 枚举数值（来自 @univerjs/core 源码）----
CVT_STRING, CVT_NUMBER, CVT_BOOLEAN, CVT_FORCE_STRING = 1, 2, 3, 4
BN_FALSE, BN_TRUE = 0, 1
HT_UNSPEC, HT_LEFT, HT_CENTER, HT_RIGHT = 0, 1, 2, 3
VT_UNSPEC, VT_TOP, VT_MIDDLE, VT_BOTTOM = 0, 1, 2, 3
TB_UNSPEC, TB_OVERFLOW, TB_CLIP, TB_WRAP = 0, 1, 2, 3
# BorderStyleTypes
BORDER_MAP = {
    'thin': 1, 'hair': 2, 'dotted': 3, 'dashed': 4, 'dashDot': 6,
    'dashDotDot': 7, 'double': 8, 'medium': 9, 'mediumDashed': 10,
    'mediumDashDot': 11, 'mediumDashDotDot': 12, 'slantDashDot': 14, 'thick': 13,
}
BORDER_REV = {v: k for k, v in BORDER_MAP.items()}
TEXTDEC_SINGLE = 11  # TextDecoration.SINGLE

APP_VERSION = '0.5.5'


def _rgb(s):
    """openpyxl 颜色 'FFF4CCCC'(ARGB) -> Univer '#F4CCCC'(RGB)。"""
    if not isinstance(s, str):
        return None
    s = s.strip()
    if s.startswith('FF') and len(s) == 8:
        s = s[2:]
    if len(s) == 6:
        return '#' + s
    return None


def _xlsx_border_side(side):
    if side is None or not getattr(side, 'style', None):
        return None
    style = BORDER_MAP.get(side.style, 1)
    cl = _rgb(getattr(getattr(side, 'color', None), 'rgb', None))
    return {'s': style, 'cl': ({'rgb': cl} if cl else {})}


def xlsx_to_univer(path, snap_id='vn-report'):
    """读取 xlsx 文件，返回 Univer IWorkbookData 字典。
    ★snap_id：Univer 工作簿 id（越南报表用默认 'vn-report'；中国报表传 'cn-report'，
      两张报表各自一个单元，切标签时互不串台）。默认值不变 → 越南那条链路完全不受影响。"""
    wb = openpyxl.load_workbook(path, data_only=False, read_only=False)
    sheet_order = []
    sheets = {}
    styles = {}
    for ws in wb.worksheets:
        sid = 'sheet_%d' % (len(sheet_order) + 1)
        sheet_order.append(sid)
        cell_data = {}
        max_r_used = 0
        max_c_used = 0
        for (r, c), cell in ws._cells.items():
            v = cell.value
            f = None
            t = None
            if isinstance(v, str) and v.startswith('='):
                f = v
                v = None
            elif v == '':
                v = None
            elif isinstance(v, (datetime.datetime, datetime.date)) and not isinstance(v, datetime.time):
                # Excel 日期 → 序列号 + 数字格式，Web 端会按原样显示日期，而不是 GMT 长字符串
                nf = getattr(cell, 'number_format', 'General') or 'General'
                if is_date_format(nf):
                    v = to_excel(v, wb.excel_base_date)
                    t = CVT_NUMBER
                else:
                    v = v.strftime('%m/%d/%Y')
                    t = CVT_STRING
            style = _cell_style(cell)
            cd = {}
            if v is not None:
                cd['v'] = v
                if t is None:
                    if isinstance(v, bool):
                        t = CVT_BOOLEAN
                    elif isinstance(v, (int, float)):
                        t = CVT_NUMBER
                    else:
                        t = CVT_STRING
                if t is not None:
                    cd['t'] = t
            if f is not None:
                cd['f'] = f
            if style:
                cd['s'] = style
            if cd:
                cell_data.setdefault(str(r - 1), {})[str(c - 1)] = cd
                if (v is not None) or (f is not None):
                    if r > max_r_used:
                        max_r_used = r
                    if c > max_c_used:
                        max_c_used = c
        # 合并单元格
        merge_data = []
        for mr in ws.merged_cells.ranges:
            merge_data.append({
                'startRow': mr.min_row - 1,
                'startColumn': mr.min_col - 1,
                'endRow': mr.max_row - 1,
                'endColumn': mr.max_col - 1,
            })
        # 列宽 / 行高
        column_data = {}
        for col_idx, dim in ws.column_dimensions.items():
            if getattr(dim, 'width', None):
                ci = openpyxl.utils.column_index_from_string(col_idx) - 1
                column_data[str(ci)] = {'w': max(40, int(dim.width * 7))}
        row_data = {}
        for row_idx, dim in ws.row_dimensions.items():
            if getattr(dim, 'height', None):
                # 单位换算：Excel 行高是「磅」(pt)，而 Univer 的 IRowData.h 是「像素」(px)。
                # 列宽上面已做 字符->像素 换算，行高此前漏了这一步，导致所有行矮 1/4，
                # 自动换行的文字装不下 → 溢出到下一行、压住网格线（2026-10-10 用户反馈
                # 「这里没有网格线」）。pt->px 用 ×96/72 = ×4/3，并保证不低于默认行高。
                row_data[str(row_idx - 1)] = {'h': max(24, int(round(dim.height * 96.0 / 72.0)))}
        sheets[sid] = {
            'id': sid,
            'name': ws.title,
            'tabColor': '',
            'hidden': BN_FALSE,
            'freeze': {'xSplit': 0, 'ySplit': 0},
            # ★EQ-GRID-20261016（用户要求）：空白表默认给 Z 列(26) × 50 行的可用网格，
            #   否则空种子 max_row/max_column=1 → 前端只显示 A1，无法录入。
            'rowCount': (max_r_used + 20) if max_r_used else max(int(ws.max_row or 0), 50),
            'columnCount': (max_c_used + 8) if max_c_used else max(min(int(ws.max_column or 0), 100), 26),
            'defaultColumnWidth': 72,
            'defaultRowHeight': 24,
            'mergeData': merge_data,
            'cellData': cell_data,
            'columnData': column_data,
            'rowData': row_data,
        }
    snapshot = {
        'id': snap_id,
        'name': snap_id,
        'appVersion': APP_VERSION,
        'locale': 'enUS',
        'styles': styles,
        'sheetOrder': sheet_order,
        'sheets': sheets,
        'defaultStyle': {},
    }
    return snapshot


def _cell_style(cell):
    s = {}
    font = cell.font
    if getattr(font, 'bold', None):
        s['bl'] = BN_TRUE
    if getattr(font, 'italic', None):
        s['it'] = BN_TRUE
    if getattr(font, 'sz', None):
        try:
            s['fs'] = int(font.sz)
        except Exception:
            pass
    if getattr(font, 'name', None):
        s['ff'] = font.name
    cl = _rgb(getattr(font.color, 'rgb', None)) if getattr(font, 'color', None) else None
    if cl:
        s['cl'] = {'rgb': cl}
    fill = cell.fill
    if fill and getattr(fill, 'patternType', None) and fill.patternType != 'none':
        bg = _rgb(getattr(getattr(fill, 'fgColor', None), 'rgb', None))
        if bg:
            s['bg'] = {'rgb': bg}
    bd = {}
    for side_name, key in (('left', 'l'), ('right', 'r'), ('top', 't'), ('bottom', 'b')):
        bs = _xlsx_border_side(getattr(cell.border, side_name, None))
        if bs:
            bd[key] = bs
    if bd:
        s['bd'] = bd
    al = cell.alignment
    if al:
        h = getattr(al, 'horizontal', None)
        if h == 'left':
            s['ht'] = HT_LEFT
        elif h == 'center':
            s['ht'] = HT_CENTER
        elif h == 'right':
            s['ht'] = HT_RIGHT
        vt = getattr(al, 'vertical', None)
        if vt == 'top':
            s['vt'] = VT_TOP
        elif vt == 'center' or vt == 'centerContinuous':
            s['vt'] = VT_MIDDLE
        elif vt == 'bottom':
            s['vt'] = VT_BOTTOM
        if getattr(al, 'wrap_text', None):
            s['tb'] = TB_WRAP
    nf = getattr(cell, 'number_format', None)
    if nf and nf != 'General':
        s['n'] = {'pattern': nf}
    return s if s else None


def _warn(msg):
    sys.stderr.write('[univer_convert.warn] ' + str(msg) + '\n')


def _safe_value(v):
    """Univer 编辑后可能产生 dict/list；openpyxl 只接受标量。"""
    if v is None:
        return None
    if isinstance(v, (str, int, float, bool)):
        return v
    if isinstance(v, (dict, list)):
        return str(v)
    return v


def univer_to_xlsx(snapshot, out_path):
    """把 Univer IWorkbookData 写回 xlsx。"""
    wb = openpyxl.Workbook()
    # 删除默认空表，后面按 sheetOrder 重建
    default = wb.active
    wb.remove(default)
    order = snapshot.get('sheetOrder', []) or list(snapshot.get('sheets', {}).keys())
    warnings = []
    for sid in order:
        sh = snapshot['sheets'].get(sid)
        if sh is None:
            continue
        ws = wb.create_sheet(title=sh.get('name', sid))
        cell_data = sh.get('cellData', {}) or {}
        for rk, row in cell_data.items():
            try:
                r = int(rk) + 1
            except Exception:
                warnings.append('bad row key %s in %s' % (rk, sid))
                continue
            for ck, cd in row.items():
                try:
                    c = int(ck) + 1
                except Exception:
                    warnings.append('bad col key %s in %s' % (ck, sid))
                    continue
                cell = ws.cell(row=r, column=c)
                f = cd.get('f')
                v = cd.get('v')
                try:
                    if f is not None:
                        fstr = str(f)
                        cell.value = fstr if fstr.startswith('=') else ('=' + fstr)
                    elif v is not None:
                        cell.value = _safe_value(v)
                except Exception as e:
                    warnings.append('cell (%s,%s) value error: %s' % (rk, ck, e))
                st = cd.get('s')
                # Univer 运行时写过样式后，cell.s 会变成「样式 id 字符串」（handleStyle → styles.setValue），
                # 真正的样式在快照的 styles 映射里。这里先还原成内联样式对象，否则整格样式（
                # 黑色边框/数字格式）都会被丢掉。~2026-10-10 修复「日期列边框消失」的根因。
                if isinstance(st, str):
                    st = (snapshot.get('styles') or {}).get(st)
                if st:
                    try:
                        _apply_style(cell, st)
                    except Exception as e:
                        warnings.append('cell (%s,%s) style error: %s' % (rk, ck, e))
        for mr in sh.get('mergeData', []) or []:
            try:
                ws.merge_cells(
                    start_row=mr['startRow'] + 1,
                    start_column=mr['startColumn'] + 1,
                    end_row=mr['endRow'] + 1,
                    end_column=mr['endColumn'] + 1,
                )
            except Exception as e:
                warnings.append('merge %s error: %s' % (mr, e))
        col_data = sh.get('columnData', {}) or {}
        for ck, cd in col_data.items():
            try:
                w = cd.get('w')
                if w:
                    ws.column_dimensions[get_column_letter(int(ck) + 1)].width = max(1, w / 7.0)
            except Exception as e:
                warnings.append('col %s width error: %s' % (ck, e))
        row_data = sh.get('rowData', {}) or {}
        for rk, rd in row_data.items():
            try:
                h = rd.get('h')
                if h:
                    # 反向换算：Univer 像素 -> Excel 磅（必须与 xlsx_to_univer 的 ×4/3 配对，
                    # 否则每存一次盘行高就被放大/缩小 1/3）。
                    ws.row_dimensions[int(rk) + 1].height = round(float(h) * 72.0 / 96.0, 2)
            except Exception as e:
                warnings.append('row %s height error: %s' % (rk, e))
    try:
        wb.save(out_path)
    except Exception as e:
        raise RuntimeError('openpyxl save failed: %s' % e)
    if warnings:
        for w in warnings[:20]:
            _warn(w)
        if len(warnings) > 20:
            _warn('... and %d more warnings' % (len(warnings) - 20))


def _apply_style(cell, st):
    font_args = {}
    if st.get('bl') == BN_TRUE:
        font_args['bold'] = True
    if st.get('it') == BN_TRUE:
        font_args['italic'] = True
    if st.get('fs'):
        font_args['sz'] = st['fs']
    if st.get('ff'):
        font_args['name'] = st['ff']
    cl = st.get('cl', {})
    if isinstance(cl, dict) and cl.get('rgb'):
        rgb = cl['rgb'].lstrip('#')
        if len(rgb) == 6:
            rgb = 'FF' + rgb
        font_args['color'] = rgb
    if font_args:
        cell.font = Font(**font_args)
    bg = st.get('bg', {})
    if isinstance(bg, dict) and bg.get('rgb'):
        rgb = bg['rgb'].lstrip('#')
        if len(rgb) == 6:
            rgb = 'FF' + rgb
        cell.fill = PatternFill(start_color=rgb, end_color=rgb, fill_type='solid')
    bd = st.get('bd')
    if isinstance(bd, dict):
        sides = {}
        for key, sn in (('l', 'left'), ('r', 'right'), ('t', 'top'), ('b', 'bottom')):
            bs = bd.get(key)
            if bs and bs.get('s'):
                style_name = BORDER_REV.get(bs['s'], 'thin')
                clr = bs.get('cl', {})
                crgb = (clr.get('rgb') if isinstance(clr, dict) else None)
                if crgb:
                    crgb = crgb.lstrip('#')
                    if len(crgb) == 6:
                        crgb = 'FF' + crgb
                sides[sn] = Side(style=style_name, color=crgb)
        if sides:
            cell.border = Border(**sides)
    al_args = {}
    ht = st.get('ht')
    if ht == HT_LEFT:
        al_args['horizontal'] = 'left'
    elif ht == HT_CENTER:
        al_args['horizontal'] = 'center'
    elif ht == HT_RIGHT:
        al_args['horizontal'] = 'right'
    vt = st.get('vt')
    if vt == VT_TOP:
        al_args['vertical'] = 'top'
    elif vt == VT_MIDDLE:
        al_args['vertical'] = 'center'
    elif vt == VT_BOTTOM:
        al_args['vertical'] = 'bottom'
    if st.get('tb') == TB_WRAP:
        al_args['wrap_text'] = True
    if al_args:
        cell.alignment = Alignment(**al_args)
    nf = st.get('n')
    if isinstance(nf, dict) and nf.get('pattern'):
        cell.number_format = nf['pattern']


if __name__ == '__main__':
    import sys, json
    src = sys.argv[1] if len(sys.argv) > 1 else r'c:\vnchoicedouble\finance_data\vn_report.xlsx'
    snap = xlsx_to_univer(src)
    print('sheets:', snap['sheetOrder'])
    for sid, sh in snap['sheets'].items():
        print(' ', sid, sh['name'], 'rows', sh['rowCount'], 'cols', sh['columnCount'],
              'cells', sum(len(r) for r in sh['cellData'].values()), 'merges', len(sh['mergeData']))
    # 抽样公式
    cnt = 0
    for sid, sh in snap['sheets'].items():
        for rk, row in sh['cellData'].items():
            for ck, cd in row.items():
                if cd.get('f'):
                    print('  FORMULA', sh['name'], rk, ck, cd['f'], '| v=', cd.get('v'))
                    cnt += 1
                    if cnt >= 8:
                        break
            if cnt >= 8:
                break
        if cnt >= 8:
            break
