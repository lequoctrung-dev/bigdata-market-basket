# Phân tích hành vi mua sắm và gợi ý sản phẩm mua kèm

Đồ án môn Nhập môn Big Data, nhóm hai thành viên. Stack đã chọn: **PySpark local + FP-Growth + MongoDB + Spring Boot, Spring MVC + Thymeleaf**. Dataset: **Online Retail II**, được giảng viên chấp thuận theo xác nhận của người dùng.

**Điểm bắt đầu:** xem [trạng thái hiện tại](STATE.md). Agent đọc thêm [quy tắc làm việc](AGENTS.md). Để theo dõi tiến độ, dùng [Milestone Checklist](requirements-review/14_MILESTONE_CHECKLIST.md); không cần đọc toàn bộ hồ sơ trong một lần.

## Phạm vi hiện tại

Ngày 14/10/2026: chuẩn bị workspace và quy tắc Agent trước M0. M0 chưa nghiệm thu; M1–M8 chưa thực hiện. Các thư mục sản phẩm mới chỉ là vị trí dự kiến, chưa có ứng dụng hoặc môi trường chạy đã được kiểm chứng.

- Website phục vụ thống kê và gợi ý từ giỏ một hoặc nhiều sản phẩm; không thêm đăng nhập, JWT, thanh toán hoặc hệ thống bán hàng.
- Batch xử lý trước, MongoDB giữ dữ liệu nguồn và kết quả; website đọc lượt kết quả hoàn chỉnh.
- Người dùng/TV1 phụ trách dữ liệu, Spark, FP-Growth và đánh giá; TV2 phụ trách Java, web và tích hợp. Hai thành viên review chéo, mỗi máy tự chạy toàn bộ pipeline theo cấu hình cuối.
- Các quyết định P-01/P-02/P-03 và U-01–U-26 nằm trong [phạm vi đã xác nhận](requirements-review/07_CONFIRMED_SCOPE.md). Giữ nguyên các lựa chọn đã chốt; bản thiết kế chi tiết vẫn cần review ở M0.

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
├── pipeline/                Chỗ dành cho Python/PySpark; hiện trống
├── web/                     Chỗ dành cho Spring Boot; hiện trống
├── scripts/                 Chỗ dành cho công cụ hỗ trợ; hiện trống
├── reports/                 Chỗ dành cho báo cáo/slide; hiện trống
└── artifacts/               Log, receipt, ảnh chạy sau này; không đưa vào Git
```

Hai file Word nguồn vẫn ở thư mục gốc, không di chuyển hoặc chỉnh sửa. Tên thư mục sản phẩm không xác lập schema, API, package Java hoặc module build.

## Git và làm việc trên hai máy

Repository cục bộ dùng nhánh `main`, chưa có commit hoặc remote. Bước chuẩn bị không tạo tài khoản, cấu hình Git toàn máy hoặc tự commit/push. Khi được giao commit, kiểm tra nội dung và chỉ stage file liên quan; không dùng `git add .` theo thói quen.

File cấu hình có bí mật, môi trường Python, Maven build, Spark scratch, dữ liệu MongoDB và dataset không thuộc Git. `.gitignore` hỗ trợ loại file; vẫn phải kiểm tra diff vì nó không tự phát hiện mọi bí mật.

Thư mục dữ liệu/log cục bộ không xuất hiện khi clone. Trước khi chạy pipeline sau này, hướng dẫn chạy cần tạo chúng và đặt nguồn đúng đường dẫn. Dataset hiện có:

- `data/raw/online-retail-ii/online_retail_II.xlsx`
- SHA-256: `bcbe73b35f5b7babf197fb0cb983a11f5d9ff929078d4aa53d171b1f2df2e980`
- Nguồn tải, khảo sát và cách đối chiếu: [Dataset Profile](requirements-review/10_DATASET_PROFILE.md) và [Dataset Evaluation](requirements-review/08_DATASET_EVALUATION.md).

Chưa có remote nên chưa có quy trình clone/chia sẻ repository được thử. Khi cần chia sẻ, người dùng chọn nơi lưu và quyền truy cập; không chặn review M0. Không dùng việc copy đầu ra dữ liệu để thay full run trên máy thứ hai.

## Thứ tự tài liệu và bước kế tiếp

1. [STATE.md](STATE.md): trạng thái hiện tại; không phải bằng chứng hệ thống đã chạy.
2. [Milestone Checklist](requirements-review/14_MILESTONE_CHECKLIST.md): việc cần làm và tiêu chí đóng mốc.
3. [Master Plan](requirements-review/13_MASTER_IMPLEMENTATION_PLAN.md): chi tiết task, AC/DoD, phụ thuộc và phân công.
4. [Confirmed Scope](requirements-review/07_CONFIRMED_SCOPE.md), [RTM](requirements-review/01_REQUIREMENT_MATRIX.md): quyết định và yêu cầu truy vết.
5. Khi làm M0, mở [đặc tả](requirements-review/11_SPECIFICATION_DRAFT.md) và [thiết kế đề xuất](requirements-review/12_TECHNICAL_DESIGN.md).

Sau bàn giao bước chuẩn bị, dừng để người dùng giao thực hiện M0. Chưa cài Java/Python/Spark/MongoDB, tạo DB/schema/index hoặc viết prototype; những việc kiểm chứng môi trường runtime nằm ở M1, sau khi M0 được đóng.
