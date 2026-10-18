# Trạng thái dự án

Cập nhật: **19/10/2026** (chuẩn bị bàn giao M6; M5 giữ đã đóng theo kỹ thuật TV1/U-48, không runtime mới). Đây là trạng thái điều phối; chỉ tick milestone theo tiêu chí và evidence trong [checklist](requirements-review/14_MILESTONE_CHECKLIST.md).

## Phạm vi giao việc hiện tại

**M5 đã đóng ngày18/10/2026**: T1–T4/AC1–AC3 đạt kỹ thuật TV1; **U-48 xác nhận cả hai review run/metrics/lỗi, TV2 tính lại mẫu và chấp thuận không còn điểm sửa**, đủ DoD. [M5 notes](reports/M5_INTEGRATION_FINAL_EVALUATION_NOTES.md) giữ ghi chép đồng thời, lỗi/ảnh/resources/evidence `artifacts/m5/`. U-47 hai run: DEVELOPMENT `8cef7ef5-6731-47b1-bcd7-bd908cfad7b2` source→Mongo train→Spark→web trước, FINAL **`04c940db-313d-4a05-a039-90163e33f070`/publication version3**, model/config/checksums đúng freeze. Test đầu15:05:29.761348UTC18/10;5.572giỏ=389single+5.183query; luật451/5.183hit(8,7015%),4.214/5.183có gợi ý(81,3043%),baseline91/5.183(1,7557%)/coverage100%.21Python/11Java,108HTTPdev/118HTTPfinal,crash/retry/CAS/80transitionGET,14browserchecks/10ảnh đạt; không tune sau test. Web8081/Mongo27019 giữ chạy để demo, lifecycle M5/M2; xem guide. **Dừng M5**, không mở M6/M7/M8, nghiệm thu máyTV2, commit/push.

Theo **U-49**, đã kiểm lại AC/DoD/review U-48 và hash artifact/mã chốt M5: không còn lựa chọn/confirm riêng để hoàn thành M5. Đã soạn [prompt M6](requirements-review/M6_START_PROMPT.md) cho thread mới, giữ hai FULL_RUN thật/từng người thao tác và giải thích, hỏi trước quyết định quan trọng, ghi notes đồng thời. Phiên19/10 chỉ đọc nguồn/artifact/Git và viết hồ sơ; không đọc process/DB/web sống, chạy test/batch, đổi publication, tạo notes/runtime M6 hoặc commit/push. Snapshot PID/version3 ngày18/10 không phải trạng thái sống19/10; mã còn ID/role/guard cần xử lý trong M6, không coi runner M5 là portable hai máy.

### Snapshot bàn giao M4 — lịch sử trước khi thực hiện M5

**M4 — Website phân tích và gợi ý theo giỏ đã đóng ngày16/10/2026**: M4-T1–T4/AC1–AC3 đạt kỹ thuật TV1, **TV1 đã kiểm UI/đối chiếu và chấp thuận không còn điểm sửa theo U-44**, đủ DoD. M0–M3 giữ đã đóng/U-41. Run DEVELOPMENT freeze `7bc55ac7-0d24-4ddd-a9b0-3b25d247b596`, publication version1; web ba khu vực đọc Mongo27019/`bigdata_m2`, loopback8081. [M4 notes](reports/M4_WEB_APPLICATION_NOTES.md) ghi quyết định/KPI/scope/lệnh/kiểm chứng/lỗi/ảnh/tài nguyên; [hướng dẫn demo](web/README.md) có đáp án. Final NOT_RUN; bàn giao rồi dừng, không refit/tune/M5/M6/commit/push hoặc suy review thành runtimeTV2.

## Những gì đã có và đã kiểm tra

- Theo U-45 đã kiểm lại hồ sơ AC/DoD/U-44, freeze/hash và mã M4 so với receipt: không còn confirm/lựa chọn riêng cần bổ sung để đóng M4. Đã tạo [prompt M5](requirements-review/M5_START_PROMPT.md) cho thread mới, có yêu cầu ghi notes đồng thời và hỏi trước quyết định quan trọng. Phiên18/10 chỉ chuẩn bị tài liệu; không đọc DB/process sống, chạy test/model/final, đổi pointer/lifecycle hoặc commit/push. Snapshot process16/10 không phải trạng thái hiện tại.

- Hồ sơ `requirements-review/01–15`, bản trích nguồn và audit dữ liệu đã có trước bước chuẩn bị. File 11/12 được bổ sung M0, lựa chọn U-27–U-29 và review hai thành viên theo xác nhận U-30; contract m0-contract-v1 đã nghiệm thu về tài liệu ở M0 và kiểm chứng mẫu TV1 ở M1; chưa nghiệm thu toàn nguồn/hai máy.
- Git `2.52.0.windows.1`, nhánh `main`; HEAD khi bắt đầu M1 là `3a834d5` — `finalize M0 scope and data contract`, sau commit chuẩn bị `760cf88`. Remote origin giữ như README. Đây là quan sát Git cục bộ, không xác nhận GitHub; Agent không commit/push trong M0/M1.
- Bước chuẩn bị đã thêm README, AGENTS, STATE, `.gitignore`, `.gitattributes` và các vị trí cho sản phẩm/công cụ/báo cáo. Mã prototype `pipeline/` và `web/` được thêm trong M1, không phải bước chuẩn bị hoặc M0.
- Đã kiểm tra loại dataset/output/build/môi trường/secrets khỏi Git; hồ sơ yêu cầu và file Word nguồn vẫn được Git nhận diện. Kiểm tra này không xác nhận mọi file tương lai đều không chứa bí mật.
- Đã đối chiếu SHA-256 sau chuẩn bị: hai Word nguồn, XLSX/ZIP nguồn, RTM, Source Audit và Source Extract không đổi.
- Các liên kết tài liệu chuẩn bị trỏ đến file hiện có; không lấy cấu trúc thư mục hoặc Git init làm minh chứng hệ thống chạy.
- M0: đã đối chiếu scope/U/RTM/report/deliverables/map và audit có sẵn; file 11 bổ sung bài toán/mục tiêu/giá trị, tập dữ liệu, mapping loại TEST và công thức KPI; file 12 bổ sung input/output/kiểu/khóa/manifest/công bố/retry/lỗi và các giả định M1. File 13 giữ phân công/khung ghi việc thật và kết quả M0; checklist 14 đã ghi receipt và tick AC/DoD theo U-30.
- Kiểm tra tài liệu là evidence của Agent, không phải review của TV1/TV2, Spark runtime hoặc full run. Không tái khảo sát toàn nguồn, cài stack, tạo DB/index hay viết ứng dụng trong M0.
- M1: có fixture/đáp án/PySpark tại `pipeline/`, MVC/Thymeleaf tại `web/`, launcher/HTTP checks tại `scripts/`; [hướng dẫn và kiến thức M1](pipeline/README.md). NumPy/decimal/native Windows được chẩn đoán bằng lỗi thực tế trước sửa; không đổi test expectation hoặc tải winutils/DLL không rõ nguồn.
- TV1 mẫu: 7 checks batch + 18 checks web đạt; 4 Python tests + 4 Java tests đạt. Run cuối `1b156c53-7c15-4a9e-a479-32b7ab3926f5`, publication version 3; 22 dòng tự tạo → 20 giữ P-01 → 12 dòng hàng → 5 giỏ, 7 tập phổ biến/9 luật. Không phải counts Online Retail II hoặc final evaluation.
- Evidence cục bộ `artifacts/m1/TV1/`: `environment.json`, `pipeline-receipt-1b156c53-7c15-4a9e-a479-32b7ab3926f5.json`, `web-receipt-8c0dff59-4d3e-404a-b084-073342db4532.json`, `lifecycle-receipt.json`. Runtime output bị loại khỏi Git; checklist 14 giữ kết luận/giới hạn, không dùng alias receipt của lượt mới thay evidence lượt cũ.
- Đã shutdown MongoDB mẫu bình thường và stop web đúng receipt; 27018/8081 không còn listener, 27017 vẫn nghe. Không drop/reset nguồn/DB, không sửa PATH/phần mềm toàn máy, không commit/push.
- Cập nhật 15/10: mở lại đúng process mẫu qua launcher để người dùng thực hành. Web tại 127.0.0.1:8081, MongoDB mẫu 27018 đang chạy khi bàn giao; không chạy lại batch/build hoặc đổi dữ liệu. Java round-trip và bốn ca form đã đọc/POST HTTP đúng cùng run/version 3; receipt `artifacts/m1/TV1/demo-ready-2026-10-15.json`. Lịch sử stop ngày 14/10 phía trên không mô tả trạng thái hiện tại. StopWeb/StopMongo theo guide khi thực hành xong.
- Kết thúc demo 15/10: người dùng xác nhận U-35; đã StopWeb và shutdown MongoDB mẫu đúng receipt. Kiểm tra ngoài sandbox xác nhận hai PID đã dừng, 27018/8081 không nghe, 27017 vẫn nghe và file WiredTiger còn; receipt `artifacts/m1/TV1/lifecycle-stop-2026-10-15.json` PASS. Đây là trạng thái hiện tại, thay snapshot đang chạy ở dòng trên; không drop/reset hoặc chạy lại batch/build.

## Trạng thái milestone

| Mốc | Trạng thái hiện tại |
| --- | --- |
| Chuẩn bị workspace/Agent, ngoài các milestone học thuật | Đã chuẩn bị và kiểm tra cục bộ; không thay M0 |
| M0 — Chốt phạm vi và hợp đồng dữ liệu | Đã đóng về tài liệu ngày 14/10/2026; AC1/AC2/AC3/DoD theo lựa chọn U-27–U-29, đối chiếu văn bản và review TV1/TV2 được người dùng xác nhận U-30 |
| M1 | Đóng 15/10/2026 theo AC/DoD điều chỉnh: mẫu TV1 PASS, ngoại lệ U-33, học/demo/review U-35; TV2 runtime chưa kiểm chứng |
| M2 | Đóng 15/10/2026: kỹ thuật TV1 PASS, AC1/AC2/AC3 và DoD đủ theo review U-38; run d7fb3f21-115f-4793-a5fe-5c40b6da64cd |
| M3 | Đóng 15/10/2026: split 29.335/4.609/5.572 không overlap; catalog 4.556 item train; run `7bc55ac7-0d24-4ddd-a9b0-3b25d247b596` có 1.349 itemsets/856 luật; freeze/postcheck/17 Python+6 Java tests đạt, review U-41 |
| M4 | Đóng16/10/2026: M4-T1–T4/AC1–AC3 đạt kỹ thuật TV1 (9Java/17Python/119HTTP/12browser checks,9ảnh); TV1 trực tiếp kiểm UI/đối chiếu, chấp thuận U-44 đủ DoD; DEVELOPMENT publication version1 |
| M5 | Đóng18/10/2026 theo kỹ thuật TV1/U-48; FINAL run04c940db…/version3, N5.183; freeze/READY cũ giữ, xem M5 notes |
| M6–M8 | Chưa thực hiện; không tự mở mốc tiếp theo hoặc suy TV1/review thành runtimeTV2 |

## Quyết định và giới hạn hiện tại

- Stack/dataset/giỏ/Thymeleaf/P-01–P-03, loại TEST, batch/MongoDB, roles, full run hai máy và khung báo cáo đã chốt: [U-01–U-26](requirements-review/07_CONFIRMED_SCOPE.md).
- Dataset và cấu trúc báo cáo được GV chấp thuận **theo xác nhận người dùng**; không phải Agent đã đọc thông báo độc lập.
- **M0-D1/D2/D3 đã chọn — U-27–U-29** ở [file 07](requirements-review/07_CONFIRMED_SCOPE.md): chín collection/run bất biến/con trỏ active/version; decimal text tại MongoDB; dashboard hàng hóa + audit toàn nguồn/gói KPI/ba khu vực. Review toàn contract đã được người dùng xác nhận cho cả TV1/TV2 theo U-30; không phải runtime PASS hoặc thông báo trực tiếp riêng từ TV2.
- Thông tin U-24 của hai máy vẫn là Windows 11/RAM 16 GB/50 GB trống theo người dùng. M1 TV1 đã đọc thật: Windows 11 x64, i5-13500H, RAM 15,63 GiB; ổ D trống khoảng 127 GiB lúc kiểm tra. RAM trống khoảng 2,6–2,7 GiB chỉ tại các snapshot đó, không kết luận đủ full run. Máy TV2 chưa kiểm tra.
- TV1 đã thử: JDK 17.0.12, Python 3.14.6, PySpark 4.2.0/Scala 2.13.18, connector 11.1.0/driver 5.1.4, PyMongo 4.18.3/NumPy 2.5.4, MongoDB 8.3.8, Maven portable 3.9.16, Boot 4.1.1/Data MongoDB 5.1.1/driver web 5.8.1. `.venv` và dependency/cache riêng dự án; chỉ mẫu TV1 được kiểm chứng. Helper chạy PowerShell 7.6.5 của môi trường Codex; Windows PowerShell 5.1 bị execution policy chặn, không đổi policy để vượt.
- Deadline, giờ/tuần, lịch bận và quy cách nộp chi tiết chưa rõ. Không hỏi lại khi chưa có thông tin mới; không cam kết đủ thời gian.
- Raw source giữ nguyên; count audit cũ trước quyết định loại TEST không phải số liệu pipeline mới. Không biến audit Python thành Spark PASS.
- Git đã có lịch sử cục bộ và remote; không suy trạng thái hiện tại trên GitHub chỉ từ cấu hình remote. Thread mới kiểm tra lại branch/status/diff/log; không tự commit/push.
- Chưa chuẩn bị/kiểm chứng workspace hoặc Git trên laptop thứ hai; không suy trạng thái máy này sang máy kia.

## Ranh giới bàn giao và việc kế tiếp

### Chuẩn bị thread M6 — 19/10/2026, U-49

M5 đã đủ AC/DoD/U-48, không hỏi lại review. Thread mới đọc đầy đủ [M6 Start Prompt](requirements-review/M6_START_PROMPT.md), triển khai M6-T1–T4 khi được giao; khi bắt đầu ghi `reports/M6_FULL_RUN_TWO_MACHINES_NOTES.md`, evidence role riêng `artifacts/m6/TV1/`/`TV2/` theo máy/thao tác thật. U-22 không miễn máyTV2; không suy imported output/lượt Agent hoặc TV1 thành FULL_RUN/human demo cả hai máy. Chưa truy cập máyTV2 thì làm phần độc lập và checkpoint, không tự hạ AC3. Test đã tiếp xúc M5, chỉ tái lập đúng freeze; giữ nguồn/READY cũ. Phiên chuẩn bị không thực hiện M6; bàn giao rồi dừng, không M7/M8/commit/push.

### Bàn giao M5 — 18/10/2026, U-46–U-48

M5 đủ AC/DoD; review thật theo người dùng U-48, receipt riêng `artifacts/m5/review-20261018.json`, không sửa receipt runtimePENDING. Đọc [M5 notes](reports/M5_INTEGRATION_FINAL_EVALUATION_NOTES.md) và [Web Guide M5](web/README.md). FINAL/version3 tại127.0.0.1:8081, webPID14344/MongoPID13768 có receipts M5/M2, Spark/browser đã dừng; giữ demo/data/evidence. StopWeb bằng invoke-m5; StopMongo bằng invoke-m2 khi kết thúc demo. Giữ nguyên source/M2/M3/freeze/protocol/config/các READY cũ. Final test đã tiếp xúc; tái kiểm là replay/replication, không test độc lập mới. Không commit/push hoặc tự mở M6/M7/M8/hai máy.

### Chuẩn bị thread M5 — 18/10/2026, U-45 (lịch sử trước triển khai)

M0–M4 đã đóng; review U-41/U-44 đủ, không hỏi lại. Đọc đầy đủ [M5 Start Prompt](requirements-review/M5_START_PROMPT.md), sau đó triển khai M5-T1–T4 khi được giao trong thread mới. M5 gồm end-to-end thật/publication-retry/final evaluation sau freeze/regression; không tự mở M6. Khi M5 bắt đầu tạo `reports/M5_INTEGRATION_FINAL_EVALUATION_NOTES.md`, ghi quyết định/thông số/KPI/mẫu số/run/hash/resources/lỗi/evidence/review ngay lúc làm. Điểm quan trọng chưa rõ sau kiểm nguồn phải trình2–3phương án/trade-off/đề nghị và chờ trước phần phụ thuộc. Phiên soạn prompt không thực hiện M5 và không mở test cuối; final vẫn NOT_RUN theo receipts đã đọc.

### Bàn giao M4 — 16/10/2026

- Đọc [hướng dẫn M4](web/README.md) mục “Gói TV1 kiểm tra trực tiếp UI” và [M4 notes](reports/M4_WEB_APPLICATION_NOTES.md); mở `http://127.0.0.1:8081`. Run/version hiện ở đầu mỗi trang, provenance đầy đủ trong khối nguồn.
- Giữ run/config/protocol/source/basket-set M2/M3 và freeze. Dashboard toàn kỳ39.516/4.895 khác train29.335/4.556; luật1.349 itemsets/856rules, K5. Dev4.293 query và final NOT_RUN, không dùng summaries toàn kỳ làm catalog/baseline train.
- Mongo27019/PID26740 đã có sẵn, giữ nguyên. Web M4 có receipt riêng `artifacts/m4/web-process.json`, JAR copy theo SHA256; xem Status/StopWeb bằng `scripts/invoke-m4.ps1`, không dùng lifecycle M1 để dừng M4. Chrome headless kiểm ảnh đã đóng đúng process riêng.
- DoD đã đủ theo U-44; receipt review riêng tại artifacts/m4/review-20261016.json. Dừng tại M4; không tự mở M5/M6 hoặc suy PASS TV1 thành nghiệm thu hai máy.

### Lịch sử bàn giao M3 — 15/10/2026

- Run chọn **`7bc55ac7-0d24-4ddd-a9b0-3b25d247b596`**, DEVELOPMENT READY chưa publication. Train 29.335 gồm 2.503 giỏ một item; dev 4.609 gồm 316 giỏ một item và 4.293 query; test 5.572 chỉ metadata invoice/time, **NOT_RUN**. Catalog/tên/baseline từ 717.574 dòng merchandise train, không dùng summaries toàn kỳ.
- K=5/seed=20261015/mask SHA-256/ranking Unicode, minSupport=.01/minConfidence=.3/8 partitions/local[2]/heap 768m/stack 4m. Luật hit 505/4.293 (Recall 11,7633%), có gợi ý 3.513/4.293 (81,8309%); baseline 109/4.293 (2,5390%), có gợi ý 100%. Giữ 265 target mới và 780 query không có ứng viên luật trong mẫu số.
- Freeze `artifacts/m3/freeze-1a1f2ec6-331e-4b02-9aaf-18804793d4e9/freeze.json`, SHA256 `f7ee9c13432f0c99e7e5bcbf0363eed77eb4d5493b39e78fbb2e8e48557d053a`. Postcheck replay mọi prediction/metric, source/M2/keys/checksum/BSON đạt; Java khớp cả4.293 query và luật tốt nhất. TV2 review thật theo người dùngU-41, không suy runtime máy kia.
- Có3 lượt PASS/2 lượt FAIL (guard RAM và StackOverflow) giữ evidence, không sửa receipt/freeze PENDING_TV2; review receipt riêng. Selected wall147,752giây, sampled peakRSS Python303,87/JVM1.090,08/Mongo101,37/combined1.381,59MiB; không gọi config/availableRAM là usage.
- [Guide mục7](pipeline/README.md#7-m3--fp-growth-baseline-và-development) hướng dẫn tái tạo; [checklist M3](requirements-review/14_MILESTONE_CHECKLIST.md) giữ receipt đóng. **Dừng trước M4/M5**, final/web thật/hai máy chưa nghiệm thu; không commit/push/reset/drop/cleanup. Mongo27019 có sẵn đầu phiên được giữ chạy đúng receipt, không động dịch vụ27017/mẫuM1.

### Lịch sử bàn giao M2 — giữ nguyên để truy vết

1. M2 thật: 1.067.371 raw → 1.033.036 P-01 → 1.007.913 positive_valid → 1.003.357 merchandise; 39.516 giỏ/4.895 item/5.347 summaries, giữ 226.761 dòng hàng thiếu khách. GBP exact 19.643.861,637. Kiểm lineage đảo thứ tự/partition, audit độc lập, partial/retry/conflict, precision và BSON Int64 đạt.
2. Run cuối `d7fb3f21-115f-4793-a5fe-5c40b6da64cd`, basket set `cae0d9e763ef38a086966d829fdeba9272f4d7fda7b61791bee9e9ba04b3287a`; run VALIDATED/basket set READY chỉ cho tiền xử lý, không có model/catalog/metrics/publication. Hai run thử trước giữ nguyên evidence, checkpoint int32 đã bị postcheck đánh dấu FAILED. 10 Python tests đạt; wall Spark cuối 301,032 giây, sampled RSS combined 2.272,68 MiB, JVM đo riêng.
3. TV2 đã review kết quả/schema/lineage/mapping/giỏ/tiền/hóa đơn mẫu và tái tạo, chấp thuận không còn điểm sửa theo người dùng U-38. M2 đủ AC/DoD và đã tick; xác nhận không phải runtime TV2. Dừng, không tự mở M3/M4, commit/push hoặc reset/drop/cleanup dữ liệu.
4. Full run cả hai máy M6/U-15/U-22 giữ nguyên; M2 TV1 không thay M6, runtime máy TV2 hoặc web thật. Full READY import lại cả workbook chưa chạy; retry thật đã thử 2.000 dòng và partial fixture riêng. Dataset/nguồn/receipt/output giữ lại; lifecycle cuối ghi theo receipt trong M2 notes/checklist.

Lifecycle cuối M2: MongoDB 27019 đã shutdown đúng process receipt, dữ liệu giữ; `artifacts/m2/stop-20261015T084344.json` STOPPED/listener 0. Preflight cuối chỉ 27017/PID 5572 nghe, 27018/27019/8081 đóng. Không commit/push/reset/drop hoặc tự mở milestone sau.

Task/AC/DoD: [M2 trong Master Plan](requirements-review/13_MASTER_IMPLEMENTATION_PLAN.md). Tiến độ/receipt: [Milestone Checklist](requirements-review/14_MILESTONE_CHECKLIST.md).

Theo **U-39**, đã soạn [prompt tiếp nối M3](requirements-review/M3_START_PROMPT.md) cho thread mới cùng project. M2 không còn confirm/demo riêng cần bổ sung; runtime/postcheck và review U-38 đã đủ AC/DoD. Phiên soạn prompt chỉ đọc/viết hồ sơ, không mở M3, chạy lại job hoặc thay DB. Khi thực hiện M3 phải ghi đồng thời thông tin phục vụ báo cáo tại `reports/M3_MODEL_DEVELOPMENT_NOTES.md`, gắn source/basket-set/run/protocol/config/metrics/tài nguyên/lỗi/evidence và review thật; file này được tạo khi M3 bắt đầu, không phải evidence M3 đã chạy.

### Chuẩn bị thread M4 — 16/10/2026, U-42

M3 không còn lựa chọn/xác nhận thiếu để đóng; U-41 đã đủ review DoD. Đã tạo `requirements-review/M4_START_PROMPT.md` với snapshot Git/IDs/hash đã đọc lại, phạm vi M4-T1–T4/AC/DoD, ba khu vực UI, giới hạn train/toàn kỳ/development/final, publication tối thiểu theo U-27, đọc schema thật thay hard-code M1, lifecycle và hướng dẫn kiểm chứng. Thread M4 phải hỏi bằng phương án/trade-off khi thông tin quan trọng vẫn chưa rõ sau kiểm nguồn, đồng thời ghi vào `reports/M4_WEB_APPLICATION_NOTES.md` từ lúc bắt đầu. Chưa tạo notes M4 hoặc code/runtime/ảnh/nghiệm thu M4. Chỉ chuẩn bị bàn giao; dừng trước triển khai M4/M5, không commit/push.
