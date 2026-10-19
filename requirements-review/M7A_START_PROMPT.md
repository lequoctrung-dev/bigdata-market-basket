# Prompt tiếp nối M7A — Word kỹ thuật, duyệt baseline trước nội dung chi tiết

Dán toàn bộ nội dung dưới đây vào thread mới trong cùng project. Đây là bàn giao chuẩn bị ngày **19/10/2026**, chưa phải báo cáo hoặc nghiệm thu M7A.

---

Tôi giao bạn thực hiện **M7A — phần Word kỹ thuật của báo cáo đồ án**, tại:

`D:\University\Semester7\BigData\DoAn`

Đọc đầy đủ prompt này và nguồn chỉ dẫn rồi thực hiện. **Lần đầu phải tạo baseline cụ thể để tôi review; chờ tôi duyệt baseline trước khi viết nội dung chi tiết.** Không chỉ trả lời bằng kế hoạch trong chat.

## 1. Phạm vi tôi giao và điểm dừng

- M0–M6 đã đóng; **U-53 đủ xác nhận demo/giải thích/review M6**, không hỏi lại. U-54 tách công việc M7: hiện chỉ giao **M7A/Word kỹ thuật**; phần slide, dry-run gói nộp và công việc còn lại của M7 để sau, chưa được giao. Không thực hiện M8 hoặc gửi/nộp Classroom.
- Tôi đảm nhiệm **toàn bộ nội dung kỹ thuật đã thực hiện của đồ án**, gồm dữ liệu, tiền xử lý, pipeline, lưu trữ MongoDB, FP-Growth/đánh giá trong triển khai, website Java/Spring và vận hành/kiểm chứng. Không giới hạn báo cáo vào nhánh data của TV1 rồi bỏ phần Java/web của TV2; cũng không suy phạm vi tôi viết báo cáo thành tôi đã làm toàn bộ code hoặc phần trăm đóng góp.
- **Không viết phần cơ sở lý thuyết riêng, khảo sát nghiệp vụ, lời mở đầu/lời chào/lời cảm ơn và các phần ngoài trách nhiệm kỹ thuật.** Vẫn giải thích đủ cơ chế, công thức và lý do lựa chọn ngay tại bước triển khai để người đọc hiểu. Ví dụ: giải thích cách tính support/Recall gắn số thực tế là trong phạm vi; viết chương tổng quan thuật toán hoặc khảo sát tài liệu dài là ngoài phạm vi.
- Các phần B yêu cầu nhưng tôi chưa giao viết phải có vị trí/mapping để ghép sau và trạng thái rõ, không âm thầm xóa nghĩa vụ của báo cáo nhóm. Không bịa danh tính, MSSV, GV, lịch tuần, giờ làm hay đóng góp để lấp trang. Không gọi phần Word kỹ thuật là toàn bộ báo cáo nộp đã đủ.
- Nguồn: **`Ke hoach Do an mon hoc Nhap mon Big data_SV.docx`** là yêu cầu môn; **`Mau bao cao_Do an_Khoa luan_2025.docx`** là mẫu cấu trúc/trình bày. Người dùng cho phép viết vào mẫu hoặc file khác; **chọn file mới trong `reports/` để bảo toàn cả hai Word nguồn**. Không sửa mẫu gốc chỉ để soạn báo cáo.
- Luồng làm: đọc nguồn/bằng chứng → tạo baseline Word → tự kiểm và trình tôi review → **dừng chờ duyệt baseline** → chỉ sau khi tôi duyệt mới viết chi tiết → render/kiểm/review bản cuối. Không coi im lặng hoặc kiểm tự động PASS là tôi đã duyệt baseline.

## 2. Cách làm việc bắt buộc

Giao tiếp và viết tiếng Việt, rõ ràng, mạch lạc. Tôi ưu tiên đúng yêu cầu và số liệu, toàn vẹn dữ liệu, nội dung có bằng chứng, giải pháp đơn giản. Làm tới đâu ghi nguồn/quyết định/thông số/lỗi/kiểm chứng tới đó vào **`reports/M7A_TECHNICAL_REPORT_NOTES.md`**, tạo ngay khi bắt đầu. STATE giữ ngắn, checklist giữ nghiệm thu; không tạo roadmap song song.

Không rõ thì **kiểm nguồn trước**. Nếu vẫn thiếu thông tin hoặc có lựa chọn quan trọng ảnh hưởng nội dung đúng/sai, cấu trúc/phạm vi báo cáo, dữ liệu, bảo mật, kiến trúc/protocol/schema: nêu tác động, **2–3 phương án cụ thể, trade-off và đề nghị**, chờ tôi chọn trước phần phụ thuộc; tiếp tục phần độc lập. Không tự hiểu hoặc tự chọn bừa, không hỏi lại U đã chốt. Các chi tiết trình bày nhỏ trong quy cách đã duyệt tự xử lý có căn cứ. Không hỏi một loạt thông tin bìa/đóng góp ngoài phần tôi giao để chặn baseline kỹ thuật.

Không sửa code, chạy lại batch/model/test cuối, tune, cài/nâng stack hoặc start/stop demo chỉ để viết báo cáo. Trước hết đọc artifact có sẵn. Nếu thật sự cần ảnh mới hoặc phép đo mới, kiểm đúng process/run/ownership và phạm vi trước; không dựng số liệu/ảnh giả. Không đọc DB bằng checker lịch sử có mutation. Không reset/drop/cleanup nguồn hoặc output, sửa freeze/READY/receipt cũ, commit/push. Không tự mở M7B/M8.

## 3. Đọc nguồn theo thứ tự

1. `AGENTS.md`, `README.md`, `STATE.md`; `git status --short`, HEAD, diff liên quan. Bảo toàn mọi thay đổi hiện có. HEAD ở phiên chuẩn bị là `4d1d254bae0dbcc555455a37029b03b709f9b885`; **nếu người dùng đã commit sau đó, dùng HEAD thực tế**, không ép khớp snapshot hoặc chạy verifier khóa HEAD cũ.
2. `requirements-review/07_CONFIRMED_SCOPE.md` (đặc biệt U-08/U-20/U-21/U-23/U-26/U-27–U-29/U-40–U-54), phần M7/M7A trong `13_MASTER_IMPLEMENTATION_PLAN.md`, `14_MILESTONE_CHECKLIST.md`; `02_REPORT_STRUCTURE_CHECKLIST.md`, `03_DELIVERABLES_CHECKLIST.md`, `15_REQUIREMENT_MILESTONE_MAP.md` và phần liên quan trong `01_REQUIREMENT_MATRIX.md`.
3. **Đọc trực tiếp đầy đủ hai Word nguồn** nêu trên, gồm bảng và quy định cuối mẫu A. Đối chiếu `SOURCE_EXTRACT.md`, `06_SOURCE_AUDIT.md`; không thay đọc nguồn bằng suy từ tên file. Nếu công cụ không đọc được, nói chính xác phần chưa đọc được. Bảng trích/ảnh lịch sử là hỗ trợ truy vết.
4. Hồ sơ từ đầu dự án: quyết định M0 và contract trong `11_SPECIFICATION_DRAFT.md`, `12_TECHNICAL_DESIGN.md`; `08_DATASET_EVALUATION.md`, `10_DATASET_PROFILE.md`; notes M2–M6 trong `reports/`, hồ sơ M1 ở checklist/guide/receipt, README `pipeline/` và `web/`. Phân biệt đề xuất, prototype và phần đã triển khai/đo thật. Không chép audit cũ thành runtime policy mới.
5. Mã thực tế liên quan: pipeline M2 source/preprocess/runtime; M3 prepare/protocol/trial/freeze; M5 integration/final/publication; M6 source/preprocess/prepare/model/evaluate/verify/publish/common; Java controller/service/repository/ranking, template và cấu hình web; scripts lifecycle/measurement/HTTP/browser. Chỉ đọc đủ phần cần cho giải thích/citation; không quét secrets hoặc code dự án khác.
6. Artifact/receipt/run/hash/ảnh được notes trỏ đến: M3 freeze/verification; M5 FINAL và test-access; M6 session/technical/review/lifecycle/HTTP/browser/resource logs. Kiểm tồn tại/hash trước dùng. Nếu clone thiếu artifacts, giữ phần có bằng chứng trong notes và liệt kê đúng file còn thiếu; không tự tái chạy full pipeline, tạo ảnh hoặc bịa receipt thay thế.

Giữ 282 ID, câu nguồn và trọng số RTM/map bất biến. U-26 chốt **khung B + quy cách A**. Yêu cầu hiện tại dùng mẫu A làm cấu trúc tham chiếu, không tự ép đủ năm chương ngoài phần kỹ thuật. Mẫu A cho phép đổi tên chương theo tính chất đề tài; baseline phải thể hiện mapping B ↔ mục trong mẫu A ↔ phần kỹ thuật đề xuất và phần để người khác bổ sung. Nếu còn cách hiểu quan trọng khác, trình lựa chọn ngay trong gói baseline, không âm thầm thay U-26.

## 4. Snapshot kỹ thuật đã chốt để đối chiếu

Đây là chỉ mục bằng chứng, không thay đọc receipt và mã. Khi ghi báo cáo, dùng tên dễ hiểu và diễn giải; UUID/hash dài đặt ở bảng provenance/phụ lục khi hữu ích.

### Hệ thống và dữ liệu

- Đề tài: **Phân tích hành vi mua sắm và gợi ý sản phẩm mua kèm**. Stack PySpark local/FP-Growth, MongoDB, Spring Boot/MVC/Thymeleaf. Batch chạy riêng; website chỉ đọc output đã công bố, không Spark fit theo HTTP request. Không thêm HDFS/cloud/cluster/SPA/API Python hoặc tính năng bán hàng mà hệ thống không có.
- Online Retail II được GV chấp thuận **theo xác nhận người dùng**, không Agent có xác nhận độc lập từ GV. File `data/raw/online-retail-ii/online_retail_II.xlsx`, SHA256 `bcbe73b35f5b7babf197fb0cb983a11f5d9ff929078d4aa53d171b1f2df2e980`.
- Hai sheet525.461/541.910 dòng, tổng **1.067.371**. P-01 giữ lần đầu tuple tám giá trị nguồn giống nhau theo thứ tự sheet rồi row, trên cả hai sheet; không dedup bằng Invoice/StockCode. Sau P-01 **1.033.036**, positive_valid **1.007.913**, merchandise **1.003.357**; **226.761** dòng merchandise thiếu khách vẫn giữ. P-02 loại phí/Manual/voucher/điều chỉnh/TEST001/TEST002 theo mapping; giữ hàng có mã chữ.
- Toàn kỳ **39.516 giỏ/4.895 mã**,5.347summaries;3.208single/36.308multi,25tháng,maxgiỏ1.108; GBP exact **19643861.637**, UI làm tròn **19643861.64**. Chỉ dùng các cỡ/chi tiết khi receipt/mã xác nhận. Tiền exact decimal text, counts BSON Long; không diễn giải double/đổi tiền VND hoặc timezone không có nguồn.

### Train và đánh giá

- Train **29.335**, dev **4.609**, test **5.572** giỏ; không overlap. Catalog/tên/baseline **4.556 mã từ train**, dựng từ717.574dòng merchandise train; khác 4.895mã toàn kỳ. Đọc protocol để ghi chính xác mốc chia thời gian, không đoán.
- Frozen minSupport=.01/minConfidence=.3/8partitions/local[2]/heap768m/stack4m; K=5,seed20261015. **1.349 itemsets/856 rules**. Không đổi cutoff/K/seed/policy để cải thiện score.
- P-03 ẩn một item từ giỏ đủ điều kiện, luật thuần so baseline phổ biến train; confidence↓/lift↓/support↓ và tie-break ổn định theo code, không fallback. Giải thích mẫu số/single/unknown cùng công thức trong ngữ cảnh chạy thực tế, không tách thành chương lý thuyết tôi chưa giao.
- Dev4.293query: luật505hit/3.513nonempty,baseline109hit/4.293nonempty. FINAL **5.183query =5.572−389single**: luật **451hit/4.214nonempty**,baseline **91hit/5.183nonempty**. Recall@5 **8,7015242138%/1,7557399190%**, tỷ lệ có gợi ý **81,3042639398%/100%**. Giữ825target mới/969no-rule và unknown trong N; không báo coverage như accuracy hoặc suy doanh thu/hiệu quả thương mại đã đo.
- M3 freeze `artifacts/m3/freeze-1a1f2ec6-331e-4b02-9aaf-18804793d4e9/freeze.json`, SHA256 `f7ee9c13432f0c99e7e5bcbf0363eed77eb4d5493b39e78fbb2e8e48557d053a`. M3 selected `7bc55ac7-0d24-4ddd-a9b0-3b25d247b596` là DEVELOPMENT. Protocol snapshotNOT_RUN trong freeze giữ lịch sử, kết quả FINAL nằm run về sau; không gọi đó là mâu thuẫn rồi sửa freeze.
- M5 DEVELOPMENT `8cef7ef5-6731-47b1-bcd7-bd908cfad7b2`, FINAL `04c940db-313d-4a05-a039-90163e33f070`/publicationv3. Test tiếp xúc đầu **18/10/2026 15:05:29.761348UTC**. M5 đã tích hợp/đánh giá cuối/crash-retry-CAS/stale forms/parity; preprocessed source M2 được reuse, không nói M5 nhập/preprocess lại toàn workbook.

### M6 tái lập và vận hành

- U-51: `bigdata_m6` riêng trên Mongo loopback27019, cùng dbpath/lifecycle M2; `bigdata_m2`/active M5 giữ nguyên. Web loopback8081, dịch vụ27017 ngoài scope.
- Session thật **`artifacts/m6/TV1/1d2862f0-a887-4826-8ef2-e3ac6bcc77c4`**. Import mới đủ1.067.371, preprocessingUUID `b924a31c-0b06-4511-ba23-02d8a4c41b54`, preparation `preparation-6a902fcb-2d61-4b2a-bbf2-0bcfd51b1272`, DEVELOPMENT `ee2597f8-7127-4d50-ad75-1c45a3782abd`, FINAL **`87b3fc04-bb8e-449f-9ecc-3c5308b3d689`/publicationv2**. Fit mới trainM6, không imported model; exact model/predictions/metrics khớp freeze/M5. Đây là replication sau test đã tiếp xúc, không test độc lập mới hoặc điểm số được nâng lên.
- `technical-full-run-2026-10-18T213757.940900+0000.json` PASS, SHA256 **`a553867db6e1db397887fa020bbdbaee2a4590adc924defbceb3198ef63a6ae4`**; `review-U53.json` người dùng **“Đã demo/giải thích/review; chấp thuận M6”**, riêng với technical snapshothumanPENDING bất biến. 25Python/11Java tests PASS;108HTTPdev/118HTTPfinal/118HTTPsau restart;16browserchecks/11ảnh. M6 technical receipt kiểm toàn BSON DBM5 giữ nguyên, full payloadM6 và output parities.
- Ảnh thật M6 ở `browser-b069491b-cd45-41c9-a78d-041e6e547854/` trong session: overview/full,patterns,FINAL,itemsets,search,recommendation,no-rule,empty,stale,mobile; receipt browser `browser-2026-10-18T212809.130Z.json`. Chọn ảnh đúng mục đích, cùng run/version; không gắn ảnh M4 vào nhãn FINAL M6.
- Lifecycle `lifecycle-20261018T213028.json`: dừng/mở lại Mongo27019 và web đúng ownership, không rerun batch, sau restart118HTTPPASS. Spark/Chrome kiểm đã đóng, Mongo/web giữ để demo tại thời điểm bàn giao. PID không phải trạng thái sống thread mới; không cần thay lifecycle chỉ để soạn Word.
- Lỗi **Spark executor-heartbeater NPE/PartitionKeyedAccumulator** có trace/runtime-incidents; jobexit0 và exhaustivecount/checksum/parityPASS. Giữ hạn chế độ ổn định, không báo log sạch/đã sửa Spark. Upstream link trong notes chỉ hỗ trợ suy luận nguyên nhân, không chứng minh đã patch/test bản mới.
- **U-52** điều chỉnh nghiệm thu: TV2 `ASSUMED_EQUIVALENT_BY_USER_NOT_MEASURED`, không full run/measurement độc lập máy đó. Báo cáo không được ghi đã chạy thật hai laptop. M6 đóng đúng phạm vi điều chỉnh và reviewU-53; không hỏi lại logs TV2 để chặn Word.
- Tài nguyên/phần mềm: đọc receipts đúng từng lượt; đã đo Windows11x64/i5-13500H/RAM16.786.550.784byte, JDK17.0.12/Python3.14.6/PySpark4.2.0/Scala2.13.18/Mongo8.3.8; webBoot4.1.1. RSS lấy mẫu1s, peak nhóm khác thời điểm không cộng thành combined, heap/availableRAM không phải usage, walljob không phải giờ-người. Dùng đúng config từng stage: preprocessingheap1280m khác model768m.

## 5. Đầu ra lần đầu — baseline để tôi duyệt

Tạo **`reports/M7A_TECHNICAL_REPORT_BASELINE.docx`** mới, cùng notes nguồn/quyết định **`reports/M7A_TECHNICAL_REPORT_NOTES.md`**. Baseline phải là tài liệu có thể mở/review, có heading/styles và bố cục thực; chưa viết các chương chi tiết hoặc tự tạo bản final.

Baseline cần thể hiện:

1. **Ranh giới và vị trí trong báo cáo nhóm:** phần tôi viết, phần ngoài scope để ghép, mapping yêu cầu B/quy cách và cấu trúc A. Không chép bìa/tên/logo/số trang mẫu thành thông tin thật. Tên chương/số thứ tự là đề xuất cần review, không cố định năm chương chỉ vì có mẫu.
2. **Mục lục đề xuất đủ rõ đến cấp mục cần thiết**, mỗi mục có mục tiêu, câu hỏi người đọc cần được giải đáp, nội dung dự kiến ngắn và bằng chứng sẽ dùng. Không dùng M0/M1/… làm chương thay cho luồng kỹ thuật; milestones là nguồn lịch sử để tổng hợp.
3. **Mạch kể xuyên suốt**: dữ liệu gốc → nhập/lưu archive → P-01/P-02 → giỏ/summaries → chia train/dev/test → catalog/train FP-Growth → luật/baseline/đánh giá → READY/publication → web → kiểm chứng/tái lập/vận hành. Phân biệt luồng tính toán batch với luồng request đọc web. Giải thích một kết quả xuất hiện ở cuối bắt nguồn từ dữ liệu và quy tắc nào ở đầu.
4. **Một sơ đồ tổng thể thực của hệ thống**, kế hoạch hình/bảng/caption (schema/keys, counts funnel, split, model/config, metrics mẫu số, UI, vận hành/resources) và nguồn thực cho từng hình/bảng. Có thể tạo sơ đồ từ mã đã kiểm; không tạo hình trang trí hoặc bịa quan sát.
5. **Danh mục bằng chứng/số liệu chuẩn**: chọn run M6 làm ví dụ triển khai/tái lập hiện tại, M3 cho freeze, M5 cho đánh giá test đầu và tích hợp; ghi rõ khi dùng run lịch sử. Mỗi bảng phải có scope/đơn vị/N và đường dẫn nguồn trong notes. Không trộn catalog train với thống kê toàn kỳ.
6. **Kế hoạch viết và QA sau duyệt**, phần còn thiếu bằng chứng/thông tin, lựa chọn cấu trúc quan trọng nếu có, và danh sách tiêu chí tôi duyệt. Nêu đề nghị cụ thể; không bắt tôi tự thiết kế từ trang trắng.

Kết thúc lượt baseline: tự review nguồn, logic trình tự, phần trùng/lệch scope, số liệu và hình thức; render/kiểm Word; gửi link baseline + tóm tắt cấu trúc/lựa chọn còn chờ. **Hỏi tôi duyệt baseline hoặc chỉ ra mục cần sửa rồi dừng.** Không coi baseline là M7A hoàn tất và không viết chi tiết trong khi chờ.

## 6. Sau khi tôi duyệt baseline — nội dung chi tiết

Chỉ thực hiện phần này sau xác nhận của tôi. Tạo **`reports/M7A_TECHNICAL_REPORT.docx`** mới, giữ baseline đã duyệt và lịch sử thay đổi. Bám baseline, chỉnh có căn cứ; đổi cấu trúc/phạm vi quan trọng phải trình lại phần ảnh hưởng.

- Viết văn xuôi khoa học, câu rõ, giải thích quan hệ nguyên nhân/kết quả, đủ chi tiết để người đọc hiểu đã làm gì, làm thế nào và vì sao có các thông số. Mỗi bước lớn nêu đầu vào → quy tắc/thuật toán áp dụng → cách cài đặt → đầu ra/counts → kiểm chứng → bước tiếp theo. Không biến báo cáo thành dán log, code dump, nhật ký các milestone hoặc danh sách file.
- Dùng ví dụ thật có lineage để giải thích duplicate/policy/giỏ, tính support/confidence/lift và masked-query metrics; phân biệt ví dụ synthetic/mẫu kiểm toán với kết quả toàn tập. Giữ công thức/mẫu số chính xác, không tạo ngưỡng đạt hoặc khẳng định business impact chưa đo.
- Mô tả Mongo nguồn/output/chín collection và khóa/run/status/active pointer/CAS theo code thực; diễn giải BSONLong/decimal, immutableREADY/retry. Mô tả Java/MVC/Thymeleaf/validation/catalog-onlyform/stale409/ranking, dashboard scope và gợi ý không fallback. Không tuyên bố kiến trúc phân tán/real-time hay HA từ Spark local.
- Bảng kết quả/biểu đồ và nhận xét dựa dữ liệu đã lưu; phân biệt dev với final và M6replication. Nêu giới hạn dataset/unknown/coverage/no-rule/single, môi trường/tài nguyên/Sparkincident/TV2assumption và ranh giới nghiệm thu; không viết bài chỉ có con số đẹp.
- Mô tả cách tái tạo/cài chạy vừa đủ và có phụ lục/tham chiếu hướng dẫn khi hợp lý. Cấu hình, phiên bản, lệnh có nguồn; dùng placeholder/path tương đối cho hướng dẫn chung, không đưa secrets, ID máy gốc hay đường dẫn cá nhân không cần thiết vào báo cáo.
- Trích dẫn nguồn dữ liệu/công nghệ thật ở nơi dùng. Không copy tài liệu ví dụ của mẫu A (PHP/React/giáo trình/nghiên cứu không dùng). Nếu phải kiểm tài liệu bên ngoài, dùng nguồn chính thức và ghi nguồn/ngày truy cập; không bịa tác giả/năm/DOI. Tài liệu dự án/receipt là bằng chứng thực nghiệm, phân biệt với tài liệu tham khảo công nghệ.

## 7. Quy cách Word và kiểm chứng

Dùng skill tài liệu phù hợp có sẵn và thông báo lần đầu áp dụng. Kiểm runtime/công cụ thật, không bịa API/lệnh hoặc tự cài phần mềm toàn máy. Bảo toàn Word nguồn; dùng mẫu A làm căn cứ styles/format, không áp template mặc định trái yêu cầu.

Các quy định đã đọc ở cuối A cần đối chiếu nguyên bản: TimesNewRoman, A4; lề trái3,5cm/phải2,5cm/trên2,5cm/dưới2,5cm; thân bài13pt/canhđều/giãn1,3/trước-sau6pt; chương18pt/inhoa/đậm/canhgiữa; mục1.1 là14pt/inhoa/đậm, mục sâu13pt/đậm. Caption hình dưới/bảng trên, đánh số theo chương; bảng12pt/giãn1,3/trước-sau0pt/lặp header. Heading/TOC/caption/field/số trang thực, không gõ mục lục hoặc số trang giả từ mẫu. Phần kỹ thuật chưa có frontmatter thì ghi cách ghép/đánh số dự kiến trong baseline, không tự thêm lời cảm ơn cho đủ số La Mã.

**Render → xem ảnh từng trang → sửa → render lại** cho baseline và bản chi tiết. Kiểm dấu tiếng Việt, font, tràn/lệch bảng, caption/sơ đồ/ảnh, khoảng trắng, ngắt trang, TOC/heading/page numbers và nguồn. Trích XML/text chỉ kiểm nội dung, không thay QA hình thức. Nếu không render/cập nhật field được với công cụ hiện có, ghi đúng giới hạn; hoàn thành phần độc lập, trình phương án cần thiết trước thay công cụ, không báo Word đã đạt kiểm trực quan. Không dựa file tồn tại hoặc script exit0 để nghiệm thu.

Kiểm bảng số liệu/công thức/N/rounding với receipts; kiểm links/ảnh có nguồn và provenance, bản gốc không đổi/hash, diff/ignore. Không rerun scientific experiment để chứng minh bản Word. Runtime render/outputQA theo `.gitignore`/dung lượng; không tự sửa ignore để giấu deliverable Word mới.

## 8. Nghiệm thu và bàn giao

- **Checkpoint baseline:** có DOCX baseline thật, mapping nguồn/phạm vi/outline/luồng/hình-bảng/bằng chứng/QA và review tự kiểm; **chờ tôi duyệt**, chưa đóng M7A.
- **M7A hoàn tất sau duyệt và viết chi tiết:** Word kỹ thuật bám baseline và dữ liệu M0–M6; đọc liền hiểu đầu vào/biến đổi/đầu ra/tạo số liệu; đủ sources/QA/giới hạn; tôi review nội dung được giao và chấp thuận. Phần ngoài phạm vi để ghép được đánh dấu, không tuyên bố toàn bộ M7/báo cáo nhóm đã đủ.
- Cập nhật notes/STATE/checklist/decisions theo bằng chứng và lời người thật, không sửa receipt cũ. Nêu file đầu ra, kiểm chứng, điều chưa kiểm và phần cần bổ sung, rồi dừng tại checkpoint baseline hoặc M7A được giao.
- **Không slide/M7B, dry-run nộp, Classroom/M8, commit/push, tune/refit hoặc thay runtime để làm đẹp báo cáo.**
