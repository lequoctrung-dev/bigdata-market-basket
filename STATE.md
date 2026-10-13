# Trạng thái dự án

Cập nhật: **14/10/2026**. Đây là trạng thái điều phối; chỉ tick milestone theo tiêu chí và evidence trong [checklist](requirements-review/14_MILESTONE_CHECKLIST.md).

## Phạm vi giao việc hiện tại

Người dùng yêu cầu chuẩn bị môi trường workspace/Agent **trước khi thực hiện M0**: Git, cấu trúc thư mục, AGENTS.md và theo dõi trạng thái. Dừng sau bàn giao chuẩn bị; chưa thực hiện review/đóng M0 hoặc mở M1.

## Những gì đã có và đã kiểm tra

- Hồ sơ `requirements-review/01–15`, bản trích nguồn và audit dữ liệu đã có trước bước chuẩn bị. Thiết kế là bản đề xuất; chưa được coi là hợp đồng kỹ thuật đã nghiệm thu.
- Git cài sẵn: `2.52.0.windows.1`; đã khởi tạo repository cục bộ nhánh `main`. Chưa stage, commit, remote hoặc push; chưa cấu hình danh tính commit.
- Đã thêm README, AGENTS, STATE, `.gitignore`, `.gitattributes` và các vị trí trống cho sản phẩm/công cụ/báo cáo. Chưa có mã ứng dụng trong `pipeline/` hoặc `web/`.
- Đã kiểm tra loại dataset/output/build/môi trường/secrets khỏi Git; hồ sơ yêu cầu và file Word nguồn vẫn được Git nhận diện. Kiểm tra này không xác nhận mọi file tương lai đều không chứa bí mật.
- Đã đối chiếu SHA-256 sau chuẩn bị: hai Word nguồn, XLSX/ZIP nguồn, RTM, Source Audit và Source Extract không đổi.
- Các liên kết tài liệu chuẩn bị trỏ đến file hiện có; không lấy cấu trúc thư mục hoặc Git init làm minh chứng hệ thống chạy.

## Trạng thái milestone

| Mốc | Trạng thái hiện tại |
| --- | --- |
| Chuẩn bị workspace/Agent, ngoài các milestone học thuật | Đã chuẩn bị và kiểm tra cục bộ; không thay M0 |
| M0 — Chốt phạm vi và hợp đồng dữ liệu | Chưa nghiệm thu. Quyết định chính đã có; còn hoàn thiện hợp đồng và review hai thành viên |
| M1–M8 | Chưa thực hiện; không có evidence nghiệm thu runtime hoặc nộp bài |

## Quyết định và giới hạn hiện tại

- Stack/dataset/giỏ/Thymeleaf/P-01–P-03, loại TEST, batch/MongoDB, roles, full run hai máy và khung báo cáo đã chốt: [U-01–U-26](requirements-review/07_CONFIRMED_SCOPE.md).
- Dataset và cấu trúc báo cáo được GV chấp thuận **theo xác nhận người dùng**; không phải Agent đã đọc thông báo độc lập.
- Cả hai Windows 11/RAM 16 GB/50 GB trống theo người dùng. CPU/kiến trúc/Java/Python/MongoDB/Maven và bộ Spark/connector chưa kiểm chứng; chưa cài đặt hoặc khởi động dịch vụ trong bước này.
- Deadline, giờ/tuần, lịch bận và quy cách nộp chi tiết chưa rõ. Không hỏi lại khi chưa có thông tin mới; không cam kết đủ thời gian.
- Raw source giữ nguyên; count audit cũ trước quyết định loại TEST không phải số liệu pipeline mới. Không biến audit Python thành Spark PASS.
- Git chưa có bản lịch sử hoặc bản sao từ xa; Git init chưa tạo bản sao lưu. Chọn remote/commit khi người dùng giao việc, không chặn M0.
- Chưa chuẩn bị/kiểm chứng workspace hoặc Git trên laptop thứ hai; không suy trạng thái máy này sang máy kia.

## Việc kế tiếp khi được giao M0

1. Rà soát phạm vi và các xác nhận đã có, không yêu cầu duyệt lại các lựa chọn đã chốt.
2. Hoàn thiện quy ước input/output, collection/khóa, tiền/ngày/ID, trách nhiệm batch/web, manifest/công bố và KPI/màn hình tối thiểu trong file 11/12.
3. Trình ngắn gọn các lựa chọn lớn còn cần quyết định; hai thành viên review hợp đồng và ghi kết quả theo M0-AC1/AC2/AC3, DoD.
4. Chỉ tick M0 khi đủ căn cứ; sau đó mới nhận việc M1 để kiểm tra môi trường runtime và chạy mẫu hai máy.

Task/AC/DoD cụ thể: [M0 trong Master Plan](requirements-review/13_MASTER_IMPLEMENTATION_PLAN.md). Tiến độ và các ô nghiệm thu: [Milestone Checklist](requirements-review/14_MILESTONE_CHECKLIST.md).
