# Edge-case library

Thư viện 10 Edge Cases tiêu biểu cho bài toán Gán nhãn 2D Road Elements & Lane Boundaries trên tập BDD100K, tích hợp quy chuẩn Qatar Road Marking, Kognic Autonomous Driving Edge Cases và ResearchGate CV Metrics.

---

CASE ID: CASE-01
Sample: BDD03
Scene: Highway curved road overcast daytime
Observation: Vạch sơn mép trái màu vàng nét liền trên cao tốc cong; bên ngoài là dải cỏ và lề đường.
Decision: LABEL
Expected: Polyline `lane/single yellow` bám theo tim vạch vàng; Polygon `area/drivable` bám sát vạch vàng, không tô lên dải cỏ.
Rationale: Theo Qatar Guideline, Single Solid Yellow Line thể hiện mép trái lòng đường phân chia với dải phân cách. Tô tràn ra dải cỏ sẽ gây lỗi xe tự lái lao ra khỏi đường.
Common mistake: Tô Polygon `area/drivable` trùm lên dải cỏ bên trái.
Diversity: ambiguous_semantics

---

CASE ID: CASE-02
Sample: BDD04
Scene: City street two-way daytime
Observation: Tim đường có vạch đôi màu vàng nét liền (Double Solid Yellow Line) chia 2 chiều xe chạy.
Decision: LABEL
Expected: 1 Polyline `lane/double yellow` vẽ chính xác vào khoảng hở giữa 2 nét sơn; Polygon `area/drivable` chỉ tô làn xe ego, cấm tô làn ngược chiều.
Rationale: Qatar Guideline quy định Double Solid Yellow Line là vạch cấm vượt và cấm đè vạch tuyệt đối. Tô làn ngược chiều thành `area/drivable` là Critical Defect (xe tự lái đi đấu đầu).
Common mistake: Dùng 2 polyline riêng cho từng vạch sơn, hoặc tô `area/drivable` trùm sang làn ngược chiều.
Diversity: critical_risk

---

CASE ID: CASE-03
Sample: BDD06
Scene: Highway overcast dashed white line
Observation: Vạch phân làn nét đứt màu trắng (`lane/single white`) chạy dài trên cao tốc nhiều làn.
Decision: LABEL
Expected: 1 Polyline `lane/single white` duy nhất vẽ đè bám theo đường tim nối các sọc sơn đứt đoạn; ngắt polyline tại cản sau xe con phía trước.
Rationale: Quy chuẩn geometry Polyline quy định không ngắt đứt polyline theo từng sọc sơn để mô hình lane detection dự đoán liên tục.
Common mistake: Ngắt polyline thành từng nét nhỏ lẻ, hoặc vẽ đè xuyên qua thân xe đi trước.
Diversity: occlusion

---

CASE ID: CASE-04
Sample: BDD07
Scene: Highway intersection clear daytime
Observation: Đèn tín hiệu giao thông treo phía trên làn rẽ trái phụ.
Decision: LABEL
Expected: BBox `traffic light` ôm sát hộp vỏ đèn; gán attribute `occluded=false`, `truncated=false`.
Rationale: Mọi cụm đèn tín hiệu giao thông quan sát được đều bắt buộc gán nhãn BBox để mô hình perception phát hiện trạng thái đèn.
Common mistake: Bỏ sót đèn giao thông vì cho rằng xe ego đang đi làn thẳng không rẽ trái.
Diversity: small_far

---

CASE ID: CASE-05
Sample: BDD10
Scene: City street intersection yield line
Observation: Vạch sơn hàng hình tam giác (Yield Line) tại điểm giao cắt ngõ ra đường chính.
Decision: LABEL
Expected: Polyline `lane/single other` nối ngang qua chân các tam giác nhường đường.
Rationale: Theo Qatar Guideline, Yield Line gồm hàng tam giác màu trắng chỉ dẫn phương tiện phải giảm tốc/dừng nhường đường.
Common mistake: Bỏ qua không gán nhãn vì không phải vạch thẳng tiêu chuẩn.
Diversity: conflicting_road_elements

---

CASE ID: CASE-06
Sample: BDD11
Scene: City street overcast pedestrian crossing
Observation: Vạch người đi bộ qua đường (Crosswalk) cắt ngang lòng đường cùng người đi bộ đang di chuyển.
Decision: LABEL
Expected: Polyline `lane/crosswalk` bao biên cụm vạch; BBox `pedestrian` cho người đi bộ bị xe đỗ che lấp phần chân (`occluded=true`).
Rationale: Bảo vệ an toàn nhóm đối tượng yếu thế (VRU - Vulnerable Road User). Bỏ sót người đi bộ là lỗi Critical.
Common mistake: Bỏ sót attribute `occluded=true` hoặc gộp người đi bộ với xe đỗ xung quanh.
Diversity: critical_risk

---

CASE ID: CASE-07
Sample: BDD12
Scene: City street intersection degraded markings
Observation: Mặt đường ngã tư bị mờ nát vạch sơn nghiêm trọng do sương mù và nước đọng, không rõ ranh giới làn đường.
Decision: ESCALATE
Expected: Tạo CVAT Issue loại `UNCERTAIN_SCOPE` kèm ghi chú nghi ngờ ranh giới làn.
Rationale: Kognic Edge Case quy định không tự ý đoán mò ranh giới làn khi không đủ bằng chứng thị giác, phải chuyển lên Lead xử lý.
Common mistake: Tự suy đoán vẽ polygon tràn qua ngã tư theo cảm tính.
Diversity: escalation

---

CASE ID: CASE-08
Sample: BDD13
Scene: City street double solid white lines
Observation: Vạch trắng đôi song song nét liền (`lane/double white`) phân cách làn xe buýt / carpool với làn xe cơ giới.
Decision: LABEL
Expected: 1 Polyline `lane/double white` ở giữa 2 nét vạch; Polygon `area/drivable` dừng lại ở ranh giới vạch trắng đôi.
Rationale: Qatar Guideline quy định Double Solid White Line là ranh giới cấm chuyển làn/cấm đè vạch giữa làn thông thường và làn ưu tiên.
Common mistake: Vẽ đè `area/drivable` trùm qua vạch trắng đôi vào làn xe buýt.
Diversity: conflicting_road_elements

---

CASE ID: CASE-09
Sample: BDD14
Scene: Highway rainy weather faded line
Observation: Vạch sơn nét liền mép trái bị mờ nhạt do mưa ẩm ướt trên đường cao tốc; xe tải ở góc trái sát biên ảnh.
Decision: LABEL
Expected: Polyline `lane/single yellow` bám theo phần vạch còn nhìn thấy; BBox `truck` với `truncated=true`.
Rationale: BBox sát ranh giới biên ảnh bắt buộc bật `truncated=true` theo quy ước visibility.
Common mistake: Quên không bật `truncated=true` cho xe bị cắt ở mép ảnh.
Diversity: truncation

---

CASE ID: CASE-10
Sample: BDD15
Scene: Residential street parked cars
Observation: Dãy xe con đỗ sát mép đường bên phải, chiếm một phần lòng đường.
Decision: LABEL
Expected: BBox `car` cho từng xe đỗ; Polygon `area/drivable` vẽ bám sát mép bánh xe đỗ, dừng lại tại mép bánh xe không tô trùm lên thân xe.
Rationale: Lòng đường bị xe đỗ chiếm chỗ thì vùng xe ego di chuyển phải thu hẹp lại bám sát biên xe đỗ.
Common mistake: Tô Polygon `area/drivable` xuyên qua bên dưới gầm xe hoặc chèn lên thân xe.
Diversity: ambiguity
