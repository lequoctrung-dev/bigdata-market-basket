# Đặc tả bài toán — quyết định đã chốt và chi tiết còn đề xuất

Ngày: **13/10/2026**. Căn cứ: [RTM](01_REQUIREMENT_MATRIX.md), [U-01–U-26](07_CONFIRMED_SCOPE.md), [khảo sát thực tế](10_DATASET_PROFILE.md).

**Bạn chỉ cần đọc phần này và phần cuối:**
- Đã chốt dataset khảo sát, stack, MVC/Thymeleaf, chọn giỏ nhận gợi ý và cả hai máy đều demo.
- Dữ liệu đã kiểm tra đủ hai sheet; GV chấp thuận dataset và khung B/quy cách A theo người dùng U-25/U-26.
- **P-01/P-02/P-03 đã chốt U-16–U-18**; P-01 chỉ giữ lần đầu, thay phương án max(n1,n2). Các KPI, bố cục và chi tiết khác chưa tự được duyệt toàn bộ.
- U-20–U-26 chốt hướng lưu dữ liệu, loại TEST, full run hai máy, đổi vai trò và báo cáo. Field/config chi tiết cần kiểm chứng, chưa tạo schema/API hoặc cài môi trường; không hỏi lại các lựa chọn.

Các mã IN/OUT/CL/EV/P chỉ tổ chức dự thảo, không phải Requirement ID mới. Điều kiện đối chiếu dưới đây là cách kiểm tra đề xuất, không phải ngưỡng chấm điểm.

## 1. Đầu vào

| Mã | Đầu vào dự thảo | Đối chiếu nguồn/xác nhận |
| --- | --- | --- |
| IN-01 | Hai sheet của XLSX Online Retail II, giữ file nguồn và thông tin sheet/dòng để truy vết. | B-D01–B-D06; B-O02; U-10 |
| IN-02 | Invoice và StockCode dùng dạng định danh chuỗi; Quantity, InvoiceDate, Price, Customer ID và Country theo schema thực tế. | B-D05/B-D06/B-D15; file 10 |
| IN-03 | Giỏ demo là tập một/nhiều StockCode do người xem chọn; tên chỉ để hiển thị, mã là khóa. | B-H09; U-11 |
| IN-04 | Tham số khai phá và đánh giá được ghi cùng lượt chạy; chưa chốt support/confidence/K/mốc chia/seed. | B-E03/B-E04; B-V01–B-V05 |

Giỏ rỗng hoặc mã không có trong danh mục cần thông báo rõ. Item chọn trùng chỉ tính một lần. Giới hạn input và phân trang sẽ được thiết kế theo dữ liệu/thử nghiệm, không tự đặt thành SLA hay rubric.

## 2. Đầu ra và tương tác đề xuất

| Mã | Đầu ra / thao tác | Đối chiếu và cách kiểm tra dự kiến |
| --- | --- | --- |
| OUT-01 | Tóm tắt dữ liệu: nguồn, khoảng thời gian, số dòng/giỏ/item trước và sau từng quy tắc; số lỗi và lý do loại khỏi từng phân tích. | B-D08–B-D15; B-E05/B-E06; không cộng lỗi chồng nhau thành tổng loại. |
| OUT-02 | Phân tích theo tháng: số hóa đơn mua, phân phối số item duy nhất/giỏ, item phổ biến theo số giỏ và lượng bán. | B-H08; B-F01/B-F02. Các KPI này là đề xuất; mẫu số và lọc item phải đi cùng số hiển thị. |
| OUT-03 | Giá trị dòng giao dịch mua dương bằng Quantity × Price, GBP, nếu đưa vào dashboard. | B-H08; file 10. Chưa gọi là doanh thu ròng/lợi nhuận; giải thích giữ/loại trùng và hủy/điều chỉnh. |
| OUT-04 | Tập phổ biến: item và số giỏ; luật: tiền đề, kết luận, support/confidence/lift; kèm cấu hình và số giỏ khai phá. | B-H05/B-H06; B-T06; B-E03/B-E06. Đối chiếu ví dụ tính tay và lượt chạy. |
| OUT-05 | Gợi ý mua kèm cho giỏ chọn: mã/tên item, luật làm căn cứ và chỉ số; loại item đã có, không trùng ứng viên. | B-H09; U-11. Tiền đề phải có đủ; không gọi confidence là xác suất riêng cho người xem. |
| OUT-06 | Kết quả so sánh và giới hạn; thời gian/tài nguyên đo thực tế theo bước khi chạy sau này. | B-V01–B-V05; B-E04/B-E07; chưa có kết quả thực nghiệm. |
| OUT-07 | Website MVC/Thymeleaf hiển thị các nhóm kết quả trên; cả hai máy đều cần demo. | B-F01/B-F02/B-N03; U-12/U-15. Bố cục/biểu đồ còn thiết kế, không biến bảy nhóm đầu ra thành bảy màn hình bắt buộc. |

Đề xuất ba khu vực điều hướng: **Tổng quan/phân tích**, **Tập phổ biến và luật**, **Gợi ý theo giỏ**. Đây là bố cục dự thảo; không thêm đăng nhập/thanh toán, quản lý đơn hoặc cá nhân hóa theo tài khoản.

## 3. Quy tắc xử lý đề xuất, chưa áp dụng vào nguồn

| Mã | Quy tắc dự thảo | Căn cứ / ảnh hưởng |
| --- | --- | --- |
| CL-01 | Giữ XLSX gốc; nhập có thông tin nguồn, sheet và dòng. Định danh chuẩn hóa thành chuỗi nhưng vẫn bảo toàn giá trị nguồn. | B-D05/B-D06/B-O02; mã có số và chữ trong file thực tế. |
| CL-02 | **Đã chốt:** chỉ giữ dòng đầu tiên cho bộ tám giá trị nguồn giống nhau trong toàn workbook; thứ tự sheet gốc rồi số dòng. Bỏ các lần lặp sau trong dữ liệu phân tích; giữ nguồn. | B-D12; U-16. Không dedup theo Invoice hoặc Invoice + StockCode vì có thể xóa dòng khác số lượng/giá/thời gian. |
| CL-03 | Giỏ mua xét dòng không có Invoice bắt đầu C, Quantity > 0, Price > 0, mã/ngày hợp lệ. Dòng hủy/điều chỉnh/giá 0 vẫn giữ ở nguồn và thống kê chất lượng. | B-D09/B-D12–B-D15; không suy rằng mọi dòng Quantity âm đều là trả hàng đã xác định. |
| CL-04 | Không loại khỏi giỏ chỉ vì thiếu Customer ID. Thống kê riêng liên quan khách chỉ dùng ID không rỗng và nêu mẫu số. | B-D11; 243.007 dòng thiếu ID; demo đã chọn theo giỏ. |
| CL-05 | **Đã chốt P-02:** loại phí/dịch vụ/điều chỉnh, Manual và voucher khỏi khai phá/gợi ý; phân loại theo mapping có căn cứ, không dựa regex năm chữ số. | B-D14/B-D15; U-17. ADJUST2/B và m có mô tả điều chỉnh/Manual, ghi rõ trong audit; U-21 đã chọn loại TEST001/TEST002 khỏi khai phá/gợi ý, giữ nguồn. |
| CL-06 | Sau xử lý nguồn, gom theo Invoice; mỗi StockCode duy nhất một lần cho FP-Growth. Quantity/Price vẫn dùng đúng ở bảng dòng hàng. | B-D15/B-H05; không xóa số lượng khỏi dữ liệu vì thuật toán dùng sự hiện diện. |
| CL-07 | Không prefix sheet để tách giỏ. Timestamp đại diện dự kiến là thời điểm nhỏ nhất trong hóa đơn; hóa đơn luôn thuộc một tập khi chia dữ liệu. | B-D05/B-D15/B-E05; 82 hóa đơn mua ứng viên có nhiều timestamp nhưng cùng ngày. Còn cần kiểm tra sau quy tắc làm sạch. |
| CL-08 | Danh mục hiển thị dự kiến chọn mô tả không rỗng phổ biến nhất của mã trong dữ liệu được phép; tie dùng quy tắc cố định, thiếu thì hiển thị mã. | B-F02/B-H09; có 1.214 mã nhiều mô tả. Không nối/tách sản phẩm chỉ dựa vào tên. |
| CL-09 | Chưa làm tròn tiền về hai chữ số tại bước nhập; cần giữ giá trị và chọn kiểu biểu diễn chính xác khi thiết kế Python–BSON–Java. | B-D06/B-D15; file chứa giá số thực. Timezone nguồn chưa biết, không tự coi timestamp là UTC. |
| CL-10 | Giữ giỏ lớn để khảo sát, ghi phân phối và tài nguyên; không tự cắt giỏ lớn/nhân bản dữ liệu. | B-D13/B-V05; giỏ ứng viên lớn nhất 1.110 mã, chưa loại phí. |

## 4. Khai phá và áp dụng luật

PySpark chạy batch và ghi kết quả MongoDB; Spring Boot đọc lượt hoàn chỉnh để phục vụ web. Schema/index và cách công bố lượt hoàn chỉnh chưa thiết kế.

Điều kiện áp dụng: toàn bộ tiền đề nằm trong giỏ; kết luận chưa có trong giỏ. Với nhiều luật gợi ý cùng item, chỉ trả một item và một căn cứ nhất quán.

**Thứ tự đã chọn theo P-03/U-18:** confidence giảm dần, rồi lift, support; nếu bằng nhau dùng mã item và tiền đề chuẩn hóa để kết quả ổn định. Một item nhiều luật dùng luật tốt nhất theo cùng thứ tự. Chưa đặt ngưỡng lift hoặc hứa luật này xếp hạng tốt hơn baseline. Không có luật thì hiển thị chưa có gợi ý; fallback phổ biến chưa đưa vào mặc định.

Support/confidence/lift phục vụ diễn giải luật; chất lượng gợi ý cần đánh giá riêng. [Spark FP-Growth](https://spark.apache.org/docs/4.2.0/ml-frequent-pattern-mining.html).

## 5. Phép đánh giá đã chọn theo P-03, giá trị cấu hình chưa chốt

| Mã | Phương pháp đề xuất | Điều kiện cần giữ |
| --- | --- | --- |
| EV-01 | Chia hóa đơn hoàn chỉnh theo thời gian thành lịch sử khai phá, phần phát triển chọn cấu hình và phần đánh giá cuối. | Mốc chia chưa chốt; cả hóa đơn ở một tập, không chia từng dòng hoặc học từ tập cuối. Danh mục/độ phổ biến chỉ dùng dữ liệu lịch sử được phép. |
| EV-02 | Giỏ đánh giá từ hai item trở lên: ẩn một item bằng quy tắc có seed cố định, phần còn lại là truy vấn. | Một item ẩn là lựa chọn giao thức, không yêu cầu nguồn. Giỏ một item báo riêng; item mới chưa có trong lịch sử được ghi nhận, không tự loại để làm đẹp điểm. |
| EV-03 | Baseline chọn item phổ biến theo số giỏ lịch sử, loại item đã có; so với luật cùng truy vấn, danh mục và K. | K/seed chưa chọn; không ép FP-Growth thắng. Thứ tự web và offline phải thống nhất. |
| EV-04 | Ưu tiên Recall@K và tỷ lệ truy vấn có gợi ý; Precision@K có thể bổ sung. | Với mục tiêu ẩn T và kết quả R tối đa K: recall = số item đúng / số item ẩn; precision đề xuất = số item đúng / K; tỷ lệ có gợi ý = truy vấn có ít nhất một kết quả / tổng truy vấn đánh giá. Khi T không rỗng mà R rỗng, recall/precision là 0. |
| EV-05 | Phân tích kết quả theo kích thước giỏ, item hiếm/mới và trạng thái không có luật; ghi thời gian đọc/khai phá/ghi và phục vụ web riêng. | Không suy offline thành tăng doanh thu, không suy profiling Python thành benchmark Spark hoặc hiệu năng máy thứ hai. |

Giao thức P-03 đã được nhóm chọn theo U-18 để hỗ trợ B-V01–B-V05/B-P13, không phải chỉ tiêu hoặc trọng số mới. [Spark ranking evaluation](https://spark.apache.org/docs/4.2.0/mllib-evaluation-metrics.html#ranking-systems).

## 6. Cả hai máy tự chạy toàn bộ dữ liệu

**Đã chốt U-22:** mỗi máy tự chạy full pipeline từ toàn bộ nguồn, xử lý/giỏ/thống kê, FP-Growth và đánh giá theo cấu hình đã freeze, rồi website demo. Fit trên phần lịch sử/train theo U-18; “toàn bộ dữ liệu” không cho phép đưa test vào train. Không cần cả hai lặp toàn bộ grid chọn cấu hình; nghiệm thu cùng cấu hình cuối.

Không dùng imported output thay receipt full run; sau batch có thể dừng Spark khi thao tác web. Theo U-24 cả hai Windows 11/RAM 16 GB/50 GB trống; CPU/kiến trúc, phần mềm và tài nguyên thực chưa kiểm chứng.

**Vai trò U-23:** TV1/người dùng lead data/Spark/evaluation, TV2 lead Java/web/tích hợp; review chéo và mỗi người chạy máy mình. Số giờ/tuần/deadline vẫn chưa rõ, không cam kết lịch.

## 7. Trạng thái các lựa chọn

| Mã | Quyết định hiện tại | Nội dung còn kiểm chứng |
| --- | --- | --- |
| **P-01 / U-16** | **Chỉ giữ lần xuất hiện đầu tiên** của bộ tám giá trị nguồn giống nhau, trên cả hai sheet. Không giữ phần lặp trong một sheet; đề xuất max(n1,n2) cũ hết áp dụng. | Mã nguồn sản phẩm sau này phải chọn dòng đầu bằng thứ tự nguồn tường minh, không dựa thứ tự partition/đọc DB. Audit ở file 10 chỉ là kiểm tra độc lập, chưa chạy Spark. |
| **P-02 / U-17** | Không gợi ý phí/dịch vụ/điều chỉnh; POST, DOT, C2, BANK CHARGES, AMAZONFEE, D, ADJUST, S; tách M/Manual và voucher khỏi khai phá. Giữ hàng hóa có mã chữ, không loại hàng loạt bằng regex. | Mapping thêm ADJUST2/B và m được ghi theo đúng mô tả điều chỉnh/Manual đã quan sát. TEST001/TEST002 đã chọn loại theo U-21; audit cũ trước quyết định này chưa phải counts cuối. Không tự xóa phí khỏi mọi thống kê. |
| **P-03 / U-18** | So sánh luật thuần/baseline phổ biến; giỏ ẩn một item, Recall@K/tỷ lệ có gợi ý; xếp confidence, lift, support; không fallback mặc định. | K/seed/mốc chia/support/confidence chưa chốt; chưa có luật hoặc điểm đánh giá thực tế. |

Quyết định này là của nhóm, không gán ngược thành rubric hoặc công nghệ bắt buộc của GV. Những phần khác của bản đặc tả chưa được chấp nhận chỉ vì ba lựa chọn này được đồng ý.

**Xác nhận học thuật đã có theo người dùng:** U-25 duyệt dataset, U-26 khung B + quy cách A. Không hỏi lại các xác nhận này; quy cách nộp/deadline cập nhật khi có thông báo.

Đã chuyển sang [thiết kế kỹ thuật đề xuất](12_TECHNICAL_DESIGN.md). Đã có [Master Implementation Plan](13_MASTER_IMPLEMENTATION_PLAN.md) để review theo milestone; chưa triển khai ứng dụng, cài stack hoặc nghiệm thu runtime.
