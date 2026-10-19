# Phân tích hành vi mua sắm và gợi ý sản phẩm mua kèm

Đồ án môn Nhập môn Big Data, nhóm hai thành viên. Stack đã chọn: **PySpark local + FP-Growth + MongoDB + Spring Boot, Spring MVC + Thymeleaf**. Dataset: **Online Retail II**, được giảng viên chấp thuận theo xác nhận của người dùng.

**Điểm bắt đầu:** xem [trạng thái hiện tại](STATE.md). Agent đọc thêm [quy tắc làm việc](AGENTS.md). Để theo dõi tiến độ, dùng [Milestone Checklist](requirements-review/14_MILESTONE_CHECKLIST.md); không cần đọc toàn bộ hồ sơ trong một lần.

## Phạm vi hiện tại

**Tiếp nối U-54:** [prompt M7A](requirements-review/M7A_START_PROMPT.md) đã sẵn sàng cho thread mới: chỉ Word kỹ thuật, tạo baseline để người dùng review trước nội dung chi tiết. Phiên hiện tại chỉ chuẩn bị bàn giao; chưa tạo baseline/Word, slide và kiểm gói/nộp để sau, chưa giao.

**19/10/2026: M0–M6 đã đóng.** M6 full source mới→Spark→fit train→DEVELOPMENT gate→FINAL replication trong `bigdata_m6`/27019 PASS; FINAL **`87b3fc04-bb8e-449f-9ecc-3c5308b3d689`/version2** tại [demo8081](http://127.0.0.1:8081/). 25Python/11Java tests, HTTP/UI/lifecycle thật đạt; người dùng đã demo/giải thích/review và chấp thuận **U-53**. [M6 notes](reports/M6_FULL_RUN_TWO_MACHINES_NOTES.md), [guide8](pipeline/README.md#8-m6--tái-lập-toàn-nguồn-trong-database-riêng) giữ nguồn/run/hash/KPI/lệnh/ảnh/resources/incident Spark heartbeat và review. TV2 giả định tương đương theo **U-52**, không có số đo/full run độc lập máy đó; M6 đóng theo phạm vi điều chỉnh này. Source/freeze/config/READY/DB M5 giữ; không tune sau test. Dừng tại M6, M7/M8 chưa mở, không commit/push. Đoạn18/10 bên dưới là bàn giao M5 lịch sử.

Ngày18/10/2026: **M0–M5 đã đóng**. M5-T1–T4/AC kỹ thuật TV1 đạt; cả hai review run/metrics/lỗi, TV2 tính lại mẫu và chấp thuận không còn điểm sửa theo **U-48**, đủ DoD. Website phục vụ FINAL run`04c940db-313d-4a05-a039-90163e33f070`/version3, model train/config/checksum đúng freeze. Test5.572giỏ=389single+5.183query: Recall@5 luật451/5.183=8,7015%,baseline91/5.183=1,7557%; có gợi ý81,3043%/100%. Mở [demo local](http://127.0.0.1:8081/), đọc [Web Guide M5](web/README.md) và [M5 notes](reports/M5_INTEGRATION_FINAL_EVALUATION_NOTES.md). Giữ nguyên M2/M3/source/protocol/freeze/READY cũ; test đã tiếp xúc15:05:29UTC18/10, không tune sau score. Dừng M5, không tự mở M6/M7/M8/commit/push hoặc suy TV1 thành nghiệm thu hai máy. Mongo27019/web8081 giữ để demo, receipts M2/M5 và lệnh stop trong guide; dữ liệu giữ.

- Website phục vụ thống kê và gợi ý từ giỏ một hoặc nhiều sản phẩm; không thêm đăng nhập, JWT, thanh toán hoặc hệ thống bán hàng.
- Batch xử lý trước, MongoDB giữ dữ liệu nguồn và kết quả; website đọc lượt kết quả hoàn chỉnh.
- Người dùng/TV1 phụ trách dữ liệu, Spark, FP-Growth và đánh giá; TV2 phụ trách Java, web và tích hợp. Hai thành viên review chéo, mỗi máy tự chạy toàn bộ pipeline theo cấu hình cuối.
- Các quyết định P-01/P-02/P-03 và U-01–U-30 nằm trong [phạm vi đã xác nhận](requirements-review/07_CONFIRMED_SCOPE.md). U-27–U-29 chốt run bất biến/con trỏ, decimal text và dashboard hàng hóa + audit; U-30 xác nhận hai thành viên chấp thuận contract m0-contract-v1 về tài liệu.

## Cấu trúc workspace

```text
DoAn/
├── README.md                Điểm đọc đầu tiên
├── AGENTS.md                Quy tắc cho Agent trong repository
├── STATE.md                 Trạng thái, giới hạn kiểm chứng, việc kế tiếp
├── .gitignore               Loại dataset, môi trường máy, build, secrets
├── .gitattributes           Quy ước xuống dòng cho file văn bản
├── requirements-review/     Hồ sơ nguồn, RTM, thiết kế đề xuất, kế hoạch
│   └── evidence/            Minh chứng đọc nguồn/audit trước triển khai
├── data/
│   ├── raw/                 Nguồn gốc giữ nguyên; không đưa vào Git
│   ├── processed/           Dữ liệu xử lý sau này; không đưa vào Git
│   └── results/             Kết quả dữ liệu sau này; không đưa vào Git
├── pipeline/                Mẫu M1; parser/audit/import/PySpark và kiểm chứng toàn nguồn M2
├── web/                     Ba khu vực đọc DEVELOPMENT/FINAL; SAMPLE M1 tách mode
├── scripts/                 Lifecycle, publication/CAS/recovery, kiểm chứng/ảnh/tài nguyên
├── reports/                 Ghi chép dữ liệu/tiền xử lý M2; chỗ báo cáo/slide
└── artifacts/               Log, receipt, ảnh chạy sau này; không đưa vào Git
```

Hai file Word nguồn vẫn ở thư mục gốc, không di chuyển hoặc chỉnh sửa. Tên thư mục sản phẩm không xác lập schema, API, package Java hoặc module build.

## Git và làm việc trên hai máy

Repository dùng nhánh `main`; khi kiểm tra bàn giao ngày 14/10/2026 đã có commit đầu tiên và remote `origin` trỏ tới `https://github.com/lequoctrung-dev/bigdata-market-basket.git`. Xem [STATE](STATE.md) và kiểm tra Git để biết trạng thái mới nhất. Agent không tự tạo tài khoản, cấu hình Git toàn máy hoặc commit/push. Khi được giao commit, kiểm tra nội dung và chỉ stage file liên quan; không dùng `git add .` theo thói quen.

File cấu hình có bí mật, môi trường Python, Maven build, Spark scratch, dữ liệu MongoDB và dataset không thuộc Git. `.gitignore` hỗ trợ loại file; vẫn phải kiểm tra diff vì nó không tự phát hiện mọi bí mật.

Thư mục dữ liệu/log cục bộ không xuất hiện khi clone. Trước khi chạy pipeline sau này, hướng dẫn chạy cần tạo chúng và đặt nguồn đúng đường dẫn. Dataset hiện có:

- `data/raw/online-retail-ii/online_retail_II.xlsx`
- SHA-256: `bcbe73b35f5b7babf197fb0cb983a11f5d9ff929078d4aa53d171b1f2df2e980`
- Nguồn tải, khảo sát và cách đối chiếu: [Dataset Profile](requirements-review/10_DATASET_PROFILE.md) và [Dataset Evaluation](requirements-review/08_DATASET_EVALUATION.md).

Remote đã được cấu hình; chưa kiểm chứng clone/quyền truy cập hoặc workspace trên máy thứ hai trong bước bàn giao. Không dùng việc copy đầu ra dữ liệu để thay full run trên máy thứ hai.

## Thứ tự tài liệu và bước kế tiếp

1. [STATE.md](STATE.md): trạng thái hiện tại; không phải bằng chứng hệ thống đã chạy.
2. [Milestone Checklist](requirements-review/14_MILESTONE_CHECKLIST.md): việc cần làm và tiêu chí đóng mốc.
3. [Master Plan](requirements-review/13_MASTER_IMPLEMENTATION_PLAN.md): chi tiết task, AC/DoD, phụ thuộc và phân công.
4. [Confirmed Scope](requirements-review/07_CONFIRMED_SCOPE.md), [RTM](requirements-review/01_REQUIREMENT_MATRIX.md): quyết định và yêu cầu truy vết.
5. Review M0 chỉ cần tập trung [đặc tả mục 8–10](requirements-review/11_SPECIFICATION_DRAFT.md) và [contract mục 9–13](requirements-review/12_TECHNICAL_DESIGN.md); checklist 14 nêu phần cần đọc của TV1/TV2 và nơi ghi receipt.

M1 theo receipt mẫuTV1/U-33/U-35; M2 preprocessing/postcheck/U-38; M3 development/freeze/Java parity/U-41; M4 kỹ thuật/UI/U-44; M5 end-to-end/crash/final/parity/UI/reviewU-48 đã đóng. Mongo27019/web8081 FINAL có lifecycle M2/M5 riêng. Namespace27018 chỉ SAMPLE tường minh. DừngM5; full run hai máyM6 chưa thực hiện. STATE/checklist giữ hiện tại, không lấy snapshot stop/lifecycle cũ thay process sống.

Lịch sử bàn giao U-45: [M5 Start Prompt](requirements-review/M5_START_PROMPT.md) soạn18/10/2026 trước khi thực hiện M5; yêu cầu đúng T1–T4, notes đồng thời và hỏi trước lựa chọn quan trọng. Phiên chuẩn bị chỉ tài liệu, sau đó M5 đã được giao/triển khai/đóng theo U-46–U-48 như trạng thái phía trên. [M4 Start Prompt](requirements-review/M4_START_PROMPT.md) và [M3 Start Prompt](requirements-review/M3_START_PROMPT.md) giữ lịch sử bàn giao trước.

Ngày19/10/2026 theo U-49 đã tạo [M6 Start Prompt](requirements-review/M6_START_PROMPT.md) cho thread mới: M5 đủ AC/DoD/U-48, không còn confirm riêng. M6 yêu cầu full pipeline/demo thật trên từng máy, kiểm tính portable/guards/role/IDs trước chạy và giữ freeze/READY. Khi bắt đầu ghi đồng thời `reports/M6_FULL_RUN_TWO_MACHINES_NOTES.md`; lựa chọn quan trọng chưa đủ nguồn phải hỏi trước phần phụ thuộc. Phiên chuẩn bị chỉ tài liệu/đối chiếu artifact, chưa chạy hoặc nghiệm thu M6/hai máy, không commit/push.
