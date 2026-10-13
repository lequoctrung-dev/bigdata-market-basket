# Khảo sát thực tế Online Retail II

Ngày kiểm tra nguồn/audit: **13/10/2026**. **Cập nhật U-25:** người dùng xác nhận Online Retail II được GV chấp thuận. Số liệu phía dưới được ghi theo phiên bản policy đã kiểm tra; không thay bằng số dự kiến hoặc coi là Spark runtime.

**Kết luận để đọc nhanh:** đã đọc hết hai sheet, 1.067.371 dòng. Có dữ liệu hóa đơn/sản phẩm/thời gian/giá để tiếp tục đặc tả bài toán. Cần xử lý phần chồng lấn giữa sheet, dữ liệu hủy/điều chỉnh và mã phí/dịch vụ. Chưa khai phá luật nên chưa kết luận chất lượng gợi ý.

## 1. Nguồn và phạm vi kiểm tra

- [Nguồn UCI và CC BY 4.0](https://archive.ics.uci.edu/dataset/502/online+retail+ii); ghi công Daqing Chen, DOI 10.24432/C5CG6D.
- [XLSX gốc](../data/raw/online-retail-ii/online_retail_II.xlsx), 45.622.278 byte. SHA-256: `bcbe73b35f5b7babf197fb0cb983a11f5d9ff929078d4aa53d171b1f2df2e980`.
- Đọc toàn bộ bằng Python 3.12.14/openpyxl 3.1.5, chế độ chỉ đọc. Không sửa/xóa dòng nguồn. [Kết quả chi tiết](evidence/online-retail-ii-profile.json).
- [Đối chiếu độc lập số dòng trong XML XLSX](evidence/online-retail-ii-row-reconciliation.json) khớp tổng dữ liệu sau khi trừ hai dòng header.
- Đây là khảo sát dữ liệu bằng công cụ phân tích, **không phải job Spark của sản phẩm**, benchmark, EXP-02 hoàn chỉnh hoặc kiểm chứng MongoDB/Spring Boot.

| Sheet | Dòng dữ liệu, không gồm header | Thời gian thực tế |
| --- | --- | --- |
| Year 2009-2010 | 525.461 | 01/12/2009 07:45 – 09/12/2010 20:01 |
| Year 2010-2011 | 541.910 | 01/12/2010 08:26 – 09/12/2011 12:50 |

## 2. Schema và chất lượng đã quan sát

Tên cột dưới đây là **tên thực trong file**, khác một số tên metadata UCI. Các mã xuất hiện dưới cả kiểu số và chuỗi; khi nhập cần quy về định danh chuỗi, không ép mọi mã thành số.

| Cột thực tế | Vai trò / quan sát |
| --- | --- |
| Invoice | Khóa hóa đơn dự kiến; có số và chuỗi, gồm mã bắt đầu C. |
| StockCode | Mã item; có mã hàng, phí/dịch vụ và mã chữ cần phân loại. |
| Description | Tên/mô tả; thiếu 4.382 dòng, còn 4 ô kiểu số. 1.214 mã có nhiều mô tả không rỗng. |
| Quantity | Số lượng; 22.950 dòng âm, không có dòng bằng 0. |
| InvoiceDate | Ngày giờ; không thấy thiếu hoặc sai kiểu trong lần đọc; chưa xác nhận timezone. |
| Price | Đơn giá; 6.202 dòng bằng 0, 5 dòng âm. GBP theo mô tả nguồn, file không có cột tiền tệ. |
| Customer ID | Thiếu 243.007 dòng; không mặc định loại khỏi bài toán theo giỏ. |
| Country | Không có ô rỗng; vẫn có 756 dòng ghi Unspecified. |

Có 53.628 mã hóa đơn và 5.304 mã item phân biệt trên dữ liệu thô; đây không phải số hóa đơn/sản phẩm hợp lệ cuối cùng. 19.494 dòng có Invoice bắt đầu C; 3.457 dòng có Quantity âm nhưng không có tiền tố C. Các loại lỗi có thể chồng nhau, **không cộng các số này làm tổng dòng cần loại**.

## 3. Phần chồng lấn và định danh giỏ

- 1.088 mã Invoice xuất hiện ở cả hai sheet; hai khoảng ngày chồng lấn đầu tháng 12/2010.
- Có 34.335 lần xuất hiện sau lần đầu của bộ tám giá trị ô giống nhau khi đọc sheet 1 rồi sheet 2.
- Phân rã: 12.133 lần lặp trong từng sheet và 22.202 bộ giá trị phân biệt của sheet 2 đã có ở sheet 1. Đây là cách đếm chẩn đoán; chưa phải số dòng loại theo quy tắc xử lý cuối.
- Không thấy một Invoice gắn với nhiều Customer ID không rỗng hoặc nhiều Country. Có 83 Invoice chứa nhiều timestamp; trong ứng viên giao dịch mua dương có 82 trường hợp, đều nằm trong cùng ngày.
- Vì vậy, không thêm sheet vào khóa giỏ mặc định: việc này có thể tách một hóa đơn thật thành hai giỏ. Việc gom theo Invoice và chọn timestamp đại diện vẫn phải có quy tắc rõ.

## 4. Cấu trúc giỏ ứng viên trước khi chốt P-01/P-02 — kết quả có điều kiện

Điều kiện khảo sát: Invoice/StockCode không rỗng, ngày hợp lệ, không có tiền tố C, Quantity > 0, Price > 0. Giữ dòng thiếu khách hàng và giữ dòng lặp; gom theo Invoice, mỗi StockCode chỉ xuất hiện một lần trong giỏ. Chưa loại mã phí/dịch vụ.

| Chỉ số ứng viên | Kết quả |
| --- | --- |
| Dòng thỏa điều kiện | 1.041.670 |
| Giỏ / mã item | 40.077 / 4.916 |
| Giỏ một item / từ hai item | 3.688 / 36.389 |
| Số item duy nhất: trung vị / P95 / lớn nhất | 15 / 72 / 1.110 |

Đủ cơ sở để khảo sát mua kèm tiếp, nhưng chưa chứng minh có luật tốt hoặc chạy FP-Growth vừa tài nguyên. Giỏ rất lớn cần phân tích ảnh hưởng, không tự cắt bỏ để làm đẹp kết quả.

Có mã như POST (POSTAGE), DOT (DOTCOM POSTAGE), C2 (CARRIAGE), BANK CHARGES, D (Discount), M (Manual). Ngược lại, PADS và một số mã DCGS có mô tả hàng hóa. **Không dùng regex “5 chữ số” để tự kết luận mã còn lại không phải sản phẩm.** Thử điều kiện regex làm số giỏ còn 39.516, nhưng đó chỉ là chẩn đoán, không là chính sách đã chọn.

## 5. Đoạn thông tin để người dùng trình duyệt dataset

> Nhóm đề xuất Online Retail II từ UCI cho đề tài “Phân tích hành vi mua sắm và gợi ý sản phẩm mua kèm”. File đã kiểm tra có hai sheet, 1.067.371 dòng, với hóa đơn, mã hàng, số lượng, thời gian, giá, mã khách và quốc gia. Nhóm dự kiến phân tích giao dịch, tạo giỏ và khai phá luật bằng PySpark/FP-Growth; dùng MongoDB và website Spring Boot/MVC/Thymeleaf để demo. Dữ liệu có thiếu, hủy/điều chỉnh và phần chồng lấn cần xử lý; nguồn cấp phép CC BY 4.0.

Đoạn trên là thông tin đã chuẩn bị. U-25 hiện ghi người dùng xác nhận GV chấp thuận dataset; trợ lý chưa trực tiếp gửi hoặc đọc thông báo độc lập. Không cần xin duyệt lại.

## 6. Chính sách đã chốt và kết quả tính lại

**U-16/P-01:** chỉ giữ lần đầu của bộ tám giá trị giống nhau, đọc Year 2009-2010 trước Year 2010-2011, từ trên xuống trong mỗi sheet. Không giữ lần lặp trong cùng sheet. Đây là thay thế đề xuất max(n1,n2), không dedup chỉ theo Invoice/StockCode.

[Audit chính sách đã chốt](evidence/online-retail-ii-approved-policy.json) đọc lại toàn nguồn và đối chiếu với profile ban đầu/hash nguồn. Chỉ tính thống kê, chưa xuất dataset sạch hoặc ghi database.

| Bước kiểm tra | Số dòng |
| --- | --- |
| Nguồn | 1.067.371 |
| Lần lặp sau lần đầu bị loại khỏi dữ liệu phân tích | 34.335 |
| Còn lại theo P-01 | 1.033.036 |
| Dòng mua dương/ngày/mã hợp lệ sau P-01 | 1.007.913 |
| Dòng thuộc nhóm item loại theo P-02 trong tập mua dương | 4.546 |
| Dòng ứng viên còn lại sau P-01/P-02 | 1.003.367 |

1.033.036 = 1.007.913 + 25.123 dòng không thuộc tập mua dương/hợp lệ. 1.007.913 = 1.003.367 + 4.546; các bước này không chồng nhau.

**U-17/P-02:** loại nhóm phí/dịch vụ/điều chỉnh, Manual/voucher khỏi khai phá/gợi ý. Audit có ghi ADJUST2/B (mô tả Adjustment/Adjust bad debt) và m (Manual) thuộc cùng nhóm; việc phân loại mã không thay toàn bộ StockCode thành chữ hoa. Voucher dùng họ mã gift_. Giữ PADS/DCGS/SP1002 có mô tả hàng hóa.

Ứng viên còn 39.526 giỏ và 4.897 item, 36.308 giỏ từ hai item; giỏ lớn nhất 1.108 item. **Các con số này thuộc audit trước U-21:** TEST001 (9 dòng) và TEST002 (1 dòng) còn nằm trong audit này. Người dùng đã chọn loại khỏi khai phá/gợi ý; giữ nguyên bằng chứng cũ, không gọi nó là counts cuối sau loại TEST.

Thay chính sách khử trùng làm thay số dòng/giá trị thống kê; giỏ dùng set item không tự tăng tần suất bởi dòng lặp. Không xóa bản gốc hoặc diễn giải tất cả bản lặp thành lỗi nghiệp vụ đã được chứng minh.

**U-18/P-03:** đã chọn so sánh/giao thức và ranking; chưa có kết quả FP-Growth hoặc đánh giá.

## 7. Trạng thái tiếp theo

P-01/P-02/P-03 đã chốt, không cần hỏi lại. [Thiết kế kỹ thuật](12_TECHNICAL_DESIGN.md) tiếp tục là đề xuất để review; B-P17 đã được người dùng xác nhận chấp thuận theo U-25. Không dùng số ứng viên/audit Python làm benchmark Spark, hoặc bằng chứng cả hai máy đã demo.


**Policy mới U-21:** TEST001/TEST002 loại khỏi tập khai phá/gợi ý, vẫn giữ trong nguồn/audit chất lượng. Nếu không đổi điều kiện nào khác, số dòng ứng viên dự kiến là **1.003.367 − 10 = 1.003.357**; đây là phép trừ từ audit đã có, **chưa chạy lại policy mới trong pipeline**. Số giỏ/item/giá trị sau loại TEST chưa đo, không tự ghi bằng số cũ.
