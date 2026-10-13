# Kiến thức cần hiểu trước thiết kế và triển khai

Danh sách này là **đề xuất chuẩn bị kiến thức**, không phải tiêu chí chấm bổ sung hoặc lịch học/triển khai. **Cập nhật theo U-09:** nhóm đã chọn PySpark local + FP-Growth + MongoDB + Spring Boot. Các công nghệ khác chỉ tham khảo khi có nhu cầu; phân tích mức học chi tiết nằm trong [file 09](09_TECHNICAL_ADVISORY_RESEARCH.md).

## Kiến thức gắn trực tiếp với yêu cầu đã nêu

| ID | Kiến thức cần hiểu | Cần giải thích được điều gì trước khi thiết kế | Căn cứ từ yêu cầu |
| --- | --- | --- | --- |
| KN-01 | Phân tích bài toán dữ liệu và giới hạn phạm vi | Ai dùng kết quả, câu hỏi thực tế cần trả lời, đầu vào/đầu ra và giá trị dự kiến; phân biệt điều làm trong đồ án với hướng phát triển | B-S01–B-S07; A-C04–A-C09; B tr.1 II.2; A tr.9 Mở đầu |
| KN-02 | Khái niệm dữ liệu lớn và đặc trưng của bộ dữ liệu thực tế | Quy mô, định dạng, cấu trúc, thuộc tính và các tính chất khiến công nghệ Big Data phù hợp; không gọi dữ liệu “lớn” chỉ vì công cụ có tên Big Data | B-D02–B-D07; B tr.1 II.2 |
| KN-03 | Vai trò lưu trữ, xử lý và phân tích dữ liệu | Phân biệt nơi dữ liệu được lưu, công cụ thực thi xử lý và kỹ thuật tạo kết quả; hiểu vai trò của công nghệ dự kiến chọn | B-G07, B-T01–B-T06; B tr.1–2 II.1–II.2 |
| KN-04 | Dữ liệu/schema và ý nghĩa thuộc tính | Một bản ghi là gì, trường nào có ý nghĩa gì, quan hệ và cấu trúc dữ liệu, định dạng đầu vào/đầu ra | B-D04–B-D06, B-P19, B-E05–B-E06; B tr.1–2 II.2 và tr.4 IV |
| KN-05 | Khảo sát dữ liệu và chất lượng dữ liệu | Cách nhận biết thiếu, trùng, ngoại lệ, không nhất quán; phân biệt lỗi dữ liệu với dữ liệu hợp lệ hiếm; lý do giữ/sửa/loại bản ghi | B-D08–B-D14; B tr.1 II.2 |
| KN-06 | Tiền xử lý và biến đổi dữ liệu | Dữ liệu phải được biến đổi thế nào để phù hợp bài toán/kỹ thuật và vì sao; dữ liệu đầu vào sau xử lý có ý nghĩa gì | B-D10, B-D15, B-P27–B-P28; B tr.1 II.2 và tr.4 IV |
| KN-07 | Kiến trúc và luồng dữ liệu | Các thành phần lưu/xử lý/hiển thị trao đổi dữ liệu ra sao, dữ liệu đi từ nguồn đến kết quả thế nào, vì sao chọn công nghệ đó | B-T01–B-T05; B tr.2 II.2 |
| KN-08 | Mô hình hoặc kỹ thuật xử lý đã chọn | Ý tưởng, đầu vào, đầu ra, tham số, giả định và giới hạn của kỹ thuật; các ví dụ MapReduce/RDD/DataFrame/Streaming là phương án, không phải mọi nhóm phải dùng hết | B-T06, B-P10–B-P12, B-E03; B tr.2 II.2 và tr.3 IV |
| KN-09 | Thực nghiệm và baseline | Baseline nghĩa là gì với bài toán, điều kiện thực nghiệm, dữ liệu, tham số và môi trường nào tạo ra kết quả; baseline cụ thể chờ chốt | B-E01–B-E07, B-P13–B-P14; B tr.2 II.2 và tr.4 IV |
| KN-10 | Đánh giá và so sánh kết quả | Độ đo phản ánh khía cạnh nào, đối tượng so sánh là gì, nhận xét nào được dữ liệu hỗ trợ và giới hạn nào còn tồn tại | B-V01–B-V05; B tr.2 II.2 |
| KN-11 | Trực quan hóa dữ liệu và diễn giải giá trị | Biểu đồ/bảng/dashboard/notebook thể hiện điều gì, người đọc có thể rút ra thông tin nào, cách tránh diễn giải vượt quá dữ liệu | B-F01–B-F02; B tr.2 II.2 |
| KN-12 | Cài đặt và vận hành sản phẩm | Điều kiện môi trường, tham số và các bước cần thiết để chạy từ đầu vào đến đầu ra; có thể giải thích quá trình demo | B-E03–B-E07, B-O05–B-O06, B-N03; B tr.2 II.2–II.3 |
| KN-13 | Viết báo cáo khoa học và sử dụng nguồn | Phân biệt lời mô tả, kết quả thực nghiệm, giả định, hạn chế và đề xuất; tổng hợp tài liệu và dẫn nguồn thực tế thay vì copy ví dụ | B-L01–B-L04, B-A01–B-A04, A-C01–A-C24; B tr.1 I, tr.4 Lưu ý; A tr.3, 9–16 |
| KN-14 | Word cho báo cáo học thuật | Styles, cấp đề mục, caption, mục lục/danh mục tự động, section để đánh số trang, spacing/margin, repeat header rows | A-F001–A-F067; A tr.17–18 thể thức và tr.5, 7–8 |
| KN-15 | Hồ sơ nhóm, thuyết trình và phản biện | Vai trò/công việc/đóng góp, lịch nhóm, ai làm gì và có thể giải thích kết quả; hiểu rubric chấm nhưng không tự tính điểm bằng số checkbox | B-O07–B-O08, B-R02–B-R03, B-P33–B-P39, B-RUB01–B-RUB14; B tr.2–4 |

## Kiến thức chỉ cần khi lựa chọn đề tài hoặc kỹ thuật tương ứng

| Lựa chọn có điều kiện | Kiến thức nên hiểu | Nguồn/quan hệ với yêu cầu |
| --- | --- | --- |
| Đề tài phân tích mua sắm và mua kèm | Cấu trúc hóa đơn/giỏ hàng, tập phổ biến, luật kết hợp, FP-Growth và cách dùng luật để gợi ý | B-H01–B-H09; đề tài đã chọn/duyệt theo U-01, FP-Growth đã chọn theo U-09. |
| MongoDB đã chọn; HDFS chỉ tham khảo | Document/collection, kiểu dữ liệu, khóa/index, đọc/ghi giữa Python và Java; dữ liệu/kết quả theo lần chạy, tránh nạp trùng hoặc hiển thị kết quả chưa hoàn chỉnh | B-H02; B-T01/B-T05; U-09. MongoDB cần hiểu đủ triển khai, không yêu cầu dùng HDFS đồng thời. |
| PySpark local đã chọn | DataFrame/Spark SQL, làm sạch, gom giỏ, FP-Growth và MongoDB Connector; hiểu phiên bản Scala/Spark/connector và tài nguyên local | B-H03–B-H06; B-T06; U-09. |
| Website Spring Boot đã chọn | Spring MVC, Spring Data MongoDB, kiểm tra đầu vào, truy vấn/giới hạn kết quả, áp dụng luật đã khai phá; HTML/Thymeleaf đã chọn theo U-12 | B-F01–B-F02; B-R07–B-R08; U-03/U-09. Không tự thêm JWT, thanh toán hoặc SPA. |
| Chọn phân lớp, hồi quy, phân cụm, lọc cộng tác, đồ thị hoặc kỹ thuật khác | Giả định, đầu vào, tham số, đầu ra và đánh giá của đúng kỹ thuật chọn; chưa mặc định mọi đề tài cần “huấn luyện” một mô hình ML | B tr.2 II.2; B-T06; AMB-08 |
| Chọn streaming hoặc dữ liệu theo thời gian | Phải hiểu cách kỹ thuật đã chọn xử lý đầu vào theo thời gian và đánh giá kết quả; đây là kiến thức theo lựa chọn, không là yêu cầu thêm streaming | B tr.2 II.2 nêu Spark Streaming như ví dụ |

## Các nội dung bổ sung nên hiểu nhưng chưa được nguồn quy định

Đây là đề xuất riêng, không đưa vào RTM như yêu cầu của tài liệu:

- **Tái lập kết quả**: biết lưu phiên bản dữ liệu, môi trường, tham số và đầu ra để có thể giải thích vì sao một lần chạy cho kết quả đó. Nguồn yêu cầu mô tả môi trường/tham số và hướng dẫn chạy, nhưng không quy định checksum, lockfile, log hay một công cụ cụ thể.
- **Tính toàn vẹn dữ liệu**: hiểu việc thay đổi kiểu dữ liệu, lọc/ghép bản ghi có thể làm thay đổi ý nghĩa kết quả; đề xuất đối chiếu trước/sau ở mức cần thiết cho bài toán.
- **Nguồn dữ liệu và quyền sử dụng**: hiểu điều kiện sử dụng dữ liệu, cách ghi nguồn và xử lý thông tin cá nhân nếu dataset thực tế tạo nhu cầu. Hai file không quy định một thủ tục pháp lý/ẩn danh cụ thể; không tự gọi đó là yêu cầu đã được GV đặt.
- **So sánh công bằng**: hiểu vì sao các kết quả so sánh cần có điều kiện được giải thích. Nguồn yêu cầu so sánh nhưng chưa quy định số lần thử, train/test, seed hay độ đo; không tự áp đặt các yếu tố này cho mọi loại đề tài.
- Nếu chọn luật kết hợp, có thể tìm hiểu **support, confidence, lift** để đọc và giải thích luật. Đây là đề xuất kiến thức của người rà soát, không phải các độ đo hoặc ngưỡng đã được File B bắt buộc.

Đề tài, local, website và stack đã chốt theo U-01/U-03/U-05/U-09; dataset khảo sát/cách chọn giỏ/MVC–Thymeleaf theo U-10–U-12. Cả hai đã học các nền tảng nhưng chưa học Spark theo U-13; cả hai máy cần demo U-15. Trước thiết kế chi tiết còn cần dữ liệu được duyệt, schema/kiểu dữ liệu, bộ phiên bản và giao thức đánh giá; xem [quyết định còn lại](04_AMBIGUITY_CONFLICT_LOG.md). Không hỏi lại các lựa chọn đã xác nhận.

