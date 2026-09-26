# Edge-case library

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
Diversity: occlusion

---

CASE ID: EC-07
Sample: BDD12
Scene: Đường đô thị trời nhiều mây, mặt đường bê tông bạc màu
Observation: Vạch sơn kẻ đường bị mài mòn nặng, đứt quãng bất thường không theo chu kỳ vạch đứt
Decision: ESCALATE
Expected: Vẽ phần vạch còn nhìn thấy với độ tin cậy cao, gán needs_review=true và log yêu cầu xem xét
Rationale: Báo hiệu cho đội ngũ phát triển thuật toán về các vùng đường chất lượng kém cần kết hợp GPS/HD Map
Common mistake: Tự ý nội suy vẽ bù các đoạn đứt quãng không có sơn
Diversity: escalation

---

CASE ID: EC-08
Sample: BDD17
Scene: Đường phố trời mưa lớn, mặt đường sũng nước
Observation: Ánh sáng đèn đường và đèn pha phản chiếu trên mặt nước tạo thành các vệt sáng thẳng dài như vạch sơn
Decision: IGNORE
Expected: Không tạo polyline trên các vệt phản quang nước mưa; chỉ vẽ vạch sơn thật nhìn rõ cấu trúc dải sơn
Rationale: Ngăn chặn xe tự hành nhận diện nhầm vệt nước phản chiếu là làn đường thật gây đánh lái sai hướng
Common mistake: Nhận nhầm dải phản chiếu mặt nước là vạch kẻ đường solid white
Diversity: critical
