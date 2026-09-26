# QA plan + quality gates

Kế hoạch kiểm thử chất lượng và các cổng kiểm soát (Quality Gates) cho dự án gắn nhãn Lane Boundary.

## Flow

Quy trình: Guideline → Calibration → Production → Self-QC → Review → Rework → Quality Gate.

- **Ai review, review bao nhiêu:**
  Vũ Ngọc Huyền (QA Owner) và Phan Quốc Tuấn (Spec Owner) chịu trách nhiệm review. Thực hiện review 100% các mẫu có gắn tag rủi ro (`critical`, `edge`, `ambiguity`) và rút mẫu ngẫu nhiên 30% đối với các mẫu `normal`.
- **Chọn sample theo rule nào:**
  Áp dụng lấy mẫu phân tầng theo rủi ro (Risk-based Stratified Sampling):
  1. 100% ảnh trời mưa/chói lóa/ban đêm (`low_visibility`).
  2. 100% ảnh có khu vực phân tách làn/nhập làn (`split`/`merge`).
  3. 100% ảnh có phương tiện che khuất (`occlusion`).
  4. Lấy ngẫu nhiên các ảnh đường thẳng quang đãng để kiểm tra độ trôi chất lượng (quality drift).
- **Issue được ghi ở đâu, đóng thế nào:**
  Mọi lỗi phát hiện được ghi chú trực tiếp qua tính năng Comment/Issue trên từng frame/object của CVAT và thống kê vào bảng review log. Issue chỉ được đóng (`Closed`) sau khi annotator sửa trực tiếp hình học/thuộc tính và QA Lead kiểm tra nghiệm thu.
- **Khi phát hiện guideline gap thì update và version ra sao:**
  Khi hai annotator hoặc QA gặp ca bất đồng không thể phân xử bằng guideline hiện tại: triệu tập họp nhanh 10 phút giữa Spec Owner và QA Owner $\rightarrow$ ban hành rule mới $\rightarrow$ cập nhật nội dung vào `02_guideline.md` và nâng version (ví dụ từ v1 lên v2, v2 lên v3) $\rightarrow$ ghi rõ lý do và bằng chứng vào `08_revision_log.md`.

## Defect severity

| Severity | Định nghĩa cho project này | Ví dụ | Action mặc định |
|---|---|---|---|
| Critical | Lỗi gây mất an toàn trực tiếp cho xe tự hành (tạo làn ảo hoặc dẫn xe vào dải phân cách) | Nối polyline xuyên qua xe khác; vẽ sai ranh giới vùng gore tại merge/split; nhầm vạch phản quang nước mưa thành vạch sơn | REJECT toàn bộ batch của annotator, yêu cầu sửa lại toàn bộ và tái đào tạo quy tắc |
| Major | Sai lệch lớn về ngữ nghĩa phân làn | Gán nhầm `laneStyle` (vạch liền thành vạch đứt); nhầm `laneTypes` (vàng thành trắng); vẽ vạch nứt nhựa đường | REWORK: Trả về annotator sửa các object bị gắn cờ trong vòng 15 phút |
| Minor | Sai lệch nhỏ về hình học hoặc thuộc tính phụ trợ | Polyline lệch tim vạch 4–6 px; chọn nhầm `visibility` giữa `faded` và `visible` | QA Owner sửa trực tiếp trên tool và ghi chú nhắc nhở annotator |
| Question | Tình huống bất định không đủ bằng chứng hình ảnh | Vạch sơn bị thi công chắp vá đè 2 lớp mờ nhạt | ESCALATE lên Spec Owner để thống nhất tiền lệ xử lý |

## Metrics

| Metric | Cách tính | Vì sao phù hợp với bài toán |
|---|---|---|
| Decision Accuracy ($D$) | Số quyết định thuộc tính/phân loại đúng / Tổng số quyết định | Đo lường độ hiểu đúng guideline của annotator đối với các ca biên |
| Geometry Alignment ($G$) | Tỷ lệ polyline đạt dung sai $\le 3$ px / Tổng số polyline | Đảm bảo quỹ đạo xe bám đúng tim làn, không rung lắc |
| Critical Escape Rate ($C_{\text{escape}}$) | Số lỗi Critical lọt qua khâu Review / Tổng số lỗi Critical | Chỉ số sống còn nhằm ngăn chặn rủi ro va chạm nghiêm trọng |

- **Chỉ tiêu rủi ro cao:** Critical Defect Escape Rate bắt buộc phải bằng **0%** trước khi bàn giao dữ liệu.

## Quality gate

```text
PASS if:
  - Critical Defect Escape Rate == 0%
  - Decision Accuracy >= 90%
  - Geometry Alignment >= 85%
REWORK if:
  - Decision Accuracy từ 80% đến dưới 90% HOẶC có 1 lỗi Critical do sơ suất thao tác (đã khoanh vùng được)
REJECT / ESCALATE if:
  - Decision Accuracy < 80% HOẶC có >= 2 lỗi Critical HOẶC phát hiện Guideline Gap mang tính hệ thống
```

**Trade-off:**
Chấp nhận dung sai hình học rộng hơn một chút ($\le 5$ px) ở các đoạn vạch sơn quá xa (trên 60 mét ở đường chân trời) nhằm tiết kiệm chi phí thời gian dán nhãn, nhưng kiên quyết áp dụng dung sai khắt khe $\le 3$ px và 0% lỗi critical ở khoảng cách gần dưới 40 mét trước đầu xe (vùng can thiệp phanh và đánh lái khẩn cấp).
