# Milestone Checklist — Master Plan

Ngày **14/10/2026**. Theo [Master Plan](13_MASTER_IMPLEMENTATION_PLAN.md). **M0 đã đóng về review tài liệu:** M0-D1/D2/D3 chọn U-27–U-29, người dùng xác nhận cả TV1/TV2 đã review và chấp thuận bản hiện tại theo U-30; AC1/AC2/AC3 và DoD có căn cứ bên dưới. **M1–M8 chưa triển khai; chưa giao/mở M1.** Không coi nghiệm thu tài liệu là runtime PASS.

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
| [ ] M1 — Học Spark cần dùng và kiểm chứng luồng mẫu trên hai máy | M1-T1, M1-T2, M1-T3, M1-T4 | M1-AC1/AC2/AC3 + DoD ở file 13 | Prototype và receipt luồng mẫu riêng hai máy | Chưa thực hiện; chưa có evidence nghiệm thu |
| [ ] M2 — Xây pipeline dữ liệu và kiểm chứng P-01/P-02 trên nguồn đầy đủ | M2-T1, M2-T2, M2-T3, M2-T4 | M2-AC1/AC2/AC3 + DoD ở file 13 | Pipeline/full-source counts/basket set và xác nhận dataset | Chưa thực hiện; chưa có evidence nghiệm thu |
| [ ] M3 — FP-Growth, baseline và đánh giá trên phần phát triển | M3-T1, M3-T2, M3-T3, M3-T4 | M3-AC1/AC2/AC3 + DoD ở file 13 | Kết quả development, eval harness và config freeze | Chưa thực hiện; chưa có evidence nghiệm thu |
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
| Cấu hình hai máy và bộ phiên bản | Theo người dùng: cả hai Windows 11/RAM 16 GB/50 GB trống; CPU/kiến trúc/versions chưa kiểm tra; chưa receipt runtime |
| Milestone đang triển khai | Không có; M0 đóng về tài liệu ngày 14/10/2026, dừng sau bàn giao; M1 chưa được giao/mở |
| Tổng effort cơ sở / gồm dự phòng | 196–296 / khoảng 236–356 giờ-người; tăng M6 vì full run hai máy; chưa đo velocity |
| Calendar 7 tuần | Khung tham chiếu, chưa có ngày/giờ đã xác nhận |
| Ngày hoàn tất/evidence theo mốc | M0: 14/10/2026; file 11/12 contract m0-contract-v1, file 07 U-27–U-30, receipt AC/DoD bên dưới. Chưa có runtime hoặc ngày hoàn tất M1–M8 |

Khi đóng mốc, ghi ngày thật, người thực hiện/review, source/run/config và đường dẫn evidence; chỉ tick sau khi AC/DoD được kiểm chứng. Nộp/live demo còn cần lịch và sự thực hiện thật.


## Việc kế tiếp — chỉ đọc phần này nếu cần thao tác

**M0 đã hoàn tất về tài liệu, dừng sau bàn giao.** Khi người dùng giao M1 mới kiểm chứng môi trường/luồng mẫu; không tự bắt đầu. Các phần M0 đã có căn cứ:

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
