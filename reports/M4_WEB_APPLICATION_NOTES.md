# M4 — Website phân tích và gợi ý theo giỏ

Ngày bắt đầu/cập nhật: 16/10/2026 (Asia/Bangkok). **M4 đã đóng**: M4-T1–T4/AC1–AC3 đạt kỹ thuật TV1; người dùng xác nhận đã kiểm trực tiếp UI/đối chiếu, chấp thuận không còn điểm sửa theo **U-44**, đủ DoD. Các trạng thái chờ trong nhật ký phía dưới là snapshot lúc chạy, không phủ nhận xác nhận mới.

## Phạm vi và nguồn

- Giao việc hiện tại và `requirements-review/M4_START_PROMPT.md`: chỉ M4-T1–T4, Spring Boot/MVC/Thymeleaf đọc MongoDB; không fit/tune/final evaluation, M5/M6 hoặc commit/push.
- M0–M3 đã đóng; U-41 là xác nhận review M3, không hỏi lại. Giữ nguyên freeze và protocol/config.
- Run DEVELOPMENT được chỉ định: `7bc55ac7-0d24-4ddd-a9b0-3b25d247b596`; M2 `d7fb3f21-115f-4793-a5fe-5c40b6da64cd`; Mongo `127.0.0.1:27019/bigdata_m2`. Các ID/count/hash trong prompt cần đối chiếu artifact và DB thật trước publication.
- Notes ghi đồng thời quyết định, fields/KPI/mẫu số, provenance/config, lệnh/phiên bản, kiểm chứng, tài nguyên, lỗi/evidence/ảnh và review. STATE/checklist giữ điều phối và nghiệm thu.

## Nhật ký đọc nguồn và quyết định

- Đã bắt đầu đọc prompt, AGENTS/README/STATE và kiểm Git. Giữ nguyên thay đổi đã có; trạng thái process/DB snapshot M3 chưa coi là hiện tại.

### Đối chiếu và lựa chọn triển khai — 16/10/2026

- Git đầu phiên sạch, main/HEAD `4466ef75cbf229c1827614fd49e793dcb06c6e58`; khác snapshot prompt. Đã đọc quy tắc, scope/U-41/U-42, AC/DoD M4 và nguồn thiết kế/schema/code được chỉ dẫn. Truy vết: B-F01/B-F02, B-H07–B-H09, B-R07/B-R08, B-P20/B-E07/B-O01; không sửa yêu cầu/282 ID.
- CIM sandbox bị từ chối; Status trong sandbox báo false do che process. Đã kiểm ngoài sandbox: Mongo 27019/PID26740 đúng receipt/executable/hash/start/cmd/loopback, có sẵn từ trước; 8081/27018 trống. JVM16756 thuộc thesis khác, giữ nguyên; không có Spark dự án.
- Kiến trúc: browser → `AnalysisController` → `AnalysisResults` → MongoTemplate/driver → DTO → Thymeleaf. `RuleRanking` M3 giữ nguyên. GET `/`, `/patterns`, `/basket`; POST `/recommend`. M1 giữ riêng khi chỉ định `app.mode=SAMPLE` và URI mẫu tường minh; mặc định DEVELOPMENT/27019, không fallback.
- Mỗi request đọc pointer đúng một lần, đọc run/preprocessing/dataset/catalog/itemsets/rules/summaries theo ID snapshot; không cache hoặc ghi Mongo. Đọc toàn bộ ~12 nghìn output nhỏ để kiểm count/keys/fields và tính bộ lọc trong Java, tránh thêm index/DB mutation; đo runtime rồi báo giới hạn. Count thiếu khác 0 output manifest xác nhận. Không đọc source_rows hoặc test baskets cho web.
- Pagination 25 hàng/trang, đánh số query từ0; sort allowlist theo loại bảng, tie codepoint ổn định. Search literal (không regex Mongo/JSON/SpEL), mã/tên train; item dashboard toàn kỳ chỉ tìm mã vì summaries không có tên. Chuỗi tìm tối đa160 ký tự. Filter support [0,1], size0=mọi cỡ; không đổi config mô hình.
- Giỏ cho mọi mã catalog, không giới hạn ở số luật hoặc cỡ giỏ train; số input lặp tối đa2×catalog (9.112), mỗi chuỗi≤160, duplicate tính một. Vượt giới hạn báo lỗi, không cắt. Tomcat max parameters10.000/form2MB giữ đủ mọi mã; giới hạn là kỹ thuật, không SLA. Client search chỉ ẩn hiển thị, không bỏ chọn.
- Tiền Java BigDecimal từ decimal text, chỉ HALF_UP2 chữ số trên tổng cuối. Quality reason chồng nhau không cộng vào stage loại; nguồn có raw3 mức mẫu số/p01/positive. Chart CSS/bảng HTML, không thêm dependency/CDN; tên dùng th:text, JS không innerHTML, CSP chỉ script self.
- Đối chiếu tài liệu chính thức: [Spring MVC RequestParam](https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-methods/requestparam.html), [Thymeleaf th:text](https://www.thymeleaf.org/doc/tutorials/3.1/usingthymeleaf.html), [MongoDB single-document atomic/CAS](https://www.mongodb.com/docs/manual/core/write-operations-atomicity/). API thực được build/runtime kiểm lại trên stack hiện có.

### Publication thật

- `scripts/m4_publish.py --publish` ngoài sandbox PASS. Receipt `artifacts/m4/publication-2026-10-15T190951.833029+0000.json`; trước null, sau active đúng selected run/version1, BSON Int64. UTC19:09:53 ngày15/10 =02:09:53 ngày16/10 Asia/Bangkok.
- Trước insert kiểm lifecycle/source SHA-256, freeze/hash/selected receipt/config/output validation; gọi postcheck M3 read-only kiểm output Mongo/file/logical checksum/keys/BSON/train/dev/metrics. Không gọi freeze/refit hoặc checker M2 có mutation. Freeze SHA256 vẫn `f7ee9c13432f0c99e7e5bcbf0363eed77eb4d5493b39e78fbb2e8e48557d053a`; final NOT_RUN.
- Helper có CAS theo run/version cũ và đọc lại khi lỗi Mongo timeout; tác vụ thực chỉ insert lần đầu, không giả gọi CAS runtime thật. Nếu có pointer cùng run thì idempotent read-only; pointer khác dừng để điều tra.
- Giữ receipt FAIL preflight sandbox `publication-2026-10-15T185241.377380+0000.json`: psutil.NoSuchProcess do process bị che, không coi Mongo đã dừng. Lần ngoài sandbox xác minh thật và PASS.

## Fields / KPI / phạm vi

| UI | Nguồn | Scope / mẫu số |
| --- | --- | --- |
| Stage raw/P-01/positive/merchandise | summaries raw/quality/all payload.stage_counts, đối chiếu M2/M3 manifest | 1.067.371→1.033.036→1.007.913→1.003.357 dòng |
| Giỏ/mã/một item | stage_counts.baskets/items/single_item_baskets | toàn kỳ merchandise39.516/4.895/3.208 |
| Monthly Invoice / GBP | merchandise/month payload.invoices/line_value_gbp | min local invoice time, 25 tháng; tổng exact19643861.637 GBP |
| Phân phối giỏ | merchandise/basket_size payload.baskets | số mã duy nhất, 426 cỡ; tổng39.516, max1.108 |
| Item phổ biến / lượng mua | merchandise/item payload.baskets/quantity | 4.895 item toàn kỳ; khác frequency train, không dùng lấp tên train |
| Danh mục chọn và tên | items stock_code/display_name/train_basket_count | 4.556 mã train gồm mã không có luật; Ntrain29.335 |
| Tập phổ biến / luật | frequent_itemsets / association_rules cùng run | 1.349/856; frequency/support train, không làm tròn ranking |
| Đánh giá luật / baseline | run.manifest.development.all | N4.293; hit505/109; nonempty3.513/4.293; 316 single dev báo riêng |
| Final | manifest.final_status | NOT_RUN, không score0 hoặc copy dev |

## Kiểm chứng và review

Đã chạy kiểm chứng M4 kỹ thuật TV1 như receipt bên dưới. TV1 kiểm UI/đối chiếu và chấp thuận theo U-44; runtime máy TV2/M6 chưa kiểm.

### Các lần kiểm và lỗi đang xử lý

- Python regression17 tests PASS (`python-regression.log`). Maven/Java9 tests PASS ngoài sandbox (`build-03.log`): shared12 fixture, real4.293 query cả consequent/best antecedent và3 tests mới gồm HTTP probe cô lập. Build đầu có6 tests cũ PASS (`build-01.log`); test HTTP `build-02.log` FAIL do `Unable to establish loopback connection / Permission denied`, chạy lại ngoài sandbox, không sửa bảo vệ để pass.
- UI probe dùng catalog synthetic chứa script/img payload và MongoTimeout giả lập trong service; real Tomcat/Thymeleaf/HTTP trên cổng ngẫu nhiên, không ghi probe vào DB. Kiểm schema/manifest thiếu/count int32, output0 theo manifest, N0/NOT_APPLICABLE, tiền1.005→1.01, rỗng/unknown/duplicate/form cũ/object params/render escaped. Đây không phải mô phỏng sửa dataset thật hoặc sự cố Mongo thật.
- HTTP thật lần đầu FAIL503 (`http-2026-10-15T191554.145071+0000.json`): guard Java tìm policy_hash ở top-level M2 run; source/DB chứng minh field nằm manifest M2. Sửa mapper đọc manifest, giữ DB/freeze nguyên; fixture chỉnh theo schema thực.
- HTTP thật lần hai FAIL503 (`http-2026-10-15T191910.582323+0000.json`): quality payload được M2 ghi trước khi final receipt thêm baskets/items/summaries/single/multi. Guard sai khi đòi toàn bộ Document counts bằng nhau. Sửa so8 fields stage nguồn quality, lấy output counts từ final manifest đã đối chiếu M2/M3; kiểm các tổng month/distribution/item riêng. Không bỏ guard hoặc bổ sung field vào output READY. Fixture giữ đúng8 fields để regression.
- Browser lần đầu không chụp được do web503, không có provenance (`browser-2026-10-15T191926.459Z.json` FAIL); browser profile/log giữ evidence, browser do script mở được đóng. Lệnh đọc nhanh bằng Python inline có SyntaxError quoting, không truy cập dữ liệu; dùng PowerShell/script để đọc lỗi an toàn, không đưa secrets vào log.
- JAR runtime chép riêng theo SHA256, receipt pin binary/start/cmd/JAR/config/listener; stop đúng receipt trước build, không kill theo tên/cổng. Startup lần đầu observed wait9,417s là polling1s kèm kiểm identity, không benchmark thời gian app chính xác.

### Kết quả cuối kỹ thuật TV1

- **Build `build-06.log` PASS**, Java9 tests không skipped; shared12 synthetic và real4.293 prediction/luật tốt nhất vẫn khớp. Python17 regression PASS, ranking/protocol M3 không sửa. Test fixture không thay HTTP thật hoặc review người dùng.
- **Real HTTP119 requests PASS**, `artifacts/m4/http-2026-10-15T192557.991315+0000.json`, UTC19:25:57–19:27:05 ngày15/10 (=02:25:57–02:27:05 ngày16/10). Kiểm tất cả25 monthly buckets/426 basket-size buckets, GBP exact→HALF_UP2, 4.556 mã train, mọi trang856 rules/1.349 itemsets không mất/trùng, sort/filter/search/empty. Giỏ một/nhiều item, thiếu tiền đề, existing/dedup/input invalid/stale và toàn bộ4.556 mã không cắt. Source/run/version/config đúng, pointer không đổi sau HTTP.
- Ca thật dev558640: query `[21080,21094,21467,21770,22704,22969]` → `[21086,21212]`, tiền đề tốt nhất `[21080,21094]` và `[21080]`; Java/Python/HTTP/browser cùng kết quả. Mã train không có luật `10002` → rỗng, không fallback. Ca missing_one `[21094]` đối chiếu **toàn bộ** rules qua Python, không giả bỏ21094 là mọi luật21086 biến mất.
- HTTP lần3 FAIL vì verifier truyền BSON Int64 K cho protocol vốn yêu cầu Python int chính xác; sửa **biên verifier** thành int(k), không sửa protocol/check. Lần4 phát hiện rendering full-catalog basket: `EL1078E Concatenated string too long >100,000`, response incomplete (`http-2026-10-15T192214.716416+0000.json`, web192054 log). Sửa template render từng item trong details/list cuộn, không tăng ngưỡng SpEL hoặc cắt giỏ. Regression2 tên60.000 ký tự và HTTP thật4.556-item basket PASS.
- **Browser12 checks/9 ảnh PASS**, `artifacts/m4/browser-2026-10-15T192616.340Z.json`, Chrome155.0.8059.40 headless/CDP/Node24.16.0, desktop1440×1000, mobile390×844; JS search theo tên, giữ6 lựa chọn khi tìm mới, selected-only, giỏ rỗng/form cũ và kết quả thật. Không JS exception, không tràn ngang ở mobile giỏ. Browser exit0; profile riêng/log giữ, không dùng profile người dùng. Agent đã xem trực tiếp ảnh overview/recommendation/mobile và kiểm bố cục; chưa là TV1 review.
- Ảnh: `overview.png` và `overview-full.png` (toàn kỳ merchandise39.516 giỏ/4.895 mã/GBP); `patterns.png` (DEVELOPMENT N4.293); `itemsets.png` (train N29.335); `catalog-search.png` (tên train); `recommendation-real.png` (query dev558640, K5, căn cứ); `empty-basket.png`, `stale-form.png`, `basket-mobile.png`. Tất cả run7bc55ac7/version1, source SHA256 như trên, schema m0-contract-v1/basket-set cae0d9e7…/policy p01-first-p02-test-v1. Hash ảnh và mã cuối chốt trong final repository receipt để truy vết.

### Phiên bản, tài nguyên và giới hạn

- JAR thực: Boot4.1.1/Data MongoDB5.1.1/driver5.8.1/Thymeleaf3.1.5/Tomcat11.0.24, dependency names từ ZIP JAR trong HTTP receipt; JDK17.0.12/binary hash trong receipt web. Maven portable3.9.16, cache riêng `tmp/maven-repository`, offline `-o`, không nâng/cài toàn máy.
- Runtime JAR SHA256 `543bea0e7e3c6a39b5fb5a92ee42b9b933e18e214ae8a8a1ab1cc0a150c7a5b5`, PID3444, startUTC19:25:17.136421 ngày15/10; heap giới hạn256MiB, **không là RSS**. Startup poll12,931s gồm kiểm identity/listener, không tương đương boot CPU time.
- 119HTTP wall min0,0769s, median0,3023s, max10,5694s; cùng phiên có browser probe chạy song song, dữ liệu/cache/GC ảnh hưởng. Số này gồm query/validation/filter/render/transfer, chưa tách query-time hoặc benchmark tải/concurrency/SLA.
- RSS sampled mỗi1s trong HTTP: web peak369.254.400 byte (~352,15MiB), Mongo98.246.656 (~93,70MiB), verifierPython123.904.000 (~118,16MiB). Đo RSS có shared pages/bỏ sót peak giữa mẫu; không gọi tổng các peak riêng là peakcombined, không gồm Chrome/ứng dụng khác. Raw samples/availableRAM trong receipt; chưa đo RSS riêng startup/build hoặc máyTV2. JVM dự án thực chỉ web, Spark dừng trong cả đợt kiểm.
- Không sửa dữ liệu/outputs/freeze/M3 để pass, không chạy final evaluation hoặc M5/M6, không nghiệm thu máyTV2. Sự cố Mongo/schema/manifest dùng probe cô lập; chưa cố tình dừng Mongo thật hoặc thay active run thật để dựng lỗi. Helper publication có insert thật; CAS/timeout là nhánh code chưa diễn tập crash campaign M5.

## Review và bàn giao

- [Web Guide](../web/README.md) có lệnh start/status/stop, ba URL, gói7 bước TV1 kiểm trực tiếp và đáp án/source/run/scope. M1 launcher truyền SAMPLE/27018 tường minh để giữ hành vi cũ khi mặc định ứng dụng chuyển DEVELOPMENT; không chạy M1 batch trong M4.
- AC1: ba khu vực dùng dữ liệu thật/scope/mẫu số; AC2: đủ tiền đề/existing/dedup/no fallback/ranking chung; AC3: snapshot/input/rendering/query an toàn — **đạt kỹ thuật TV1** theo các layer đã nêu.
- **DoD đủ theo U-44**: sau khi có gói review cụ thể, người dùng trả lời nguyên văn **“Đã kiểm UI và đối chiếu, chấp thuận M4, không còn điểm sửa”**. Câu hỏi nêu Web Guide7bước/URL, KPI39.516/4.895/GBP19643861.64, dev505/4.293 và query6mã→21086/21212, cùng nguồn DoD Master Plan13. Xác nhận được người dùng báo lại, không suy từ Agent/browser. Receipt review riêng `artifacts/m4/review-20261016.json`; giữ nguyên runtime receipts trước đó. **Đóng M4 ngày16/10/2026 và dừng trước M5/M6**; không suy review thành runtimeTV2/GV/final/giờ đóng góp.

### Kiểm chốt repository / dữ liệu / lifecycle

`artifacts/m4/final-repository-verification.json` **PASS**: 60file pipeline/audit/freeze giữ hash đầu phiên; XLSX/source và hai Word không đổi, ranking/sharedJava/pom đúng integration hashes freeze. RTM và map đều282ID, 42dòngU cũ giữ nguyên; U-43/U-44 thêm theo giao việc/review thật. Diff tracked/untracked không whitespace lỗi, không staged/commit/push; dữ liệu/artifacts/DB/build/cache/.venv bị Git ignore. Web source không có Mongo mutation hoặc th:utext.

Postcheck DB chỉ đọc: active run/version1 đúng, selected manifest/receipt/config và logical checksums của catalog/itemsets/rules giữ nguyên sau119HTTP/browser; M2 manifest/39.516 baskets/5.347 summaries giữ đúng. Test cuối NOT_RUN. Không đọc test items hoặc chạy lại checkerM2 có mutation. Hash mã M4 và9ảnh chốt tại receipt trên; môi trường máyTV2 không được suy từ TV1.

Checker ban đầu dùng regex chỉ nhận một chữ trong prefix ID, đếm268 vì bỏ RUB; đọc checker M3/sourceRTM xác định lỗi kiểm, sửa thành `[A-Z]+` mới nhận đúng282. Không sửa RTM/map hoặc yêu cầu để pass; giữ `final-repository-verification-initial-fail.json` riêng. Đây là lỗi script kiểm chốt, không là mất14yêu cầu.

Lifecycle cuối: webPID3444 đúng executable/hash/start/args/JAR/listener127.0.0.1:8081; MongoPID26740/27019 đã có sẵn, giữ chạy. JVM dự án chỉ có web, Spark đã dừng; Chrome probe exit0. Dịch vụ27017 và JVM thesis khác giữ nguyên. Web được giữ để tái demo; `scripts/invoke-m4.ps1 -Action StopWeb` chỉ dừng process khớp receipt, giữ toàn bộ dữ liệu. **Dừng công việc tại M4 đã đóng theo U-44**, không tự mở M5/M6.

### Bàn giao sang thread M5 — 18/10/2026, U-45

Đọc lại AC/DoD/checklist/U-44/review receipt: **M4 đã đủ, không còn confirm/lựa chọn riêng để đóng**. Đã đọc lại hash freeze/verification và đối chiếu toàn bộ mã M4 trong `final-repository-verification.json`: khớp, không chạy lại model/test/DB sống. Snapshot Git main/HEAD4466ef7, M4 còn unstaged/untracked; đề nghị tiêu đề commit không có nghĩa Agent đã commit/push.

Đã soạn [M5 Start Prompt](../requirements-review/M5_START_PROMPT.md): end-to-end/publication/retry/final evaluation sau freeze, ghi `reports/M5_INTEGRATION_FINAL_EVALUATION_NOTES.md` từ lúc bắt đầu, hỏi bằng options/trade-off khi còn thiếu quyết định quan trọng và chờ trước phần phụ thuộc. Ghi rõ code M4 chỉ DEVELOPMENT/NOT_RUN, M2 checker có guard/mutation theo giai đoạn, M5 chưa có implementation/final scores. Chưa tạo notes M5 hoặc mở test cuối trong phiên này; snapshot process/lifecycle16/10 giữ lịch sử, không được gọi là trạng thái sống18/10. Bàn giao rồi dừng, không triển khai M5/M6 hoặc commit/push.
