# Revision log

<<<<<<< HEAD
Bảng nhật ký thay đổi phiên bản Guideline qua các giai đoạn làm bài:

| Version | Đổi gì | Vì sao | Bằng chứng |
|---|---|---|---|
| `v1` | Khởi tạo bản nháp Guideline v1 tiêu chuẩn dựa trên quy ước BDD100K 2D BBox, Polygon & Polyline. | Thiết lập khung quy tắc ban đầu cho nhóm thực hiện annotation. | `01_problem_statement.md`, `02_guideline.md` v1 |
| `v2` | Cập nhật quy tắc vẽ vạch đứt nét (`lane/single white`) thành 1 polyline liền bám tim; bổ sung quy tắc gán nhãn cụm đèn giao thông trên xà ngang và vạch tam giác nhường đường (`yield line`). | Kết quả đo bất đồng Calibration cho thấy annotator An ngắt polyline theo từng sọc sơn nhỏ và bỏ sót vạch nhường đường. | `06_calibration_report.csv` (dòng 1, dòng 2, dòng 4) |
| `v3` | Bổ sung chi tiết quy chuẩn Qatar Road Marking (vạch đôi nét liền `double yellow` / `double white`, vạch kết thúc làn `end of lane`), quy tắc xử lý ca biên Kognic (vạch mờ, che khuất, thời tiết pluie/neige), và tiêu chuẩn đo lường Computer Vision (mAP, mIoU, Chamfer distance, Fleiss' Kappa). | Kết quả nhận xét từ Peer team02 và yêu cầu mở rộng bài toán đảm bảo bao phủ đầy đủ các ca biên thực tế. | `07_blind_handoff/peer_feedback.md`, `04_edge_cases/edge_case_cards.md` (CASE-01 đến CASE-10) |
=======
Guideline v1 = bản nháp đầu; v2 = sau calibration nội bộ; v3 = sau blind handoff. Mỗi lần tăng `Version` trong `02_guideline.md`, thêm một hoặc nhiều dòng vào bảng: đổi gì và vì sao, kèm bằng chứng (sample_id, dòng calibration report, câu hỏi trong clarification log, feedback của peer).

Cột Version ghi dạng `v1`, `v2`, `v3` — `make status` tìm dòng bảng có `v2` và dòng có `v3`.

| Version | Đổi gì | Vì sao | Bằng chứng |
|---|---|---|---|
| v1 | Khởi tạo Guideline bản nháp đầu tiên | Thiết lập hệ thống quy tắc ban đầu cho bài toán Lane Boundary | Dựa trên hợp đồng downstream tại `01_problem_statement.md` |
| v2 | Làm rõ quy tắc vạch liền đoạn cong, cập nhật ngưỡng lóa kính và bổ sung quy định dừng khi bị xe đỗ che khuất | Khắc phục bất đồng sau khi 6 thành viên gắn nhãn độc lập trên tập ảnh calibration | Kết quả đo đạc calibration tại `06_calibration_report.csv` (các ảnh BDD03, BDD06, BDD10) |
>>>>>>> 02cdd5326e0beb55bcaf28193ee8968a84d847c0
