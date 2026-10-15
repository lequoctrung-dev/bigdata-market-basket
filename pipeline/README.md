# Pipeline — mẫu M1 và tiền xử lý toàn nguồn M2

M2 dùng mã và namespace riêng; xem mục 6 cuối file, [bản ghi báo cáo](../reports/M2_DATA_PREPROCESSING_NOTES.md) và [checklist](../requirements-review/14_MILESTONE_CHECKLIST.md). Mục 1–5 dưới đây giữ hướng dẫn mẫu M1.

Chỉ prototype của **M1**, không chạy Online Retail II, không mở M2 hoặc dashboard đầy đủ M4. M0 giữ hợp đồng `m0-contract-v1`; MongoDB mẫu riêng `127.0.0.1:27018`, database `bigdata_m1_sample`, web chỉ loopback `127.0.0.1:8081`. **M1 đã đóng ngày 15/10/2026** theo receipt TV1 thật, ngoại lệ U-33 miễn receipt TV2 riêng và xác nhận demo/học/giải thích/review U-35, không còn điểm sửa. Full run hai máy tại M6 giữ nguyên; TV2 runtime chưa kiểm chứng. Process mẫu đã dừng sau demo, giữ dữ liệu. Các receipt ở `artifacts/m1/TV1` hoặc `TV2` bị loại khỏi Git.

## 1. Bộ phiên bản để thử và căn cứ

| Thành phần | Bản prototype | Căn cứ và giới hạn |
| --- | --- | --- |
| JDK | 17; máy hiện tại 17.0.12 | Spark 4.2/Boot 4.1 yêu cầu Java 17 phù hợp; không cài/nâng cấp JDK toàn máy. TV2 xác minh bản thực tế, không sao chép receipt TV1. |
| Python | 3.12–3.14 cho bộ dependency đã pin; TV1 3.14.6 | Spark hỗ trợ từ 3.10, nhưng NumPy 2.5.4 trong bộ thử này yêu cầu Python >=3.12 theo metadata thực tế. Dùng `.venv` riêng; TV2 báo bản hiện có nếu ngoài khoảng, không tự nâng Python toàn máy. |
| PySpark | 4.2.0 với extra `ml` (NumPy), Scala 2.13 | FP-Growth cần NumPy qua MLlib; không thêm pandas/Arrow/SciPy khi chưa dùng. Pin `requirements.txt`, bản phụ thuộc thực tế ghi receipt. Chạy `local[2]`, driver 512 MB cho mẫu, không coi đây là cấu hình full run cuối. |
| MongoDB Spark Connector | `org.mongodb.spark:mongo-spark-connector_2.13:11.1.0`, driver riêng 5.1.4 | Maven resolve/copy đúng năm JAR vào `tmp/connector`; local classpath trước khi JVM khởi động, không cần phân phối file bằng `addFile`. Read FAILFAST/schema tường minh; write append/replace/upsert `_id`, không overwrite/drop. Driver web vẫn do Boot quản lý, không trộn với driver Spark. |
| PyMongo | 4.18.3 | Dùng nhập nguồn mẫu, metadata/pointer; Spark connector thực sự đọc/ghi giỏ/luật/probe, không dùng PyMongo thay evidence connector. |
| MongoDB | Binary có sẵn trên máy; TV1 8.3.8 | Khởi động process riêng từ mongod hiện có, không cấu hình lại dịch vụ tại 27017. Cache WiredTiger 0,25 GiB chỉ cho mẫu. |
| Spring Boot | 4.1.1; Java target 17 | Dùng dependency Data MongoDB/driver do Boot quản lý. Spring MVC/Thymeleaf, không thêm auth hoặc Python HTTP service. |
| Maven | Portable 3.9.16 | Tải Apache và kiểm tra SHA-512; `tmp/tools` và cache `tmp/maven-repository`, không sửa PATH/config toàn máy. |

Nguồn tra cứu ngày 14/10/2026: [Spark 4.2](https://spark.apache.org/docs/4.2.0/), [PySpark 4.2 metadata](https://pypi.org/project/pyspark/4.2.0/), [PyMongo](https://pypi.org/project/pymongo/), [MongoDB connector](https://www.mongodb.com/docs/spark-connector/current/getting-started/), [batch read](https://www.mongodb.com/docs/spark-connector/current/batch-mode/batch-read-config/), [batch write](https://www.mongodb.com/docs/spark-connector/current/batch-mode/batch-write-config/), [Boot requirements](https://docs.spring.io/spring-boot/system-requirements.html), [Boot properties](https://docs.spring.io/spring-boot/appendix/application-properties/index.html), [Maven download](https://maven.apache.org/download.cgi). Bộ này chỉ được gọi đã tương thích trên từng máy sau receipt runtime, không từ bảng phiên bản.

## 2. Chạy mẫu trên máy thực tế

Hướng dẫn dưới đây giữ để tái tạo trên TV1 hoặc chuẩn bị máy TV2. Theo U-33, chạy lại trên TV2 **không còn là điều kiện đóng M1**; không dùng ngoại lệ này thay full run hai máy M6.

Mở **PowerShell 7** tại thư mục gốc repository (TV1 đã quan sát 7.6.5). Windows PowerShell 5.1 trên TV1 chặn script do execution policy; chưa xác minh chạy helper dưới 5.1. Không tự đặt Bypass/đổi policy toàn máy; TV2 kiểm tra shell/quyền chạy trước, báo nếu thiếu để chọn setup phù hợp. Cần Java/JDK 17+, Python được hỗ trợ và `mongod` hiện có. Không copy `.venv`, MongoDB files hoặc receipt giữa laptop. Copy/clone source không thay chạy mẫu thật.

```powershell
# Đổi TV1 thành TV2 trên laptop thành viên còn lại.
.\scripts\invoke-m1.ps1 -Action Preflight -MachineRole TV1
.\scripts\invoke-m1.ps1 -Action Setup
.\scripts\invoke-m1.ps1 -Action Build
.\scripts\invoke-m1.ps1 -Action StartMongo
.\scripts\invoke-m1.ps1 -Action RunSample -MachineRole TV1
.\scripts\invoke-m1.ps1 -Action StartWeb
.\scripts\invoke-m1.ps1 -Action VerifyWeb -MachineRole TV1
.\scripts\invoke-m1.ps1 -Action Status
```

Nếu Python hoặc MongoDB chưa trên PATH, truyền đường dẫn executable thật vào `-PythonPath` cho Setup/Preflight hoặc `-MongoPath` cho StartMongo/Preflight. Không truyền mật khẩu/URI thật; prototype chỉ nhắm server mẫu riêng đã chọn. Mở web theo địa chỉ loopback trong receipt, thử giỏ và đọc bảng luật. Không chạy Spark trong HTTP request.

Kết thúc demo:

```powershell
.\scripts\invoke-m1.ps1 -Action StopWeb
.\scripts\invoke-m1.ps1 -Action StopMongo
.\scripts\invoke-m1.ps1 -Action Status
```

Launcher chỉ thao tác process trong receipt của workspace, đối chiếu PID/thời điểm/executable/hash/command line và listener. Không stop theo tên Java/mongod hoặc cổng đơn lẻ. MongoDB shutdown bình thường, giữ dữ liệu mẫu; không drop/reset/clean. Phải stop web trước Build để giữ JAR khớp receipt. Cần quyền đọc thông tin process trên máy; nếu không đọc được, báo lỗi thay vì bỏ guard.

Kết quả thành công dự kiến:

- `pipeline-receipt.json`: `status=PASS`, hash/code/run/config thật; Spark đọc MongoDB, xử lý mẫu, fit FP-Growth, ghi output và round-trip/công bố được kiểm tra.
- `web-receipt.json`: `status=PASS`, cùng run/version với batch; Java đọc ID/null/array/BigDecimal/ngày local; ranking Python/Java và form chạy thật.
- Receipt có bản riêng theo run/lần kiểm tra để giữ evidence khi chạy lại; tên ngắn ở trên là alias kết quả gần nhất, luôn đối chiếu run_id/version/status. Không lấy alias đã bị lượt sau thay đổi để gọi là evidence của lượt cũ.
- `environment.json` chỉ ghi môi trường, **không phải PASS luồng**. Build/test xanh không thay hai receipt trên, không thay demo/review người thật.
- TV2 gửi receipt của chính máy mình để review; không đưa receipt nguyên bản có đường dẫn cá nhân/secrets lên Git. Log lỗi cần trích phần lỗi và bước chạy, không gửi credentials.

## 3. Bài học M1-T1 và đáp án độc lập

### Driver, partition, transformation/action, shuffle, schema và window

- **Driver** là tiến trình điều phối SparkSession/job. Python điều khiển API qua JVM; web Java chạy riêng, đọc kết quả đã công bố. Dừng Spark sau batch không làm mất luật trong MongoDB.
- **Partition** chia dữ liệu để task xử lý. Mẫu đọc một partition rồi `repartition(2)` nhằm kiểm tra lựa chọn dòng đầu không phụ thuộc thứ tự đọc. Hai task local không có nghĩa cluster hai laptop.
- **Transformation** như select/filter/groupBy mô tả kế hoạch; **action** như count/collect/save mới kích hoạt tính toán. `explain` dùng xem kế hoạch, không tự chứng minh output đúng.
- **Shuffle** phân phối lại dữ liệu theo khóa, thường có ở repartition/groupBy/window; ảnh hưởng tài nguyên nhưng không cho phép đổi policy để làm nhanh. Mẫu ít dòng không đo được full-source performance.
- **Schema** tường minh giữ string ID/null/array/decimal text. Không suy BSON string tiền thành kiểu double hoặc tự dịch ngày local sang UTC.
- **Window** partition theo tuple nguồn, order theo sheet_index/source_row, row_number=1 chọn dòng đầu. `dropDuplicates` không bảo đảm giữ đúng vị trí đầu; Invoice/StockCode không phải khóa so trùng tám ô.

Hai thành viên đọc, giải thích cho nhau và đối chiếu ví dụ bên dưới. Agent chuẩn bị hướng dẫn không chứng minh thành viên đã học/hiểu; xác nhận này được theo dõi ở checklist M1, không tự tick M1-T1.

### Năm giỏ và công thức

Ký hiệu A/B/C trong toán học tương ứng StockCode `SKU_A/SKU_B/SKU_C`; mã nguồn thật `B` thuộc nhóm điều chỉnh vẫn bị loại, không thay mapping đã duyệt.

| Hóa đơn mẫu | Giỏ sau policy |
| --- | --- |
| 0001 | A, B, C |
| 0002 | A, B, C |
| 0003 | A, B |
| 0004 | A, C |
| 0005 | C |

N=5; frequency A=4, B=3, C=4, AB=3, AC=3, BC=2, ABC=2. Mẫu chọn minSupport=0,4, minConfidence=0,5 và K=3 **chỉ để kiểm tra cơ chế**. Không chốt các tham số Online Retail II/M3 hoặc tạo điểm/ngưỡng đạt mới.

- Support AB = 3/5 = 0,6.
- Confidence A→B = 3/4 = 0,75; lift = 0,75/(3/5) = 1,25.
- Confidence B→A = 3/3 = 1; lift = 1/(4/5) = 1,25.
- A→C có confidence 0,75, lift 0,9375; không tự đặt lift>1 làm bộ lọc.
- Query A: thứ tự B trước C vì confidence bằng nhau, B có lift cao hơn. Query A+B: chỉ C, căn cứ tốt nhất A→C có confidence 0,75; các luật AB→C và B→C có confidence 2/3 và không thắng luật tốt hơn. Nếu các chỉ số bằng nhau, dùng tiền đề chuẩn hóa để tie-break. Query A+B+C: không có gợi ý, không fallback.

Prototype đối chiếu đầy đủ tập/luật với enumeration độc lập từ năm giỏ, không chỉ ba ví dụ. Dữ liệu nguồn tự tạo có 22 dòng, hai lần lặp sau dòng đầu; giữ 20 dòng theo P-01, giữ dòng cùng Invoice/StockCode nhưng khác Quantity. POST/Manual/voucher/TEST/hủy/giá 0/số lượng âm chỉ dùng kiểm tra chính sách. Sau lọc có 12 dòng hàng, 5 giỏ, tổng Quantity=13; giá mỗi đơn vị 1,23456789 GBP, tổng chính xác 16,04938257 GBP. Đây là **đáp án fixture**, không counts dataset thật.

Tiền Spark dùng decimal mẫu `(20,8)` cho giá, `(10,0)` cho Quantity có kiểm tra miền, sản phẩm `(31,8)`; đối chiếu tổng exact, chưa kết luận scale/range toàn nguồn phù hợp. Đã tái hiện `(20,0) × (20,8)` khiến Spark giảm về `(38,6)` và mất chữ số; không đổi đáp án hoặc làm tròn trước tính tổng để vượt kiểm tra. Thời gian hóa đơn mẫu `2020-01-02T03:04:05` giữ local không offset; mốc hệ thống receipt riêng UTC. `customer_id=null`, empty array và ID `0001` cần giữ qua Python–Spark–BSON–Java.

## 4. Lỗi và ranh giới nghiệm thu

| Tình huống | Hành động |
| --- | --- |
| Port 27018/8081 đang dùng | Launcher dừng; kiểm tra process/receipt. Không kill process không thuộc dự án, không tự chuyển sang MongoDB đang dùng tại 27017. |
| DNS/tải PyPI/Maven Central hoặc checksum timeout | Báo bước/URL công khai; thử tải trong quyền mạng phù hợp. Không bỏ checksum/TLS hoặc đổi mirror không có căn cứ. |
| Python executable hoặc ensurepip lỗi | Kiểm tra đường dẫn/phiên bản và venv; không sửa PATH/registry/Python toàn máy để chữa prototype âm thầm. |
| Spark/Scala/connector không tương thích | Giữ error receipt, chẩn đoán lỗi/bản thật trước thay phiên bản hoặc môi trường. Không tải winutils/DLL không rõ nguồn hoặc tự chuyển WSL. |
| Batch FAILED hoặc output thiếu | Pointer current không đổi; web chỉ đọc READY đúng run/version. Không drop/reset dữ liệu; thử lại tạo run mới hoặc cùng nguồn immutable. |
| Form cũ, giỏ rỗng/mã lạ hoặc không có luật | Báo đúng tình huống, không trộn run, bỏ mã lạ âm thầm hoặc thêm fallback phổ biến. |

M1-AC1/AC2 nhận theo runtime mẫu TV1 thật; AC3 điều chỉnh theo U-33, miễn receipt TV2 riêng ở M1 và ghi rõ giới hạn. M1 DoD có bộ phiên bản đã thử, hướng dẫn tái tạo và giới hạn/lỗi công khai; M1-T1/review đã được người dùng xác nhận hoàn tất theo U-35. Receipt đóng M1 ở checklist 14. Full-source pipeline, scientific evaluation và full run nằm ở M2/M3/M5/M6; prototype này không được mở rộng thành các mốc đó khi chưa giao.

**Lỗi Windows đã quan sát:** dùng `spark.jars.packages` khiến startup gọi `addFile → Utils.fetchFile → FileUtil.chmod`, thiếu winutils. Prototype chuyển sang JAR chính thức đã resolve bằng Maven và `spark.driver.extraClassPath` trước launch của PySpark, giữ local[2] cùng JVM. Đây là cấu hình dependency local có căn cứ từ [Spark configuration](https://spark.apache.org/docs/4.2.0/configuration.html) và mã nguồn đúng bản [Utils.scala](https://github.com/apache/spark/blob/v4.2.0/core/src/main/scala/org/apache/spark/util/Utils.scala). Không sửa Spark/Hadoop để bỏ kiểm tra quyền; không khẳng định mọi thao tác filesystem/full source đều tránh được native dependency. Nếu còn lỗi native ở bước khác phải chẩn đoán, không gọi bản native hoàn chỉnh chỉ vì startup qua được.

## 5. Bài thực hành học/review M1

Hai thành viên có thể xem chung demo TV1; không cần tạo receipt TV2 theo U-33. Đây là hướng dẫn để thực hành, không ghi nhận hai thành viên đã thực hiện. Chưa cần sửa code, cài lại, Build hoặc RunSample nếu mẫu hiện có vẫn dùng được.

### Bước 1 — Xem luồng và hiểu trách nhiệm

```text
Nguồn mẫu trong MongoDB → batch PySpark → giỏ → FP-Growth → output MongoDB
                                                             ↓
                                      Spring MVC/Thymeleaf đọc và gợi ý
```

Batch đã chạy xong và Spark đã dừng. Web vẫn đọc được luật vì kết quả đã lưu trong MongoDB; bấm gợi ý chỉ áp luật lên giỏ. Driver điều phối job, partition là phần dữ liệu được giao cho task; `local[2]` không phải hai laptop hay hai máy chủ.

### Bước 2 — Mở web và đối chiếu bốn ca

Mở địa chỉ `http://127.0.0.1:8081/` trên máy TV1. Nếu process đã dừng, dùng StartMongo/StartWeb tại mục 2; khi mongod không trên PATH, truyền đường dẫn executable đã xác minh. Xác nhận nhãn SAMPLE, run/version và tổng mẫu `16.04938257` GBP. Tên có chữ `<script>` hiện như văn bản là dữ liệu kiểm tra escape.

| Thao tác trên form | Kết quả cần quan sát | Giải thích |
| --- | --- | --- |
| Chỉ chọn SKU_A | SKU_B trước SKU_C | Confidence cùng 0,75; lift B=1,25 cao hơn C=0,9375. |
| Chọn SKU_A và SKU_B | Chỉ SKU_C | B đã nằm trong giỏ nên không được gợi ý lại. C lấy luật tốt nhất theo confidence/lift/support. |
| Chọn cả A, B, C | Không có luật gợi ý | Không còn item ngoài giỏ; không thêm fallback phổ biến. |
| Bỏ chọn tất cả rồi gửi | Yêu cầu chọn ít nhất một sản phẩm | Giỏ rỗng khác tình huống giỏ hợp lệ nhưng không có luật. |

Ở bảng luật, tìm A→B và B→A. Dùng năm giỏ mục 3 để đếm: AB xuất hiện 3/5 giỏ nên support=0,6; A xuất hiện 4 giỏ nên confidence A→B=3/4=0,75; B xuất hiện 3 giỏ nên confidence B→A=3/3=1. Lift A→B=0,75/(3/5)=1,25: so tần suất B trong nhóm giỏ chứa A với tần suất B chung, không chứng minh quan hệ nhân quả hoặc chất lượng toàn nguồn.

### Bước 3 — Đọc các đoạn code cần giải thích

- Trong [sample_pipeline.py](sample_pipeline.py), tìm `read_spark`, `Window.partitionBy`, `repartition(2)`, `groupBy`, `FPGrowth` và `write_spark`. `filter/select` mô tả transformation; `count/collect/save` là action kích hoạt tính toán. Repartition/groupBy/window cần phân phối dữ liệu theo cách xử lý, tạo shuffle trong luồng mẫu.
- Giải thích P-01: partition theo tuple tám ô nguồn, sắp theo sheet rồi dòng, giữ row_number=1. Đổi thứ tự partition vẫn phải chọn đúng lineage đầu; cùng Invoice/StockCode nhưng khác Quantity vẫn là dòng khác.
- Schema phải giữ ID `0001` dưới dạng string, null và empty array; tiền lưu decimal text rồi tính bằng Spark decimal/Java BigDecimal. Tổng mẫu exact không chứng minh miền/scale của dataset thật phù hợp.
- Trong [SampleResults.java](../web/src/main/java/vn/edu/bigdata/m1/SampleResults.java), xem `snapshot()` đọc pointer một lần và lọc cùng run; trong [SampleController.java](../web/src/main/java/vn/edu/bigdata/m1/SampleController.java), xem `render()`; trong [RuleRanking.java](../web/src/main/java/vn/edu/bigdata/m1/RuleRanking.java), xem `recommend()`. Giải thích tiền đề phải đủ, bỏ item đã có, giữ luật tốt nhất cho từng ứng viên rồi xếp hạng; HTTP không fit lại Spark.

### Bước 4 — Review chéo và ghi kết quả thật

TV1 giải thích luồng Spark/P-01 và tính tay một luật cho TV2; TV2 giải thích luồng Java/pointer/ranking và một ca form cho TV1. Đổi vai để cả hai giải thích lại được. Đây là hướng dẫn review trong M1-T1 và vai trò đã chốt, không tạo bài thi hoặc ngưỡng điểm mới.

Sau khi thực hiện, báo ai đã học/giải thích/review, bốn ca có khớp hay không, còn câu hỏi hoặc điểm sửa nào. Chỉ xác nhận “Cả hai đã học, giải thích và review mẫu M1; bốn ca đúng; chấp thuận, không còn điểm sửa” nếu đó là kết quả thực tế. Nếu chưa hoàn tất, ghi phần còn thiếu; không cần screenshot để thay lời xác nhận. Agent sẽ đối chiếu rồi cập nhật checklist, không tự mở M2.

Kết thúc thực hành, dùng StopWeb rồi StopMongo tại mục 2 để dừng đúng process và giữ dữ liệu. Nếu không chạy được helper do shell/quyền, báo lỗi ở bước nào; không tự kill theo cổng/tên process hoặc đổi execution policy.

## 6. M2 — tiền xử lý toàn nguồn

Chỉ Online Retail II có hash cố định tại `data/raw/online-retail-ii/online_retail_II.xlsx`. U-37 chọn `127.0.0.1:27019`, database `bigdata_m2`, dbpath `artifacts/m2/mongo-data`. Bộ dependency bổ sung trong .venv: openpyxl 3.1.5, et-xmlfile 2.0.0, psutil 7.0.0. Setup M1 vẫn resolve đúng năm JAR local. Chạy PowerShell 7 từ root, với quyền đọc CIM/process và kết nối loopback. Nếu môi trường Codex chặn mạng/CIM, dùng cơ chế xin quyền công cụ. Import/batch/probe kiểm tra receipt process và file lock một writer.

```powershell
.\scripts\invoke-m2.ps1 -Action Preflight
.\scripts\invoke-m2.ps1 -Action StartMongo
# Tên thư mục audit phải mới; giữ evidence lượt trước.
.venv\Scripts\python.exe scripts/measure_m2.py --label audit .venv/Scripts/python.exe pipeline/m2_source.py audit --output artifacts/m2/audit-source-v1
.venv\Scripts\python.exe scripts/measure_m2.py --label import .venv/Scripts/python.exe pipeline/m2_source.py import
.venv\Scripts\python.exe scripts/measure_m2.py --label mongo-checks .venv/Scripts/python.exe pipeline/m2_verify_mongo.py
.venv\Scripts\python.exe -m unittest discover -s pipeline -p 'test_*.py' -v
.venv\Scripts\python.exe scripts/measure_m2.py --label spark .venv/Scripts/python.exe pipeline/m2_pipeline.py --audit artifacts/m2/audit-source-v1 --machine-role TV1
# Thay placeholder bằng run_id thực trong receipt PASS có storage encoding Int64.
.venv\Scripts\python.exe scripts/measure_m2.py --label final-checks .venv/Scripts/python.exe pipeline/m2_final_verify.py --run-id '<run_id>'
.\scripts\invoke-m2.ps1 -Action StopMongo
.\scripts\invoke-m2.ps1 -Action Status
```

Có thể audit trước StartMongo để tách số đo đĩa từng bước. Retry import cùng bytes/parser kiểm tra toàn bộ payload theo vị trí: READY không ghi bù hoặc sửa dữ liệu; WRITING chỉ thêm vị trí chưa có. Cùng khóa khác payload dừng. Nguồn thiếu vẫn WRITING, bị chặn trước Spark. Probe thực `m2_verify_mongo.py` giữ dataset `SYNTHETIC_IMPORT_TEST` với hai dòng riêng cho partial/retry/conflict; không trộn source hash thật hoặc xóa evidence. Probe source retry dùng 2.000 dòng thật, không gọi đó là full retry 1.067.371 dòng.

Audit đọc lại XLSX, dùng SQLite độc lập để so trùng/đếm/tiền/giỏ. Batch đọc MongoDB FAILFAST/schema tường minh; window giữ dòng đầu qua hai cấu hình 8/13 partition, lần hai đảo chiều đọc DB. Checksum lineage toàn bộ tập giữ lại là tổng bốn limb uint64 của SHA-256 `sheet:row`, kèm count; checksum có phiên bản, không phải chứng minh toán học không thể va chạm. Checksum giỏ dùng SHA-256 canonical `[invoice,items,min_local_time,line_count]` sort Invoice; đối chiếu mọi item/month/số tiền với audit.

Precision/scale lấy từ miền toàn nguồn đã audit; kiểm schema product/sum, bật ANSI và `allowPrecisionLoss=false`, đối chiếu tổng exact. Hóa đơn local parse TimestampNTZ. P-02 mapping có version/hash; danh tính mã giữ case, trim ngoài sau P-01. Counts lỗi chồng nhau tách khỏi số loại stage tuần tự. `storage_encoding_version=m2-bson-counts-int64-v1` tham gia hash basket set; số nguyên được ghi BSON Int64 tường minh và kiểm `$type` thật. Các basket set thử trước encoding này giữ nguyên, không được chọn chỉ vì có output.

Đầu ra ngoài Git: `data/processed/m2/<basket_set_id>/<run_id>/retained-lines.jsonl` giữ dòng P-01, Quantity/Price/line_value decimal text, flags và source_id/sheet/row; `artifacts/m2/` giữ audit/receipt/log/RSS samples và Mongo files. MongoDB `baskets` có tập item/min thời gian/line count/quality flags; `summaries` giữ thống kê hàng hóa toàn kỳ và audit mẫu số riêng. Dataset READY chỉ nói nguồn nhập đủ. `runs.status=VALIDATED`, `basket_set_status=READY` chỉ là checkpoint tiền xử lý; không tạo run READY phục vụ web, catalog train, itemsets/rules, metrics hoặc active publication. Không dùng summaries toàn kỳ làm baseline/catalog train M3.

Mỗi lượt đo lưu UTC, wall seconds, code revision/hash chưa commit, package/config và RSS theo giây. JVM riêng với Python/launcher và Mongo; RSS gồm shared pages, peak sampled không phải exact high-water mark/heap config. Byte đĩa trước/sau artifacts/processed gồm output các bước đang chạy đồng thời; scratch Spark ở `tmp/m2-spark/<run_id>` phải báo riêng. Không tự cleanup dữ liệu để làm đẹp phép đo.

Tổng hợp RSS từng bước bằng `scripts/summarize_m2.py --receipt artifacts/m2/pipeline-<run_id>.json --measurement artifacts/m2/<label>-<timestamp>.json`. Script ghép timestamp UTC của step với samples, ghi resource summary kèm status gốc; lượt FAIL vẫn giữ FAIL. Final checks đọc lại BSON/manifest/file/hash, có thể đánh dấu checkpoint cũ VALIDATED thành FAILED nếu phát hiện count int32; giữ manifest/receipt/output cũ để truy vết, không sửa run READY/đã công bố.

TV2 review kết quả cụ thể: nguồn/hash/lineage; counts/TEST; dòng thiếu khách; mã chữ/trim; giỏ một item/lớn; hóa đơn tính tay; tháng/tiền và hướng dẫn tái tạo. Agent không thay review TV2. Chỉ làm M2; full run/demo hai máy M6 giữ nguyên.
