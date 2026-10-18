# Website — phân tích và gợi ý theo giỏ

Đọc [STATE](../STATE.md), [M5 notes](../reports/M5_INTEGRATION_FINAL_EVALUATION_NOTES.md), [checklist](../requirements-review/14_MILESTONE_CHECKLIST.md) trước thao tác. Hiện phục vụ **FINAL, run `04c940db-313d-4a05-a039-90163e33f070`, publication version3**. **M0–M5 đã đóng**, M5 đạt kỹ thuật và cả hai review/TV2 tính lại mẫu/chấp thuận không còn sửa theo U-48. Spring Boot4.1.1/JDK17/MVC/Thymeleaf/MongoDB, batch Spark riêng. M6/hai máy chưa nghiệm thu.

## M5 — mở, kiểm và dừng demo hiện tại

Mở [Tổng quan](http://127.0.0.1:8081/), [Luật và FINAL](http://127.0.0.1:8081/patterns), [Giỏ](http://127.0.0.1:8081/basket). Mỗi trang có run/version và scope. Tổng quan toàn kỳ39.516giỏ/4.895item/GBP19643861.64; mô hình chỉ train29.335giỏ/catalog4.556/1.349itemsets/856rules. Test5.572=389single+5.183query. FINAL luật451/5.183hit,4.214/5.183có gợi ý; baseline91/5.183hit,5.183/5.183có gợi ý. Xem **Gói review M5** trong notes để TV2 tự tính mẫu10query: luật1hit/7nonempty,baseline0hit/10nonempty. Mỗi người review run/metrics/lỗi trước đóng M5.

```powershell
./scripts/invoke-m2.ps1 -Action Status
./scripts/invoke-m5.ps1 -Action Status
# Nếu process dự án thực sự đã dừng/port trống:
# ./scripts/invoke-m2.ps1 -Action StartMongo
# ./scripts/invoke-m5.ps1 -Action StartWeb
.venv/Scripts/python.exe -X utf8 scripts/verify_m5.py --previous-run 8cef7ef5-6731-47b1-bcd7-bd908cfad7b2 --previous-version 2
node scripts/m5_browser.mjs artifacts/m5/04c940db-313d-4a05-a039-90163e33f070
# Khi kết thúc review/demo: stop đúng process receipt, giữ dữ liệu
./scripts/invoke-m5.ps1 -Action StopWeb
./scripts/invoke-m2.ps1 -Action StopMongo
```

Nếu sandbox che process/loopback/CIM, xin quyền công cụ; không suy process đã dừng hoặc kill theo tên/cổng. M5 dùng `artifacts/m5/web-process.json`, JAR copy/hash; Mongo vẫn lifecycle `artifacts/m2/mongo-process.json`/27019/dbpath cũ. Không dùng receipt M4 để stop M5. Config `app.mode=DEVELOPMENT` giữ chọn nhóm controller phân tích tương thích M4; **nhãn và validation evaluation_stage DEVELOPMENT/FINAL lấy manifest**, không phụ thuộc tên JAR/mode. SAMPLE riêng khi chỉ định tường minh.

## M5 — tái tạo có kiểm soát từ nguồn đến web

Nguồn và tiền xử lý: [Pipeline Guide mục6–7](../pipeline/README.md), XLSX Online Retail II/hash `bcbe73b3…df2e980`, M2 run/basket-set và preparation/freeze ghi đầy đủ trong notes. **Trên namespace đã có M3/M4, dùng kiểm theo stage; không chạy m2_pipeline/m2_final_verify có guard/mutation giai đoạn cũ**. M5 hiện dùng source Mongo READY và M2 preprocessing bất biến đã kiểm; không tuyên bố re-import/P-01/P-02 toàn workbook vừa chạy lại. Clone thiếu artifacts phải tái tạo prerequisite theo nguồn/guide, không dựng receipt hoặc import output thay full run M6. Không chạy grid hoặc freeze lại bằng test.

Lệnh dưới mô tả luồng đã chạy. Mỗi model/final UUID mới; thay `<...>` bằng ID/path thật từ output, đọc pointer sống trước CAS. **Test đã tiếp xúc ngày18/10 lúc15:05:29UTC**; tái chạy cùng test là replication, không test độc lập mới. Không tự chạy lại final vì score thấp.

```powershell
.venv/Scripts/python.exe -X utf8 scripts/m5_preflight.py
.venv/Scripts/python.exe -X utf8 scripts/measure_m5.py --label integrated-model .venv/Scripts/python.exe -X utf8 pipeline/m5_model.py
.venv/Scripts/python.exe -X utf8 scripts/m5_harness_check.py --run-id '<development_uuid>'
# Web phải chạy bằng JAR hỗ trợ M5; nếu cần build mới, StopWeb trước Build rồi StartWeb.
.venv/Scripts/python.exe -X utf8 scripts/m5_publish.py --run-id '<development_uuid>' --expected-run '<active_uuid>' --expected-version <active_version>
.venv/Scripts/python.exe -X utf8 scripts/verify_m5.py
# Chỉ sau gate HTTP PASS của chính development_uuid:
.venv/Scripts/python.exe -X utf8 scripts/measure_m5.py --label final-evaluation .venv/Scripts/python.exe -X utf8 pipeline/m5_evaluate.py --integrated-run '<development_uuid>' --e2e-receipt '<development_http_receipt>'
.venv/Scripts/python.exe -X utf8 scripts/m5_publish.py --run-id '<final_uuid>' --expected-run '<development_uuid>' --expected-version <development_version>
.venv/Scripts/python.exe -X utf8 scripts/verify_m5.py --previous-run '<development_uuid>' --previous-version <development_version>
```

Để thử crash/retry đúng M5-T2 thay lần publish DEVELOPMENT bằng `m5_failure_campaign.py --run-id '<development_uuid>'` (target phải là run mới chưa active): script giữ probes có provenance, không active fixture, crash chỉ child writer/publisher của nó. Sau đó verify HTTP để có gate. `m5_transition.py --run-id '<final_uuid>'` thay lần publish FINAL để kiểm concurrent pages/CAS/old-form và nhánh timeout **được tiêm sau write thật**; đây không phải server timeout tự phát. Không replay campaign trên run đang active để ép xanh. Không stop Mongo thật để dựng lỗi.

Recovery publisher: intent ghi trước CAS tại `artifacts/m5/publication-intent-*.json`; nếu process crash/kết quả ghi chưa rõ, chạy `m5_publish.py --recover '<intent_path>'` để đọc **APPLIED/NOT_APPLIED/CONFLICT**, không blind retry. CAS matched0 dừng đối chiếu. READY/run cũ giữ nguyên cho request đang chạy; lỗi READY về sau ghi incident riêng, không sửa receipt/output.

Offline test giữ context/target mới trong mẫu số; form web chỉ nhận catalog train nên query có mã ngoài catalog trả400. Không cắt/lọc query test rồi gọi đó là cùng phép đánh giá. Demo web sáu mã21080/21094/21467/21770/22704/22969→21086/21212 vẫn là **case development**, không gọi là final sample. Form version2 gửi lênFINAL/version3 trả409/yêu cầu tải lại.

Regression: Python21tests, Java11tests với cả `-Dm3.runDirectory=<development_folder>` và `-Dm5.runDirectory=<final_folder>`; giữ cache Maven cục bộ/offline như lệnh lịch sử dưới. `test` không thay JAR runtime đã pin; nếu sửa Java/template/static cần StopWeb→Build→StartWeb→HTTP/browser lại. Không nâng stack hoặc dùng output máy này nghiệm thu máyTV2.

## Lịch sử M4 — giữ để truy vết và tái tạo giai đoạn DEVELOPMENT

Phần dưới là hướng dẫn/đáp án M4 trên run7bc55ac7/version1. Active hiện tại đã chuyển FINAL/version3 theo M5; không dùng các lệnh publisher/verifier M4 làm kiểm trạng thái M5. U-44 đã đóng review M4, không yêu cầu làm lại.

## Mở và dừng

PowerShell7, từ root dự án. Không chạy batch M1/RunSample để dựng dữ liệu thật. Nếu Mongo27019 có sẵn thì giữ process; kiểm identity ngoài sandbox khi cần, không coi lỗi quyền là process đã dừng.

```powershell
./scripts/invoke-m2.ps1 -Action Status
# Chỉ khi Mongo dự án đã dừng và 27019 trống:
# ./scripts/invoke-m2.ps1 -Action StartMongo

# Chỉ khi thiếu active pointer; helper kiểm freeze/output rồi insert lần đầu.
# Pointer cùng run: read-only, không tăng version; pointer khác: dừng.
.venv/Scripts/python.exe scripts/m4_publish.py --publish

# Nếu web đang chạy, dừng đúng receipt trước khi build.
./scripts/invoke-m4.ps1 -Action StopWeb
./scripts/invoke-m4.ps1 -Action Build
./scripts/invoke-m4.ps1 -Action StartWeb
./scripts/invoke-m4.ps1 -Action Status
# Kết thúc demo:
./scripts/invoke-m4.ps1 -Action StopWeb
```

Website: [Tổng quan](http://127.0.0.1:8081/), [Luật/đánh giá](http://127.0.0.1:8081/patterns), [Giỏ](http://127.0.0.1:8081/basket). Receipt `artifacts/m4/web-process.json` pin JAR copy theo hash, executable/start/args, chỉ loopback8081/Mongo27019 `bigdata_m2`. Không stop Mongo đã chạy từ trước phiên nếu chưa được giao. Không stop theo tên/cổng hoặc reset/drop dữ liệu. Nếu nhận lỗi identity, đối chiếu receipt/process trước phần phụ thuộc.

M1 giữ riêng: launcher M1 truyền `app.mode=SAMPLE` và URI27018 tường minh, nhãn SAMPLE/endpoints mẫu chỉ bật trong mode đó. Không chạy cùng M4 trên8081. Artifact Maven vẫn tên `market-basket-m1-0.0.1-SNAPSHOT.jar` để giữ script/build cũ; tên JAR không quyết định chế độ dữ liệu.

## Gói TV1 kiểm tra trực tiếp UI — DoD M4

Run `7bc55ac7-0d24-4ddd-a9b0-3b25d247b596`, version1, DEVELOPMENT; source/hash/basket-set đầy đủ trong khối nguồn mỗi trang và notes. Ảnh dưới `artifacts/m4/` là Chrome thật trên run này, không là người dùng đã review.

1. Tổng quan: đọc 39.516 giỏ, 4.895 mã toàn kỳ, 3.208 giỏ một item. GBP hiển thị `19643861.64`, exact `19643861.637`, là giá trị mua dương hàng hóa. Mở bảng phân phối đủ426 cỡ (max1.108), audit quality; số lý do chồng nhau không cộng thành số loại. 25 tháng dùng min-time hóa đơn, timezone UNKNOWN. Ảnh `overview.png`, `overview-full.png`.
2. Luật/đánh giá: Ntrain29.335, catalog4.556; 1.349 tập/856 luật. Đổi bảng chọn Support hoặc Frequency hợp lệ cho itemsets; thử tìm mã/tên, size/support, trang trước/sau. Recall@5 luật505/4.293 =11,7633%; baseline109/4.293 =2,5390%. Có gợi ý3.513/4.293 =81,8309% và baseline100%; final **NOT_RUN**. Ảnh `patterns.png`, `itemsets.png`.
3. Giỏ: tìm từng mã `21080`, `21094`, `21467`, `21770`, `22704`, `22969`, tích checkbox. Tìm mã tiếp theo vẫn giữ lựa chọn. Nút “Chỉ xem lựa chọn” hiển thị sáu mã; gửi giỏ.
4. Kết quả cần đúng thứ tự `21086`, `21212`. Căn cứ tốt nhất `{21080,21094}→21086`, `{21080}→21212`. Đây là query dev Invoice558640 (targetẩn21086); không là test prediction. Ảnh `recommendation-real.png`.
5. Thử chỉ chọn `21080`, nhiều item và thêm `21086`: không trả item đã chọn; mỗi mã chỉ một kết quả. Thiếu21094 không áp **riêng luật** `{21080,21094}→21086`, nhưng có thể có luật khác gợi ý cùng mã; đối chiếu căn cứ thực tế, không kết luận chỉ từ consequent.
6. Bỏ chọn hết rồi gửi: báo chọn ít nhất một sản phẩm. Chọn mã không có luật (mã cụ thể/expected trong HTTP receipt mục samples `catalog_no_rule`): báo không có gợi ý, không baseline fallback. Ảnh `empty-basket.png`; stale-form fixture/probe và HTTP version0 chỉ dùng kiểm tra, không cần đổi pointer thật.
7. Review trực tiếp nội dung, thao tác, mã/tên/scope/mẫu số với notes/receipts. Báo **đã kiểm UI và đối chiếu, chấp thuận** hoặc mô tả điểm sửa. Chỉ xác nhận điều đã làm; Agent/browser automation không thay review TV1. M3/U-41 không cần review lại.

## Kiểm chứng tái chạy (không fit)

```powershell
.venv/Scripts/python.exe -m unittest discover -s pipeline -p 'test_*.py' -v
./tmp/tools/apache-maven-3.9.16/bin/mvn.cmd -o '-Dmaven.repo.local=D:/University/Semester7/BigData/DoAn/tmp/maven-repository' '-Dm3.runDirectory=D:/University/Semester7/BigData/DoAn/artifacts/m3/7bc55ac7-0d24-4ddd-a9b0-3b25d247b596' -f web/pom.xml verify
.venv/Scripts/python.exe scripts/verify_m4.py
node scripts/m4_browser.mjs
```

Sửa đường dẫn cache/run theo workspace nếu trên máy khác; phải có outputs riêng hợp lệ, không lấy imported output thay full run M6. Maven HTTP test cần loopback; script verifier cần quyền process/Mongo. Node24 dùng WebSocket tích hợp và Chrome tại đường dẫn ghi trong script, profile riêng/đóng browser; không yêu cầu cài Playwright. Script browser ghi ảnh receipt ngoài Git, tái chạy ghi đè ảnh tên dễ đọc nhưng giữ receipt theo UTC; gói nghiệm thu chốt hash ảnh để truy vết.

Schema/manifest/output0, Mongo unavailable và XSS được kiểm bằng fixture/probe trong `AnalysisWebTest` (HTTP Tomcat thật, service synthetic), không phá DB thật để dựng lỗi. Real HTTP đối chiếu KPI từng bucket, catalog và các trang model với DB/Python; Java parity kiểm toàn bộ4.293 prediction từ output M3. Các lớp này khác review người thật, final evaluation và full run hai máy.

## Input và tính nhất quán

Mỗi request giữ một run/version snapshot; link filter/trang/form mang runId/version. Form cũ trả409/yêu cầu tải lại, invalid400, nguồn/schema/manifest lỗi503; không lộ URI/stacktrace. Scalar fields không được lặp; browser chỉ gửi mã chuỗi, không object Mongo/JSON/SpEL. Search tối đa160 ký tự; input tối đa2×catalog entries, distinct vẫn nhận đủ mọi mã catalog; vượt giới hạn báo lỗi và giữ lựa chọn hợp lệ, không tự cắt. K lấy config freeze.

Mỗi trang25 hàng; sort allowlist/Unicode tie ổn định. Tên dùng `th:text`, JS chỉ đổi checkbox/hiển thị và textContent, không fit hoặc sửa dữ liệu. Không cache một phần: đọc outputs hoàn chỉnh theo run và summaries theo basket-set; service kiểm kiểu/count/keys/cross-reference/stage/metrics/tiền. Publication helper kiểm file/hash/logical checksum trước insert; không chọn “run mới nhất”.
