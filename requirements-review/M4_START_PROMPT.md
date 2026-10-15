# Prompt bắt đầu M4 trong thread mới

Ngày soạn: **16/10/2026**. M0/M1/M2/M3 đã đóng; phiên soạn prompt chỉ chuẩn bị bàn giao, **không triển khai M4**. Copy phần sau dấu phân cách vào thread mới cùng project, hoặc dùng lời dẫn ngắn cuối file để yêu cầu đọc đầy đủ prompt này.

---

Bạn tiếp tục đồ án Nhập môn Big Data tại workspace:
`D:\University\Semester7\BigData\DoAn`.

Tôi giao bạn thực hiện **M4 — Website phân tích và gợi ý theo giỏ**, gồm **M4-T1–M4-T4** tại `requirements-review/13_MASTER_IMPLEMENTATION_PLAN.md`, nghiệm thu theo `requirements-review/14_MILESTONE_CHECKLIST.md`.

Hãy đọc đủ ngữ cảnh, triển khai trực tiếp repository và kiểm chứng thực tế trên dữ liệu thật. **Không chỉ lập kế hoạch. Chỉ làm M4**, bàn giao đạt hoặc checkpoint chưa đạt rồi dừng; không tự mở M5/M6, chạy final evaluation, tune/refit mô hình, commit hoặc push. Ngôn ngữ giao tiếp/tài liệu/UI tiếng Việt, stack giữ **Spring Boot + Spring MVC + Thymeleaf + MongoDB**, PySpark batch riêng.

**Không biết/không rõ thì phải xác minh bằng nguồn trước, không tự đoán hoặc gán giả định thành yêu cầu.** Nếu vẫn còn thiếu thông tin ảnh hưởng đúng/sai, hành vi người dùng, ngữ nghĩa số liệu, dữ liệu, bảo mật, kiến trúc hoặc phạm vi: nêu rõ điều đã biết/chưa biết, tác động, 2–3 lựa chọn cụ thể, trade-off và đề nghị; chờ tôi chọn trước phần phụ thuộc, tiếp tục phần độc lập. Không tự chọn thay tôi ở điểm chưa được giao quyền. Không hỏi lại quyết định đã chốt; chi tiết triển khai thông thường đã nằm trong quyền chọn của nhóm, có căn cứ rõ thì làm và ghi rationale.

Ngay khi bắt đầu, tạo/cập nhật **`reports/M4_WEB_APPLICATION_NOTES.md`**. Ghi thông tin phục vụ báo cáo **đồng thời khi quyết định/chạy**, không đợi cuối phiên dựng lại. STATE/checklist giữ điều phối/nghiệm thu; notes là bản ghi kỹ thuật, không tạo roadmap song song.

## 1. Đọc đầu phiên và đối chiếu trạng thái thật

1. Đọc đầy đủ `AGENTS.md`, `README.md`, `STATE.md`; kiểm branch/HEAD/status và diff liên quan, cả file untracked. Snapshot soạn prompt: branch `main`, HEAD `ddb8970a49167d3a913a4f64f033a9ec5ad2c3b6`; thay đổi M3 và hồ sơ còn chưa commit, có source untracked. Người dùng có thể commit sau bàn giao, nên phải kiểm lại; không tự kết luận đã commit/push hoặc bỏ thay đổi cũ.
2. Đọc đầy đủ `requirements-review/07_CONFIRMED_SCOPE.md`, checklist 14; đọc nguyên văn M4, quy tắc nghiệm thu/cổng và QD-08 trong Master Plan 13. Quyết định mới hơn ưu tiên snapshot cũ.
3. Đọc file 11 mục 2/4/8–10: KPI, scope, ba khu vực, catalog, ranking, lỗi/mẫu số. Đọc file 12 mục 9–12/15–16: collection/kiểu/khóa/manifest theo stage, publication/version/CAS, M2/M3 outputs. Tra file 01/02/03/09/15 theo Requirement ID M4; không sửa 282 ID/câu nguồn/trọng số. Tài liệu nguồn/fixture/thiết kế không thay runtime hoặc review người thật.
4. Đọc **`reports/M3_MODEL_DEVELOPMENT_NOTES.md`**, receipt đóng M3 cuối checklist, `pipeline/README.md` mục 7; đọc phần dữ liệu/output/tái tạo trong **`reports/M2_DATA_PREPROCESSING_NOTES.md`** và Guide mục 6. M3 notes không thay M2 counts toàn kỳ; M2 notes không là train catalog.
5. Đọc `web/pom.xml`, `application.properties`, toàn bộ Java/controller/service/ranking/template/tests liên quan tại `web/`. Đọc `scripts/invoke-m1.ps1`, `scripts/m1_control.py`, `scripts/invoke-m2.ps1`, `pipeline/sample_pipeline.py` phần publication và caller trước tái dùng. M1 chỉ là prototype; không coi endpoint verification mẫu hoặc fixture là public API sản phẩm.
6. Đọc `pipeline/m3_protocol.py`, `m3_trial.py` phần output/schema/manifest, `m3_verify.py`, `m3_freeze.py`, `m3_prepare.py`, shared cases `m3_ranking_cases.json`, `test_m3_protocol.py`, `M3SharedRankingTest.java`; đọc M2 phần summaries/quality payload cùng caller. Đối chiếu artifact/hash/ID thật trước dùng. Không chạy checker có mutation hoặc có guard chỉ phù hợp stage cũ một cách máy móc.

Sau khi đọc, báo ngắn trạng thái, phạm vi, kế hoạch triển khai/kiểm chứng, điểm nào cần lựa chọn nếu có và cách ghi evidence; tiếp tục thực hiện phần đã rõ.

## 2. M0–M3 đã đóng — không hỏi lại nghiệm thu

- M0: contract `m0-contract-v1`, U-27 run bất biến/active pointer/chín collection, U-28 decimal text, U-29 dashboard hàng hóa + audit, review U-30.
- M1: mẫu TV1 Mongo→Spark→Mongo→MVC/Thymeleaf đã đạt; U-33 miễn receipt TV2 riêng M1, U-35 xác nhận học/demo/review. Không ghi TV2 đã chạy; số fixture 5 giỏ/7 itemsets/9 luật không phải kết quả thật.
- M2: tiền xử lý toàn nguồn TV1/postcheck đạt, U-38 xác nhận TV2 review/chấp thuận không còn điểm sửa. Không còn confirm/demo riêng phải bổ sung để đóng M2.
- **M3 đóng 15/10/2026:** full-train/development/freeze/postcheck/Java parity TV1 đạt; **U-41 xác nhận TV2 đã review split, tính lại mẫu metrics và chấp thuận, không còn điểm sửa**. Không cần hỏi lại review/config M3. Receipt runtime/freeze ghi `PENDING_TV2` là snapshot trước U-41; giữ bất biến, đọc review receipt riêng.
- M3 chưa publication và chưa có UI dữ liệu thật. Java parity là đọc JSONL qua tests, không phải web/HTTP runtime thật. M4 phải kiểm phần web thật; không suy M3 đã làm thay M4.
- Full run/demo riêng hai máy thuộc M6/U-15/U-22, chưa nghiệm thu máy TV2. M4 TV1 không thay M6. Dataset/GV chấp thuận theo U-25, khung B/quy cách A theo U-26, vai trò theo U-23 đã chốt; không hỏi lại.

## 3. Đầu vào M2/M3 và freeze được phép tái sử dụng

| Trường | Giá trị đã nghiệm thu |
| --- | --- |
| Source | `data/raw/online-retail-ii/online_retail_II.xlsx`, 45.622.278 byte; Daqing Chen, UCI Online Retail II, DOI10.24432/C5CG6D, CC BY4.0 |
| Source/dataset SHA-256 | `bcbe73b35f5b7babf197fb0cb983a11f5d9ff929078d4aa53d171b1f2df2e980` |
| M2 preprocessing run | `d7fb3f21-115f-4793-a5fe-5c40b6da64cd`, VALIDATED / basket_set READY / PREPROCESSING |
| Basket set | `cae0d9e763ef38a086966d829fdeba9272f4d7fda7b61791bee9e9ba04b3287a` |
| Source stage counts | 1.067.371 raw → 1.033.036 P-01 → 1.007.913 positive_valid → 1.003.357 merchandise |
| Toàn kỳ merchandise | 39.516 giỏ / 4.895 item / 5.347 summaries; 3.208 giỏ một item; max1.108 item/giỏ không cắt |
| Giá trị mua dương hàng hóa toàn kỳ | Exact `19643861.637` GBP, **không phải doanh thu ròng** |
| M3 selected run | **`7bc55ac7-0d24-4ddd-a9b0-3b25d247b596`**, FULL_SOURCE / MODEL_DEVELOPMENT / DEVELOPMENT / READY, chưa publication |
| Preparation | `artifacts/m3/preparation-7da29e52-53cf-4986-beff-dfaad251663c/` |
| Train / dev / test | 29.335 / 4.609 / 5.572 giỏ, không overlap; 2.503 giỏ một item train; 316 giỏ một item dev; test chỉ metadata |
| Catalog của run M3 | **4.556 item train** từ717.574 dòng hàng train, gồm cả item không có luật; tên modal không rỗng/trim/tie Unicode, thiếu dùng mã |
| Model output | **1.349 frequent_itemsets / 856 association_rules**; consequent scalar, antecedent canonical unique |
| Config chọn | support=.01, confidence=.3, partitions8, local[2], heap768m/stack4m; **K=5**, seed20261015 |
| Protocol | `m3-temporal-hide-one-v1`; SHA-256 `68798cbc3c5eae28c51f6e7df4dfc98cab8d439a168da85ed326715eb2a30bdf` |
| Ranking | `confidence-lift-support-codepoint-v1`, không rounding trước so sánh |
| Schema / policy | `m0-contract-v1` / `p01-first-p02-test-v1`; policy SHA-256 `35f10093da02b67ad56ada7cbc498a79b25bd9ee02719e504b81e60b102a5016` |
| Final evaluation | **NOT_RUN**, không ghi0 giả hoặc copy dev score sang final |

Split thời gian **local/timezone UNKNOWN**, biên `[start,end)`: train [01/12/2009,01/07/2011), dev [01/07,01/10/2011), test [01/10,10/12/2011). M4 không đổi split/K/seed/mask/ranking/policy/config, không dùng test để chỉnh mô hình hoặc minh họa predictions. Dashboard mô tả toàn kỳ đã có ở M2 được phép hiển thị, nhưng không dùng tên/frequency toàn kỳ lấp catalog hoặc baseline train.

Các file quan trọng ngoài Git:

- `artifacts/m3/freeze-1a1f2ec6-331e-4b02-9aaf-18804793d4e9/freeze.json`: SHA-256 **`f7ee9c13432f0c99e7e5bcbf0363eed77eb4d5493b39e78fbb2e8e48557d053a`**.
- `verification.json` cùng thư mục: SHA-256 **`153263e3ceaddb50ceebc893942984b21ce70130cbea683ad633acfdbf601de6`**; `hashes.json` khóa hai file này. Freeze lưu config/protocol/source/policy/split/selection/all trials/code/output hashes, không sửa để hợp thức hóa M4.
- `artifacts/m3/<selected_run>/receipt.json`, `items.jsonl`, `frequent_itemsets.jsonl`, `association_rules.jsonl`, `dev-predictions.jsonl`, `resources.json`; `artifacts/m3/review-20261015.json` ghi U-41; `repository-final-verification.json` và `lifecycle-final.json` là snapshot cuối M3.
- Logical checksums: catalog `a99f74a37f3a99f003e9b79debc3325e3c58783a0bef18e242669541c6063b54`; itemsets `c0348117dd5df9a8c07659c8c68e9f4ae729b91081fc7e0c2e1393c4dd830386`; rules `10d880e91f2fb4afc2b81640f500bb60ccfd6c525552154c07e0c37b589e0c96`. Đọc thuật toán checksum/caller, không so raw file hash có run_id với logical checksum đã bỏ run_id.
- `artifacts/m2/pipeline-<M2_run>.json`, `final-verification-<M2_run>.json`, `review-20261015.json`; retained-lines ở `data/processed/m2/<basket_set>/<M2_run>/retained-lines.jsonl` có SHA-256 `82ddde19db72b295d723ebb3ca1068ccbabf3a44a49d8ab396598842e5bc5c74`. M4 ưu tiên đọc outputs Mongo, không bắt browser/web đọc JSONL trên đĩa.

Artifact bị Git ignore, clone thiếu không đồng nghĩa mốc chưa từng chạy. Nếu không có outputs thật, xác định thiếu gì và phương án tái tạo theo Guide. Không dựng receipt, không đổi run ID nguồn để giả khớp, không reset/seed lại namespace. Nếu cần tái tạo model thì giữ protocol freeze/new UUID; trình rõ phạm vi phát sinh trước khi làm, không mặc định chạy lại toàn M2/M3 chỉ để xây UI.

## 4. Môi trường, lifecycle và công bố DEVELOPMENT cho web

- Namespace nguồn thật theo U-37: **127.0.0.1:27019 / bigdata_m2**, dbpath `artifacts/m2/mongo-data`. Tái sử dụng đúng namespace này, không đổi DB theo số milestone. Không ghi27017 hoặc mẫu M1/27018. Web chỉ đọc DB, browser gửi scalar/list mã, không gửi object Mongo query.
- Snapshot cuối M3 (15/10): Mongo27019/PID26740 có sẵn từ trước phiên được giữ chạy đúng receipt; 27017/PID5572 vẫn nghe,27018/8081 đóng, không còn JVM dự án. **Đây không phải trạng thái hiện tại.** Kiểm lại PID/executable/hash/start/command/listener/receipt trước start/stop/build, chỉ bind loopback. Sandbox chặn CIM/process/loopback phải xin quyền công cụ, không bypass hoặc suy process đã dừng.
- Web hiện `spring.mongodb.uri` trỏ M1/27018 và chỉ nhận SAMPLE, hard-code3 item, summary_type m1, endpoint `/m1/verification`. Không chỉ sửa URI rồi coi đã hỗ trợ dữ liệu thật. Đọc cả mapper/guards/config/template/caller/tests và hoàn thiện theo contract M4; giữ nhận diện SAMPLE/DEVELOPMENT rõ, không ngầm fallback sang mẫu khi nguồn thật lỗi.
- App hiện dùng8081 loopback; nếu cổng trống, tái sử dụng cho M4 với receipt web nhận diện JAR/hash/args/config đích thật. Đọc launcher trước tái dùng: `StartWeb` M1 không truyền đích M2, `VerifyWeb` có đáp án synthetic, `RunSample` tạo batch mẫu. Không gọi các action đó như thể là runtime M4. Nếu cần dùng đích khác hoặc namespace/quyền chưa cấp, trình lựa chọn trước phần phụ thuộc.
- Phiên bản đã thử TV1: JDK17.0.12, Boot4.1.1/Data MongoDB5.1.1, driver web5.8.1, Maven portable3.9.16/cache `tmp/maven-repository`; Python3.14.6/PySpark4.2.0/Scala2.13.18/connector11.1.0/PyMongo4.18.3. Đọc dependency/version thực trước dùng API; tra tài liệu chính thức khi cần, không nâng cấp toàn máy hoặc mặc định máy TV2 giống máy này.
- Mongo decimal text → Java BigDecimal, hiển thị GBP hai chữ số HALF_UP trên tổng cuối; không cộng tiền bằng double hoặc sort/range tiền bằng chuỗi. Counts/frequency BSON Long; ngày hóa đơn LocalDateTime/string không offset, timestamp hệ thống UTC riêng. Không sửa output để vừa mapper.
- M3 selected run READY **chưa có active pointer** ở snapshot. Để nghiệm thu M4 trên dữ liệu thật, được làm **phần nối tối thiểu cần thiết** theo U-27: helper batch/control kiểm selected run/schema/stage/manifest/output/hash/basket-set đủ, đọc pointer thật; lần đầu insert active/version1 nếu chưa có, lần sau CAS theo cả run/version cũ. Web không ghi pointer/output và không chọn “run mới nhất”. Nếu pointer khác snapshot, xác minh nguồn trước; không replace/upsert mù hoặc âm thầm đổi selected run. Timeout phải đọc lại pointer trước kết luận. Ghi receipt/provenance DEVELOPMENT và giữ run cũ.
- Phần công bố tối thiểu này chỉ phục vụ đọc run DEVELOPMENT thật của M4, không tự mở toàn bộ chiến dịch retry/crash/end-to-end/final evaluation của M5. Kiểm form cũ/lỗi đọc cần cho M4 có thể dùng fixture/probe cô lập, không phá active run thật hoặc sửa READY outputs. Nếu phát hiện contract thiếu/ngữ nghĩa lớn mâu thuẫn, nêu lựa chọn rồi chờ.
- `m2_pipeline.py`/`m2_final_verify.py` có guard namespace chưa có model; checker sau có mutation invalidation checkpoint cũ. Không chạy lại chúng sau M3 để “kiểm khỏe”. `m3_verify.py` là postcheck read-only theo stage; đọc caller/giới hạn trước chạy. `artifacts/m3/final_repository_check.py` và receipt bảo vệ cũ là snapshot M3, không mặc định yêu cầu mọi code web không được đổi trong M4; hash freeze giữ phiên bản đã chạy, code M4 ghi hash/version riêng.

## 5. M4-T1/T2 — đọc đúng dữ liệu và ba khu vực UI

Hoàn thiện DTO/model đọc/template trong module `web/` hiện có. Ưu tiên giải pháp nhỏ, dễ học và miễn phí cho hai laptop; không tự thêm service/SPA/framework mới. Màu/bố cục/chart/URL/pagination là chi tiết triển khai được giao, chọn có căn cứ; không biến thành hàng loạt câu hỏi nhỏ hoặc ngưỡng nghiệm thu mới.

1. **Tổng quan/phân tích:** metadata run/source/policy; stage counts và raw quality audit; xu hướng số hóa đơn/giá trị mua dương GBP theo tháng; phân phối kích thước giỏ; item phổ biến theo số giỏ và lượng mua. Dùng `summaries` đúng basket_set/scope/type/bucket. Toàn kỳ merchandise39.516 giỏ/4.895 item khác catalog train4.556 item và train29.335 giỏ; nhãn phải rõ, không gộp các mẫu số. Quality reasons có chồng nhau khác số loại tuần tự; không cộng chồng thành tổng loại. Không gọi GBP mua dương là net revenue/lợi nhuận.
2. **Tập phổ biến/luật/đánh giá:** bảng itemsets/frequency/support và luật/metrics, mẫu số train/config; lọc/phân trang/thứ tự ổn định, đầy đủ dữ liệu phía sau bảng. Đánh giá DEVELOPMENT luật và baseline từ manifest đúng run; final hiển thị **Chưa đánh giá (NOT_RUN)**. 0 luật được manifest xác nhận khác collection thiếu/ghi dở; không yêu cầu có luật bằng mọi giá.
3. **Gợi ý theo giỏ:** tìm/chọn theo mã/tên trong **toàn bộ catalog train của run**, kể cả item không có luật; chọn một/nhiều item, xem Top-5 mới cùng tiền đề/mã/tên/confidence/lift/support giải thích. Không dùng4.895 item toàn kỳ để cho chọn4.556-item model, không tìm tên dev/test để lấp thiếu. Không tự thêm RFM, phân khúc khách, bản đồ quốc gia, giỏ mua hàng/checkout hoặc thông tin khách cá nhân.

Một request đọc pointer một lần, kiểm run READY/schema/basket-set/manifest theo DEVELOPMENT; giữ run/version snapshot cho tất cả query/page/form. Summaries liên kết basket_set của cùng run, không trộn “run mới nhất” ở từng collection. Nếu cache, gắn đúng run/version và kiểm đủ output; không stale một phần. Hiển thị provenance đủ cho demo/báo cáo mà không nhồi chi tiết nội bộ vào thao tác người dùng.

## 6. M4-T3 — gợi ý và input đúng contract

- Đủ **mọi** tiền đề, consequent chưa trong query. Một item nhiều luật giữ luật tốt nhất theo confidence giảm → lift giảm → support giảm → antecedent tăng. Xếp ứng viên thêm StockCode tăng rồi antecedent tăng. Unicode code point, tuple prefix ngắn trước; không locale/UTF-16 mặc định nếu khác contract, không rounding/tie gần bằng.
- K=5 từ config của run đã freeze, không hard-code một K mới. Không mặc định fallback baseline hoặc thêm lift>1. Baseline chỉ là phép so sánh ở khu vực evaluation, không thay luật khi rỗng.
- Giỏ trùng mã tính một item; rỗng/mã không thuộc catalog/parameter sai dạng/giới hạn input phải báo rõ, giữ lựa chọn hợp lệ, không âm thầm bỏ unknown hoặc cắt giỏ. Đặt giới hạn kỹ thuật có căn cứ/ghi rõ nếu cần; nếu làm đổi semantics lớn thì hỏi trước.
- Form gửi run_id/version; form cũ không dùng luật mới lên lựa chọn cũ. Kiểm stale trước xử lý gợi ý; giải thích dữ liệu đã đổi và yêu cầu tải lại.
- Dùng typed binding/query, allowlist sort/filter, giới hạn/validate pagination; không chuyển browser object/string tùy ý thành Mongo query/JSON hay SpEL. Escape tên/mô tả trong Thymeleaf, không `th:utext` cho dữ liệu nguồn. Không lộ stacktrace/URI/secrets; xử lý Mongo unavailable, chưa có pointer, schema không hỗ trợ, manifest/output thiếu khác với “giỏ hợp lệ nhưng không có gợi ý”. Không tắt bảo vệ có sẵn để test pass.

## 7. M4-T4 — kiểm chứng thật, không chỉ build xanh

- Giữ/chạy shared12 cases và regression Java/Python liên quan khi thay logic. Đối chiếu Java với selected run predictions, gồm consequent và antecedent của luật tốt nhất; fixture tách rõ khỏi real development. Không thay expected để khớp implementation khi chưa có căn cứ.
- Chạy Spring Boot thực đọc Mongo27019, xác nhận pointer/run/version/source/basket_set/stage/config; HTTP GET/POST các khu vực/bộ lọc/phân trang và giỏ. Đối chiếu KPI/số tiền/mẫu số/selected output với M2/M3 receipts và DB readback. 17Python/6Java M3 đã PASS là lịch sử, không thay M4 runtime mới.
- Có ca một item, nhiều item, thiếu một tiền đề của luật nhiều item, existing item, duplicate candidate/input, item catalog không có luật, không có gợi ý, giỏ rỗng/unknown/invalid, empty dataset theo manifest, lỗi Mongo/schema/manifest, form cũ và render text độc hại. Ca lỗi/mutation dùng fixture/probe riêng có provenance; không sửa tên/catalog/model thật hoặc drop source để dựng lỗi. Nếu chưa kiểm được qua browser/ảnh thật, nói rõ layer đã kiểm và phần còn thiếu, không gọi HTTP tự động là người dùng đã xem UI.
- Ca thật đã xác minh: Invoice dev `558640`, query `[21080,21094,21467,21770,22704,22969]`, target đã ẩn `21086`; gợi ý đúng `[21086,21212]`. Luật tốt nhất lần lượt `{21080,21094}→21086` và `{21080}→21212`; baseline `[85123A,22423,85099B,21212,20725]`. Giữ đúng strings khi so code. Không khẳng định chỉ cần bỏ21094 là21086 chắc chắn biến mất vì có thể còn luật khác áp dụng; kiểm riêng luật và kết quả theo bộ luật đầy đủ.
- Hiển thị dev N4.293: luật hit505/4.293, có gợi ý3.513/4.293; baseline hit109/4.293, có gợi ý4.293/4.293. Recall@5=11,7633% vs2,5390%, rate81,8309% vs100%. Nhãn development rõ; rate có gợi ý không là độ chính xác. Giữ265 target mới/780 query không ứng viên luật trong mẫu số,316 giỏ một item dev báo riêng; không biến unknown offline thành silently dropped web input.
- Chứng minh web dùng outputs khi **Spark đã dừng**, HTTP không gọi Python/fit. Không chạy pipeline chỉ để có demo động. Đo startup/request/query/time/RSS web theo phương pháp rõ, nếu đo; không tự đặt SLA. Build/UI/fixture/Java parity/manual demo/two-machine acceptance là các layer riêng.
- Lưu ảnh UI thật có run/scope/provenance và hướng dẫn thao tác/đáp án dễ hiểu để **TV1/người dùng kiểm tra trực tiếp UI, đối chiếu output theo DoD M4**. Sau khi có gói cụ thể mới hỏi phần review/manual còn thiếu; không xin xác nhận trước khi có evidence hoặc lấy Agent thay TV1. Không hỏi lại M3.

## 8. Ghi thông tin báo cáo đồng thời khi thực hiện

Tạo `reports/M4_WEB_APPLICATION_NOTES.md` ngay khi bắt đầu M4; không tạo sẵn số liệu/chứng nhận khi mới soạn prompt. Tối thiểu ghi:

1. Requirement IDs, kiến trúc thực tế, dataflow browser→MVC/service→Mongo→Thymeleaf; sơ đồ/classes/DTO/routes/fields triển khai và trách nhiệm, web chỉ đọc batch outputs. Nguồn tài liệu chính thức/phiên bản đã tra, nguồn dataset/citation/giấy phép khi dùng hình/số liệu.
2. Các lựa chọn/điểm chưa rõ/câu hỏi và câu trả lời người dùng; rationale kỹ thuật trong scope; phần nào là confirmed, quan sát source/runtime, đề xuất hoặc chưa kiểm. Không gán tự chọn thành xác nhận của người dùng/GV.
3. Run/source/basket_set/schema/policy/config/freeze/hash, publication version/receipt trước–sau nếu có; bảng đối chiếu mỗi KPI/nhãn UI→field/scope/mẫu số. Tách toàn kỳ/train/development/final NOT_RUN, integer/decimal/local time và quy tắc format.
4. Commit HEAD và hash mã chưa commit, environment/build/JDK/Boot/Data Mongo/driver/Maven/dependencies/config không bí mật, UTC start/end, commands tái tạo và URLs local. Thông số mới quan trọng như page size/sort/search/input bound/cache/cổng/query/index/RSS ghi lúc chọn/đo, kèm lý do/đơn vị/giới hạn; không tự gán benchmark thành SLA hoặc wall time thành giờ-người.
5. Mỗi ca demo/test: input/query, run/version, expected/actual, nguyên nhân gợi ý/không gợi ý, so Python/Java, HTTP/UI screenshot/evidence; stage đã kiểm và chưa kiểm. Ảnh/bảng có caption/source/run/scope/currency/mẫu số, không chỉ ảnh đẹp hoặc score thiếu denominator.
6. Lỗi → evidence → nguyên nhân → sửa → kiểm lại/regression; ghi cả fail/chưa chạy. Manual TV1/TV2 review thực tế và AC/DoD đạt/chưa đạt, hướng dẫn mở/dừng đúng process và điểm bàn giao. Không tự ghi đóng góp/giờ/phần trăm từ công việc Agent.

Evidence/log/receipt/ảnh/resource chi tiết tại **`artifacts/m4/`**, ngoài Git; source/config example/hướng dẫn/notes rút gọn được version control, không secrets/dữ liệu cá nhân. Cập nhật `STATE.md` ngắn, checklist14 theo bằng chứng, file07 khi có xác nhận mới; file11/12/13 chỉ khi thay đổi được chấp thuận làm nội dung hiện hành sai, giữ lịch sử/freeze cũ.

## 9. Nghiệm thu và ranh giới kết thúc

Đọc nguyên văn AC/DoD M4 ở Master Plan13; đối chiếu tối thiểu:

- **M4-AC1:** đủ ba nhóm thông tin đã đồng ý, mã/tên/scope có ý nghĩa và không gây nhầm; không fit theo HTTP.
- **M4-AC2:** thiếu tiền đề không áp luật nhiều item; không trả item đã chọn; trạng thái không luật đúng, ranking khớp ca chung.
- **M4-AC3:** dữ liệu thật cùng run, input invalid được xử lý, tên/mô tả render an toàn, browser không gửi object Mongo query.
- **DoD:** TV1 kiểm tra trực tiếp UI và đối chiếu đầu ra, hướng dẫn demo/ảnh có provenance. Không suy M4 TV1 thành full run hai máy M6 hoặc chấp thuận của GV.

Khi kết thúc: đọc final diff (gồm source untracked), `git diff --check`, kiểm source/freeze/M2/M3 không bị sửa để pass, dữ liệu/artifacts/DB/scratch/.venv/build/secrets ngoài Git. Kiểm identity/lifecycle JAR/hash/config/listener, tiến trình nào có sẵn/phiên này mở; giữ dữ liệu, hướng dẫn demo/stop phù hợp trạng thái thật. Không kill theo tên/cổng, reset/drop/ghi đè READY outputs, đổi phần mềm/policy toàn máy, commit/push hoặc gửi GV/nộp Classroom.

**Bàn giao M4 đạt hoặc checkpoint chưa đạt rồi dừng trước M5/M6.** Không chạy test cuối, refit/tune hoặc tuyên bố final score, không tạo website bán hàng/auth/payment/cloud/cluster. Nếu bị chặn thông tin/quyền/review, nêu rõ blocker và lựa chọn còn cần; không tự mở mốc khác để né.

Hãy bắt đầu đọc và thực hiện M4 theo các chỉ dẫn trên, không yêu cầu tôi kể lại ngữ cảnh đã có trong repository.

---

Lời dẫn ngắn để paste vào thread mới trong cùng project:

```text
Tôi giao bạn thực hiện M4 — Website phân tích và gợi ý theo giỏ tại D:\University\Semester7\BigData\DoAn.
Hãy đọc đầy đủ requirements-review/M4_START_PROMPT.md, sau đó đọc tài liệu/mã nguồn được chỉ dẫn và triển khai, kiểm chứng thực tế đúng M4-T1–T4. Không chỉ lập kế hoạch.
M0/M1/M2/M3 đã đóng; U-41 xác nhận TV2 review split/tính lại mẫu metrics và chấp thuận M3, không hỏi lại nghiệm thu M3. Dùng run DEVELOPMENT đã freeze, không tune/refit hoặc đánh giá test cuối.
Điều chưa biết/chưa rõ phải xác minh nguồn; nếu vẫn thiếu thông tin ảnh hưởng đúng/sai/hành vi/dữ liệu/bảo mật/scope thì nêu tác động, các lựa chọn/trade-off/đề nghị và chờ tôi chọn trước phần phụ thuộc, không tự đoán. Không hỏi lại quyết định đã chốt.
Ngay khi bắt đầu, tạo/cập nhật reports/M4_WEB_APPLICATION_NOTES.md; ghi đồng thời quyết định/thông số/run/source/config/fields/KPI/scope/mẫu số/lệnh/phiên bản/kiểm chứng/ảnh/tài nguyên/lỗi/evidence và review để dùng cho báo cáo đồ án. Cập nhật STATE/checklist/decisions theo prompt, không chỉ giữ trong chat.
Chỉ M4; bàn giao đạt hoặc checkpoint chưa đạt rồi dừng. Không tự mở M5/M6, chạy final evaluation, commit hoặc push.
```
