# Phân tích hành vi mua sắm và gợi ý sản phẩm mua kèm

Đồ án môn Nhập môn Big Data, nhóm hai thành viên. Stack đã chọn: **PySpark local + FP-Growth + MongoDB + Spring Boot, Spring MVC + Thymeleaf**. Dataset: **Online Retail II**, được giảng viên chấp thuận theo xác nhận của người dùng.

**Điểm bắt đầu:** xem [trạng thái hiện tại](STATE.md). Agent đọc thêm [quy tắc làm việc](AGENTS.md). Để theo dõi tiến độ, dùng [Milestone Checklist](requirements-review/14_MILESTONE_CHECKLIST.md); không cần đọc toàn bộ hồ sơ trong một lần.

## Phạm vi hiện tại

Ngày 15/10/2026: **M0 và M1 đã đóng.** M1 có receipt mẫu TV1 thật, ngoại lệ U-33 miễn receipt TV2 riêng và xác nhận demo/học/giải thích/review U-35, không còn điểm sửa. Full run hai máy tại M6 giữ nguyên; chưa mở M2. Hướng dẫn tái tạo và bài thực hành: [M1 Guide](pipeline/README.md).

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
├── pipeline/                Fixture/đáp án, PySpark batch mẫu, dependency và hướng dẫn M1
├── web/                     Spring Boot/MVC/Thymeleaf đọc run mẫu hoàn chỉnh
├── scripts/                 Launcher M1, lifecycle guard và kiểm tra HTTP
├── reports/                 Chỗ dành cho báo cáo/slide; hiện trống
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

M1 đã nghiệm thu ngày 15/10 theo receipt mẫu TV1, ngoại lệ U-33 và xác nhận học/demo/review U-35; không ghi TV2 đã chạy. MongoDB mẫu riêng 27018 và web 8081 đã dừng đúng receipt sau demo, dữ liệu giữ nguyên, dịch vụ 27017 vẫn nghe. Full run hai máy M6 giữ nguyên. Chưa xử lý Online Retail II bằng pipeline sản phẩm hoặc mở M2; chờ giao việc tiếp theo.
