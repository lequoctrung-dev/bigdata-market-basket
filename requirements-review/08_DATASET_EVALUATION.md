# Đánh giá dataset và phương án đề xuất

Ngày khảo sát: **13/10/2026**; cập nhật kỹ thuật theo **U-09** cùng ngày. Dataset ưu tiên không thay đổi. Căn cứ học phần: B tr.1–2, II.2; B tr.3, II.5/T1, P042–P043; [phạm vi và stack đã chọn](07_CONFIRMED_SCOPE.md).

Bảng so sánh dưới đây giữ căn cứ khảo sát metadata ban đầu; các ứng viên khác chưa tải/kiểm tra. **Online Retail II đã được chọn để khảo sát theo U-10 và đã kiểm tra file thực tế**, xem [file 10](10_DATASET_PROFILE.md). Các kết quả có điều kiện trong file 10 chưa phải pipeline Spark/FP-Growth hoặc benchmark. U-25 xác nhận GV đã chấp thuận dataset theo người dùng.

## Các lựa chọn

| Dataset | Thông tin đã kiểm tra từ nguồn | Nhận định của người phân tích | Giới hạn / điều chưa xác minh |
| --- | --- | --- | --- |
| **[UCI Online Retail II](https://archive.ics.uci.edu/dataset/502/online+retail+ii)** | 1.067.371 dòng; 01/12/2009–09/12/2011; XLSX 43,5 MB; hóa đơn, sản phẩm, số lượng, thời điểm, đơn giá GBP, khách hàng, quốc gia; có thiếu dữ liệu; CC BY 4.0, cần ghi công. | **Ưu tiên**: cùng dữ liệu phục vụ phân tích mua hàng và tạo giỏ cho luật kết hợp; nguồn và quyền sử dụng rõ; dung lượng tải nhỏ hơn các lựa chọn giao dịch hàng chục triệu dòng. | Nhà bán quà tặng ở Anh, nhiều khách bán buôn; dữ liệu lịch sử không đại diện mặc nhiên cho bán lẻ Việt Nam. 43,5 MB không phải mức RAM cần dùng. Tên cột/file thực tế đã kiểm tra ở file 10; chưa có kết quả khai phá/đánh giá cuối. |
| **[UCI Online Retail](https://archive.ics.uci.edu/dataset/352/online+retail)** | 541.909 dòng; 01/12/2010–09/12/2011; XLSX 22,6 MB; có trường hóa đơn/sản phẩm/số lượng/giá/thời gian/khách hàng/quốc gia; CC BY 4.0. | **Dự phòng** nếu bộ II gây khó khăn thực tế; quy mô nhỏ hơn và vẫn đúng loại bài toán. | Chưa kiểm tra chất lượng thực tế; không coi metadata là chứng minh dữ liệu sạch. Mô tả nhà bán lẻ và thời gian gần với II: cần kiểm tra trùng nếu dùng đồng thời, không mặc nhiên coi là tập kiểm thử độc lập. |
| **[Instacart 2017 — mô tả do Jeremy Stanley công bố](https://gist.github.com/jeremystan/c3b39d947d9b88b3ccff3147dbcf6c6b)** | Khoảng 3,4 triệu đơn, 206 nghìn người dùng, 50 nghìn sản phẩm; bảng quan hệ đơn–sản phẩm hơn 30 triệu dòng; có thứ trong tuần, giờ, khoảng cách đơn, nhóm sản phẩm và dấu mua lại. | Phù hợp nghiên cứu giỏ hàng tạp hóa, phân loại sản phẩm và mua lại; nhiều dữ liệu hơn nhưng phải ghép nhiều bảng. | Các trường được công bố không có giá/số lượng: suy ra chưa thể tính doanh thu thực từ chúng. Chưa xác minh tải dữ liệu và điều khoản hiện hành; công cụ không đọc được trang tải Instacart/Kaggle trong lượt khảo sát. Không khẳng định chạy vừa RAM 16 GB. |
| **[dunnhumby The Complete Journey](https://www.dunnhumby.com/source-files/)** | Trang nhà cung cấp mô tả giao dịch trong hai năm của 2.500 hộ, kèm một số thông tin hộ và tiếp thị trực tiếp. | Có tiềm năng phân tích hành vi hộ gia đình/tiếp thị; phạm vi đó rộng hơn nhu cầu mua kèm hiện tại. | Chưa xác minh số dòng, dung lượng, schema đầy đủ, tải thực tế và điều khoản. Các số 4,3 GB/300 triệu giao dịch trên cùng trang thuộc bộ khác, không gán sang Complete Journey. |

## Khuyến nghị

**Online Retail II đã được chọn để khảo sát theo U-10**; U-25 xác nhận dataset đã được GV chấp thuận theo người dùng. Online Retail chỉ là phương án dự phòng, chưa tự chuyển dataset. Lựa chọn dựa trên độ phù hợp với hai vế của đề tài, dữ liệu giá/số lượng/thời gian, quyền sử dụng rõ và điều kiện máy cá nhân; không dựa vào một ngưỡng số dòng do người phân tích tự đặt.

Hơn một triệu dòng giao dịch không đồng nghĩa hơn một triệu hóa đơn hoặc khách hàng. Số dòng cũng không tự chứng minh cần cluster hay Spark nhanh hơn mọi công cụ khác. Phần mô tả Big Data nên nêu quy mô thật, chất lượng dữ liệu và vai trò công nghệ xử lý thực tế.

Các nội dung đã khảo sát được ghi ở file 10; trước chốt quy tắc vẫn đối chiếu: số bảng/sheet và schema; khóa hóa đơn; số sản phẩm/giỏ; giao dịch hủy/đổi trả; giá/số lượng không hợp lệ; thiếu mã khách hàng; các dòng lặp; tỷ lệ giỏ một sản phẩm. Đây là **các câu kiểm tra dữ liệu đề xuất**, không phải kết quả đã đo. Không tự loại dòng chỉ vì thiếu CustomerID nếu vẫn xác định được giỏ; không coi sản phẩm xuất hiện nhiều lần là trùng sai nếu chưa xét nghiệp vụ.

Chính sách hủy/đổi trả ảnh hưởng khác nhau đến doanh thu và giỏ dùng khai phá; cần quyết định có căn cứ từ dữ liệu. Luật mua cùng không chứng minh quan hệ nhân quả hoặc doanh thu tăng. Nếu tín hiệu mua kèm nghèo, phải báo cáo hạn chế thay vì nhân bản dữ liệu để làm đẹp quy mô.

File B:P152 yêu cầu duyệt dataset. U-25 đã giải quyết theo xác nhận của người dùng rằng GV chấp thuận Online Retail II; chưa đọc thông báo độc lập, không hỏi lại việc duyệt.

## Phương án kỹ thuật đã chọn theo U-09

**PySpark local + FP-Growth + MongoDB local + Spring Boot** được người dùng lựa chọn và tư vấn đánh giá phù hợp tại [file 09, SOL-05](09_TECHNICAL_ADVISORY_RESEARCH.md). Spring MVC + Thymeleaf và cách chọn giỏ đã chốt U-11/U-12; schema, bố cục cụ thể và bộ phiên bản chưa chốt. Cả hai máy cần demo U-15; chưa triển khai/benchmark stack.

| Thành phần | Vai trò trong phương án | Căn cứ và giới hạn |
| --- | --- | --- |
| Dataset/file gốc | Giữ XLSX gốc và thông tin nguồn để kiểm tra/tái tạo; đã có khảo sát thực tế file 10 | U-25 xác nhận dataset được GV chấp thuận theo người dùng; không suy runtime đã chạy. |
| MongoDB local | Lưu dữ liệu nhập từ nguồn và kết quả phân tích/luật phù hợp; chia vai trò dữ liệu theo lần chạy | B-H02; B-T01; bám gợi ý đề tài. Schema/index và phần dữ liệu sạch/giỏ cần lưu còn thiết kế; không gom toàn bộ dữ liệu/luật vào một document. |
| PySpark local | Đọc dữ liệu, làm sạch, thống kê, tạo giỏ và xử lý theo lô; ghi kết quả về MongoDB | B-H03–B-H04; B-T02. MongoDB Connector và kiểu dữ liệu phải được kiểm chứng; không đọc toàn bộ DB vào pandas để thay Spark. |
| FP-Growth | Tập phổ biến và luật kết hợp; đánh giá phù hợp | B-H05–B-H06; B-V01–B-V05. Thuật toán và giao thức không đổi khi chuyển web/lưu trữ. |
| Spring Boot | Đọc dữ liệu/kết quả từ MongoDB, phục vụ thống kê, tra luật và gợi ý trên website | U-03/U-09; B-F01–B-F02. PySpark vẫn ở Python; không đổi sang Java Spark. |
| Giao diện | **Spring MVC + Thymeleaf đã chọn theo U-12**; HTML/CSS và biểu đồ cần thiết | Cách chọn giỏ U-11 đã chốt; bố cục và thư viện biểu đồ còn thiết kế. Cả hai máy cần demo U-15. |

Đề xuất xử lý theo lô trước buổi demo rồi dùng MongoDB + Spring Boot phục vụ kết quả; không khai phá lại trong mỗi request. Parquet + Streamlit được giữ làm phương án so sánh trong file 09, không còn là stack chính; Parquet chỉ tham khảo nếu có nhu cầu file trung gian thực tế.

Các nguồn chính thức: [MongoDB Spark Connector](https://www.mongodb.com/docs/spark-connector/current/getting-started/), [Spring Data MongoDB](https://spring.io/guides/gs/accessing-data-mongodb/), [Spring MVC/Thymeleaf](https://spring.io/guides/gs/serving-web-content/), [MongoDB Community](https://www.mongodb.com/products/self-managed/community-edition). Bộ phiên bản và thử nghiệm mới nằm ở file 09; chưa xác nhận chạy được trên RAM 16 GB.

## Đánh giá kết quả: P-03 đã chọn, không phải tiêu chí chấm mới

- Báo cáo thống kê dữ liệu trước/sau xử lý, kích thước giỏ, tập phổ biến và luật; dùng support/confidence/lift để giải thích độ phổ biến và quan hệ kết hợp.
- U-18 chốt so sánh gợi ý theo luật với gợi ý sản phẩm phổ biến, ẩn một item trong giỏ; Recall@K/tỷ lệ có gợi ý. Cách chia tập theo thời gian, cách ẩn sản phẩm trong giỏ kiểm thử, số lượng gợi ý và độ đo cần chốt sau khi kiểm tra dữ liệu; không để dữ liệu kiểm thử tham gia khai phá.
- Các phép đánh giá gợi ý có thể xem xét độ đúng trong danh sách gợi ý và độ phủ; chưa đặt ngưỡng bắt buộc. Sự hiện diện của luật không tự chứng minh chất lượng gợi ý.
- Đo thời gian/tài nguyên trên môi trường thật để mô tả thực nghiệm; không cam kết trước mức RAM, tốc độ hay mức cải thiện.

Yêu cầu nguồn giữ nguyên là **đánh giá bằng độ đo phù hợp; phân tích, so sánh, giải thích và nêu hạn chế** (B:P018). Lịch cũ còn nhắc baseline (B:P147). U-05 không quy định baseline/độ đo cụ thể; không suy ra được miễn toàn bộ đánh giá.

U-16 chốt P-01 giữ duy nhất lần đầu cho tuple tám giá trị, U-17 chốt nhóm phí/dịch vụ/điều chỉnh không gợi ý; số liệu tính lại ở file 10. Thiết kế file 12 còn là đề xuất, chưa triển khai.


**Cập nhật U-20–U-26:** loại TEST001/TEST002 khỏi khai phá/gợi ý; giữ nguồn MongoDB để Spark xử lý, phân tích chỉ dòng đầu; cả hai máy phải full run; TV1 data/Spark, TV2 Java/web; khung B + quy cách A. Counts audit cũ là lịch sử trước loại TEST, chưa là counts cuối.
