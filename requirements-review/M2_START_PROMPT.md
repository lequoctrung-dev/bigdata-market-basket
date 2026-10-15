# Prompt bắt đầu M2 trong thread mới

Ngày soạn: 15/10/2026. Đây là prompt bàn giao, không phải evidence M2 đã triển khai. Copy phần dưới vào thread mới trong cùng project, hoặc yêu cầu thread đó đọc đầy đủ file này rồi thực hiện.

---

Bạn tiếp tục đồ án Nhập môn Big Data tại workspace:
`D:\University\Semester7\BigData\DoAn`.

Tôi giao bạn thực hiện **M2 — Xây pipeline dữ liệu và kiểm chứng P-01/P-02 trên nguồn đầy đủ**, gồm M2-T1–M2-T4 trong `requirements-review/13_MASTER_IMPLEMENTATION_PLAN.md` và nghiệm thu tại `requirements-review/14_MILESTONE_CHECKLIST.md`.

Hãy làm trực tiếp trên repository, kiểm chứng bằng chạy thật và cập nhật hồ sơ theo bằng chứng. Không dừng ở lập kế hoạch. Nếu thiếu quyết định quan trọng thì trình phương án cụ thể, giải thích tác động, đề nghị một phương án và chờ tôi chọn trước phần phụ thuộc; vẫn tiếp tục phần độc lập có thể làm. Không tự bịa, suy xác nhận hoặc tự đổi scope/contract để vượt kiểm tra. Chỉ làm M2; bàn giao M2 đạt hoặc checkpoint chưa đạt rồi dừng, không tự mở M3/M4.

## 1. Đọc đầu phiên và đối chiếu trạng thái thật

1. Đọc đầy đủ `AGENTS.md`, `README.md`, `STATE.md`; kiểm tra branch, HEAD, status và diff liên quan. Giữ mọi thay đổi có sẵn; không giả định tôi đã commit/push theo lời đề nghị ở thread trước.
2. Đọc checklist 14, mục M2 và các quy tắc/cổng liên quan trong master plan 13; đọc đầy đủ file `07_CONFIRMED_SCOPE.md` để nắm xác nhận U và ngoại lệ mới nhất.
3. Đọc phần liên quan M2 trong `11_SPECIFICATION_DRAFT.md` (P-01/P-02, tập dữ liệu, mapping, scope/KPI) và `12_TECHNICAL_DESIGN.md` (collection/khóa/kiểu/source cells, lineage, manifest, retry/công bố). Tra file 01/02/03/15 theo ID cần cho M2, không yêu cầu tôi đọc lại toàn bộ hồ sơ.
4. Đọc `10_DATASET_PROFILE.md` cùng evidence nguồn/policy liên quan và `pipeline/README.md`; xem mã thật trong `pipeline/`, `scripts/` và các caller/contract cần thiết. Dùng file 09 và tài liệu chính thức khi cần kiểm chứng kỹ thuật/phiên bản. Nếu không đọc được nguồn cần thiết, nêu rõ giới hạn, không dựng lại nội dung từ suy đoán.
5. Phân biệt snapshot lịch sử và trạng thái hiện tại. Tài liệu hoặc bộ nhớ nói M1 còn mở trước U-35 là lịch sử; source of truth hiện tại là U mới nhất, STATE và receipt đóng M1. Nếu có mâu thuẫn thực sự, nêu căn cứ và tác động.

Sau khi đọc, báo ngắn trạng thái, phần M2 sẽ làm, quyết định còn thiếu và cách lưu bằng chứng; lập kế hoạch ngắn rồi triển khai trong phạm vi đã rõ.

## 2. Trạng thái bàn giao đã xác nhận

- **M0 đã đóng 14/10/2026**: U-27/U-28/U-29 chốt run bất biến + active/version, decimal text tại MongoDB và dashboard hàng hóa + audit toàn nguồn; hai thành viên review contract theo U-30. Contract `m0-contract-v1`.
- **M1 đã đóng 15/10/2026**: prototype thật MongoDB → PySpark/FP-Growth → MongoDB → MVC/Thymeleaf chạy trên TV1; 7 checks batch/18 checks web, 4 tests Python/4 tests Java đạt. U-35 xác nhận đã demo; cả hai đã học, giải thích và review, chấp thuận, không còn điểm sửa. Không hỏi lại các xác nhận này.
- **U-33 miễn receipt TV2 riêng ở M1**, không ghi TV2 đã chạy, không suy hai môi trường giống nhau là bằng chứng runtime. **Full run và demo thật riêng trên cả hai máy tại M6 vẫn giữ** theo U-15/U-22. M2 DoD vẫn cần TV2 review, chưa có ngoại lệ miễn phần đó.
- M1 chỉ dùng dữ liệu tự tạo: 22 dòng → P-01 giữ 20 → hàng hóa 12 dòng → 5 giỏ, 7 tập phổ biến/9 luật; đây không phải counts Online Retail II. Các tham số/precision của fixture không phải cấu hình toàn nguồn hoặc cấu hình M3 đã chốt.
- Run mẫu: `1b156c53-7c15-4a9e-a479-32b7ab3926f5`, publication version 3. Evidence cục bộ bị Git bỏ qua, gồm:
  - `artifacts/m1/TV1/environment.json`;
  - `pipeline-receipt-1b156c53-7c15-4a9e-a479-32b7ab3926f5.json`;
  - `web-receipt-8c0dff59-4d3e-404a-b084-073342db4532.json`;
  - `demo-ready-2026-10-15.json`, `lifecycle-stop-2026-10-15.json` trong cùng thư mục TV1.
  Thiếu file khi clone không đồng nghĩa chưa từng chạy; đối chiếu kết luận trong checklist và chỉ tái tạo kiểm tra cần thiết. Không tự dựng receipt thay thế.
- Khi bàn giao M1, web/MongoDB mẫu đã dừng đúng receipt, dữ liệu giữ lại; cổng 8081/27018 đóng, MongoDB sẵn có 27017 vẫn nghe. Đây là snapshot, kiểm tra lại trước thao tác mới. Không dùng PID lịch sử hoặc kill theo tên/cổng.
- Mã M1 nằm ở `pipeline/sample_fixture.py`, `sample_pipeline.py`, `test_sample_fixture.py`, dependency/connector POM, `scripts/invoke-m1.ps1`, `scripts/m1_control.py`, `web/pom.xml` và `web/src/`. Tái sử dụng phần có ích sau khi đọc, không biến fixture thành pipeline toàn nguồn bằng thay nhãn.

## 3. Quyết định phải giữ và lựa chọn mới phải hỏi

- Stack giữ **PySpark local + FP-Growth + MongoDB + Spring Boot/MVC/Thymeleaf**; batch riêng, không fit trên HTTP. Không thêm Python service, SPA, cloud/cluster, WSL/replica set hoặc chức năng bán hàng để chữa lỗi.
- Dataset Online Retail II và khung báo cáo B/quy cách A đã được GV chấp thuận **theo xác nhận người dùng U-25/U-26**. Không hỏi lại duyệt dataset/đề tài hoặc tự ghi đã đọc xác nhận độc lập của GV.
- TV1/tôi lead data/Spark/đánh giá; TV2 lead Java/web/tích hợp; review chéo. Không tự gán việc Agent làm thành đóng góp cá nhân hoặc ghi giờ/phần trăm chưa được xác nhận.
- Các lựa chọn U-01–U-35 đã có không hỏi lại. Deadline/giờ tuần vẫn chưa rõ, không ép trả lời lại hoặc cam kết kịp hạn. Đọc U mới hơn nếu có trong repository.
- U-32 cấp phạm vi MongoDB **mẫu M1** riêng tại 27018, database `bigdata_m1_sample`; không tự coi đó là namespace đã duyệt cho dữ liệu thật M2. Trước ghi toàn nguồn, làm rõ đích/namespace và cách cô lập dữ liệu thật với mẫu. Nếu chưa được chỉ dẫn hiện tại cho phép, trình phương án cụ thể để tôi chọn; không ghi vào dịch vụ 27017 hoặc ghi đè mẫu để tiết kiệm bước.
- Với mã/mô tả mới mơ hồ, thay đổi chính sách ngoại lệ, schema/semantics có ảnh hưởng, cách xử lý mất giá trị/giảm dữ liệu hoặc đổi môi trường lớn: đưa bằng chứng, số dòng/ảnh hưởng và phương án, rồi hỏi. Chi tiết kỹ thuật ít rủi ro trong contract đã duyệt thì tự xử lý, không xin phép từng hàm/lệnh.

## 4. Phạm vi thực hiện M2

### M2-T1 — Nhập nguồn bất biến, lineage và retry

- Nguồn tại `data/raw/online-retail-ii/online_retail_II.xlsx`; SHA-256 dự kiến `bcbe73b35f5b7babf197fb0cb983a11f5d9ff929078d4aa53d171b1f2df2e980`. Tự xác minh bytes/hash/header/thứ tự hai sheet trước nhập; khác nguồn thì báo, không ép khớp counts cũ.
- Hai sheet: `Year 2009-2010`, `Year 2010-2011`; tám cột theo thứ tự contract: Invoice, StockCode, Description, Quantity, InvoiceDate, Price, Customer ID, Country. Đối chiếu count từng sheet: 525.461 và 541.910 dòng dữ liệu, tổng 1.067.371, không gồm header.
- Giữ tám giá trị nguồn và nhãn kiểu trước chuẩn hóa; `dataset_id` từ hash XLSX, `sheet_index` từ 0, `source_row` là dòng Excel từ 2. Raw archive khác bản sao bytes XLSX; XLSX/ZIP nguồn giữ nguyên.
- Khóa/idempotency/conflict/READY theo file 12: retry không nhân bản, cùng khóa khác payload phải báo xung đột; nhập chưa đủ không được gọi dataset hoàn chỉnh. Kiểm chứng đường ghi/đọc MongoDB thật, không thay nguồn MongoDB bằng đọc file trực tiếp ở Spark để tránh khó khăn tích hợp.

### M2-T2 — Spark/P-01 và kiểm tra chất lượng

- Chỉ giữ lần đầu tuple tám giá trị nguồn giống nhau trên toàn workbook, gồm cả trùng trong một sheet và qua sheet; thứ tự `(sheet_index, source_row)`, không dựa thứ tự DB/partition.
- Number 1 và 1.0 bằng nhau theo giá trị; number 1 khác text "1"; giữ khác biệt text whitespace/case/null/ngày theo contract. Không dedup bằng Invoice/StockCode; dòng khác Quantity/Price phải còn.
- Đối chiếu trước mọi lọc khác: **1.067.371 − 34.335 = 1.033.036** trên source hash đã nêu, đồng thời kiểm chứng đúng lineage đầu và tính ổn định khi thay partition/thứ tự đọc. Sai số phải điều tra nguyên nhân, không sửa đáp án/audit để pass.
- Kiểm tra thiếu, hóa đơn hủy/điều chỉnh, giá/số lượng, mã/ngày và consistency. Không loại Customer ID thiếu mặc định; không thay null bằng giá trị bịa hoặc tự trim nguồn trước P-01.

### M2-T3 — P-02, giỏ và dữ liệu dòng hàng

- Áp dụng mapping có căn cứ ở file 11, gồm phí/dịch vụ/điều chỉnh, Manual, voucher và **TEST001/TEST002**. Không lọc hàng loạt bằng regex mã hàng hoặc xóa các nhóm này khỏi audit toàn nguồn.
- Giữ hàng hóa có mã chữ; giữ danh tính StockCode theo contract, không gộp item theo tên. Mã/mô tả mơ hồ mới phải có source row và ảnh hưởng để review trước thay policy.
- Giỏ unique item, không mất dữ liệu Quantity/Price ở dòng hàng; cùng Invoice qua sheet theo contract; giữ giỏ một item. Không tự cắt giỏ lớn để chạy nhẹ.
- Kiểm tra miền/precision/scale toàn nguồn và cả phép nhân/tổng tiền trước chọn cấu hình. MongoDB lưu decimal text, Spark tính decimal, Java đọc BigDecimal. Không bê kiểu decimal fixture hoặc dùng double/làm tròn để che mất chữ số. Ngày hóa đơn giữ local, không tự suy timezone.

### M2-T4 — Summaries, quality manifest, đối chiếu và tài nguyên

- Sinh đầu ra tiền xử lý/basket set, summaries và quality manifest theo scope/mẫu số file 11/12, có source/policy/parser/schema/code version/hash. Không tạo model/metrics final hoặc công bố một run thiếu output như run hoàn chỉnh.
- Dữ liệu M2 bao phủ nguồn để tiền xử lý/thống kê, chưa phải tập train đã đóng băng của M3. Không gán catalog/counts toàn nguồn thành train catalog/train frequency hoặc fit test khi split chưa được chốt.
- Counts các stage tuần tự phải cân bằng; thống kê lý do lỗi chồng nhau phải ghi riêng. Tính lại số sau P-02/TEST bằng pipeline thật, không dùng phép trừ từ audit cũ làm kết quả.
- Đối chiếu audit độc lập phù hợp đúng policy và vài hóa đơn/dòng tính tay có lineage; ghi phân phối giỏ, số lượng dòng/giỏ/item và thống kê tiền chính xác theo scope thực chạy.
- Đo thời gian/RAM/đĩa theo bước với phương pháp/đơn vị rõ. RAM Spark/JVM khác RAM Python; nói rõ phần đo bao phủ và giới hạn. Không biến dung lượng cache cấu hình hoặc RAM trống lúc preflight thành peak usage đã đo.

## 5. Môi trường M1 và giới hạn cần tránh lặp lại

Bộ đã chạy mẫu TV1: JDK 17.0.12; Python 3.14.6; PySpark 4.2.0/Scala 2.13.18; connector `_2.13:11.1.0`/driver Spark 5.1.4; PyMongo 4.18.3, NumPy 2.5.4; MongoDB 8.3.8; Maven portable 3.9.16; Boot 4.1.1/Data MongoDB 5.1.1/driver web 5.8.1. Đọc dependency thật và kiểm tra môi trường hiện tại; không coi các bản này đã chứng minh chạy toàn nguồn hoặc TV2.

- `.venv`, Maven/cache/JAR nằm trong dự án và bị Git bỏ qua; không nâng cấp phần mềm toàn máy hoặc sửa PATH/registry/execution policy âm thầm.
- Helper đã thử PowerShell 7.6.5 của môi trường Codex; Windows PowerShell 5.1 từng bị execution policy chặn. Không dùng Bypass để chữa.
- Spark startup qua `spark.jars.packages` từng gọi addFile/fetchFile/chmod và thiếu winutils; M1 dùng năm JAR chính thức resolve bằng Maven, local classpath trước JVM gateway. Không tải DLL/winutils không rõ nguồn hoặc patch bỏ quyền. Native/filesystem toàn nguồn chưa được kiểm chứng.
- Decimal Quantity `(20,0)` × Price `(20,8)` từng giảm scale xuống 6. Mẫu sửa bằng miền Quantity/decimal phù hợp và kiểm tra tổng exact; đó không phải cấu hình M2 đã chốt.
- Spark LongType cần Python int khi tạo DataFrame trong prototype; ghi PyMongo trực tiếp dùng BSON Int64. Không tắt schema verification hoặc đổi counts sang double.
- TV1 từng chỉ còn khoảng 2,6–2,7 GiB RAM trống ở snapshot; đo lại trước full-source job, cân đối tiến trình/cấu hình và ghi giới hạn, không tự hứa đủ RAM.

## 6. Ghi bằng chứng ngay khi làm để dùng cho báo cáo đồ án

Đây là yêu cầu thực hiện xuyên suốt, không đợi cuối phiên để nhớ lại hoặc chỉ lưu trong chat:

1. Cập nhật `STATE.md` ngắn gọn, checklist 14 theo evidence, file 07 khi có quyết định người dùng mới; cập nhật file 11/12/13 nếu thay đổi được chấp thuận làm nội dung cũ sai. Không tạo roadmap hoặc checklist tiến độ song song.
2. Khi bắt đầu M2, tạo/cập nhật **`reports/M2_DATA_PREPROCESSING_NOTES.md`** làm bản ghi phục vụ chương dữ liệu/tiền xử lý, khác với trạng thái điều phối. Viết bằng tiếng Việt, tổng hợp gọn nhưng đủ tái sử dụng:
   - nguồn/DOI/giấy phép/ghi công, hash, sheet/header, schema/quy mô và đặc trưng dữ liệu thật;
   - quyết định, căn cứ/trade-off, parser/mapping/policy và các cách xử lý chất lượng;
   - bảng trước–sau có mẫu số/cân bằng counts, phân phối giỏ và ví dụ dòng/hóa đơn có lineage;
   - môi trường/config/code revision và hash thay đổi chưa commit, lệnh tái tạo, run/dataset/basket-set ID;
   - thời gian/RAM/đĩa thực đo, cách đo, lỗi → nguyên nhân → sửa → kiểm chứng;
   - kiểm tra đạt/chưa đạt, giới hạn, kết quả review thực tế, gợi ý bảng/hình có ích và link evidence.
   Phân biệt số dự kiến, audit lịch sử, fixture, pipeline toàn nguồn và nghiệm thu con người; trường chưa đo/chưa xác nhận ghi rõ như vậy. Không tự viết kết luận chất lượng FP-Growth hoặc phần trăm đóng góp.
3. Receipt/log/counts chi tiết/measurement output giữ dưới `artifacts/m2/` hoặc vị trí output hiện có phù hợp, ngoài Git; dataset/processed/DB/cache cũng ngoài Git. Source/config example/hướng dẫn và bản ghi báo cáo đã rút gọn được version control. Ghi run/hash/thời điểm trong bản ghi để truy vết ngay cả khi clone không mang evidence cục bộ; không gửi secrets, dữ liệu cá nhân hoặc dump toàn nguồn lên Git.
4. Với claim quan trọng, ghi evidence tương ứng tại lúc chạy; hình/bảng phải có đơn vị, scope, policy/run. Không dựng screenshot/log, điền thời gian/RAM ước lượng như đo thật hoặc sửa audit lịch sử thành kết quả mới.

## 7. Nghiệm thu, an toàn và bàn giao

- M2-AC1: P-01/counts/lineage đúng nguồn; AC2: không loại mặc định Customer ID thiếu/không gộp theo tên và có căn cứ mapping/ngoại lệ; AC3: giỏ unique, chất lượng/summaries khớp đối chiếu và counts P-02 tính thật. Đọc nguyên văn AC/DoD tại file 13 để đối chiếu đầy đủ.
- M2 DoD cần **TV2 review thật**, nguồn giữ nguyên, lineage/hướng dẫn tái tạo/counts rõ; U-25 đã xác nhận. Không lấy Agent/test/build thay review TV2; hỏi đúng phần nghiệm thu còn thiếu sau khi có kết quả cụ thể để review, không hỏi tôi xác nhận trước kết quả.
- Không sửa câu nguồn/282 Requirement ID/trọng số; giữ audit lịch sử và nguồn XLSX/ZIP/Word. Không reset/clean/drop DB/xóa đáng kể dữ liệu/ghi đè secrets, commit/push hoặc đổi Git toàn máy khi chưa có chỉ dẫn rõ.
- Lifecycle phải đọc receipt hiện tại và kiểm tra đúng executable/thời điểm/PID/đích của process dự án trước Start/Stop; không đọc được thông tin process/CIM vì giới hạn quyền thì ghi chưa xác định, không suy là process đã dừng.
- Kiểm thử theo rủi ro: typed tuple/P-01/lineage, retry/conflict/partial import, precision/tổng/ngày, mapping/giỏ/đối chiếu nguồn và các phần bị ảnh hưởng. Phân biệt lỗi có sẵn với regression; không sửa expectation để khớp implementation sai.
- Nếu bị chặn quyết định/hạ tầng/tài nguyên: ghi checkpoint, lỗi và evidence thật; tiếp tục phần độc lập, không bịa PASS hoặc tự chuyển sang mốc khác để né blocker. Quyền chạy tool/mạng tuân theo môi trường, không bypass sandbox.
- Khi kết thúc: đọc diff cuối, kiểm tra `.gitignore`, hash nguồn và artifact bị loại; cập nhật bản ghi báo cáo cùng STATE/checklist; nêu phần thực hiện, quyết định, lệnh/kết quả kiểm chứng, phần chưa kiểm chứng, review còn thiếu và việc kế tiếp. Chỉ tick M2 khi đủ AC/DoD. **Bàn giao rồi dừng trước M3/M4**, không tự commit/push.

Hãy bắt đầu đọc và triển khai M2 theo các chỉ dẫn trên; không yêu cầu tôi kể lại ngữ cảnh đã có trong repository.
