# Quy tắc Agent — đồ án Nhập môn Big Data

## Đọc đầu phiên và xác định phạm vi

1. Đọc `README.md` và `STATE.md`, kiểm tra trạng thái Git và diff liên quan trước khi sửa.
2. Đọc milestone hiện được giao trong `requirements-review/14_MILESTONE_CHECKLIST.md` và phần tương ứng của file `13_MASTER_IMPLEMENTATION_PLAN.md`. Chỉ mở hồ sơ liên quan; không yêu cầu người dùng đọc lại toàn bộ tài liệu.
3. Thực hiện đúng mốc/task được giao. Cập nhật trạng thái theo bằng chứng, bàn giao rồi dừng ở ranh giới được giao; không tự mở milestone sau.

Ngôn ngữ giao tiếp và tài liệu là tiếng Việt. Ưu tiên đúng yêu cầu, toàn vẹn dữ liệu, giải pháp đơn giản và miễn phí cho hai laptop Windows 11/RAM 16 GB/50 GB trống theo người dùng. CPU, kiến trúc, phiên bản và khả năng full run chưa được xác minh.

## Nguồn và quyết định

- Chỉ dẫn hiện tại của người dùng có ưu tiên cao nhất. `07_CONFIRMED_SCOPE.md` giữ xác nhận U; bảng áp dụng đầu RTM giải thích điều chỉnh yêu cầu nguồn. Ghi quyết định quan trọng vào hồ sơ hiện có, không chỉ giữ trong chat.
- Hai file Word nguồn và `01_REQUIREMENT_MATRIX.md` cung cấp yêu cầu truy vết. Không sửa câu nguồn, 282 ID hoặc trọng số để khớp một thiết kế. Nếu không đọc được nguồn, nói rõ giới hạn.
- File 11/12 là đặc tả/thiết kế có phần đề xuất; sự tồn tại của tài liệu không chứng minh đã được duyệt hoặc triển khai. File 13/14/15 là kế hoạch, không phải evidence PASS.
- Audit trong file 10 và `requirements-review/evidence/` là quan sát lịch sử; không đổi nhãn thành Spark runtime hoặc số liệu chính sách mới đã chạy.
- Không hỏi lại các lựa chọn đã chốt. Tự giải quyết chi tiết kỹ thuật trong phạm vi đã duyệt; nếu phải đổi kiến trúc, protocol, schema có ảnh hưởng lớn hoặc scope, trình phương án cụ thể và chờ quyết định trước phần phụ thuộc.

## Phạm vi và quy tắc dữ liệu phải giữ

- Stack: PySpark local, FP-Growth, MongoDB, Spring Boot/MVC/Thymeleaf. Batch chạy riêng; không fit Spark trên từng HTTP request, không tự thêm service Python, SPA, cloud/cluster hoặc tính năng bán hàng.
- P-01: chỉ giữ lần đầu của tuple tám giá trị nguồn giống nhau, trên cả hai sheet và trong từng sheet; thứ tự sheet nguồn rồi số dòng. Không dedup bằng Invoice/StockCode hoặc thứ tự đọc DB. File nguồn giữ nguyên; archive nguồn có thể giữ phần lặp để truy vết.
- P-02/U-21: loại phí/dịch vụ/điều chỉnh, Manual, voucher và TEST001/TEST002 khỏi khai phá/gợi ý theo mapping có căn cứ. Giữ hàng hóa có mã chữ; không lọc hàng loạt bằng regex mã hàng.
- P-03: luật thuần so với baseline phổ biến, ẩn một item từ giỏ đánh giá; Recall@K và tỷ lệ có gợi ý. Rank confidence, lift, support rồi tie-break ổn định; không fallback mặc định. K/seed/mốc chia/tham số chưa chốt; không tạo ngưỡng đạt hoặc buộc FP-Growth thắng baseline.
- Full run trên cả hai máy không cho phép fit từ tập test. Mỗi máy cần minh chứng thật riêng; PASS một máy, dữ liệu mẫu hoặc imported output không thay nghiệm thu máy kia.
- TV1/người dùng lead data/Spark/đánh giá; TV2 lead Java/web/tích hợp; hai người review chéo. Không tự gán việc đã làm hoặc phần trăm đóng góp từ phân công.

## Ranh giới hiện tại và nghiệm thu

Trạng thái cụ thể đọc từ `STATE.md`. Bước chuẩn bị repository không đóng M0. M0 review scope/hợp đồng dữ liệu, không cài stack/tạo DB/viết app. Chỉ thực hiện M1 sau khi M0 đủ AC/DoD và có chỉ dẫn giao việc phù hợp.

Không cần runtime PASS để đóng một review tài liệu M0; vẫn cần quyết định và review theo AC/DoD. Chưa biết deadline/giờ tuần không chặn review M0 nhưng chặn kết luận kịp hạn. Không thay review hai thành viên bằng review của Agent.

Khi thay đổi: kiểm chứng đúng phạm vi, đọc diff cuối và phân biệt tài liệu, audit độc lập, fixture/prototype, full-source pipeline và acceptance thực tế. Ghi kết quả, điều chưa kiểm chứng và căn cứ trước khi tick; không tick chỉ vì file đã tồn tại hoặc build xanh.

## An toàn repository và môi trường

- Giữ thay đổi người dùng; không reset/clean/revert, xóa nguồn, drop DB hoặc ghi đè secrets khi chưa được cho phép rõ ràng.
- Không tự commit/push, tạo remote hoặc thay Git config toàn máy. Nếu được giao commit, chỉ stage file thuộc task; commit không bao hàm push.
- Dữ liệu lớn, output, DB files, môi trường và secrets phải nằm ngoài Git; kiểm tra `.gitignore` và diff. Ví dụ cấu hình chỉ có placeholder, không chứa thông tin thật.
- Không cài/nâng cấp phần mềm toàn máy hoặc dựng hạ tầng để chữa lỗi khi chưa có phạm vi phù hợp. Khi M1 được giao, kiểm tra phiên bản thực tế và tài liệu chính thức trước khi chọn bộ tương thích.
- Tìm bằng `rg`, đọc các phần liên quan; không quét hoặc in cấu hình bí mật. Không khởi chạy tiến trình nền/GUI cho bước chuẩn bị này.
- Dùng ngày theo ngữ cảnh thời gian của người dùng; trạng thái có ngày thật, không biến ước lượng lịch hoặc giờ-người thành việc đã làm.

## Cập nhật và bàn giao

`STATE.md` giữ trạng thái ngắn và việc kế tiếp; checklist 14 giữ nghiệm thu milestone; file 07 giữ quyết định người dùng. Cập nhật các tài liệu này khi nội dung thay đổi, không tạo roadmap hay ghi chú song song trùng chức năng.

Bàn giao nêu thay đổi, quyết định, kiểm chứng và giới hạn. Không tự ghi chi tiết môi trường máy thứ hai hoặc xác nhận giảng viên mà chưa có nguồn. Không đưa thông tin cá nhân/secrets vào log kiểm tra.
