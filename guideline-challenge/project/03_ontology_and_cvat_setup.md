# Ontology + CVAT setup

Bảng ontology là **source of truth** cho schema CVAT: `03_cvat_labels.json` khớp chính xác từng dòng ở đây.

## Ontology table

| Name | Geometry | Type (class / attribute) | Allowed values | Default | Mutable? | Rationale |
|---|---|---|---|---|---|---|
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
