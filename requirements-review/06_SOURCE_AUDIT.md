# Source Audit và kiểm tra độ phủ

Đã đọc và đối chiếu **18/18 trang A**, **4/4 trang B**, toàn bộ **4 bảng** của hai file, **3 vị trí ảnh** trong A và các phần nội dung bổ sung trong gói Word. Không phát hiện phần văn bản nguồn không đọc được. Có khác biệt hiển thị ở bìa phụ A khi xuất PDF; nội dung đó đã được đọc bằng XML và Word, nên không bỏ sót. Không có phụ lục nội dung thực tế trong hai file; B chỉ liệt kê “Phụ lục (nếu có)” trong cấu trúc báo cáo.

## Cách kiểm tra

1. Trích toàn bộ đoạn trong nội dung Word XML, không chỉ đoạn ngoài bảng; kiểm tra các phần footer/footnote/endnote và phần ảnh.
2. Mở từng file **chỉ đọc**, xác minh phân trang bằng Word và xuất bản PDF kiểm tra cục bộ; đóng không lưu.
3. Dựng và xem **từng ảnh của cả 22 trang**; xem riêng cả hai tài nguyên ảnh gốc của A. Đối chiếu bảng theo hàng/cột để giữ đúng rubric và thời điểm.
4. Tách nghĩa vụ độc lập trong câu/bảng; giữ lựa chọn “hoặc”, “như”, “tùy đề tài” và “nếu có”; không đổi ví dụ thành nghĩa vụ.
5. Kiểm tra ngược tất cả đoạn có chữ sang RTM hoặc một phân loại ngữ cảnh/ví dụ rõ ràng. Việc kiểm tra liên kết và mã là kiểm tra hồ sơ phân tích, không là nghiệm thu sản phẩm đồ án.

## Thống kê cấu trúc đã đọc

| Nội dung | File A | File B |
| --- | --- | --- |
| Trang vật lý theo Word và ảnh render | 18 | 4 |
| Tổng đoạn nội dung XML, gồm đoạn trống | 287 | 171 |
| Đoạn có văn bản XML | 115 | 163 |
| Đoạn trống/đoạn chỉ có ảnh | 172 | 8 |
| Bảng | 1 bảng minh họa | 3 bảng: đề tài, rubric, kế hoạch |
| Vị trí ảnh | 3: logo trên hai bìa, ảnh giao diện ví dụ | 0 |
| Tài nguyên ảnh khác nhau | 2 | 0 |
| Text box trong nội dung XML | 0 | 0 |
| Chèn/xóa được theo dõi | 0/0 | 0/0 |
| Footnote/endnote có nội dung | Không; chỉ cấu trúc phân cách hệ thống | Không; chỉ cấu trúc phân cách hệ thống |
| Comment chứa nội dung | Không có phần comment | Không có phần comment |
| Footer | 2 phần footer, chứa field PAGE/số trang | Không có phần footer |
| Phụ lục nội dung thực tế | Không có | Không có |

Phần footer của A phục vụ quy tắc đánh số trang đã truy vết tại A-F058–A-F063; field PAGE/cached value không tạo thêm yêu cầu nghiệp vụ. Không có nội dung nhúng/OLE hoặc văn bản trong header cần đọc thêm theo kiểm tra gói.

## Đối chiếu từng phần và trang

| File | Trang vật lý | Phần nguồn | Phạm vi đoạn | Dòng/nhóm truy vết | Kết quả kiểm tra |
| --- | --- | --- | --- | --- | --- |
| A | 1 | Bìa chính | A:P001–A:P024 | A-S01, A-S03–A-S14 | Đã đọc chữ, trường điền, danh sách mẫu và logo. Ba dòng sinh viên là ví dụ; nhóm 2 người theo B. |
| A | 2 | Bìa phụ | A:P025–A:P048 | A-S02–A-S15 | Đã đọc XML và Word, xem trang render. Cơ quan/trường/khoa/logo/ngành không hiển thị trong PDF kiểm tra; văn bản/ảnh gốc vẫn đọc được. |
| A | 3 | Lời cảm ơn | A:P049–A:P053 | A-S16, A-C01–A-C03 | Ngắn gọn, trang trọng, biết ơn người hỗ trợ được tách riêng. |
| A | 4 | Nhận xét GVHD | A:P054–A:P078 | A-S17–A-S19 | Đã kiểm tra trang nhận xét, nhãn người ký và ghi họ tên; không giả định phải có chữ ký thật. |
| A | 5 | Mục lục | A:P079–A:P106 | A-S20, A-F064–A-F065 | Tạo tự động là yêu cầu; tên mục và số trang ví dụ là minh họa, có số trang không khớp. |
| A | 6 | Danh mục ký hiệu/viết tắt | A:P107–A:P135 | A-S21–A-S23, A-S34 | Đọc đủ các cột và hai dòng DBMS/IT; đó là ví dụ, không là thuật ngữ phải dùng. |
| A | 7 | Danh mục hình | A:P136–A:P162 | A-S24, A-F066 | Tạo danh mục tự động; tên hình/số trang là ví dụ. |
| A | 8 | Danh mục bảng | A:P163–A:P187 | A-S25, A-F067 | Đã giữ điều kiện 'nếu có'; tên bảng và trang 28/30 không là dữ liệu bắt buộc. |
| A | 9 | Mở đầu | A:P188–A:P212 | A-S26, A-C04–A-C09 | Tách giới thiệu, lý do, dẫn chứng tùy chọn, mục tiêu, đối tượng và phạm vi. |
| A | 10 | Chương 1 | A:P213–A:P214 | A-S27, A-C10–A-C11 | Đọc nội dung và quyền đổi tên; các nhánh khảo sát/thuật toán/nghiên cứu/mạng tùy đề tài. |
| A | 11 | Chương 2 | A:P215–A:P217 | A-S28, A-C12–A-C13, A-C28–A-C29 | Đọc nội dung và quyền đổi tên; nhánh phân tích hệ thống/mô hình nghiệp vụ đã tách. |
| A | 12 | Chương 3 | A:P218–A:P219 | A-S29, A-C14, A-C25–A-C27 | Thiết kế cấu trúc, giao diện, tương tác được tách riêng theo điều kiện hướng hệ thống. |
| A | 13 | Chương 4 | A:P220–A:P221 | A-S30, A-C15–A-C17 | Cài đặt/cấu hình, môi trường và đặc tả được giữ. |
| A | 14 | Chương 5 | A:P222–A:P224 | A-S31, A-C18, A-C30–A-C31 | Đã tách đánh giá thuật toán và thử nghiệm/triển khai hệ thống theo hướng đề tài; không thêm production. |
| A | 15 | Kết luận | A:P225–A:P230 | A-S32, A-C19–A-C24 | Kết quả, yêu cầu hoàn thành, mức hoàn thiện, hạn chế, khó khăn, hướng phát triển được tách. |
| A | 16 | Tài liệu tham khảo | A:P231–A:P246 | A-S33; AMB-24 | Đọc đủ 4 tài liệu mẫu, kể cả web/ngày truy cập; không suy chuẩn/số lượng nguồn bắt buộc. |
| A | 17 | Thể thức §1 và §2, ảnh/bảng mẫu | A:P247–A:P273 | A-F001–A-F033 | Đọc đủ quy định font/lề/giấy/heading/caption/table và ảnh ví dụ; bảng tiếp sang trang 18. |
| A | 18 | Phần cuối bảng mẫu; thể thức §3 và §4 | A:P271–A:P287 | A-F034–A-F065 | Đã xem hàng tiêu đề lặp, bullet cấp 1/2, spacing, numbering và TOC. P281–P287 trống. |
| B | 1 | I; II.1; đầu II.2 | B:P001–B:P014 | B-L01–B-L07, B-G01–B-G07, B-S01–B-S07, B-D01–B-D15 | Mục tiêu năng lực tách khỏi nghĩa vụ cụ thể; đủ nhóm, đề tài, đặc tả và dữ liệu. |
| B | 2 | Cuối II.2; II.3; đầu II.5 | B:P015–B:P036 | B-T01–B-T06, B-E01–B-E07, B-V01–B-V05, B-F01–B-F02, B-O01–B-O08, B-R01–B-R12, B-N01–B-N08 | Đọc đầy đủ công nghệ, thực nghiệm, đánh giá, trực quan hóa, hồ sơ, nộp Classroom và 10 phần cấu trúc nguồn. |
| B | 3 | II.5/T1; III/T2; đầu IV/T3 | B:P037–B:P145 | B-H01–B-H09, B-RUB01–B-RUB14, B-P01–B-P12 | Đọc toàn bộ 1 đề tài gợi ý; đủ 6 hàng rubric và 5 cột chất lượng; đủ phần đầu kế hoạch. |
| B | 4 | Phần cuối IV/T3; Lưu ý | B:P146–B:P171 | B-P13–B-P39, B-A01–B-A04, B-RUB09 | Đọc các dòng tuần 6–7, 8–9, 10, hai lưu ý và chế tài copy điểm 0. |

## Kiểm tra độ phủ ngược của từng đoạn

- Có **278 đoạn có văn bản**. **201 đoạn** được ít nhất một dòng RTM dẫn trực tiếp. **77 đoạn** còn lại đã được phân loại từng đoạn là tiêu đề, cột/STT, ví dụ, dấu lược/trang trí hoặc mục tiêu tổng quát đã được cụ thể hóa.
- **0 đoạn có văn bản chưa được phân loại** trong lượt đối chiếu cuối. Chi tiết cho từng Pxxx, câu gốc và các ID liên quan nằm trong [SOURCE_EXTRACT.md](SOURCE_EXTRACT.md).
- Có **282 ID truy vết duy nhất**: **150 từ B**, **132 từ A**. Các ID chỉ dẫn đoạn nguồn tồn tại, có trang được xác minh. ID vấn đề đều tồn tại trong [log](04_AMBIGUITY_CONFLICT_LOG.md).
- Không có đoạn bị loại chỉ vì nằm trong bảng/phụ lục. Các đoạn trống không tạo nghĩa vụ; hình đã xem riêng. Nội dung mục tiêu I của B được đọc và nối với yêu cầu cụ thể, phần rèn luyện năng lực được giữ ở B-L01–B-L07.

“0 đoạn chưa phân loại” là kết quả kiểm tra độ phủ cấu trúc cùng rà soát thủ công ý nghĩa, **không phải chứng nhận tuyệt đối không thể còn cách diễn giải khác**. Các điểm mơ hồ được giữ mở; tài liệu ngoài hai file chưa được cung cấp vẫn là giới hạn tại AMB-16.

## Các bảng đã kiểm tra theo cấu trúc

| Bảng | Trang | Số hàng cấu trúc | Nội dung đã đọc | Xử lý |
| --- | --- | --- | --- | --- |
| A T1 | 17–18 | 4 hàng: tiêu đề và 3 dòng ví dụ | STT, Loại dữ liệu, Ghi chú, các dòng 1–3; header lặp ở trang sau | Quy định caption/định dạng/lặp header vào A-F026–A-F033; không biến ô ví dụ thành schema |
| B T1 | 3 | 2 hàng: header và 1 đề tài | Tên đề tài mua sắm/mua kèm và toàn bộ gợi ý công nghệ/kỹ thuật/sản phẩm | B-H01–B-H09 ở mức gợi ý |
| B T2 | 3 | 8 hàng: 2 hàng header và 6 tiêu chí | 6 tiêu chí, CLO tương ứng, 5 mức chất lượng, toàn bộ dải tỷ lệ, điểm 1.0/2.0/2.5/2.5/1.0/1.0 | B-RUB01–B-RUB14; tổng điểm 10.0; không phân bổ trọng số riêng |
| B T3 | 3–4 | 6 hàng: header và 5 nhóm tuần | Tuần 1–3, 4–5, 6–7, 8–9, 10; cả nội dung công việc và sản phẩm cần đạt | B-P01–B-P39; giữ các mâu thuẫn lịch tại AMB-02–AMB-04 |

## Quan sát mẫu được giữ riêng khỏi yêu cầu

- B dùng khổ trang Letter/lề 1 inch trong thiết lập file nguồn. Đó là định dạng của **đề bài**, không là quy định báo cáo thay thế A4/lề được A ghi thành văn.
- B đánh số mục từ II.3 sang II.5; không có mục II.4 trong nội dung nguồn. Không phát hiện văn bản phần II.4 bị ẩn/không đọc được; không tự tạo yêu cầu cho mục vắng.
- A có ảnh logo trường và ảnh trang chủ để minh họa caption. Các chữ/chức năng trong screenshot không là yêu cầu ứng dụng đồ án.
- A có ba dòng sinh viên mẫu, còn B và thông tin bạn cho là nhóm hai người; đây là khác biệt ví dụ, không là hai quy định sĩ số xung đột.
- Các số trang trong TOC/danh mục A là số mẫu, có mục trỏ trang không tồn tại; quy tắc đánh số thành văn và mục lục tự động phải được phân biệt với dữ liệu mẫu.
- Bìa phụ A trong PDF kiểm tra không hiện cơ quan/trường/khoa/logo/ngành dù các phần này có trong XML/Word. Không kết luận nguyên nhân là nội dung bị ẩn; kiểm tra XML không có vanish/webHidden trong nội dung. Nội dung đã đọc được bằng cách khác, nhưng không coi bản render này là mẫu hiển thị hoàn hảo để sao chép.
- A tr.16 có bốn tài liệu ví dụ, trong đó web có ngày truy cập; không có tuyên bố về chuẩn IEEE/APA hay số lượng tài liệu bắt buộc.

## Dấu vết phiên bản nguồn

SHA-256 trước/sau đọc được đối chiếu để bảo đảm hai file nguồn không bị thay đổi. Giá trị chuẩn tại lượt đọc ngày **12/10/2026**, múi giờ Asia/Bangkok:

| File | SHA-256 |
| --- | --- |
| Mau bao cao_Do an_Khoa luan_2025.docx | 25CE340FFA6C1931CFE59E2BE22AE689B8EAF76AC5068B1B25FE7913D79FEC35 |
| Ke hoach Do an mon hoc Nhap mon Big data_SV.docx | 7D1CF21EF1DAC4E791A0E765C3FC15353E95078F729A907B766C8E9779F95AD6 |

Các bản PDF/ảnh, đoạn trích có vị trí và bảng chỉ mục trong thư mục evidence là bằng chứng đọc nguồn. Chúng không là minh chứng sản phẩm đã cài đặt, đã chạy hay đã được giảng viên nghiệm thu.

## Giới hạn xác nhận

Đã đọc toàn bộ nội dung có trong **hai file được giao**, chưa đọc đề cương học phần, thông báo Classroom hoặc hướng dẫn miệng ngoài hai file. Chưa chọn đề tài, dữ liệu, baseline, kiến trúc hay công nghệ; chưa lập kế hoạch triển khai hoặc cài đặt sản phẩm. Tiêu chí đối chiếu và minh chứng dự kiến của RTM là diễn giải để rà soát, không phải một bộ tiêu chí chấm mới được GV xác nhận.

