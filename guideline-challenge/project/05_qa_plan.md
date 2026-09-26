# QA plan + quality gates

## 1. Flow

Quy trình bảo đảm chất lượng tuân theo mô hình 6 bước khép kín:
`Guideline v3` → `Calibration (Calibration Report)` → `Production Annotation` → `Self-QC (Checklist)` → `Review & Audit` → `Rework / Quality Gate`.

- **Ai review, review bao nhiêu:**
  - QA Auditor độc lập (Phạm Thị D) tiến hành review **100% dữ liệu** đối với các ảnh thuộc tag rủi ro cao (`critical`, `ambiguity`), và **20% sample ngẫu nhiên** đối với các ảnh thuộc tag `normal`.
- **Chọn sample theo rule nào:**
  - Ưu tiên chọn sample dựa trên danh sách tag rủi ro (`critical` $\rightarrow$ `ambiguity` $\rightarrow$ `edge` $\rightarrow$ `normal`), sample từ annotator mới gia nhập nhóm, và sample có số lượng object lớn $> 15\text{ objects/frame}$.
- **Issue được ghi ở đâu, đóng thế nào:**
  - Issue được ghi trực tiếp trên CVAT Tool bằng chức năng "Create Issue" tại đúng vị trí tọa độ bị lỗi.
  - Annotator tiến hành sửa lỗi theo phản hồi, đổi trạng thái Issue thành "Resolved". QA Lead kiểm tra lại và nhấn "Close Issue".
- **Khi phát hiện guideline gap thì update và version ra sao:**
  - Khi phát hiện tình huống mới chưa có trong quy tắc (guideline gap), QA Lead họp nhóm chốt cách xử lý, cập nhật bổ sung vào `02_guideline.md`, tăng `Version` (từ `v1` $\rightarrow$ `v2` $\rightarrow$ `v3`), đồng thời ghi nhận bằng chứng vào `08_revision_log.md`.

## 2. Defect severity

Bảng phân loại mức độ lỗi (Defect Severity Matrix) dựa trên hậu quả vận hành đối với hệ thống xe tự lái (downstream AD system):

| Severity | Định nghĩa cho project này | Ví dụ | Action mặc định |
|---|---|---|---|
| **Critical** | Lỗi làm sai lệch nghiêm trọng logic điều khiển an toàn xe tự lái (gây tai nạn hoặc đi sai làn đường cấm). | Tô `area/drivable` trùm lên làn ngược chiều; nhầm vạch cấm đè `double yellow` thành vạch đứt; bỏ sót người đi bộ `pedestrian` hoặc đèn đỏ `traffic light`. | **Reject Task immediately**, yêu cầu Annotator làm lại 100% batch. |
| **Major** | Lỗi gán sai class vật thể cùng nhóm hoặc sai lệch tọa độ geometry lớn hơn tolerance quy định. | Lầm lẫn giữa `car` và `truck`; Polygon `area/drivable` lệch ranh giới lòng đường $> 5\text{ px}$; BBox vẽ quá rộng ôm cả bóng đổ. | Yêu cầu Annotator **Rework** điều chỉnh lại các object bị lỗi. |
| **Minor** | Lỗi bỏ sót hoặc chọn sai attribute phụ mà không làm đổi class chính và vị trí vật thể. | Bỏ quên check `occluded=true` cho xe bị che 10%; Polyline lệch tim vạch sơn $3 - 5\text{ px}$. | Gửi thông báo feedback trực tiếp cho Annotator tự sửa. |
| **Question** | Tình huống mơ hồ, ảnh bị mờ nặng hoặc lóa sáng không đủ bằng chứng thị giác khẳng định. | Vật thể ở xa mờ ảo không rõ là biển báo hay cột đèn; vạch sơn bị đè lên bởi đống tuyết. | Tạo CVAT Issue `UNCERTAIN_CLASS` / `SCOPE` đẩy lên Lead/Mentor giải quyết. |

## 3. Metrics

Bảng chỉ số đo lường chất lượng dữ liệu và độ tương đồng giữa các annotator:

| Metric | Cách tính | Vì sao phù hợp với bài toán |
|---|---|---|
| **Bounding Box mAP@IoU 0.5** | Average Precision tại ngưỡng IoU $0.5$ cho 10 class object instance. | Đánh giá chính xác khả năng phát hiện vật thể rời rạc (phương tiện, người, biển báo) theo tiêu chuẩn MS-COCO / BDD100K. |
| **Polygon mIoU (Mean IoU)** | $\text{mIoU} = \frac{\text{TP}}{\text{TP} + \text{FP} + \text{FN}}$ trung bình trên 2 class `area/drivable` và `area/alternative`. | Đo độ phủ và độ chính xác của vùng lòng đường xe ego được phép di chuyển. |
| **Polyline Chamfer Distance** | Khoảng cách trung bình giữa các điểm trên polyline dự đoán và polyline chuẩn. | Đánh giá độ lệch tim đường và độ mượt hình học của vạch kẻ làn. |
| **Fleiss' Kappa ($\kappa$)** | Hệ số thống kê đo độ đồng thuận giữa $\ge 2$ annotator trên các quyết định phân loại class. | Đánh giá tính nhất quán dữ liệu calibration ($\kappa > 0.8$ đạt mức đồng thuận rất cao). |

- **Metric High-Risk (Critical Defect Escape Rate):**
  $$\text{Critical Escape Rate} = \frac{\text{Số lỗi Critical lọt qua bước Self-QC}}{\text{Tổng số sample review}} \times 100\%$$
  Yêu cầu bắt buộc: **$\text{Critical Escape Rate} = 0\%$** (tuyệt đối không để lọt bất kỳ lỗi Critical nào vào tập nộp cuối).

## 4. Quality gate

Tiêu chuẩn nghiệm thu chất lượng bài làm:

```text
PASS if:
  - Critical Defect Escape Rate = 0%
  - Polygon mIoU (Drivable Area) >= 90.0%
  - Bounding Box mAP@0.5 (Objects) >= 85.0%
  - Polyline Chamfer Distance <= 3.0 px
  - 100% ca mơ hồ (Question) đều đã được tạo Issue và chốt quyết định.

REWORK if:
  - Critical Defect Escape Rate = 0% nhưng mIoU hoặc mAP nằm trong khoảng 75.0% - 89.9%
  - Tỷ lệ lỗi Major > 5% tổng số annotations.

REJECT / ESCALATE if:
  - Phát hiện >= 1 lỗi Critical Defect trong batch nộp.
  - mIoU < 75.0% hoặc mAP < 70.0%.
  - Tỷ lệ lỗi Major > 15%.
```

- **Trade-off Cost vs. Risk:**
  Nhóm chấp nhận dành thêm $20\%$ thời gian sản xuất cho khâu Self-QC và Independent Review để triệt tiêu toàn bộ lỗi Critical Risk ($0\%$ escape rate). Điều này hạn chế tối đa rủi ro gây mất an toàn nguy hiểm cho mô hình điều khiển xe tự lái phía downstream, dù chi phí nhân công kiểm thử tăng nhẹ.
