# Phân tích hành vi mua sắm và gợi ý sản phẩm mua kèm

Đồ án môn Nhập môn Big Data, nhóm hai thành viên. Stack đã chọn: **PySpark local + FP-Growth + MongoDB + Spring Boot, Spring MVC + Thymeleaf**. Dataset: **Online Retail II**, được giảng viên chấp thuận theo xác nhận của người dùng.

**Điểm bắt đầu:** xem [trạng thái hiện tại](STATE.md). Agent đọc thêm [quy tắc làm việc](AGENTS.md). Để theo dõi tiến độ, dùng [Milestone Checklist](requirements-review/14_MILESTONE_CHECKLIST.md); không cần đọc toàn bộ hồ sơ trong một lần.

## Phạm vi hiện tại

Ngày16/10/2026: **M0–M4 đã đóng**. M4-T1–T4/AC kỹ thuật TV1 PASS, người dùng đã kiểm UI/đối chiếu và chấp thuận không còn điểm sửa U-44, đủ DoD. Website ba khu vực đọc run DEVELOPMENT freeze, publication version1; mở [demo local](http://127.0.0.1:8081/), đọc [hướng dẫn/đáp án M4](web/README.md) và [M4 notes](reports/M4_WEB_APPLICATION_NOTES.md). Run chọn1.349 itemsets/856 luật, Recall@5 dev505/4.293 so baseline109/4.293; test cuối **NOT_RUN**. Giữ nguyên M2/M3/source/config/protocol/freeze; dừng tại M4, không refit/M5/M6/commit/push hoặc suy TV1 thành nghiệm thu hai máy. Mongo27019 có sẵn giữ chạy, web8081 có receipt/lifecycle riêng tại `artifacts/m4/`.

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
├── web/                     Ba khu vực M4 đọc DEVELOPMENT; SAMPLE M1 tách mode
├── scripts/                 Lifecycle M1/M2/M4, publication và kiểm chứng/ảnh/tài nguyên
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

M1 theo receipt mẫu TV1/U-33/U-35; M2 theo preprocessing/postcheck/U-38; M3 theo development/freeze/Java parity/U-41; M4 theo kỹ thuật TV1/U-44 đã đóng. M4 dùng Mongo27019, web8081 DEVELOPMENT và lifecycle riêng. Namespace mẫu27018 chỉ cho SAMPLE tường minh. Dừng tại M4; full run hai máyM6 giữ nguyên. Trạng thái/receipt hiện tại ở STATE/checklist, không lấy snapshot stop M2 làm lifecycle hiện tại.

Để tiếp tục sau M4, dùng [M5 Start Prompt](requirements-review/M5_START_PROMPT.md) soạn18/10/2026 theo U-45. M4 đã đủ AC/DoD/U-44, không còn confirm riêng. Prompt giao M5-T1–T4/end-to-end/publication-retry/final evaluation đúng freeze; khi bắt đầu ghi đồng thời `reports/M5_INTEGRATION_FINAL_EVALUATION_NOTES.md`, hỏi trước các lựa chọn quan trọng còn thiếu sau kiểm nguồn. Phiên chuẩn bị prompt chỉ đọc/viết hồ sơ, không thực hiện M5, mở test cuối hoặc đổi lifecycle. [M4 Start Prompt](requirements-review/M4_START_PROMPT.md) và [M3 Start Prompt](requirements-review/M3_START_PROMPT.md) giữ lịch sử bàn giao trước.
