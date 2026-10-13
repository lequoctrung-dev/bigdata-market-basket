# Rà soát yêu cầu đồ án Nhập môn Big Data

**Điểm vào workspace:** [README gốc](../README.md), [trạng thái hiện tại](../STATE.md), [quy tắc Agent](../AGENTS.md). Ngày 14/10/2026 đã chuẩn bị repository/Agent trước M0; chưa thực hiện hoặc đóng M0, chưa mở M1.

Bộ hồ sơ phân tích yêu cầu cho nhóm **2 sinh viên**, rà soát nguồn ngày **12/10/2026**, cập nhật xác nhận, khảo sát và lựa chọn kỹ thuật ngày **13/10/2026**. Đã đọc và đối chiếu đủ **22 trang, 4 bảng và 3 vị trí ảnh**. Stack đã chọn; đã có thiết kế đề xuất và Master Plan. Chưa triển khai, cài đặt sản phẩm hoặc xác nhận lịch/năng lực làm việc.

Có **282 dòng truy vết từ A/B**, gồm nghĩa vụ trực tiếp, điều kiện, mẫu/hướng dẫn, mục tiêu năng lực và quy tắc chấm. Không coi tất cả là yêu cầu bắt buộc hoặc dùng số checkbox để tự tính điểm. Có **29 mục trong log**; trạng thái hiện tại đã được cập nhật theo câu trả lời của người dùng, không còn mặc định 27 mục đều cần hỏi lại.

**Đã chốt:** đề tài/stack/MVC–Thymeleaf/chọn giỏ/P-01/P-02/P-03; U-20 giữ nguồn MongoDB và phân tích unique, web kết quả hoàn chỉnh; loại TEST; **cả hai tự full run**; **bạn data/Spark, người còn lại Java/web**. GV chấp thuận dataset và khung B/quy cách A theo người dùng. Cả hai Windows 11/RAM 16 GB/50 GB trống theo thông tin cung cấp; CPU/versions/runtime chưa kiểm chứng. Deadline/giờ tuần chưa rõ. Không cần đọc lại toàn hồ sơ: xem phần cuối checklist 14.

## Các đầu ra

| Đầu ra | Nội dung |
| --- | --- |
| [Requirement Matrix](01_REQUIREMENT_MATRIX.md) | 282 ID; nguồn file/trang/mục/đoạn; mức áp dụng; điểm khi được nêu; tiêu chí đối chiếu; minh chứng dự kiến; liên kết vấn đề |
| [Report Structure Checklist](02_REPORT_STRUCTURE_CHECKLIST.md) | Khung B, cấu trúc mẫu A, trường bìa, nội dung học thuật và từng quy định định dạng; chưa tự ghép thành cấu trúc bắt buộc |
| [Deliverables Checklist](03_DELIVERABLES_CHECKLIST.md) | 34 mục hồ sơ/sản phẩm/nộp/demo, giữ mốc trong nguồn và phần chưa rõ |
| [Ambiguity and Conflict Log](04_AMBIGUITY_CONFLICT_LOG.md) | 29 mục; phân biệt vấn đề nguồn với trạng thái hiện tại và các quyết định còn lại |
| [Kiến thức trước thiết kế](05_KNOWLEDGE_BEFORE_DESIGN.md) | Kiến thức gắn với yêu cầu; phần chỉ học khi chọn kỹ thuật; đề xuất bổ sung được tách rõ |
| [Source Audit](06_SOURCE_AUDIT.md) | Đối chiếu từng trang/phần/bảng; thống kê độ phủ; quan sát mẫu; giới hạn xác nhận |
| [Bản trích nguồn](SOURCE_EXTRACT.md) | 278 đoạn có văn bản, vị trí trang, câu gốc và ánh xạ yêu cầu/ngữ cảnh |
| [Phạm vi đã xác nhận](07_CONFIRMED_SCOPE.md) | 26 xác nhận U-01–U-26; cách demo/stack và P-01/P-02/P-03 đã chốt |
| [Đánh giá dataset](08_DATASET_EVALUATION.md) | 4 lựa chọn ban đầu; Online Retail II đã chọn để khảo sát; vai trò thành phần |
| [Tư vấn kỹ thuật và kiến thức](09_TECHNICAL_ADVISORY_RESEARCH.md) | Knowledge Gap Analysis, 5 phương án so sánh, SOL-05 đã chọn, ưu/nhược điểm, nguồn học, rủi ro và thử nghiệm |
| [Khảo sát dữ liệu thực tế](10_DATASET_PROFILE.md) | Đọc đủ 2 sheet/1.067.371 dòng, schema/thiếu/trùng/hủy/giỏ và đoạn giới thiệu để trình duyệt dataset |
| [Đặc tả và quyết định](11_SPECIFICATION_DRAFT.md) | P-01 chỉ giữ lần đầu; P-02/P-03 đã chọn; phần KPI/bố cục còn đề xuất |
| [Thiết kế kỹ thuật đề xuất](12_TECHNICAL_DESIGN.md) | Luồng batch, collection/kiểu dữ liệu, chọn đúng dòng đầu, công bố kết quả, website và kiểm chứng hai máy |
| [Master Implementation Plan](13_MASTER_IMPLEMENTATION_PLAN.md) | M0–M8, task/phụ thuộc/phân công đề xuất, ước lượng, báo cáo song song và quyết định cần duyệt |
| [Milestone Checklist](14_MILESTONE_CHECKLIST.md) | Bảng theo dõi ngắn; toàn bộ milestone triển khai chưa được tick |
| [Requirement–Milestone Map](15_REQUIREMENT_MILESTONE_MAP.md) | Ánh xạ đủ 282 ID nguồn vào mốc dự kiến/điều kiện áp dụng; không phải kết quả nghiệm thu |

## Các điểm cần chốt trước khi dựa vào để thiết kế

- **Cấu trúc báo cáo**: U-26 chốt khung B + quy cách trình bày A theo người dùng; không tự bắt đủ 5 chương/trang nhận xét/chữ ký hoặc in của A.
- **Hạn nộp cuối**: chưa có ngày giờ cụ thể. Các mốc hai giai đoạn trong B được giữ làm dấu vết nguồn; U-08 đã thay bằng nộp một lần cuối.
- **Công nghệ, dữ liệu và sản phẩm**: stack đã chọn theo U-09; thiết kế chi tiết và bộ phiên bản còn cần kiểm chứng. U-03 yêu cầu website, U-05 cho local/không có ngưỡng dataset. Việc chọn MongoDB/Spark/FP-Growth của nhóm không biến toàn bộ gợi ý trong File B thành quy định chung.
- **Đánh giá**: B:P018 yêu cầu độ đo phù hợp, phân tích, so sánh, giải thích và hạn chế. B:P147 có baseline trong lịch cũ; U-05 không đặt baseline/độ đo cụ thể, chưa có ngưỡng đạt. Giữ đánh giá có căn cứ, không thêm tiêu chí chấm.
- **Rubric/nộp/demo**: điểm các tiêu chí đã rõ; công thức tỷ lệ đáp ứng, cách đóng gói tài liệu kèm và thời lượng demo chưa rõ. Không cần hỏi tỷ trọng hai giai đoạn cho cách nộp hiện tại.

## Điều tài liệu quy định và đề xuất của người rà soát

**Điều nguồn quy định** được ghi trong cột nội dung/nguồn/mức áp dụng của RTM. Mẫu minh họa và mục tiêu năng lực không bị đổi thành nghĩa vụ bắt buộc. Các giá trị số về lề, font, spacing, số người và rubric đều lấy từ nguồn.

**Đề xuất riêng** gồm cách đối chiếu nghiệm thu, loại minh chứng có thể dùng, cách giải quyết điểm mơ hồ và kiến thức bổ sung trong file 05. Ví dụ: lưu xác nhận duyệt, ghi điều kiện thực nghiệm để tái lập, đối chiếu dữ liệu trước/sau và chọn hình thức sản phẩm nhỏ nhất được GV chấp nhận. Không xem các đề xuất này là yêu cầu đã được tài liệu/GV xác nhận. Không tạo trọng số/độ đo/ngưỡng bắt buộc mới.

## Cách dùng

**Đọc nhanh khi chuẩn bị triển khai:** bảng đầu file 13 và checklist file 14; quyết định đã chốt/điểm kỹ thuật còn kiểm chứng ở cuối file 13. File 15 chỉ tra cứu truy vết. **Hồ sơ dữ liệu/thiết kế:** file 10 cho kết quả dữ liệu, file 11 cho quyết định đã chốt, phần đầu/cuối file 12 cho thiết kế và giới hạn xác minh. File 07 giữ xác nhận hiện tại; file 09 là tài liệu tra cứu kiến thức, không bắt buộc đọc hết để tiếp tục; RTM giữ căn cứ và điều kiện từ A/B, kèm bảng điều chỉnh áp dụng ở đầu. Dùng checklist khi chuẩn bị hồ sơ. Các ô chưa tick không phải kết luận FAIL. Không cần trả lời lại đề tài, local, quy mô tối thiểu, website hoặc nộp giai đoạn 1; vấn đề còn lại được thu thập ở bước cần dùng.

Hai file Word nguồn được giữ nguyên. Các PDF/ảnh và dữ liệu trong evidence chỉ phục vụ kiểm tra đọc nguồn; không phải báo cáo đồ án hoặc minh chứng hệ thống đã chạy.



Các quyết định QD-01–QD-06 đã giải quyết theo U-20–U-26; phần kỹ thuật chi tiết phải kiểm chứng, không phải hỏi lại lựa chọn. Master Plan đã đổi vai trò và tăng M6 cho full run cả hai; tổng ước lượng mới 196–296 giờ-người, khoảng 236–356 gồm dự phòng, chưa cam kết deadline.

