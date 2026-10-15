# Ghi chép dữ liệu và tiền xử lý M2

Ngày bắt đầu/cập nhật: **15/10/2026**. **M2 đã đóng: kỹ thuật toàn nguồn PASS trên TV1; TV2 review/chấp thuận, không còn điểm sửa theo xác nhận người dùng U-38.** Run cuối `d7fb3f21-115f-4793-a5fe-5c40b6da64cd`; kết quả/evidence ở cuối bản ghi. Các phần audit/lượt lỗi giữ rõ trình tự và giới hạn, không phải số liệu nghiệm thu thay thế.

## Nguồn và phạm vi

Online Retail II, Daqing Chen, DOI [10.24432/C5CG6D](https://doi.org/10.24432/C5CG6D), [UCI, CC BY 4.0](https://archive.ics.uci.edu/dataset/502/online+retail+ii). Dataset được GV chấp thuận **theo người dùng U-25**. XLSX dự kiến SHA-256 `bcbe73b35f5b7babf197fb0cb983a11f5d9ff929078d4aa53d171b1f2df2e980`; hai sheet Year 2009-2010 / Year 2010-2011, dự kiến 525.461 / 541.910 dòng, tám cột theo contract file 12 mục 10. Chưa gọi các số dự kiến là kết quả pipeline M2.

Giữ P-01/U-16, P-02/U-17/U-21, decimal text/U-28 và dashboard hàng hóa + audit/U-29. Ngày hóa đơn local, timezone UNKNOWN. Không bỏ khách thiếu, không gộp item theo tên, không cắt giỏ lớn. M2 chưa chia train/dev/test, không fit FP-Growth, tạo metrics, train catalog hoặc publication.

Schema/raw types đo lại trên 1.067.371 dòng (header giữ đúng thứ tự):

| Cột | Kiểu đã đọc / thiếu | Vai trò/cách dùng |
| --- | --- | --- |
| Invoice | 1.047.871 int, 19.500 text; không thiếu | ID hóa đơn chuỗi; tiền tố C audit hủy, không prefix sheet |
| StockCode | 932.385 int, 134.986 text; không thiếu | Danh tính item chuỗi, giữ case/mã chữ |
| Description | 1.062.985 text, 4 number, 4.382 null | Tên nguồn; không gộp theo tên, số sai kiểu ghi audit, raw giữ nguyên |
| Quantity | 1.067.371 int; không thiếu | Số lượng dòng, giữ khi set hóa giỏ |
| InvoiceDate | 1.067.371 datetime; không thiếu | Local datetime; min theo hóa đơn sau policy |
| Price | 1.057.347 float, 10.024 int; không thiếu | Decimal(str(value)), GBP theo UCI; không tính tổng bằng float |
| Customer ID | 824.364 int, 243.007 null | Chuỗi/null; không bắt buộc cho giỏ |
| Country | 1.067.371 text; không thiếu | Giữ raw, kiểm consistency; không thêm KPI ngoài scope |

Quy mô bytes XLSX 45.622.278; 1.067.371 dòng/8 cột, chồng lấn hai sheet và timestamp/mã/thiếu/điều chỉnh tạo nhu cầu lineage, shuffle và audit toàn nguồn. Không gọi đây là dữ liệu vượt năng lực máy đơn hoặc quy mô cluster chỉ từ số dòng; Spark local là lựa chọn U-09. Khoảng thời gian nguồn 01/12/2009–09/12/2011 theo profile hash cố định; không khẳng định múi giờ giao dịch.

## Quyết định và phương pháp

- Người dùng chọn MongoDB riêng loopback 27019, database `bigdata_m2`, dbpath `artifacts/m2/mongo-data` ngày 15/10/2026; cô lập mẫu M1/27018 và dịch vụ 27017. Ghi U-37 tại file 07.
- Đọc streaming bằng openpyxl 3.1.5; giữ nhãn kiểu và payload tám ô trước chuẩn hóa. Số theo `Decimal(str(value))`; number 1/1.0 bằng nhau nhưng text khác number.
- Spark đọc MongoDB thật qua connector đã pin trong M1; P-01 chọn vị trí nhỏ nhất theo tuple có kiểu. Audit độc lập đọc lại XLSX, dùng SQLite ngoài Git để giữ tập đã gặp và đo counts/tiền/giỏ mà không giữ toàn nguồn trong RAM Python.
- Precision/scale/config toàn nguồn sẽ được chọn sau khi đo miền giá trị; chưa lấy cấu hình fixture làm cấu hình M2.

## Môi trường, lỗi và bằng chứng đang thu thập

Git đầu phiên sạch, branch `main`, HEAD `d975e6c`. Python .venv có PySpark 4.2.0, PyMongo 4.18.3, NumPy 2.5.4. Bộ nhớ cũ nói M1 mở đã lỗi thời; STATE/U-35 hiện tại xác nhận M1 đóng.

Lỗi preflight: sandbox từ chối CIM; pip không phân giải pypi.org. Đã yêu cầu quyền chạy đúng lệnh ngoài sandbox để đọc process/tài nguyên và cài openpyxl/psutil trong .venv; không đổi PATH/registry/policy hoặc phần mềm toàn máy. Kết quả cài và preflight chờ receipt thực tế.

Evidence chi tiết đặt tại `artifacts/m2/` (ngoài Git): nguồn/hash, môi trường, audit độc lập, receipt import/batch, resource samples và logs. Counts, lineage, thời gian, RAM Python/JVM/MongoDB, đĩa sẽ cập nhật từ lượt chạy thật. RAM sampled RSS là tổng theo nhóm process tại các mẫu, không phải cấu hình heap hoặc RAM trống. Chưa đo trường nào phải giữ rõ chưa đo.

## Nghiệm thu và giới hạn hiện tại

Đã kiểm chứng pipeline tiền xử lý toàn nguồn TV1 và đọc lại output/BSON/hash. TV2 đã review/chấp thuận không còn điểm sửa theo người dùng U-38, đủ DoD; chưa full READY re-import cả workbook, chưa web/Java đọc dataset thật, chưa FP-Growth/split/evaluation và chưa full run máy TV2. M1 fixture/audit lịch sử giữ nguyên. Không mở M3/M4, commit/push hoặc ghi đóng góp/giờ-người.

## Audit độc lập đã chạy ngày 15/10/2026

Evidence: `artifacts/m2/audit-source-v1/audit.json`, `item-reference.json`, `invoice-examples.json`, SQLite `seen.sqlite`; measurement `artifacts/m2/audit-20261015T075717.json`. Đây là đọc lại XLSX, **chưa phải Spark**. Hash, hai sheet/header/count khớp nguồn. 1.067.371 raw − 34.335 trùng = 1.033.036 retained; trừ 25.123 không mua dương/hợp lệ = 1.007.913; trừ 4.556 nhóm P-02/TEST = 1.003.357 dòng hàng. Giữ 226.761 dòng hàng thiếu Customer ID. 39.516 giỏ / 4.895 mã; giá trị mua dương hàng hóa 19.643.861,637 GBP (không phải doanh thu ròng).

Miền toàn nguồn: Quantity −80.995..80.995, scale 0; Price −53.594,36..38.970, scale tối đa 3; phần nguyên tối đa 5 chữ số mỗi trường. Cấu hình Spark suy ra `quantity decimal(5,0)`, `price decimal(8,3)`, phép nhân `decimal(14,3)` và tổng dự kiến `decimal(24,3)`; còn phải kiểm tra schema và giá trị runtime, bật ANSI và không cho mất precision. Không cộng tiền qua double, không làm tròn từng dòng. Decimal bảo toàn giá trị số đã đọc theo contract, không khôi phục chính xác trước Excel.

Audit có 82 giỏ nhiều timestamp nhưng 0 nhiều ngày/khách/quốc gia và 0 giỏ hàng hóa xuất hiện qua cả hai sheet sau P-01. Không prefix sheet vào Invoice. Trong raw/retained có một collision chuẩn hóa StockCode: `47503J` (77 dòng retained) và `47503J ` (1 dòng), cùng mô tả `SET/3 FLORAL GARDEN TOOLS IN BAG`; bỏ whitespace ngoài đúng file 12 mục 10.2, không đổi chính sách hay gộp theo tên. P-01 vẫn so text gốc có khoảng trắng. Chi tiết `stock-normalization.json`; source row cụ thể còn chờ đọc MongoDB khi import đủ.

Audit đo 325,013 giây trong hàm; wrapper 327,792 giây, sampled peak RSS Python 315.183.104 byte (~300,6 MiB), không có JVM/Mongo trong nhóm process audit. Tổng byte tại artifacts/m2 khi wrapper kết thúc gồm cả import/Mongo đang chạy đồng thời nên **không phải dung lượng riêng audit**. Không coi hai thời gian này là giờ-người.

Preflight `preflight-20261015T075750.json`: Windows 11 x64 10.0.26200, i5-13500H, RAM tổng 16.786.550.784 byte; RAM khả dụng 3.803.860.992 byte và đĩa trống 124.536.606.720 byte lúc snapshot. MongoDB M2 riêng đã LISTENING theo receipt; chỉ dịch vụ 27017 nghe trước khi start. openpyxl 3.1.5/et-xmlfile 2.0.0/psutil 7.0.0 cài vào .venv thành công sau khi có quyền mạng.

## Import và kiểm chứng MongoDB thật

Import kết thúc 08:08 UTC (15:08 giờ Việt Nam) ngày 15/10; `import-1792051683308077200.json` PASS, đủ hai sheet 525.461/541.910 dòng, tổng 1.067.371. Dataset READY chỉ sau đối chiếu từng sheet/tổng. Hàm import 550,198 giây; wrapper `import-20261015T075852.json` 551,989 giây; sampled peak RSS Python/launcher 110,8 MiB, MongoDB 403,4 MiB, combined 508,9 MiB. File nguồn không ghi; archive lưu tám ô có kiểu + tuple_key và vị trí nguồn, khác bản sao bytes XLSX.

Probe `mongo-checks-20261015T080847.json`/`mongo-verification-*.json`: partial WRITING bị chặn; retry hai dòng synthetic không nhân bản; payload khác bị từ chối và đọc lại payload cũ không đổi. Dataset probe `m2-import-probe-0b63544d-34b3-4b62-a485-130589a5d679` giữ nhãn synthetic và hai dòng riêng để truy vết; không tính trong hash/count nguồn thật. Retry 1.000 dòng thật mỗi sheet, count trước/sau giữ 1.067.371; **chưa chạy lại full READY import cả workbook**, không suy phần đó từ probe. Wrapper 29,504 giây, sampled peak Python 71,0 MiB/Mongo 354,6 MiB/combined 425,6 MiB.

Ba hóa đơn 489434/489435/489436 tính riêng từ archive khớp audit; chi tiết từng dòng Quantity × Price và sheet/row trong `artifacts/m2/hand-invoices.json`. Ví dụ sheet 0, row 2: item 85048, 12 × 6,95 = 83,40 GBP. Mã có khoảng trắng cuối được truy vết tại sheet 0, row 260888 (`stock-normalization-lineage.json`); 77 + 1 là counts **retained** từ SQLite, không nhầm với số bản lặp raw tìm thấy trong MongoDB.

Chín unittest Python đạt (5 M2 + 4 fixture M1), log/measurement `unit-tests-20261015T080735.*`. Không chạy lại web/Java vì không sửa web; sample M1 giữ nguyên.

Nguồn kỹ thuật đối chiếu ngày 15/10: [openpyxl read-only/lazy loading và đóng workbook](https://openpyxl.readthedocs.io/en/stable/optimized.html), [Spark DecimalType tối đa precision 38](https://spark.apache.org/docs/4.2.0/api/python/reference/pyspark.sql/api/pyspark.sql.types.DecimalType.html), [MongoDB connector read FAILFAST/schema/partitioner](https://www.mongodb.com/docs/spark-connector/current/batch-mode/batch-read-config/). Các cấu hình cụ thể của dự án vẫn phải có receipt runtime, không suy PASS từ tài liệu.

## Lượt Spark đầu và lỗi thật

Run `34f6dd24-c5e8-42e6-80c4-3db26876d37c`, basket set `fc8b1469b178f68f88fbe23816fbdebbbe08de3eafb46fe63d47d221ee04f39f`; evidence `pipeline-<run_id>.json`, `spark-20261015T080917.*` và `resources-<run_id>.json` trong artifacts/m2. **FAIL**, không công bố: dù counts/lineage/tiền/giỏ/item/month và output Mongo đã khớp đối chiếu, ghi manifest bị `bson.errors.InvalidDocument: documents must have only string keys, key was 1`. Bảng phân phối dùng key Python int (kích thước giỏ); JSON file tự đổi key nhưng BSON không cho phép. Sửa key thành chuỗi trước lưu manifest; giữ run FAILED, output và log lượt đầu, chạy run UUID mới để kiểm lại toàn bộ; không sửa receipt FAIL thành PASS.

Đồng thời log có `TaskMemoryManager`/`HeapMemoryAllocator`/`UnsafeExternalSorter` và `OutOfMemoryError: Java heap space` từ shuffle, Spark phục hồi và tiếp tục; đây là áp lực heap có thật, **không phải lỗi native Hadoop cuối cùng chặn run**. Cấu hình đầu local[2]/768m/AQE coalesce đã dùng; peak sampled JVM 1.245 MiB, Python/launcher 194,8 MiB, Mongo 372,7 MiB, combined 1.779,2 MiB; wall 407,668 giây. RSS không bằng Java heap. Mốc OOM có cả trước bước giỏ, không quy toàn bộ lỗi cho một operator không có bằng chứng.

Sửa có căn cứ cho lượt sau: heap 1280m trong RAM trống còn thực đo; giữ 16 shuffle partition, tắt adaptive coalesce để tránh gom partition lớn. Cờ consistency chỉ cần biết nhiều giá trị khác nhau: so min/max không null tương đương countDistinct > 1, tránh Expand cho bốn distinct aggregate đồng thời. Không cắt giỏ/dòng, đổi policy, ép count hoặc làm tròn. Kiểm lại toàn nguồn/audit và immutable output trước lượt mới đủ điều kiện; kết quả chờ receipt.

## Encoding BSON và kết quả cuối

Lượt `7ea685bc-c5e5-4c37-a53f-db57663c4f13` chạy 288,731 giây, không còn OOM; checks tính toán/đối chiếu lúc đó PASS. Kiểm tra thêm phát hiện count nhỏ Python int bị PyMongo ghi BSON int32. Equality Python không phát hiện khác kiểu này. Đã sửa encoding recursive Int64, giữ bool/ID string; thêm regression round-trip BSON thật và kiểm `$type` toàn bộ output. Encoding `m2-bson-counts-int64-v1` tham gia basket-set hash, giữ nguyên dữ liệu/version thử cũ. Postcheck đã đánh dấu run 7ea685bc thành FAILED/INCOMPLETE do `POSTCHECK_BSON_INT32_COUNTS`; receipt PASS gốc giữ nguyên và **không dùng nghiệm thu contract**. Không sửa lịch sử thành PASS cuối.

Run nghiệm thu kỹ thuật: **`d7fb3f21-115f-4793-a5fe-5c40b6da64cd`**, máy TV1, stage `PREPROCESSING`, mode `FULL_SOURCE`. Basket set **`cae0d9e763ef38a086966d829fdeba9272f4d7fda7b61791bee9e9ba04b3287a`**. Dataset hash như đầu bản ghi; parser `openpyxl-3.1.5-typed-v1`, schema `m0-contract-v1`, policy `p01-first-p02-test-v1`. Git HEAD `d975e6ce768156b7b1549bcb64eabdb940268085`; mã chưa commit được hash trong receipt và measurement, không gọi là mã đã commit. Code của các lượt đầu có hash riêng, giữ đúng evidence tương ứng.

| Stage tuần tự | Dòng còn | Loại tại bước |
| --- | ---: | ---: |
| Raw hai sheet | 1.067.371 | — |
| P-01 giữ dòng đầu | 1.033.036 | 34.335 |
| Mua dương/mã/ngày hợp lệ | 1.007.913 | 25.123 |
| Hàng hóa sau P-02/TEST | 1.003.357 | 4.556 |

Counts cân bằng đủ ba phương trình contract. Trong hàng hóa giữ **226.761 dòng thiếu khách**; **39.516 giỏ**, **4.895 item**, **3.208 giỏ một item / 36.308 từ hai item**. Trung vị 15, P95 73, P99 197, max **1.108 item/giỏ**, trung bình 25,105; percentile nearest-rank trên 39.516 giỏ, không cắt tail. 5.347 summaries = 4.895 item + 25 tháng + 426 kích thước + 1 quality. Tổng giá trị mua dương hàng hóa exact **19.643.861,637 GBP**, tổng positive_valid **20.476.260,448 GBP**; không gọi doanh thu ròng. Toàn bộ item/month và checksum giỏ khớp audit độc lập.

P-01 Spark đối chiếu count + bốn tổng limb SHA-256 vị trí với audit SQLite; 8/13 partition và đảo chiều đọc Mongo vẫn cùng checksum. Giỏ canonical/sort Invoice có SHA-256 `982ab870ab7f8118cdada770c9269fa0e464f2a789c778f9f0289ad852b8c05d`. Checksum logic có xác suất va chạm, không thay chứng minh toán học; fixture riêng kiểm number/text, whitespace/case/null/ngày và khác Quantity/Price. Mười unittest cuối đạt (6 M2 + 4 M1), `unit-final-20261015T082201.*`.

File `data/processed/m2/<basket_set_id>/<run_id>/retained-lines.jsonl`: **1.033.036 dòng / 413.222.079 byte**, SHA-256 `82ddde19db72b295d723ebb3ca1068ccbabf3a44a49d8ab396598842e5bc5c74`; có source_id/sheet/row, Quantity/Price/line_value và flags. Full eight cells giữ ở Mongo archive. Đọc lại file/hash/count đạt; source XLSX cuối vẫn đúng hash đầu. Trạng thái run Mongo `VALIDATED`, basket set `READY`; không có publication/catalog/model/metrics. `FULL_SOURCE PREPROCESSING` không phải `FULL_RUN M6`.

### Thời gian/RAM/đĩa lượt cuối

`spark-int64-20261015T082151.*`, `resources-d7fb3f21-115f-4793-a5fe-5c40b6da64cd.json`. Wall wrapper **301,032 giây**; batch kết thúc **15:26:49 giờ Việt Nam**. Sample RSS cách khoảng 1 giây, tách Python/launcher–JVM–Mongo, bao gồm shared pages và bỏ sót peak giữa mẫu; đây không phải heap config/private RAM. Peak từng nhóm không nhất thiết cùng thời điểm.

| Bước | Giây | Python/launcher peak MiB | JVM peak MiB | Mongo peak MiB | Combined peak MiB |
| --- | ---: | ---: | ---: | ---: | ---: |
| Startup + fixture | 26,790 | 182,8 | 500,4 | 359,1 | 957,5 |
| Đọc Mongo đầy đủ | 54,659 | 98,1 | 1.647,0 | 371,9 | 2.115,9 |
| P-01 + ổn định lineage | 91,055 | 98,1 | 1.700,6 | 377,1 | 2.157,7 |
| Quality/P-02 | 28,428 | 98,1 | 1.518,1 | 360,4 | 1.976,5 |
| Xuất dòng hàng | 49,014 | 104,6 | 1.483,3 | 360,3 | 1.947,1 |
| Giỏ/summaries/đối chiếu | 28,880 | 185,6 | 1.717,0 | 360,3 | 2.262,9 |
| Ghi/đọc lại Mongo | 17,599 | 195,3 | 1.717,2 | 361,9 | 2.272,7 |

Peak toàn lượt Python/launcher **195,27 MiB**, JVM **1.717,21 MiB**, Mongo **377,06 MiB**, combined **2.272,68 MiB**. Cấu hình local[2], driver heap 1280m, 16 shuffle partition, AQE coalesce tắt; WiredTiger cache 0,25 GiB chỉ là config. Không suy từ các số này rằng FP-Growth/full run hai máy sẽ vừa RAM.

Đĩa đo tổng kích thước file logic ở cuối từng step: scratch lớn nhất trong các snapshot **747.811.343 byte**, processed lượt cuối **413.222.079 byte**, Mongo dbpath cuối step ghi **508.196.579 byte** (bao gồm nguồn + probe + cả basket set thử). Không gọi đây là allocated bytes/peak đĩa chính xác hoặc dung lượng riêng dataset. Scratch có thể được Spark tự dọn khi stop; output/evidence các lượt vẫn giữ. Chi tiết từng step/đĩa trước–sau nằm resource/measurement JSON, không tính cache cấu hình thành usage.

### Evidence, tái tạo và phần review

- [Receipt pipeline cuối](../artifacts/m2/pipeline-d7fb3f21-115f-4793-a5fe-5c40b6da64cd.json), [postcheck BSON/file/source](../artifacts/m2/final-verification-d7fb3f21-115f-4793-a5fe-5c40b6da64cd.json), [tài nguyên từng bước](../artifacts/m2/resources-d7fb3f21-115f-4793-a5fe-5c40b6da64cd.json). Postcheck 15:40:25 giờ Việt Nam đạt; không coi thời gian chờ/điều phối là runtime job.
- [Hướng dẫn/lệnh tái tạo mục 6](../pipeline/README.md); `m2_source.py` audit/import, `m2_pipeline.py` tiền xử lý, `m2_verify_mongo.py` partial/retry/hóa đơn, `m2_final_verify.py` đọc lại output. Mỗi lượt có manifest/code/config/hash; receipt/log/raw/output bị Git ignore, clone không mang evidence cục bộ.
- Kiểm repository: 50 file bảo vệ không đổi so với HEAD, gồm Word nguồn/RTM/audit lịch sử/fixture M1; 282 ID RTM/map khớp. `repository-protection.json` giữ hash. Không đọc/render lại Word trong M2; truy vết theo RTM/source extract có sẵn, không tự gán xác nhận GV độc lập.
- **Review đã xác nhận U-38:** người dùng trả lời “TV2 đã review và chấp thuận, không còn điểm sửa” sau câu hỏi gắn run cuối/M2 notes/Guide mục 6/checkpoint và schema/lineage/counts/mapping/giỏ/tiền/hóa đơn/tái tạo. Đóng DoD M2 theo xác nhận người dùng; Agent không thay review, không nhận thông báo riêng trực tiếp từ TV2. U-25 đã có, không hỏi duyệt dataset lại. Receipt runtime PENDING_TV2 giữ snapshot trước xác nhận; `artifacts/m2/review-20261015.json` ghi xác nhận riêng. Không suy review thành runtime TV2; chưa mở M3/M4.

Bảng/hình hữu ích cho báo cáo: bảng stage trên; bảng quality có mẫu số raw/retained và lý do chồng nhau riêng; CDF/histogram kích thước giỏ có tail 1.108; số hóa đơn/giá trị mua dương theo 25 tháng (min thời gian hóa đơn, cùng scope); sơ đồ XLSX→archive Mongo→Spark→dòng/giỏ/summaries. Mỗi hình ghi dataset/policy/basket-set/run, đơn vị và mẫu số. Không tự kết luận chất lượng gợi ý hoặc đóng góp cá nhân.

Lifecycle cuối: shutdown MongoDB M2 bình thường, kiểm đúng PID/executable/hash/start/command/listener theo receipt; `stop-20261015T084344.json` ghi STOPPED, listener 27019 = 0, dữ liệu giữ nguyên. Preflight cuối `preflight-20261015T084347.json` chỉ còn loopback 27017/PID 5572 nghe, không có 27018/27019/8081. Không reset/drop/xóa output, sửa PATH/policy, commit hoặc push. **M2 đủ AC/DoD theo runtime/postcheck và U-38, bàn giao rồi dừng.**

### Bàn giao tài liệu sang M3 — U-39, 15/10/2026

Đã đối chiếu Master Plan/checklist/receipt/U-38: không còn confirm/demo riêng cần thêm để đóng M2. [Prompt tiếp nối M3](../requirements-review/M3_START_PROMPT.md) giữ ngữ cảnh/IDs/counts/giới hạn và yêu cầu ghi báo cáo ngay khi chạy vào `reports/M3_MODEL_DEVELOPMENT_NOTES.md`. Bản ghi M2 tiếp tục là bằng chứng tiền xử lý toàn kỳ; train/dev/test/model/metrics sẽ có scope và evidence riêng, không đổi số M2 thành số train. Phiên soạn prompt không fit/chạy lại pipeline, đọc lại DB sống hoặc tạo số đo runtime mới; chỉ xác minh tài liệu/artifact cục bộ và hash. M3 chưa triển khai; không commit/push.
