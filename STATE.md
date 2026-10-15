# Trạng thái dự án

Cập nhật: **15/10/2026**. Đây là trạng thái điều phối; chỉ tick milestone theo tiêu chí và evidence trong [checklist](requirements-review/14_MILESTONE_CHECKLIST.md).

## Phạm vi giao việc hiện tại

Đã hoàn tất giao việc **M1 — Học Spark cần dùng và kiểm chứng luồng mẫu** ngày **15/10/2026**: receipt mẫu TV1 đạt, **U-33 miễn receipt TV2 riêng ở M1**, **U-35 xác nhận đã demo và cả hai đã học/giải thích/review, chấp thuận, không còn điểm sửa**. M1 đủ AC/DoD theo tiêu chí điều chỉnh, đã đóng; không ghi TV2 runtime PASS. Full run hai máy M6 giữ nguyên. Dừng sau bàn giao, chưa mở M2.

## Những gì đã có và đã kiểm tra

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
| M2–M8 | Chưa thực hiện; không có evidence nghiệm thu runtime hoặc nộp bài |

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

1. M1 đã đóng, không hỏi lại phần demo/học/review theo U-35 hoặc receipt TV2 đã được miễn riêng M1 theo U-33. Agent dừng sau bàn giao; không tự mở M2.
2. Khi được giao M2, đọc task/AC/DoD tương ứng và kiểm tra lại source/code/môi trường hiện tại. Chưa xử lý Online Retail II bằng pipeline sản phẩm; counts/range/scale toàn nguồn, tài nguyên/native và chất lượng đánh giá chưa được M1 chứng minh.
3. U-15/U-22 và full run hai máy M6 giữ nguyên. TV2 thực tế chưa được kiểm chứng; không dùng giả định cấu hình giống hoặc output TV1 thay bằng chứng M6.
4. Theo U-36 đã soạn [prompt tiếp nối M2](requirements-review/M2_START_PROMPT.md) cho thread mới; phiên soạn prompt chưa mở/triển khai M2. Khi M2 bắt đầu, phải ghi thông tin phục vụ báo cáo vào `reports/M2_DATA_PREPROCESSING_NOTES.md`, gắn evidence/run/hash và phân biệt quan sát thật với điều chưa đo. Không tự commit/push.

Task/AC/DoD cụ thể: [M1 trong Master Plan](requirements-review/13_MASTER_IMPLEMENTATION_PLAN.md). Tiến độ và các ô nghiệm thu: [Milestone Checklist](requirements-review/14_MILESTONE_CHECKLIST.md).
