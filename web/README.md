# Website M4 — phân tích và gợi ý theo giỏ

Đọc [STATE](../STATE.md), [M4 notes](../reports/M4_WEB_APPLICATION_NOTES.md), [checklist M4](../requirements-review/14_MILESTONE_CHECKLIST.md) trước thao tác. Đây là website DEVELOPMENT, không phải kết quả test cuối/M6. Spring Boot 4.1.1, JDK17, Spring MVC/Thymeleaf/MongoDB; không có Python service hoặc Spark trong HTTP.

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
