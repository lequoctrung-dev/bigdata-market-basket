# M6 — Full run và demo trên hai máy

Ngày bắt đầu và đóng: **19/10/2026**. Phạm vi người dùng giao: M6-T1–T4; M0–M5 đã đóng, U-48 đủ review M5. **M6 đã đóng theo phạm vi điều chỉnh U-52 và review U-53**: full run thật máy hiện tại kỹ thuật PASS; người dùng xác nhận đã demo/giải thích/review và chấp thuận. TV2 là giả định tương đương do người dùng yêu cầu, không có số đo/full run độc lập máy đó. Nhật ký bên dưới giữ nguyên diễn biến theo thời điểm; mục nghiệm thu cuối file là kết quả mới nhất. Không M7/M8/commit/push.

## Khởi tạo và nguyên tắc

- Git đầu phiên: nhánh `main`, HEAD `4d1d254bae0dbcc555455a37029b03b709f9b885`; `git status --short` và `git diff --stat` rỗng. Snapshot HEAD trong prompt đã cũ; dùng HEAD thực tế này.
- Đã đọc prompt M6, README, STATE và AGENTS; tiếp tục đọc nguồn bắt buộc trước mutation/runtime.
- Giữ nguyên XLSX, freeze/protocol/config, các READY và lịch sử M2–M5. Test đã tiếp xúc ở M5; M6 chỉ tái lập, không tune/fit dev/test.
- Evidence mới: `artifacts/m6/TV1/`, `artifacts/m6/TV2/` ngoài Git. Role không chứng minh máy/người; Agent hỗ trợ kỹ thuật không thay thao tác/giải thích/review thật.
- Chưa start/stop/build/batch, ghi DB hoặc đổi publication; đang kiểm caller/guard/ID/ownership.

## Bằng chứng theo máy

| Nội dung | TV1 | TV2 |
| --- | --- | --- |
| Truy cập máy thực | Workspace hiện tại, identity Mongo/web đã kiểm ngoài sandbox | Theo U-52 giả định tương đương, không truy cập/đo |
| Môi trường/phiên bản/tài nguyên | Đã đo Windows/i5/RAM/disk/versions và RSS1s từng job, chi tiết dưới | ASSUMED_EQUIVALENT_BY_USER_NOT_MEASURED |
| Source/config/freeze/code hashes | PASS; source/freeze/config/32file core M5 giữ, mọi BSON DBM5 không đổi | Không đo riêng |
| Full import/preprocessing/fit/evaluation/publication | Full source mới→Spark→train→dev gate→FINAL replication READY/version2 PASS | ASSUMED_EQUIVALENT_BY_USER_NOT_MEASURED |
| KPI/tử số/mẫu số/logical checksums | FINAL luật451hit/4.214nonempty/N5.183; baseline91hit/5.183nonempty; parity/checksums exact | Không đo riêng |
| Lifecycle/HTTP/UI/ảnh | Mongo/web stop→start PASS;108HTTPdev/118final/118sau restart;16UIchecks/11ảnh | Không đo riêng |
| Thao tác/giải thích/review người thật | U-53: “Đã demo/giải thích/review; chấp thuận M6” theo người dùng, receipt riêng | Không gán TV2 đã thao tác/review độc lập |

## Tiến độ, lệnh và điểm cần xử lý — nhật ký lịch sử

1. Đọc nguồn: `Get-Content` prompt/AGENTS/README/STATE; kiểm `git status --short`, `git branch --show-current`, `git rev-parse HEAD`, `git diff --stat`. Không suy trạng thái process từ PID lịch sử.
2. Cần xác định luồng preprocessing mới không vi phạm guard namespace có M3–M5; quyết định namespace/ownership có ảnh hưởng lớn phải trình người dùng trước phần phụ thuộc.
3. Chưa có evidence máy TV2; giữ M6-T3/AC3 chưa đạt. Không tạo receipt thay máy đó.

### Quyết định vận hành mới và quan sát môi trường

- Người dùng chọn **A: database `bigdata_m6` trên Mongo loopback27019**. Giữ `bigdata_m2`/active M5; không reset/drop. Schema/chín collection và protocol giữ, output/run M6 mới; reference chỉ đối chiếu.
- Người dùng điều chỉnh yêu cầu TV2: coi máy TV2 tương đương 100% máy hiện tại và không cần tách/chờ runtime TV2. Áp dụng cho phạm vi kiểm chứng M6 theo chỉ dẫn mới; **TV2 là giả định do người dùng chấp thuận, không phải quan sát runtime, receipt hay số đo máy TV2**. Không tạo bản FULL_RUN giả cho TV2; không yêu cầu lại logs để chặn phần máy hiện tại. Phần người dùng demo/giải thích vẫn cần ghi đúng thao tác thật.
- `artifacts/m6/TV1/environment-initial.json`: 18/10/2026 19:47:46UTC (=19/10 02:47 giờ Việt Nam), Windows11Home10.0.26200/64-bit/i5-13500H, RAM16.786.550.784byte; available1.289.547.776byte, đĩa120.109.793.280byte. Đây là snapshot, không usage/peak.
- Sandbox từ chối CIM và che process làm launcher trả running=false; **không dùng kết quả đó kết luận process dừng**. Chạy lại ngoài sandbox có quyền: Mongo27019/PID13768 và web8081/PID14344 vẫn sống, identity/hash/start/args khớp receipts M2/M5;27017/PID5940 là dịch vụ ngoài scope. Chưa start/stop/rebuild.
- Implementation M6 sẽ dùng entrypoint mới/inputs theo session riêng, tái dùng hàm thuần đã freeze cho policy/ranking/kiểm model; không đổi mã M2/M3, freeze hoặc READY để vừa runner.

### Audit toàn nguồn mới — PASS

- Session thực `artifacts/m6/TV1/1d2862f0-a887-4826-8ef2-e3ac6bcc77c4/`; opaque machine-id trong session, không ghi ID Windows gốc. `protected-m2-before.json` đọc mọi document BSON/chín collection DB M5 và giữ hash/count để đối chiếu cuối; không mutation.
- Reference package `artifacts/m6/reference-v1/` là bản sao nguyên bytes freeze/verification/hashes/selected receipt/final receipt. Khớp freeze `f7ee9c13…57d053a`, FINALreceipt `e2552b5a…da7efe`, protocol/policy/core-code/deps/ranking và năm JAR. Không có imported model/preparation làm input fit M6.
- Lệnh: `.venv/Scripts/python.exe -X utf8 scripts/measure_m6.py --session artifacts/m6/TV1/1d2862f0-a887-4826-8ef2-e3ac6bcc77c4 --label audit .venv/Scripts/python.exe -X utf8 pipeline/m6_source.py audit --session artifacts/m6/TV1/1d2862f0-a887-4826-8ef2-e3ac6bcc77c4`. Process/Mongo read có quyền ngoài sandbox; audit chỉ đọc XLSX và ghi SQLite/evidence mới, không Spark/DB mutation.
- `audit-96d1c4e2-9b95-4588-8fe5-1f1039acbb0c.json`: UTC19:53:05.899270→19:58:15.190032 ngày18/10 (=02:53→02:58 ngày19/10 giờ Việt Nam), wall309,243249s; exit0. 1.067.371raw→1.033.036P-01→1.007.913positive_valid→1.003.357merchandise; giữ226.761dòng thiếu khách;39.516giỏ/4.895item; GBP exact19643861.637. Đây là **audit độc lập mới**, chưa phải Spark preprocessing.
- RSS mẫu1s: Python316.846.080/Mongo290.459.648/combined607.096.832byte; JVM0. Combined tính tại từng sample, RSS có sharedpages/peak giữa mẫu; không exactpeak/heap/giờ-người. Web M5 có sẵn chưa được sampler audit đầu tách đo; web=0 ở receipt này nghĩa không đo nhóm đó, không phải web đã dừng. Preimage wrapper audit giữ ở `executed-code/<sha>-measure_m6.py`; audit thực dùng hàm `m2_source.audit` có hash freeze nguyên vẹn.
- 25Python tests (21regression+4M6guards) PASS, `artifacts/m6/TV1/python-regression-outside.log`. Lượt sandbox FAIL2 do WinError5/TemporaryDirectory, giữ `python-regression-initial.log`, rerun nguyên bộ ngoài sandbox đạt; không sửa expected. PowerShell M6 parse không có lỗi, mọi module M6 import được. Đây là fixture/guard checks, không full run/acceptance.
- Tiếp: full import vào `bigdata_m6` mới, đọc lại/hash mọi payload/BSON trước READY. Physical insert được đo từ count trước/sau, không suy sourceREADY là không cần đọc workbook.

### Full import mới — PASS, không tái dùng archive M5

- Lệnh cùng wrapper/session phía trên, thay `--label audit … m6_source.py audit` bằng `--label import … m6_source.py import`. Evidence `import-63f3e7a8-f81e-4512-b66c-492b7edbcae7.{json,stdout.log,stderr.log,samples.jsonl}`; receipt import theo epoch nanoseconds trong session. Executed-code snapshots/hash được wrapper ghi trước launch.
- UTC19:59:09.787227→20:09:56.788312 ngày18/10 (=02:59→03:09 ngày19/10), wall646,441970s; hàm644,507077s, exit0. **Physical insert1.067.371**, đủ525.461/541.910 dòng hai sheet; không phải sourceREADY reuse hoặc probe2.000 dòng.
- XLSX/header/sheet/tám ô có kiểu/vị trí/key/count/BSON Long đạt. Đọc lại mọi source document từ MongoM6 sort sheet/row; SHA256 của canonical JSON từng document + newline **`e297db6edaa4c194cd59518beaa432b9b1d05e9466e5b13a247526e6be29461b`**, khớp stream documents tạo từ workbook. Source chỉ READY sau full readback. Same-payload probe không nhân bản, payload đổi bị từ chối; không cập nhật nguồn để thử xung đột.
- Sampled RSS Python174.276.608/Mongo350.760.960/combined498.683.904byte; JVM0, webM5 không đo nhóm riêng; giới hạn1s/sharedpages/logicaldisk như trên. Không gọi wall import là giờ-người.
- Đã chuyển sang `measure_m6 --label preprocessing … pipeline/m6_preprocess.py --session …`: Spark đọc archive **M6 vừa tạo**, giỏ/summaries/retained-lines mới; M5 source/active giữ. Chưa có kết quả fit/evaluation M6 tại dòng này.

### Spark preprocessing đang chạy

- UUID mới **`b924a31c-0b06-4511-ba23-02d8a4c41b54`**, basket-set logic giữ `cae0d9e7…b3287a`, DB `bigdata_m6`; không lấy preprocessing M2 làm input thay tính toán. Receipt `pipeline-<uuid>.json` đang RUNNING.
- RAM khả dụng trước JVM2.671.865.856byte. Runtime thật: Python3.14.6/PySpark4.2.0/Scala2.13.18/Mongo8.3.8/JDK17.0.12/PyMongo4.18.3/openpyxl3.1.5/psutil7.0.0. `preprocessing-jvm-observed.json` đối chiếu PID31604/create-time/executable/SparkSubmit/scratchM6 và cờ **-Xmx1280m**; cờ là config, không usage. Local[2]/16shuffle/AQEcoalescefalse/ANSItrue/noPrecisionLoss giữ cấu hình M2 đã kiểm.
- Startup125,048507s, Mongo full read83,805177s, P-01+đảo đọc/8–13partition323,330685s, quality/P-02137,437139s; các bước sau chưa hoàn tất tại dòng này. Không có lỗi chặn ở log đã đọc; cảnh báo Hadoop/native dùng Java fallback như môi trường cũ, không tải winutils/DLL để chữa cảnh báo.
- P-01count1.033.036 và toàn bộ checksum lineage khớp audit qua thứ tự/partition khác. Quality/P-02counts/khách thiếu/tiền khớp audit mới: raw1.067.371−34.335=retained1.033.036−25.123=positive1.007.913−4.556=merchandise1.003.357; giữ226.761dòng thiếu khách; GBP19643861.637. Quantity decimal(5,0),price(8,3),product(14,3),sum(24,3) thật; không double/tune/cắt giỏ.
- Chưa kết luận preprocessing PASS trước giỏ/summaries/readback/BSON/file postcheck. Mỗi stage có hash mã thực và preimage ngoài Git; các hardening guard/orchestration M6 được ghi version riêng, hàm policy/fit/ranking M2/M3 không đổi.32file mã M5 so closure snapshot vẫn cùng hash.

### Preprocessing và preparation hoàn tất — PASS

- `preprocessing-6cdc6184-3b41-41dd-935c-2340c124064e.json` exit0: UTC20:10:41.763220→20:27:13.836917 ngày18/10 (=03:10→03:27 ngày19/10), wall**991,279331s**. Các bước cuối line_export143,937089s, baskets/summaries123,504582s, Mongooutputvalidation43,466123s. Không dùng thời gian lịch sử301s làm kết quả lượt M6 hoặc suy nguyên nhân chậm chưa đo.
- Run`b924a31c…41b54` VALIDATED/basket-setREADY; **39.516giỏ/4.895item/5.347summaries**,3.208single/36.308multi,25tháng/426cỡ,maxgiỏ1.108. Counts/tiền/item/month/lineage/keys/schema/BSONLong/readback/retry/final file check PASS. Không gọi checkpoint preprocessing này là modelREADY/FULL_RUN hoàn chỉnh.
- Retained-lines mới413.222.079byte/1.033.036dòng trong `processed/<pre_uuid>/`; byteSHA **`82ddde19db72b295d723ebb3ca1068ccbabf3a44a49d8ab396598842e5bc5c74`** tình cờ cũng khớp tham chiếu sau khi tái tạo; không dùng hash giống làm bằng chứng tự thân đã chạy hay lấy file M2 thay output. Basket logicalSHA **`982ab870ab7f8118cdada770c9269fa0e464f2a789c778f9f0289ad852b8c05d`** khớp audit.
- Peak sampledRSS Python204.398.592/JVM1.739.796.480/Mongo360.660.992/combined2.229.301.248byte. Log Windows “SUCCESS…terminated” cuối là cleanup cây gateway/Spark do batch sở hữu; Spark đã dừng/exit0, không kill Java khác. Kiểm web thực sau batch sẽ xác nhận không còn Spark. WebM5 vẫn chưa chuyển tại thời điểm này.
- Preparation **`preparation-6a902fcb-2d61-4b2a-bbf2-0bcfd51b1272`** PASS, receipt/wrapper `prepare-6ec93a8e-691b-433f-aec6-28613bd5f65d.json`: wall20,607450s, sampledRSS Python276.242.432/Mongo345.853.952/combined622.096.384byte. Train29.335giỏ(2.503single)/dev4.609(316single)/testmetadata5.572, overlap0;717.574dòng merchandise train dựng4.556catalog/tên mới;4.293devqueries mới. Train/dev/catalog/query/split hashes khớp freeze trước model.
- Đã gọi `measure_m6 --label model … m6_model.py --session <session> --preparation <preparation>`; **fit mới từ Mongo trainM6**, nguyên support.01/confidence.3/8partitions/local[2]/768m/-Xss4m/K5/seed20261015, guards600s/200000output. Chưa có kết quả M6model/FINAL khi ghi dòng này; không grid/tune hoặc imported model.

### Incident runtime trong model M6 — giữ log, không đổi stack/freeze

`model-aa3f5faf-e1bc-48d2-8137-de79c52c8aa1.stderr.log` lúc03:32:54 ngày19/10 local (=20:32:54UTC18/10) có **ERROR Utils / NullPointerException ở executor-heartbeater**, `PartitionKeyedAccumulator.isZero` vì `byPartition` null. Job vẫn chạy các stage sau; chưa suy exit0/PASS từ việc tiếp tục. Lượt tìm có mục tiêu không thấy signature này trong các `*.stderr.log` M3/M5 đã lưu. Không gọi đây là OOM/StackOverflow hay lỗi mã ranking.

Đã đối chiếu nguồn chính thức [Apache Spark PR58960](https://github.com/apache/spark/pull/58960), đọc19/10/2026: cơ chế accumulator được heartbeat truy cập trong lúc giải tuần tự hóa chưa hoàn tất phù hợp signature quan sát. Đây là **suy luận nguyên nhân từ trace và upstream**, không phải đã patch/test bản Spark mới trên máy này; không suy một release cụ thể đã chứa fix từ tên PR. Giữ nguyên4.2.0/freeze/config; không cài/nâng dependency hay đổi cache/heartbeat để né. Chỉ cho READY/publication sau batch thành công và đầy đủ all-count/checksum/dev parity/postcheck; dù đạt vẫn giữ incident và giới hạn độ ổn định, không báo log sạch.

### Model mới và publication DEVELOPMENT — PASS, có incident runtime nêu trên

- DEVELOPMENT UUID **`ee2597f8-7127-4d50-ad75-1c45a3782abd`** READY sau VALIDATED/postcheck, exit0; không đọc test items/masks/predictions trong command train. `model-aa3f5faf-e1bc-48d2-8137-de79c52c8aa1.json` UTC20:32:07.468253→20:41:54.900251 ngày18/10 (=03:32→03:41 ngày19/10), wall587,283484s. Startup/input16,041374s; materialize/fit40,548497s; extract+independent counts485,892528s; dev/output12,230265s. Guard600s áp cho Spark job group (fit+extraction), không phải toàn wrapper/pre/postcheck; không nới guard, không retry chọn score.
- Mới fit **29.335giỏ train**;4.556catalog/1.349itemsets/856rules. Mọi frequency được đếm độc lập theo tập invoice train; luật đầy đủ/công thức/schema/keys/crossref/BSON/readback/postcheck đạt. Ba logicalchecksums **khớp chính xác**: items`a99f74a37f3a99f003e9b79debc3325e3c58783a0bef18e242669541c6063b54`,itemsets`c0348117dd5df9a8c07659c8c68e9f4ae729b91081fc7e0c2e1393c4dd830386`,rules`10d880e91f2fb4afc2b81640f500bb60ccfd6c525552154c07e0c37b589e0c96`.
- Toàn bộ4.293dev predictions/best rules/baseline/subgroup metrics khớp reference: luật505hit/3.513nonempty,baseline109hit/4.293nonempty; mẫu số4.293 giữ unknown/no-rule. Không dùng source/model/outputs M5 làm đầu vào tính toán; reference chỉ config/checksum/metrics đối chiếu.
- SampledRSS Python376.426.496/JVM1.160.560.640/Mongo359.219.200/combined1.714.966.528byte; cờ stack4m/heap768m được assert từ JVM thật. Spark dừng trước READY; gateway cleanup đúng cây batch. `runtime-incidents.json` giữ NPE/tracehash/upstream/disposition riêng, không sửa READY receipt để giấu lỗi; độ ổn định runtime vẫn có giới hạn.
- `m6_publish.py --session <session> --run-id ee2597f8-7127-4d50-ad75-1c45a3782abd --initial`: PASS/version**1** của DBM6 sau postcheck, durableintent/readback. DBM5/activeFINALversion3 giữ.
- Đã `invoke-m5 Status→StopWeb` đúng identity/receipt để build/startM6 tại8081; JAR/receipts M5 giữ. `build-web.log` là checks build/fixture, không fullrun acceptance. Chưa mở FINAL M6 trước HTTP gate của DEVELOPMENT mới.

### Web gate và FINAL replication — PASS

- `invoke-m6 -Action Build -Session <session>` BUILD SUCCESS, fixture9tests chạy đạt/2actual-data tests skipped do chưa truyền runDirectory; không gán skips thành parity. WebM6 StartWeb thành công, DBURI`bigdata_m6`/loopback8081/DEVELOPMENT v1; M5web đã dừng đúng receipt. Bộ25Python tests cuối **PASS**, `python-final-regression.log` trong session, không đổi expectation.
- Gate **`http-2026-10-18T210507.625872+0000.json` PASS108requests** trên đúng DEVELOPMENT UUID/version1: mọi bucket/GBP/KPI/catalog/rule/itemsetpage/rank/best antecedent/no-rule/input/stale khớp; form M5 FINAL/version3 cũ trên cùng URL trả409, không predictions. Spark không còn chạy; đây là read-only web thật, khác Java fixture/build.
- Lệnh `measure_m6 --label final … m6_evaluate.py --session <session> --integrated-run ee2597f8… --e2e-receipt <gate>` exit0; FINAL UUID **`87b3fc04-bb8e-449f-9ecc-3c5308b3d689`** READY sau postcheck, rekey **model M6 vừa fit**, không imported model/refit/tune.
- Ledger exclusive `87b3fc04…/test-access.json`: **2026-10-18T21:07:39.177612UTC (=04:07:39ngày19/10)**, event`M6_REPLICATION_TEST_ITEMS_READ_ATTEMPT`, lưu argv/code/freeze/model/gate và exposure gốc M5 **18/10 15:05:29.761348UTC**. M6 không phải test độc lập mới. Protocol snapshotNOT_RUN trong freeze giữ bytes gốc; manifest FINAL mới MEASURED.
- Test5.572giỏ=389single+**5.183query**, max1.108,825newtarget/3.786query newcontext/22.803occurrence/969no-rule giữ trong N. Mọi mask/prediction/best rule/subgroup/metrics và ba file test baskets/queries/predictions bytehash khớp exact M5reference theo checker; fullM6basket logicalhash khớp audit. Không lọc unknown khỏi đánh giá để ép UI200.

| FINAL tái lập | Hit / N | Recall@5 | Nonempty / N | Tỷ lệ có gợi ý |
| --- | ---: | ---: | ---: | ---: |
| Luật thuần | 451 / 5.183 | 8,7015242138% | 4.214 / 5.183 | 81,3042639398% |
| Baseline train | 91 / 5.183 | 1,7557399190% | 5.183 / 5.183 | 100% |

- Wrapper `final-8baf717e-987f-4ec9-979e-b4092fea1a3e.json`: wall81,311840s; sampledRSS Python416.063.488/JVM0/Mongo164.245.504/web327.237.632/combined905.269.248byte. WebM6 được đo nhóm riêng ở phase này; combined tính cùng sample, không cộng các peak nhóm. JVM0 phù hợp không fit lại.
- Publisher CAS explicit expected`ee2597f8…/version1`→FINAL`87b3fc04…/version2` **PASS**, durableintent/readback. Giữ các READY cũ và DBM5. Đang chạy Java parity đủ dev/final và HTTP FINAL, chưa tick human demo/DoD.

### Parity, UI và lifecycle thực tế

- **11Java tests PASS/0skipped**, `java-final-parity.log`; Maven offline projectcache, property m3.runDirectory trỏ **M6 DEVELOPMENT**, m5.runDirectory trỏ **M6 FINAL**. Kiểm đủ4.293dev/5.183final về consequent/thứ tự/tiền đề tốt nhất, baseline và arithmetic; tên property lịch sử không biến dữ liệu kiểm thành M3/M5. HTTP Tomcat fixture còn kiểm unavailable/schema/XSS/input; đây là probe/service synthetic, không tuyên bố đã phá Mongo thật để dựng lỗi.
- **HTTP FINAL118requests PASS**, `http-2026-10-18T212654.974252+0000.json`, run87b3fc04…/version2; tất cả output/KPI/catalog/ranking/stale/unknown input khớp. Đã gửi form DEVELOPMENT/version1 cũ và nhận409/no predictions. Offline query có unknown vẫn giữ nguyên N; raw context không thuộc catalog trên form phải400.
- **Browser16checks/11ảnh PASS**, `browser-b069491b-cd45-41c9-a78d-041e6e547854/browser-2026-10-18T212809.130Z.json`, current machine/session guard, exact FINALUUID/version2. Chrome headless profile riêng, exit0, không JSexception;1440×1000 và390×844/mobile không tràn ngang. Case no-rule train**10002** trả[]/không fallback. Ảnh overview/full,patterns,FINAL,itemsets,search,recommendation,no-rule,empty,stale,mobile có caption/run/version/path; đã xem trực tiếp ảnh FINAL và mobile, số/N/nhãn/layout đúng. Đây là Agent/browser QA, không thay người thật demo.
- **Lifecycle PASS** `lifecycle-20261018T213028.json`, UTC21:30:28.8305936→21:31:03.7565252: lưu oldreceipts→StopWebM6 đúng owner→Mongo27019 shutdown bình thường→xác nhận8081/27019 không nghe→StartMongo→StartWebM6, **không rerun batch**. MongoPID13768→29820, webPID24520→23704; exe/hash/start/args/loopback kiểm theo receipt. Dịch vụ27017/PID5940 vẫn nghe xuyên quá trình; không thao tác.
- RuntimeJAR **`5a7357a51d4b92c15679c0ad3847fa9e8c628b0327da07d68fd66db619f07aa6`**, bản copy M6 riêng trong session; cùng bytes code M5 sau build là hợp lệ, không imported dữ liệu/model. Đang kiểm lại HTTP saurestart và hash toàn dữ liệu để chốt technical receipt; chưa gán lifecycle file tồn tại thành nghiệm thu.

## Gói demo và review M6 của người thật

Nguồn: MasterPlan13 **M6-AC2/DoD** cần thao tác/giải thích thật; U-48 chỉ đóng M5. U-52 đã điều chỉnh máyTV2 thành giả định tương đương, không hỏi lại logs máy đó. Agent chạy kỹ thuật/ảnh/HTTP không tự xác nhận người dùng đã demo/hiểu luồng M6.

1. Mở [Tổng quan](http://127.0.0.1:8081), [FINAL](http://127.0.0.1:8081/patterns), [Giỏ](http://127.0.0.1:8081/basket). Kiểm run **87b3fc04-bb8e-449f-9ecc-3c5308b3d689 / phiên2**. Giải thích tổng quan toàn kỳ39.516giỏ/4.895item/GBP19643861.64 khác train29.335/catalog4.556.
2. Giải thích P-01 giữ đầu tuple8ô theo sheet/row; sourcearchive khác retained-lines/giỏ. P-02/TEST loại phí/Manual/voucher/test, vẫn giữ mã chữ và khách thiếu. M6đã nhập1.067.371dòng vào DBriêng rồi Spark xử lý mới; checksum giống không tự chứng minh đã chạy, phải đi cùng run/lệnh/source/readback/resources mới.
3. Đọc dev505/4.293hit và3.513nonempty; FINAL451/5.183hit và4.214nonempty; baseline91/5.183hit/100%nonempty. Test5.572=389single+5.183query;825target mới/969no-rule không bỏ khỏi N. K5/seed/mask/ranking giữ freeze; M6là replication sau test đã tiếp xúc M5, không chất lượng mới/tune theo score.
4. Tự chọn sáu mã **21080/21094/21467/21770/22704/22969**, gửi giỏ; cần đúng **21086 rồi21212**, căn cứ tốt nhất `{21080,21094}→21086`, `{21080}→21212`. Đây là case dev558640. Thử một item/trùng/item đã có: đủ mọi tiền đề trước áp luật, mỗi consequent một lần, không trả item đã có.
5. Chọn **10002**: hợp lệ nhưng không có gợi ý, không fallback baseline. Gửi giỏ rỗng báo lỗi; form phiên cũ409 yêu cầu tải lại. Context ngoài train giữ trong offline N nhưng form trả400. Tìm kiếm vẫn giữ lựa chọn/“Chỉ xem lựa chọn”.
6. Giải thích kiến trúc batchSpark→Mongo READY/publication→MVC/Thymeleaf; Spark dừng mà web vẫn đọc đúng final sau Mongo/webrestart. Publisher explicitUUID/expected-run/version tránh trộn snapshot. Đọc incident NPE heartbeat: nguồnupstream/trace, không giấu log hoặc đổi freeze; output/counts/parity vẫn được kiểm độc lập. Nếu cần thay Spark để xử lý độ ổn định, đó là lựa chọn riêng chưa thực hiện.
7. Review hướng dẫn M6/những lỗi đã ghi, báo đã trực tiếp thao tác/giải thích/review/chấp thuận hay điểm cần sửa. Chỉ xác nhận điều đã làm; không cần giả một receipt TV2. Chưa có xác nhận M6 ở thời điểm tạo gói này nên DoD/human phần tương ứng giữ pending.

## Trạng thái nghiệm thu

**M6 đã đóng19/10/2026 theo phạm vi U-52/U-53.** Nguyên bản yêu cầu hai full run thật chưa được chứng minh bằng hai máy; U-52 đã điều chỉnh phạm vi hiện tại trước triển khai phần phụ thuộc. Chỉ có FULL_RUN đo thật trên máy hiện tại, TV2 là `ASSUMED_EQUIVALENT_BY_USER_NOT_MEASURED`, không bản receipt gắn role thay máy.

- Technical receipt **`artifacts/m6/TV1/1d2862f0-a887-4826-8ef2-e3ac6bcc77c4/technical-full-run-2026-10-18T213757.940900+0000.json`**, statusPASS, SHA256 **`a553867db6e1db397887fa020bbdbaee2a4590adc924defbceb3198ef63a6ae4`**. Đọc lại toàn source M6 khớp SHA payload mới; mọi document BSON/count/hash trong DB `bigdata_m2` khớp snapshot trước chạy. Mã/freeze/source/READY giữ nguyên. Incident heartbeat được giữ trong receipt; không gán PASS thành log sạch hoặc đã sửa Spark.
- HTTP sau restart **`http-2026-10-18T213157.198470+0000.json` PASS118requests**, đúng FINAL87b3fc04…/version2; không chạy Spark để phục vụ web. Đây là lượt kiểm riêng sau lifecycle, không tái dùng lượt HTTP trước restart.
- **Review U-53**: người dùng trả lời nguyên văn **“Đã demo/giải thích/review; chấp thuận M6”** sau câu hỏi gắn URL8081/FINALversion2,39.516giỏ/4.895mã,451/5.183,giỏ6mã→21086/21212,no-rule10002,hướng dẫn và incident Spark đã ghi. Lưu **`review-U53.json`** lúc2026-10-18T21:41:50.605843UTC (=04:41:50ngày19/10), liên kết SHA technical receipt; không sửa snapshot humanPENDING trong READY/technical receipt. Đây là xác nhận người dùng, không Agent xác nhận thay, không suy GV nghiệm thu/hai người độc lập/giờ hoặc phần trăm đóng góp.
- T1: guide8/runners/nguồn/freeze/guard/session/lệnh và kết quả thật; T2: full import/preprocess/fit/evaluate/publication/web máy hiện tại do Agent hỗ trợ, người dùng demo/giải thích/review U-53; T3: phạm vi thay bởi U-52, không tick như đã đo TV2; T4: lỗi/hướng dẫn/HTTP/UI và stop/start Mongo/web thực tế, review U-53. AC1/AC3 áp dụng U-52; AC2/DoD đủ outputs/parity/demo/review theo thực tế.
- Kiểm repository cuối bằng `.venv/Scripts/python.exe -X utf8 artifacts/m6/TV1/1d2862f0-a887-4826-8ef2-e3ac6bcc77c4/repository-m6-check.py artifacts/m6/TV1/1d2862f0-a887-4826-8ef2-e3ac6bcc77c4`; receipt `repository-final-*.json` cùng session giữ kết quả diff/nguồn/282ID+hàng/trọng số/U cũ/32file core M5/READY/links/ignore/syntax. Kết luận chỉ theo receipt PASS, không suy từ file tồn tại.

**Kết quả repository cuối:** `repository-final-2026-10-18T214557.580323+0000.json` **PASS**; HEAD giữ `4d1d254…b885`, không staged/commit/push;282dòng nguồn/trọng số RTM và map giữ nguyên,49U cũ/twoWord/32file core M5/freeze/READY giữ. Kiểm799liên kết file và ignore dữ liệu/runtime/cache, AST mã Python M6 đạt. Sau kiểm chỉ bổ sung tên receipt/kết luận vào docs, không đổi code/runtime/READY; `git diff --check` cuối được kiểm lại. Build/test/runtime đã kiểm phía trên; không chạy batch lại vì cập nhật review tài liệu.

Giữ demo FINAL/version2 tại [127.0.0.1:8081](http://127.0.0.1:8081/), Mongo27019; Spark/Chrome đã đóng. Lệnh Status/StopWeb/StopMongo theo [Web Guide](../web/README.md), không xóa DB/output/source; dịch vụ27017 giữ. **Bàn giao rồi dừng tại M6**, không tự mở M7/M8 hoặc commit/push; không còn xác nhận M6 cần hỏi lại.

## Chuẩn bị tiếp nối M7A — 19/10/2026, U-54

Người dùng hỏi M6 còn cần confirm/lựa chọn không, nếu đủ thì đề nghị tiêu đề commit và tạo prompt thread mới. **Không còn confirm riêng cho M6 trong phạm vi U-52/U-53**. Đã kiểm lại repository bằng checker read-only, `repository-final-2026-10-19T122206.697254+0000.json` PASS; không chạy batch/đọc DB/process sống/đổi lifecycle hoặc sửa READY. Snapshot giữ nguồn/Word/freeze/32file core M5 và M6 code hiện hành; U-53 receipt riêng vẫn đủ, không hỏi lại.

Đọc trực tiếp OOXML toàn nội dung/bảng hai Word nguồn, SHA256 B`7d1cf21ef1dac4e791a0e765c3fc15353e95078f729a907b766c8e9779f95ad6`, A`25ce340ffa6c1931cfe59e2be22ae689b8eaf76ac5068b1b25fe7913d79fec35`. Đối chiếu B phần II.2/II.3 và quy định cuối A: B liệt kê phần xây dựng ứng dụng/trực quan hóa, A cho phép đổi tên chương theo tính chất đề tài; U-26 khung B/quy cách A giữ. Đây là kiểm nguồn văn bản/cấu trúc, không render/QA một báo cáo Word mới.

U-54 chỉ giao phần Word kỹ thuật cho thread mới, không lý thuyết riêng/khảo sát nghiệp vụ/mở đầu/cảm ơn; slide và kiểm gói/nộp để sau. Người dùng cho phép viết vào mẫu hoặc file khác; chọn DOCX mới để giữ nguồn gốc. **Tạo baseline cụ thể để người dùng duyệt trước chi tiết**, không tự qua cổng này. [Prompt M7A](../requirements-review/M7A_START_PROMPT.md) giữ sources/run/hash/số liệu/luồng M0–M6/mapping phần nhóm ngoài scope/renderQA/phong cách/điểm dừng; STATE/07/13/14 đã ghi phân rã. Baseline/Word chưa tạo, M7A chưa thực hiện; không tự làm slide/M8 hoặc stage/commit/push. Kiểm prompt và preservation tại `artifacts/m6/handoff-m7a-*.json`; không biến chuẩn bị prompt thành nghiệm thu báo cáo.

Kiểm bàn giao **`artifacts/m6/handoff-m7a-20261019T122704145916Z.json` PASS5nhóm checks**: technical/U-53 đúng hash; hai Word/XLSX/freeze/M5FINAL giữ nguyên;282hàng nguồn/trọng số và U cũ giữ; M6/M5code không đổi; prompt có input thực/baseline gate/QA/phạm vi, links/ignore hợp lệ, không có baseline/finalDOCX được tạo. Đây là kiểm file/nguồn/tài liệu, không xác minh DB/process sống ngày19/10. Sau receipt chỉ bổ sung tên/kết quả receipt vào notes/checklist, không đổi code/nguồn/runtime; diff cuối kiểm lại. Tiêu đề đề nghị: `feat(m6): reproduce full pipeline and prepare M7A handoff`; không stage/commit/push.
