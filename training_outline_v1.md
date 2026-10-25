# Tài liệu đào tạo hệ thống Choice Slats VN
# Choice 越南漏缝地板生产管理系统 · 培训资料大纲
# Training Manual Outline — Choice Slats VN Production Management System

> **Ghi chú ngôn ngữ / 语言说明 / Language note**: Bản chính dùng tiếng Việt. Các thuật ngữ then chốt ghi kèm tiếng Trung + English trong ngoặc. (正文越南语为主，关键术语附中/英对照。)
> **Đối tượng / 培训对象 / Audience**: Toàn bộ vai trò — nhân viên nhập liệu, kế toán, quản lý. (全覆盖：录入人员 / 财务 / 管理层)
> **Mục tiêu / 页数目标 / Page target**: ≥ 40–50 trang, mỗi chương có sơ đồ luồng dữ liệu + ảnh chụp thực tế (giao diện thật, dữ liệu demo/脱敏).

---

## MỤC LỤC / 目录 / Table of Contents
1. Tổng quan & Đăng nhập (系统概览与登录)
2. Phân quyền PERM-V2 (权限体系)
3. Sản xuất – Tổng quan & Kế hoạch (Tab A, B) (生产概况与计划)
4. Sản xuất hàng ngày (Tab E) (每日生产)
5. Lắp đặt – Nhân công/Thời tiết/Sản lượng (Tab C lắp đặt) (安装管理·人工天气安装量)
6. Kho nguyên liệu & Xác nhận nhập hàng (Tab D / D区) (原料库存与收货确认)
7. Nhân sự & Thiết bị (Tab C người / Tab F) (人员与设备)
8. Tài chính & Báo cáo (财务 / 中国报表 / 权益报表) (财务报表)
9. Trung tâm Phê duyệt (审批中心)
10. Bảng điều khiển Dashboard (看板)
11. Bảo vệ dữ liệu & Sao lưu (数据保护与备份)
+ Phụ lục: Bảng thuật ngữ 3 ngôn ngữ (三语术语表)

---

## CHƯƠNG 1 — Tổng quan & Đăng nhập
### 1.1 Kiến trúc hệ thống (系统架构)
- `choice_lite.html` (tệp đơn / 单文件应用) + `app.py` (backend Flask, cổng 5050 / 端口5050).
- Dữ liệu là **nguồn sự thật duy nhất tại máy chủ** (server is single source of truth).
### 1.2 Đăng nhập (登录)
- Truy cập `http://127.0.0.1:5050/`, tài khoản admin `tom` / mật khẩu `66668888`.
- Vai trò (role): admin / edit / view. tom = quyền edit toàn hệ thống.
### 1.3 Chuyển ngôn ngữ (语言切换)
- Nút chuyển zh / en / vi (sự kiện `app:langchange`), áp dụng cho toàn bộ nhãn (labels).
### 1.4 Cấu trúc điều hướng (导航结构)
- Menu模块: Sản xuất (Production), Lắp đặt (Install), Tài chính (Finance), Dashboard, Phê duyệt (Approval), Thư viện (Library).
### Ảnh chụp计划 (Screenshot plan): Màn hình đăng nhập, menu chính, bộ chuyển ngôn ngữ.
### Luồng dữ liệu (Data flow): Đăng nhập → lấy `refreshAuthFromServer` + `startPermWatch` → áp dụng quyền theo dự án.

## CHƯƠNG 2 — Phân quyền PERM-V2
### 2.1 Nguyên tắc (原则)
- Chưa được cấp = **ẩn** (unauthorized = hidden). Dự án có thể "Hiển thị toàn bộ" (whole-project show).
- Quyền theo **id dự án** (project id), không theo对象. Hàm `_curPid(v)` chuẩn hóa.
### 2.2 Quyền báo cáo tài chính & quyền chỉ đọc (财务权限与只读)
- Báo cáo quyền lợi (equity) khóa chỉ đọc toàn bảng (EQ-RO-LOCK).
### 2.3 Phạm vi ngày nhập liệu (录入日期范围)
- Ngày sản xuất ≤ hôm nay (ngày tương lai bị khóa / future dates disabled).
### Ảnh: Bảng phân quyền, dự án bị ẩn/hiện.
### Luồng: Phân quyền → lọc tại `loadWon()` → ẩn tab/theo dự án.

## CHƯƠNG 3 — Sản xuất: Tổng quan & Kế hoạch (Tab A, B)
### 3.1 Tab A Tổng quan (概况)
- Thẻ tổng hợp, liên kết với dự án CRM `globalWonData` (签约项目).
### 3.2 Tab B Kế hoạch sản xuất (生产计划)
- `pg_prep_start` / `pg_prep_end` cho phép ngày tương lai (排产可用未来日期 — ngoại lệ duy nhất).
- Gan biểu đồ Gantt (甘特图) bỏ qua ngày lễ VN (`BOARD_HOLIDAYS`).
### 3.3 Tab G Bàn giao (交付) — đưa vào chương này
- Ghi nhận bàn giao sản phẩm hoàn thành.
### 3.4 Tab H Tồn kho thành phẩm & Xuất kho (成品库存与出库明细) — đưa vào chương này hoặc 4
- Ràng buộc **xuất ≤ sản lượng** (出库量≤产量): `out ≤ produced`, không âm (防负库存).
### Luồng: Kế hoạch B → sinh ngày sản xuất E → tồn kho H → báo cáo tài chính.

## CHƯƠNG 4 — Sản xuất hàng ngày (Tab E) ⭐ Trọng tâm
### 4.1 Chế độ chỉ đọc / chỉnh sửa (只读/编辑模式)
- Ngày **đã lưu = chỉ đọc** (read-only); ngày chưa có dữ liệu = vào chế độ nhập (edit).
- Nút "Sửa" (编辑) mở form; sau lưu → `PROD_PE_EDIT_MODE=false` về chỉ đọc.
### 4.2 Viên nang chuồng & hộp nhập (猪舍胶囊 ↔ 输入框联动)
- Viên nang sáng = `line.houses` = ô nhập hiển thị (三类不变量: không hiển thị input khi bỏ chọn / không dùng `prod_houseSpecMap` / đồng bộ `.on`).
### 4.3 Khóa thời tiết (天气时间锁) ⏱
- Sáng chỉ hiện sau **09:00**, chiều chỉ sau **14:00** (上午9点后/下午14点后).
- Hàm `prod_wxDisplay(slot, wx, dateDmy)`.
### 4.4 Sao chép dòng 1→2/3/4 (复用线1)
- Nếu dòng đích **đã có dữ liệu → không ghi đè** (保护: 跳到卡片, focus input).
### 4.5 Thu gọn bằng double-click (双击空白收起)
- Chỉnh sửa → double-click vùng trống → thu gọn về chỉ đọc.
### 4.6 Lưu & truyền (保存与传递)
- `prod_saveProduction` → `prod_pushToServer` → `PUT /api/prod-factory/<id>`.
### Ảnh: Tab E ở chế độ chỉ đọc + chế độ nhập; viên nang chuồng; khóa thời tiết.
### Luồng (Data flow E):
`Nhập E (line/houses/qty/weather)` → `PROD_PE_DRAFT` (local) → `prod_saveProduction` → `PUT server` → `prod_factory_<id>` (nguồn sự thật) → `prod_stockOutSection` (H: produced-out) → `Tài chính`.

## CHƯƠNG 5 — Lắp đặt: Nhân công / Thời tiết / Sản lượng (Tab C lắp đặt)
### 5.1 Chế độ chỉ đọc / chỉnh sửa (同 Tab E)
- Đã lưu = chỉ đọc; "Sửa" → nhập; lưu → `INST_TAB_C_EDIT_MODE=false`.
### 5.2 Thẻ khu vực (区域卡片) & nhóm lắp đặt (安装小组)
- `inst_zoneCardHtml` / `inst_zoneCardReadOnlyHtml`; `zoneTeams`.
### 5.3 Nhập nhanh từ ngoài (外部快速录入)
- `inst_quickInstallEntry` → vào chế độ sửa, ngày = hôm nay, focus ô "lắp đặt hôm nay".
### 5.4 Khóa chống xóa (防清零)
- `inst_saveWorkers` ghi `w.zones = zones.filter(...)`; `inst_workerZones` fallback.
### Ảnh: Tab C lắp đặt, thẻ khu vực, nhập nhanh.
### Luồng: Lắp đặt C → `prod_factory_<id>.workers/zoneTeamWorkers` → báo cáo lắp đặt / Dashboard tiến độ.

## CHƯƠNG 6 — Kho nguyên liệu & Xác nhận nhập hàng (Tab D / D区) ⭐
### 6.1 Bảng nhập nhiều dòng (多行录入表格)
- Cột: vật liệu / quy cách (dropdown + ✎, lưu `prod_specs_<vật liệu>`) / đơn vị / đơn giá VND + RMB/USD (tự tính) / số lượng / thành tiền / ghi chú / thao tác.
### 6.2 Ba loại tiền tệ (三币种)
- Đơn giá RMB/USD là **chỉ đọc**, tự tính từ `#w_rate_rmb_vnd` / `#w_rate_usd_vnd`.
### 6.3 Ngày nhập & ảnh (到货日期与照片)
- Ngày nhập ≤ hôm nay; ảnh chụp hàng nhận.
### 6.4 Quy trình phê duyệt (审批流)
- Gửi `POST /api/approval-requests` (block `PROD-RECEIPT`, người duyệt = 采购经理).
- Duyệt (通过) → `prodApprApplyInbound` → **nhập kho** (过账入库, status=confirmed).
- Từ chối (驳回) → status=returned, có thể gửi lại.
### Ảnh: Bảng D区, hộp xác nhận 3 ngôn ngữ, trung tâm phê duyệt.
### Luồng: Nhập D区 → `receipt{rows,status}` → `prod_factory_<id>` → `POST approval` → Trung tâm phê duyệt → nhập kho → tồn kho nguyên liệu → sản xuất.

## CHƯƠNG 7 — Nhân sự & Thiết bị (Tab C người / Tab F)
### 7.1 Tab C Nhân sự ngày (人员·日)
- 11 vai trò (PROD_WORKERS): quản đốc (manager), thợ sửa máy (machinist), thợ hàn (welder)…; nhật ký thời tiết sáng/chiều.
### 7.2 Tab F Thiết bị & Sự cố (设备与故障)
- Ghi nhận hỏng hóc, bảo trì.
### Ảnh: Tab C nhân sự, Tab F thiết bị.
### Luồng: Nhân sự/Thiết bị → `prod_factory_<id>` → chi phí → báo cáo tài chính.

## CHƯƠNG 8 — Tài chính & Báo cáo ⭐
### 8.1 Báo cáo tài chính (财务报表)
- Univer bảng, sao chép Ctrl+C/X/V (màn hình hiển thị / 屏幕显示文本), cuộn ngang Excel.
- Bảng Undo/Redo 10 bước (FIN-UNDO-LEDGER).
### 8.2 Báo cáo Trung Quốc (中国报表) — `cn_report.xlsx`
- Tiền tệ gốc = VND; mặc định hiển thị = RMB.
- Ba khối đồng nhất (D/E cơ sở, N/O Trung, X/Y Anh).
- Nút **Ẩn bản ghi đã đối chiếu** (隐藏核销记录, FIN-CN-HIDE-CHECKED).
- Khóa `FIN-CN-STAT-LOCK`: thống kê chọn vùng, lưu không mất.
### 8.3 Báo cáo quyền lợi (股东权益报表 / Equity)
- Univer独立实例 `#equity_container`, `unitId=equity-report`.
- Cột tiền tệ bên **trái** (货币符号在数值左侧), chuyển đổi tỷ giá (汇率) theo `/api/fx-rates`.
- Xóa hàng bằng Delete (框选删除).
### Ảnh: 3 báo cáo, nút ẩn核销, thanh tỷ giá.
### Luồng: Nhập chứng từ / báo cáo → `/api/finance/*` → xlsx → Dashboard & in ấn.

## CHƯƠNG 9 — Trung tâm Phê duyệt (审批中心)
### 9.1 Danh sách yêu cầu (审批请求列表)
- `approval-requests` theo block (VD `PROD-RECEIPT`).
### 9.2 Thao tác (操作)
- Xem/Sửa (duyệt sửa số lượng, đơn giá) / Duyệt (通过) / Từ chối (驳回).
### Luồng: Tạo tại D区 → hiện tại Trung tâm → Duyệt → quay về module gốc cập nhật.

## CHƯƠNG 10 — Bảng điều khiển Dashboard (看板)
### 10.1 Bản đồ & nhãn tỉnh (地图与省标签)
- Hiện tỉnh có dự án + Hà Nội / TP.HCM (红点/红色).
### 10.2 Ảnh hiện trường, lịch, TOP10, tiến độ lắp đặt, giá vật liệu, tỷ giá (现场图/日历/TOP10/安装进度/材料价/汇率)
### Luồng: Tổng hợp từ `prod_factory_*`, `finance_data` → biểu đồ thời gian thực.

## CHƯƠNG 11 — Bảo vệ dữ liệu & Sao lưu (数据保护)
### 11.1 Nguyên tắc (原则)
- Máy chủ là nguồn sự thật; cổng chống lùi (防回退闸): nếu chỉ số < 65% → giữ bản server (`stale`).
### 11.2 Lịch sử & Khôi phục (历史与恢复)
- Nút "🛡 Dữ liệu bảo vệ" (`prod_protectOpen`): xem phiên bản, khôi phục (回滚), sao lưu ngay.
### 11.3 Sao lưu tự động (自动备份)
- `backups/auto/` giữ 80 bản; mỗi 30 phút + khi khởi động.
### Luồng: Mọi `PUT` → lưu lịch sử 10 bản + sao lưu → khôi phục khi cần.

---

## PHỤ LỤC — Bảng thuật ngữ 3 ngôn ngữ (三语术语表)
| Tiếng Việt | 中文 | English |
|---|---|---|
| Viên nang chuồng | 猪舍胶囊 | Shed capsule |
| Khóa thời tiết | 天气时间锁 | Weather time-lock |
| Quyền lợi | 股东权益 | Equity |
| Xác nhận nhập hàng | 收货确认 | Receiving confirmation |
| Nguồn sự thật duy nhất | 唯一事实源 | Single source of truth |
| Chế độ chỉ đọc | 只读模式 | Read-only mode |

---

## KẾ HOẠCH ẢNH CHỤP MÀN HÌNH (截图计划 — Playwright)
1. Cài extension/script Playwright, mở headless Chromium.
2. Đăng nhập `tom/66668888` vào `http://127.0.0.1:5050/`.
3. Duyệt từng Tab, **nhập dữ liệu demo/脱敏** vào các trường then chốt trước khi chụp (không ảnh hưởng dữ liệu thật — dùng dự án demo hoặc trường đã làm mờ).
4. Lưu ảnh vào `training_shots/`, chèn vào đúng chương.
5. Mỗi chương ≥ 2–4 ảnh → đảm bảo tính sinh động.

## SƠ ĐỒ TỔNG THỂ (端到端数据流向总图 — chèn ở đầu hoặc cuối)
```
[Nhập liệu: E/C/D/finance] 
   → PROD_MEM (local, localStorage)
   → prod_save / PUT /api/prod-factory/<id>
   → MÁY CHỦ (nguồn sự thật, prod_factory + prod_kv)
        ├─→ Tồn kho H / Nguyên liệu D / Lắp đặt C
        ├─→ Tài chính (xlsx: VN/CN/Equity) → In/Export
        ├─→ Dashboard (map, TOP10, tiến độ, tỷ giá)
        └─→ Trung tâm Phê duyệt (PROD-RECEIPT…) → Duyệt → cập nhật module
   ↔ Sao lưu auto (80 bản) + Khôi phục (🛡)
```

---
*Dự kiến độ dài / Estimated length*: Chương 4,6,8 chiếm nhiều trang nhất (trọng tâm nhập liệu & báo cáo). Tổng ≥ 40–50 trang khi hoàn thiện ảnh + bản đầy đủ.
*Bước tiếp theo / Next step*: Bạn duyệt outline → tôi cài Playwright, chụp ảnh thực tế (giao diện thật + dữ liệu demo/脱敏), viết bản đầy đủ, xuất PDF.
