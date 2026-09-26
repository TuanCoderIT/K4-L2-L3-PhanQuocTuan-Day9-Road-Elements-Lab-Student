# QA/QC Reviewer Note & Inspection Checklist
## Tài liệu Hướng dẫn Kiểm duyệt Chất lượng Gán nhãn (QA/QC Manual)

**Project:** BDD100K 2D Road Elements & Lane Marking Annotation
**Dành cho:** QA Auditor, Reviewer, QC Lead & Mentors
**Phiên bản Guideline áp dụng:** Version v3

---

## 1. Tổng quan quy trình kiểm soát chất lượng

Tài liệu này hướng dẫn cách áp dụng các tiêu chuẩn đo lường (metrics) và quy trình kiểm duyệt chất lượng (QA/QC) cho dữ liệu gán nhãn giao thông thông minh. Mục tiêu là đảm bảo dữ liệu đạt độ chính xác cao nhất trước khi đưa vào huấn luyện mô hình xe tự hành (Autonomous Driving Perception).

Quy trình QA sẽ đánh giá chất lượng dựa trên ba trụ cột: **Tính đầy đủ (Completeness)**, **Độ chính xác hình học (Geometric Accuracy)**, và **Phân loại nhãn (Taxonomy Compliance)**. Bất kỳ lỗi nào phát hiện đều được phân loại theo mức độ nghiêm trọng để quyết định việc chấp nhận (Pass) hay trả về làm lại (Rework).

---

## 2. Thang đánh giá mức độ nghiêm trọng (Severity Matrix)

Mọi sai sót phát hiện trong quá trình kiểm tra (Audit) sẽ được phân loại vào một trong ba mức độ sau. Tỷ lệ lỗi ở các mức độ này sẽ quyết định chất lượng của toàn bộ lô dữ liệu (batch).

### 🔴 Critical (Nghiêm trọng)
Lỗi làm hỏng hoàn toàn thuật toán học máy hoặc gây nguy hiểm trong thực tế.
- **Bao gồm:** Sai class (VD: nhầm vạch cấm vượt `double yellow` thành vạch nét đứt cho phép chuyển làn); bỏ sót người đi bộ `pedestrian` hoặc đèn giao thông đỏ; vẽ `area/drivable` tràn lên làn ngược chiều hoặc vỉa hè.
- **Xử lý:** **Reject Task ngay lập tức**, yêu cầu Annotator làm lại 100% lô dữ liệu.

### 🟡 Major (Lỗi lớn)
Lỗi ảnh hưởng đáng kể đến độ chính xác IoU hoặc khoảng cách hình học.
- **Bao gồm:** Box vẽ quá rộng bao gồm cả bóng đổ (shadow); Polyline vẽ xuyên qua xe phía trước; Polygon bị tự cắt (self-intersection) không xuất file được; lầm lẫn giữa `car` và `truck`.
- **Xử lý:** Yêu cầu Annotator **Rework** sửa lại các đối tượng sai sót.

### 🟢 Minor (Lỗi nhỏ)
Lỗi không thay đổi tính chất dữ liệu nhưng làm giảm chất lượng tổng thể.
- **Bao gồm:** Quên gán thuộc tính `occluded` khi vật thể bị che một phần rất nhỏ ($< 10\%$); viền box lệch từ $3-5\text{ px}$ so với mép thực tế; polyline lệch tim $3-5\text{ px}$.
- **Xử lý:** Gửi phản hồi nhắc nhở Annotator tự khắc phục.

---

## 3. Hệ thống Metric đánh giá Computer Vision

Reviewer sử dụng các chỉ số (metrics) chuẩn trong ngành thị giác máy tính dưới đây để định lượng độ sai lệch giữa dữ liệu của Annotator và Ground Truth (Gold Standard). Nếu điểm số dưới ngưỡng Threshold, dữ liệu yêu cầu phải Rework.

| Nhóm đối tượng | Chỉ số (Metric) | Threshold | Mô tả & Cách ứng dụng |
|---|---|---|---|
| **Object Detection** (Bounding Box) | **IoU (Intersection over Union)** | $\ge 0.75$ | Đo lường mức độ khớp giữa Box vẽ và mép thực tế của xe/người. Box không được rộng hơn để chứa bóng đổ (làm giảm IoU) và không được cắt lẹm vào xe. Ngưỡng cho xe cộ là 0.75, với người đi bộ hoặc biển báo xa có thể linh động ở mức 0.65. |
| **Object Detection** (Bounding Box) | **mAP (Mean Average Precision)** | $\ge 85\%$ | Đánh giá tổng hợp lỗi bỏ sót (False Negative) và vẽ nhầm bóng đổ/hình quảng cáo (False Positive). Lô dữ liệu đạt chuẩn không được phép bỏ sót quá 5% số lượng đối tượng hiển thị rõ trên ảnh. |
| **Drivable Area** (Polygon) | **mIoU (Mean IoU)** | $\ge 0.90$ | Đo lường độ chính xác của phân vùng mặt đường. Bất kỳ phần Polygon nào lấn lên vỉa hè (sidewalk) hoặc đè lên làn alternative (overlap) sẽ làm sụt giảm mIoU nghiêm trọng. Các điểm biên cong phải đủ dày để bám sát mép. |
| **Lane Marking** (Polyline) | **Chamfer Distance (CD)** | $\le 3\text{ px}$ | Tính toán khoảng cách trung bình từ các điểm trên Polyline được vẽ tới tim đường chuẩn. Yêu cầu Polyline phải bám cực sát vào chính giữa (centerline) của vạch sơn. Khoảng cách chệch hướng vượt quá 3 pixel bị tính là Major Error. |
| **Tất cả hình học** | **Attribute Accuracy** | $\ge 90\%$ | Tỷ lệ gán đúng các thuộc tính (`occluded`, `truncated`). Việc đánh giá bám sát tình trạng hiển thị của vật thể tại mép ảnh và sau vật cản. |

> **Lưu ý khi tính toán:**
> Trong thực tế vận hành trên CVAT, Reviewer thường dùng mắt thường (Visual Audit) để ước lượng nhanh các chỉ số IoU và Chamfer Distance. Việc tính toán chính xác bằng thuật toán sẽ diễn ra trong giai đoạn Calibration hoặc Blind Test tự động.

---

## 4. Hướng dẫn thực thi quy trình QA từng bước

Để áp dụng các metric trên vào thực tế kiểm duyệt, QA Engineer / Reviewer cần tuân thủ quy trình 4 bước tiêu chuẩn dưới đây khi đánh giá một Task gán nhãn:

### Bước 1: Random Sampling (Lấy mẫu ngẫu nhiên)
Trong một lô dữ liệu (batch), chọn ngẫu nhiên từ $10\%$ đến $20\%$ số lượng frames để kiểm tra chi tiết. Ưu tiên tập trung vào các khung hình có điều kiện phức tạp: chói sáng, sương mù, mưa, hoặc mật độ xe cộ đông đúc (nút giao ngã tư).

### Bước 2: Visual & Metric Audit (Đối chiếu trực quan)
Reviewer phóng to (Zoom in) để kiểm tra:
1. Box có dính bóng đổ hay không? (Ước lượng IoU).
2. Polyline vạch đứt có được vẽ bằng 1 đường liền liên tục qua tim vạch hay không? (Đảm bảo Chamfer Distance).
3. Có bỏ sót vật thể nhỏ ở phía xa cuối đường không?
4. Polygon có lấn vỉa hè không?

### Bước 3: Resolution of Edge Cases (Kiểm tra xử lý ca khó)
Kiểm tra xem Annotator có tự ý đoán mò (guess) trong các trường hợp vạch sơn bị mòn, lóa sáng hay vật thể bị che khuất nặng hay không. Đảm bảo Annotator đã làm đúng quy trình: tạo Issue `UNCERTAIN_CLASS` hoặc `UNCERTAIN_BOUNDARY` thay vì label sai lệch dữ liệu.

### Bước 4: Scoring & Decision (Chấm điểm & Quyết định)
Dựa trên số lỗi tìm thấy, đưa ra quyết định cuối cùng cho Task:
- **PASS:** Không có lỗi Critical, số lỗi Minor dưới 5%.
- **REWORK (Làm lại):** Có bất kỳ 1 lỗi Critical nào, hoặc tỷ lệ lỗi Major/Minor vượt quá giới hạn.
- Ghi chú rõ ràng tọa độ và mô tả lỗi vào hệ thống để Annotator có cơ sở sửa đổi.
