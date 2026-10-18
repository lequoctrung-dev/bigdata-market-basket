# Prompt bắt đầu M6 trong thread mới

Ngày soạn: **19/10/2026**. M0–M5 đã đóng; đây là chuẩn bị bàn giao theo U-49, **chưa triển khai hoặc nghiệm thu M6**. Copy phần sau vào thread mới trong cùng project, hoặc dùng lời dẫn ngắn cuối file để yêu cầu đọc đầy đủ tài liệu này.

---

Bạn tiếp tục đồ án Nhập môn Big Data tại workspace:
`D:\University\Semester7\BigData\DoAn`.

Tôi giao bạn thực hiện **M6 — Full run và demo trên cả hai máy**, đúng **M6-T1–T4** trong `requirements-review/13_MASTER_IMPLEMENTATION_PLAN.md`, nghiệm thu theo `requirements-review/14_MILESTONE_CHECKLIST.md`. Hãy đọc nguồn, triển khai phần cần thiết và kiểm chứng thực tế; **không chỉ lập kế hoạch**. Chỉ M6, bàn giao đạt hoặc checkpoint chưa đạt rồi dừng; không tự mở M7/M8, commit/push, nộp bài hoặc liên hệ người khác. Ngôn ngữ tài liệu/UI/giao tiếp tiếng Việt. Giữ stack PySpark local + FP-Growth + MongoDB + Spring Boot/MVC/Thymeleaf, batch riêng, web chỉ đọc kết quả hoàn chỉnh.

## 1. Nguyên tắc làm việc và ghi chép bắt buộc

- Giữ các nguyên tắc trong AGENTS.md và chỉ dẫn hiện tại của tôi: correctness → data integrity → security → maintainability → simplicity; giải pháp thực dụng cho hai laptop, không thêm hạ tầng/service/cloud/SPA/tính năng bán hàng ngoài scope.
- Điều chưa biết phải kiểm tài liệu, mã, caller, config/schema, receipts và môi trường thật trước. Không biến giả định, bản đề xuất hoặc snapshot lịch sử thành yêu cầu đã duyệt hay trạng thái đang sống.
- Nếu sau kiểm nguồn vẫn thiếu thông tin hoặc còn lựa chọn quan trọng ảnh hưởng đúng/sai, hành vi, dữ liệu, bảo mật, kiến trúc, protocol/schema/ownership hoặc phạm vi: **nêu đã biết/chưa biết, tác động, 2–3 phương án cụ thể, trade-off và đề nghị; chờ tôi chọn trước phần phụ thuộc**, tiếp tục phần độc lập. Không tự hiểu/tự chọn bừa rồi xin xác nhận sau. Chi tiết kỹ thuật thông thường trong scope được tự giải quyết có căn cứ, ghi rationale; không gán thành xác nhận U của tôi.
- Không hỏi lại quyết định đã chốt hoặc nghiệm thu M0–M5. Không hỏi lại deadline/giờ tuần “chưa rõ” nếu chưa có thông tin mới; không cam kết kịp hạn hoặc tự gán giờ-người/đóng góp từ thời gian job.
- **Ngay khi bắt đầu M6 tạo/cập nhật `reports/M6_FULL_RUN_TWO_MACHINES_NOTES.md`.** Làm tới đâu ghi thông tin phục vụ báo cáo tới đó: quyết định, nguồn/lý thuyết, config/version, inputs/outputs, machine-role, run/lineage/hash, counts/KPI/tử số/mẫu số, lệnh/UTC, tài nguyên, lỗi/cách sửa, kiểm chứng/ảnh, thao tác/giải thích/review thật. Không đợi cuối phiên dựng lại từ chat.
- Evidence mới đặt ngoài Git tại **`artifacts/m6/TV1/` và `artifacts/m6/TV2/`**; thư mục role không chứng minh máy/người đã chạy. Receipt phải ghi đúng máy quan sát thực, ai thao tác theo nguồn xác nhận và phần Agent hỗ trợ. Dữ liệu, môi trường/cache/build/scratch/DB/secrets vẫn ngoài Git.
- STATE giữ trạng thái ngắn, checklist14 giữ AC/DoD/receipts, file07 giữ quyết định người dùng; cập nhật theo bằng chứng, không tạo roadmap hoặc decision log song song. Không tự tick bằng sự tồn tại của file, build/health xanh hoặc receipt import.

## 2. Đọc đầu phiên, xác minh và báo ngắn trước phần phụ thuộc

1. Đọc đầy đủ `AGENTS.md`, `README.md`, `STATE.md`, `requirements-review/07_CONFIRMED_SCOPE.md`; kiểm branch/HEAD/status/diff cả untracked. Snapshot soạn prompt: main, HEAD **`e6a4b76b1ea057b0ff2b4d61051043996f3e8582`**, thay đổi M5 và hồ sơ đang chưa commit. Người dùng có thể commit trước thread mới; kiểm lại, không kết luận từ snapshot. Không reset/clean/revert/overwrite thay đổi có sẵn; không stage/commit/push khi chưa được giao.
2. Đọc nguyên văn M6-T1–T4/AC1–AC3/DoD, dependencies/cổng G-TWO/G-SPLIT/QD-03/QD-08 trong Master Plan13, checklist14 và receipt đóng M5. Tra RTM01, Deliverables03, Map15 theo **B-O02/B-O05/B-O06, B-E04/B-E07, B-N03, DEL-21/DEL-22/DEL-30, U-15/U-22**. Giữ 282ID/câu nguồn/trọng số, phân biệt hướng dẫn/diễn tập M6 với báo cáo/nộp/thuyết trình M7/M8.
3. Đọc đầy đủ `reports/M5_INTEGRATION_FINAL_EVALUATION_NOTES.md`, `web/README.md`, M2/M3 notes và `pipeline/README.md` mục setup/6/7; đọc file11 phần policy/KPI/đánh giá và file12 mục9–12/15–17. Nguồn archive, retained lines, basket set, catalog train, summaries toàn kỳ và model run là các lớp khác nhau.
4. Đọc `pipeline/m2_source.py`, `m2_runtime.py`, `m2_pipeline.py`, `m2_final_verify.py` và callers; `m3_protocol.py`, `m3_prepare.py`, `m3_trial.py`, `m3_verify.py`, `m3_freeze.py`; các file `pipeline/m5_*.py`, shared `m3_ranking_cases.json`/tests. Phân biệt read-only và mutation/guard theo stage trước gọi checker/runner. Không giả định runner M5 đã portable cho M6.
5. Đọc lifecycle `scripts/invoke-m2.ps1`, `invoke-m5.ps1`, measurement/summarize M2/M5, `m5_publish.py`, `m5_preflight.py`, `m5_final_verify.py`, `verify_m5.py`, `m5_browser.mjs`. Đọc pom/properties/Java/template/tests liên quan trước sửa web/parity. M1 RunSample không phải luồng FULL_RUN.
6. Đọc artifact tham chiếu mục4 dưới, kiểm hash/quan hệ IDs. Kiểm khả năng truy cập **từng máy**, OS/CPU/kiến trúc/RAM/disk/version thực tế, dependency có sẵn, process receipt/executable/hash/start/args/listener/DB trước mọi start/stop/build/run. PID snapshot không phải process sống. Không in secrets hoặc thông tin khách/cá nhân vào log.

Sau đọc báo ngắn: phần M6 đã rõ, các giới hạn code/máy, kế hoạch triển khai/kiểm chứng, thông tin hoặc lựa chọn quan trọng còn thiếu và phần độc lập sẽ làm. Không yêu cầu tôi kể lại toàn bộ ngữ cảnh.

## 3. M0–M5 đã đóng; không xin confirm lại

- M0 contract/schema `m0-contract-v1`, chín collection, run bất biến/active-version/U-27, decimal text/U-28, dashboard merchandise + audit/U-29; review U-30.
- M1 mẫu TV1 và học/review U-35 đã đóng; **U-33 chỉ miễn receipt TV2 ở M1**, không miễn U-15/U-22/M6. Không coi SAMPLE là dữ liệu thật.
- M2 preprocessing toàn nguồn TV1/postcheck và review U-38 đã đóng; M3 train/dev/freeze/parity/review U-41 đã đóng; M4 website/review U-44 đã đóng.
- **M5 đóng18/10/2026**: U-47 chọn DEVELOPMENT UUID mới end-to-end→web trước, rồi FINAL UUID mới dùng nguyên model đã kiểm checksum. U-48: **“Cả hai đã review; TV2 tính lại mẫu; chấp thuận M5, không còn điểm sửa”**, đủ phần human review của DoD. Receipt runtime/freeze còn PENDING là snapshot bất biến trước review; receipt review riêng cập nhật sự kiện, không sửa READY.
- M5 đã có21Python/11Java,108HTTPdev/118HTTPfinal, crash writer/publisher/retry/CAS/readback,80GET qua chuyển phiên,14browserchecks/10ảnh. Đây là M5/TV1 và review được người dùng xác nhận, **không phải hai receipt FULL_RUN tự thực hiện trên hai máy**.
- Không còn lựa chọn/confirm riêng để hoàn thành M5. Thông tin máyTV2/quyền truy cập/cách nhận evidence là đầu vào vận hành M6, hỏi đúng lúc cần, không dùng để mở lại nghiệm thu M5 hoặc tự hạ yêu cầu hai máy.

## 4. Nguồn, freeze và kết quả tham chiếu phải giữ

| Trường | Tham chiếu đã đóng; kiểm lại trước sử dụng |
| --- | --- |
| XLSX | `data/raw/online-retail-ii/online_retail_II.xlsx`,45.622.278byte, hai sheet; Daqing Chen/UCI/Online Retail II/DOI10.24432/C5CG6D/CC BY4.0 |
| Source/dataset SHA256 | `bcbe73b35f5b7babf197fb0cb983a11f5d9ff929078d4aa53d171b1f2df2e980` |
| Schema/policy | `m0-contract-v1` / `p01-first-p02-test-v1`, policyhash`35f10093da02b67ad56ada7cbc498a79b25bd9ee02719e504b81e60b102a5016` |
| M2 run / basket set | `d7fb3f21-115f-4793-a5fe-5c40b6da64cd` / `cae0d9e763ef38a086966d829fdeba9272f4d7fda7b61791bee9e9ba04b3287a` |
| Stage counts / summaries | 1.067.371raw→1.033.036P-01→1.007.913positive_valid→1.003.357merchandise;39.516giỏ/4.895item/5.347summaries;GBP exact`19643861.637` |
| M3 selected / preparation | `7bc55ac7-0d24-4ddd-a9b0-3b25d247b596` / `artifacts/m3/preparation-7da29e52-53cf-4986-beff-dfaad251663c/` |
| Freeze | `artifacts/m3/freeze-1a1f2ec6-331e-4b02-9aaf-18804793d4e9/freeze.json`,SHA256`f7ee9c13432f0c99e7e5bcbf0363eed77eb4d5493b39e78fbb2e8e48557d053a` |
| Freeze verification | Cùng thư mục `verification.json`,SHA256`153263e3ceaddb50ceebc893942984b21ce70130cbea683ad633acfdbf601de6`;`hashes.json` khóa hai file |
| Protocol / ranking | `m3-temporal-hide-one-v1`,SHA256`68798cbc3c5eae28c51f6e7df4dfc98cab8d439a168da85ed326715eb2a30bdf` / `confidence-lift-support-codepoint-v1` |
| Cấu hình khóa | support.01/confidence.3/8partitions/local[2]/heap768m/stack4m/K5/seed20261015;max_job_seconds600/max_outputs200000 là guard vận hành |
| Split / model | train29.335/dev4.609/test5.572,overlap0;train2.503single/dev316single/test389single;catalog4.556train,itemsets1.349/rules856 |
| Development | N4.293: luật505hit/3.513nonempty;baseline109hit/4.293nonempty |
| M5 integrated / FINAL | `8cef7ef5-6731-47b1-bcd7-bd908cfad7b2` / `04c940db-313d-4a05-a039-90163e33f070` |
| Final | N5.183: luật451hit/4.214nonempty(Recall8,7015%/rate81,3043%);baseline91hit/5.183nonempty(1,7557%/100%);825newtarget/969no-rule vẫn trongN |
| Lần test tiếp xúc đầu | **2026-10-18T15:05:29.761348+00:00**,ledger`artifacts/m5/<FINAL>/test-access.json`; M6 là replication đúng freeze, không test độc lập mới |
| FINAL receipt | `artifacts/m5/<FINAL>/receipt.json`,SHA256`e2552b5aca7fc45c2c86a32f53700ed474bb0c2e670ed0424f9fa332c1da7efe` |
| Model logical checksums | items`a99f74a37f3a99f003e9b79debc3325e3c58783a0bef18e242669541c6063b54`;itemsets`c0348117dd5df9a8c07659c8c68e9f4ae729b91081fc7e0c2e1393c4dd830386`;rules`10d880e91f2fb4afc2b81640f500bb60ccfd6c525552154c07e0c37b589e0c96` |

Biên local/timezone nguồn UNKNOWN: train[01/12/2009,01/07/2011),dev[01/07,01/10/2011),test[01/10,10/12/2011). Mask SHA256 canonical/version/seed/invoice; một target mỗi giỏ≥2item, không cắt giỏ lớn hoặc bỏ unknown/no-rule khỏi denominator. Fit/catalog/tên/baseline **chỉ train**, không train+dev/toàn kỳ/test. P-01 tuple8giá trị trước chuẩn hóa lấy đầu theo sheet/row; P-02 mapping/TEST loại theo căn cứ, giữ mã chữ/khách thiếu. Counts tiền và summaries toàn kỳ không dùng thay train/catalog.

Artifact bổ sung cần đọc: M2 pipeline/postcheck/retained-lines SHA256`82ddde19db72b295d723ebb3ca1068ccbabf3a44a49d8ab396598842e5bc5c74`;M5 `<FINAL>/test-{baskets,queries,predictions}.jsonl`,`independent-final-verification.json`,postcheck/resources-m5; `artifacts/m5/review-20261018.json`, `repository-final-2026-10-18T152538.488892+0000.json` (SHA256`1f790929b5741126a2ae884ee81420162ec3de0613469411b3b8334c25901898`). Logical checksum canonical/sort/bỏrun_id khác raw byte hash; output mới có UUID/mốc/partition-order khác không được so bytes mù hoặc sửa expected để ép khớp.

Clone thiếu artifacts là thiếu inputs/reference cục bộ, không chứng minh mốc cũ chưa chạy. Xác định cần mang **dataset/config/freeze/reference** gì và phải tự tái tạo **outputs/runtime** gì. Không dựngreceipt/giảID hoặc copy Mongo/output M5 rồi gọi là FULL_RUN máyTV2. Nếu thiếu bằng chứng thật không thể tái tạo an toàn, ghi checkpoint và hỏi đúng phần thiếu.

## 5. Giới hạn thực tế phải xử lý trước full run M6

- Namespace đã duyệt U-37: loopback27019/`bigdata_m2`,dbpath`artifacts/m2/mongo-data`; M1 là27018, dịch vụ27017 không thuộc scope. Web loopback8081. Snapshot cuối M5 webPID14344/MongoPID13768/JARhash`5a7357a51d4b92c15679c0ad3847fa9e8c628b0327da07d68fd66db619f07aa6`,activeFINAL/version3; **không phải trạng thái sống của thread mới hoặc máyTV2**. Kiểm receipt/executable/hash/start/cmd/listener trướcstart/stop/build. Chỉ stop đúng process sở hữu; không kill theo tên/cổng, không tác động JVM dự án khác. Lỗi quyền CIM/loopback dùng approval công cụ, không bypass hoặc suy process đã dừng.
- TV1 đã quan sát Windows11x64/i5-13500H/RAM15,63GiB; bộ đã chạy: JDK17.0.12/Python3.14.6/PySpark4.2.0/Scala2.13.18/connector11.1.0/PyMongo4.18.3/Mongo8.3.8/Mavenportable3.9.16/Boot4.1.1. TV2 chỉ có thông tin người dùng Windows11/RAM16GB/50GBtrống; **CPU/version/khả năng chạy chưa kiểm**. Không copy .venv/đường dẫn tuyệt đối/receipt process sang máy khác để coi hợp lệ. Không cài/nâng stack toàn máy khi chưa có phạm vi/quyền phù hợp; nếu cần thay version, kiểm tương thích và tài liệu chính thức trước, ghi quyết định/hashes/ảnh hưởng tái lập.
- `m2_pipeline.py`/`m2_final_verify.py` có guard chưa có model/publication; final verifier M2 còn invalidate checkpoint cũ. **Không gọi máy móc trên namespace đã có M3–M5**, không xóa active/model để qua guard. M6 cần luồng full preprocessing/validation theo stage giữ dữ liệu cũ. Nếu cần namespace mới hoặc đổi ownership/protocol/schema lớn, nêu2–3phương án/trade-off/chờ lựa chọn trước ghi. Không tự tạo clean install bằng reset/drop.
- `m3_prepare.py` khóa M2_RUN/BASKET_SET; `m5_common.py` khóa M2/M3selected/preparation/freeze local; `m5_model.py` đang gắn `machine_role='TV1'`; evaluator/publisher/verifiers còn phụ thuộc artifacts M5. Launcher pin path/root, m5_final_verify khóaversion3/HEAD M5. **Đổi tên thư mục/role không biến thành runner M6 portable hoặc máyTV2.** Thiết kế entrypoint/config/checker M6 có lineage riêng sau đọc nguồn; giữ semantics/hash freeze và bằng chứng code đã chạy M2–M5, không sửa freeze/READY/history để vừa script mới. Không gọi checker snapshot M5 rồi kết luận M6 sai chỉ vì UUID/version/HEAD đổi hợp lệ.
- Bản thân `provenance.code_sha256` liệt kê rộng cả script không được dùng làm input fit. M5 đã ghi lỗi guard quá rộng với hash m3_freeze trước/sau hoàn thiện; dùng ranh giới mã train/input/ranking/deps có căn cứ và lưu hash mã M6 mới, không bỏ kiểm hoặc đòi mọi tài liệu/script sau M3 phải cùng hash snapshot cũ.
- Full run U-22 gồm **nhập/đối chiếu toàn nguồn→Spark preprocessing→fit train đúngconfig→đánhgiá→publish/web** trên từng máy. Reuse source/basket/model M5 chỉ được ghi đúng phần reuse; không tự coi M5 integrated từng tái dùng source/preprocessing là đã đủ FULL_RUN M6-T2. READY import retry có thể kiểm toàn bộpayload mà không sửa nguồn; nếu dùng cần chứng minh đọc đủ1.067.371dòng, không gọi probe2.000dòng là full import. Phân biệt physical insert0 do sourceREADY với không thực hiện nhập/đối chiếu toàn nguồn.

## 6. Thực hiện M6-T1–T4

**M6-T1 — Hoàn thiện luồng và hướng dẫn chạy.** Đọc giới hạn trên; lập hướng dẫn/entrypoint tái lập từ XLSX đúnghash đến web theo frozenconfig, machine-role và inputs do máy đó tạo thật, không hard-code UUID TV1 sangTV2. Cho phép giữ referencefreeze cũ để đối chiếu, không lấy referenceoutputs thay tính toán. Kiểm bằng unit/fixture/dev phù hợp trước fullsource; chỉ sửa implementation/doc cần cho M6, không tune hoặc thêm feature. Thiết lập mộtwriter/identity/output-directory mới có guard, expected/actual/schema/keys/BSONLong/cross-reference/checksum trướcVALIDATED→READY; giữ lỗi/partial để chẩn đoán. Quyết định quan trọng chưa đủ nguồn thì hỏi trước phần phụ thuộc.

**M6-T2 — TV1 tự full run và demo.** Kiểm RAM/disk/process/version mới; chạy thật nguồn đầy đủ/nhập/preprocessing/fittrain/evaluation theo hướng dẫn và lưu measurements/receipts riêng M6. Không đổi cấu hình học theo score hoặc bỏtail/single/missingcustomer/unknown. Với dữ liệu/namespace cũ, bảo vệactive/READY/freeze trước mutation, mọi output run UUID mới. Dừng Spark sau batch; kiểm Mongo/web dùng đúngrun/scope/config, ranking/KPI/parity vàformstale/khôngluật. Ghi phần TV1 tự thao tác/giải thích thật và TV2 review theo nguồn xác nhận; Agent chạy kỹ thuật hỗ trợ không tự đồng nghĩa TV1 đã demo/giải thích. Nếu thiếu thao tác người thật, tạo gói cụ thể có đáp án rồi hỏi phần còn thiếu.

**M6-T3 — TV2 tự full run trên máyTV2.** Kiểm môi trường thực/đườngdẫn/quyền/setup/phụthuộc/network/RAM/disk trên chính máy đó, dùng source/freeze/config đãchốt, chạy toànluồng và demo tương tự, receipt/resources độc lập. UUID/process/timestamp/path/bytes có thể khác; đối chiếu policy/source/split/train/catalog/logicalmodel/metrics và ranking theo comparator không làmtròn. Dữ liệu export chỉ đối chiếu. Không chạy hai lần trênTV1 gắn roleTV2 hoặc sửa importedreceipt. Nếu chưa truy cập được máyTV2, hỏi tốithiểu cách thực hiện/nhận evidence có căn cứ: chạy trực tiếp trong workspace trên máyTV2 hoặc hướng dẫnTV2 chạy và cung cấp góilogs thật. Hoàn thành phần độc lập trênTV1/hướng dẫn trước, **giữ T3/AC3 chưa đạt** nếu chưa có evidence; không tự suy máy giống nhau hoặc đổi scope miễnTV2.

**M6-T4 — Sửa hướng dẫn, kiểm lifecycle và diễn tập.** Sau người thứhai làm theo guide, ghi lỗi ở bước nào/nguyênnhân/fix và kiểm lại phần ảnh hưởng. Thử start→batch→Sparkstop→webdemo→stop đúng ownership; không cần dừng dịch vụ không thuộc dựán hoặc làm hỏng DB thật để dựng lỗi kết nối. Mongo unavailable/schema/error có thể dùng probe riêng và ghi đúng lớp evidence; phần lifecycle/demo mỗi máy vẫn cần chứng minh thật. Cảhai giải thích được phần mình và luồng chung; đối chiếu source/run/config/outputs và giữ ảnh/caption/provenance. Diễn tập M6 không thay thuyết trìnhGV/nộpM8.

## 7. Ghi nhận báo cáo, chất lượng và giới hạn

Trong `reports/M6_FULL_RUN_TWO_MACHINES_NOTES.md`, duy trì bảng riêng TV1/TV2: actualaccess/runtime/humansteps/review; source/hash/header/sheets/policy/schema; codeHEAD/hash dirty/referencefreeze; versions/runtimeconfig/heap/stack/guards; UTC/timings từngstage; stagecounts/lineage/DecimalGBP/baskets/train/dev/test/single; eligibleN/hit/nonempty/newtarget/context/no-rule; outputs/validation/logicalchecksums; publicationbefore/after/CAS/readback/formsnapshot; URLs/screenshots/answerkeys; lỗi→evidence→rootcause→fix→regression; lifecycleowningprocess/kept/stopped.

Đo RSS mỗi nhóm Python/JVM/Mongo/web, RAMkhảdụng, disklogical/scratch/dataset/output/timing khi thực chạy; ghi interval/units/gaps/sharedpages, sampledpeak không exactpeak, heap/config không usage, walljob không giờ-người. Không ghi resources máyTV2 từTV1 hoặc cộng peak khác thờiđiểm thành combined. CPU/version chỉ ghi từ quan sát thật.

Test đã tiếp xúc M5: M6 so sánh tái lập đúng cấu hình, ghi thời điểm/command/code/hash tiếp xúc lại và mọi FAIL. Không gọi là tập test độc lập mới; không chọn lại K/seed/cutoff/support/confidence/policy/ranking bằng score. Nếu bugfix làm thay model/kếtquả, dừng phần phụ thuộc, ghi exposure/ảnhhưởng và trình phương án protocol trước chạy lại. N0 giữ NOT_APPLICABLE/null. Kết quả thấp/khác giữa máy phải điều tra, không sửa expected/tolerance/receipt hoặc bỏ bảo vệ để épPASS.

Giữ train-onlycatalog/tên/baseline và Java–Python ranking/parity. Web chỉ nhận mã catalogtrain; offline unknown context/target vẫn trongN. Dashboard toàn kỳ khác mẫu sốtrain/evaluation. Case demo sáu mã21080/21094/21467/21770/22704/22969→21086/21212 là case dev558640, không gọi test mới. Mẫu final10query đầu:1hit/7nonempty luật,0hit/10nonempty baseline chỉ là kiểm toánmẫu, không thay toàn bộN5.183 hoặc fullrunTV2.

## 8. AC/DoD, kiểm chốt và điểm dừng

- **M6-AC1:** cảhai máy web+Mongo dùng đúng output, thao tác khi Spark đã dừng; không thay bằngảnh/health.
- **M6-AC2:** giỏ/ranking/statistics khớp snapshot; từng người giải thích phần mình và luồng chung. Agent/unit/HTTP không tự thay phần người thật.
- **M6-AC3:** **hai receipt FULL_RUN thật**, không SAMPLE/importedoutput/lượtTV1đổinhãnTV2. Bằng chứng M5 không thayT2/T3.
- **DoD:** hướng dẫn đã sửa sau người thứhai chạy; start/demo/stop đã thử đúng phạmvi, môi trường/lỗi/giớihạn ghi rõ. Không tự xác nhận máyTV2/GV/giờ/đónggóp. Sau có gói cụ thể mới hỏi phần review/thao tác người thật còn thiếu, không hỏi lạiU-48.

Trước bàn giao: đọc finaldiff cảuntracked; `git diff --check`; kiểm links/282ID/ignore/no staged/commit/push; nguồn/freeze/runREADY/referenceM5 hashes; postcheckDB/pointer/JAR/lifecycle từng máy thực truy cập. Không chạy snapshotchecker cũ làm sai giaiđoạn, không sửa historicalreceipts. STATE/checklist tick đúng evidence; reportnotes có lệnh/đápán/đườngdẫn/checkpoint/lỗi/phầnchưakiểm.

**Bàn giao M6 đạt hoặc checkpoint chưa đạt rồi dừng.** Nếu chỉTV1 đạt, ghi rõTV1/T1/T4phầnđãkiểm và TV2/T3/AC3chưađạt, thiếuquyền/input/evidence nào, lựa chọn cầnngười dùng và phầnđộc lập đãxong. Không tự mở M7/M8, commit/push/reset/drop/cleanup hoặc hạU-22 để đóngmốc.

---

## Lời dẫn ngắn để paste vào thread mới

```text
Tôi giao bạn thực hiện M6 — Full run và demo trên cả hai máy tại D:\University\Semester7\BigData\DoAn.
Hãy đọc đầy đủ requirements-review/M6_START_PROMPT.md, đọc nguồn được chỉ dẫn, rồi triển khai/kiểm chứng thật M6-T1–T4, không chỉ lập kế hoạch.
M0–M5 đã đóng; U-48 đủ review M5, không hỏi lại. U-15/U-22 yêu cầu hai FULL_RUN thật riêng trên hai máy; không lấy imported output hoặc TV1 gắn roleTV2 thay nghiệm thu.
Ngay khi bắt đầu tạo/cập nhật reports/M6_FULL_RUN_TWO_MACHINES_NOTES.md; làm tới đâu ghi quyết định/thông số/nguồn/run/config/hash/KPI/mẫu số/lệnh/versions/resources/lỗi/ảnh/evidence/review tới đó để dùng cho báo cáo. Cập nhật STATE/checklist/decisions theo bằng chứng.
Điều chưa rõ phải kiểm nguồn trước; nếu còn thiếu thông tin/lựa chọn quan trọng ảnh hưởng đúng-sai, hành vi, dữ liệu, bảo mật, kiến trúc, protocol/schema hoặc phạm vi, nêu tác động,2–3phương án/trade-off/đề nghị và chờ tôi chọn trước phần phụ thuộc; tiếp tục phần độc lập. Không tự cho rằng/tự chọn bừa, không hỏi lại quyết định đã chốt.
Giữ nguồn/freeze/protocol/config và READY cũ bất biến. Test đã tiếp xúc M5; M6 là tái lập, không tune theo score, không fit train+dev/toàn kỳ/test. Kiểm caller/guards/role/IDs trước dùng runner cũ; không reset namespace để qua guard.
Chỉ M6; bàn giao đạt hoặc checkpoint chưa đạt rồi dừng. Không tự mở M7/M8, commit/push hoặc nghiệm thu máyTV2/việc người thật nếu chưa có bằng chứng.
```
