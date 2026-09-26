# Problem statement + downstream contract

Tối đa nửa trang, viết **trước khi mở CVAT**. Đây là bằng chứng của gate G1 (topic lock).

## Bài toán

Nhận diện và phân định ranh giới làn đường (Lane Boundary) bằng Polyline tại các khu vực phức tạp: nút giao nhập/tách làn (merge/split), khu vực có vạch sơn bị mờ do thời tiết/mài mòn và vạch phân làn tạm thời do thi công.

## Downstream contract

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

## Scope

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

## Output chấm được

- **LABEL**: Polyline đúng vị trí tim vạch, đúng attribute `lane_style`, `lane_type`, `lane_direction`.
- **IGNORE**: Không xuất hiện polyline trên các vết nứt nhựa đường, vết trám hoặc bóng đổ.
- **ESCALATE / UNKNOWN**: Gán attribute `needs_review = true` đối với các vạch bị mờ ngắt quãng dài hoặc vạch chồng chéo gây tranh cãi.
- Mọi quyết định đều được xuất và kiểm tra tự động qua file CVAT XML annotation export.

## Dữ liệu và giới hạn

- **Nguồn ảnh**: 26 ảnh từ tập `data/bdd100k/` (BDD01 đến BDD26).
- **Đặc điểm dữ liệu**: Ảnh chụp từ camera hành trình góc nhìn ego-vehicle (1280x720), bao gồm đường cao tốc (highway), đường phố đô thị (city street), khu dân cư với nhiều điều kiện thời tiết (nắng, nhiều mây, mưa, tuyết, chạng vạng và ban đêm).
- **Giới hạn**: Không có chuỗi frame liên tiếp theo thời gian (ảnh đơn), một số ảnh bị chói lóa kính chắn gió hoặc vạch sơn quá xa (dưới 20 px) khó xác định màu sắc chính xác.
