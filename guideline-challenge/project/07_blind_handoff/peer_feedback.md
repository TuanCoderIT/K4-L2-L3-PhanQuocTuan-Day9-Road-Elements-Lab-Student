# Peer Feedback & Usability Assessment

Nhóm peer (`team02`) đã tiến hành gán nhãn độc lập (blind labeling) trên tập 5 ảnh blind (`BDD11` đến `BDD15`) dựa hoàn toàn vào tài liệu `02_guideline.md` (v3) và để lại các nhận xét chi tiết sau:

## 1. Điểm mạnh của Guideline

- **Cấu trúc cực kỳ rõ ràng:** Phân định 3 nhóm shape độc lập (BBox Rectangle, Drivable Polygon, Lane Polyline) giúp annotator dễ thao tác và không bị lầm lẫn tool trong CVAT.
- **Tích hợp quy chuẩn thực tế tốt:** Việc trích dẫn cụ thể Qatar Road Marking Rules (vạch vàng/trắng đơn/đôi, vạch nhường đường yield line) và Kognic Edge Cases giúp annotator tự tin xử lý các tình huống khó mà không cần hỏi lại.
- **Tiêu chí loại trừ (Exclusion) dễ hiểu:** Quy định cấm tô bóng đổ, cấm tô hình phản chiếu trên kính, cấm tô pano quảng cáo rất cụ thể.

## 2. Góp ý cải tiến & Phản hồi

- **Vạch kẻ đường mờ nhạt (Degraded Line):** Đề xuất nhóm bổ sung thêm minh họa cho trường hợp vạch sơn bị mất nét đoạn ngắn (gap $< 1\text{m}$) thì có được nối liền polyline qua gap hay ngắt tại điểm mờ.
- **Dải phân cách cứng (Road Curb):** Đề xuất làm rõ chiều cao của mép bó vỉa hè để phân biệt với rào chắn di động tạm thời.

## 3. Kết luận đánh giá Usability

Guideline đạt chỉ số **Usability Score 95/100**, nhóm peer hoàn thành gán nhãn 5 ảnh blind hoàn toàn độc lập với chỉ 1 câu hỏi làm rõ trong clarification log, không có bất kỳ thắc mắc nào về taxonomy hay geometry setup.
