# Problem statement + downstream contract

<<<<<<< HEAD
## 1. Bài toán
=======
Tối đa nửa trang, viết **trước khi mở CVAT**. Đây là bằng chứng của gate G1 (topic lock).
>>>>>>> 02cdd5326e0beb55bcaf28193ee8968a84d847c0

Xây dựng bộ Guideline và Ontology chuẩn hóa cho bài toán gán nhãn 2D Road Elements (vạch kẻ đường, làn đường được phép di chuyển, và các đối tượng tham gia giao thông) trên tập dữ liệu BDD100K (`bdd100k`), giải quyết các thách thức thực tế về nứt vỡ/mờ nhạt vạch sơn, thời tiết bất lợi (mưa, đêm, tuyết), dải gạch chéo phân tách làn (gore zone), dải dừng/nhường đường (yield line), và ranh giới không rõ ràng trong hệ thống xe tự lái (Autonomous Driving Perception & Motion Planning).

<<<<<<< HEAD
Tài liệu này tham chiếu trực tiếp các quy chuẩn kỹ thuật và nghiên cứu quốc tế:
1. **Qatar Road Marking Guidelines** (`https://www.roadmarkingqatar.com/post/road-marking-guideline`): Quy định về vạch vàng đơn/đôi (solid/broken yellow), vạch trắng đơn/đôi (solid/broken white), vạch kết thúc làn (end of lane), và vạch tam giác nhường đường (yield line).
2. **Kognic Edge Cases in Autonomous Driving** (`https://www.kognic.com/articles/edge-cases-autonomous-driving`): Phân loại và xử lý các ca biên đặc thù trong xe tự lái (vạch mờ nhạt, thời tiết cực đoan, che khuất phức tạp, xung đột tín hiệu).
3. **ResearchGate Traffic Monitoring CV Metrics** (`https://www.researchgate.net/publication/386284928_Computer_Vision_for_Intelligent_Traffic_Monitoring_and_Control`): Tiêu chuẩn đo lường Computer Vision cho giám sát giao thông (Precision, Recall, mAP, IoU, Boundary F1, Chamfer/Fréchet distance, Fleiss' Kappa).
4. **Guideline Lane & Drivable Area v1** (`Guideline_Lane_Drivable_v1.docx` / `02_guideline.md`): Quy ước chuẩn hóa 10 mục về BBox, Polygon và Polyline cho BDD100K.
=======
Nhận diện và phân định ranh giới làn đường (Lane Boundary) bằng Polyline tại các khu vực phức tạp: nút giao nhập/tách làn (merge/split), khu vực có vạch sơn bị mờ do thời tiết/mài mòn và vạch phân làn tạm thời do thi công.
>>>>>>> 02cdd5326e0beb55bcaf28193ee8968a84d847c0

## 2. Downstream contract

<<<<<<< HEAD
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
=======
1. **Downstream task / model / user là ai?**
   Module Định vị làn đường (Lane Keeping Assist - LKA, Lane Centering) và Lập quỹ đạo di chuyển (Trajectory Planning) của hệ thống xe tự hành ADAS cấp độ L2+/L3.
2. **Output annotation nào thực sự cần?**
   - Geometry: `Polyline` chạy dọc theo tâm của từng đoạn vạch kẻ đường nhìn thấy được.
   - Classes & Attributes:
     - Class: `lane_marking`
     - Attribute `lane_style`: `solid` (vạch liền), `dashed` (vạch đứt), `double` (vạch đôi).
     - Attribute `lane_type`: `white` (trắng), `yellow` (vàng), `other`.
     - Attribute `lane_direction`: `parallel` (song song hướng đi), `vertical` (vạch ngang/vạch dừng/người đi bộ).
     - Attribute `lane_status`: `normal` (rõ), `faded` (mờ), `temporary` (vạch thi công/phân luồng tạm).
     - Attribute `needs_review`: `false`, `true` (dùng để escalate ca bất định).
3. **Failure nào gây hậu quả lớn nhất?**
   - Failure critical: Vẽ sai ranh giới vùng nhập/tách làn (gore area) dẫn đến xe hiểu nhầm làn chạy và đâm vào dải phân cách/đảo giao thông; hoặc nối vạch xuyên qua thân xe khác phía trước tạo ra làn ảo không có thật trên thực tế.
4. **Khi ambiguity không resolve được, ai / ở đâu là escalation path?**
   - Khi vạch bị mòn biến mất cục bộ trên 15 mét hoặc có nhiều lớp vạch đè lên nhau không thể suy đoán: Annotator vẽ theo phần nhìn thấy chắc chắn nhất, bật cờ attribute `needs_review = true` và ghi chú vào decision log gửi Spec Owner / QA Lead phân xử.
>>>>>>> 02cdd5326e0beb55bcaf28193ee8968a84d847c0

## 3. Scope

<<<<<<< HEAD
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
=======
- **Trong scope (bắt buộc label):**
  - Mọi vạch sơn kẻ đường nhìn thấy được (vạch phân làn, vạch tim đường, vạch mép đường, vạch sơn khu vực merge/split).
  - Vạch người đi bộ qua đường (crosswalk) và vạch dừng (stop line).
  - Vạch bị mờ một phần nhưng vẫn suy luận được phương hướng và mắt người nhận diện được.
- **Ngoài scope (ignore):**
  - Vết nứt nhựa đường, vệt trám bitum, vết hằn lốp xe đen trên mặt đường.
  - Bóng đổ của cây cối, xe cộ, tòa nhà hoặc lan can cầu.
  - Gờ bó vỉa (curb) bằng bê tông nếu không có vạch sơn kẻ phân làn riêng biệt.
- **Geometry tolerance:**
  - Polyline phải đi qua tim vạch sơn, sai số lệch tâm $\le 3$ px.
  - Vạch đứt (dashed line) được vẽ thành 1 polyline duy nhất nối qua tâm các đoạn vạch đứt, không ngắt quãng từng nét nhỏ.
  - Khi vạch bị che khuất (occluded) bởi xe khác: dừng polyline ngay tại mép vật cản, tuyệt đối không nối xuyên qua xe.
>>>>>>> 02cdd5326e0beb55bcaf28193ee8968a84d847c0

## 4. Output chấm được

<<<<<<< HEAD
Mọi quyết định gán nhãn trong tập blind test đều thuộc 4 nhóm và có thể kiểm tra trực tiếp trên file export CVAT (định dạng XML/ZIP):
- **LABEL:** Vẽ đúng shape (BBox/Polygon/Polyline), gán đúng class và attributes.
- **IGNORE:** Bỏ qua hoàn toàn đối tượng nằm trong danh mục exclusion.
- **UNKNOWN:** Vẽ shape vị trí quan sát được và gắn cờ Issue `UNCERTAIN_CLASS` / `UNCERTAIN_BOUNDARY`.
- **ESCALATE:** Gắn cờ Issue `UNCERTAIN_SCOPE` để chờ quy định bổ sung từ Lead.
=======
- **LABEL**: Polyline đúng vị trí tim vạch, đúng attribute `lane_style`, `lane_type`, `lane_direction`.
- **IGNORE**: Không xuất hiện polyline trên các vết nứt nhựa đường, vết trám hoặc bóng đổ.
- **ESCALATE / UNKNOWN**: Gán attribute `needs_review = true` đối với các vạch bị mờ ngắt quãng dài hoặc vạch chồng chéo gây tranh cãi.
- Mọi quyết định đều được xuất và kiểm tra tự động qua file CVAT XML annotation export.
>>>>>>> 02cdd5326e0beb55bcaf28193ee8968a84d847c0

## 5. Dữ liệu và giới hạn

<<<<<<< HEAD
- **Nguồn ảnh:** Dữ liệu BDD100K 2D (`data/bdd100k/`, định dạng JPG, độ phân giải $1280 \times 720$).
- **Số ảnh sử dụng trong bài:** 15 ảnh (gồm 4 ảnh `example`, 6 ảnh `calibration`, 5 ảnh `blind`).
- **Giới hạn đã biết:** Ảnh tĩnh độc lập (image-level annotations), không có chuỗi frame liên tục temporal; độ phân giải ban đêm và thời tiết mưa/tuyết có hiện tượng lóa sáng và nhòe nét ở cự ly xa.
=======
- **Nguồn ảnh**: 26 ảnh từ tập `data/bdd100k/` (BDD01 đến BDD26).
- **Đặc điểm dữ liệu**: Ảnh chụp từ camera hành trình góc nhìn ego-vehicle (1280x720), bao gồm đường cao tốc (highway), đường phố đô thị (city street), khu dân cư với nhiều điều kiện thời tiết (nắng, nhiều mây, mưa, tuyết, chạng vạng và ban đêm).
- **Giới hạn**: Không có chuỗi frame liên tiếp theo thời gian (ảnh đơn), một số ảnh bị chói lóa kính chắn gió hoặc vạch sơn quá xa (dưới 20 px) khó xác định màu sắc chính xác.
>>>>>>> 02cdd5326e0beb55bcaf28193ee8968a84d847c0
