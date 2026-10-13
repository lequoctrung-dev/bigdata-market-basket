# Đặc tả bài toán — quyết định đã chốt và chi tiết còn đề xuất

Ngày cập nhật: **14/10/2026**. Căn cứ: [RTM](01_REQUIREMENT_MATRIX.md), [U-01–U-30](07_CONFIRMED_SCOPE.md), [khảo sát thực tế](10_DATASET_PROFILE.md).

**Review M0 đã hoàn tất về tài liệu:** Agent cụ thể hóa bối cảnh/mục tiêu, mapping và KPI tại mục 8–10; người dùng chọn M0-D1/D2/D3 theo U-27–U-29 và xác nhận cả TV1/TV2 đã review, chấp thuận bản hiện tại theo U-30. M0 đóng ngày 14/10/2026; chưa triển khai sản phẩm hoặc nghiệm thu runtime.

**Bạn chỉ cần đọc phần này và phần cuối:**
- Đã chốt dataset khảo sát, stack, MVC/Thymeleaf, chọn giỏ nhận gợi ý và cả hai máy đều demo.
- Dữ liệu đã kiểm tra đủ hai sheet; GV chấp thuận dataset và khung B/quy cách A theo người dùng U-25/U-26.
- **P-01/P-02/P-03 đã chốt U-16–U-18**; P-01 chỉ giữ lần đầu, thay phương án max(n1,n2). KPI/bố cục/scope dashboard chốt U-29, công bố/kiểu tiền chốt U-27/U-28; contract được hai thành viên chấp thuận theo U-30.
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
| OUT-02 | Phân tích hàng hóa theo tháng: số hóa đơn mua, phân phối số item duy nhất/giỏ, item phổ biến theo số giỏ và lượng bán. | B-H08; B-F01/B-F02; U-29. KPI đã chọn; mẫu số và lọc item phải đi cùng số hiển thị. |
| OUT-03 | Giá trị dòng mua hàng hóa dương bằng Quantity × Price, GBP, tổng hợp lên dashboard. | B-H08; file 10; U-29. Không gọi là doanh thu ròng/lợi nhuận; giải thích giữ/loại trùng và hủy/điều chỉnh. |
| OUT-04 | Tập phổ biến: item và số giỏ; luật: tiền đề, kết luận, support/confidence/lift; kèm cấu hình và số giỏ khai phá. | B-H05/B-H06; B-T06; B-E03/B-E06. Đối chiếu ví dụ tính tay và lượt chạy. |
| OUT-05 | Gợi ý mua kèm cho giỏ chọn: mã/tên item, luật làm căn cứ và chỉ số; loại item đã có, không trùng ứng viên. | B-H09; U-11. Tiền đề phải có đủ; không gọi confidence là xác suất riêng cho người xem. |
| OUT-06 | Kết quả so sánh và giới hạn; thời gian/tài nguyên đo thực tế theo bước khi chạy sau này. | B-V01–B-V05; B-E04/B-E07; chưa có kết quả thực nghiệm. |
| OUT-07 | Website MVC/Thymeleaf hiển thị các nhóm kết quả trên; cả hai máy đều cần demo. | B-F01/B-F02/B-N03; U-12/U-15/U-29. Ba khu vực đã chọn, chi tiết biểu đồ còn triển khai; không biến bảy nhóm đầu ra thành bảy màn hình bắt buộc. |

Ba khu vực điều hướng **đã chọn U-29**: **Tổng quan/phân tích**, **Tập phổ biến và luật** (kèm kết quả đánh giá), **Gợi ý theo giỏ**. Công thức và nội dung tối thiểu ở mục 9; không thêm đăng nhập/thanh toán, quản lý đơn hoặc cá nhân hóa theo tài khoản.

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

PySpark chạy batch và ghi kết quả MongoDB; Spring Boot đọc lượt hoàn chỉnh để phục vụ web. Contract collection/manifest/công bố trong file 12 đã nghiệm thu về tài liệu M0 theo U-30; chưa triển khai hoặc kiểm chứng runtime.

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

## 8. Bối cảnh, mục tiêu và ranh giới dữ liệu của M0

**Bài toán/bối cảnh:** phân tích các hóa đơn lịch sử của một nhà bán lẻ trong Online Retail II để mô tả xu hướng mua và tìm các mặt hàng thường xuất hiện cùng nhau. Người xem website chọn một/nhiều mã hàng trong giỏ, hệ thống áp dụng luật đã khai phá để đưa gợi ý có căn cứ. Bối cảnh này phục vụ B-S01/B-S02 và đề tài đã duyệt U-01, không giả định dữ liệu đại diện mọi thị trường.

**Mục tiêu/giá trị dự kiến:** tạo quy trình truy vết từ nguồn → làm sạch → thống kê/giỏ → FP-Growth/baseline/đánh giá → website; giúp quan sát dữ liệu và giải thích lý do có/không có gợi ý. Đánh giá khả năng khôi phục item bị ẩn bằng cùng giao thức cho hai phương pháp. Đây là mục tiêu B-S03/B-S07, chưa chứng minh tăng doanh thu, dự đoán nhu cầu cá nhân hoặc hiệu quả kinh doanh.

**Phạm vi B-S04–B-S06:** toàn bộ hai sheet làm nguồn; batch riêng local và web đọc kết quả hoàn chỉnh; raw archive giữ phần lặp, dữ liệu phân tích chỉ dòng đầu P-01. Khai phá/gợi ý chỉ hàng hóa theo P-02/U-21, không loại Customer ID thiếu khỏi giỏ. Cả hai máy tự full run cấu hình cuối, fit chỉ train; vai trò và review giữ U-22/U-23. Các input/output mục 1–2 được cụ thể hóa trong contract file 12, không thêm nguồn, mô hình hoặc hệ thống bán hàng.

### 8.1. Các tập dữ liệu và chính sách thống kê

| Tập/scope | Định nghĩa | Mục đích và mẫu số |
| --- | --- | --- |
| `raw` | Tất cả source rows của hai sheet, có lineage; không sửa XLSX. | Audit chất lượng và giải thích nguồn; các loại lỗi có thể chồng nhau. |
| `p01_retained` | Một dòng đầu cho mỗi tuple tám giá trị nguồn bằng nhau, trước chuẩn hóa/lọc. | Đầu vào chung của các phân tích sau P-01; counts bước này không phụ thuộc P-02/TEST. |
| `positive_valid` | Từ p01_retained: Invoice/StockCode hợp lệ, Invoice không bắt đầu C (kiểm tra tiền tố không phân biệt case nhưng giữ ID), Quantity nguyên > 0, Price > 0, ngày local hợp lệ. | Giao dịch mua dương gồm cả mã phí/Manual/voucher/TEST; không gọi toàn bộ là hàng hóa/doanh thu ròng. |
| `merchandise` | positive_valid trừ nhóm loại mapping P-02 và TEST theo mục 8.2. | Giỏ khai phá và thống kê hàng hóa; Invoice chỉ còn mã loại không tạo giỏ rỗng. Giỏ một item vẫn giữ, chỉ không đủ điều kiện ẩn một item để đánh giá. |
| `train`, `dev`, `test` | Hóa đơn merchandise chia hoàn chỉnh theo thời gian local; mọi hóa đơn chỉ một tập. | Train cho fit, danh mục, tên, baseline và mẫu số support; dev chọn cấu hình, test cuối sau freeze. Mốc/K/seed/tham số ở M3 theo QD-08, chưa chốt số ở M0. |

Các tập trên là quy ước review, **chưa xuất dataset/pipeline**. Timestamp giỏ lấy min trên dòng hàng còn trong giỏ; nhiều timestamp hoặc ID sau chuẩn hóa gây xung đột phải ghi audit và kiểm tra sau policy, không dựa riêng quan sát lịch sử để cam kết không còn lỗi.

### 8.2. Mapping P-02 và TEST có căn cứ

| Nhóm | Điều kiện phân loại | Căn cứ đã có | Khai phá/gợi ý |
| --- | --- | --- | --- |
| Phí/dịch vụ/discount | Mã `POST`, `DOT`, `C2`, `BANK CHARGES`, `AMAZONFEE`, `D`, `S` | U-17; file 10 và [audit policy](evidence/online-retail-ii-approved-policy.json), tên/mô tả đã quan sát. | Loại; giữ raw/quality audit. |
| Điều chỉnh | `ADJUST`, `ADJUST2`, `B` | U-17 theo nghĩa điều chỉnh; audit ghi ADJUST2: Adjustment by Peter, B: Adjust bad debt. | Loại; không gọi mọi số lượng âm là trả hàng đã xác định. |
| Manual | `M` và `m` | U-17; audit xác nhận mô tả Manual ở cả hai spelling. | Loại theo phân loại, không đổi case toàn bộ ID hàng hóa. |
| Voucher | Tiền tố `gift_` hoặc mã `GIFT` khi phân loại không phân biệt case | Họ voucher trong audit và quy tắc `p02_voucher_rule`; U-17. | Loại; không dùng regex này cho tất cả mã chữ khác. |
| Test product | `TEST001`, `TEST002` | U-21 quyết định loại; audit cũ ghi 9 và 1 dòng ứng viên, trước khi quyết định được áp dụng. | Loại; vẫn giữ trong raw/quality audit. |
| Mã hàng có chữ | Ví dụ `PADS`, các mã `DCGS` có mô tả hàng hóa, `SP1002` | File 10/audit; U-17 giữ mã chữ có căn cứ hàng hóa. | Giữ khi thỏa điều kiện giao dịch; không whitelist chỉ ba ví dụ hoặc loại toàn bộ mã ngoài regex năm chữ số. |

Đối chiếu exclusion dùng spelling không phân biệt case; danh tính StockCode vẫn giữ case. Các mã ngoài mapping tiếp tục theo chính sách ứng viên đã có, không biến bảng trên thành whitelist hàng hóa. Nếu phát hiện mã/mô tả mới mơ hồ, ghi mã, mô tả, source row và ảnh hưởng để TV1/TV2 review; không tự gán đã được U-17 chấp thuận hoặc âm thầm đổi policy. Thay mapping có version/hash và counts mới ở M2, không sửa audit lịch sử hoặc gán lại con số cũ.

Mapping này hoàn thiện hồ sơ M0-T3; **chưa chạy Spark hoặc tái xử lý nguồn**. Counts sau TEST chưa đo; phép trừ 10 ở file 10 không thay counts giỏ/item/GBP mới. P-02/U-21 đã chốt phạm vi khai phá/gợi ý, chưa tự quyết định xóa các nhóm này khỏi mọi thống kê; phạm vi dashboard là M0-D3 dưới đây.

## 9. KPI/màn hình tối thiểu — M0-D3 đã chọn theo U-29

**Đã chọn U-29:** dashboard chính phân tích **hàng hóa (`merchandise`)**, kèm khu vực chất lượng toàn nguồn/bảng số dòng loại. Cách này nhất quán với giỏ gợi ý, tránh phí/Manual/TEST chi phối “sản phẩm phổ biến”.

**Phương án so sánh không chọn:** dashboard chính dùng **toàn bộ dòng mua dương/hợp lệ (`positive_valid`)**, đồng thời tách thống kê hàng hóa để giải thích khác biệt. Giữ được góc nhìn toàn bộ dòng mua dương nhưng có hai bộ mẫu số, nhiều bảng/nhãn hơn. Giữ tập positive_valid để stage counts/audit; không tự thêm bộ dashboard thứ hai.

**Trạng thái: người dùng đã chọn gói dashboard hàng hóa + audit toàn nguồn ngày 14/10/2026; TV1/TV2 chấp thuận contract theo U-30.** M0-D3 thuộc DEC-02/DEC-05, không thêm điểm chấm hoặc tính năng ngoài đề tài. Toàn bộ KPI mua ở bảng dưới dùng scope merchandise; raw/p01_retained/positive_valid chỉ phục vụ phần chất lượng/stage counts.

### 9.1. Công thức và ngữ nghĩa KPI để review contract

| KPI/đầu ra | Định nghĩa cần giữ | Truy vết/đối chiếu |
| --- | --- | --- |
| Chất lượng nguồn | Raw count, giữ/loại P-01, không mua dương/hợp lệ, nhóm loại P-02/TEST, rows/baskets/items còn lại. Counts stage tuần tự có phương trình cân bằng; counts lỗi chồng nhau hiển thị riêng. | OUT-01; B-D08–B-D15/B-E05/B-E06. Scope và policy/source hash gắn lượt. |
| Số hóa đơn mua theo tháng | Count Invoice phân biệt có ít nhất một dòng trong scope đang hiển thị. Tháng lấy timestamp nhỏ nhất của các dòng còn lại của hóa đơn trong scope đó; toàn hóa đơn ở một tháng. | OUT-02/B-H08/B-F01/B-F02. Tổng buckets khớp tổng Invoice của scope; không lấy raw invoices làm mẫu số. |
| Kích thước giỏ | Số StockCode phân biệt trong từng Invoice của scope; phân phối số giỏ theo kích thước, nêu số giỏ một item/từ hai item. | Không dùng số dòng hoặc tổng Quantity thay số item duy nhất. Tần suất FP-Growth vẫn tính sự hiện diện. |
| Item phổ biến theo số giỏ | Count hóa đơn chứa item trong scope; nếu hiển thị tỷ lệ thì chia tổng giỏ của scope. Sort count giảm, StockCode tăng theo comparator ổn định. | Khác lượng bán; bảng toàn kỳ không dùng để xếp baseline train. |
| Lượng mua item | Tổng Quantity trên dòng của item trong scope sau P-01 và lọc đã ghi. | Khác số giỏ chứa item; không mất dòng khác giá/số lượng khi set hóa giỏ. |
| Giá trị mua dương GBP | Tổng `Quantity × Price` trên dòng thuộc scope; tổng theo tháng dùng cùng tháng hóa đơn của scope, cộng từ giá trị chưa làm tròn. | OUT-03; không gọi là doanh thu ròng/lợi nhuận/giá trị sau trả hàng. Giữ currency GBP theo nguồn; cách lưu tiền theo M0-D2. |
| Tập phổ biến/luật | frequency và support từ `train_basket_count`; support luật là tỷ lệ giỏ train chứa cả antecedent và consequent, confidence/lift theo mục 3.2 file 09. | OUT-04/B-H05/B-H06; bảng luật nêu run/config/mẫu số train, tách dashboard toàn kỳ. |
| Kết quả đánh giá | Recall@K và tỷ lệ truy vấn có gợi ý cho luật thuần/baseline, tách dev/final; kèm query count/K/seed/split và giới hạn. | OUT-06/B-V01–B-V05. Không tự bịa score, đặt ngưỡng đạt hoặc bắt FP-Growth thắng. |

Không bắt thêm RFM/phân khúc khách, biểu đồ quốc gia, doanh thu ròng hoặc số biểu đồ/trang cụ thể. Chi tiết màu, loại biểu đồ, URL, pagination là triển khai trong phạm vi, không cần người dùng chọn từng chi tiết.

### 9.2. Ba khu vực trên cùng website

| Khu vực | Nội dung tối thiểu để review | Các trạng thái cần giải thích |
| --- | --- | --- |
| Tổng quan/phân tích | Metadata run/source/policy, quality/stage counts; xu hướng hóa đơn/GBP theo tháng; kích thước giỏ; item phổ biến theo số giỏ và lượng mua. | Scope hiện tại, nguồn chưa sẵn sàng/lỗi kết nối; không hiển thị sample như dữ liệu thật. |
| Tập phổ biến và luật | Items/frequency/support, luật/metrics và cấu hình/mẫu số train; phần/bảng kết quả đánh giá dev/final cùng run khi có. | 0 luật hợp lệ khác chưa có kết quả hoặc output ghi thiếu; chưa có final metric ghi chưa đánh giá. |
| Gợi ý theo giỏ | Chọn/tìm item trong catalog train của run, gửi một/nhiều mã; nhận Top-K item chưa có cùng luật tốt nhất và metrics làm căn cứ. | Giỏ rỗng/mã sai/chọn trùng/form cũ; không có luật thì không có gợi ý, không mặc định fallback. |

Ba khu vực không buộc ba URL hoặc bảy màn hình. Giá trị K dùng cấu hình được ghi/freeze, không tự đặt mặc định trong M0. Danh mục chọn giỏ dùng toàn bộ item train hợp lệ, không chỉ item có luật; item mới ngoài train trong dev/test vẫn giữ trong denominator đánh giá, không tự bỏ để làm đẹp kết quả.

## 10. Quy tắc gợi ý/đánh giá chung giữa Python và Java

- Luật áp dụng khi **mọi** item tiền đề có trong query, kết luận chưa có. Lọc đầy đủ trước chọn Top-K; một ứng viên chỉ một lần. Cùng ứng viên dùng luật tốt nhất theo confidence giảm → lift giảm → support giảm → antecedent tăng khi bằng chỉ số.
- Xếp ứng viên theo confidence/lift/support của luật tốt nhất giảm, rồi StockCode tăng, rồi antecedent tăng; so antecedent theo tuple mã đã sắp, phần tử từng vị trí, prefix ngắn trước. Mã so Unicode code point, không locale; phiên bản comparator ghi cùng run. Không làm tròn metrics trước so sánh.
- Baseline xếp `train_basket_count` giảm, tie StockCode tăng; bỏ item có sẵn. Hai phương pháp dùng cùng query, target bị ẩn, catalog train, K và chính sách merchandise; baseline không bật thành fallback web.
- Giỏ evaluation có ít nhất hai item; ẩn đúng một item theo algorithm/seed version ghi manifest. Giỏ một item báo riêng. Item target mới ngoài train vẫn tính trong query count/Recall; gợi ý không thể phục hồi target đó phải phản ánh đúng điểm.
- Với N truy vấn hợp lệ, Recall@K trung bình là tổng indicator target nằm trong Top-K chia N (vì ẩn một item); tỷ lệ có gợi ý là số truy vấn trả ít nhất một item chia N. Query không có gợi ý đóng góp 0 vào cả hai; N=0 ghi không áp dụng/chưa có mẫu, không coi đã đo chất lượng 0.
- Train không đọc dev/test để chọn tên, tính baseline hoặc fit. Chọn tham số từ dev rồi freeze trước final; không tự refit toàn nguồn cho website. Dashboard toàn kỳ chỉ có vai trò mô tả, không truyền vào nhánh chọn tham số.

**Tình trạng review:** quy ước kỹ thuật trên cụ thể hóa P-03/U-18, không đổi giao thức. K/seed/mốc chia/support/confidence, precision/scale và bộ phiên bản còn để mốc tương ứng kiểm chứng. M0-D1/D2/D3 đã chọn U-27–U-29; TV1/TV2 chấp thuận theo U-30 và M0 đã đóng về tài liệu tại [checklist M0](14_MILESTONE_CHECKLIST.md). Dừng sau bàn giao, chưa mở M1.
