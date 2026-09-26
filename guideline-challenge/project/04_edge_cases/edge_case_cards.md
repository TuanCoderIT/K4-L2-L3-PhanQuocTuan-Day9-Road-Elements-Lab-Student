# Edge-case library

<<<<<<< HEAD
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
=======
Thư viện các ca biên (Edge-case library) hỗ trợ đào tạo annotator và đối chiếu khi nghiệm thu.

---

CASE ID: EC-01
Sample: BDD01
Scene: Đường cao tốc ban ngày, mật độ xe trung bình
Observation: Xe SUV phía trước che khuất một đoạn vạch liền và vạch đứt bên trái
Decision: LABEL
Expected: Dừng polyline chính xác tại góc sau xe SUV, không nối dài qua thân xe; polyline đạt dung sai <= 3px
Rationale: Tránh tạo làn ảo cho module Trajectory Planning khi xe phía trước đang chắn đường
Common mistake: Kéo polyline đi xuyên qua gầm hoặc nóc xe phía trước
Diversity: occlusion

---

CASE ID: EC-02
Sample: BDD02
Scene: Ngã tư đường phố đô thị có vạch dừng và vạch kẻ người đi bộ
Observation: Các dải sơn trắng bản rộng cắt ngang làn đường xe chạy
Decision: LABEL
Expected: Gán nhãn polyline ngang đường, laneDirection=vertical, laneTypes=crosswalk
Rationale: Phân biệt rõ ràng giữa vạch dẫn hướng làn xe chạy và vạch cảnh báo người đi bộ
Common mistake: Gán nhầm laneDirection=parallel như làn đường thông thường
Diversity: conflict

---

CASE ID: EC-03
Sample: BDD03
Scene: Đường cao tốc đoạn uốn cong hình chữ S
Observation: Vạch sơn liền màu trắng uốn lượn liên tục, có vết ghép nối nhựa đường song song
Decision: LABEL
Expected: 1 polyline duy nhất bám theo tim vạch sơn màu trắng, laneStyle=solid; bỏ qua vết nối nhựa đường
Rationale: Giúp module Lane Centering giữ xe ổn định giữa tâm làn khi vào cua gắt
Common mistake: Nhầm vết nối rãnh bê tông là vạch phân làn phụ
Diversity: ambiguity

---

CASE ID: EC-04
Sample: BDD05
Scene: Nút giao phân nhánh tách làn (highway split gore)
Observation: Vạch sơn chữ V mở rộng phân chia làn đi thẳng và nhánh rẽ phải, bên trong có vạch sơn chéo
Decision: LABEL
Expected: Vẽ polyline bám sát hai đường biên ngoài của vùng gore, laneStyle=solid, laneTypes=single white; không vẽ theo các nét sọc chéo phụ
Rationale: Tránh trường hợp xe tự hành lái chệch vào vùng đệm dẫn tới đâm vào dải phân cách cứng
Common mistake: Bẻ nhánh polyline đi vào từng vạch sơn sọc chéo bên trong
Diversity: critical

---

CASE ID: EC-05
Sample: BDD06
Scene: Đường cao tốc buổi chiều, ánh nắng phản chiếu qua kính chắn gió
Observation: Kính lái bị chói lóa sáng làm mờ gần như hoàn toàn vạch kẻ ở cự ly trên 40 mét
Decision: LABEL
Expected: Vẽ đoạn vạch nhìn thấy rõ ở cự ly gần; đoạn xa gán visibility=faded và dừng lại khi mất dấu vết
Rationale: Đảm bảo dữ liệu huấn luyện phản ánh đúng độ tin cậy của cảm biến quang học
Common mistake: Cố đoán mò kéo dài vạch về phía đường chân trời khi không nhìn thấy vết sơn
Diversity: low_visibility

---

CASE ID: EC-06
Sample: BDD10
Scene: Tuyến phố đô thị có ô tô con đỗ sát lề đường bên phải
Observation: Xe đỗ che khuất ngắt quãng dải vạch kẻ mép đường
Decision: LABEL
Expected: Ngắt polyline tại mép đuôi xe đỗ và bắt đầu đoạn mới ở đầu xe nếu nhìn thấy rõ
Rationale: Định hình chính xác biên lề đường có thể lưu thông được cho hệ thống tự lái
Common mistake: Nối một đường thẳng tắp xuyên qua thân các xe đang đỗ bên đường
>>>>>>> 02cdd5326e0beb55bcaf28193ee8968a84d847c0
Diversity: occlusion

---

<<<<<<< HEAD
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
=======
CASE ID: EC-07
Sample: BDD12
Scene: Đường đô thị trời nhiều mây, mặt đường bê tông bạc màu
Observation: Vạch sơn kẻ đường bị mài mòn nặng, đứt quãng bất thường không theo chu kỳ vạch đứt
Decision: ESCALATE
Expected: Vẽ phần vạch còn nhìn thấy với độ tin cậy cao, gán needs_review=true và log yêu cầu xem xét
Rationale: Báo hiệu cho đội ngũ phát triển thuật toán về các vùng đường chất lượng kém cần kết hợp GPS/HD Map
Common mistake: Tự ý nội suy vẽ bù các đoạn đứt quãng không có sơn
>>>>>>> 02cdd5326e0beb55bcaf28193ee8968a84d847c0
Diversity: escalation

---

<<<<<<< HEAD
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
=======
CASE ID: EC-08
Sample: BDD17
Scene: Đường phố trời mưa lớn, mặt đường sũng nước
Observation: Ánh sáng đèn đường và đèn pha phản chiếu trên mặt nước tạo thành các vệt sáng thẳng dài như vạch sơn
Decision: IGNORE
Expected: Không tạo polyline trên các vệt phản quang nước mưa; chỉ vẽ vạch sơn thật nhìn rõ cấu trúc dải sơn
Rationale: Ngăn chặn xe tự hành nhận diện nhầm vệt nước phản chiếu là làn đường thật gây đánh lái sai hướng
Common mistake: Nhận nhầm dải phản chiếu mặt nước là vạch kẻ đường solid white
Diversity: critical
>>>>>>> 02cdd5326e0beb55bcaf28193ee8968a84d847c0
