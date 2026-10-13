# Trạng thái dự án

Cập nhật: **14/10/2026**. Đây là trạng thái điều phối; chỉ tick milestone theo tiêu chí và evidence trong [checklist](requirements-review/14_MILESTONE_CHECKLIST.md).

## Phạm vi giao việc hiện tại

Đã hoàn tất giao việc **M0 — Chốt phạm vi làm việc và hợp đồng dữ liệu**, M0-T1–M0-T4, ngày 14/10/2026. Agent hoàn thiện tài liệu, người dùng chọn M0-D1/D2/D3 theo U-27–U-29 và xác nhận cả TV1/TV2 đã review, chấp thuận bản hiện tại theo U-30. **M0 đã đóng về tài liệu theo AC/DoD; dừng sau bàn giao, chưa giao/mở M1.**

## Những gì đã có và đã kiểm tra

- Hồ sơ `requirements-review/01–15`, bản trích nguồn và audit dữ liệu đã có trước bước chuẩn bị. File 11/12 được bổ sung M0, lựa chọn U-27–U-29 và review hai thành viên theo xác nhận U-30; contract m0-contract-v1 đã nghiệm thu về tài liệu, chưa runtime.
- Git cài sẵn: `2.52.0.windows.1`; repository nhánh `main` hiện có commit `760cf88` — `prepare project workspace and agent instructions`, và remote `origin` là `https://github.com/lequoctrung-dev/bigdata-market-basket.git`. Đây là quan sát Git cục bộ khi bàn giao ngày 14/10/2026; chưa kiểm tra trạng thái GitHub qua mạng. Agent không thực hiện commit/push trong bước bàn giao.
- Đã thêm README, AGENTS, STATE, `.gitignore`, `.gitattributes` và các vị trí trống cho sản phẩm/công cụ/báo cáo. Chưa có mã ứng dụng trong `pipeline/` hoặc `web/`.
- Đã kiểm tra loại dataset/output/build/môi trường/secrets khỏi Git; hồ sơ yêu cầu và file Word nguồn vẫn được Git nhận diện. Kiểm tra này không xác nhận mọi file tương lai đều không chứa bí mật.
- Đã đối chiếu SHA-256 sau chuẩn bị: hai Word nguồn, XLSX/ZIP nguồn, RTM, Source Audit và Source Extract không đổi.
- Các liên kết tài liệu chuẩn bị trỏ đến file hiện có; không lấy cấu trúc thư mục hoặc Git init làm minh chứng hệ thống chạy.
- M0: đã đối chiếu scope/U/RTM/report/deliverables/map và audit có sẵn; file 11 bổ sung bài toán/mục tiêu/giá trị, tập dữ liệu, mapping loại TEST và công thức KPI; file 12 bổ sung input/output/kiểu/khóa/manifest/công bố/retry/lỗi và các giả định M1. File 13 giữ phân công/khung ghi việc thật và kết quả M0; checklist 14 đã ghi receipt và tick AC/DoD theo U-30.
- Kiểm tra tài liệu là evidence của Agent, không phải review của TV1/TV2, Spark runtime hoặc full run. Không tái khảo sát toàn nguồn, cài stack, tạo DB/index hay viết ứng dụng trong M0.

## Trạng thái milestone

| Mốc | Trạng thái hiện tại |
| --- | --- |
| Chuẩn bị workspace/Agent, ngoài các milestone học thuật | Đã chuẩn bị và kiểm tra cục bộ; không thay M0 |
| M0 — Chốt phạm vi và hợp đồng dữ liệu | Đã đóng về tài liệu ngày 14/10/2026; AC1/AC2/AC3/DoD theo lựa chọn U-27–U-29, đối chiếu văn bản và review TV1/TV2 được người dùng xác nhận U-30 |
| M1–M8 | Chưa thực hiện; không có evidence nghiệm thu runtime hoặc nộp bài |

## Quyết định và giới hạn hiện tại

- Stack/dataset/giỏ/Thymeleaf/P-01–P-03, loại TEST, batch/MongoDB, roles, full run hai máy và khung báo cáo đã chốt: [U-01–U-26](requirements-review/07_CONFIRMED_SCOPE.md).
- Dataset và cấu trúc báo cáo được GV chấp thuận **theo xác nhận người dùng**; không phải Agent đã đọc thông báo độc lập.
- **M0-D1/D2/D3 đã chọn — U-27–U-29** ở [file 07](requirements-review/07_CONFIRMED_SCOPE.md): chín collection/run bất biến/con trỏ active/version; decimal text tại MongoDB; dashboard hàng hóa + audit toàn nguồn/gói KPI/ba khu vực. Review toàn contract đã được người dùng xác nhận cho cả TV1/TV2 theo U-30; không phải runtime PASS hoặc thông báo trực tiếp riêng từ TV2.
- Cả hai Windows 11/RAM 16 GB/50 GB trống theo người dùng. CPU/kiến trúc/Java/Python/MongoDB/Maven và bộ Spark/connector chưa kiểm chứng; chưa cài đặt hoặc khởi động dịch vụ trong bước này.
- Deadline, giờ/tuần, lịch bận và quy cách nộp chi tiết chưa rõ. Không hỏi lại khi chưa có thông tin mới; không cam kết đủ thời gian.
- Raw source giữ nguyên; count audit cũ trước quyết định loại TEST không phải số liệu pipeline mới. Không biến audit Python thành Spark PASS.
- Git đã có lịch sử cục bộ và remote; không suy trạng thái hiện tại trên GitHub chỉ từ cấu hình remote. Thread mới kiểm tra lại branch/status/diff/log; không tự commit/push.
- Chưa chuẩn bị/kiểm chứng workspace hoặc Git trên laptop thứ hai; không suy trạng thái máy này sang máy kia.

## Ranh giới bàn giao và việc kế tiếp

1. M0 đã đóng; Agent dừng sau bàn giao. Các lựa chọn U-01–U-30 không hỏi lại; QD-07/QD-09 vẫn mở, không cam kết lịch hoặc kịp hạn.
2. Khi người dùng giao **M1 — Học Spark cần dùng và kiểm chứng luồng mẫu trên hai máy**, mới kiểm tra môi trường/bộ phiên bản và chạy mẫu từng máy theo AC/DoD của mốc đó. Chưa cài stack, tạo DB/index hoặc viết prototype trong M0.
3. Giữ giả định precision/scale/mapper/ngày local/ranking/retry và counts policy TEST cần kiểm chứng ở đúng milestone; nghiệm thu tài liệu M0 không thay sample/full-source/two-machine acceptance.

Task/AC/DoD cụ thể: [M0 trong Master Plan](requirements-review/13_MASTER_IMPLEMENTATION_PLAN.md). Tiến độ và các ô nghiệm thu: [Milestone Checklist](requirements-review/14_MILESTONE_CHECKLIST.md).
