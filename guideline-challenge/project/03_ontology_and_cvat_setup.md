# Ontology + CVAT setup

<<<<<<< HEAD
Bảng ontology này là **source of truth** cho schema CVAT: file `03_cvat_labels.json` hoàn toàn khớp từng dòng với bảng dưới đây.
=======
Bảng ontology là **source of truth** cho schema CVAT: `03_cvat_labels.json` khớp chính xác từng dòng ở đây.
>>>>>>> 02cdd5326e0beb55bcaf28193ee8968a84d847c0

## Ontology table

| Name | Geometry | Type (class / attribute) | Allowed values | Default | Mutable? | Rationale |
|---|---|---|---|---|---|---|
<<<<<<< HEAD
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
=======
| `lane_marking` | polyline | class | n/a | n/a | false | Thực thể vạch kẻ đường chính cần gắn nhãn |
| `laneTypes` | n/a | attribute (select) | `single white`, `single yellow`, `double white`, `double yellow`, `crosswalk`, `road curb`, `single other`, `double other` | `__undefined__` | false | Phân biệt màu sắc và loại phân làn vật lý |
| `laneStyle` | n/a | attribute (select) | `solid`, `dashed` | `__undefined__` | false | Kiểu dáng vạch kẻ (vạch liền hay vạch đứt quãng) |
| `laneDirection` | n/a | attribute (select) | `parallel`, `vertical` | `__undefined__` | false | Hướng vạch (song song làn xe chạy hay cắt ngang như vạch dừng) |
| `visibility` | n/a | attribute (radio) | `visible`, `partially_occluded`, `faded`, `truncated` | `visible` | false | Độ rõ ràng của vạch phục vụ đánh giá chất lượng |
| `needs_review` | n/a | attribute (checkbox) | `false`, `true` | `false` | false | Cờ đánh dấu ca mơ hồ cần escalate lên cấp trên |
| `image_context` | tag | class | n/a | n/a | false | Gắn thẻ ngữ cảnh toàn cảnh cho ảnh |
| `weather` | n/a | attribute (select) | `clear`, `partly cloudy`, `overcast`, `rainy`, `snowy`, `foggy`, `undefined` | `__undefined__` | false | Điều kiện thời tiết môi trường |
| `timeofday` | n/a | attribute (select) | `daytime`, `dawn/dusk`, `night`, `undefined` | `__undefined__` | false | Khung thời gian chiếu sáng |

## Class hay attribute

- **Tại sao chỉ dùng 1 class `lane_marking` và nhiều attributes:**
  Nếu tách thành các class con rời rạc (như `lane_solid_white`, `lane_dashed_yellow`...) sẽ gây bùng nổ tổ hợp class (combinatorial explosion), khiến giao diện CVAT rối loạn và annotator dễ chọn nhầm. Việc gom về 1 class duy nhất với các attribute độc lập giúp annotator tư duy theo từng bước: vẽ geometry $\rightarrow$ chọn màu/loại $\rightarrow$ chọn kiểu dáng vạch.
- **Tránh default bias:**
  Các trường phân loại cốt lõi (`laneTypes`, `laneStyle`, `laneDirection`, `weather`, `timeofday`) đều đặt default là `__undefined__`. Điều này ép buộc annotator phải chủ động suy nghĩ và click chọn giá trị đúng, loại bỏ hoàn toàn lỗi "quên không chọn nên bị nhận nhầm giá trị mặc định". Trường `needs_review` mặc định là `false` để giữ quy trình chuẩn, chỉ bật khi thực sự bất định.

## CVAT

- **Phiên bản CVAT** (`make cvat-status`): CVAT v2.x (Docker container chạy local trên port 8080)
- **Tên task calibration**: `team03-calib-v1`
- **Guide của task đã dán `02_guideline.md`?**: Có (toàn bộ nội dung `02_guideline.md` được copy dán vào tab Guide của Task để annotator đọc trực tiếp khi làm việc).
- **Nhóm dùng Track hay Shape, vì sao:** Dùng **Shape** (Polyline). Do tập dữ liệu BDD100K là các ảnh đơn lẻ độc lập (static images), không phải chuỗi video liên tục nên không cần duy trì ID tracking giữa các frame.

## Setup test

- **Người thực hiện test setup:** Nguyễn Như Quỳnh (CVAT Owner) và Trần Minh Hiếu (Data Lead).
- **Quy trình test:** Mở task `team03-calib-v1` trên giao diện web CVAT, tạo thử 1 polyline trên ảnh BDD03, kiểm tra danh sách dropdown attributes.
- **Kết quả và chỗ vấp ghi nhận:**
  1. Giao diện dropdown hiển thị đầy đủ, không bị lỗi font tiếng Anh/Việt.
  2. Điểm vấp: Cần lưu ý annotator chuyển sang chế độ gán nhãn thuộc tính nhanh (Attribute Annotation Mode) để không mất thời gian click từng menu sau khi vẽ đường line.
  3. Đã xác nhận cơ chế gán cờ `needs_review=true` xuất hiện chính xác trong file export CVAT XML.
>>>>>>> 02cdd5326e0beb55bcaf28193ee8968a84d847c0
