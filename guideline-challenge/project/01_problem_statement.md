# Problem statement + downstream contract

## 1. Bài toán

Xây dựng bộ Guideline và Ontology chuẩn hóa cho bài toán gán nhãn 2D Road Elements (vạch kẻ đường, làn đường được phép di chuyển, và các đối tượng tham gia giao thông) trên tập dữ liệu BDD100K (`bdd100k`), giải quyết các thách thức thực tế về nứt vỡ/mờ nhạt vạch sơn, thời tiết bất lợi (mưa, đêm, tuyết), dải gạch chéo phân tách làn (gore zone), dải dừng/nhường đường (yield line), và ranh giới không rõ ràng trong hệ thống xe tự lái (Autonomous Driving Perception & Motion Planning).

Tài liệu này tham chiếu trực tiếp các quy chuẩn kỹ thuật và nghiên cứu quốc tế:
1. **Qatar Road Marking Guidelines** (`https://www.roadmarkingqatar.com/post/road-marking-guideline`): Quy định về vạch vàng đơn/đôi (solid/broken yellow), vạch trắng đơn/đôi (solid/broken white), vạch kết thúc làn (end of lane), và vạch tam giác nhường đường (yield line).
2. **Kognic Edge Cases in Autonomous Driving** (`https://www.kognic.com/articles/edge-cases-autonomous-driving`): Phân loại và xử lý các ca biên đặc thù trong xe tự lái (vạch mờ nhạt, thời tiết cực đoan, che khuất phức tạp, xung đột tín hiệu).
3. **ResearchGate Traffic Monitoring CV Metrics** (`https://www.researchgate.net/publication/386284928_Computer_Vision_for_Intelligent_Traffic_Monitoring_and_Control`): Tiêu chuẩn đo lường Computer Vision cho giám sát giao thông (Precision, Recall, mAP, IoU, Boundary F1, Chamfer/Fréchet distance, Fleiss' Kappa).
4. **Guideline Lane & Drivable Area v1** (`Guideline_Lane_Drivable_v1.docx` / `02_guideline.md`): Quy ước chuẩn hóa 10 mục về BBox, Polygon và Polyline cho BDD100K.

## 2. Downstream contract

1. **Downstream task / model / user:** Mô hình Đa nhiệm Multi-Task Learning (Detection + Segmentation + Lane Marking) phục vụ hệ thống ADAS/AD Perception (Lane Keeping Assist - LKA, Autonomous Emergency Braking - AEB, Motion Planning).
2. **Output annotation thực sự cần:**
   - **Bounding Box (Rectangle):** `car`, `truck`, `bus`, `pedestrian`, `rider`, `motorcycle`, `bicycle`, `traffic light`, `traffic sign`. Attributes: `occluded` (boolean), `truncated` (boolean).
   - **Drivable Area (Polygon):** `area/drivable` (làn ego đang di chuyển), `area/alternative` (làn kế cận xe có thể chuyển sang).
   - **Lane Marking (Polyline):** `lane/single white`, `lane/double white`, `lane/single yellow`, `lane/double yellow`, `lane/crosswalk`, `lane/road curb`, `lane/single other`.
3. **Failure gây hậu quả lớn nhất (Critical Decisions):**
   - **Critical Failure 1:** Tô nhầm vùng ngược chiều hoặc vùng cấm (gore zone) thành `area/drivable` làm xe đi nhầm làn (nguy cơ va chạm trực diện).
   - **Critical Failure 2:** Nhầm lẫn giữa `lane/double yellow` (vạch đôi nét liền cấm lấn làn) thành `lane/single white` đứt nét (cho phép đè vạch).
   - **Critical Failure 3:** Bỏ sót người đi bộ (`pedestrian`) hoặc tín hiệu đèn đỏ (`traffic light`) khi bị che khuất một phần.
   - **Critical Failure 4:** Bỏ sót hoặc gán sai vạch tam giác nhường đường (yield line) gây tai nạn tại nút giao.
4. **Escalation Path khi ambiguity không resolve được:**
   - Annotator tạo **CVAT Issue** trên giao diện tool (với các loại flag `UNCERTAIN_CLASS`, `UNCERTAIN_BOUNDARY`, `UNCERTAIN_SCOPE`, `ATTRIBUTE_CHECK`).
   - Escalate trực tiếp lên QA Lead / Mentor duyệt và quyết định rule trong bảng revision log (`08_revision_log.md`).

## 3. Scope

- **Trong scope (Bắt buộc label):**
  - Tất cả 10 class object instances rõ ràng hoặc bị che khuất/cắt mép nhưng vẫn đủ bằng chứng thị giác để nhận diện.
  - Mặt đường lưu thông hợp pháp trong tầm quan sát (`area/drivable` và `area/alternative`).
  - Các loại vạch sơn kẻ đường nhìn thấy được (vạch phân làn, vạch tim đường, vạch mép vỉa, vạch sang đường, vạch nhường đường).
- **Ngoài scope (Ignore):**
  - Bóng đổ của phương tiện/người/cột điện đổ xuống mặt đường.
  - Hình ảnh phản chiếu trên kính xe, gương chiếu hậu, vũng nước.
  - Hình in trên pano quảng cáo (billboard), biển hiệu thương mại.
  - Phương tiện ở xa ngoài tầm nhìn an toàn (kích thước $< 10 \times 10\text{ px}$ không thể nhận diện class).
- **Geometry tolerance:**
  - Bounding Box: Ôm sát biên đối tượng, lệch biên $\le 2\text{ px}$.
  - Polygon (Drivable Area): Lệch ranh giới lòng đường $\le 3\text{ px}$, tuyệt đối không tự cắt (no self-intersection, 0 lỗi).
  - Polyline (Lane Marking): Đi theo đường tim vạch kẻ đường, sai số lệch tim $\le 3\text{ px}$.

## 4. Output chấm được

Mọi quyết định gán nhãn trong tập blind test đều thuộc 4 nhóm và có thể kiểm tra trực tiếp trên file export CVAT (định dạng XML/ZIP):
- **LABEL:** Vẽ đúng shape (BBox/Polygon/Polyline), gán đúng class và attributes.
- **IGNORE:** Bỏ qua hoàn toàn đối tượng nằm trong danh mục exclusion.
- **UNKNOWN:** Vẽ shape vị trí quan sát được và gắn cờ Issue `UNCERTAIN_CLASS` / `UNCERTAIN_BOUNDARY`.
- **ESCALATE:** Gắn cờ Issue `UNCERTAIN_SCOPE` để chờ quy định bổ sung từ Lead.

## 5. Dữ liệu và giới hạn

- **Nguồn ảnh:** Dữ liệu BDD100K 2D (`data/bdd100k/`, định dạng JPG, độ phân giải $1280 \times 720$).
- **Số ảnh sử dụng trong bài:** 15 ảnh (gồm 4 ảnh `example`, 6 ảnh `calibration`, 5 ảnh `blind`).
- **Giới hạn đã biết:** Ảnh tĩnh độc lập (image-level annotations), không có chuỗi frame liên tục temporal; độ phân giải ban đêm và thời tiết mưa/tuyết có hiện tượng lóa sáng và nhòe nét ở cự ly xa.
