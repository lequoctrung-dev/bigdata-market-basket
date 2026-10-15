# Milestone Checklist — Master Plan

Ngày **15/10/2026**. Theo [Master Plan](13_MASTER_IMPLEMENTATION_PLAN.md). **M0/M1/M2/M3 đã đóng.** M3 theo development/freeze/postcheck TV1 và TV2 review split/tính lại mẫu metrics chấp thuận theo U-41; [M3 notes](../reports/M3_MODEL_DEVELOPMENT_NOTES.md) và receipt cuối file giữ evidence. Test cuối NOT_RUN, chưa M4/M5; full run hai máy M6 giữ nguyên. Các receipt M0/M1/M2 bên dưới giữ lịch sử.

**Workspace/Agent:** đã chuẩn bị repository cục bộ và tài liệu điều phối trước M0 theo yêu cầu ngày 14/10/2026; xem [STATE](../STATE.md). Đây không phải nghiệm thu M0 hoặc kiểm chứng môi trường runtime M1.

## Trước khi bắt đầu

- [x] QD-01: U-20 chốt hướng batch/MongoDB nguồn/phân tích unique/web đầu ra hoàn chỉnh; field/config cần kiểm chứng, chưa schema/runtime.
- [x] QD-04/QD-03: U-23 đổi vai trò (bạn data/Spark, người kia Java/web); U-22 yêu cầu full run cả hai máy.
- [x] QD-05: U-25 người dùng xác nhận GV chấp thuận Online Retail II; không xin duyệt lại.
- [x] QD-02: U-21 loại TEST001/TEST002 khỏi khai phá/gợi ý; giữ nguồn.
- [x] QD-06: U-26 người dùng xác nhận khung B + quy cách trình bày A, không tự bắt 5 chương/trang bổ sung/in.
- [ ] Khi có thông tin mới QD-07/QD-09, cập nhật deadline, giờ từng người, lịch bận, quy cách nộp/demo. Hiện vẫn “chưa rõ”; không bắt trả lời lại để bản kế hoạch có thể tồn tại.

## Các mốc và tiêu chí đóng

| Mốc | Task theo Master Plan | Kiểm tra để đóng | Deliverable phải có | Trạng thái/evidence |
| --- | --- | --- | --- | --- |
| [x] M0 — Chốt phạm vi làm việc và hợp đồng dữ liệu | M0-T1, M0-T2, M0-T3, M0-T4 | M0-AC1/AC2/AC3 + DoD ở file 13 | Thiết kế/contract được review, roles và decision log | Đóng ngày 14/10/2026 về tài liệu; contract m0-contract-v1 ở file 11/12, lựa chọn U-27–U-29, review TV1/TV2 theo xác nhận U-30; không runtime PASS |
| [x] M1 — Học Spark cần dùng và kiểm chứng luồng mẫu | M1-T1, M1-T2, M1-T3, M1-T4 | M1-AC1/AC2/AC3 + DoD ở file 13 | Prototype/receipt TV1 thật, hướng dẫn và review; miễn receipt TV2 riêng theo U-33 | Đóng 15/10/2026: kỹ thuật mẫu TV1 PASS, demo/học/giải thích/review chấp thuận theo U-35; AC/DoD theo tiêu chí điều chỉnh U-33; không phải TV2 runtime PASS |
| [x] M2 — Xây pipeline dữ liệu và kiểm chứng P-01/P-02 trên nguồn đầy đủ | M2-T1, M2-T2, M2-T3, M2-T4 | M2-AC1/AC2/AC3 + DoD ở file 13 | Pipeline/full-source counts/basket set và xác nhận dataset | Đóng 15/10: kỹ thuật TV1 PASS, run d7fb3f21-115f-4793-a5fe-5c40b6da64cd/postcheck đạt; TV2 review/chấp thuận không còn điểm sửa theo U-38 |
| [x] M3 — FP-Growth, baseline và đánh giá trên phần phát triển | M3-T1, M3-T2, M3-T3, M3-T4 | M3-AC1/AC2/AC3 + DoD ở file 13 | Kết quả development, eval harness và config freeze | Đóng 15/10: full-train/dev/freeze/postcheck TV1, 17 Python/6 Java tests, parity 4.293 query đạt; TV2 review split/tính lại mẫu metrics chấp thuận U-41; xem M3 notes/receipt cuối file |
| [ ] M4 — Website phân tích và gợi ý theo giỏ | M4-T1, M4-T2, M4-T3, M4-T4 | M4-AC1/AC2/AC3 + DoD ở file 13 | Website dùng run thật, UI/query/ranking cases | Chưa thực hiện; chưa có evidence nghiệm thu |
| [ ] M5 — Tích hợp, công bố an toàn và đánh giá cuối | M5-T1, M5-T2, M5-T3, M5-T4 | M5-AC1/AC2/AC3 + DoD ở file 13 | Run integrated/final metrics và lỗi đã xử lý | Chưa thực hiện; chưa có evidence nghiệm thu |
| [ ] M6 — Full run và demo trên cả hai máy | M6-T1, M6-T2, M6-T3, M6-T4 | M6-AC1/AC2/AC3 + DoD ở file 13 | Hai receipt FULL_RUN thật và web demo từng máy, hướng dẫn chạy chéo | Chưa thực hiện; chưa có evidence nghiệm thu |
| [ ] M7 — Hoàn thiện báo cáo, slide và thử quy trình nộp | M7-T1, M7-T2, M7-T3, M7-T4 | M7-AC1/AC2/AC3 + DoD ở file 13 | Word/PPT/source/data-link/hướng dẫn/đóng góp + dry-run | Chưa thực hiện; chưa có evidence nghiệm thu |
| [ ] M8 — Nộp chính thức, thuyết trình và phản biện | M8-T1, M8-T2, M8-T3, M8-T4 | M8-AC1/AC2/AC3 + DoD ở file 13 | Receipt Classroom + buổi demo/thuyết trình/Q&A thật | Chưa thực hiện; chưa có evidence nghiệm thu |

## Không nhầm minh chứng

- [ ] M1/EXP mẫu không thay full run M2/M3/M5.
- [ ] Audit Python đã có không được đổi nhãn thành pipeline Spark đã chạy.
- [ ] B-D11 kiểm tra thiếu; B-D12 khử trùng; B-D13 ngoại lệ — không đảo ID khi ghi evidence.
- [ ] P-01 trước lọc khác đối chiếu 1.067.371 − 34.335 = 1.033.036 trên hash nguồn hiện có.
- [ ] Count sau P-02 dùng policy/mapping/TEST đã chốt; không ép số ứng viên cũ thành target.
- [ ] Final eval sau freeze; không coi FP-Growth phải vượt baseline là AC.
- [ ] Gợi ý tiền đề phải đủ, loại item đã có, khử trùng/ranking consistent; không fallback mặc định.
- [ ] Result/page/form cùng run/version; job lỗi không làm web đọc phần ghi dở.
- [ ] Cả hai có receipt FULL_RUN toàn nguồn theo U-22; sample/imported output không thay nghiệm thu, không suy PASS máy này sang máy kia.
- [ ] Lịch/đóng góp ghi việc thật, không dùng ước lượng hoặc tự đặt 50/50.
- [ ] M7 dry-run không thay nộp Classroom hoặc thuyết trình thật M8.
- [ ] Nguồn/điểm/điều kiện của A/B giữ đúng; conditional không biến thành nghĩa vụ tự thêm.

## Trường cần cập nhật khi triển khai

| Trường | Giá trị hiện tại |
| --- | --- |
| Hạn nộp / ngày demo | Chưa rõ — U-19 |
| Giờ/tuần TV1 / TV2 và lịch bận | Chưa rõ — U-19 |
| Vai trò được nhận | TV1/bạn data/Spark/FP-Growth/đánh giá; TV2 Java/web/tích hợp — U-23 |
| Chế độ demo từng máy | **Cả hai tự full run** toàn nguồn, fit train và đánh giá theo cấu hình freeze rồi demo; import output không thay — U-22 |
| Cấu hình hai máy và bộ phiên bản | TV1 đã quan sát Windows 11 x64/i5-13500H/RAM 15,63 GiB, bộ phiên bản và sample receipts ở STATE/guide. TV2 vẫn chỉ thông tin U-24, chưa kiểm tra hoặc runtime |
| Milestone đang triển khai | M3 đã đóng theo runtime/freeze/U-41; bàn giao rồi dừng trước M4/M5, test cuối NOT_RUN |
| Tổng effort cơ sở / gồm dự phòng | 196–296 / khoảng 236–356 giờ-người; tăng M6 vì full run hai máy; chưa đo velocity |
| Calendar 7 tuần | Khung tham chiếu, chưa có ngày/giờ đã xác nhận |
| Ngày hoàn tất/evidence theo mốc | M0: 14/10/2026. M1/M2/M3: 15/10, receipts/U-35/U-38/U-41. M3 development có freeze/postcheck; M4–M8 chưa nghiệm thu |

Khi đóng mốc, ghi ngày thật, người thực hiện/review, source/run/config và đường dẫn evidence; chỉ tick sau khi AC/DoD được kiểm chứng. Nộp/live demo còn cần lịch và sự thực hiện thật.


## Việc kế tiếp — chỉ đọc phần này nếu cần thao tác

**M0/M1/M2/M3 đã đóng theo các receipt và U-35/U-38/U-41.** Bàn giao M3 rồi dừng trước M4/M5; test cuối NOT_RUN. Phần hướng dẫn M0/M1 bên dưới giữ lịch sử đọc/tái tạo, không phải việc đang chờ. Các phần M0 đã có căn cứ:

- [x] Agent đã đối chiếu tài liệu M0-T1/T3/T4 ngày 14/10: scope/truy vết/mapping TEST/xác nhận học thuật/roles/full run được ghi tại file 11 mục 8, file 13 phần review M0 và file 07. Đây chỉ là hoàn thành đối chiếu tài liệu của Agent, không thay thành viên review hoặc counts mới.
- [x] Agent đã bổ sung M0-T2: file 11 mục 8–10 và file 12 mục 9–13 nêu input/output/khóa/kiểu/manifest/công bố/lỗi/KPI và giả định M1; TV1/TV2 chấp thuận bản hiện tại theo U-30, không suy từ sự tồn tại tài liệu.
- [x] Người dùng đã chọn M0-D1/M0-D2/M0-D3 ngày 14/10; ghi U-27–U-29 ở file 07, cập nhật kết luận trong file 11/12 theo câu trả lời thật.
- [x] TV1/TV2 đã review, chấp thuận bản hiện tại theo câu trả lời U-30, ghi nhận 14/10/2026. Giả định cần thử ở M1 giữ trong file 12 mục 13. Review tài liệu không phải runtime PASS.
- [x] M0 đủ AC/DoD và được tick ngày 14/10/2026 theo receipt bên dưới. QD-07 lịch vẫn mở; không cam kết kịp hạn.

**Sau khi M0 được đóng và được giao thực hiện M1:**
1. Ghi CPU/kiến trúc Windows và bản Java/Python/MongoDB/Maven hiện có trên từng máy; không tự kết luận 16 GB/50 GB đủ cho fit.
2. Nhóm chốt bộ phiên bản để thử từ tài liệu chính thức.
3. Chạy luồng mẫu MongoDB → PySpark/FP-Growth → MongoDB → MVC/Thymeleaf, mỗi máy có receipt riêng.
4. Sau M1 mới mở pipeline toàn nguồn và full run từng máy theo milestones; không lấy mẫu PASS thay full run.

Không cần hỏi lại dataset, hướng báo cáo, TEST, vai trò hoặc chế độ hai máy. Deadline/giờ tuần vẫn chưa rõ, không chặn chuẩn bị kỹ thuật; CPU có thể kiểm tra trực tiếp ở máy được truy cập.

## Receipt review M0 — bản tài liệu ngày 14/10/2026

| Tiêu chí | Đối chiếu tài liệu hiện tại của Agent | Trạng thái nghiệm thu |
| --- | --- | --- |
| [x] M0-AC1 | File 11 giữ U-16/P-01, U-17/U-21/P-02, U-18/P-03; scope batch/web không thêm tính năng ngoài đề tài. | Đạt về review tài liệu ngày 14/10; Agent đối chiếu văn bản, TV1/TV2 chấp thuận theo U-30. |
| [x] M0-AC2 | File 11 mục 8–10 và file 12 mục 9–12 cụ thể hóa input/output/tiền/ngày/ID/writer/web; người dùng đã chọn các phương án lớn U-27–U-29. | Đạt về tài liệu: lựa chọn có kết luận, TV1/TV2 chấp thuận contract theo U-30; version m0-contract-v1. Round-trip/runtime còn chờ mốc triển khai. |
| [x] M0-AC3 | File 07/file 13 giữ U-25/U-26 theo người dùng; lịch/CPU/phiên bản/runtime chưa rõ hoặc chưa thử; không cam kết kịp hạn. | Đạt về cách ghi nguồn/giới hạn; review chấp thuận U-30. Không phải xác nhận GV độc lập hoặc runtime PASS. |
| [x] DoD | QD-01–QD-06 và M0-D1/D2/D3 đã chốt theo U; contract được hai người chấp thuận; QD-07 vẫn mở. | Đạt: người dùng xác nhận review cả TV1/TV2 theo U-30, ghi nhận 14/10/2026. Không cần runtime PASS để đóng review M0. |

| Người review | Phạm vi review được nêu trong câu hỏi | Ngày ghi nhận/kết luận |
| --- | --- | --- |
| TV1/người dùng, phía data | File 11 mục 8–10: tập dữ liệu/mapping/KPI/đánh giá; file 12 mục 10–11: nguồn/kiểu/khóa/counts/split, manifest. Kiểm tra U-16–U-18/U-21 không bị thay nghĩa. | Ghi nhận 14/10/2026: **đã review, chấp thuận bản hiện tại** theo U-30. Không có điểm sửa được báo trong câu trả lời. |
| TV2, phía Java/web | File 12 mục 9–12: collection/kiểu/output/pointer/lỗi/ranking; file 11 mục 9: ba khu vực và mẫu số, cùng run/version. Kiểm tra có thể triển khai từ contract và nêu điểm cần sửa. | Ghi nhận 14/10/2026: **đã review, chấp thuận bản hiện tại** theo xác nhận người dùng U-30; chưa nhận một thông báo độc lập trực tiếp từ TV2. |

**Nguồn receipt:** câu hỏi đã nêu bản ngày 14/10, phần cần đọc theo vai trò và yêu cầu chưa đọc thì không xác nhận; người dùng trả lời nguyên văn **“Cả hai đã review, chấp thuận bản hiện tại”**. Ngày trên là ngày ghi nhận xác nhận, không tự gán giờ hoặc ngày review riêng của từng người. Đây là review được người dùng báo lại, không thay bằng kiểm tra Agent hoặc suy từ lựa chọn M0-D. Sau xác nhận chỉ cập nhật trạng thái/receipt/version tài liệu, không đổi các điều khoản kỹ thuật đã được chấp thuận.

### Kiểm chứng tài liệu của Agent ngày 14/10/2026

- Đọc prompt đính kèm và AGENTS/README/STATE; đọc đầy đủ file 07/11/12/14, phần M0/quy tắc chung/cổng/dependency/quyết định/bàn giao của file 13. Đối chiếu các phần liên quan trong RTM/report/deliverables/ambiguity/profile/map và nghiên cứu kỹ thuật. Dùng Source Audit/audit policy có sẵn; không đọc lại toàn bộ hai Word bằng render hoặc chạy khảo sát toàn dataset trong M0.
- Kiểm tra Git branch/status/diff/log/remote bằng thao tác đọc: `main`, HEAD `760cf88`, origin như README/STATE. Hai thay đổi có sẵn ở README/STATE về Git/remote được giữ nội dung. Không suy trạng thái GitHub hoặc clone máy thứ hai.
- RTM và map vẫn cùng 282 ID duy nhất; đối chiếu 25 ID nguồn được liệt kê cho M0-T1–T4 (B-G01–G07, B-S01–S07, B-T01–T06, B-P06–P08, B-O07–O08). Đây là kiểm tra truy vết, không PASS các nghĩa vụ học thuật/runtime tương ứng.
- 26 dòng xác nhận U cũ không đổi; U-27–U-29 khớp ba câu trả lời hiện tại. Kiểm tra các liên kết/anchor nội bộ, tham chiếu U và diff văn bản; `git diff --check` không báo lỗi whitespace.
- Đối chiếu SHA-256 trước/sau của 49 file được bảo vệ, gồm hai Word, XLSX/ZIP, RTM/checklist báo cáo/đầu ra, Source Audit/Source Extract, toàn bộ file evidence và quy tắc Agent/Git: không đổi; hash XLSX khớp file 10. Không chỉnh ID/trọng số/câu nguồn, dữ liệu thô hoặc audit lịch sử.
- Tra cứu tài liệu chính thức MongoDB atomicity, Spring Data mapping và Spark DecimalType để đối chiếu contract; dẫn nguồn trong file 12. Không chọn/cài bộ phiên bản hoặc suy kết nối/round-trip đã chạy từ tài liệu.
- Sau câu trả lời review U-30, kiểm tra lại khi đóng: 30 xác nhận U, 199 liên kết nội bộ/146 anchor hợp lệ, RTM/map vẫn khớp 282 ID và 49 hash bảo vệ không đổi. M0-AC1/AC2/AC3/DoD và chỉ milestone M0 được tick; M1–M8 giữ chưa thực hiện. `git diff --check` đạt; không có file staged hoặc commit/push của Agent.

**Giới hạn kiểm chứng:** không Spark/FP-Growth/MongoDB/Spring Boot runtime, không counts mới sau TEST, không số đo hiệu năng/tài nguyên hoặc minh chứng máy thứ hai; Agent không thay review thành viên. Cổng review M0 đã đạt theo U-30; chưa thực hiện M1 vì chưa có giao việc M1. Deadline/giờ tuần vẫn chưa rõ, không cam kết kịp hạn.

## Receipt M1 ngày 14/10/2026 — snapshot trước điều chỉnh U-33/U-34

Phần giới hạn M0 phía trên là snapshot lúc đóng M0; M1 đã được giao sau đó. [M1 Guide](../pipeline/README.md) giữ thao tác/kiến thức/đáp án; STATE giữ trạng thái ngắn. Không lấy receipt Agent chạy trên TV1 thay xác nhận hai thành viên đã học hoặc review.

| Task/tiêu chí | Bằng chứng hiện có | Kết luận hiện tại |
| --- | --- | --- |
| M1-T1 — kiến thức và giải thích | Guide phần 3 giải thích driver/partition/action/shuffle/schema/window và 5 giỏ/support/confidence/lift. | Đã chuẩn bị bài học/đáp án; **chưa xác nhận TV1/TV2 đã đọc và giải thích cho nhau**. |
| M1-T2 — bộ phiên bản | TV1 `environment.json`, dependency đã pin, Maven SHA-512 chính thức được đối chiếu; Spark/connector/Java/web thật đã thử. | Chỉ máy TV1 đã kiểm chứng; TV2 cần preflight/setup riêng. Không nâng cấp/cài phần mềm toàn máy trong lần này. |
| M1-T3 / M1-AC1 phía batch | 7 checks PASS: source retry/xung đột, P-01 đầu theo lineage, FP-Growth theo đáp án độc lập, connector retry, tiền exact, round-trip, publication/CAS/FAILED guard. | TV1 mẫu PASS; **chưa tick AC1 toàn mốc** vì TV2 và review còn chờ. |
| M1-T4 / M1-AC1 phía Java/web | 18 checks PASS: ID/null/array/empty array/int64/BigDecimal/ngày local, Python–Java ranking, nhãn SAMPLE/escape/form version, query thật/chọn trùng/giỏ rỗng/mã lạ/không fallback/form cũ. | TV1 HTTP MVC/Thymeleaf thật PASS; chưa có xác nhận demo/review người thật hoặc máy TV2. |
| M1-AC2 | Spark mẫu thực đọc/ghi MongoDB; 7 itemsets/9 rules khớp enumeration 5 giỏ. Web chỉ đọc/apply luật, không gọi Python/fit trong HTTP. | Đã kiểm tra tự động TV1; chưa nghiệm thu thay nhóm. |
| M1-AC3 | Chỉ có bộ receipt TV1. | **Chưa đạt**, TV2 chạy sau theo U-31; không lấy output import/receipt TV1 thay. |
| M1 DoD | Code/prototype, bộ phiên bản thử trên TV1, hướng dẫn người còn lại và lỗi/giới hạn đã ghi. | **Chưa đạt toàn mốc:** chờ TV2 chạy hướng dẫn và review, cùng xác nhận học/giải thích. M1 giữ chưa tick. |

### Evidence đúng lượt TV1

- Run cuối: `1b156c53-7c15-4a9e-a479-32b7ab3926f5`, publication version **3**, schema `m0-contract-v1`, `mode=SAMPLE`, `dataset_kind=SYNTHETIC`, final evaluation `NOT_RUN`.
- Batch: [receipt riêng theo run](../artifacts/m1/TV1/pipeline-receipt-1b156c53-7c15-4a9e-a479-32b7ab3926f5.json); Java/web: [receipt riêng lần kiểm tra](../artifacts/m1/TV1/web-receipt-8c0dff59-4d3e-404a-b084-073342db4532.json); môi trường: [environment](../artifacts/m1/TV1/environment.json); stop/lỗi DB: [lifecycle](../artifacts/m1/TV1/lifecycle-receipt.json).
- Các file runtime ở artifacts bị loại khỏi Git, chỉ có trên máy đã chạy; clone/TV2 không mặc nhiên có các link evidence cục bộ này. Giữ run/status/hash trong kết luận để truy vết; hướng dẫn đủ để TV2 tạo receipt của mình.
- Fixture: 22 raw, P-01 giữ 20, mua dương/hợp lệ 17, hàng hóa 12, 5 giỏ, 7 itemsets/9 rules; tổng Quantity 13, giá trị mua dương **16,04938257 GBP**. Đây là số mẫu có đáp án, không counts Online Retail II.
- 4 Python unit tests/4 Java unit tests đạt; build Maven/`pip check` đạt. 7+18 runtime checks được chạy thật, không suy từ unit/build hoặc trang tĩnh.
- MongoDB/web mẫu đã dừng theo receipt, 27018/8081 không nghe, 27017 vẫn nghe; dữ liệu giữ nguyên. HTTP khi MongoDB mẫu dừng hiển thị lỗi kết nối an toàn. Không drop/reset/commit/push.

### Lỗi đã xử lý và giới hạn còn lại

| Quan sát | Nguyên nhân/sửa và kiểm chứng |
| --- | --- |
| Import FP-Growth thiếu NumPy | Khai báo `pyspark[ml]` và pin NumPy theo metadata; import/runtime/pip check qua. Không đổi Python toàn máy. |
| Spark startup gọi winutils khi phân phối JAR | Trace addFile/fetchFile/chmod; resolve/copy 5 JAR chính thức và dùng classpath local trước gateway launch. Luồng local[2] qua thực tế; không patch quyền/Spark, không tải winutils/DLL không rõ nguồn. |
| Tổng tiền không exact | `(20,0) × (20,8)` tạo `(38,6)` đã tái hiện; chọn Quantity `(10,0)` có check miền cho mẫu, giá `(20,8)`, product `(31,8)`, sum exact. Không đổi đáp án/làm tròn để vượt test. Range/scale toàn nguồn còn M2. |
| Spark LongType từ chối bson.Int64 | Dùng Python int khi tạo DataFrame LongType; dùng Int64 ở ghi PyMongo trực tiếp. Java xác nhận BSON long; không tắt verifySchema hoặc đổi counts thành double. |
| PowerShell 5.1 không chạy helper | Execution policy chặn; TV1 chạy PowerShell 7.6.5 môi trường Codex. Không Bypass/đổi policy toàn máy; shell/quyền của TV2 chưa biết, phải kiểm tra trước setup. |
| Warning native Hadoop/case-insensitive options | Vẫn hiện ở bản native đã thử; sample PASS không chứng minh mọi filesystem/full-source operation chạy được. Chẩn đoán ở bước có lỗi, không đổi môi trường âm thầm. |

**Đối chiếu cuối của Agent ngày 14/10:** 49 SHA-256 bảo vệ nguồn/audit/quy tắc không đổi; RTM/map cùng 282 ID duy nhất; U-01–U-30 giữ nguyên, thêm đúng U-31/U-32. 58 liên kết file nội bộ trong bảy tài liệu bàn giao hợp lệ. Hash hai file Python/năm JAR connector/JAR web và hash fixture khớp receipt; batch/web cùng run/version, bản receipt riêng khớp alias hiện tại. `git diff --check` đạt, không file staged; venv/cache/build/runtime evidence được Git bỏ qua. Chỉ M0 được tick. Đây là kiểm tra tính nhất quán bàn giao, không thêm nghiệm thu TV2 hoặc review thành viên.

### Điều chỉnh và chuẩn bị thực hành ngày 15/10/2026 — snapshot trước U-35

- **U-33:** miễn receipt TV2 riêng tại M1, dùng receipt TV1 thật. Điều chỉnh M1-AC3 và yêu cầu lặp lại trên máy kia của T2/T4; các câu chờ TV2 trong receipt/snapshot 14/10 phía trên được thay bởi ngoại lệ này. TV2 vẫn chưa được kiểm chứng; full run hai máy M6 theo U-15/U-22 giữ nguyên.
- **U-34:** người dùng xác nhận chưa hoàn tất học/giải thích/review, cần hướng dẫn/demo; không miễn M1-T1/review. Vì thế M1 vẫn chưa tick dù phần kỹ thuật và ngoại lệ AC3 đã đủ căn cứ.
- Bổ sung [bài thực hành mục 5](../pipeline/README.md#5-bài-thực-hành-họcreview-m1): xem luồng, bốn ca giỏ, tính tay support/confidence/lift, đọc đoạn Spark/Java và giải thích chéo. Không tạo bài thi/ngưỡng đạt mới.
- Demo TV1 đã mở lại qua launcher: MongoDB riêng 27018/web 8081, giữ dữ liệu. Đọc Java round-trip và POST bốn ca form ngày 15/10 đều đúng cùng run `1b156c53-7c15-4a9e-a479-32b7ab3926f5`, version 3; [receipt sẵn sàng demo](../artifacts/m1/TV1/demo-ready-2026-10-15.json). Không chạy lại batch/build, không ghi đây là thành viên đã xem demo.
- Process mẫu đang chạy phục vụ thực hành khi bàn giao 15/10; receipt stop 14/10 là lịch sử. Dùng StopWeb/StopMongo theo guide khi xong; không drop/reset/commit/push.
- Đối chiếu tài liệu 15/10: 34 dòng U, U-01–U-30 không đổi so với HEAD; 65 liên kết file nội bộ hợp lệ, 49 hash bảo vệ/282 ID và code/JAR/fixture khớp receipt cũ. `git diff --check` đạt, không staged; chỉ M0 tick. Không sửa mã ứng dụng hoặc chạy lại batch để chuẩn bị bài thực hành.

### Receipt đóng M1 ngày 15/10/2026

U-35 ghi hai câu trả lời thực tế: người dùng đã demo xong; cả hai đã học, giải thích và review, chấp thuận M1, không còn điểm sửa. Đây là xác nhận qua người dùng, không phải Agent trực tiếp quan sát việc học từng người hoặc nhận thông báo riêng TV2. Thay trạng thái học/review còn chờ của U-34 và các snapshot phía trên; không suy giờ hoặc phần trăm đóng góp.

| Điều kiện | Căn cứ nghiệm thu | Kết luận |
| --- | --- | --- |
| [x] M1-T1 / học và review | Bài thực hành/đáp án M1 Guide; xác nhận U-35 cho cả hai thành viên sau demo. | Hoàn tất theo xác nhận người dùng; không có điểm sửa được báo. |
| [x] M1-AC1 | 7 batch/18 web checks TV1, trong đó connector thực đọc/ghi MongoDB và Java đọc ID/null/array/int64/tiền/ngày; cùng run/version. | Đạt trên mẫu TV1, không khẳng định toàn nguồn hoặc runtime TV2. |
| [x] M1-AC2 | FP-Growth thực chạy, 7 itemsets/9 rules khớp đáp án độc lập 5 giỏ; web chỉ áp luật đã lưu; code/ranking tests và review U-35. | Đạt mẫu; HTTP không fit Spark. |
| [x] M1-AC3 điều chỉnh | U-33 miễn receipt TV2 riêng M1; nghiệm thu bằng receipt TV1 thật, đã ghi TV2 chưa kiểm chứng. | Đủ theo ngoại lệ được người dùng chấp thuận; yêu cầu full run hai máy M6 giữ nguyên. |
| [x] M1 DoD | Bộ phiên bản đã thử trên TV1, source/hướng dẫn tái tạo/kiến thức/đáp án/lỗi/giới hạn đã ghi; học/demo/review U-35, không còn điểm sửa. | Đạt theo phạm vi U-33; M1 được tick ngày 15/10/2026. |

Sau demo đã StopWeb và shutdown MongoDB mẫu đúng receipt. [Receipt dừng ngày 15/10](../artifacts/m1/TV1/lifecycle-stop-2026-10-15.json) xác nhận hai PID dừng, cổng 27018/8081 đóng, 27017 vẫn nghe, file WiredTiger giữ nguyên. Receipt demo-ready phía trên là snapshot khi đang chạy; không dùng làm trạng thái hiện tại. Không drop/reset hoặc chạy lại batch/build; không commit/push.

Kiểm tra khi đóng: 35 dòng U, U-01–U-30 giữ nguyên so với HEAD; 49 hash bảo vệ không đổi, RTM/map cùng 282 ID, 64 liên kết file nội bộ hợp lệ. Hash code/JAR/fixture và run/version khớp receipt mẫu; `git diff --check` đạt, không staged. Chỉ M0/M1 được tick; không chạy lại runtime/test ứng dụng vì lần đóng này chỉ sửa hồ sơ nghiệm thu và dừng process sau demo.

**Bàn giao:** M1 đã đóng; M2–M8 chưa mở. TV2 runtime, full-source counts/range/scale/tài nguyên và full run vẫn chưa được mẫu M1 chứng minh. Agent dừng, chỉ triển khai M2 khi được giao.

## Receipt đóng M2 ngày 15/10/2026

M2 được giao sau snapshot M1 trên. U-37 chọn namespace riêng 27019 / `bigdata_m2`. [M2 notes](../reports/M2_DATA_PREPROCESSING_NOTES.md) giữ nguồn/DOI/giấy phép, cấu hình, code/hash, counts/lineage, tài nguyên theo bước, lỗi/cách sửa, lệnh tái tạo và giới hạn. [Pipeline Guide mục 6](../pipeline/README.md) hướng dẫn chạy.

| Tiêu chí | Bằng chứng thực tế | Trạng thái |
| --- | --- | --- |
| M2-T1 / nguồn | Hash/header/hai sheet đúng, nhập 525.461 + 541.910 = 1.067.371 dòng. Mongo READY sau đủ count. Partial bị chặn; retry 2.000 dòng thật không nhân bản; xung đột bị từ chối. | Kỹ thuật đạt TV1; không gọi probe là full READY re-import workbook |
| M2-AC1 / P-01 | Spark 1.067.371 − 34.335 = 1.033.036; checksum toàn bộ vị trí đầu khớp audit SQLite. 8/13 partition + DB đọc đảo chiều cùng kết quả; fixture bảo toàn dòng khác Quantity/Price, kiểu/text/null/whitespace/case/ngày. | Kỹ thuật đạt |
| M2-AC2 / mapping | Mapping U-17/U-21 có hash, TEST001/TEST002 bị loại; giữ mã chữ và 226.761 dòng hàng thiếu khách. Trim collision 47503J tại sheet 0/row 260888 cùng mô tả, giữ raw trước P-01. | Đạt; TV2 chấp thuận theo U-38 |
| M2-AC3 / giỏ/summaries | 1.007.913 positive_valid − 4.556 P-02/TEST = 1.003.357 dòng hàng; 39.516 giỏ, 4.895 item, 5.347 summaries. Mọi item/month, GBP exact 19.643.861,637 và checksum giỏ khớp audit; ba hóa đơn archive tính riêng khớp. Giỏ 1 item giữ, max 1.108 không cắt. | Kỹ thuật đạt |
| Kiểu/output/tài nguyên | Quantity (5,0), Price (8,3), product (14,3), sum (24,3); Mongo decimal text và BSON Int64 thật. File 1.033.036 dòng/413.222.079 byte đọc lại hash/count đạt. 10 tests Python đạt; Spark wall 301,032 giây, sampled RSS Python 195,27/JVM 1.717,21/Mongo 377,06/combined 2.272,68 MiB. | Kỹ thuật đạt; không suy FP-Growth/hai máy PASS |
| DoD | U-25 có sẵn, nguồn/hash bảo toàn, lineage/counts/hướng dẫn rõ; **TV2 review/chấp thuận, không còn điểm sửa theo xác nhận người dùng U-38**. | **Đạt — đóng M2 15/10/2026** |

Run cuối **`d7fb3f21-115f-4793-a5fe-5c40b6da64cd`**, basket set **`cae0d9e763ef38a086966d829fdeba9272f4d7fda7b61791bee9e9ba04b3287a`**, parser `openpyxl-3.1.5-typed-v1`, schema `m0-contract-v1`, storage `m2-bson-counts-int64-v1`, policy `p01-first-p02-test-v1`. HEAD `d975e6c`, hash mã chưa commit trong receipt. Run Mongo VALIDATED/basket set READY là checkpoint PREPROCESSING; không tạo model, metrics, catalog train hay active publication.

Evidence ngoài Git: [receipt cuối](../artifacts/m2/pipeline-d7fb3f21-115f-4793-a5fe-5c40b6da64cd.json), [postcheck cuối](../artifacts/m2/final-verification-d7fb3f21-115f-4793-a5fe-5c40b6da64cd.json), [resources từng bước](../artifacts/m2/resources-d7fb3f21-115f-4793-a5fe-5c40b6da64cd.json), `audit-source-v1/`, `hand-invoices.json`, `mongo-verification-*.json`, `unit-final-20261015T082201.*` và retained-lines dưới data/processed/m2. Clone không có artifacts không đồng nghĩa chưa từng chạy.

Lượt lỗi `34f6dd24...` FAILED khi key phân phối BSON là int; cảnh báo heap có thật đã được Spark phục hồi. Lượt `7ea685bc...` PASS các checks lúc đó nhưng bị postcheck đánh dấu FAILED do BSON int32; giữ receipt/output cũ, không dùng nghiệm thu. Lượt cuối sửa string key/Int64, giảm distinct aggregate, heap 1280m/16 partition/AQE coalesce off, không còn OOM trong log. Không sửa audit cũ, expectation hoặc counts để pass.

Người dùng trả lời **“TV2 đã review và chấp thuận, không còn điểm sửa”** sau câu hỏi chỉ rõ M2 notes, Pipeline Guide mục 6, checkpoint này và run cuối; ghi U-38. Đây là xác nhận review được người dùng báo lại, không phải Agent thay TV2 hoặc thông báo riêng trực tiếp TV2. **M2 đủ AC/DoD, đã đóng**; dừng trước M3/M4, không commit/push. Runtime web/Java toàn nguồn, full READY re-import và full run máy TV2 chưa kiểm chứng. Các receipt runtime ghi PENDING_TV2 là snapshot trước U-38, giữ bất biến; xác nhận mới ghi trong hồ sơ/review receipt riêng.

Lifecycle cuối: `artifacts/m2/stop-20261015T084344.json` STOPPED, dữ liệu giữ/listener 27019 = 0; preflight cuối 084347 chỉ 27017/PID 5572 nghe, mẫu 27018/web 8081 đóng. Đối chiếu 50 file bảo vệ không đổi và RTM/map 282 ID; artifacts/processed/DB/scratch/.venv bị Git ignore. Không staged/commit/push.

### Bàn giao sang thread M3 theo U-39 — 15/10/2026

M2 đã hoàn thành, không còn confirm/demo riêng để đóng mốc. Đã tạo [M3 Start Prompt](M3_START_PROMPT.md) với trạng thái/source/code/IDs M2, scope M3-T1–T4, P-03/QD-08, chống leakage, freeze trước final và yêu cầu review M3 riêng. Khi thực hiện, ghi thông tin báo cáo vào `reports/M3_MODEL_DEVELOPMENT_NOTES.md` và evidence chi tiết ngoài Git tại artifacts/m3. U-38 không thay DoD M3 (TV2 tính lại mẫu metrics và review split). Phiên soạn prompt chưa chạy M3/DB/model hoặc tự mở M4/M5; giữ M3 chưa tick.

## Receipt đóng M3 — 15/10/2026

U-40 giao M3-T1–T4; [M3 notes](../reports/M3_MODEL_DEVELOPMENT_NOTES.md) được ghi đồng thời khi quyết định/chạy. Source/basket set/preprocessing run M2 giữ nguyên. Không dùng fixture M1 hoặc audit lịch sử thay development thật.

| Tiêu chí | Evidence thực | Kết luận |
| --- | --- | --- |
| [x] M3-T1 | Preparation `7da29e52-53cf-4986-beff-dfaad251663c`: 29.335 train / 4.609 dev / 5.572 test, coverage39.516, overlap0, split local theo nguyên Invoice, test chỉ metadata; mask/K/seed/version/checksum có trước dev queries. | Đạt kỹ thuật; TV2 review split U-41 |
| [x] M3-T2 | Train-only catalog4.556 item/717.574 dòng hàng; tên modal/trim/tie, baseline basket frequency, mọi train basket đối chiếu dòng retained. FP-Growth chỉ29.335 train gồm2.503 giỏ một item. | Đạt, không dùng frequency/tên toàn kỳ |
| [x] M3-T3 / M3-AC1 | 12 ca synthetic có expected độc lập, Python/Java cùng dùng: đủ tiền đề, existing/dedup, nhiều luật, tie/prefix/Unicode, empty/unknown/no-rule/zero-rule/K lớn. Real Java khớp4.293 query cả candidate và tiền đề luật tốt nhất. | Đạt; không fallback/lift filter/rounding trước rank |
| [x] M3-AC2 | Cùng query/target/catalog/K/train; dev4.293 query,316 giỏ một item báo riêng,265 target mới/1.586 query context mới không bị loại,780 query không ứng viên luật vẫn góp0. Empty denominator NOT_APPLICABLE được kiểm. | Đạt; counts/numerator/denominator và subgroup lưu rõ |
| [x] M3-T4 / M3-AC3 | Ba config hữu hạn .03/.02/.01, confidence.3; tất cả3 PASS/2 FAIL được giữ. Chọn .01 bằng quy tắc development có trước, freeze source/policy/protocol/schema/code/config/outputs; finalNOT_RUN. | Đạt development; không ép thắng baseline/đặt scoreAC |
| [x] DoD | Configuration/source/policy/code hashes/runtime/RSS/commands/errors/limits trong notes/receipt/freeze; người dùng xác nhận **TV2 đã review split, tính lại mẫu metrics và chấp thuận, không còn điểm sửa — U-41**. | Đủ DoD, **đóng M3 ngày15/10/2026**; không suy runtimeTV2/GV/final |

**Run chọn:** `7bc55ac7-0d24-4ddd-a9b0-3b25d247b596`, FULL_SOURCE / MODEL_DEVELOPMENT / DEVELOPMENT READY, chưa publication. 1.349 itemsets/856 luật, K5/seed20261015/support.01/confidence.3/8partitions/local[2]/heap768m/stack4m. Mọi itemset frequency tính lại độc lập; mọi luật/keys/hash/readback/BSONLong/manifest và toàn bộ prediction/metrics replay đạt. 17 Python tests + 6 Java tests (không skipped khi truyền runDirectory) đạt. Không thay web ứng dụng hoặc namespace mẫu M1.

Dev luật hit505/4.293 (Recall@5=11,7633%), có gợi ý3.513/4.293 (81,8309%); baseline hit109/4.293 (2,5390%), có gợi ý4.293/4.293 (100%). Selected wrapper147,752giây, peak sampled RSS Python303,87 / JVM1.090,08 / Mongo101,37 / combined1.381,59MiB. .03 PASS thua baseline vẫn báo; lỗi guardRAM và StackOverflow cùng retry stack4m giữ lịch sử. Số đo không phải giờ-người, heap/stack config không là usage.

**Freeze:** `artifacts/m3/freeze-1a1f2ec6-331e-4b02-9aaf-18804793d4e9/freeze.json`, SHA256 `f7ee9c13432f0c99e7e5bcbf0363eed77eb4d5493b39e78fbb2e8e48557d053a`; `verification.json` cùng thư mục SHA256 `153263e3ceaddb50ceebc893942984b21ce70130cbea683ad633acfdbf601de6`. Receipt runtime/freeze PENDING_TV2 là snapshot trước U-41, giữ bất biến; `artifacts/m3/review-20261015.json` ghi xác nhận riêng. Câu hỏi review đã gắn đúng notes/gói review/freeze verification, mẫu10 query và split thật. Xác nhận được người dùng báo lại, không phải Agent thay thành viên hoặc trực tiếp quan sát độc lập TV2.

**Giới hạn/bàn giao:** test cuối NOT_RUN, không test items/mask/predictions/metrics, không refit toàn nguồn; chưa publication/HTTP dữ liệu thật/M4/M5 hoặc runtime máyTV2/M6. Guide mục7 đủ tái tạo, artifacts/output/DB/scratch ngoài Git; clone không có artifacts vẫn đọc được kết luận/IDs/hash trong notes. Mongo27019 có sẵn đầu phiên giữ chạy đúng receipt, dữ liệu không reset/drop, 27017 không tác động; kiểm lifecycle cuối trong repository evidence. Không commit/push, bàn giao rồi dừng trước M4/M5.

### Bàn giao prompt M4 — 16/10/2026, U-42

Đã đọc lại AC/DoD M3, review receipt U-41 và hash freeze/verification: M3 đủ điều kiện, không còn xác nhận/lựa chọn riêng cần bổ sung. Đã soạn [M4 Start Prompt](M4_START_PROMPT.md) và lời dẫn paste cho thread mới; yêu cầu triển khai M4-T1–T4/kiểm chứng UI dữ liệu thật, xử lý điểm chưa rõ bằng lựa chọn có căn cứ và ghi báo cáo vào `reports/M4_WEB_APPLICATION_NOTES.md` từ lúc bắt đầu. Snapshot Git khi soạn: main/HEAD ddb8970, M3 còn unstaged/untracked; không suy người dùng chưa/sẽ commit từ snapshot này. Chỉ chuẩn bị tài liệu, không chạy runtime/test ứng dụng/DB/publication/final hoặc tạo evidence M4; M4 vẫn chưa tick. M3 notes và receipts/freeze giữ kết quả, lần soạn prompt không làm lại nghiệm thu M3.
