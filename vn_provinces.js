// 越南省份坐标（看板地图省级闪光 + 按省取天气）
// ★ 省份清单与「编辑模态框 provinceOptionsHtml()」完全一致：2025 年合并后的 34 个省市。
//   三语名称（vi/zh/en）也与下拉中的 ['Hà Nội','河内市','Hanoi City'] 对应，保证看板与表单显示一致。
//   历史数据中若存的是旧省名，通过 VN_PROV_ALIAS 自动映射到新省（坐标照旧可用）。
window.VN_PROVINCES = [
  { vi:'Hà Nội',          zh:'河内市',   en:'Hanoi City',         lat:21.03, lng:105.85 },
  { vi:'Hải Phòng',       zh:'海防市',   en:'Hai Phong City',     lat:20.86, lng:106.68 },
  { vi:'Huế',             zh:'顺化市',   en:'Hue City',           lat:16.46, lng:107.60 },
  { vi:'Đà Nẵng',         zh:'岘港市',   en:'Da Nang City',       lat:16.05, lng:108.20 },
  { vi:'TP. Hồ Chí Minh', zh:'胡志明市', en:'Ho Chi Minh City',   lat:10.82, lng:106.63 },
  { vi:'Cần Thơ',         zh:'芹苴市',   en:'Can Tho City',       lat:10.03, lng:105.77 },
  { vi:'Cao Bằng',        zh:'高平省',   en:'Cao Bang Province',  lat:22.67, lng:106.26 },
  { vi:'Tuyên Quang',     zh:'宣光省',   en:'Tuyen Quang Province',lat:21.82, lng:105.21 },
  { vi:'Điện Biên',       zh:'奠边省',   en:'Dien Bien Province', lat:21.39, lng:103.02 },
  { vi:'Lai Châu',        zh:'莱州省',   en:'Lai Chau Province',  lat:22.39, lng:103.06 },
  { vi:'Sơn La',          zh:'山罗省',   en:'Son La Province',    lat:21.33, lng:103.91 },
  { vi:'Lào Cai',         zh:'老街省',   en:'Lao Cai Province',   lat:22.48, lng:103.97 },
  { vi:'Thái Nguyên',     zh:'太原省',   en:'Thai Nguyen Province',lat:21.59, lng:105.85 },
  { vi:'Lạng Sơn',        zh:'谅山省',   en:'Lang Son Province',  lat:21.85, lng:106.76 },
  { vi:'Quảng Ninh',      zh:'广宁省',   en:'Quang Ninh Province',lat:21.01, lng:107.29 },
  { vi:'Bắc Ninh',        zh:'北宁省',   en:'Bac Ninh Province',  lat:21.18, lng:106.07 },
  { vi:'Phú Thọ',         zh:'富寿省',   en:'Phu Tho Province',   lat:21.32, lng:105.40 },
  { vi:'Hưng Yên',        zh:'兴安省',   en:'Hung Yen Province',  lat:20.79, lng:106.07 },
  { vi:'Ninh Bình',       zh:'宁平省',   en:'Ninh Binh Province', lat:20.25, lng:105.97 },
  { vi:'Thanh Hóa',       zh:'清化省',   en:'Thanh Hoa Province', lat:19.80, lng:105.77 },
  { vi:'Nghệ An',         zh:'义安省',   en:'Nghe An Province',   lat:18.68, lng:105.68 },
  { vi:'Hà Tĩnh',         zh:'河静省',   en:'Ha Tinh Province',   lat:18.34, lng:105.90 },
  { vi:'Quảng Trị',       zh:'广治省',   en:'Quang Tri Province', lat:17.48, lng:106.60 },
  { vi:'Quảng Ngãi',      zh:'广义省',   en:'Quang Ngai Province',lat:15.12, lng:108.79 },
  { vi:'Gia Lai',         zh:'嘉莱省',   en:'Gia Lai Province',   lat:13.99, lng:108.00 },
  { vi:'Khánh Hòa',       zh:'庆和省',   en:'Khanh Hoa Province', lat:12.25, lng:109.18 },
  { vi:'Đắk Lắk',         zh:'得乐省',   en:'Dak Lak Province',   lat:12.71, lng:108.24 },
  { vi:'Lâm Đồng',        zh:'林同省',   en:'Lam Dong Province',  lat:11.94, lng:108.44 },
  { vi:'Đồng Nai',        zh:'同奈省',   en:'Dong Nai Province',  lat:10.95, lng:106.82 },
  { vi:'Tây Ninh',        zh:'西宁省',   en:'Tay Ninh Province',  lat:11.31, lng:106.10 },
  { vi:'Đồng Tháp',       zh:'同塔省',   en:'Dong Thap Province', lat:10.45, lng:105.63 },
  { vi:'Vĩnh Long',       zh:'永隆省',   en:'Vinh Long Province', lat:10.25, lng:106.00 },
  { vi:'An Giang',        zh:'安江省',   en:'An Giang Province',  lat:10.38, lng:105.44 },
  { vi:'Cà Mau',          zh:'金瓯省',   en:'Ca Mau Province',    lat:9.18,  lng:105.15 }
];
// 重点城市（地图白点 + 三语标注）
window.VN_CITIES = [
  { vi:'Hà Nội',          zh:'河内',     en:'Hanoi',            lat:21.03, lng:105.85 },
  { vi:'Hải Phòng',       zh:'海防',     en:'Hai Phong',        lat:20.86, lng:106.68 },
  { vi:'Đà Nẵng',         zh:'岘港',     en:'Da Nang',          lat:16.05, lng:108.20 },
  { vi:'TP. Hồ Chí Minh', zh:'胡志明市', en:'Ho Chi Minh City', lat:10.82, lng:106.63 },
  { vi:'Cần Thơ',         zh:'芹苴',     en:'Can Tho',          lat:10.03, lng:105.77 }
];
// 越南国界近似轮廓（[lng,lat]，视觉示意用，非精确边界）
window.VN_OUTLINE = [
  [102.14,22.43],[103.0,22.83],[103.9,22.56],[104.5,22.83],[105.3,23.39],[106.7,22.83],[107.97,21.55],
  [107.0,20.8],[106.2,20.4],[106.0,19.8],[105.7,19.2],[106.3,18.3],[106.6,17.5],[107.1,16.98],[107.6,16.4],
  [108.25,15.9],[108.9,15.1],[109.3,13.8],[109.32,13.1],[109.27,12.4],[108.99,11.57],[109.2,11.3],
  [108.1,10.93],[107.0,10.4],[106.7,10.3],[106.5,9.9],[106.2,9.5],[106.0,9.4],[105.7,9.2],[105.0,8.9],
  [104.8,8.6],[104.8,9.5],[104.9,10.0],[105.1,10.4],[105.43,10.7],[105.6,11.0],[106.1,11.3],[106.6,11.7],
  [107.2,12.0],[107.55,12.3],[107.6,12.9],[107.4,13.8],[107.2,14.6],[107.3,15.3],[107.1,16.0],[106.6,16.75],
  [105.3,17.4],[104.7,18.5],[104.1,19.2],[104.0,19.9],[104.2,20.7],[103.7,21.0],[103.3,21.6],[102.7,21.9]
];
window.VN_MAP = { W:1000, H:620, latMin:8.5, latMax:23.5, lngMin:102.0, lngMax:110.0 };
window.vnProject = function(lat, lng) {
  var M = window.VN_MAP;
  var x = (lng - M.lngMin) / (M.lngMax - M.lngMin) * M.W;
  var y = (M.latMax - lat) / (M.latMax - M.latMin) * M.H;
  return { x: +x.toFixed(1), y: +y.toFixed(1) };
};
// 省名归一化：去声调/去符号/转小写
window._vnProvNorm = function(s) {
  return String(s || '').toLowerCase()
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .replace(/đ/g, 'd')
    .replace(/[^a-z0-9]/g, '');
};
// 旧省名（2025 合并前）-> 新省名 key，用于兼容历史数据
window.VN_PROV_ALIAS = {
  bacgiang:'bacninh', backan:'thainguyen', haiduong:'haiphong', baclieu:'camau',
  bentre:'vinhlong', binhduong:'tphochiminh', binhdinh:'gialai', binhphuoc:'dongnai',
  binhthuan:'lamdong', kontum:'quangngai', daknong:'lamdong',
  hagiang:'tuyenquang', hanam:'ninhbinh', namdinh:'ninhbinh', hoabinh:'phutho', vinhphuc:'phutho',
  haugiang:'cantho', soctrang:'cantho', kiengiang:'angiang',
  longan:'tayninh', ninhthuan:'khanhhoa', phuyen:'daklak', quangbinh:'quangtri', quangnam:'danang',
  thaibinh:'hungyen', thuathienhue:'hue', tiengiang:'dongthap', travinh:'vinhlong', yenbai:'laocai',
  baria:'tphochiminh', vungtau:'tphochiminh', bariavungtau:'tphochiminh',
  hochiminh:'tphochiminh', tphcm:'tphochiminh', hcm:'tphochiminh', saigon:'tphochiminh', hue:'hue'
};
// 按任意写法的省名查找省份记录（先精确/归一化匹配 34 省，再走旧名映射），找不到返回 null
window.vnProvinceByKey = function(name) {
  if (!name) return null;
  var k = window._vnProvNorm(name);
  var list = window.VN_PROVINCES || [];
  for (var i = 0; i < list.length; i++) { if (window._vnProvNorm(list[i].vi) === k) return list[i]; }
  var a = window.VN_PROV_ALIAS[k];
  if (a) { for (var j = 0; j < list.length; j++) { if (window._vnProvNorm(list[j].vi) === a) return list[j]; } }
  return null;
};
