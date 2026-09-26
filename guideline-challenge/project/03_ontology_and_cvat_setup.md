# Ontology + CVAT setup

Bảng ontology này là **source of truth** cho schema CVAT: file `03_cvat_labels.json` hoàn toàn khớp từng dòng với bảng dưới đây.

## Ontology table

| Name | Geometry | Type (class / attribute) | Allowed values | Default | Mutable? | Rationale |
|---|---|---|---|---|---|---|
| `pedestrian` | Rectangle | Class | N/A | N/A | No | Người đi bộ trên đường/vỉa hè; phân biệt rõ với người đi xe. |
| `rider` | Rectangle | Class | N/A | N/A | No | Người điều khiển xe đạp, xe máy, ngựa. |
| `car` | Rectangle | Class | N/A | N/A | No | Xe ô tô con, SUV, sedan, hatchback, bán tải nhỏ. |
| `truck` | Rectangle | Class | N/A | N/A | No | Xe tải hàng, xe container, xe đầu kéo. |
| `bus` | Rectangle | Class | N/A | N/A | No | Xe khách, xe buýt công cộng. |
| `train` | Rectangle | Class | N/A | N/A | No | Tàu hỏa, tàu điện trên đường ray. |
| `motorcycle` | Rectangle | Class | N/A | N/A | No | Xe máy, xe tay ga, môtô phân khối lớn. |
| `bicycle` | Rectangle | Class | N/A | N/A | No | Xe đạp thô sơ hoặc xe đạp điện nhỏ. |
| `traffic light` | Rectangle | Class | N/A | N/A | No | Cụm hộp đèn tín hiệu điều khiển giao thông. |
| `traffic sign` | Rectangle | Class | N/A | N/A | No | Biển báo giao thông đường bộ các loại. |
| `area/drivable` | Polygon | Class | N/A | N/A | No | Lòng đường xe ego trực tiếp di chuyển (direct lane). |
| `area/alternative` | Polygon | Class | N/A | N/A | No | Làn đường cùng chiều kế cận xe ego có thể chuyển sang. |
| `lane/single white` | Polyline | Class | N/A | N/A | No | Vạch trắng đơn (nét liền hoặc nét đứt). |
| `lane/double white` | Polyline | Class | N/A | N/A | No | Vạch trắng đôi song song nét liền. |
| `lane/single yellow` | Polyline | Class | N/A | N/A | No | Vạch vàng đơn phân chia chiều đường hoặc mép trái. |
| `lane/double yellow` | Polyline | Class | N/A | N/A | No | Vạch vàng đôi nét liền cấm lấn làn/vượt. |
| `lane/crosswalk` | Polyline | Class | N/A | N/A | No | Vạch kẻ đường cho người đi bộ qua đường. |
| `lane/road curb` | Polyline | Class | N/A | N/A | No | Đường mép bó vỉa hè hoặc rào chắn hộ lan. |
| `lane/single other` | Polyline | Class | N/A | N/A | No | Vạch sơn màu khác (vàng cam, xanh) hoặc vạch nhường đường. |
| `occluded` | N/A | Attribute | `true`, `false` | `false` | Yes | Trạng thái đối tượng bị che khuất một phần bởi vật cản khác. |
| `truncated` | N/A | Attribute | `true`, `false` | `false` | Yes | Trạng thái đối tượng bị cắt bởi mép biên của khung hình. |

## Class hay attribute

1. **Vì sao dùng Class:**
   - Các class `car`, `truck`, `bus`, `pedestrian` có đặc trưng hình học, tải trọng, và phản ứng điều khiển khác hẳn nhau trong mô hình perception.
   - `area/drivable` vs `area/alternative` quyết định trực tiếp đến logic điều hướng (planning trajectory). Nếu dùng attribute cho drivable, mô hình segmentation sẽ dễ bị lầm lẫn ranh giới làn.
   - Các loại vạch kẻ đường `lane/*` có ý nghĩa pháp lý giao thông riêng biệt (cho phép/cấm đè vạch).
2. **Vì sao dùng Attribute:**
   - `occluded` và `truncated` mô tả trạng thái góc nhìn quan sát (viewpoint/visibility) của cùng một vật thể, không thay đổi bản chất của đối tượng.
3. **Default risk bias:**
   - Mặc định `occluded=false` và `truncated=false`. Nếu annotator thao tác vội có thể quên bật `true` khi xe bị che hoặc bị cắt ranh giới. Do đó QA Plan bắt buộc có bước Audit Attribute Checklist.

## CVAT

- **Phiên bản CVAT (`make cvat-status`):** CVAT v2.14.0 (Docker compose local deployment).
- **Tên task calibration:** `team01-road-elements-calib-v1`.
- **Guide của task đã dán `02_guideline.md`?:** Có, đã dán đầy đủ nội dung Guideline v3 vào mục Task Guide trong CVAT.
- **Nhóm dùng Track hay Shape, vì sao:** Sử dụng **Shape mode**, vì dữ liệu BDD100K trong tập bài tập là các ảnh tĩnh độc lập (`.jpg`), không phải chuỗi video frame liên tục.

## Setup test

Thành viên Trần Thị B (chưa từng tham gia soạn thảo quy tắc chi tiết) đã thử gán nhãn 2 ảnh thử nghiệm và trả lời các câu hỏi:
- *Label gì:* Chọn `car` (BBox), `area/drivable` (Polygon), `lane/single white` (Polyline).
- *Dùng tool nào:* BBox Rectangle, Polygon tool (no self-intersection), Polyline tool.
- *Gán attribute nào:* Check `occluded=true` cho xe đậu sau cây; check `truncated=true` cho xe cắt mép phải.
- *Khi nào escalate:* Khi gặp dải gạch chéo màu vàng tại nút giao bị mờ nhạt, tạo Issue `UNCERTAIN_SCOPE` để hỏi Mentor.
- *Điểm vấp:* Vạch đứt ban đầu lầm tưởng phải ngắt thành nhiều đường nhỏ; sau khi đọc lại Guide đã vẽ đúng 1 polyline liền chạy bám theo tim các nét đứt.
