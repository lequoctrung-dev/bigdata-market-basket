# Prompt bắt đầu M3 trong thread mới

Ngày soạn: **15/10/2026**. Đây là prompt bàn giao sau khi M2 đã đóng; phiên soạn prompt **không triển khai M3**. Copy phần sau dấu phân cách vào thread mới trong cùng project, hoặc dùng lời dẫn cuối file để yêu cầu thread đó đọc đầy đủ file này.

---

Bạn tiếp tục đồ án Nhập môn Big Data tại workspace:
`D:\University\Semester7\BigData\DoAn`.

Tôi giao bạn thực hiện **M3 — FP-Growth, baseline và đánh giá trên phần phát triển**, gồm **M3-T1–M3-T4** tại `requirements-review/13_MASTER_IMPLEMENTATION_PLAN.md`, nghiệm thu theo `requirements-review/14_MILESTONE_CHECKLIST.md`.

Hãy đọc đủ ngữ cảnh cần thiết, triển khai trực tiếp vào repository và kiểm chứng bằng chạy thật. **Không chỉ lập kế hoạch.** Tự giải quyết chi tiết kỹ thuật có căn cứ trong phạm vi đã duyệt/QD-08; nếu thiếu lựa chọn quan trọng làm đổi protocol, kiến trúc, schema/semantics lớn hoặc scope, trình phương án cụ thể, trade-off và đề nghị rồi chờ tôi chọn trước phần phụ thuộc; vẫn tiếp tục phần độc lập. Không tự bịa hoặc hỏi lại quyết định đã chốt.

**Chỉ làm M3**, bàn giao đạt hoặc checkpoint chưa đạt rồi dừng. Không tự mở M4/M5, chạy final evaluation, commit hoặc push. Trong suốt quá trình phải ghi thông tin phục vụ báo cáo vào hồ sơ repository, không chỉ giữ trong chat.

## 1. Đọc đầu phiên và xác minh trạng thái

1. Đọc đầy đủ `AGENTS.md`, `README.md`, `STATE.md`; kiểm tra branch/HEAD/status và diff liên quan. Khi soạn prompt này, branch `main`, HEAD `d975e6ce768156b7b1549bcb64eabdb940268085`; toàn bộ thay đổi M2 còn chưa commit và có file untracked. Đây là snapshot, phải kiểm tra lại; không tự suy tôi đã commit/push hoặc bỏ thay đổi có sẵn.
2. Đọc đầy đủ `07_CONFIRMED_SCOPE.md`, checklist 14 và mục M3/quy tắc nghiệm thu/cổng/quyết định QD-08 của Master Plan 13. Các file đánh số nằm trong `requirements-review/`. Đọc U mới hơn nếu có; trạng thái đã xác nhận mới ưu tiên hơn snapshot cũ.
3. Đọc file 11 mục 3/5/8/10: giỏ, split, catalog/tên từ train, P-03, mẫu số metrics và ranking. Đọc file 12 mục 9–12/15: schema/khóa/kiểu, manifest theo stage, retry/công bố và encoding M2. Tra file 01/02/03/09/15 theo Requirement ID của M3; không sửa câu nguồn, 282 ID hoặc trọng số. Khi cần thuật toán/API/version, đọc code/dependency thực tế và tài liệu chính thức phù hợp phiên bản; không suy API theo trí nhớ.
4. Đọc **`reports/M2_DATA_PREPROCESSING_NOTES.md`**, receipt đóng M2 cuối checklist 14 và `pipeline/README.md` mục 6. Xem mã `pipeline/m2_source.py`, `m2_pipeline.py`, `m2_runtime.py`, `m2_verify_mongo.py`, `m2_final_verify.py`, `test_m2_contract.py`; các helper lifecycle/measurement tại `scripts/`.
5. Đọc phần có ích của `sample_fixture.py`, `sample_pipeline.py`, `test_sample_fixture.py` cùng caller/DTO/ranking tests Java tại `web/`. Mẫu M1 giúp kiểm cơ chế, không phải cấu hình/đáp án M3. Không xây UI M4 trong mốc này.
6. Đối chiếu receipt/hash/IDs với artifact hiện có trước khi tái sử dụng; nếu thiếu artifact sau clone, dựa kết luận đã ghi và tái tạo đúng phần cần thiết. Không dựng receipt thay thế, tự reset dữ liệu hoặc mặc định phải chạy lại toàn M2.

Sau khi đọc, báo ngắn trạng thái, kế hoạch thực hiện M3, lựa chọn kỹ thuật sẽ chốt theo QD-08 và cách lưu evidence; sau đó triển khai trong phạm vi đã rõ.

## 2. M0/M1/M2 đã đóng — không hỏi lại nghiệm thu

- **M0 đóng 14/10/2026**: contract `m0-contract-v1`; U-27 run bất biến + active/version/chín collection, U-28 decimal text, U-29 dashboard hàng hóa + audit toàn nguồn; review hai thành viên U-30.
- **M1 đóng 15/10/2026**: luồng mẫu MongoDB → PySpark/FP-Growth → MongoDB → MVC/Thymeleaf trên TV1, U-33 miễn receipt TV2 riêng M1; U-35 xác nhận demo/học/giải thích/review, không còn điểm sửa. Không ghi TV2 đã chạy. Tham số và 5 giỏ/7 itemsets/9 luật của M1 là synthetic fixture.
- **M2 đóng 15/10/2026**: pipeline tiền xử lý toàn nguồn TV1 và postcheck đạt; **U-38 xác nhận TV2 đã review/chấp thuận, không còn điểm sửa** về schema/lineage, mapping/counts, giỏ/tiền/hóa đơn mẫu và tái tạo. **Không còn confirm/demo riêng cần bổ sung để đóng M2.** Các trường `PENDING_TV2` trong receipt runtime là snapshot trước U-38, không phải blocker hiện tại; giữ receipt bất biến và đọc review receipt riêng.
- Chưa full READY re-import lại cả workbook: retry thật đã kiểm 2.000 dòng, partial/retry/conflict có probe riêng. Chưa web/Java đọc dataset thật, chưa split/model/baseline/evaluation toàn nguồn và chưa runtime máy TV2. Các giới hạn này đã ghi khi đóng M2, không tự biến thành thiếu AC M2 mới.
- Full run/demo thật riêng cả hai máy tại **M6** vẫn giữ theo U-15/U-22; review TV2 hoặc receipt TV1 không thay runtime TV2. Không hỏi lại dataset/đề tài được GV chấp thuận theo U-25, khung B/quy cách A theo U-26, vai trò U-23 hoặc ngoại lệ M1.

## 3. Đầu vào M2 được phép tái sử dụng

| Trường | Snapshot đã nghiệm thu |
| --- | --- |
| Nguồn | `data/raw/online-retail-ii/online_retail_II.xlsx`, 45.622.278 byte; Daqing Chen, UCI Online Retail II, DOI 10.24432/C5CG6D, CC BY 4.0 |
| Dataset/source SHA-256 | `bcbe73b35f5b7babf197fb0cb983a11f5d9ff929078d4aa53d171b1f2df2e980` |
| Run tiền xử lý M2 hợp lệ | `d7fb3f21-115f-4793-a5fe-5c40b6da64cd` |
| Basket set hợp lệ | `cae0d9e763ef38a086966d829fdeba9272f4d7fda7b61791bee9e9ba04b3287a` |
| Phiên bản | Parser `openpyxl-3.1.5-typed-v1`; schema `m0-contract-v1`; storage `m2-bson-counts-int64-v1`; policy `p01-first-p02-test-v1` |
| Stage counts | Raw 1.067.371 → P-01 1.033.036 → positive_valid 1.007.913 → merchandise 1.003.357 |
| Loại tuần tự | Trùng 34.335; không mua dương/hợp lệ 25.123; P-02/TEST 4.556 |
| Giỏ/item | 39.516 giỏ; 4.895 item; 3.208 giỏ một item; 36.308 từ hai item; max 1.108 item/giỏ, không cắt |
| Thiếu khách | Giữ 226.761 dòng merchandise thiếu Customer ID |
| Summary toàn kỳ | 5.347 documents; giá trị mua dương hàng hóa exact 19.643.861,637 GBP, không phải doanh thu ròng |
| Kiểu decimal đã đo | Quantity (5,0), Price (8,3), product (14,3), sum (24,3); biên Mongo tiền là text, counts/vị trí là BSON Int64 |
| Checksum giỏ | `982ab870ab7f8118cdada770c9269fa0e464f2a789c778f9f0289ad852b8c05d` |
| Output dòng | `data/processed/m2/<basket_set_id>/<run_id>/retained-lines.jsonl`: 1.033.036 dòng/413.222.079 byte; SHA-256 `82ddde19db72b295d723ebb3ca1068ccbabf3a44a49d8ab396598842e5bc5c74` |

Hai sheet `Year 2009-2010` / `Year 2010-2011`: 525.461 / 541.910 dòng. Header đúng thứ tự: Invoice, StockCode, Description, Quantity, InvoiceDate, Price, Customer ID, Country. P-01 so tám ô có kiểu trước trim, giữ vị trí đầu `(sheet_index,source_row)`; number 1/1.0 bằng nhau nhưng number khác text. Source cells đầy đủ nằm Mongo archive; file dòng là đầu ra tiền xử lý có flags/lineage, không phải bản sao bytes XLSX. Nếu dùng file này, phải lọc đúng merchandise theo flags/policy, không lấy cả retained làm giỏ train.

P-02/U-21 giữ nguyên mapping phí/dịch vụ/điều chỉnh/Manual/voucher/TEST, không regex loại toàn bộ mã chữ. Không gộp sản phẩm theo tên hoặc loại mặc định khách thiếu. Đã audit trim `47503J ` tại sheet 0/row 260888 cùng mô tả với `47503J`; raw vẫn giữ khác biệt trước P-01. Thời gian hóa đơn local, timezone UNKNOWN; giỏ lấy min trên dòng hàng còn lại, không prefix sheet. Giữ giỏ một item và tail lớn.

**Đây là toàn kỳ tiền xử lý, chưa phải train đã freeze.** Không lấy 4.895 item, summaries/frequency/tên toàn kỳ làm train catalog/baseline. Đọc basket set đúng ID từ MongoDB; nếu cần tên/line data, nối đúng hóa đơn train với dòng sau P-01/P-02 có lineage, không đếm lại duplicate archive.

Evidence cục bộ ở `artifacts/m2/`: `pipeline-d7fb3f21-115f-4793-a5fe-5c40b6da64cd.json`, `final-verification-d7fb3f21-115f-4793-a5fe-5c40b6da64cd.json`, `resources-d7fb3f21-115f-4793-a5fe-5c40b6da64cd.json`, `review-20261015.json`, `audit-source-v1/`, `hand-invoices.json`, `unit-final-20261015T082201.*`, `repository-final-verification.json`. Những file này bị Git ignore; đọc schema/hash thực tế, không suy thiếu cục bộ thành M2 chưa từng chạy.

Không chọn run thử `34f6dd24-c5e8-42e6-80c4-3db26876d37c` hoặc `7ea685bc-c5e5-4c37-a53f-db57663c4f13`: lượt đầu FAILED do key BSON số nguyên; lượt sau PASS các checks lúc đó nhưng postcheck đã đánh FAILED do count int32. Giữ receipt/output cũ để truy vết, không sửa lịch sử hoặc chọn “run mới nhất” mù.

## 4. Môi trường, lifecycle và điểm phải kiểm trước tái sử dụng

- U-37 cấp namespace dự án M2: loopback `127.0.0.1:27019`, database `bigdata_m2`, dbpath `artifacts/m2/mongo-data`. Ưu tiên tái sử dụng nguồn/basket set đã nghiệm thu và ghi output M3 dưới **run UUID mới, đúng collection contract**, cô lập theo run; không đổi tên DB chỉ theo milestone. Trước ghi đối chiếu quyền/scope hiện tại; nếu cần namespace mới, đích khác hoặc thay cơ chế/schema lớn chưa được cấp, trình lựa chọn cụ thể và chờ quyết định. Không ghi dịch vụ 27017 hoặc mẫu M1/27018.
- Snapshot cuối M2: mongod 27019 đã shutdown đúng receipt, dữ liệu giữ nguyên; 27018/8081 đóng; 27017/PID 5572 còn nghe. Receipt `stop-20261015T084344.json` / `preflight-20261015T084347.json`. Phải kiểm lại PID/executable/hash/start/command/listener trước Start/Stop; không dùng PID lịch sử hoặc kill theo tên/cổng. Chưa đọc được CIM/process do sandbox không được suy đã dừng; dùng cơ chế xin quyền tool, không bypass policy.
- Đã chạy TV1: Windows 11 x64/i5-13500H/RAM 15,63 GiB; JDK 17.0.12, Python 3.14.6, PySpark 4.2.0/Scala 2.13.18, connector 11.1.0/driver Spark 5.1.4, PyMongo 4.18.3, NumPy 2.5.4, openpyxl 3.1.5, psutil 7.0.0; Maven portable 3.9.16, Boot 4.1.1/Data MongoDB 5.1.1/driver web 5.8.1. Đọc dependency và kiểm tra thực tế; không nâng cấp/cài toàn máy hoặc suy môi trường TV2.
- M2 Spark cuối local[2], heap 1280m, shuffle 16, adaptive coalesce tắt, ANSI bật/không mất decimal precision. Wall 301,032 giây; sampled peak RSS Python/launcher 195,27 MiB, JVM 1.717,21 MiB, Mongo 377,06 MiB, combined 2.272,68 MiB. Đây là số M2, **không chứng minh fit FP-Growth vừa RAM**. Đo lại available RAM/đĩa và tài nguyên fit/evaluation từng bước, có giới hạn phép đo.
- Không dùng `spark.jars.packages` mù: M1/M2 nạp năm JAR chính thức từ `tmp/connector` qua local classpath trước gateway vì fetch/addFile từng lỗi chmod/winutils. Không tải DLL/winutils lạ, patch bỏ quyền hoặc đổi execution policy. `.venv`, JAR/cache/Mongo/scratch ngoài Git. Helper đã dùng PowerShell 7; không đổi PATH/registry toàn máy.
- BSON khác JSON: small Python int có thể thành int32, equality Python int == Int64 không chứng minh kiểu lưu; ghi counts/frequency Int64 và kiểm `$type` thật. Key dict BSON phải string. `bson_counts`/test hiện có là điểm tham khảo, không dùng Int64 trực tiếp khi Spark schema đòi Python int cho LongType. Giữ decimal text/BigDecimal contract và local time.
- **Đọc caller trước tái dùng helper M2:** `m2_pipeline.py` và `m2_final_verify.py` kiểm namespace chưa có items/model/publication; checker cuối còn có nhánh thay trạng thái checkpoint cũ. Chạy lại máy móc sau M3 có thể lỗi vì model hợp lệ đã tồn tại, không chứng minh nguồn hỏng. Tách kiểm input/basket set phù hợp stage/read-only cho M3 nếu cần; không gỡ guard đại trà, reset collection, sửa receipt M2 hoặc chạy checker có mutation ngoài ý muốn.
- Run M2 `status=VALIDATED`, `basket_set_status=READY`, stage PREPROCESSING; không phải model run READY, không có active pointer. Không sửa run M2 thành run M3. Xem contract theo stage khi tạo model run mới; output đủ/khóa bất biến mới VALIDATED/READY. Nếu cần công bố run DEVELOPMENT để web đọc ở mốc sau, dùng đúng U-27/CAS, đủ manifest và nhãn DEVELOPMENT; không xây UI M4 hoặc mở final M5 để làm đủ output.

## 5. M3-T1 — split và giao thức có phiên bản

- Chọn split hóa đơn hoàn chỉnh theo thời gian local thành train/lịch sử, dev và test cuối, biên `[start,end)` rõ. Cùng hóa đơn chỉ một tập; timestamp bằng mốc xử lý cố định. Kiểm coverage/count/checksum và invoice overlap = 0; giỏ một item vẫn trong basket set/split, báo riêng khi không đủ điều kiện mask.
- **QD-08 đã giao nhóm chọn có căn cứ** K/seed/mốc chia/tham số/comparator trong P-03; không cần xin duyệt từng config nhỏ. Dựa metadata thời gian/quy mô, train/dev và tài nguyên thực tế để chốt, ghi rationale/version trước dùng. Không bịa rằng K/seed/mốc/tham số đã được chọn ở M1/M2. Đổi giao thức, bỏ nghĩa vụ, thêm fallback hoặc đổi stack/scope mới là lựa chọn lớn phải hỏi.
- Tách test cuối ngay khi định nghĩa split. Chỉ dùng metadata/counts để kiểm ranh giới/bao phủ; không tạo truy vấn/đánh giá test, xem score hoặc dùng phân bố item/target test để tune. Không chọn mốc hay đổi split sau khi xem test metrics. M5 mới final evaluation theo freeze.
- Với dev có ≥2 item: ẩn đúng một item bằng thuật toán xác định từ seed + identity hóa đơn + thứ tự item canonical, có version; đổi partition/thứ tự đọc vẫn cùng target/query. Luật và baseline dùng đúng cùng query/target/K/catalog train. Không loại target mới ngoài train hoặc query không có luật để làm đẹp mẫu số; báo riêng item mới ở target/context, không biến unknown offline thành mất truy vấn âm thầm.
- Ghi định nghĩa Recall@K và tỷ lệ có gợi ý cùng numerator/denominator. Một target: Recall trung bình = số query hit/N; có gợi ý = số query trả ít nhất một item/N. Query không có gợi ý góp 0; N=0 là NOT_APPLICABLE. Nếu bổ sung Precision@K, ghi rõ mẫu số K đã quy định, không thay bằng số kết quả trả về để làm đẹp điểm.

## 6. M3-T2/T3 — fit train, baseline và kiểm đúng gợi ý

- Fit FP-Growth **chỉ train**. Train chứa giỏ một item; không cắt giỏ lớn/vứt item hiếm tự ý. Không fit lại toàn nguồn để phục vụ web hoặc lấy dev/test làm nguồn fit/frequency/name.
- Baseline xếp theo **số giỏ train chứa item**, tie StockCode tăng; không theo tổng Quantity hoặc tần suất dòng. Catalog gồm item train đủ policy kể cả item không có luật; mô tả lấy modal description không rỗng từ dòng train đúng policy, trim ngoài, tie Unicode, thiếu hiển thị mã. Không dùng tên/counts toàn kỳ M2 để lấp catalog.
- Kiểm itemset/rule frequency, support/confidence/lift và mẫu số train bằng ví dụ độc lập. Đọc schema output Spark thật, chuyển sang contract consequent scalar đúng nghĩa; không âm thầm lấy phần tử đầu nếu dữ liệu không đáp ứng contract. Counts Int64, metrics hữu hạn/miền hợp lệ, array unique/canonical, ID/rule key có collision check theo file 12.
- Luật chỉ áp khi **mọi** item tiền đề nằm trong query. Loại item đã có và dedup ứng viên; với mỗi item lấy luật tốt nhất theo confidence giảm → lift giảm → support giảm → antecedent Unicode tăng. Xếp ứng viên thêm tie StockCode rồi antecedent đúng contract; không làm tròn trước ranking hoặc đổi comparator thành “gần bằng”. Không fallback mặc định, không tự thêm lift>1 hay mô hình khác.
- Tạo ca chung có expected tính độc lập: nhiều item tiền đề, thiếu một tiền đề, item đã có, nhiều luật cùng ứng viên, tie/prefix antecedent/Unicode, rỗng, unknown/new item, không có luật, 0 luật, K lớn hơn số ứng viên, empty denominator. So metrics với tính tay; có ca thật từ train/dev với lineage. Phân biệt fixture/probe với kết quả development toàn nguồn.
- Dùng code/test ranking Java hiện có để đối chiếu trong phạm vi M3-T3 nếu cần; giữ tương thích và cung cấp ca/DTO/run cho TV2. Không mở dashboard/forms/website dữ liệu thật của M4 hoặc trộn namespace mẫu M1 để demo M3.

## 7. M3-T4 — development, tài nguyên và freeze

- Chạy một tập thử cấu hình có căn cứ và giới hạn tài nguyên/thời gian rõ trên train/dev; ghi **mọi lượt đã thử**, cả fail/OOM/không luật. Không chạy grid vô hạn hoặc lấy riêng điểm đẹp. Giới hạn vận hành không phải ngưỡng đạt khoa học.
- Đọc tài liệu chính thức của bản Spark đang dùng về tham số/chi phí fit, kể cả vai trò minSupport/minConfidence; không giả định đổi confidence chữa được bùng tập phổ biến. Đo fit/read/write/eval và JVM/Python riêng. Khi quá tài nguyên, giữ evidence, điều chỉnh cấu hình trên development hoặc bàn giao checkpoint; không cắt giỏ, chuyển stack, fit test hoặc giảm dữ liệu lặng lẽ.
- So sánh luật thuần và baseline cùng giao thức, ghi Recall@K/tỷ lệ có gợi ý, counts và phân tích giỏ/item mới/không luật, chi phí. Không ép FP-Growth thắng hoặc tạo SLA/score tối thiểu chưa có trong AC.
- Chọn cấu hình theo rationale/selection rule công khai dựa development và tài nguyên, ghi hạn chế nếu điểm thấp/coverage thấp. Freeze split/K/seed/mask/ranking/policy/catalog nguồn train/tham số/schema/code version và hash, kèm kết quả dùng để chọn. Sau freeze không sửa dựa trên test; thay freeze phải tạo phiên bản và giải thích trong đúng scope được giao.
- Sinh model/run outputs, baseline/evaluation harness, manifest DEVELOPMENT và ca chung, hướng dẫn tái tạo để web đọc run thật ở mốc sau. Kết quả final ghi NOT_RUN, không điền 0 giả hoặc copy dev score sang final. Không sửa con trỏ mù, overwrite/drop output hoặc công bố run thiếu field/output theo stage; giữ run lỗi/phiên bản cũ.

## 8. Ghi thông tin báo cáo đồng thời khi thực hiện

Ngay khi bắt đầu M3, tạo/cập nhật **`reports/M3_MODEL_DEVELOPMENT_NOTES.md`**; giữ bản M2 là bằng chứng tiền xử lý đã nghiệm thu, không thay số M2 bằng số train. Bản ghi M3 là tài liệu kỹ thuật phục vụ báo cáo, không tạo roadmap/checklist tiến độ song song.

Ghi tại lúc quyết định/chạy, không đợi cuối phiên dựng lại:

1. Nguồn/citation/giấy phép và lý thuyết FP-Growth/support/confidence/lift/baseline; nguồn tài liệu chính thức, phiên bản và ví dụ tính tay. Không copy nội dung dài hoặc tự kết luận giá trị kinh doanh từ offline recall.
2. Dataset/basket-set/run/config/trial ID; split local/biên/coverage/checksum/no-overlap; train/dev/test counts theo scope, catalog/names/frequency từ train; K/seed/mask/ranking và rationale/ai xác nhận, version/hash.
3. Bảng tất cả thử nghiệm development: tham số, train denominator, itemsets/rules, eligible queries, targets/context mới ngoài train, query có gợi ý/hit, Recall@K/tỷ lệ có gợi ý từng phương pháp, numerator/denominator và so sánh cùng điều kiện. Tách fixture, train/dev thực, failed trials và test NOT_RUN.
4. Môi trường/config/code revision và hash mã chưa commit, UTC start/end, lệnh tái tạo, thời gian từng bước, sampled peak RSS JVM/Python/Mongo, đĩa/scratch và phương pháp/đơn vị/giới hạn đo. Không lấy heap/cache config/RAM trống làm peak usage hoặc wall time làm giờ-người.
5. Lỗi → evidence → nguyên nhân → cách sửa → kiểm chứng lại/regression; quyết định chọn cấu hình/freeze và trade-off, bảng/hình có ích kèm run/scope/đơn vị. Không xóa lượt lỗi, sửa audit cũ hoặc chỉ báo lượt tốt nhất.
6. AC/DoD đạt/chưa đạt, review TV2 thực tế, phần chưa kiểm chứng, lý do checkpoint và handoff. Không gán công việc Agent thành đóng góp cá nhân hoặc phần trăm/giờ chưa được xác nhận.

Chi tiết log/receipt/query-level outputs/measurements/model/dataset tại **`artifacts/m3/`** hoặc vị trí output ngoài Git phù hợp; source/config example/hướng dẫn/bản ghi báo cáo rút gọn được version control, không chứa secrets/dữ liệu cá nhân. Mỗi claim chính có evidence/hash/ID để clone không mang artifact vẫn truy vết được. Dùng helper đo có ích sau khi đọc; không giả rằng helper M2 đã bao phủ chi phí FP-Growth/evaluation M3.

Cập nhật `STATE.md` ngắn, checklist 14 theo evidence; file 07 khi có quyết định người dùng mới, file 11/12/13 khi nội dung thay đổi được chấp thuận làm chúng sai. Các lựa chọn kỹ thuật QD-08 do nhóm tự chọn phải ghi thành lựa chọn kỹ thuật có rationale, không gán thành người dùng đã xác nhận.

## 9. Nghiệm thu và ranh giới bàn giao

Đọc nguyên văn AC/DoD M3 trong Master Plan 13; tối thiểu:

- **M3-AC1:** đủ tiền đề, loại item đã có/ứng viên trùng; ranking/tie nhất quán, không fallback.
- **M3-AC2:** luật và baseline cùng query/catalog/K/lịch sử; giỏ một item, item mới và không luật tính/báo đúng.
- **M3-AC3:** cấu hình chọn bằng development, test cuối chưa dùng; không ép FP-Growth vượt baseline/đạt score tự đặt.
- **DoD:** **TV2 tính lại mẫu metrics và review split thật**; lưu configuration/source/policy version, kết quả phát triển khoa học/runtime truy vết được. U-38 chỉ là review M2, không thay review M3. Chuẩn bị kết quả cụ thể để TV2 review rồi hỏi phần còn thiếu, không xin xác nhận trước khi có evidence. Không lấy Agent/build/fixture thay người review.

Không cần demo lại M2 hoặc yêu cầu thêm receipt TV2 M1 đã được miễn. Final evaluation M5 và full run/demo hai máy M6 chưa thuộc M3. Nếu bị chặn lựa chọn/hạ tầng/tài nguyên/review thì ghi checkpoint đúng sự thật và phần có thể làm độc lập, không mở milestone khác để né blocker.

Kết thúc: đọc diff cuối; kiểm `.gitignore`, nguồn/hash, dữ liệu/DB/output/secrets ngoài Git; kiểm lifecycle đúng receipt, giữ dữ liệu; cập nhật M3 notes/STATE/checklist/decisions tương ứng và hướng dẫn tái tạo. Báo rõ thay đổi, quyết định, commands/results, phần chưa kiểm chứng/review còn thiếu. Không reset/clean/drop/xóa đáng kể dữ liệu, commit/push, gửi GV/nộp Classroom hoặc đổi phần mềm toàn máy khi chưa được cấp rõ. **Bàn giao M3 đạt hoặc checkpoint chưa đạt rồi dừng trước M4/M5.**

Hãy bắt đầu đọc và thực hiện M3 theo các chỉ dẫn trên; không yêu cầu tôi kể lại ngữ cảnh đã có trong repository.

---

Lời dẫn ngắn để paste vào thread mới thay vì copy toàn bộ phần prompt:

```text
Tôi giao bạn thực hiện M3 — FP-Growth, baseline và đánh giá trên phần phát triển tại D:\University\Semester7\BigData\DoAn. Hãy đọc đầy đủ requirements-review/M3_START_PROMPT.md, sau đó đọc tài liệu/mã nguồn được chỉ dẫn và triển khai, kiểm chứng thật đúng phạm vi. M0/M1/M2 đã đóng; U-38 đã xác nhận TV2 chấp thuận M2, không hỏi lại nghiệm thu M2. Trong quá trình làm phải ghi đồng thời nguồn/quyết định/protocol/config/counts/metrics/tài nguyên/lỗi/evidence và review vào reports/M3_MODEL_DEVELOPMENT_NOTES.md cùng hồ sơ repository theo prompt. Không chỉ lập kế hoạch, không tự bịa hoặc hỏi lại quyết định đã chốt; lựa chọn quan trọng ngoài phạm vi đã duyệt thì trình phương án có căn cứ và chờ trước phần phụ thuộc. Chỉ làm M3, bàn giao đạt hoặc checkpoint chưa đạt rồi dừng; không tự mở M4/M5, chạy final evaluation, commit hoặc push.
```
