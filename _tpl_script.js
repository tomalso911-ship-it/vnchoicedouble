
/* ============================ 国际化（i18n） ============================ */
var GANTT_I18N = {
  zh: {
    g_title:'房舍水泥板安装排程', g_sub:'分区 · 房舍 · 小组产能驱动 · 自动生成甘特',
    g_params:'排程参数', g_params_tip:'改完点「重新排程」',
    g_lbl_cap:'日安装(片/组/天)', g_lbl_start:'预计安装日期', g_lbl_cal:'工作日历',
    g_lbl_contract:'合同签订日期', g_lbl_prep:'建厂筹备至试运营', g_lbl_prep_end:'试运营结束（开始生产）', g_lbl_prod_start:'开始生产日期', g_lbl_install_end:'安装结束日', g_lbl_due:'项目交期', g_lbl_install_days:'总安装天数',
    g_cal_natural:'自然日（天天作业）', g_cal_week:'跳过周六日', g_cal_work:'周末+停工日',
    g_lbl_strat:'区内房舍分配', g_strat_lpt:'大栋优先（LPT）', g_strat_greedy:'按清单顺序，谁空谁接',
    g_lbl_zmode:'区与区之间', g_zmode_parallel:'同时开工', g_zmode_serial:'串行（前区完工才开下一区）',
    g_lbl_view:'甘特行视图', g_view_house:'按房舍（每栋一行）', g_view_team:'按小组泳道',
    g_lbl_color:'配色依据', g_color_zone:'按分区', g_color_team:'按小组',
    g_btn_recompute:'重新排程', g_btn_baseline:'设为基线', g_btn_clearbase:'清除基线',
    g_btn_displaycfg:'⚙ 显示设置',
    g_cfg_title:'显示设置', g_cfg_visual:'可视化',
    g_cfg_weekend:'周末底色', g_cfg_today:'今日基准线', g_cfg_grid:'网格线', g_cfg_deps:'依赖连线', g_cfg_base:'基线对比条',
    g_cfg_granularity:'时间粒度', g_gran_day:'日', g_gran_week:'周', g_gran_month:'月',
    g_cfg_datesep:'日期分隔', g_cfg_colwidth:'列宽', g_cfg_rowheight:'列高', g_cfg_color:'配色',
    g_cfg_fields:'数据字段', g_btn_colfit:'列宽自适应', g_btn_colreset:'恢复默认',
    g_cfg_hint:'勾选数据字段可显示/隐藏左侧列；拖表头右边缘调宽，双击自适应',
    g_lbl_hol:'停工日 / 节假日（每行一个，支持 2026-10-01 或 01/10/2026）',
    g_houses:'房舍清单', g_houses_tip:'来源：现有数据源 / 粘贴 / 文件',
    g_btn_imp:'粘贴 / 导入数据', g_btn_sample:'载入示例', g_btn_add:'+ 新增房舍', g_btn_csv:'导出 CSV',
    g_hint_edit:'直接改下表里的「板数 / 已装 / 小组」即可；改完自动重排',
    g_imp_ph:'从 Excel 直接复制粘贴（自动识别制表符/逗号），或粘贴 CSV / JSON\n\n示例：\n区\t房舍\t水泥板数\t已装\nA区\t1号舍\t2400\t600\nA区\t2号舍\t1800\t0',
    g_col_zone:'区', g_col_name:'房舍', g_col_panels:'水泥板', g_col_done:'已装', g_col_prog:'进度%', g_col_days:'天数', g_col_team:'小组', g_col_start:'预计安装日期', g_col_end:'安装结束',
    g_hdr:'首行为表头', g_btn_parse:'解析并替换', g_btn_cancel:'取消',
    g_splitter_title:'拖动调整宽度 · 双击适应列宽',
    g_zone_sum_h2:'分区汇总', g_load:'小组负载', g_load_tip:'利用率 = 作业天数 ÷ 该组占用跨度',
    g_zone_summary:'（区汇总）', g_finish:' 完工',
    g_collapse:'收起详细栋舍', g_expand:'展开详细栋舍',
    g_col_resize_tip:'拖右边缘调宽，双击自适应',
    g_unit_group:'组', g_idle:'空闲', g_unit_pcs:'片', g_unit_day:'天', g_kpi_done:'已装', g_lbl_remaining:'剩', g_locked_tip:'开工日已锁定',
    g_load_dong:'栋', g_overlap_with:' 与 ', g_time_overlap:'时间重叠', g_not_scheduled:'未排上期',
    g_load_first:'首栋', g_load_last:'末栋', g_load_idle_warn:'空档较多，可考虑减组或调序',
    g_load_workday:'个工作日', g_load_util:'利用率',
    g_check_title:'排程校验',
    g_legend_team:'按小组着色', g_legend_idle:'小组空档', g_legend_base:'基线计划', g_legend_milestone:'区完工里程碑',
    g_legend_lock:'🔒 = 开工日已锁定（手工指定，排程不再自动挪动）',
    g_imp_empty:'请先粘贴数据或选择文件', g_imp_json_err:'JSON 解析失败：', g_imp_nodata:'未识别到数据',
    g_col_n:'列', g_unzoned:'未分区', g_bld_fmt:'房舍{n}',
    g_imp_norow:'没有解析出有效行（板数列必须是数字）', g_imp_ok:'已导入 <b>{n}</b> 栋房舍', g_imp_skip:'{n} 行板数无效已跳过',
    g_auto:'自动', g_csv_name:'房舍安装排程', g_imp_none:'— 无 —', g_ro_auto:'自动生成，不可编辑',
    g_cards_toggle_title:'展开/收起（区汇总 + 小组负载）',
    g_btn_excel:'打印EXCEL', g_btn_pdf:'打印PDF',
    g_zt_zone:'分区', g_zt_team:'安装小组', g_zt_count:'房舍数', g_zt_panels:'总板数', g_zt_done:'已装',
    g_zt_start:'预计安装日期', g_zt_end:'完工', g_zt_days:'工期(天)', g_zt_ideal:'理论最少天数', g_zt_util:'利用率',
    g_ph_follow:'跟随项目', g_zone_start_tip:'留空=自动顺延（首区=项目开工日，其后各区=前一区完工日+1）',
    g_kpi_zone:'分区', g_kpi_houses:'房舍', g_kpi_panels:'总板数', g_kpi_cap:'产能', g_kpi_teams:'安装小组',
    g_kpi_range:'项目区间', g_kpi_days:'总工期', g_kpi_latezone:'最晚完工区', g_kpi_util:'小组平均利用率',
    g_kpi_empty:'暂无数据', g_empty_houses:'暂无房舍，点上方「载入示例」或「粘贴/导入数据」',
    g_team_fmt:'第{n}组', g_allgroup:'全部组', g_year:'年', g_month:'月'
  },
  en: {
    g_title:'Installation Scheduling', g_sub:'Zones · Houses · Team-capacity driven · Auto Gantt',
    g_params:'Schedule Parameters', g_params_tip:'Click "Recompute" after changes',
    g_lbl_cap:'Daily install (pcs/team/day)', g_lbl_start:'Expected install date', g_lbl_cal:'Work calendar',
    g_lbl_contract:'Contract date', g_lbl_prep:'Factory prep & trial run', g_lbl_prep_end:'Trial run end (prod start)', g_lbl_prod_start:'Production start date', g_lbl_install_end:'Installation end', g_lbl_due:'Project due date', g_lbl_install_days:'Total install days',
    g_cal_natural:'Natural days (work daily)', g_cal_week:'Skip Sat & Sun', g_cal_work:'Weekends + off-days',
    g_lbl_strat:'House assignment in zone', g_strat_lpt:'Largest first (LPT)', g_strat_greedy:'By list order, first free',
    g_lbl_zmode:'Between zones', g_zmode_parallel:'Parallel', g_zmode_serial:'Serial (next after prev)',
    g_lbl_view:'Gantt row view', g_view_house:'By house (one row each)', g_view_team:'By team lane',
    g_lbl_color:'Color by', g_color_zone:'By zone', g_color_team:'By team',
    g_btn_recompute:'Recompute', g_btn_baseline:'Set baseline', g_btn_clearbase:'Clear baseline',
    g_btn_displaycfg:'⚙ Display settings',
    g_cfg_title:'Display Settings', g_cfg_visual:'Visualization',
    g_cfg_weekend:'Weekend shading', g_cfg_today:'Today line', g_cfg_grid:'Grid lines', g_cfg_deps:'Dependency arrows', g_cfg_base:'Baseline bars',
    g_cfg_granularity:'Time unit', g_gran_day:'Day', g_gran_week:'Week', g_gran_month:'Month',
    g_cfg_datesep:'Date separator', g_cfg_colwidth:'Column width', g_cfg_rowheight:'Row height', g_cfg_color:'Color by',
    g_cfg_fields:'Data fields', g_btn_colfit:'Fit columns', g_btn_colreset:'Reset',
    g_cfg_hint:'Tick data fields to show/hide left columns; drag header right edge to resize, double-click to fit',
    g_lbl_hol:'Off-days / Holidays (one per line; 2026-10-01 or 01/10/2026)',
    g_houses:'House List', g_houses_tip:'Source: data source / paste / file',
    g_btn_imp:'Paste / Import', g_btn_sample:'Load sample', g_btn_add:'+ Add house', g_btn_csv:'Export CSV',
    g_hint_edit:'Edit panels / done / team below; auto-reschedule',
    g_imp_ph:'Copy-paste from Excel (auto-detect tab/comma), or paste CSV / JSON\n\nExample:\nzone\thouse\tpanels\tdone\nA\t1\t2400\t600\nA\t2\t1800\t0',
    g_col_zone:'Zone', g_col_name:'House', g_col_panels:'Panels', g_col_done:'Done', g_col_prog:'Progress%', g_col_days:'Days', g_col_team:'Team', g_col_start:'Expected install', g_col_end:'Install end',
    g_hdr:'First row is header', g_btn_parse:'Parse & replace', g_btn_cancel:'Cancel',
    g_splitter_title:'Drag to resize · double-click to fit',
    g_zone_sum_h2:'Zone Summary', g_load:'Team Load', g_load_tip:'Utilization = workdays ÷ team span',
    g_zone_summary:'(zone summary)', g_finish:' done',
    g_collapse:'Collapse houses', g_expand:'Expand houses',
    g_col_resize_tip:'Drag right edge to resize, double-click to fit',
    g_unit_group:' teams', g_idle:'idle', g_unit_pcs:'pcs', g_unit_day:'days', g_kpi_done:'Installed', g_lbl_remaining:'left', g_locked_tip:'Start date locked',
    g_load_dong:' bldg', g_overlap_with:' and ', g_time_overlap:'time overlap', g_not_scheduled:'not scheduled',
    g_load_first:'First', g_load_last:'Last', g_load_idle_warn:'Large idle gap; consider fewer teams or reorder',
    g_load_workday:' workdays', g_load_util:'Utilization',
    g_check_title:'Schedule check',
    g_legend_team:'Colored by team', g_legend_idle:'Team idle', g_legend_base:'Baseline', g_legend_milestone:'Zone-done milestone',
    g_legend_lock:'🔒 = Start locked (manual; schedule will not auto-move)',
    g_imp_empty:'Paste data or pick a file', g_imp_json_err:'JSON parse failed: ', g_imp_nodata:'No data recognized',
    g_col_n:'col', g_unzoned:'Unzoned', g_bld_fmt:'House {n}',
    g_imp_norow:'No valid rows (panels must be numeric)', g_imp_ok:'Imported <b>{n}</b> houses', g_imp_skip:'{n} rows skipped (invalid panels)',
    g_auto:'Auto', g_csv_name:'House install schedule', g_imp_none:'— none —', g_ro_auto:'Auto-generated, read-only',
    g_cards_toggle_title:'Expand/Collapse (Zone Summary + Team Load)',
    g_btn_excel:'Print Excel', g_btn_pdf:'Print PDF',
    g_zt_zone:'Zone', g_zt_team:'Install team', g_zt_count:'Houses', g_zt_panels:'Total panels', g_zt_done:'Done',
    g_zt_start:'Expected install date', g_zt_end:'Done', g_zt_days:'Duration (days)', g_zt_ideal:'Min ideal days', g_zt_util:'Utilization',
    g_ph_follow:'Follow project', g_zone_start_tip:'Leave empty = auto: 1st zone = project start, later zones = prev zone end +1',
    g_kpi_zone:'Zones', g_kpi_houses:'Houses', g_kpi_panels:'Total panels', g_kpi_cap:'Capacity', g_kpi_teams:'Install teams',
    g_kpi_range:'Project span', g_kpi_days:'Total duration', g_kpi_latezone:'Latest zone', g_kpi_util:'Avg team utilization',
    g_kpi_empty:'No data', g_empty_houses:'No houses yet; click "Load sample" or "Paste / Import" above',
    g_team_fmt:'Team {n}', g_allgroup:'All groups', g_year:'', g_month:''
  },
  vi: {
    g_title:'Lập lịch lắp đặt tấm xi măng', g_sub:'Phân vùng · Chuồng · Theo năng suất đội · Tự động Gantt',
    g_params:'Tham số lịch', g_params_tip:'Nhấn "Tính lại" sau khi đổi',
    g_lbl_cap:'Lắp/ngày (viên/đội/ngày)', g_lbl_start:'Ngày lắp dự kiến', g_lbl_cal:'Lịch làm việc',
    g_lbl_contract:'Ngày ký hợp đồng', g_lbl_prep:'Chuẩn bị nhà máy & chạy thử', g_lbl_prep_end:'Kết thúc chạy thử (bắt đầu SX)', g_lbl_prod_start:'Ngày bắt đầu sản xuất', g_lbl_install_end:'Ngày kết thúc lắp đặt', g_lbl_due:'Ngày bàn giao dự án', g_lbl_install_days:'Tổng số ngày lắp đặt',
    g_cal_natural:'Ngày tự nhiên (làm hàng ngày)', g_cal_week:'Bỏ T7 & CN', g_cal_work:'Cuối tuần + ngày nghỉ',
    g_lbl_strat:'Phân bổ chuồng trong vùng', g_strat_lpt:'Ưu tiên lớn (LPT)', g_strat_greedy:'Theo thứ tự, đội rảnh nhận',
    g_lbl_zmode:'Giữa các vùng', g_zmode_parallel:'Cùng lúc', g_zmode_serial:'Nối tiếp (xong vùng trước mới tới sau)',
    g_lbl_view:'Kiểu hàng Gantt', g_view_house:'Theo chuồng (mỗi chuồng 1 hàng)', g_view_team:'Theo làn đội',
    g_lbl_color:'Tô màu theo', g_color_zone:'Theo vùng', g_color_team:'Theo đội',
    g_btn_recompute:'Tính lại', g_btn_baseline:'Đặt baseline', g_btn_clearbase:'Xóa baseline',
    g_btn_displaycfg:'⚙ Cài đặt hiển thị',
    g_cfg_title:'Cài đặt hiển thị', g_cfg_visual:'Trực quan',
    g_cfg_weekend:'Nền cuối tuần', g_cfg_today:'Đường hôm nay', g_cfg_grid:'Lưới', g_cfg_deps:'Mũi tên phụ thuộc', g_cfg_base:'Thanh cơ sở',
    g_cfg_granularity:'Đơn vị thời gian', g_gran_day:'Ngày', g_gran_week:'Tuần', g_gran_month:'Tháng',
    g_cfg_datesep:'Dấu cách ngày', g_cfg_colwidth:'Độ rộng cột', g_cfg_rowheight:'Chiều cao hàng', g_cfg_color:'Tô màu theo',
    g_cfg_fields:'Trường dữ liệu', g_btn_colfit:'Vừa cột', g_btn_colreset:'Khôi phục',
    g_cfg_hint:'Tick trường dữ liệu để ẩn/hiện cột trái; kéo cạnh phải tiêu đề để đổi rộng, nhấp đúp để vừa',
    g_lbl_hol:'Ngày nghỉ (mỗi dòng một; 2026-10-01 hoặc 01/10/2026)',
    g_houses:'Danh sách chuồng', g_houses_tip:'Nguồn: dữ liệu / dán / tệp',
    g_btn_imp:'Dán / Nhập', g_btn_sample:'Tải mẫu', g_btn_add:'+ Thêm chuồng', g_btn_csv:'Xuất CSV',
    g_hint_edit:'Sửa số tấm / đã lắp / đội bên dưới; tự tính lại',
    g_imp_ph:'Copy-dán từ Excel (tự nhận tab/dấu phẩy), hoặc dán CSV / JSON\n\nVí dụ:\nvùng\tchuồng\ttấm\tdã lắp\nA\t1\t2400\t600\nA\t2\t1800\t0',
    g_col_zone:'Vùng', g_col_name:'Chuồng', g_col_panels:'Tấm', g_col_done:'Đã lắp', g_col_prog:'Tiến độ%', g_col_days:'Ngày', g_col_team:'Đội', g_col_start:'Lắp dự kiến', g_col_end:'Kết thúc lắp',
    g_hdr:'Hàng đầu là tiêu đề', g_btn_parse:'Phân tích & thay', g_btn_cancel:'Hủy',
    g_splitter_title:'Kéo đổi rộng · nhấn đúp vừa cột',
    g_zone_sum_h2:'Tổng hợp vùng', g_load:'Tải đội', g_load_tip:'Tỷ lệ = ngày làm ÷ trải đội',
    g_zone_summary:'(tổng vùng)', g_finish:' hoàn thành',
    g_collapse:'Thu gọn các tòa', g_expand:'Mở rộng các tòa',
    g_col_resize_tip:'Kéo cạnh phải đổi rộng, nhấn đúp vừa',
    g_unit_group:' đội', g_idle:'rảnh', g_unit_pcs:'viên', g_unit_day:'ngày', g_kpi_done:'Đã lắp', g_lbl_remaining:'còn', g_locked_tip:'Ngày bắt đầu đã khóa',
    g_load_dong:' chuồng', g_overlap_with:' và ', g_time_overlap:'trùng thời gian', g_not_scheduled:'chưa lên lịch',
    g_load_first:'Chuồng đầu', g_load_last:'Chuồng cuối', g_load_idle_warn:'Nhiều khoảng trống, giảm đội hoặc đổi thứ tự',
    g_load_workday:' ngày làm', g_load_util:'Tỷ lệ',
    g_check_title:'Kiểm tra lịch',
    g_legend_team:'Tô theo đội', g_legend_idle:'Khoảng trống đội', g_legend_base:'Kế hoạch cơ sở', g_legend_milestone:'Mốc hoàn thành vùng',
    g_legend_lock:'🔒 = Ngày bắt đầu đã khóa (chỉnh tay; lịch không tự dời)',
    g_imp_empty:'Dán dữ liệu hoặc chọn tệp', g_imp_json_err:'Lỗi phân tích JSON: ', g_imp_nodata:'Không nhận diện được dữ liệu',
    g_col_n:'cột', g_unzoned:'Chưa phân vùng', g_bld_fmt:'Chuồng {n}',
    g_imp_norow:'Không có dòng hợp lệ (cột tấm phải là số)', g_imp_ok:'Đã nhập <b>{n}</b> chuồng', g_imp_skip:'{n} dòng bỏ qua (tấm không hợp lệ)',
    g_auto:'Tự động', g_csv_name:'Lịch lắp đặt chuồng', g_imp_none:'— không —', g_ro_auto:'Tự động tạo, không sửa được',
    g_cards_toggle_title:'Mở rộng/Thu gọn (Tổng hợp vùng + Tải đội)',
    g_btn_excel:'In Excel', g_btn_pdf:'In PDF',
    g_zt_zone:'Vùng', g_zt_team:'Đội lắp', g_zt_count:'Số chuồng', g_zt_panels:'Tổng tấm', g_zt_done:'Đã lắp',
    g_zt_start:'Ngày lắp dự kiến', g_zt_end:'Xong', g_zt_days:'Thời gian (ngày)', g_zt_ideal:'Số ngày lý thuyết', g_zt_util:'Tỷ lệ',
    g_ph_follow:'Theo dự án', g_zone_start_tip:'Để trống = tự động: vùng đầu = ngày khởi công dự án, vùng sau = vùng trước xong +1',
    g_kpi_zone:'Vùng', g_kpi_houses:'Chuồng', g_kpi_panels:'Tổng tấm', g_kpi_cap:'Năng suất', g_kpi_teams:'Đội lắp',
    g_kpi_range:'Khoảng dự án', g_kpi_days:'Tổng thời gian', g_kpi_latezone:'Vùng xong muộn', g_kpi_util:'Tỷ lệ đội TB',
    g_kpi_empty:'Chưa có dữ liệu', g_empty_houses:'Chưa có chuồng, nhấn "Tải mẫu" hoặc "Dán / Nhập" bên trên',
    g_team_fmt:'Đội {n}', g_allgroup:'Tất cả đội', g_year:' năm', g_month:' tháng'
  }
};
function curLang(){ return (window.parent&&window.parent.CUR_LANG)?window.parent.CUR_LANG:'zh'; }
function it(k){ var l=curLang(), d=GANTT_I18N[l]; if(d&&d[k]!==undefined) return d[k]; var z=GANTT_I18N.zh[k]; return z!==undefined?z:k; }
function localize(root){ root=root||document; var i;
  var list=root.querySelectorAll('[data-i18n]'); for(i=0;i<list.length;i++){ list[i].textContent=it(list[i].getAttribute('data-i18n')); }
  var al=root.querySelectorAll('[data-i18n-ph]'); for(i=0;i<al.length;i++){ al[i].setAttribute('placeholder', it(al[i].getAttribute('data-i18n-ph'))); }
  var tl=root.querySelectorAll('[data-i18n-title]'); for(i=0;i<tl.length;i++){ tl[i].setAttribute('title', it(tl[i].getAttribute('data-i18n-title'))); }
}
/* =========================================================================
 * 0. 数据源接入点  ★★★
 *    把你的现有数据源结果赋给 HOUSE_SOURCE，再调 rebuild() 即可。
 *    要求的字段：{ zone:区名, name:房舍名, panels:水泥板数, done:已装板数(可选) }
 *    例：
 *      fetch('/api/houses').then(r=>r.json()).then(d=>{ HOUSE_SOURCE=d; rebuild(); });
 *    或在本文件末尾直接写： HOUSE_SOURCE = [...]; rebuild();
 * ======================================================================= */
var HOUSE_SOURCE = null;
var SAMPLE = [
  {zone:'A区',name:'1号舍',panels:2400,done:600},
  {zone:'A区',name:'2号舍',panels:1800,done:1800},
  {zone:'A区',name:'3号舍',panels:3000,done:0},
  {zone:'A区',name:'4号舍',panels:1200,done:0},
  {zone:'A区',name:'5号舍',panels:2000,done:0},
  {zone:'A区',name:'6号舍',panels:1600,done:0},
  {zone:'A区',name:'7号舍',panels:2800,done:0},
  {zone:'B区',name:'1号舍',panels:2200,done:2200},
  {zone:'B区',name:'2号舍',panels:1900,done:900},
  {zone:'B区',name:'3号舍',panels:2600,done:0},
  {zone:'B区',name:'4号舍',panels:1400,done:0},
  {zone:'B区',name:'5号舍',panels:2100,done:0},
  {zone:'C区',name:'1号舍',panels:3200,done:0},
  {zone:'C区',name:'2号舍',panels:1700,done:0},
  {zone:'C区',name:'3号舍',panels:2300,done:0},
  {zone:'C区',name:'4号舍',panels:1500,done:0},
  {zone:'C区',name:'5号舍',panels:2900,done:0},
  {zone:'C区',name:'6号舍',panels:1300,done:0}
];

/* =========================================================================
 * 1. 日期工具（UTC，避免时区；存储 YYYY-MM-DD，显示 DD/MM/YYYY）
 * ======================================================================= */
function pad2(n){ n=parseInt(n,10)||0; return (n<10?'0':'')+n; }
function validYmd(y){
  if(!y) return ''; var p=String(y).split('-'); if(p.length!==3) return '';
  var Y=+p[0],M=+p[1],D=+p[2];
  if(Y<1970||Y>2100||M<1||M>12||D<1||D>31) return '';
  var d=new Date(Date.UTC(Y,M-1,D));
  if(d.getUTCFullYear()!==Y||d.getUTCMonth()!==M-1||d.getUTCDate()!==D) return '';
  return p[0]+'-'+pad2(M)+'-'+pad2(D);
}
function toYmd(v){
  if(v===null||v===undefined||v==='') return '';
  if(v instanceof Date) return isNaN(v.getTime())?'':toYmd(v.getUTCFullYear()+'-'+pad2(v.getUTCMonth()+1)+'-'+pad2(v.getUTCDate()));
  var s=String(v).trim(); if(!s) return '';
  if(/^\d{10,13}$/.test(s)){ var ts=+s; if(s.length<=10) ts*=1000; return toYmd(new Date(ts)); }
  var m=s.match(/^(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})/); if(m) return validYmd(m[1]+'-'+m[2]+'-'+m[3]);
  m=s.match(/^(\d{1,2})[-/.](\d{1,2})[-/.](\d{4})/); if(m) return validYmd(m[3]+'-'+m[2]+'-'+m[1]);
  m=s.match(/^(\d{4})(\d{2})(\d{2})$/); if(m) return validYmd(m[1]+'-'+m[2]+'-'+m[3]);
  m=s.match(/^(\d{1,2})[-/.](\d{1,2})$/); if(m) return validYmd(new Date().getFullYear()+'-'+m[2]+'-'+m[1]);
  return '';
}
function dSep(){ return (cfg.dateSep==='-')?'-':'/'; }
function dmy(v){ var y=toYmd(v); if(!y) return ''; var p=y.split('-'),s=dSep(); return p[2]+s+p[1]+s+p[0]; }
function today(){ return toYmd(new Date()); }
function addDays(y,n){ y=toYmd(y); if(!y) return ''; var p=y.split('-'),d=new Date(Date.UTC(+p[0],+p[1]-1,+p[2]));
  d.setUTCDate(d.getUTCDate()+(parseInt(n,10)||0)); return toYmd(d); }
function diffDays(a,b){ a=toYmd(a);b=toYmd(b); if(!a||!b) return 0;
  return Math.round((Date.parse(b+'T00:00:00Z')-Date.parse(a+'T00:00:00Z'))/86400000); }
function dow(y){ y=toYmd(y); if(!y) return 1; var p=y.split('-');
  return new Date(Date.UTC(+p[0],+p[1]-1,+p[2])).getUTCDay(); }
function isoWeek(d){ var p=toYmd(d).split('-'); if(p.length<3) return {w:0,y:''};
  var t=new Date(Date.UTC(+p[0],+p[1]-1,+p[2])), dn=t.getUTCDay()||7;
  t.setUTCDate(t.getUTCDate()+4-dn); var y=t.getUTCFullYear();
  return {w:Math.ceil(((t.getTime()-Date.UTC(y,0,1))/86400000+1)/7),y:y}; }
function esc(s){ return String(s==null?'':s).replace(/[&<>"']/g,function(c){
  return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]; }); }
function fmtNum(n){ return Number(n||0).toLocaleString(); }
function hash(s){ var h=0;s=String(s||'');for(var i=0;i<s.length;i++) h=(h*31+s.charCodeAt(i))>>>0; return h; }
function lum(hex){ var n=parseInt(hex.slice(1),16),c=[(n>>16)&255,(n>>8)&255,n&255].map(function(v){
  v/=255; return v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4); });
  return 0.2126*c[0]+0.7152*c[1]+0.0722*c[2]; }
function fgOn(hex){ return lum(hex)>0.45?'#263238':'#fff'; }
function shade(hex,a){ var n=parseInt(hex.slice(1),16);
  var r=Math.max(0,Math.min(255,(n>>16)+a)),g=Math.max(0,Math.min(255,((n>>8)&255)+a)),b=Math.max(0,Math.min(255,(n&255)+a));
  return '#'+((1<<24)+(r<<16)+(g<<8)+b).toString(16).slice(1); }

/* =========================================================================
 * 2. 工作日历（已锁定：除越南春节外，全年无休；春节停工日由生产模块自动注入）
 * ======================================================================= */
var HOL={};
var TET={};
function isWork(d){ return !TET[d]; }
function nextWork(d){ var g=0; while(!isWork(d)&&g++<400) d=addDays(d,1); return d; }
/* 从 start 起，占用 n 个工作日，返回最后一个工作日 */
function addWork(s,n){ var d=nextWork(s), rem=Math.max(0,(n|0)-1), g=0;
  while(rem>0&&g++<4000){ d=addDays(d,1); if(isWork(d)) rem--; } return d; }
function nextAfter(e){ return nextWork(addDays(e,1)); }
/* 区间内工作日数 */
function workDaysBetween(a,b){ var n=0,d=toYmd(a),e=toYmd(b),g=0;
  while(d&&d<=e&&g++<4000){ if(isWork(d)) n++; d=addDays(d,1); } return n; }
function parseTetHolidays(){
  TET={};
  try{
    var list=(typeof window.parent!=='undefined' && window.parent.BOARD_HOLIDAYS)?window.parent.BOARD_HOLIDAYS:[];
    list.forEach(function(h){
      if(h.zh!=='春节' || !h.vn) return;
      for(var i=-7;i<=10;i++){ TET[addDays(h.from,i)]=1; }
    });
  }catch(e){}
}
function parseHolidays(){
  HOL={}; (cfg.holidays||'').split(/\n|,|;/).forEach(function(x){ var y=toYmd(x); if(y) HOL[y]=1; });
  parseTetHolidays();
}

/* =========================================================================
 * 3. 数据模型
 * ======================================================================= */
var ZONE_C=['#5c6bc0','#26a69a','#ffa726','#ef5350','#66bb6a','#ab47bc','#29b6f6','#8d6e63'];
/* 小组颜色固定：第1组蓝、第2组红、第3组深黄、第4组紫；之后循环回退色 */
var TEAM_C=['#1E88E5','#E53935','#FBC02D','#8E24AA','#43A047','#FB8C00','#00897B','#78909c'];
/* 全部组（1组+2组…并行）专属色：棕色，不与第1–4组蓝/红/黄/紫冲突 */
var ALL_C='#795548';

var houses=[];   // {id,zone,name,panels,done,days,team,start,end,lockStart,lockTeam,bs,be}
var zones=[];    // {name,teams,start}
var cfg={};
var DEF={cap:200,start:'',cal:'natural',strat:'lpt',zmode:'serial',view:'house',
  color:'team',holidays:'',dateSep:'/',tableWidth:470,colW:{},collapsed:{},
  visible:['zone','name','panels','done','prog','days','team','start','end'],
  cfgOpen:false, cardsCollapsed:false,
  showWeekend:true,
  showToday:true,showGrid:true,showDeps:true,showBase:true,viewMode:'Week',colWidth:40,barHeight:22};

var COLS=[
  {k:'zone',   w:72, n:it('g_col_zone'),     e:'text'},
  {k:'name',   w:92, n:it('g_col_name'),   e:'text'},
  {k:'panels', w:76, n:it('g_col_panels'), e:'num', align:'right'},
  {k:'done',   w:72, n:it('g_col_done'),   e:'num', align:'right'},
  {k:'prog',   w:58, n:it('g_col_prog'),  e:'ro'},
  {k:'days',   w:52, n:it('g_col_days'),   e:'ro'},
  {k:'team',   w:76, n:it('g_col_team'),   e:'team'},
  {k:'start',  w:92, n:it('g_col_start'), e:'date'},
  {k:'end',    w:92, n:it('g_col_end'),    e:'ro'}
];
var COL_MIN=40, COL_MAX=420;
function findCol(k){ var r=null; COLS.forEach(function(c){ if(c.k===k) r=c; }); return r; }
function colW(k){ var c=findCol(k); return Math.max(COL_MIN,Math.min(COL_MAX,(cfg.colW||{})[k]||(c?c.w:80))); }

function zoneOf(n){ var r=null; zones.forEach(function(z){ if(z.name===n) r=z; }); return r; }
function teamsOf(n){ var z=zoneOf(n); return z?Math.max(1,z.teams|0):1; }
function zoneColor(n){ return ZONE_C[hash(n)%8]; }
function teamColor(z,t){ var n=parseInt(t,10); if(isNaN(n)) n=0; n=((n%8)+8)%8; return TEAM_C[n]; }

function ganttStorageKey(base){
  return ((typeof GANTT_PROJECT_ID!=='undefined' && GANTT_PROJECT_ID) ? ('gantt_'+GANTT_PROJECT_ID+'_') : '') + base;
}
function loadCfg(){
  var c={}; for(var k in DEF) c[k]=DEF[k];
  var raw=null; try{ raw=localStorage.getItem(ganttStorageKey('house_sched_v1')); }catch(e){}
  if(raw){ try{ var o=JSON.parse(raw); for(var k2 in o) if(o[k2]!==undefined&&o[k2]!==null) c[k2]=o[k2]; }catch(e){} }
  /* 迁移：旧默认按分区 → 统一改为按小组着色（2026-09-30 小组配色蓝/红/深黄/紫） */
  if(c._ver===undefined||c._ver<2){ c.color='team'; c._ver=2; }
  if(!c.visible||!c.visible.length) c.visible=DEF.visible.slice();
  if(!c.start) c.start=(typeof GANTT_DEFAULT_START!=='undefined' && GANTT_DEFAULT_START) ? GANTT_DEFAULT_START : today();
  cfg=c;
}
function saveCfg(){ try{ localStorage.setItem(ganttStorageKey('house_sched_v1'),JSON.stringify(cfg)); }catch(e){} }

function loadHouses(){
  var src=HOUSE_SOURCE||SAMPLE;
  houses=(src||[]).map(function(h,i){
    var rawName=String(h.name||(it('g_bld_fmt').replace('{n}',(i+1))));
    var sp=rawName.split('#');
    var name1=sp[0]||rawName, name2=sp.slice(1).join('#');
    if(name2) name2='#'+name2;
    return {id:'H'+(i+1), zone:String(h.zone||it('g_unzoned')), name:rawName, name1:name1, name2:name2,
      panels:Math.max(0,Math.round(+h.panels||0)), done:Math.max(0,Math.round(+h.done||0)),
      days:0,team:0,start:'',end:'',lockStart:'',lockTeam:null,bothTeams:false,bs:'',be:''};
  });
  // 区表：按出现顺序，默认 2 组（可在区汇总表里改）
  var seen={}; zones=[];
  houses.forEach(function(h){ if(!seen[h.zone]){ seen[h.zone]=1; zones.push({name:h.zone,teams:2,start:''}); } });
  try{
    var raw=localStorage.getItem(ganttStorageKey('house_zones_v1'));
    if(raw){ var oz=JSON.parse(raw)||[];
      zones.forEach(function(z){ oz.forEach(function(o){ if(o.name===z.name) z.teams=Math.max(1,o.teams|0); }); }); }
  }catch(e){}
}

/* =========================================================================
 * 4. 排程核心
 *    规则：日产能固定 → 天数 = ceil(板数/产能)
 *          一组独占一栋 → 组内严格串行，本栋完成「次日」才开下一栋
 *          区内专属     → 小组只在自己区内流转
 * ======================================================================= */
function houseDays(h){ return Math.max(1,Math.ceil(h.panels/Math.max(1,cfg.cap))); }

function schedule(){
  parseHolidays();
  var projStart=nextWork(toYmd(cfg.start)||today());
  var prevEnd=null;
  zones.forEach(function(z){
    /* userStart = 用户显式指定的区开工日，优先级最高（可编辑覆盖默认值）。
       未指定时：串行模式下第 2 区起 = 前一区完工日+1；否则 = 项目开工日。
       不要把排程算出的 z.start 当用户输入，否则串行切回并行会残留旧日期 */
    var base;
    if(z.userStart) base = nextWork(toYmd(z.userStart));
    else if(cfg.zmode==='serial' && prevEnd) base = nextWork(nextAfter(prevEnd));
    else base = projStart;
    z.start = base;
    var hs=houses.filter(function(h){ return h.zone===z.name; });
    if(!hs.length){ z.end=''; z.days=0; return; }

    /* 分配顺序 */
    var order=hs.slice();
    if(cfg.strat==='lpt') order.sort(function(a,b){ return b.panels-a.panels || a.name.localeCompare(b.name,'zh'); });

    var n=Math.max(1,z.teams|0), free=[];
    for(var i=0;i<n;i++) free[i]=z.start;
    /* 默认（未手选小组）按「房舍列表顺序」第1组、第2组…交替分配，直到本区排完 */
    var rrMap={}, rrn=0;
    hs.forEach(function(h){ if(!h.bothTeams && h.lockTeam==null){ rrMap[h.id]=rrn++; } });

    order.forEach(function(h){
      /* 全部组：1组+2组…全部并行 → 产能 n×cap，且独占全部 n 个组
         开始取各组最晚空闲（含锁定开始日），完工后把全部组推进到其结束次日 */
      if(h.bothTeams){
        h.days=Math.max(1,Math.ceil(h.panels/(n*Math.max(1,cfg.cap))));
        var s=h.lockStart?nextWork(h.lockStart):nextWork(free[0]);
        for(var bi=1;bi<n;bi++){ if(free[bi]>s) s=nextWork(free[bi]); }
        var e=addWork(s,h.days);
        h.start=s; h.end=e; h.team=0;
        for(var bj=0;bj<n;bj++){ free[bj]=nextAfter(e); }
        return;
      }
      h.days=houseDays(h);
      /* 选组：锁定优先，否则选最早空闲的组（并列取组号小的）
         注意：free 里存的是 'YYYY-MM-DD' 字符串，定宽格式下字典序 == 时间序，
         不能用 free[j] < Infinity 这种写法（字符串转数字得 NaN，比较恒 false） */
      var k=0;
      if(h.lockTeam!=null&&h.lockTeam<n&&h.lockTeam>=0) k=h.lockTeam|0;
      else{ k=(rrMap[h.id]||0)%n; }
      var s=h.lockStart?nextWork(h.lockStart):nextWork(free[k]);
      var e=addWork(s,h.days);
      h.start=s; h.end=e; h.team=k;
      free[k]=nextAfter(e);
    });

    var mn='',mx='';
    hs.forEach(function(h){ if(!mn||h.start<mn) mn=h.start; if(!mx||h.end>mx) mx=h.end; });
    z.start=mn; z.end=mx; z.days=diffDays(mn,mx)+1;
    prevEnd=mx;
  });
}
/* 锁定：手改开始日 / 手选小组 */
function setLockStart(h,v){ h.lockStart=toYmd(v)||''; schedule(); renderAll(); saveCfg(); }
function setLockTeam(h,v){
  if(v==='all'){ h.bothTeams=true; h.lockTeam=null; }
  else { h.bothTeams=false; h.lockTeam=(v===''||v==null)?null:(+v|0); }
  schedule(); renderAll(); saveCfg();
}
function snapBaseline(){ houses.forEach(function(h){ h.bs=h.start; h.be=h.end; }); renderAll(); saveCfg(); }
function clearBaseline(){ houses.forEach(function(h){ h.bs=''; h.be=''; }); renderAll(); saveCfg(); }
function toggleBaseline(checked){
  cfg.showBase=!!checked;
  if(checked) snapBaseline(); else clearBaseline();
}

/* =========================================================================
 * 4.5 区折叠状态
 * ======================================================================= */
function isZoneCollapsed(zname){ return !!(cfg.collapsed||{})[zname]; }
function toggleZone(zname, ev){
  if(ev && ev.stopPropagation) ev.stopPropagation();
  cfg.collapsed=cfg.collapsed||{};
  cfg.collapsed[zname]=!cfg.collapsed[zname];
  renderAll(); saveCfg();
}
function expandAllZones(){ cfg.collapsed={}; renderAll(); saveCfg(); }
function collapseAllZones(){ cfg.collapsed={}; zones.forEach(function(z){ cfg.collapsed[z.name]=true; }); renderAll(); saveCfg(); }

/* =========================================================================
 * 5. 行模型（甘特行）
 * ======================================================================= */
var rows=[];
function buildRows(){
  rows=[];
  if(cfg.view==='team'){
    zones.forEach(function(z){
      var hs=houses.filter(function(h){ return h.zone===z.name; });
      if(!hs.length) return;
      rows.push({kind:'zone',id:'Z:'+z.name,name:z.name+it('g_zone_summary'),zone:z.name,
        start:z.start,end:z.end,days:diffDays(z.start,z.end)+1,
        panels:sum(hs,'panels'),done:sum(hs,'done')});
      if(isZoneCollapsed(z.name)) return;
      for(var t=0;t<Math.max(1,z.teams|0);t++){
        var ths=hs.filter(function(h){ return !h.bothTeams && h.team===t; }).sort(function(a,b){ return a.start<b.start?-1:(a.start>b.start?1:0); });
        rows.push({kind:'team',id:'T:'+z.name+':'+(t+1),name:z.name+' · '+teamLabel(t),zone:z.name,team:t,
          start:ths.length?ths[0].start:'',end:ths.length?ths[ths.length-1].end:'',
          panels:sum(ths,'panels'),done:sum(ths,'done'),houses:ths});
      }
      /* 全部组泳道：本区由 1组+2组…全部并行完成的房（放在各小组泳道最下方、里程碑之前） */
      var ah=hs.filter(function(h){ return h.bothTeams; }).sort(function(a,b){ return a.start<b.start?-1:(a.start>b.start?1:0); });
      if(ah.length){
        rows.push({kind:'allgroup',id:'A:'+z.name,name:z.name+' · '+it('g_allgroup'),zone:z.name,team:-1,
          start:ah[0].start,end:ah[ah.length-1].end,
          panels:sum(ah,'panels'),done:sum(ah,'done'),houses:ah});
      }
      /* 区完工里程碑 */
      rows.push({kind:'ms',id:'M:'+z.name,name:z.name+it('g_finish'),zone:z.name,start:z.end,end:z.end});
    });
  }else{
    zones.forEach(function(z){
      var hs=houses.filter(function(h){ return h.zone===z.name; });
      if(!hs.length) return;
      rows.push({kind:'zone',id:'Z:'+z.name,name:z.name+it('g_zone_summary'),zone:z.name,
        start:z.start,end:z.end,days:diffDays(z.start,z.end)+1,
        panels:sum(hs,'panels'),done:sum(hs,'done')});
      if(isZoneCollapsed(z.name)) return;
      /* 区内行序严格按「安装计划总览」小方格的实际排列（houses 输入顺序 = HOUSE_SOURCE 顺序）
         逐栋列出，不再按小组/开始时间重排，保证与安装总览次序一致。
         依赖线仅在相邻两栋同组时才连，避免跨组乱连。 */
      hs.forEach(function(h,i){
        var prev=i>0?hs[i-1]:null;
        h._prev=(prev && prev.team===h.team)?prev:null;
        rows.push({kind:'house',id:h.id,name:h.name,zone:z.name,team:h.team,house:h,
          start:h.start,end:h.end,panels:h.panels,done:h.done,days:h.days});
      });
      rows.push({kind:'ms',id:'M:'+z.name,name:z.name+it('g_finish'),zone:z.name,start:z.end,end:z.end});
    });
  }
}
function sum(arr,k){ var n=0; arr.forEach(function(x){ n+=(+x[k]||0); }); return n; }
function teamLabel(t){ return it('g_team_fmt').replace('{n}',(t+1)); }

/* =========================================================================
 * 6. 时间刻度
 * ======================================================================= */
var S=null;
function buildScale(){
  var ds=[]; rows.forEach(function(r){ if(r.start) ds.push(r.start); if(r.end) ds.push(r.end); });
  ds.push(today());
  ds=ds.filter(Boolean).sort();
  var min=ds[0]||today(), max=ds[ds.length-1]||min;
  var vm=cfg.viewMode;
  if(vm==='Day'){ min=addDays(min,-3); max=addDays(max,4); }
  else if(vm==='Week'){ min=addDays(min,-7); max=addDays(max,10); }
  else { min=addDays(min,-20); max=addDays(max,30); }
  if(vm==='Week') min=addDays(min,-((dow(min)+6)%7));
  if(vm==='Month') min=min.slice(0,8)+'01';

  var cw=cfg.colWidth, cols=[], width=0, ppd;
  if(vm==='Month'){
    var mStartX={}, cur=min, cx=0, g=0;
    while(cur<=max&&g++<400){
      var y=+cur.slice(0,4), m=+cur.slice(5,7), dim=new Date(Date.UTC(y,m,0)).getUTCDate();
      mStartX[y+'-'+pad2(m)]=cx;
      cols.push({s:cur,e:cur.slice(0,8)+pad2(dim),l1:m+it('g_month'),ym:y+'-'+pad2(m)});
      cx+=cw; cur=addDays(cur,dim);
    }
    width=cx;
    S={min:min,max:max,cols:cols,x:function(d){ d=toYmd(d); if(!d) return 0;
      var ym=d.slice(0,7); if(mStartX[ym]==null) return 0;
      return mStartX[ym]+(parseInt(d.slice(8),10)-1)*cw/new Date(Date.UTC(+d.slice(0,4),+d.slice(5,7),0)).getUTCDate(); },
       dayW:cw/30, width:Math.max(width,200)};
  }else{
    ppd = vm==='Day' ? cw : cw/7;
    var d2=min,g2=0;
    while(d2<=max&&g2++<1500){
      var end= vm==='Day'? d2 : addDays(d2,6);
      var l1= vm==='Day' ? String(parseInt(d2.slice(8),10)) : weekLabel(d2,end,cw);
      S=S||null;
      cols.push({s:d2,e:end,l1:l1,l2:'W'+isoWeek(d2).w,ym:(vm==='Day'?d2.slice(0,7):addDays(d2,3).slice(0,7))});
      d2=addDays(end,1);
    }
    width=cols.length*cw;
    S={min:min,max:max,cols:cols,x:function(d){ d=toYmd(d); if(!d) return 0; return diffDays(min,d)*ppd; },
       dayW:ppd, width:Math.max(width,200)};
  }
  var up=[],last=null;
  S.cols.forEach(function(c,i){
    var key=(cfg.viewMode==='Month')?c.ym.slice(0,4):c.ym;
    var lb=(cfg.viewMode==='Month')?key+it('g_year'):(c.ym.slice(0,4)+it('g_year')+parseInt(c.ym.slice(5),10)+it('g_month'));
    if(!last||last.key!==key){ last={key:key,w:cw,label:lb}; up.push(last); } else last.w+=cw;
  });
  S.up=up; S.rowsH=rows.length*rowH(); S.colW=cw;
  return S;
}
function weekLabel(s,e,cw){
  var sp=dSep(), sd=pad2(s.slice(8)), sm=pad2(s.slice(5,7)), ed=pad2(e.slice(8)), em=pad2(e.slice(5,7));
  if(cw>=62) return sd+sp+sm+' - '+ed+sp+em;
  if(cw>=44) return sd+sp+sm+' - '+ed+(em!==sm?(sp+em):'');
  return parseInt(sd,10)+'-'+parseInt(ed,10)+(em!==sm?(sp+parseInt(em,10)):'');
}
function rowH(){ return cfg.barHeight+10; }

/* =========================================================================
 * 7. 渲染甘特
 * ======================================================================= */
function barColorOf(r){
  if(r&&(r.kind==='allgroup'||r.bothTeams||(r.house&&r.house.bothTeams))) return ALL_C;   /* 全部组 */
  if((r.kind==='house'||r.kind==='team')&&r.team!=null) return teamColor(r.zone,r.team);
  return zoneColor(r.zone);
}
function renderChart(){
  buildScale();
  igHideBarTip();
  var inner=document.getElementById('chartInner'), rh=rowH(), bh=cfg.barHeight, h='';
  var todayX=(cfg.showToday)?(S.x(today())+S.dayW/2):-1;
  var showToday=(cfg.showToday&&todayX>=0&&todayX<=S.width);
  h+='<div class="thead">';
  h+='<div class="tu">'; S.up.forEach(function(u){
    h+='<div style="width:'+u.w+'px">'+esc(u.w>=68?u.label:u.label.replace(/^\d{4}年/,''))+'</div>'; }); h+='</div>';
  h+='<div class="tl">'; S.cols.forEach(function(c){
    var we=(cfg.viewMode==='Day'&&(dow(c.s)===0||dow(c.s)===6));
    h+='<div class="'+(we?'we':'')+'" style="width:'+S.colW+'px" title="'+esc(dmy(c.s))+'">'
      +'<span class="t1">'+esc(c.l1)+'</span><span class="t2">'+esc(c.l2||'')+'</span></div>'; }); h+='</div>'+(showToday?'<div class="today-flag" style="left:'+todayX+'px"></div>':'')+'</div>';
  h+='<div class="bd" style="height:'+S.rowsH+'px">';
  if(cfg.showWeekend&&cfg.viewMode!=='Month'){
    if(cfg.viewMode==='Day'){
      S.cols.forEach(function(c,i){ if(dow(c.s)===0||dow(c.s)===6)
        h+='<div class="wkend'+(dow(c.s)===6?' sat':'')+'" style="left:'+(i*S.colW)+'px;width:'+S.colW+'px"></div>'; });
    }else{
      S.cols.forEach(function(c){
        var sx=S.x(addDays(c.s,5)), ex=S.x(addDays(c.s,7));
        h+='<div class="wkend" style="left:'+sx+'px;width:'+(ex-sx)+'px"></div>'; });
    }
  }
  if(cfg.showGrid) S.cols.forEach(function(c,i){ h+='<div class="cl" style="left:'+(i*S.colW)+'px"></div>'; });
  if(showToday) h+='<div class="today-line" style="left:'+todayX+'px"></div>';
  /* ★ 这里【不能】闭合 .bd！
     .thead 是 sticky 但仍占 48px 文档流，.bd 从 y=48 才开始；
     条形/依赖线若放在 .bd 外面，top 会以 .ci 的 0 为基准，
     整体上移 66px 被表头遮住，表现为「左侧表格与右侧横道图错开一个表头高度」。
     必须让它们成为 .bd 的子元素（.bd 是 position:relative），top 才以行区域顶部为基准。 */

  /* 依赖连线（勾选「依赖连线」时，房舍视图 / 泳道视图都按同一套规则绘制）：
     逐条对应需求原话：
       1) 第1组结束：下面若是全部组 → 指向全部组；否则 → 下一个第1组；
       2) 第2组结束：下面若是全部组 → 指向全部组；否则 → 下一个第2组；
       3) 全部组：先汇入本组前面最近的第1组、第2组；再指向下面最近的第1组、第2组；
          若下面紧接的仍是全部组（中间没有组行），则单项指向那个全部组。
     实现：把当前视图里带「组」的行按顺序取出，用一个状态机连接。 */
  if(cfg.showDeps){
    var paths='';
    function depPath(ri, ti, cat){
      var r=rows[ri], t=rows[ti];
      if(!r||!t||!r.end||!t.start) return;
      /* 分道布线：全部组 / 第2组 / 第1组 各走不同竖向通道，线的竖向段互不重叠、不交叉 */
      var off=(cat==='all')?14:((cat==='t1')?8:2);
      var y1=ri*rh+rh/2, y2=ti*rh+rh/2;
      var x1=S.x(r.end)+S.dayW, x2=S.x(t.start);
      var cx=x1+off;
      var d='M'+x1+' '+y1+' H'+cx+' V'+y2+' H'+(x2-1);
      paths+='<path d="'+d+'" fill="none" stroke="#607d8b" stroke-width="1.5" marker-end="url(#arw)"/>';
    }
    /* 取出「组行」序列：泳道视图取 team/allgroup 行；房舍视图取每栋房舍行（按列表顺序） */
    var seq=[];
    rows.forEach(function(r,i){
      if(cfg.view==='team'){
        if(r.kind==='team') seq.push({i:i, cat:'t'+r.team});
        else if(r.kind==='allgroup') seq.push({i:i, cat:'all'});
      }else{
        if(r.kind==='house') seq.push({i:i, cat:(r.house&&r.house.bothTeams)?'all':('t'+r.team)});
      }
    });
    /* 状态机：lastTeam=各「最近未汇出的组行」；lastAll=最近的「全部组」行 */
    var lastAll=null, allUsedFor={}, lastTeam={};
    seq.forEach(function(s){
      if(s.cat==='all'){
        var had=false;
        for(var tk in lastTeam){ if(lastTeam.hasOwnProperty(tk)){ depPath(lastTeam[tk], s.i, tk); delete lastTeam[tk]; had=true; } }
        if(!had && lastAll!=null) depPath(lastAll, s.i, 'all');   /* 中间没有组行 → 单项指向新全部组 */
        lastAll=s.i; allUsedFor={};
      }else{
        if(lastAll!=null && !allUsedFor[s.cat]){ depPath(lastAll, s.i, 'all'); allUsedFor[s.cat]=1; }  /* 全部组 → 下面最近的该组 */
        else if(lastTeam[s.cat]!=null){ depPath(lastTeam[s.cat], s.i, s.cat); }                        /* 否则 → 下一个同组 */
        lastTeam[s.cat]=s.i;
      }
    });
    h+='<svg class="deps" id="depSvg" width="'+S.width+'" height="'+S.rowsH+'">'
      +'<defs><marker id="arw" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">'
      +'<path d="M0,0 L7,3.5 L0,7 Z" fill="#607d8b"/></marker></defs>'+paths+'</svg>';
  }

  /* 条 */
  rows.forEach(function(r,i){
    var top=i*rh+(rh-bh)/2;
    if(r.kind==='ms'){
      var sz=Math.round(bh*0.8), col=zoneColor(r.zone);
      h+='<div class="bar ms" data-id="'+esc(r.id)+'" style="left:'+Math.round(S.x(r.start)+S.dayW/2-sz/2)
        +'px;top:'+Math.round(top+(bh-sz)/2)+'px;width:'+sz+'px;height:'+sz+'px;background-color:'+col+'"'
        +' data-tip="'+esc(r.name+' · '+dmy(r.start))+'" onmouseenter="igShowBarTip(event,this)" onmouseleave="igHideBarTip()"></div>';
      return;
    }
    if(r.kind==='zone'){
      var x=S.x(r.start), w=Math.max(S.x(addDays(r.end,1))-x,3), col2=zoneColor(r.zone);
      var _zt=r.name+' | '+dmy(r.start)+' ~ '+dmy(r.end)+' | '+fmtNum(r.panels)+it('g_unit_pcs')+' | '+fmtNum(r.days||0)+it('g_unit_day');
      h+='<div class="bar sum" data-id="'+esc(r.id)+'" style="left:'+Math.round(x)+'px;top:'+Math.round(top+bh/2-4)
        +'px;width:'+Math.round(w)+'px;background-color:'+col2+'"'
        +' data-tip="'+esc(_zt)+'" onmouseenter="igShowBarTip(event,this)" onmouseleave="igHideBarTip()"></div>';
      return;
    }
    /* house / team */
    var pct= r.panels? Math.round(Math.min(100,(r.done||0)/r.panels*100)) : 0;
    var col3=barColorOf(r);
    var x2=S.x(r.start), w2=Math.max(Math.round(S.dayW*(diffDays(r.start,r.end)+1)),4);
    var lbl;
    if(r.kind==='house') lbl=r.name+' '+fmtNum(r.days||0)+it('g_unit_day');
    else lbl=r.name+' · '+fmtNum((r.houses&&r.houses.length)||0)+it('g_load_dong');
    var locked=(r.kind==='house'&&r.house&&r.house.lockStart)?' locked':'';
    if(cfg.showBase&&r.kind==='house'&&r.house&&r.house.bs){
      var bx=S.x(r.house.bs), bw=Math.max(S.x(addDays(r.house.be,1))-bx,3);
      h+='<div class="base" style="left:'+Math.round(bx)+'px;top:'+Math.round(top-5)+'px;width:'+Math.round(bw)+'px"></div>';
    }
    h+='<div id="bar-'+esc(r.id)+'" class="bar'+(w2<48?' out':'')+locked+'" data-id="'+esc(r.id)+'" data-lbl="'+esc(lbl)+'"'
      +' style="left:'+Math.round(x2)+'px;top:'+Math.round(top)+'px;width:'+w2+'px;height:'+bh+'px;'
      +'--fg:'+fgOn(col3)+'"'
      +' data-tip="'+tipOf(r)+'" onmouseenter="igShowBarTip(event,this)" onmouseleave="igHideBarTip()"'
      +(r.kind==='house'?' onmousedown="dragStart(event,this)" ontouchstart="dragStart(event,this)"':'')+'></div>';
  });
  h+='</div>';   /* ← .bd 在这里才闭合：所有条形/依赖线都是它的子元素 */
  inner.style.width=S.width+'px';
  inner.innerHTML=h;
  rows.forEach(function(r,i){
    if(r.kind==='house'||r.kind==='team'||r.kind==='allgroup'){
      var el=document.getElementById('bar-'+esc(r.id));
      if(el){ var col=barColorOf(r); var pct=r.panels?Math.round(Math.min(100,(r.done||0)/r.panels*100)):0; setBarBody(el,r,S.x(r.start),Math.max(Math.round(S.dayW*(diffDays(r.start,r.end)+1)),4),col,pct); }
    }
  });
}
function bgForProgress(col,p){ return 'background-image:linear-gradient(to right,'
  +shade(col,-30)+' 0 '+p+'%,rgba(0,0,0,0) '+p+'% 100%)'; }
function barSegs(s,e){
  var segs=[]; var cur=toYmd(s), last=toYmd(e);
  if(!cur||!last) return segs;
  var curTet=!!TET[cur], segStart=cur;
  while(cur<last){
    cur=addDays(cur,1);
    var t=!!TET[cur];
    if(t!==curTet){ segs.push({start:segStart,end:addDays(cur,-1),tet:curTet}); segStart=cur; curTet=t; }
  }
  segs.push({start:segStart,end:last,tet:curTet});
  return segs;
}
function setBarBody(el,r,x,w,col,pct){
  var segs=barSegs(r.start,r.end), gray='#9e9e9e', h='';
  if(segs.length<=1){
    var fill=(segs[0]&&segs[0].tet)?gray:col;
    h+='<div class="bar-seg" style="left:0;top:0;width:100%;background:'+fill+'"></div>';
  } else {
    segs.forEach(function(seg){
      var sx=Math.round(S.x(seg.start)-x);
      var sw=Math.max(1, Math.round(S.x(addDays(seg.end,1))-S.x(seg.start)));
      h+='<div class="bar-seg" style="left:'+sx+'px;width:'+sw+'px;background:'+(seg.tet?gray:col)+'"></div>';
    });
  }
  h+='<div class="bar-progress" style="width:100%;'+bgForProgress(col,pct)+'"></div>';
  el.innerHTML=h;
}
function tipOf(r){
  if(r.kind==='house'){
    var h=r.house, rest=h.panels-h.done, wd=workDaysBetween(h.start,h.end);
    return esc(h.zone+' '+h.name+' | '+fmtNum(h.panels)+it('g_unit_pcs')+' → '+fmtNum(h.days)+it('g_unit_day')+'（'+fmtNum(cfg.cap)+it('g_unit_pcs')+'/'+it('g_unit_day')+'）'
      +' | '+teamLabel(h.team)+' | '+dmy(h.start)+' ~ '+dmy(h.end)
      +' | '+it('g_kpi_done')+fmtNum(h.done)+'（'+it('g_lbl_remaining')+fmtNum(rest)+'）'+(h.lockStart?' | '+it('g_locked_tip'):''));
  }
  if(r.kind==='team') return esc(r.name+' | '+fmtNum((r.houses&&r.houses.length)||0)+it('g_load_dong')+' | '+fmtNum(r.panels)+it('g_unit_pcs')+' | '+dmy(r.start)+' ~ '+dmy(r.end));
  return esc(r.name+' | '+dmy(r.start)+' ~ '+dmy(r.end)+' | '+fmtNum(r.panels)+'片');
}
/* 横道图自绘 tooltip：内容恒定可见（替代原生 title），随鼠标跟随并自动避让视口边缘 */
function igHideBarTip(){ var t=document.getElementById('igBarTip'); if(t) t.style.display='none'; }
function igShowBarTip(e, el){
  var txt = el.getAttribute('data-tip'); if(!txt){ igHideBarTip(); return; }
  var tip = document.getElementById('igBarTip');
  if(!tip){ tip=document.createElement('div'); tip.id='igBarTip'; tip.className='ig-tip'; document.body.appendChild(tip); }
  tip.textContent = txt;
  tip.style.display = 'block';
  var r = el.getBoundingClientRect();
  var tw = tip.offsetWidth || 220, th = tip.offsetHeight || 40;
  var vw = window.innerWidth || document.documentElement.clientWidth;
  var vh = window.innerHeight || document.documentElement.clientHeight;
  var left = r.left + r.width/2 - tw/2;
  left = Math.max(4, Math.min(left, vw - tw - 4));
  var top = r.top - th - 8;
  if(top < 4) top = r.bottom + 8;
  if(top + th > vh - 4) top = Math.max(4, r.top - th - 8);
  tip.style.left = Math.round(left)+'px';
  tip.style.top = Math.round(top)+'px';
}

/* =========================================================================
 * 8. 左侧表
 * ======================================================================= */
function renderTable(){
  var box=document.getElementById('tblWrap'), h='';
  var cols=visibleCols();
  h+='<table><colgroup>';
  cols.forEach(function(c){ h+='<col data-k="'+c.k+'" style="width:'+colW(c.k)+'px">'; });
  h+='</colgroup><thead><tr>';
  cols.forEach(function(c){
    h+='<th data-k="'+c.k+'" title="'+it('g_col_resize_tip')+'">'+esc(c.n)
      +'<i class="rs" onmousedown="colResizeStart(event,this)" ondblclick="colAutoFit(\''+c.k+'\')"></i></th>';
  });
  h+='</tr></thead><tbody>';
  if(cfg.view==='team'){
    zones.forEach(function(z){
      var zs=houses.filter(function(x){return x.zone===z.name;});
      if(!zs.length) return;
      var collapsed=isZoneCollapsed(z.name);
      h+='<tr class="zrow'+(collapsed?' collapsed':'')+'">'+cellsZone(z,cols,collapsed)+'</tr>';
      if(collapsed) return;
      for(var t=0;t<Math.max(1,z.teams|0);t++){
        h+='<tr class="trow">'+cellsTeam(z,t,cols)+'</tr>';
      }
      h+='<tr class="msrow">'+cellsMs(z,cols,false)+'</tr>';
    });
  }else{
    /* 房舍视图：左表必须与 buildRows() 严格同序（区汇总 → 按「安装计划总览」小方格顺序逐栋 → 区完工） */
    zones.forEach(function(z){
      var hs=houses.filter(function(h){ return h.zone===z.name; });
      if(!hs.length) return;
      var collapsed=isZoneCollapsed(z.name);
      h+='<tr class="zrow'+(collapsed?' collapsed':'')+'">'+cellsZone(z,cols,collapsed)+'</tr>';
      if(collapsed) return;
      /* 直接按 houses 输入顺序（= HOUSE_SOURCE = 安装总览排列）逐栋列出，不再按小组/开工日重排 */
      hs.forEach(function(hh){
        h+='<tr data-id="'+esc(hh.id)+'" onclick="selRow(this)">'+cellsHouse(hh,cols)+'</tr>';
      });
      h+='<tr class="msrow">'+cellsMs(z,cols,true)+'</tr>';
    });
  }
  if(!houses.length) h+='<tr><td class="empty" colspan="'+(cols.length||1)+'">'+it('g_empty_houses')+'</td></tr>';
  h+='</tbody></table>';
  box.innerHTML=h;
  syncTableWidth();
}
/* 可见列（至少保留一列，否则表格无法渲染） */
function visibleCols(){
  var cols=COLS.filter(function(c){ return (cfg.visible||[]).indexOf(c.k)>=0; });
  if(!cols.length) cols=[findCol('name')||COLS[0]];
  return cols;
}
/* 逐列拼单元格：隐藏某列时其余列仍能正确对齐 */
function rowCells(map, cols){
  var s=''; cols.forEach(function(c){ s+=(map[c.k]!==undefined?map[c.k]:'<td></td>'); }); return s;
}
function cellsZone(z, cols, collapsed){
  var hs=houses.filter(function(h){ return h.zone===z.name; });
  var pn=sum(hs,'panels'), dn=sum(hs,'done');
  return rowCells({
    zone:'<td><i class="collapse-btn" onclick="toggleZone(\''+esc(z.name)+'\',event)" title="'+esc(collapsed?it('g_expand'):it('g_collapse'))+'">'+(collapsed?'▶':'▼')+'</i>'+esc(z.name)+'</td>',
    name:'<td>'+it('g_zone_summary')+'</td>',
    panels:'<td class="num">'+fmtNum(pn)+'</td>',
    done:'<td class="num">'+fmtNum(dn)+'</td>',
    prog:'<td>'+(pn?Math.round(dn/pn*100)+'%':'0%')+'</td>',
    days:'<td>'+fmtNum(z.days||0)+'</td>',
    team:'<td>'+fmtNum(Math.max(1,z.teams|0))+it('g_unit_group')+'</td>',
    start:'<td>'+dmy(z.start)+'</td>',
    end:'<td>'+dmy(z.end)+'</td>'
  }, cols);
}
function cellsTeam(z, t, cols){
  var ths=houses.filter(function(x){ return x.zone===z.name&&x.team===t; })
                .sort(function(a,b){ return a.start<b.start?-1:(a.start>b.start?1:0); });
  var last=ths.length?ths[ths.length-1]:null;
  return rowCells({
    zone:'<td></td>',
    name:'<td>'+teamLabel(t)+'</td>',
    panels:'<td class="num">'+(ths.length?fmtNum(sum(ths,'panels')):'—')+'</td>',
    done:'<td class="num">'+(ths.length?fmtNum(sum(ths,'done')):'—')+'</td>',
    prog:'<td></td>',
    days:'<td>'+(ths.length?fmtNum(ths.length)+it('g_load_dong'):it('g_idle'))+'</td>',
    team:'<td></td>',
    start:'<td>'+(ths.length?dmy(ths[0].start):'—')+'</td>',
    end:'<td>'+(last?dmy(last.end):'—')+'</td>'
  }, cols);
}
function cellsMs(z, cols, showZone){
  return rowCells({
    zone:'<td>'+(showZone?esc(z.name):'')+'</td>',
    name:'<td>🏁'+it('g_finish')+'</td>',
    start:'<td>'+dmy(z.end)+'</td>',
    end:'<td>'+dmy(z.end)+'</td>'
  }, cols);
}
function cellsHouse(hh, cols){
  var nl1=hh.name1||hh.name||'', nl2=hh.name2||'';
  var nameCell='<td><div class="hn-l1">'+esc(nl1)+'</div>'+(nl2?'<div class="hn-l2">'+esc(nl2)+'</div>':'')+'</td>';
  return rowCells({
    zone:'<td>'+esc(hh.zone)+'</td>',
    name:nameCell,
    panels:'<td class="num"><span class="ro-num" title="'+esc(it('g_ro_auto'))+'">'+fmtNum(hh.panels)+'</span></td>',
    done:'<td class="num"><input type="text" value="'+fmtNum(hh.done)+'" onchange="evNum(\''+hh.id+'\',\'done\',this.value)"></td>',
    prog:'<td>'+(hh.panels?Math.round((hh.done||0)/hh.panels*100)+'%':'0%')+'</td>',
    days:'<td class="num">'+fmtNum(hh.days)+'</td>',
    team:'<td><select onchange="evTeam(\''+hh.id+'\',this.value);teamSelColor(this,\''+hh.id+'\')"'+(hh.bothTeams?' style="color:'+ALL_C+'"':((hh.lockTeam!=null||typeof hh.team==='number')?' style="color:'+teamColor(hh.zone,(hh.lockTeam!=null?hh.lockTeam:hh.team))+'"':''))+'>'+teamOpts(hh)+'</select></td>',
    start:'<td><input value="'+esc(dmy(hh.start))+'" onchange="evStart(\''+hh.id+'\',this.value)">'
      +(hh.lockStart?'<span class="lk" title="'+it('g_locked_tip')+'">🔒</span>':'')+'</td>',
    end:'<td>'+dmy(hh.end)+'</td>'
  }, cols);
}
function pctOf(r){ return r.panels?Math.round((r.done||0)/r.panels*100)+'%':'0%'; }
function teamOpts(h){
  var n=teamsOf(h.zone), s='';
  /* 默认显示排程实际分配到的组（未手选时 = h.team），不再默认显示全部组 */
  var eff=(h.lockTeam!=null)?(h.lockTeam|0):((typeof h.team==='number')?h.team:null);
  s+='<option value="all"'+(h.bothTeams?' selected':'')+' style="color:'+ALL_C+';font-weight:700;">'+it('g_allgroup')+'</option>';
  for(var i=0;i<n;i++){
    var col=teamColor(h.zone,i);
    s+='<option value="'+i+'"'+(!h.bothTeams&&eff===i?' selected':'')+' style="color:'+col+';font-weight:700;">'+teamLabel(i)+'</option>';
  }
  return s;
}
function teamSelColor(sel,id){
  var h=byId(id); if(!h) return;
  if(sel.value==='all'){ sel.style.color=ALL_C; return; }
  sel.style.color=teamColor(h.zone,+sel.value);
}
function evNum(id,k,v){
  var h=byId(id); if(!h) return;
  var raw=String(v||'').replace(/,/g,'');
  var n=Math.max(0,Math.round(+raw||0));
  if(k==='done') n=Math.min(n,h.panels);
  h[k]=n; schedule(); renderAll(); saveCfg();
}
function evTeam(id,v){ var h=byId(id); if(!h) return; setLockTeam(h,v); }
function evStart(id,v){ var h=byId(id); if(!h) return; setLockStart(h,v); }
function byId(id){ var r=null; houses.forEach(function(h){ if(h.id===id) r=h; }); return r; }
function selRow(tr){ var id=tr.getAttribute('data-id');
  var rs=document.querySelectorAll('#tblWrap tr[data-id]');
  for(var i=0;i<rs.length;i++) rs[i].classList.toggle('sel',rs[i].getAttribute('data-id')===id);
  var bs=document.querySelectorAll('#chartInner .bar');
  for(var j=0;j<bs.length;j++) bs[j].classList.toggle('sel',bs[j].getAttribute('data-id')===id); }
function syncTableWidth(){
  var box=document.getElementById('tblWrap'), tb=box&&box.querySelector('table'); if(!tb) return;
  var cols=visibleCols();
  var s=0; cols.forEach(function(c){ s+=colW(c.k); });
  var avail=Math.max(0,(box.clientWidth||0)-2), extra=avail>s?(avail-s):0;
  tb.style.width=(s+extra)+'px';
  var nm=tb.querySelector('col[data-k="name"]');
  if(nm) nm.style.width=(colW('name')+extra)+'px';
}
function colResizeStart(e,el){
  if(e.button!==undefined&&e.button!==0) return;
  var th=el.parentNode, k=th.getAttribute('data-k');
  e.preventDefault(); e.stopPropagation();
  var col=document.querySelector('#tblWrap col[data-k="'+k+'"]'); if(!col) return;
  var w0=colW(k), x0=e.clientX;
  th.classList.add('rs-on'); document.body.classList.add('col-resizing');
  function mv(ev){ var w=Math.max(COL_MIN,Math.min(COL_MAX,Math.round(w0+ev.clientX-x0)));
    cfg.colW=cfg.colW||{}; cfg.colW[k]=w; col.style.width=w+'px'; syncTableWidth(); }
  function up(){ document.removeEventListener('mousemove',mv); document.removeEventListener('mouseup',up);
    th.classList.remove('rs-on'); document.body.classList.remove('col-resizing'); saveCfg(); renderCfg(); }
  document.addEventListener('mousemove',mv); document.addEventListener('mouseup',up);
}
function estText(s){ s=String(s==null?'':s); var n=0;
  for(var i=0;i<s.length;i++) n+=(s.charCodeAt(i)>0x2e80)?12:6.6; return n; }
function measureText(s){
  s=String(s==null?'':s);
  var d=document.getElementById('igMeasure');
  if(!d){ d=document.createElement('span'); d.id='igMeasure';
    d.style.cssText='position:absolute;left:-9999px;top:0;visibility:hidden;white-space:nowrap;'
      +'font:12px -apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",Arial,sans-serif';
    document.body.appendChild(d); }
  d.textContent=s; var m=d.scrollWidth; return m>0?m:estText(s);
}
function colAutoFit(k, quiet){
  var c=findCol(k); if(!c) return;
  var mx=measureText(c.n)+30;
  if(k==='name') houses.forEach(function(h){ var n1=h.name1||h.name||''; mx=Math.max(mx,measureText(n1)+22); if(h.name2) mx=Math.max(mx,measureText(h.name2)+22); });
  if(k==='zone') houses.forEach(function(h){ mx=Math.max(mx,measureText(h.zone)+22); });
  if(k==='team') mx=Math.max(mx,measureText(it('g_team_fmt').replace('{n}',1))+40);
  if(k==='prog'||k==='days') mx=Math.max(mx, measureText('100%')+22);
  cfg.colW=cfg.colW||{}; cfg.colW[k]=Math.max(COL_MIN,Math.min(COL_MAX,Math.ceil(mx)));
  if(!quiet){ saveCfg(); renderTable(); syncTableWidth(); renderCfg(); }
}
function colFitAll(){
  cfg.colW={};
  visibleCols().forEach(function(c){ colAutoFit(c.k, true); });
  renderTable(); saveCfg(); syncTableWidth(); renderCfg();
}
function colReset(){
  cfg.colW={};
  cfg.visible=DEF.visible.slice();
  renderAll(); saveCfg();
}

/* =========================================================================
 * 9. KPI / 区汇总 / 负载
 * ======================================================================= */
function renderKPI(){
  var box=document.getElementById('kpi');
  if(!houses.length){ box.innerHTML='<span class="chip">'+it('g_kpi_empty')+'</span>'; return; }
  var tp=sum(houses,'panels'), td=sum(houses,'done');
  var mn='',mx='',lateZone='',zt={};
  zones.forEach(function(z){ if(!z.start) return;
    if(!mn||z.start<mn) mn=z.start;
    if(!mx||z.end>mx){ mx=z.end; lateZone=z.name; } });
  var totalDays=mn?diffDays(mn,mx)+1:0;
  /* 总作业组日 vs 总容量组日 */
  var work=0, span=0;
  zones.forEach(function(z){
    var n=Math.max(1,z.teams|0);
    houses.filter(function(h){ return h.zone===z.name; }).forEach(function(h){ work+=h.days; });
    if(z.start&&z.end) span+= workDaysBetween(z.start,z.end)*n;
  });
  var util=span?Math.round(work/span*100):0;
  var h='<span class="chip">'+it('g_kpi_zone')+' <b>'+fmtNum(zones.length)+'</b></span>'
   +'<span class="chip">'+it('g_kpi_houses')+' <b>'+fmtNum(houses.length)+'</b>'+it('g_load_dong')+'</span>'
   +'<span class="chip">'+it('g_kpi_panels')+' <b>'+fmtNum(tp)+'</b> '+it('g_unit_pcs')+'</span>'
   +'<span class="chip">'+it('g_kpi_done')+' <b>'+fmtNum(td)+'</b> ('+Math.round(td/tp*100)+'%)</span>'
   +'<span class="chip">'+it('g_kpi_cap')+' <b>'+fmtNum(cfg.cap)+'</b> '+it('g_unit_pcs')+'/'+it('g_unit_group')+'/'+it('g_unit_day')+'</span>'
   +'<span class="chip">'+it('g_kpi_teams')+' <b>'+fmtNum(zones.reduce(function(a,z){return a+Math.max(1,z.teams|0);},0))+'</b>'+it('g_unit_group')+'</span>'
   +'<span class="chip">'+it('g_kpi_range')+' <b>'+dmy(mn)+' ~ '+dmy(mx)+'</b></span>'
   +'<span class="chip">'+it('g_kpi_days')+' <b>'+fmtNum(totalDays)+'</b>'+it('g_unit_day')+'</span>'
   +'<span class="chip">'+it('g_kpi_latezone')+' <b>'+esc(lateZone)+'</b></span>'
   +'<span class="chip '+(util>=80?'ok':'')+'">'+it('g_kpi_util')+' <b>'+util+'%</b></span>';
  box.innerHTML=h;
}
function renderZoneTbl(){
  var t=document.getElementById('zoneTbl');
  var h='<thead><tr><th>'+it('g_zt_zone')+'</th><th>'+it('g_zt_team')+'</th><th class="n">'+it('g_zt_count')+'</th><th class="n">'+it('g_zt_panels')+'</th>'
    +'<th class="n">'+it('g_zt_done')+'</th><th class="n">'+it('g_zt_start')+'</th><th class="n">'+it('g_zt_end')+'</th><th class="n">'+it('g_zt_days')+'</th>'
    +'<th class="n">'+it('g_zt_ideal')+'</th><th class="n">'+it('g_zt_util')+'</th></tr></thead><tbody>';
  zones.forEach(function(z){
    var hs=houses.filter(function(x){ return x.zone===z.name; });
    var n=Math.max(1,z.teams|0), tp=sum(hs,'panels'), td=sum(hs,'done');
    var work=0; hs.forEach(function(x){ work+=x.days; });
    var ideal=Math.ceil(tp/Math.max(1,cfg.cap)/n);
    var real=hs.length?diffDays(z.start,z.end)+1:0;
    var realW=hs.length?workDaysBetween(z.start,z.end):0;
    var util=realW?Math.round(work/(realW*n)*100):0;
    h+='<tr><td><b>'+esc(z.name)+'</b></td>'
      +'<td><input type="number" min="1" max="12" value="'+n+'" style="width:56px;border:1px solid var(--bd);border-radius:4px;padding:2px 5px"'
      +' onchange="setTeams(\''+esc(z.name)+'\',this.value)"></td>'
      +'<td class="n">'+fmtNum(hs.length)+'</td><td class="n">'+fmtNum(tp)+'</td><td class="n">'+fmtNum(td)+'</td>'
      +'<td class="n"><input value="'+esc(z.userStart?dmy(z.userStart):dmy(z.start))+'" placeholder="'+it('g_ph_follow')+'"'
      +' style="width:84px;border:1px solid var(--bd);border-radius:4px;padding:2px 5px"'
      +' onchange="setZoneStart(\''+esc(z.name)+'\',this.value)" title="'+it('g_zone_start_tip')+'"></td>'
      +'<td class="n">'+dmy(z.end)+'</td>'
      +'<td class="n"><b>'+fmtNum(real)+'</b></td><td class="n">'+fmtNum(ideal)+'</td>'
      +'<td class="n"><span style="color:'+(util>=85?'#2e7d32':(util>=65?'#f57c00':'#c62828'))+'"><b>'+util+'%</b></span></td></tr>';
  });
  h+='</tbody>';
  t.innerHTML=h;
}
function setZoneStart(zname,v){
  var z=zoneOf(zname); if(!z) return;
  z.userStart=toYmd(v)||'';
  schedule(); renderAll(); saveCfg();
}
function setTeams(zname,v){
  var z=zoneOf(zname); if(!z) return;
  z.teams=Math.max(1,Math.min(12,parseInt(v,10)||1));
  houses.forEach(function(h){ if(h.zone===zname&&h.lockTeam!=null&&h.lockTeam>=z.teams) h.lockTeam=null; });
  try{ localStorage.setItem(ganttStorageKey('house_zones_v1'),JSON.stringify(zones)); }catch(e){}
  schedule(); renderAll(); saveCfg();
}
function renderLoad(){
  var box=document.getElementById('loadBox'), h='';
  zones.forEach(function(z){
    for(var t=0;t<Math.max(1,z.teams|0);t++){
      var hs=houses.filter(function(x){ return x.zone===z.name&&x.team===t; })
                   .sort(function(a,b){ return a.start<b.start?-1:1; });
      var work=0; hs.forEach(function(x){ work+=x.days; });
      var span=hs.length?workDaysBetween(hs[0].start,hs[hs.length-1].end):0;
      var util=span?Math.round(work/span*100):0;
      var col=teamColor(z.name,t);
      h+='<div class="load"><div class="lh"><span class="ln">'+esc(z.name)+' · '+teamLabel(t)+'</span>'
        +'<span class="lv">'+fmtNum(hs.length)+it('g_load_dong')+' · '+fmtNum(work)+it('g_load_workday')+' · '+it('g_load_util')+' <b>'+util+'%</b></span></div>'
        +'<div class="lbar">';
      if(span){
        var cursor=hs[0].start, idle=0;
        hs.forEach(function(x){
          var gap=diffDays(cursor,x.start);
          if(gap>0){ h+='<i style="width:'+(workDaysBetween(cursor,x.start)/span*100)+'%;background:#eceff1"></i>'; }
          h+='<i style="width:'+(workDaysBetween(x.start,x.end)/span*100)+'%;background:'+col
            +'" title="'+esc(x.name+' '+dmy(x.start)+'~'+dmy(x.end)+' '+fmtNum(x.days)+it('g_unit_day'))+'"></i>';
          cursor=addDays(x.end,1);
        });
      }else h+='<i style="width:100%;background:#eceff1"></i>';
      h+='</div><div class="lf">'+(hs.length?(it('g_load_first')+' <b>'+esc(hs[0].name)+'</b> '+dmy(hs[0].start)
        +' → '+it('g_load_last')+' <b>'+esc(hs[hs.length-1].name)+'</b> '+dmy(hs[hs.length-1].end)
        +(util<70?' · <span style="color:#c62828">'+it('g_load_idle_warn')+'</span>':'')):'<b>'+it('g_idle')+'</b>' )
        +'</div></div>';
    }
  });
  box.innerHTML=h;
  /* 冲突检测 */
  var cb=document.getElementById('conflict'), warn=[];
  zones.forEach(function(z){
    var byTeam={};
    houses.forEach(function(h){ if(h.zone!==z.name) return;
      (byTeam[h.team]=byTeam[h.team]||[]).push(h); });
    Object.keys(byTeam).forEach(function(tk){
      var arr=byTeam[tk].slice().sort(function(a,b){ return a.start<b.start?-1:1; });
      for(var i=1;i<arr.length;i++){
        if(arr[i].start<=arr[i-1].end)
          warn.push(z.name+' '+teamLabel(+tk)+'：'+arr[i-1].name+it('g_overlap_with')+arr[i].name+' '+it('g_time_overlap')+'（'+dmy(arr[i-1].end)+' / '+dmy(arr[i].start)+'）');
      }
    });
  });
  zones.forEach(function(z){ if(z.teams>Math.max(1,z.teams|0)) warn.push(''); });
  houses.forEach(function(h){ if(!h.start||!h.end) warn.push('【'+h.zone+' '+h.name+'】'+it('g_not_scheduled')); });
  cb.innerHTML=warn.filter(Boolean).length
    ? '<div class="warnbox"><b>'+it('g_check_title')+'（'+warn.filter(Boolean).length+'）</b><ul>'
      +warn.filter(Boolean).slice(0,8).map(function(x){ return '<li>'+esc(x)+'</li>'; }).join('')+'</ul></div>' : '';
  /* 图例 */
  var lg=document.getElementById('legend');
  lg.innerHTML=cfg.color==='zone'
    ? zones.map(function(z){ return '<span><i style="background:'+zoneColor(z.name)+'"></i>'+esc(z.name)+'</span>'; }).join('')
    : '<span>'+it('g_legend_team')+'</span>';
  lg.innerHTML+='<span><i style="background:#eceff1"></i>'+it('g_legend_idle')+'</span>'
    +'<span><i style="background:#cbd5e0"></i>'+it('g_legend_base')+'</span>'
    +'<span><i style="background:#ffa726;transform:rotate(45deg)"></i>'+it('g_legend_milestone')+'</span>'
    +'<span style="color:#c62828">'+it('g_legend_lock')+'</span>';
}

/* =========================================================================
 * 10. 拖拽（房舍条 -> 锁定开工日）
 * ======================================================================= */
var drag=null;
function ptX(e){ if(e.touches&&e.touches.length) return e.touches[0].clientX;
  if(e.changedTouches&&e.changedTouches.length) return e.changedTouches[0].clientX; return e.clientX; }
function ptY(e){ if(e.touches&&e.touches.length) return e.touches[0].clientY;
  if(e.changedTouches&&e.changedTouches.length) return e.changedTouches[0].clientY; return e.clientY; }
function dragStart(e,el){
  var id=el.getAttribute('data-id'), h=byId(id); if(!h) return;
  if(e.type==='touchstart'&&e.touches.length>1) return;
  igHideBarTip();
  drag={h:h,x0:ptX(e)+(document.getElementById('chartWrap').scrollLeft||0),moved:false,
        touch:e.type.indexOf('touch')===0};
  e.preventDefault();
  var mv=drag.touch?'touchmove':'mousemove', up=drag.touch?'touchend':'mouseup';
  document.addEventListener(mv,dragMove,{passive:false});
  document.addEventListener(up,dragEnd);
  document.addEventListener('touchcancel',dragEnd);
}
function applyDrag(x){
  if(!drag) return;
  var cw=document.getElementById('chartWrap');
  var dx=(x+(cw?cw.scrollLeft:0))-drag.x0;
  if(Math.abs(dx)>2) drag.moved=true;
  var target=addDays(drag.h.lockStart||drag.h.start, Math.round(dx/S.dayW));
  drag.h.start=nextWork(target);
  drag.h.end=addWork(drag.h.start,drag.h.days);
  updateRowsAfterDrag();
}
function updateRowsAfterDrag(){
  var r=null; rows.forEach(function(x){ if(x.kind==='house'&&x.house===drag.h) r=x; });
  if(r){ r.start=drag.h.start; r.end=drag.h.end; }
  var i=rows.indexOf(r); if(i>=0) updateBar(i);
  var svg=document.getElementById('depSvg'); if(svg) svg.classList.add('dragging');
}
function dragMove(e){
  if(!drag) return;
  if(e.cancelable) e.preventDefault();
  var x=ptX(e), y=ptY(e); drag.lastX=x; drag.lastY=y;
  applyDrag(x); edgeScroll(x,y);
}
var edgeRAF=null;
function edgeScroll(x,y){
  var cw=document.getElementById('chartWrap'); if(!cw||!drag) return;
  var r=cw.getBoundingClientRect(), E=48, hx=0, vy=0;
  if(x>r.right-E) hx=1; else if(x<r.left+E) hx=-1;
  if(y>r.bottom-E) vy=1; else if(y<r.top+E) vy=-1;
  drag.edge=hx; drag.edgeV=vy;
  if((hx||vy)&&!edgeRAF) edgeRAF=requestAnimationFrame(edgeTick);
}
function edgeTick(){
  edgeRAF=null; if(!drag||(!drag.edge&&!drag.edgeV)) return;
  var cw=document.getElementById('chartWrap'), tw=document.getElementById('tblWrap');
  if(drag.edge) cw.scrollLeft+=drag.edge*16;
  if(drag.edgeV){ var mx=Math.max(0,cw.scrollHeight-cw.clientHeight);
    var tp=Math.max(0,Math.min(cw.scrollTop+drag.edgeV*10,mx)); cw.scrollTop=tp; if(tw) tw.scrollTop=tp; }
  if(drag.edge) applyDrag(drag.lastX);
  edgeRAF=requestAnimationFrame(edgeTick);
}
function dragEnd(){
  if(edgeRAF){ cancelAnimationFrame(edgeRAF); edgeRAF=null; }
  var svg=document.getElementById('depSvg'); if(svg) svg.classList.remove('dragging');
  if(drag){
    if(drag.moved){ drag.h.lockStart=drag.h.start; }   /* 拖过 = 锁定开工日 */
    schedule(); renderAll(); saveCfg();
  }
  drag=null;
  document.removeEventListener('mousemove',dragMove);
  document.removeEventListener('mouseup',dragEnd);
  document.removeEventListener('touchmove',dragMove);
  document.removeEventListener('touchend',dragEnd);
  document.removeEventListener('touchcancel',dragEnd);
}
function updateBar(i){
  var r=rows[i]; if(!r) return;
  var el=document.querySelector('#chartInner .bar[data-id="'+cssEsc(r.id)+'"]'); if(!el) return;
  var rh=rowH(), bh=cfg.barHeight, top=i*rh+(rh-bh)/2;
  var pct=r.panels?Math.round(Math.min(100,(r.done||0)/r.panels*100)):0;
  var col=barColorOf(r);
  var x=S.x(r.start), w=Math.max(Math.round(S.dayW*(diffDays(r.start,r.end)+1)),4);
  el.className='bar'+(w<48?' out':'')+(r.house&&r.house.lockStart?' locked':'');
  el.style.cssText='left:'+Math.round(x)+'px;top:'+Math.round(top)+'px;width:'+w+'px;height:'+bh+'px;';
  setBarBody(el,r,x,w,col,pct);
  el.setAttribute('data-tip', tipOf(r));
  if(r.kind==='house') el.setAttribute('data-lbl',r.name+' '+fmtNum(r.days||0)+it('g_unit_day'));
}
function cssEsc(s){ return String(s).replace(/([ #.;?%&,@+*~':"!\^$[\]()=>|/])/g,'\\$1'); }

/* =========================================================================
 * 11. 分隔线
 * ======================================================================= */
function applyTblW(){ document.documentElement.style.setProperty('--tbl-w',Math.round(cfg.tableWidth||470)+'px'); }
function fitTblW(){ var s=0; COLS.forEach(function(c){ s+=colW(c.k); });
  cfg.tableWidth=Math.max(220,Math.min(s+2,Math.max(window.innerWidth-360,280)));
  applyTblW(); saveCfg(); }
function initSplitter(){
  var sp=document.getElementById('splitter'); if(!sp||sp.__init) return; sp.__init=1;
  function clamp(w){ return Math.max(220,Math.min(w,Math.max(window.innerWidth-360,300))); }
  sp.addEventListener('mousedown',function(e){
    if(e.button!==0) return; e.preventDefault();
    var w0=cfg.tableWidth||470, x0=e.clientX;
    sp.classList.add('on'); document.body.classList.add('resizing');
    function mv(ev){ cfg.tableWidth=Math.round(clamp(w0+ev.clientX-x0)); applyTblW(); }
    function up(){ document.removeEventListener('mousemove',mv); document.removeEventListener('mouseup',up);
      sp.classList.remove('on'); document.body.classList.remove('resizing'); saveCfg(); }
    document.addEventListener('mousemove',mv); document.addEventListener('mouseup',up); });
  sp.addEventListener('dblclick',fitTblW);
}
function syncScroll(){
  var a=document.getElementById('tblWrap'), b=document.getElementById('chartWrap');
  if(!a||!b||a.__sync) return; a.__sync=1; var lock=false, src=null;
  function link(p,q){ p.addEventListener('scroll',function(){
    if(lock||src===p) return; lock=true; src=p;
    q.scrollTop=p.scrollTop; q.scrollLeft=p.scrollLeft;
    requestAnimationFrame(function(){ lock=false; src=null; }); }); }
  link(a,b); link(b,a);
}


/* =========================================================================
 * 13. 参数绑定 / 主入口
 * ======================================================================= */
function readParams(){
  var e=document.getElementById('p_cap'); if(e) cfg.cap=Math.max(1,parseInt(e.value,10)||200);
  e=document.getElementById('p_start'); if(e) cfg.start=toYmd(e.value)||cfg.start||today();
}
function syncParamUI(){
  var e=document.getElementById('p_cap'); if(e) e.value=cfg.cap;
  e=document.getElementById('p_start');
  if(e) e.value=cfg.start?cpFmtDDMMYYYY(+cfg.start.slice(0,4),+cfg.start.slice(5,7)-1,+cfg.start.slice(8,10)):'';
}
function recompute(){ readParams(); schedule(); renderAll(); saveCfg(); }
/* ---------- 显示设置面板 ---------- */
var CFG_SCHED_KEYS={cap:1,start:1,cal:1,strat:1,zmode:1,holidays:1};
function setCfg(k,v){
  if(k==='cap') cfg.cap=Math.max(1,parseInt(v,10)||200);
  else if(k==='start') cfg.start=toYmd(v)||cfg.start||today();
  else cfg[k]=v;
  if(CFG_SCHED_KEYS[k]) schedule();
  renderAll(); saveCfg();
}
/* 顶部快捷按钮：在「按房舍 / 按小组泳道」之间切换（依赖连线只在泳道视图绘制） */
function toggleViewQuick(){ cfg.view=(cfg.view==='team')?'house':'team'; renderAll(); saveCfg(); }
function syncViewQuick(){
  var b=document.getElementById('btnViewQuick');
  if(b){ b.textContent=it(cfg.view==='team'?'g_view_team':'g_view_house'); b.title=it('g_lbl_view'); }
}
function toggleCol(k,on){
  cfg.visible=cfg.visible||[];
  var i=cfg.visible.indexOf(k);
  if(on&&i<0) cfg.visible.push(k);
  if(!on&&i>=0) cfg.visible.splice(i,1);
  if(!cfg.visible.length) cfg.visible=['name'];
  renderAll(); saveCfg();
}
function gToggleCfg(){
  var p=document.getElementById('cfgPanel'); if(!p) return;
  p.classList.toggle('open');
  cfg.cfgOpen=p.classList.contains('open');
  saveCfg();
}
function syncCfgOpen(){
  var p=document.getElementById('cfgPanel'); if(!p) return;
  var shouldOpen=cfg.cfgOpen, isOpen=p.classList.contains('open');
  if(shouldOpen===isOpen) return;
  if(shouldOpen){
    p.classList.add('no-anim');
    p.classList.add('open');
    void p.offsetWidth;          // force reflow before re-enabling transition
    p.classList.remove('no-anim');
  } else {
    p.classList.remove('open');
  }
}
function renderCfg(){
  var box=document.getElementById('cfgPanel'); if(!box) return;
  var h='<div class="cfg-h"><span>'+it('g_cfg_title')+'</span><button type="button" onclick="gToggleCfg()">×</button></div><div class="cfg-b">';
  /* 可视化 */
  h+='<div class="cfg-sec"><div class="cfg-t">'+it('g_cfg_visual')+'</div>';
  [['showWeekend','g_cfg_weekend'],['showToday','g_cfg_today'],['showGrid','g_cfg_grid'],
   ['showDeps','g_cfg_deps']].forEach(function(o){
    h+='<label><input type="checkbox" '+(cfg[o[0]]?'checked':'')+' onchange="setCfg(\''+o[0]+'\',this.checked)"> '+it(o[1])+'</label>';
  });
  h+='<label><input type="checkbox" '+(cfg.showBase?'checked':'')+' onchange="toggleBaseline(this.checked)"> '+it('g_cfg_base')+'</label>';
  h+='<label>'+it('g_cfg_granularity')+' <select onchange="setCfg(\'viewMode\',this.value)">';
  [['Day','g_gran_day'],['Week','g_gran_week'],['Month','g_gran_month']].forEach(function(o){
    h+='<option value="'+o[0]+'"'+(cfg.viewMode===o[0]?' selected':'')+'>'+it(o[1])+'</option>';
  }); h+='</select></label>';
  h+='<label>'+it('g_cfg_datesep')+' <select onchange="setCfg(\'dateSep\',this.value)">';
  [['/','17/08/2026'],['-','17-08-2026'],['.','17.08.2026']].forEach(function(o){
    h+='<option value="'+o[0]+'"'+(cfg.dateSep===o[0]?' selected':'')+'>'+o[1]+'</option>';
  }); h+='</select></label>';
  h+='<label>'+it('g_cfg_colwidth')+' <input type="range" min="24" max="110" value="'+cfg.colWidth+'" onchange="setCfg(\'colWidth\',+this.value)"><span class="cw">'+cfg.colWidth+'</span></label>';
  h+='<label>'+it('g_cfg_rowheight')+' <input type="range" min="14" max="38" value="'+cfg.barHeight+'" onchange="setCfg(\'barHeight\',+this.value)"><span class="cw">'+cfg.barHeight+'</span></label>';
  h+='<label>'+it('g_cfg_color')+' <select onchange="setCfg(\'color\',this.value)">';
  [['zone','g_color_zone'],['team','g_color_team']].forEach(function(o){
    h+='<option value="'+o[0]+'"'+(cfg.color===o[0]?' selected':'')+'>'+it(o[1])+'</option>';
  }); h+='</select></label>';
  h+='</div>';
  /* 排程参数（原顶部下拉已并入此处，基线控制已并入「可视化」复选框） */
  h+='<div class="cfg-sec"><div class="cfg-t">'+it('g_params')+'</div>';

  h+='<label>'+it('g_lbl_strat')+' <select onchange="setCfg(\'strat\',this.value)">';
  [['lpt','g_strat_lpt'],['greedy','g_strat_greedy']].forEach(function(o){
    h+='<option value="'+o[0]+'"'+(cfg.strat===o[0]?' selected':'')+'>'+it(o[1])+'</option>';
  }); h+='</select></label>';
  h+='<label>'+it('g_lbl_zmode')+' <select onchange="setCfg(\'zmode\',this.value)">';
  [['parallel','g_zmode_parallel'],['serial','g_zmode_serial']].forEach(function(o){
    h+='<option value="'+o[0]+'"'+(cfg.zmode===o[0]?' selected':'')+'>'+it(o[1])+'</option>';
  }); h+='</select></label>';
  h+='<label>'+it('g_lbl_view')+' <select onchange="setCfg(\'view\',this.value)">';
  [['house','g_view_house'],['team','g_view_team']].forEach(function(o){
    h+='<option value="'+o[0]+'"'+(cfg.view===o[0]?' selected':'')+'>'+it(o[1])+'</option>';
  }); h+='</select></label>';
  /* 春节停工日由生产模块 BOARD_HOLIDAYS 自动注入，无需手动输入 */
  h+='</div>';
  /* 数据字段 */
  h+='<div class="cfg-sec"><div class="cfg-t">'+it('g_cfg_fields')+'</div>';
  COLS.forEach(function(c){
    h+='<label><input type="checkbox" '+(cfg.visible.indexOf(c.k)>=0?'checked':'')
      +' onchange="toggleCol(\''+c.k+'\',this.checked)"> '+esc(c.n)
      +'<span class="cw">'+colW(c.k)+'</span></label>';
  });
  h+='<div class="cfg-btns"><button type="button" onclick="colFitAll()">'+it('g_btn_colfit')+'</button>'
    +'<button type="button" onclick="colReset()">'+it('g_btn_colreset')+'</button></div>';
  h+='<div class="cfg-hint">'+it('g_cfg_hint')+'</div>';
  h+='</div>';
  h+='</div>';
  box.innerHTML=h;
  syncViewQuick();
}
function renderAll(){
  refreshCols();
  document.documentElement.style.setProperty('--row-h',rowH()+'px');
  document.documentElement.style.setProperty('--head-h','48px');
  applyTblW();
  buildRows(); renderChart(); renderTable();
  renderKPI(); renderZoneTbl(); renderLoad(); renderCfg(); syncScroll();
  syncCfgOpen();
  applyCardsCollapsed();
  applyPlanFields();
}
/* 排程参数里新增的只读字段：
   - 合同签订日期 / 建厂筹备至试运营 / 试运营结束（开始生产）/ 开始生产日期：来自安装计划（GANTT_PLAN，父页注入）
   - 安装结束日 / 总安装天数：取自 KPI（项目区间的结束 与 总工期），与 #kpi 同源 */
/* 列标题按当前语言刷新（COLS 在加载时只算一次，切换语言后需重新取 it） */
function refreshCols(){
  COLS.forEach(function(c){ var v=it('g_col_'+c.k); if(v && v!==('g_col_'+c.k)) c.n=v; });
}
function applyPlanFields(){
  var plan = (typeof GANTT_PLAN!=='undefined' && GANTT_PLAN) ? GANTT_PLAN : {};
  var setv=function(id,v){ var el=document.getElementById(id); if(el) el.value=(v==null?'':String(v)); };
  setv('gp_contract', plan.contract);
  setv('gp_prep', plan.prepStart);
  setv('gp_prep_end', plan.prepEnd);
  setv('gp_due', plan.due);
  var endVal='', daysVal='';
  try{
    var rEl=document.querySelector('#kpi > span:nth-child(7) > b');
    if(rEl){ var t=String(rEl.textContent||''); var parts=t.split('~'); endVal=((parts.length>1?parts[1]:t)||'').trim()||t.trim(); }
    var dEl=document.querySelector('#kpi > span:nth-child(8)');
    if(dEl){ var b=dEl.querySelector('b'); daysVal=((b?b.textContent:'').trim()||'')+it('g_unit_day'); }
  }catch(e){}
  setv('gp_install_end', endVal);
  setv('gp_install_days', daysVal);
}
/* 打印 EXCEL：导出整份计划（参数 + 各区汇总 + 全部房舍明细）为 .xls（Excel 可直接打开） */
function printExcel(){
  var cols=[
    {n:it('g_col_zone'),   v:function(h){ return h.zone; }},
    {n:it('g_col_name'),   v:function(h){ return h.name1+(h.name2?(' '+h.name2):''); }},
    {n:it('g_col_panels'), v:function(h){ return fmtNum(h.panels); }, num:1},
    {n:it('g_col_done'),   v:function(h){ return fmtNum(h.done); }, num:1},
    {n:it('g_col_prog'),   v:function(h){ return (h.panels?Math.round((h.done||0)/h.panels*100):0)+'%'; }},
    {n:it('g_col_days'),   v:function(h){ return fmtNum(h.days); }, num:1},
    {n:it('g_col_team'),   v:function(h){ return h.bothTeams?it('g_allgroup'):teamLabel(h.lockTeam!=null?h.lockTeam:(typeof h.team==='number'?h.team:0)); }},
    {n:it('g_col_start'),  v:function(h){ return dmy(h.start); }},
    {n:it('g_col_end'),    v:function(h){ return dmy(h.end); }}
  ];
  var N=cols.length;
  var gv=function(id){ var e=document.getElementById(id); return e&&e.value?e.value:''; };
  var h='<meta charset="utf-8"><table border="1" cellspacing="0" cellpadding="3" style="border-collapse:collapse;font-family:Arial,sans-serif;font-size:11px;">';
  h+='<tr><td colspan="'+N+'" style="font-size:15px;font-weight:bold;">'+esc(it('g_title'))+'</td></tr>';
  h+='<tr><td colspan="'+N+'">'
    +esc(it('g_lbl_contract')+'：'+gv('gp_contract'))
    +' ｜ '+esc(it('g_lbl_prep')+'：'+gv('gp_prep'))
    +' ｜ '+esc(it('g_lbl_prep_end')+'：'+gv('gp_prep_end'))
    +' ｜ '+esc(it('g_lbl_start')+'：'+gv('p_start'))
    +' ｜ '+esc(it('g_lbl_install_end')+'：'+gv('gp_install_end'))
    +' ｜ '+esc(it('g_lbl_due')+'：'+gv('gp_due'))
    +' ｜ '+esc(it('g_lbl_install_days')+'：'+gv('gp_install_days'))
    +'</td></tr>';
  h+='<tr>'+cols.map(function(c){ return '<th style="background:#f3eaff;">'+esc(c.n)+'</th>'; }).join('')+'</tr>';
  zones.forEach(function(z){
    var hs=houses.filter(function(x){ return x.zone===z.name; });
    if(!hs.length) return;
    var _pn=sum(hs,'panels'), _dn=sum(hs,'done');
    h+='<tr style="background:#f7f9fb;font-weight:bold;">'
      +'<td>'+esc(z.name)+'</td><td>'+esc(it('g_zone_summary'))+'</td>'
      +'<td align="right">'+fmtNum(_pn)+'</td><td align="right">'+fmtNum(_dn)+'</td>'
      +'<td align="center">'+(_pn?Math.round(_dn/_pn*100):0)+'%</td>'
      +'<td align="right">'+fmtNum(z.days||0)+'</td><td>'+fmtNum(Math.max(1,z.teams|0))+esc(it('g_unit_group'))+'</td>'
      +'<td>'+esc(dmy(z.start))+'</td><td>'+esc(dmy(z.end))+'</td></tr>';
    hs.forEach(function(hh){
      h+='<tr>'+cols.map(function(c){
        return '<td'+(c.num?' align="right"':'')+'>'+esc(c.v(hh)||'')+'</td>';
      }).join('')+'</tr>';
    });
  });
  h+='</table>';
  var blob=new Blob(['\ufeff'+h],{type:'application/vnd.ms-excel;charset=utf-8'});
  var a=document.createElement('a'); a.href=URL.createObjectURL(blob);
  a.download=it('g_title')+'_'+today()+'.xls';
  document.body.appendChild(a); a.click();
  setTimeout(function(){ try{ URL.revokeObjectURL(a.href); }catch(e){} if(a.parentNode) a.parentNode.removeChild(a); }, 200);
}
/* ═══════════════════════════════════════════════════════════════════════════
   [FROZEN 契约 · 打印] 甘特(横道图)打印 —— 改动前先读 check_print_logic.py
   ───────────────────────────────────────────────────────────────────────────
   1) 必须保持「左右两栏」：模板里有 @media (max-width:1000px){.layout{flex-direction:column}}，
      打印时纸宽按纸张算（A4 竖版可打印宽≈748px < 1000px 会命中这条移动端规则），
      不覆盖就会把「左表」和「横道图」拆成上下两半 —— 所以必须 flex-direction:row !important。
   2) 左表必须固定宽度 width:var(--tbl-w,470px) !important
      （改成 auto 会让 flex:0 0 auto 吃光整行，横道图被挤成 0 宽 → 打印时消失）。
   3) 三档纸张缩放（A3 横向 / A4 横向 / A4 竖版）必须保留；
      缩放高度 totalH 必须包含版面上方内容(offTop)，否则甘特被顶到第 2 页。
   4) 必须排除甘特下方 #cardsWrap（区汇总/小组负载/图例），否则多打一张空白废页。
   5) 禁止强制分页 break-before:page / page-break-before:always（会把甘特整块顶到第 2 页）。
   ═══════════════════════════════════════════════════════════════════════════ */
function printPdf(){
  var st=document.getElementById('printStyle');
  if(!st){ st=document.createElement('style'); st.id='printStyle'; document.head.appendChild(st); }
  var totalW=0, totalH=0, offTop=0;
  try{
    var tw=document.getElementById('tblWrap');
    var ci=document.getElementById('chartInner');
    var lay=document.querySelector('.layout');
    /* 版面上方还有标题/参数卡片，缩放要连它们一起算，否则甘特会被顶到第 2 页 */
    offTop = lay ? Math.max(0, Math.round(lay.getBoundingClientRect().top + (window.pageYOffset||0))) : 0;
    totalW=(tw?tw.scrollWidth:0)+((ci&&ci.scrollWidth)||0);
    totalH=offTop + Math.max(tw?tw.scrollHeight:0, (ci&&ci.scrollHeight)||0);
  }catch(e){}
  /* 按「纸张可打印区」算缩放比（96dpi，已扣 6mm 页边距）：
     A3 横向 ≈1480x1020、A4 横向 ≈1077x720、A4 竖版 ≈748x1030。
     打印时用 @media print and (max-width:…) 按实际纸张选一套，保证任何纸张都"一页装下"。 */
  function fitZ(pw, ph){
    if(!(totalW>0 && totalH>0)) return 1;
    return Math.min(totalW>pw ? pw/totalW : 1, totalH>ph ? ph/totalH : 1);
  }
  var zA3=fitZ(1480,1020), zA4L=fitZ(1077,720), zA4P=fitZ(748,1030);
  st.textContent='@media print{'
    +'@page{size:A3 landscape;margin:6mm;}'
    +'.hdr-btns,.params-row .btn,.splitter,.cfg,.cards-toggle,#btnDisplayCfg{display:none !important;}'
    /* 甘特下方的「区汇总 + 小组负载 + 图例」不属于打印内容：它在窄纸下会被挤到第 2 页，
       打出一张几乎空白的废页（用户要的是完整甘特一页）。 */
    +'.cards-wrap,#cardsWrap,.loadgrid,#loadBox,#conflict,.legend{display:none !important;}'
    /* ★ 根因修复「左表与横道图被拆成上下两半」：
       模板里有 @media (max-width:1000px){ .layout{flex-direction:column} .tbl-wrap{width:100% !important} … }
       这条移动端规则在【窄纸打印】时同样会命中（A4 竖版可打印宽 ≈748px < 1000px），
       于是 .layout 变成纵向排列 —— 左表跑到上面、横道图被压到下面，看上去就是"左右两部分被拆成上下两半"。
       这里强制回左右两栏，override 掉移动端规则（本样式在模板样式之后注入，同优先级下后写者胜）。 */
    +'.layout{display:flex !important;flex-direction:row !important;flex-wrap:nowrap !important;height:auto !important;max-height:none !important;overflow:visible !important;border:none !important;border-radius:0 !important;'
    +'break-inside:avoid !important;page-break-inside:avoid !important;}'
    /* 关键：左表保持原宽度（不要 width:auto，否则 flex:0 0 auto 会吃光整行，把右表挤成 0 宽→横道图消失） */
    +'.tbl-wrap{flex:0 0 auto !important;width:var(--tbl-w,470px) !important;max-height:none !important;overflow:visible !important;border-right:1px solid var(--bd) !important;border-bottom:0 !important;}'
    +'.chart-wrap{flex:1 1 auto !important;min-width:0 !important;min-height:0 !important;max-height:none !important;overflow:visible !important;}'
    +'.tbl-wrap table{width:auto !important;}'
    +'.tbl-wrap th,.thead{position:static !important;}'
    +'.tbl-wrap,.chart-wrap,.ci,.bd,.thead,.bd *{break-inside:avoid !important;page-break-inside:avoid !important;}'
    +'.bd,.ci{overflow:visible !important;}'
    +'*{-webkit-print-color-adjust:exact !important;print-color-adjust:exact !important;}'
    +'}'
    +'@media print{html{zoom:'+zA3.toFixed(3)+' !important;}}'
    +'@media print and (max-width:1120px){html{zoom:'+zA4L.toFixed(3)+' !important;}}'
    +'@media print and (max-width:800px){html{zoom:'+zA4P.toFixed(3)+' !important;}}';
  window.print();
}
/* 区汇总 + 小组负载：右上角 +/− 一起收起/展开（状态存 cfg，持久化） */
function applyCardsCollapsed(){
  var wrap=document.getElementById('cardsWrap'); if(!wrap) return;
  wrap.classList.toggle('collapsed', !!cfg.cardsCollapsed);
  var btn=document.getElementById('cardsToggle');
  if(btn) btn.textContent = cfg.cardsCollapsed ? '+' : '−';
}
function toggleCards(){
  cfg.cardsCollapsed=!cfg.cardsCollapsed;
  saveCfg();
  applyCardsCollapsed();
}
function rebuild(){ loadHouses(); schedule(); renderAll(); }

window.addEventListener('resize',function(){ clearTimeout(window.__rt); window.__rt=setTimeout(function(){ renderChart(); renderTable(); syncTableWidth(); },150); });

/* ============================ 日历弹出框（DD-MM-YYYY，标准设计，iframe 内自包含） ============================ */
var cpCalTarget=null, cpCalOpenedAt=0, cpCalViewYear, cpCalViewMonth;
function cpPad(n){ return n<10?'0'+n:''+n; }
function cpFmtDDMMYYYY(y,m,d){ return cpPad(d)+'/'+cpPad(m+1)+'/'+y; }
function cpParseDDMMYYYY(s){ if(!s) return null; var m=s.match(/^(\d{1,2})[-/.](\d{1,2})[-/.](\d{4})$/); return m?{y:+m[3],m:+m[2]-1,d:+m[1]}:null; }
function cpGetWeekDays(){ var lang=curLang(); if(lang==='en') return ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']; if(lang==='vi') return ['CN','T2','T3','T4','T5','T6','T7']; return ['日','一','二','三','四','五','六']; }
function cpGetMonthName(m){ var lang=curLang(); var months = lang==='en' ? ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'] : lang==='vi' ? ['Th.1','Th.2','Th.3','Th.4','Th.5','Th.6','Th.7','Th.8','Th.9','Th.10','Th.11','Th.12'] : ['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月']; return months[m]||''; }
function cpOpenCalendar(inputEl){
  if(inputEl && inputEl.disabled) return;
  cpCalTarget=inputEl;
  var rect=inputEl.getBoundingClientRect();
  var popup=document.getElementById('cpCalPopup');
  var top=rect.bottom+4, left=rect.left;
  if(left+248>window.innerWidth) left=Math.max(8,window.innerWidth-260);
  if(top+330>window.innerHeight) top=Math.max(8,rect.top-334);
  popup.style.top=top+'px'; popup.style.left=left+'px';
  popup.classList.add('show');
  cpCalOpenedAt=Date.now();
  var L=curLang(); var lbl=L==='en'?{today:'Today',clear:'Clear'}:L==='vi'?{today:'Hôm nay',clear:'Xóa'}:{today:'今天',clear:'清除'};
  var tb=document.querySelector('.cp-cal-today'); if(tb) tb.textContent=lbl.today;
  var cb=document.getElementById('cpCalClear'); if(cb) cb.textContent=lbl.clear;
  var cur=cpParseDDMMYYYY(inputEl.value);
  var now=new Date();
  cpCalViewYear=cur?cur.y:now.getFullYear();
  cpCalViewMonth=cur?cur.m:now.getMonth();
  cpRenderCal(cur);
}
function cpCloseCalendar(){ var popup=document.getElementById('cpCalPopup'); if(popup) popup.classList.remove('show'); cpCalTarget=null; }
function cpCalBuildYM(){
  var ys=document.getElementById('cpYearSel'), ms=document.getElementById('cpMonthSel'); if(!ys||!ms) return;
  var yNow=new Date().getFullYear(), o='';
  for(var yy=2000; yy<=yNow+50; yy++) o+='<option value="'+yy+'"'+(yy===cpCalViewYear?' selected':'')+'>'+yy+'</option>';
  ys.innerHTML=o;
  var mm=''; for(var i=0;i<12;i++) mm+='<option value="'+i+'"'+(i===cpCalViewMonth?' selected':'')+'>'+cpGetMonthName(i)+'</option>';
  ms.innerHTML=mm;
}
function cpCalSetYM(){ var ys=document.getElementById('cpYearSel'), ms=document.getElementById('cpMonthSel'); if(!ys||!ms) return; cpCalViewYear=parseInt(ys.value,10)||cpCalViewYear; cpCalViewMonth=parseInt(ms.value,10)||cpCalViewMonth; cpRenderCal(cpParseDDMMYYYY(cpCalTarget?cpCalTarget.value:'')); }
function cpCalPick(d){
  var val=cpFmtDDMMYYYY(cpCalViewYear,cpCalViewMonth,d);
  if(cpCalTarget){ cpCalTarget.value=val; cpCalTarget.dispatchEvent(new Event('input',{bubbles:true})); }
  cpCloseCalendar();
}
function cpCalPickToday(){ var n=new Date(); cpCalViewYear=n.getFullYear(); cpCalViewMonth=n.getMonth(); cpCalPick(n.getDate()); }
function cpRenderCal(selected){
  var weekContainer=document.getElementById('cpCalWeek'); if(weekContainer) weekContainer.innerHTML=cpGetWeekDays().map(function(w){return '<span>'+w+'</span>';}).join('');
  var titleEl=document.getElementById('cpCalTitle'); if(titleEl) titleEl.textContent=cpCalViewYear+'-'+cpPad(cpCalViewMonth+1);
  cpCalBuildYM();
  var firstDow=new Date(cpCalViewYear,cpCalViewMonth,1).getDay();
  var daysInMonth=new Date(cpCalViewYear,cpCalViewMonth+1,0).getDate();
  var today=new Date();
  var maxDate=null; if(cpCalTarget&&cpCalTarget.getAttribute('data-max')){ var mp=cpParseDDMMYYYY(cpCalTarget.getAttribute('data-max')); if(mp) maxDate=new Date(mp.y,mp.m,mp.d,0,0,0,0); }
  var minDate=null; if(cpCalTarget&&cpCalTarget.getAttribute('data-min')){ var np=cpParseDDMMYYYY(cpCalTarget.getAttribute('data-min')); if(np) minDate=new Date(np.y,np.m,np.d,0,0,0,0); }
  var html='';
  for(var i=0;i<firstDow;i++) html+='<button type="button" class="empty" disabled></button>';
  for(var d=1; d<=daysInMonth; d++){
    var cls=[], thisDate=new Date(cpCalViewYear,cpCalViewMonth,d);
    var isDisabled=(maxDate&&thisDate.getTime()>maxDate.getTime())||(minDate&&thisDate.getTime()<minDate.getTime());
    if(selected&&selected.y===cpCalViewYear&&selected.m===cpCalViewMonth&&selected.d===d) cls.push('selected');
    if(today.getFullYear()===cpCalViewYear&&today.getMonth()===cpCalViewMonth&&today.getDate()===d) cls.push('today');
    if(isDisabled) cls.push('disabled');
    if(isDisabled) html+='<button type="button" class="'+cls.join(' ')+'" disabled>'+d+'</button>';
    else html+='<button type="button" class="'+cls.join(' ')+'" onclick="cpCalPick('+d+')">'+d+'</button>';
  }
  var grid=document.getElementById('cpCalGrid'); if(grid) grid.innerHTML=html;
}
function cpCalGoPrev(){ cpCalViewMonth--; if(cpCalViewMonth<0){ cpCalViewMonth=11; cpCalViewYear--; } cpRenderCal(cpParseDDMMYYYY(cpCalTarget?cpCalTarget.value:'')); }
function cpCalGoNext(){ cpCalViewMonth++; if(cpCalViewMonth>11){ cpCalViewMonth=0; cpCalViewYear++; } cpRenderCal(cpParseDDMMYYYY(cpCalTarget?cpCalTarget.value:'')); }
function cpCalDoClear(){ if(cpCalTarget){ cpCalTarget.value=''; cpCalTarget.dispatchEvent(new Event('input',{bubbles:true})); } cpCloseCalendar(); }
document.addEventListener('click', function(e){
  var popup=document.getElementById('cpCalPopup');
  if(!popup||!popup.classList.contains('show')) return;
  if(popup.contains(e.target)) return;
  if(Date.now()-cpCalOpenedAt<120) return;
  if(cpCalTarget){
    if(cpCalTarget===e.target) return;
    var wrap=cpCalTarget.parentNode;
    if(wrap&&wrap.classList&&wrap.classList.contains('cp-date-input-wrapper')&&wrap.contains(e.target)) return;
  }
  cpCloseCalendar();
});

localize(); document.title=it('g_title'); loadCfg(); loadHouses(); syncParamUI(); schedule(); renderAll(); initSplitter();
window.ganttSetLang=function(lang){ window.CUR_LANG=lang; try{ if(window.parent && window.parent!==window) window.parent.CUR_LANG=lang; }catch(e){} document.title=it('g_title'); localize(); renderAll(); };
