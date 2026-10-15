# Ghi chép phát triển mô hình M3

Bắt đầu/cập nhật **15/10/2026**, theo giao việc M3-T1–T4/U-40. **M3 đã đóng**: runtime development/freeze TV1 PASS và TV2 review split/tính lại mẫu metrics chấp thuận, không còn điểm sửa theo người dùng **U-41**. M0/M1/M2 giữ đã đóng. Các phần phía dưới ghi theo thời điểm thực hiện; receipt PENDING_TV2 giữ snapshot trước U-41. Final evaluation **NOT_RUN**; không mở M4/M5, commit/push. Agent thực hiện kỹ thuật, không tự gán giờ hay đóng góp thành viên.

## Nguồn, phương pháp và phạm vi

Online Retail II, Daqing Chen, DOI [10.24432/C5CG6D](https://doi.org/10.24432/C5CG6D), [UCI, CC BY 4.0](https://archive.ics.uci.edu/dataset/502/online+retail+ii). Tái sử dụng preprocessing run `d7fb3f21-115f-4793-a5fe-5c40b6da64cd`, basket set `cae0d9e763ef38a086966d829fdeba9272f4d7fda7b61791bee9e9ba04b3287a`; giữ nguyên source/policy và 39.516 giỏ, kể cả giỏ một item/tail lớn. Counts M2 toàn kỳ không được gọi là train counts.

[Spark 4.2.0 FP-Growth](https://spark.apache.org/docs/4.2.0/ml-frequent-pattern-mining.html), đối chiếu 15/10/2026: FP-tree nén các tiền tố chung, khai phá các cây điều kiện; Spark dùng PFP phân việc theo suffix. minSupport quyết định tập phổ biến; minConfidence chỉ lọc tạo luật, không giảm chi phí khai phá tập phổ biến. consequent Spark là array một phần tử: phải kiểm trước chuyển scalar. Không dùng thứ tự predictions của transform làm Top-K contract.

Với N giỏ train: support(A→b)=count(A∪{b})/N, confidence=count(A∪{b})/count(A), lift=confidence/(count(b)/N). Ví dụ độc lập 5 giỏ M1: count(A)=4, count(B)=3, count(AB)=3; support=.6, confidence A→B=.75, lift=1.25. Đây là fixture, không là kết quả train thật. Lift không chứng minh nhân quả; offline Recall không chứng minh tăng doanh thu.

Baseline đếm số giỏ train chứa item, tie Unicode StockCode; tên là mô tả modal không rỗng của dòng merchandise train, tie Unicode, thiếu dùng mã. Luật đủ mọi tiền đề, bỏ item đã có, mỗi ứng viên giữ luật tốt nhất confidence/lift/support/antecedent; xếp thêm StockCode/antecedent. Không fallback, không ngưỡng lift tự thêm, không làm tròn trước xếp hạng.

## Quan sát đầu phiên và quyết định trước thực nghiệm

Git sạch, branch main, HEAD `ddb8970a49167d3a913a4f64f033a9ec5ad2c3b6`; khác snapshot prompt. Dependency thực PySpark 4.2.0. Mongo 27019 đang chạy trước phiên; đã kiểm lifecycle bằng helper/CIM ngoài sandbox sau lỗi quyền CIM. Không khởi động lại hoặc tác động 27017/27018.

Preflight `artifacts/m2/preflight-20261015T094803.json`: Windows 11 x64/i5-13500H, tổng RAM 16.786.550.784 byte, available 675.553.280 byte, đĩa D trống 122.696.720.384 byte. Đây là snapshot tài nguyên, không peak fit. Phải đo lại trước fit; giữ checkpoint nếu không đủ vận hành. Bộ phiên bản pin hiện có, không cài/nâng cấp toàn máy.

Lựa chọn QD-08 do Agent triển khai trong quyền chọn kỹ thuật được giao; cần TV2 review, không gán là người dùng đã xác nhận. Dự kiến split train trước 01/07/2011, dev [01/07,01/10/2011), test từ 01/10/2011; dựa phạm vi hai năm và giữ trọn quý phát triển/quý cuối, không chọn bằng score test. Chốt sau kiểm metadata thời gian/coverage, trước tạo dev queries. K=5 (danh sách ngắn), seed=20261015; mask SHA-256 canonical [version,seed,invoice], integer modulo số item đã sort Unicode. Một query/target mỗi giỏ dev ≥2 item, không loại unknown. Recall=hits/N, có gợi ý=nonempty/N; N=0 là NOT_APPLICABLE, không ghi 0 giả.

Thử có giới hạn minSupport .03/.02/.01, minConfidence .3, partitions 8, local[2], heap 768m để khảo sát ngưỡng phổ biến giảm dần trong RAM máy; mỗi fit tối đa 600 giây bằng cancel job group, tối đa 200.000 outputs mỗi loại trước collect. Đây là giới hạn vận hành, không AC khoa học. Chọn Recall dev cao nhất, tie coverage, tie ít luật, tie support cao hơn; chỉ trong các lượt PASS đầy đủ. Không thay split/K/seed theo test. Evidence/receipt/query/resources ngoài Git tại artifacts/m3; cập nhật kết quả/lỗi ngay khi chạy.

## Kết quả và review

Chưa có kết quả M3 thực tại lúc tạo ghi chép. TV2 tính lại mẫu metrics/review split **PENDING**. Test cuối **NOT_RUN**.

### Chuẩn bị dữ liệu thật và regression — 15/10/2026

Preparation `artifacts/m3/preparation-7da29e52-53cf-4986-beff-dfaad251663c/`, receipt PASS 09:52:57 UTC. Nguồn XLSX/hash file 413.222.079 byte M2 và receipt Mongo khớp; không chạy lại checker M2 có mutation. Chỉ truy vấn invoice/time cho test; không lấy test items vào Spark/Python. Chốt protocol như trên trước dev queries.

| Phần | Giỏ | Giỏ một item | Giỏ tối đa | Khoảng local thực |
| --- | ---: | ---: | ---: | --- |
| Train | 29.335 | 2.503 | 703 | 01/12/2009 07:45–30/06/2011 20:08 |
| Development | 4.609 | 316 | 486 | 01/07/2011 08:16–30/09/2011 17:22 |
| Test cuối | 5.572 | Không đọc items | Không đọc items | 02/10/2011 10:32–09/12/2011 12:50 |

Coverage 39.516, invoice overlap=0. Catalog 4.556 item, 717.574 dòng merchandise **train**; đã tái dựng mọi giỏ train từ retained lines và kiểm item/line count/min local time. Tên modal/trim/tie theo dòng train. Dev 4.293 query đủ điều kiện mask; 316 giỏ một item vẫn ở split, không tham gia mẫu số mask.

Checksum SHA-256 train baskets `30c1402211c7149e343886824f6645e19d3ed6c37560cbebf28cdeec16a4f28b`; dev baskets `9787fb0223d446cf5ddeeac31603fc3d7e4219ea2625ae6ddd3e4ac3cef93992`; dev queries `b03f53d9165f9dd19879a8c0a0323d00897811066d56ec2d1b8bebe65cb47adf`; catalog `a99f74a37f3a99f003e9b79debc3325e3c58783a0bef18e242669541c6063b54`. Split invoice/time hashes từng phần trong preparation receipt; không gọi checksum M2 cũ là checksum mới đã đọc toàn bộ test items.

Preparation wrapper `preparation-20261015T095241.json`: 16,314 giây (hàm 13,972 giây), peak sampled RSS Python/launcher 262,45 MiB, JVM 0, Mongo 92,34 MiB, combined 354,57 MiB. Mẫu mỗi giây, RSS cộng shared pages, bỏ sót peak giữa mẫu. Snapshot logical bytes cuối artifacts/m3 21.386.199, Mongo dbpath 404.180.929; không là allocated bytes/peak usage riêng nguồn.

17 unittest Python đạt (7 M3, 10 regression M1/M2); Java 5 tests đạt, trong đó test M3 đọc 12 ca độc lập dùng chung `pipeline/m3_ranking_cases.json` với Python, kiểm cả đảo thứ tự luật. Không đổi ứng dụng web hoặc chạy UI M4. Lệnh Maven đầu thiếu cấu hình cache riêng nên sandbox chặn cache người dùng; chạy lại đúng cache dự án `-o -Dmaven.repo.local=.../tmp/maven-repository -f web/pom.xml test` đạt. Giữ log lỗi nếu có; không cài/nâng cấp stack.

Lượt trial-index 0 đầu: **FAIL trước Spark**, `AVAILABLE_RAM_OPERATIONAL_GUARD`, available 462.135.296 byte; measurement `trial-0-20261015T095531.json`, receipt UUID trong artifacts/m3. Không có itemsets/rules/metrics đã đo, không gọi số 0 hoặc kết quả support .03. Người dùng trả lời sẽ giải phóng RAM; tiếp tục hoàn thiện phần độc lập trong lúc chờ. Guard đòi available ≥1 GiB trước khởi tạo JVM, đây là giới hạn vận hành có thể fail chứ không ngưỡng chất lượng.

### Trial 0 chạy lại sau khi có RAM

RAM đo lại 4.234.305.536 byte trước gọi wrapper; mỗi trial còn tự đo guard trước JVM. Run `7c91893d-ada2-40b8-a1b8-f0db0abc7bda`, support .03/confidence .3, train N=29.335: **PASS** 118 itemsets/13 luật, tất cả frequency đếm độc lập bằng giao tập invoice train; mọi luật kiểm support/confidence/lift và completeness. Mongo readback payload/checksum và BSON Long đạt; run DEVELOPMENT READY, không publication.

Dev N=4.293: luật hit 62, có gợi ý 1.146, Recall@5=0,014442115071045888, tỷ lệ có gợi ý=0,2669461914744934. Baseline cùng queries/catalog/K: hit 109, có gợi ý 4.293, Recall@5=0,025390170044258094, coverage=1. Target mới 265; 1.586 query có context mới với 6.287 occurrence item mới. Không bỏ các query này. Đây là kết quả development thật đầu tiên, chưa chọn cấu hình; test NOT_RUN. Receipt/JSONL/measurement `trial-0-retry-20261015T095901.json`, resources từng bước dưới UUID run. Lượt fail guard `741d89c1-f6c7-4060-b16b-82c17b240b65` giữ nguyên.

### Trial 1

Run `da870aec-d7f9-4c6e-ba89-52a24b17d0fb`, support .02/confidence .3: **PASS**, 334 itemsets/91 luật. N train 29.335/N dev 4.293 giữ nguyên; luật hit 215, có gợi ý 2.334, Recall@5=0,05008152806894945, coverage=0,543675751222921; baseline vẫn 109/4.293 hit và 4.293/4.293 có gợi ý. Các subgroup/new items cùng protocol, không loại target mới. Wall wrapper 80,784 giây, hàm 77,480 giây; measurement `trial-1-20261015T100113.json`, resources cùng run. Trial 2 support .01 đang chạy, chưa chọn/freeze. Postcheck trial 0 replay mọi prediction/metrics và kiểm Mongo/M2 theo stage đã PASS (`verify-0-20261015T100331.json`).

### Trial 2 lỗi stack và điều chỉnh vận hành trước retry

Run `63989ecb-b6d8-4025-8174-885305d44c15` **FAILED**, measurement `trial-2-20261015T100305.json`. Hàm 48,081 giây; lỗi thật đầu `java.lang.StackOverflowError` ở ObjectInputStream/Scala DefaultSerializationProxy trong task stage 17 khi count itemsets, **không có căn cứ gọi đây là heap OOM**. Gateway chết tạo lỗi ConnectionRefused lúc cleanup; lỗi gốc vẫn trong receipt/DB. Chưa có kết quả metrics .01, không chọn số đẹp hoặc xóa run lỗi.

Đối chiếu [Spark 4.2.0 JVM launch config](https://spark.apache.org/docs/4.2.0/configuration.html#runtime-environment) và [JDK 17 java -Xss](https://docs.oracle.com/en/java/javase/17/docs/specs/man/java.html), 15/10/2026. Chọn thử một lần tăng stack mỗi thread JVM thành `-Xss4m` trước gateway launch qua spark.driver.extraJavaOptions; heap vẫn 768m, local[2], không đổi dữ liệu/protocol/support/confidence. Đây là giả thuyết sửa giới hạn stack dựa trace, phải kiểm lại runtime; không hứa chữa mọi lỗi. Ghi JVM input arguments/max heap thực trong receipt và assert cấu hình launch có hiệu lực; đo RSS lại. Tăng stack có chi phí memory mỗi thread, không xem stack config là usage thực. Retry tạo UUID mới, giữ nguyên code hash/receipt lỗi cũ.

## Kết quả development cuối và freeze — 15/10/2026

Retry stack4m **PASS**, run **`7bc55ac7-0d24-4ddd-a9b0-3b25d247b596`**, 1.349 itemsets/856 luật. JVM arguments thực có `-Xss4m`, max heap 805.306.368 byte đúng 768 MiB. N train=29.335, catalog=4.556, dev đủ điều kiện=4.293 không đổi. Không có StackOverflow/OOM ở log retry. Tất cả frequency itemsets kiểm độc lập, rules/counts/metrics/key/readback/BSON Int64 đạt; postcheck freeze kiểm thêm mọi số nguyên trong manifest/config thật là BSON Long, giữ bool.

Tất cả lượt thử, confidence .3/partitions 8/local[2]/heap768m; hai lượt đầu thành công dùng stack JVM mặc định, retry cuối dùng stack4m. Dấu “—” nghĩa **chưa đo**, không phải 0. N train 29.335 là cấu hình đầu vào của tất cả lượt, chưa gọi lượt bị guard chặn là đã fit.

| Thứ tự / run UUID | Support | Trạng thái | Itemsets / luật | Dev N | Hit luật | Có gợi ý luật | Recall@5 | Tỷ lệ có gợi ý |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 / `741d89c1-f6c7-4060-b16b-82c17b240b65` | .03 | FAIL guard RAM trước Spark | — | — | — | — | — | — |
| 2 / `7c91893d-ada2-40b8-a1b8-f0db0abc7bda` | .03 | PASS | 118 / 13 | 4.293 | 62 | 1.146 | 1,4442% | 26,6946% |
| 3 / `da870aec-d7f9-4c6e-ba89-52a24b17d0fb` | .02 | PASS | 334 / 91 | 4.293 | 215 | 2.334 | 5,0082% | 54,3676% |
| 4 / `63989ecb-b6d8-4025-8174-885305d44c15` | .01 | FAIL StackOverflow | — | — | — | — | — | — |
| 5 / `7bc55ac7-0d24-4ddd-a9b0-3b25d247b596` | .01 | PASS, chọn | 1.349 / 856 | 4.293 | 505 | 3.513 | 11,7633% | 81,8309% |
| Baseline, cùng điều kiện cho cả ba lượt PASS | — | MEASURED | Catalog train 4.556 | 4.293 | 109 | 4.293 | 2,5390% | 100% |

Recall và tỷ lệ có gợi ý ở bảng đều có mẫu số 4.293. Không dùng tổng số result làm mẫu số, không thêm Precision chưa cần. Values đầy đủ không làm tròn nằm receipt/query-level JSONL; chỉ bảng hiển thị làm tròn. Ba config hữu hạn không chứng minh tối ưu toàn bộ không gian; confidence/K/seed chỉ cố định một lựa chọn. Support thấp hơn tăng số mẫu khai phá và chi phí; config .03 thua baseline cũng được báo. Không ép luật thắng là AC.

Run chọn có 265 target mới ngoài train (hit=0 cho cả hai), 1.586 query có context mới (6.287 occurrence), 780 query không có ứng viên luật sau lọc (hit luật=0, baseline hit10). Trên subgroup target đã biết: luật 505/4.028, baseline109/4.028; đây là phân tích, **không thay mẫu số chính**. Query có context mới: luật150/1.586, baseline38/1.586. Nhóm kích thước giỏ 2–5:56/643; 6–20:258/1.872; 21–100:182/1.623; >100:9/155, so baseline tương ứng8/643,56/1.872,41/1.623,4/155. Context lớn có thêm cơ hội khớp nhưng cạnh tranh Top-5; các subgroup chồng nhau, không cộng tùy ý. Offline mask một item không là cá nhân hóa/nhân quả/giá trị kinh doanh, chưa có kết quả test cuối hoặc độ bất định thống kê.

Selection rule đã ghi **trước thử**: Recall dev cao nhất, tie tỷ lệ có gợi ý, ít luật, support cao, UUID. Chọn .01/.3 chỉ từ development trong các run PASS; failed default stack .01 được giữ. Freeze không refit train+dev hoặc toàn kỳ. Freeze file bất biến mới:

- `artifacts/m3/freeze-1a1f2ec6-331e-4b02-9aaf-18804793d4e9/freeze.json`, SHA-256 **`f7ee9c13432f0c99e7e5bcbf0363eed77eb4d5493b39e78fbb2e8e48557d053a`**.
- Protocol SHA-256 **`68798cbc3c5eae28c51f6e7df4dfc98cab8d439a168da85ed326715eb2a30bdf`**; schema `m0-contract-v1`, policy `p01-first-p02-test-v1`/hash `35f10093da02b67ad56ada7cbc498a79b25bd9ee02719e504b81e60b102a5016`. Train catalog/baseline/names chỉ từ preparation train, file hashes như trên.
- `verification.json` cùng freeze, SHA-256 **`153263e3ceaddb50ceebc893942984b21ce70130cbea683ad633acfdbf601de6`**: exact Mongo/local output/checksum, split/mask/catalog, M2 manifest và giỏ train/dev không đổi, replay mọi query/metric. Manifest/source/runtime/config và hash mã chưa commit nằm selected receipt/freeze; HEAD `ddb8970a49167d3a913a4f64f033a9ec5ad2c3b6`, không gọi code M3 là đã commit.
- `hashes.json` khóa hai file freeze/verification; measurement `artifacts/m3/freeze-20261015T100835.json`. Final **NOT_RUN**, test items không được truy vấn. Run DEVELOPMENT **READY nhưng chưa publication**, không tạo/đổi active pointer. Đây là kỹ thuật sẵn cho mốc sau khi được giao, không phải đã xây hoặc nghiệm thu web M4.

### Chi phí thực và giới hạn phép đo

Môi trường runtime đã đọc: Python 3.14.6/PySpark4.2.0/Scala2.13.18/JDK17.0.12/MongoDB8.3.8; PyMongo4.18.3/NumPy2.5.4/psutil7.0.0, năm JAR connector đúng hash receipt M2. Java tests dùng Boot4.1.1 theo pom hiện có, không chạy ứng dụng/HTTP thật M3. Selected receipt có UTC start/end/JVM arguments/package/code/config hash, từng lượt có measurement riêng.

| Lượt | Wall wrapper giây | Python/launcher peak MiB | JVM peak MiB | Mongo peak MiB | Combined peak MiB |
| --- | ---: | ---: | ---: | ---: | ---: |
| Guard FAIL | 3,043 | 75,49 | 0 | 99,93 | 175,42 |
| .03 PASS | 49,956 | 270,46 | 880,95 | 107,26 | 1.178,69 |
| .02 PASS | 80,784 | 262,41 | 989,55 | 77,49 | 1.260,09 |
| .01 default stack FAIL | 55,387 | 294,11 | 945,87 | 96,79 | 1.240,22 |
| .01 stack4m PASS | 147,752 | 303,87 | 1.090,08 | 101,37 | 1.381,59 |

Selected function 144,533 giây: đọc chuẩn bị/start Spark 7,332; train materialization+fit 15,645; extract/count/collect+kiểm độc lập 119,579; dev evaluation+JSONL 0,360; ghi/đọc Mongo 1,614. Spark có lazy computation nên phần extraction chứa chi phí khai phá action tiếp theo; không gọi fit() timing riêng là toàn chi phí model. JVM sampled peaks theo bước lần lượt315,55/609,19/1.090,08/843,49/801,41 MiB; số chi tiết/count mẫu trong `resources.json`. Bước ngắn có thể 0/1 mẫu; null nghĩa không có mẫu, không gán0. RSS tổng nhóm có shared pages, peak nhóm có thể khác thời điểm, không là private memory/high-water chính xác. Wrapper không tính RAM các ứng dụng khác và measurement process cha; vẫn ghi available RAM samples, không xem nó là peak usage job.

Logical file bytes sau selected wrapper: artifacts/m3 **32.673.934**, scratch **10.515.639**, Mongo dbpath **405.960.145**. Đây là snapshot trước postcheck/freeze và bao gồm lịch sử, không riêng output run chọn; scratch còn là output lỗi, lượt PASS có thể tự dọn. Chưa đo allocated bytes/peak scratch; giữ nguyên thư mục lỗi/nguồn/DB. Năm measurement `trial-0-20261015T095531`, `trial-0-retry-20261015T095901`, `trial-1-20261015T100113`, `trial-2-20261015T100305`, `trial-2-stack4m-20261015T100526` cùng stdout/stderr/samples JSONL ngoài Git; `resources.json` từng run giữ hash receipt/measurement, timings/RSS/disk và status gốc. Wall job không phải giờ-người.

### Gói review M3 cụ thể cho TV2

Theo DoD M3 ở Master Plan 13 và M3_START_PROMPT mục9, **TV2 phải tính lại mẫu metrics và review split thật**. U-38 chỉ là M2. Chưa nhận review M3 tại lúc lập gói này; Agent/test không thay reviewer. Không yêu cầu runtime máy TV2 để thay DoD M3 hiện tại; full run hai máy vẫn M6.

1. Review bảng split/biên/train-only catalog/mask/mẫu số phía trên; đối chiếu `preparation.json`, `split-metadata.jsonl`, `train-baskets.jsonl`, `dev-baskets.jsonl` và hashes. Xác nhận không overlap/leakage, test chỉ metadata, single basket/unknown giữ đúng.
2. Mở `verification.json` trong thư mục freeze: `sample_predictions` là **10 query dev đầu theo Invoice**, có full query/target/Top-K luật/baseline/rule_keys. Tự đếm target thuộc result. Đáp án: luật hit1/10 (Invoice558640, target21086), có gợi ý10/10 → Recall=.1, rate=1; baseline hit0/10, có gợi ý10/10 → Recall=0, rate=1. Đây là mẫu kiểm toán, không thay kết quả4.293 query.
3. Tính tay luật thật `85152 → 85123A`: trainN29.335; count tiền đề1.168, kết luận4.420, hợp390 → support390/29.335=0,01329469916482018; confidence390/1.168=0,3339041095890411; lift=(390/1.168)/(4.420/29.335)=2,2160807816277197. Witness Invoice489519/489556/489597; liên kết basket_set/Invoice trong train-baskets và retained-lines đã hash, không đếm duplicate archive. Hai mẫu luật khác nằm `real_train_rules`.
4. Đọc 12 shared fixture cases và kiểm Java/Python. Java đã khớp toàn bộ4.293 prediction của cả .02 và selected .01, gồm luật tốt nhất/tiền đề, không chỉ consequent. 17 tests Python và 6 Java tests cuối đạt, không skipped khi truyền selected runDirectory. Build/parity không phải review TV2.
5. Báo thực tế TV2 đã review/tính lại, chấp thuận hay còn điểm sửa. Chỉ đóng M3 khi phần này có xác nhận; nếu chưa, giữ checkpoint. Không hỏi lại M2 hoặc tự mở M4/M5.

## Handoff và trạng thái AC/DoD

- M3-T1/T2/T3/T4: đã triển khai và có runtime development/freeze như trên; ghi riêng failed trials và source/version/hash. M3-AC1/AC2/AC3 đạt kỹ thuật TV1 qua fixture+full-train/dev+postcheck+Java parity; không gán scientific final/hai máy/web UI PASS.
- **DoD M3 đã đủ theo U-41:** sau khi được cung cấp gói review cụ thể/verification/split/mẫu metrics, người dùng trả lời “TV2 đã review split, tính lại mẫu metrics và chấp thuận, không còn điểm sửa”. Đã tick M3; đây là review người dùng báo lại, không phải Agent thay reviewer hoặc nhận thông báo riêng trực tiếp TV2. Không có điểm số tối thiểu hoặc yêu cầu luật thắng baseline tự thêm.
- Tái tạo theo [Pipeline Guide mục7](../pipeline/README.md#7-m3--fp-growth-baseline-và-development); dùng new preparation/run UUID. Selected run ID ở trên cho phần tiếp nối được giao sau; M3 không publication/final evaluation/commit/push/reset/drop hoặc cleanup nguồn/evidence.

Receipt review riêng `artifacts/m3/review-20261015.json` gắn U-41/run/freeze/hash, giữ nguyên mọi receipt runtime/freeze/verification PENDING_TV2 trước đó. **M3 đóng ngày15/10/2026, dừng trước M4/M5**. Chưa xác minh runtime máyTV2/whole-system acceptance/giảng viên; U-41 không thay M6. Lifecycle cuối/repository protection/282 ID và ignore checks lưu `artifacts/m3/repository-final-verification.json`; Mongo27019 đã chạy trước phiên nên giữ nguyên, không tự stop/reset dữ liệu của người dùng.

Kiểm cuối: 86 file tracked được bảo vệ không đổi (gồm Word nguồn/RTM/map/audit/M1/M2 code/ứng dụng web), RTM/map cùng 282 ID duy nhất; 39 dòng U cũ giữ nguyên, 91 liên kết file nội bộ hợp lệ, nguồn XLSX đúng SHA-256. Freeze/verification/code/integration hashes không đổi; không staged, `git diff --check` đạt, runtime artifacts/processed/DB/scratch/.venv bị Git ignore. Lifecycle 15/10/2026 12:15 UTC xác nhận không còn JVM dự án, Mongo 27019/PID26740 và dịch vụ 27017/PID5572 vẫn nghe, mẫu27018/web8081 đóng, WiredTiger còn. `lifecycle-final.json` và `preflight-20261015T121546.json` giữ snapshot; không thao tác start/stop/reset trong phiên M3. Đây là kiểm tra repository/lifecycle, không thêm final evaluation hoặc runtime máy thứ hai.

### Bàn giao sang thread M4 — 16/10/2026

Đọc lại AC/DoD/U-41 và hash freeze/verification: M3 đã đủ nghiệm thu, không còn confirm/lựa chọn riêng để đóng. Theo U-42, tạo [prompt M4](../requirements-review/M4_START_PROMPT.md) với scope UI/DTO/query/ranking/lifecycle/kiểm chứng và yêu cầu ghi đồng thời `reports/M4_WEB_APPLICATION_NOTES.md` khi bắt đầu. Phiên này chỉ đọc artifact/mã/hồ sơ và soạn tài liệu, không chạy lại model/test ứng dụng hoặc đọc/ghi Mongo sống, không đổi số M3/freeze/review và không mở M4/M5. Trạng thái process ngày 15/10 là snapshot, thread M4 phải kiểm lại. Đề nghị tiêu đề commit không phải Agent đã commit/push.
