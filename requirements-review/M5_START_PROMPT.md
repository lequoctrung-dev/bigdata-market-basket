# Prompt bắt đầu M5 trong thread mới

Ngày soạn: **18/10/2026**. M0–M4 đã đóng; phiên soạn prompt chỉ đọc nguồn và chuẩn bị bàn giao, **không triển khai M5 hoặc mở tập test cuối**. Copy phần sau dấu phân cách vào thread mới trong cùng project, hoặc dùng lời dẫn ngắn cuối file.

---

Bạn tiếp tục đồ án Nhập môn Big Data tại workspace:
`D:\University\Semester7\BigData\DoAn`.

Tôi giao bạn thực hiện **M5 — Tích hợp, công bố an toàn và đánh giá cuối**, gồm **M5-T1–T4** trong `requirements-review/13_MASTER_IMPLEMENTATION_PLAN.md`, nghiệm thu theo `requirements-review/14_MILESTONE_CHECKLIST.md`.

Hãy đọc tài liệu/mã nguồn liên quan, **triển khai trực tiếp và kiểm chứng thực tế trên dữ liệu thật, không chỉ lập kế hoạch**. Chỉ M5; bàn giao đạt hoặc checkpoint chưa đạt rồi dừng. Không tự mở M6/M7/M8, nghiệm thu máy thứ hai, commit/push hoặc gửi/nộp bài. Ngôn ngữ giao tiếp/tài liệu/UI tiếng Việt; stack PySpark batch riêng + FP-Growth + MongoDB + Spring Boot/MVC/Thymeleaf giữ nguyên.

**Quy tắc làm việc phải giữ:**

- Điều chưa biết/chưa rõ phải kiểm nguồn trước, không tự đoán hoặc gán giả định thành yêu cầu. Đọc version/config/caller/schema/receipt trước tái dùng; tra tài liệu chính thức khi cần.
- Nếu sau kiểm nguồn vẫn còn thiếu thông tin hoặc nhiều phương án ảnh hưởng đúng/sai, hành vi, dữ liệu, bảo mật, kiến trúc, protocol, schema/ownership hoặc phạm vi: nêu điều đã biết/chưa biết, tác động, **2–3 lựa chọn cụ thể, trade-off và phương án đề nghị; chờ tôi chọn trước phần phụ thuộc**, tiếp tục phần độc lập. Không âm thầm chọn phương án quan trọng rồi xin xác nhận sau.
- Không hỏi lại lựa chọn đã chốt. Chi tiết triển khai thông thường trong scope đã giao được tự chọn có căn cứ và ghi rationale; không biến chúng thành quyết định người dùng đã xác nhận.
- Ghi thông tin báo cáo **đồng thời khi quyết định/chạy**, không đợi cuối phiên dựng lại từ chat. Ngay khi bắt đầu tạo/cập nhật **`reports/M5_INTEGRATION_FINAL_EVALUATION_NOTES.md`**. Evidence chi tiết tại **`artifacts/m5/`**, ngoài Git. STATE/checklist/decisions là nơi điều phối/nghiệm thu, không tạo roadmap song song.

## 1. Đọc đầu phiên và xác minh trạng thái thật

1. Đọc đầy đủ `AGENTS.md`, `README.md`, `STATE.md`, `requirements-review/07_CONFIRMED_SCOPE.md`; kiểm branch/HEAD/status/diff liên quan, gồm untracked. Snapshot soạn prompt: **main / HEAD `4466ef75cbf229c1827614fd49e793dcb06c6e58`**, M4 và hồ sơ còn unstaged/untracked. Người dùng có thể commit trước khi sang thread; phải kiểm lại, không kết luận trạng thái commit/push từ snapshot này. Không overwrite/reset/clean/revert thay đổi có sẵn.
2. Đọc checklist14, nguyên văn M5-T1–T4/AC/DoD, quy tắc nghiệm thu/cổng/dependency và QD-08 tại Master Plan13. Tra RTM01, Report02, Deliverables03, Advisory09 và Map15 theo **B-E01–B-E07, B-V01–B-V05, B-T03/B-T04, B-H08/B-H09, B-O01; DEL-13/DEL-14/DEL-16**. Không sửa 282ID/câu nguồn/trọng số để khớp implementation.
3. Đọc file11 phần KPI/scope/ranking/đánh giá và file12 mục9–12/15–16: kiểu/khóa/chín collection, manifest theo stage, bất biến/READY/publication/CAS/retry/lỗi, train/dev/test. Chi tiết chưa được nguồn chốt không tự coi là quyết định đã duyệt.
4. Đọc đầy đủ `reports/M3_MODEL_DEVELOPMENT_NOTES.md`, `reports/M4_WEB_APPLICATION_NOTES.md`, `web/README.md`, receipt đóng M3/M4 cuối checklist14; đọc M2 notes/`pipeline/README.md` mục6–7 cho nguồn/preprocessing/tái tạo. M2 toàn kỳ khác train catalog và các mẫu số evaluation.
5. Đọc `pipeline/m2_source.py`, `m2_runtime.py`, `m2_pipeline.py`, `m2_final_verify.py` và callers liên quan; `m3_protocol.py`, `m3_prepare.py`, `m3_trial.py`, `m3_verify.py`, `m3_freeze.py`, shared `m3_ranking_cases.json`/tests. Phân biệt code đọc, code ghi và guard theo giai đoạn trước khi chạy bất cứ checker nào.
6. Đọc `scripts/m4_publish.py`, `invoke-m4.ps1`, `invoke-m2.ps1`, `verify_m4.py`, `m4_browser.mjs`; các helper đo tài nguyên `measure_m2.py`/`measure_m3.py` và summarize trước tái dùng. Đọc `web/pom.xml`, properties, toàn bộ Java/controller/service/ranking/templates/static/tests liên quan. M1 launcher/endpoints là mẫu, không phải luồng thật M5.
7. Đọc artifact thật đã chỉ ra dưới đây: freeze/hashes/selected receipt, preparation/split metadata, M4 publication/final verification/review. Kiểm hash và quan hệ ID; không dùng tên file hoặc receipt PASS lịch sử để suy process/DB/web đang khỏe.

Sau khi đọc, báo ngắn trạng thái, phần M5 đã rõ, kế hoạch triển khai/kiểm chứng và điểm quan trọng nào còn cần lựa chọn. Thực hiện phần đã đủ căn cứ, không yêu cầu tôi kể lại ngữ cảnh.

## 2. M0–M4 đã đóng, không hỏi lại nghiệm thu

- M0: contract `m0-contract-v1`, U-27 chín collection/run bất biến/active-version, U-28 decimal text, U-29 dashboard hàng hóa + audit, review U-30.
- M1: sample TV1 đạt, ngoại lệ U-33 chỉ miễn receiptTV2 ở M1; U-35 học/demo/review đủ. Không coi fixture5giỏ/7itemsets/9luật là dữ liệu thật.
- M2: toàn nguồn TV1/postcheck đạt; U-38 xác nhận TV2 review/chấp thuận không còn sửa.
- M3: train/development/freeze/postcheck/Java parity đạt; U-41 xác nhận TV2 review split/tính lại mẫu metrics và chấp thuận. Receipt PENDING_TV2 cũ là snapshot, không sửa bất biến để cập nhật review.
- **M4 đóng16/10/2026:** M4-T1–T4/AC1–AC3 đạt kỹ thuật TV1; **U-44: “Đã kiểm UI và đối chiếu, chấp thuận M4, không còn điểm sửa”**, đủ DoD. Không hỏi lại review M4 hoặc yêu cầu confirm riêng để chuyển M5.
- M4 đã nối/công bố DEVELOPMENT version1 và UI thật, gồm9Java tests (parity4.293query/best antecedent),17Python regression,119HTTP,12browser checks/9ảnh. Đây là evidence M4, **chưa là end-to-end/retry/crash/final evaluation của M5**.
- U-15/U-22/M6 vẫn yêu cầu hai máy tự full run riêng; không lấy TV1 hoặc imported outputs nghiệm thu TV2. Dataset/GV chấp thuận U-25, khungB/quy cáchA U-26, roles U-23 đã chốt. Không hỏi lại deadline/giờ tuần vẫn “chưa rõ” nếu không có thông tin mới; không cam kết kịp hạn.

## 3. Đầu vào và protocol phải giữ

| Trường | Snapshot đã nghiệm thu |
| --- | --- |
| Nguồn | `data/raw/online-retail-ii/online_retail_II.xlsx`,45.622.278byte; Online Retail II, Daqing Chen/UCI, DOI10.24432/C5CG6D, CC BY4.0 |
| Dataset/source SHA-256 | `bcbe73b35f5b7babf197fb0cb983a11f5d9ff929078d4aa53d171b1f2df2e980` |
| M2 preprocessing run | `d7fb3f21-115f-4793-a5fe-5c40b6da64cd`, VALIDATED/basket_set READY/PREPROCESSING |
| Basket set | `cae0d9e763ef38a086966d829fdeba9272f4d7fda7b61791bee9e9ba04b3287a` |
| Stage counts | 1.067.371 raw →1.033.036 P-01 →1.007.913 positive_valid →1.003.357 merchandise |
| Toàn kỳ merchandise | 39.516giỏ/4.895item/5.347summaries; exact `19643861.637`GBP, không phải doanh thu ròng |
| M3 selected run | **`7bc55ac7-0d24-4ddd-a9b0-3b25d247b596`**, FULL_SOURCE/MODEL_DEVELOPMENT/DEVELOPMENT/READY |
| Preparation | `artifacts/m3/preparation-7da29e52-53cf-4986-beff-dfaad251663c/` |
| Train/dev/test | 29.335/4.609/5.572giỏ; overlap0; train2.503single, dev316single; **test5.572 là tổng giỏ metadata, chưa phải số query đủ điều kiện** |
| Train catalog/model | 4.556item từ717.574dòng hàng train;1.349itemsets/856rules; cả item không có luật nằm catalog |
| Cấu hình chọn | minSupport=.01/minConfidence=.3/8partitions/local[2]/heap768m/stack4m; **K5/seed20261015** |
| Protocol/version | `m3-temporal-hide-one-v1`; SHA256 `68798cbc3c5eae28c51f6e7df4dfc98cab8d439a168da85ed326715eb2a30bdf` |
| Ranking | `confidence-lift-support-codepoint-v1`, không rounding trước so sánh |
| Schema/policy | `m0-contract-v1` / `p01-first-p02-test-v1`; policyhash `35f10093da02b67ad56ada7cbc498a79b25bd9ee02719e504b81e60b102a5016` |
| M4 publication | selected run nói trên/version1; đây là snapshot receipt, phải đọc pointer sống trước đổi |
| Final | **NOT_RUN trong snapshot M3/M4**; M5 mới được giao mở/đánh giá final theo protocol, không có score cuối hiện tại |

Biên local `[start,end)`, timezone nguồn **UNKNOWN**: train[01/12/2009,01/07/2011),dev[01/07,01/10/2011),test[01/10,10/12/2011). Fit/catalog/tên/baseline chỉ train; dashboard toàn kỳ chỉ mô tả. Giữ P-01 tuple8giá trị lấy đầu theo sheet/row, mapping P-02/TEST và giỏ không cắt tail. Không dedup bằng Invoice/StockCode, không loại toàn bộ mã chữ, không bỏ dòng chỉ vì thiếu CustomerID.

Artifact cần giữ ngoài Git:

- Freeze `artifacts/m3/freeze-1a1f2ec6-331e-4b02-9aaf-18804793d4e9/freeze.json`, SHA256 **`f7ee9c13432f0c99e7e5bcbf0363eed77eb4d5493b39e78fbb2e8e48557d053a`**; `verification.json` cùng thư mục SHA256 **`153263e3ceaddb50ceebc893942984b21ce70130cbea683ad633acfdbf601de6`**; `hashes.json` khóa chúng. M3 lưu config/protocol/source/policy/split/code/output và mọi trial.
- `artifacts/m3/<selected_run>/receipt.json`, `items.jsonl`, `frequent_itemsets.jsonl`, `association_rules.jsonl`, `dev-predictions.jsonl`, `resources.json`; `artifacts/m3/review-20261015.json` cho U-41.
- Logical checksums: items `a99f74a37f3a99f003e9b79debc3325e3c58783a0bef18e242669541c6063b54`; itemsets `c0348117dd5df9a8c07659c8c68e9f4ae729b91081fc7e0c2e1393c4dd830386`; rules `10d880e91f2fb4afc2b81640f500bb60ccfd6c525552154c07e0c37b589e0c96`. Đọc thuật toán/caller: logical bỏ `_id/run_id`, sort đúng canonical; khác raw file SHA256.
- M2 `artifacts/m2/pipeline-<M2_run>.json`, `final-verification-<M2_run>.json`; retained-lines `data/processed/m2/<basket_set>/<M2_run>/retained-lines.jsonl`, SHA256 **`82ddde19db72b295d723ebb3ca1068ccbabf3a44a49d8ab396598842e5bc5c74`**. Không sửa/ghi đè để khớp run mới.
- M4 `artifacts/m4/publication-2026-10-15T190951.833029+0000.json`, `http-2026-10-15T192557.991315+0000.json`, `browser-2026-10-15T192616.340Z.json`, `build-06.log`, `python-regression.log`, `review-20261016.json` cho U-44.
- `artifacts/m4/final-repository-verification.json` PASS snapshot, SHA256 đọc khi soạn **`4139ce9450948fd87bdc1b6d036eeb0b4dc09bca5dede7d369a80ec2c14f3f91`**; chứa M4 code/screenshot hashes. Không chạy lại checker snapshot này rồi kết luận M5 sai chỉ vì run/version/code đã đổi hợp lệ.

Clone thiếu artifacts không có nghĩa mốc cũ chưa chạy. Nếu thiếu inputs/evidence thật, xác định thiếu gì/cách tái tạo/ảnh hưởng; không dựng receipt, giả runID, xóa namespace hoặc mặc định chạy lại mọi mốc để chữa thiếu file.

## 4. Môi trường và các giới hạn code hiện tại

- Namespace nguồn thật theo U-37: **127.0.0.1:27019 / bigdata_m2**, dbpath `artifacts/m2/mongo-data`; giữ namespace qua milestone. Không ghi dịch vụ27017 hoặc SAMPLE27018. Loopback8081 cho web nếu khả dụng. Nếu cần namespace/quyền khác, trình lý do/lựa chọn trước phần phụ thuộc.
- Lifecycle snapshot cuối M4: MongoPID26740 đã có sẵn, webPID3444 được giữ cho demo, Spark dừng/Chromeexit0. **Không phải trạng thái sống ngày chạy M5.** Kiểm PID/executable/hash/start/cmd/args/listener/receipt và tài nguyên trước start/stop/build; chỉ dừng đúng process sở hữu. Sandbox chặn CIM/process/loopback phải xin quyền công cụ, không bypass hoặc suy process đã dừng. Không kill theo tên/cổng, không đụng JVM dự án khác.
- M4 JAR copy theo SHA256 `543bea0e7e3c6a39b5fb5a92ee42b9b933e18e214ae8a8a1ab1cc0a150c7a5b5`, receipt `artifacts/m4/web-process.json`; mode DEVELOPMENT/heap256MiB. Artifact build vẫn tên `market-basket-m1-0.0.1-SNAPSHOT.jar`, tên không quyết định mode. Đọc launcher trước tái dùng; không dùng M1 RunSample/VerifyWeb cho thật.
- Bộ đã thử TV1: JDK17.0.12, Boot4.1.1/DataMongo5.1.1/driver5.8.1/Thymeleaf3.1.5/Tomcat11.0.24, Mavenportable3.9.16/cache `tmp/maven-repository`; Python3.14.6/PySpark4.2.0/Scala2.13.18/connector11.1.0/PyMongo4.18.3. Kiểm bản thực; không nâng/cài toàn máy hoặc suy TV2 giống TV1. Đo RAM khả dụng trước JVM, RSS/đĩa/timing lúc chạy; heap/config không phải usage.
- **M2 checkers có guard giai đoạn cũ:** `m2_pipeline.py` đòi chưa có model/publication; `m2_final_verify.py` còn mutation invalidate checkpoint cũ. Không gọi máy móc trên DB đã có M3/M4. Muốn kiểm hoặc thực hiện end-to-end phải đọc caller, dùng validation theo stage/có phạm vi; không xóa model/pointer hoặc bỏ bảo vệ để test xanh. Nếu cách chạy đòi đổi contract/namespace/scope quan trọng, trình phương án rồi chờ.
- **M3 runners/verifier chỉ DEVELOPMENT:** `m3_prepare.py` trước đây chỉ lấy metadata test; `m3_trial.py`, `m3_verify.py`, `m3_freeze.py` chứa assumptions theo M3. Không gọi trial grid/chọn lại config bằng test; không sửa freeze cũ. Chạy fit lại **chỉ train, đúng cấu hình freeze** cho end-to-end thuộc M5 khi cần; không fit train+dev/toàn kỳ/test.
- **M4 chưa hỗ trợ FINAL:** `AnalysisResults` kiểm `MODEL_DEVELOPMENT/DEVELOPMENT`, manifest `final_status=NOT_RUN`; template có chữ NOT_RUN cố định. `m4_publish.main()` khóa selected DEVELOPMENT và không đổi pointer đã có; hàm `publish()` có CAS nhưng M4 thực chỉ insert lần đầu. HTTP/browser verifiers M4 có golden run/dev-counts. Phải mở rộng đúng stage/fields/callers/tests cho M5, không chỉ đổi nhãn/URI hoặc bỏ guard.
- `PROTOCOL`/freeze M3 có field `final_status=NOT_RUN` trong snapshot đã hash. Không sửa snapshot này để nói final đã chạy. Giữ reference/hash protocol freeze, ghi trạng thái/kết quả final ở artifact/manifest M5 mới theo contract. Nếu ngữ nghĩa stage/schema/tổ chức run thật vẫn chưa rõ sau đọc nguồn, trình options/trade-off trước mở test/chuyển publication; không tự ghi nối final metrics vào run READY cũ.
- Kiểu phải giữ: counts/frequency BSON Long; decimaltext→BigDecimal, HALF_UP2 trên tổng cuối; invoice local time/string không offset riêng với hệ thống UTC. M2 policy_hash ở **manifest**, quality payload chỉ có8stage nguồn trước khi manifest cuối thêm output counts; không đòi hai Document counts bằng nhau hoặc sửa READY output cho vừa mapper.

## 5. M5-T1/T2 — end-to-end và công bố an toàn

1. Triển khai/chạy end-to-end thật source→MongoDB→Spark→run→web theo Master Plan. Giữ lineage/hashes/sourceREADY/M2/split; chỉ một writer mỗi máy. Tái dùng nguồn bất biến hợp lệ không đồng nghĩa reset/import giả; phải ghi phần thực chạy mới và phần dùng lại/đã kiểm. Receipt M2/M3/M4 cũ riêng lẻ không tự thay receipt end-to-end M5.
2. Run mới dùng UUID mới, output ghi riêng; expected/actual counts kể cả0, canonical keys/unique/checksum/schema/BSON/ref/run/basket-set/catalog/train denominator đều kiểm trước VALIDATED→READY. Không dùng “run mới nhất”, không ghi đè READY/selected run hoặc sửa freeze để hợp thức hóa code M5. Ghi hash phiên bản code M5 đã chạy và liên kết freeze cũ.
3. Trước công bố đọc pointer sống. Chỉ công bố run hoàn chỉnh sau postcheck; cập nhật có điều kiện theo **cả run/version cũ**, matched0 dừng/readback, không blind upsert/replace. Timeout sau ghi phải đọc lại kết quả trước kết luận/thử lại. Giữ run cũ để request đã snapshot tiếp tục đọc nhất quán.
4. Ca ghi dở/FAILED/lỗi schema/count/hash/output thiếu/0luật hợp lệ; retry cùng payload không nhân bản, changed payload xung đột; retry chỉ khi writer trước đã kết thúc và inputs/config không đổi, nếu không rõ dùng run mới. Kiểm crash trước công bố giữ phiên cũ, kết quả không rõ sau đổi pointer được readback, CAS conflict không ghi đè.
5. Dùng dữ liệu thử/ID/probe cô lập có provenance cho lỗi và crash; không làm hỏng selectedrun/source/READY hoặc cho active sản phẩm trỏ fixture. Nếu cần namespace mới phải trình trước. Stop/crash chỉ process thử thuộc sở hữu, không dừng Mongo thật để tạo lỗi khi chưa được giao rõ.
6. Kiểm HTTP khi chuyển **run thật hoàn chỉnh**: trang giữ một snapshot run/version/scope, form cũ bị từ chối rõ ràng; request/form cũ không áp luật mới vào lựa chọn cũ. Chứng minh thất bại trước publication không làm web mất run trước. Tách fixture/unit/mock khỏi Mongo/HTTP thật; không gọi nhánh code đã viết là test crash runtime đã PASS.

## 6. M5-T3 — đánh giá cuối có kiểm soát

- Đây là lần được giao đánh giá tập test cuối sau freeze. **Trước lần đầu đọc test items/tạo mask/predictions**, kiểm freeze/config/source/split/training-only catalog/baseline/ranking và tất cả quyết định quan trọng còn thiếu; chuẩn bị kiểm harness bằng dev/fixture. Ghi UTC/thời điểm/lệnh/code/hash xác định test bắt đầu bị tiếp xúc.
- Giữ test[01/10,10/12/2011), toàn hóa đơn, K5/seed20261015/mask SHA-256/Unicode, cùng query/target/catalog/K cho luật và baseline. Không đổi cutoff/K/seed/minSupport/minConfidence/ranking/policy/names hoặc thêm fallback/lift filter theo kết quả test.
- Từ5.572giỏ test metadata, tính **thực tế** giỏ một item, giỏ≥2 đủ mask và Nquery; không dùng5.572 hoặc4.293 dev như mẫu số mặc định. Target mới ngoài train, context mới và query không có luật vẫn ở denominator chính; single-item báo riêng. Không lấy tên/frequency dev/test để bổ sung catalog/baseline train.
- Lưu từng query/target/Top-K/best rule key/consequent/antecedent/baseline, kết quả hit/nonempty, counts/metrics và checksum; Recall@K=hit/N với một target, tỷ lệ có gợi ý=nonempty/N. N0 ghi NOT_APPLICABLE/null, không ghi score0 giả. Score thấp hoặc thua baseline vẫn phân tích trung thực, không đặt ngưỡng chất lượng mới.
- Kiểm lại metrics từ predictions độc lập, mẫu tính tay có đáp án/căn cứ, Java–Python cả thứ tự và luật tốt nhất; giữ shared12case/regression liên quan. Báo runtime/resource theo bước và giới hạn, không gọi timing fit() riêng là toàn khai phá khi Spark lazy.
- Đã tiếp xúc test thì ghi rõ kể cả lần FAIL. Nếu phát hiện bug hoặc sửa logic làm thay model/kết quả, ghi exposure/lỗi/phạm vi ảnh hưởng và **trình cách xử lý protocol minh bạch trước chạy lại**; không giấu lần trước, chọn run có score đẹp hoặc gọi test đã dùng để chọn config là độc lập. Không sửa receipt/freeze/PENDING cũ thành kết quả mới.

## 7. M5-T4 — web, regression và bản bàn giao

- Web đọc đúng kết quả/stage được công bố, tách development/final và mẫu số, không copy score hoặc hiển thị NOT_RUN cố định khi final đã thực chạy. Source/full-period/train/catalog/money/current-run provenance rõ như M4. Không mở rộng sang SPA/auth/checkout/chat/RFM/cloud/cluster.
- Giữ logic đủ mọi tiền đề, loại item đã chọn, khử trùng ứng viên trước Top-K, luật tốt nhất confidence/lift/support/antecedent, xếp thêm StockCode Unicode; không rounding trước rank. Input rỗng/unknown/invalid/giới hạn báo lỗi, giữ lựa chọn hợp lệ, không tự cắt. Browser không gửi object Mongo/JSON/SpEL; search literal/allowlist/filter/page bounds, th:text/escape, không lộ secrets/stacktrace.
- Giữ regression M4 cho DEVELOPMENT, thêm kiểm FINAL riêng; expected chỉ thay khi có căn cứ contract. Rỗng đã được manifest xác nhận khác output thiếu/ghi dở. Catalog toàn bộ train kể cả item không có luật. Tên/giỏ dài render từng item: M4 đã gặp SpEL EL1078E ngưỡng100.000ký tự, không tăng ngưỡng/tắt bảo vệ để che lỗi.
- Build/Java/Python có báo skipped rõ; HTTP thật mọi khu vực/filter/page/giỏ, đọc DB postcheck, browser/ảnh thật cho stage cuối, web dùng outputs khi Spark dừng. Kiểm code/hash/JAR/config/runtime identity, không dùng health/listener/test fixture thay acceptance.
- Chốt build/run/config/hướng dẫn source→web cho báo cáo và M6; chỉ chuẩn bị đầu vào M6, không tự chạy/đóng full run hai máy hoặc mở M7. Không gán contribution/giờ người từ vai trò hoặc thời gian job.

## 8. Notes/evidence phải ghi đồng thời

Tại `reports/M5_INTEGRATION_FINAL_EVALUATION_NOTES.md`, tối thiểu:

1. Requirement IDs/nguồn/decisions, vấn đề→options/trade-off/đề nghị→câu trả lời; chi tiết kỹ thuật do Agent chọn có rationale, không gán thành user/GV đã duyệt.
2. Dataflow/classes/routes/fields và thay đổi contract theo stage; bảng UI/KPI→field/scope/denominator; chín collection/ownership, run/source/preprocessing/basket-set/schema/policy/protocol/config/freeze/IDs/hash/keys.
3. UTC start/end, HEAD/hash mã chưa commit, version/dependencies/config không bí mật, lệnh/inputs/output paths/steps và URLs; nguồn dataset/DOI/license/caption cho ảnh/bảng.
4. Run/publication trước–sau mỗi ca, expected/actual/count/checksum/readback, retry/conflict/crash/timeout/stale form; tách synthetic/real/Mongo/HTTP/browser và lưu FAIL/chưa chạy.
5. Ledger tiếp xúc test, N/testsingle/newtarget/context/no-rule, numerator/denominator, per-query prediction/hash, arithmetic check/Java parity, final vsdev/baseline/giới hạn khoa học. Không lộ customerID/thông tin cá nhân.
6. RAM khả dụng, heap/stack/partitions/guards, wall/startup/query/request timing khi đo, sampled RSS Python/JVM/Mongo/web riêng; phương pháp/tần suất/units/gaps/shared pages, disklogical/scratch/dataset/output. Không coi config là usage, samplepeak là exactpeak hoặc jobwall là giờ-người.
7. Bug→evidence→rootcause→fix→verification/regression và ảnh/provenance; review thực tế, AC/DoD đạt/chưa đạt, lifecycle process nào có sẵn/phiên mở/đã dừng/giữ lại, hướng dẫn demo/stop và giới hạn.

Logs/receipts/ảnh/predictions/resources chi tiết ở `artifacts/m5/`, dữ liệu/cache/build/scratch/.venv/secrets ngoài Git. STATE ngắn; checklist14 tick theo evidence; file07 ghi xác nhận mới; file11/12/13 chỉ cập nhật phần hiện hành sai do thay đổi được chấp thuận, giữ lịch sử/freeze cũ.

## 9. AC/DoD và điểm dừng

Đối chiếu nguyên văn Master Plan13:

- **M5-AC1:** mọi trang/request cùng run/scope, không đọc ghi dở, retry không nhân bản kết quả.
- **M5-AC2:** final metrics tái tính/phân tích được dù thấp; không dùng final chọn lại config rồi gọi test độc lập.
- **M5-AC3:** không còn lỗi đã biết làm sai số liệu/gợi ý hoặc ngăn demo; giới hạn nhỏ khác ghi rõ.
- **DoD:** **hai người review run/metrics và lỗi đã sửa**, có hướng dẫn nguồn→web. TV2 tính lại mẫu final/review theo M5-T3. Sau khi có gói evidence/đáp án cụ thể mới hỏi phần review M5 còn thiếu; không suy U-41/U-44, Agent/unit/HTTP thành review M5 hoặc runtimeTV2.

Kết thúc đọc final diff gồm untracked, `git diff --check`, links/282IDs/ignore và hashes nguồn/freeze/outputs cũ; chốt postcheck DB/pointer/run/JAR và lifecycle thật. Không chạy snapshot verifier cũ để ép M5 khớp stage/ID/code M4; giữ receipt riêng theo mốc. Không commit/push/reset/drop/cleanup hoặc mở M6/M7/M8.

**Bàn giao M5 đạt hoặc checkpoint chưa đạt rồi dừng.** Nếu còn blocker/quyền/review hoặc quyết định quan trọng chưa đủ căn cứ, nêu chính xác phần đạt/chưa đạt, tác động, lựa chọn/đề nghị và việc độc lập đã hoàn tất. Không tự hạ AC hoặc mở mốc khác để né blocker.

Hãy bắt đầu đọc và thực hiện M5 theo các chỉ dẫn trên, không yêu cầu tôi kể lại các quyết định đã có trong repository.

---

## Lời dẫn ngắn để paste vào thread mới

```text
Tôi giao bạn thực hiện M5 — Tích hợp, công bố an toàn và đánh giá cuối tại D:\University\Semester7\BigData\DoAn.
Hãy đọc đầy đủ requirements-review/M5_START_PROMPT.md, sau đó đọc tài liệu/mã nguồn được chỉ dẫn và triển khai, kiểm chứng thực tế đúng M5-T1–T4. Không chỉ lập kế hoạch.
M0–M4 đã đóng; U-41 đủ review M3 và U-44 xác nhận tôi đã kiểm UI/đối chiếu, chấp thuận M4 không còn điểm sửa. Không hỏi lại nghiệm thu các mốc cũ.
Ngay khi bắt đầu tạo/cập nhật reports/M5_INTEGRATION_FINAL_EVALUATION_NOTES.md; làm tới đâu ghi quyết định/thông số/fields/KPI/mẫu số/run/source/config/hash/lệnh/phiên bản/kiểm chứng/ảnh/tài nguyên/lỗi/evidence/review tới đó để dùng cho báo cáo. Cập nhật STATE/checklist/decisions theo bằng chứng.
Điều chưa biết/chưa rõ phải kiểm nguồn trước. Nếu vẫn thiếu thông tin hoặc có lựa chọn quan trọng ảnh hưởng đúng/sai/hành vi/dữ liệu/bảo mật/kiến trúc/protocol/schema/scope, nêu tác động,2–3phương án/trade-off/đề nghị và chờ tôi chọn trước phần phụ thuộc; tiếp tục phần độc lập. Không tự quyết thay tôi hoặc hỏi lại quyết định đã chốt.
Giữ freeze/protocol/config và các run READY cũ bất biến; chỉ fit train với cấu hình đã freeze khi cần cho end-to-end. M5 được đánh giá tập test cuối sau kiểm freeze, phải ghi thời điểm tiếp xúc test; không tune/refit train+dev/toàn kỳ hoặc đổi mô hình theo score test.
Chỉ M5; bàn giao đạt hoặc checkpoint chưa đạt rồi dừng. Không tự mở M6/M7/M8, nghiệm thu máy thứ hai, commit hoặc push.
```
