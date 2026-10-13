# Milestone Checklist — Master Plan

Ngày **14/10/2026**. Theo [Master Plan](13_MASTER_IMPLEMENTATION_PLAN.md). **M0 đã có các quyết định chính, chưa nghiệm thu toàn hợp đồng kỹ thuật; M1–M8 chưa triển khai. Phải đóng M0 trước khi thực hiện M1.** Không đánh dấu runtime PASS chỉ vì quyết định đã chốt. Đọc phần cuối file này để biết việc kế tiếp.

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
| [ ] M0 — Chốt phạm vi làm việc và hợp đồng dữ liệu | M0-T1, M0-T2, M0-T3, M0-T4 | M0-AC1/AC2/AC3 + DoD ở file 13 | Thiết kế/contract được review, roles và decision log | Quyết định chính có U-20–U-26; chưa nghiệm thu toàn hợp đồng kỹ thuật |
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
| Milestone đang triển khai | Không có; đã chuẩn bị workspace/Agent trước M0, dừng sau bàn giao; M0 chưa được thực hiện/đóng trong bước chuẩn bị |
| Tổng effort cơ sở / gồm dự phòng | 196–296 / khoảng 236–356 giờ-người; tăng M6 vì full run hai máy; chưa đo velocity |
| Calendar 7 tuần | Khung tham chiếu, chưa có ngày/giờ đã xác nhận |
| Ngày hoàn tất/evidence theo mốc | Chưa có |

Khi đóng mốc, ghi ngày thật, người thực hiện/review, source/run/config và đường dẫn evidence; chỉ tick sau khi AC/DoD được kiểm chứng. Nộp/live demo còn cần lịch và sự thực hiện thật.


## Việc kế tiếp — chỉ đọc phần này nếu cần thao tác

**Bước kế tiếp là hoàn tất M0, chưa phải chạy thử M1.** Các quyết định chính đã có; không hỏi lại các lựa chọn đã chốt. Phần còn lại của M0:

- [ ] Hoàn tất rà soát M0-T1/T3/T4: đối chiếu phạm vi, truy vết, mapping loại TEST, xác nhận học thuật, phân công và full run hai máy; ghi kết quả review, không chỉ dựa vào việc đã có tài liệu.
- [ ] Hoàn thiện và review M0-T2 trong file 11/12: quy ước input/output, collection/khóa, tiền/ngày/ID, trách nhiệm batch và web, manifest/công bố kết quả, KPI/màn hình tối thiểu. Chi tiết triển khai được chọn trong phạm vi đã duyệt; lựa chọn lớn chưa được chấp thuận phải trình người dùng.
- [ ] TV1/TV2 review hợp đồng kỹ thuật, ghi kết quả theo M0-AC1/AC2/AC3 và DoD ở file 13; nêu rõ các giả định cần kiểm chứng bằng mẫu ở M1. Review tài liệu không phải runtime PASS.
- [ ] Khi đủ AC/DoD, ghi ngày và căn cứ rồi mới tick M0. Chưa có deadline/giờ tuần không tự chặn đóng M0; vẫn giữ QD-07 mở.

**Sau khi M0 được đóng và được giao thực hiện M1:**
1. Ghi CPU/kiến trúc Windows và bản Java/Python/MongoDB/Maven hiện có trên từng máy; không tự kết luận 16 GB/50 GB đủ cho fit.
2. Nhóm chốt bộ phiên bản để thử từ tài liệu chính thức.
3. Chạy luồng mẫu MongoDB → PySpark/FP-Growth → MongoDB → MVC/Thymeleaf, mỗi máy có receipt riêng.
4. Sau M1 mới mở pipeline toàn nguồn và full run từng máy theo milestones; không lấy mẫu PASS thay full run.

Không cần hỏi lại dataset, hướng báo cáo, TEST, vai trò hoặc chế độ hai máy. Deadline/giờ tuần vẫn chưa rõ, không chặn chuẩn bị kỹ thuật; CPU có thể kiểm tra trực tiếp ở máy được truy cập.
