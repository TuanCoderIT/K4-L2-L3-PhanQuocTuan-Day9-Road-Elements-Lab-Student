# Revision log

Guideline v1 = bản nháp đầu; v2 = sau calibration nội bộ; v3 = sau blind handoff. Mỗi lần tăng `Version` trong `02_guideline.md`, thêm một hoặc nhiều dòng vào bảng: đổi gì và vì sao, kèm bằng chứng (sample_id, dòng calibration report, câu hỏi trong clarification log, feedback của peer).

Cột Version ghi dạng `v1`, `v2`, `v3` — `make status` tìm dòng bảng có `v2` và dòng có `v3`.

| Version | Đổi gì | Vì sao | Bằng chứng |
|---|---|---|---|
| v1 | Khởi tạo Guideline bản nháp đầu tiên | Thiết lập hệ thống quy tắc ban đầu cho bài toán Lane Boundary | Dựa trên hợp đồng downstream tại `01_problem_statement.md` |
| v2 | Làm rõ quy tắc vạch liền đoạn cong, cập nhật ngưỡng lóa kính và bổ sung quy định dừng khi bị xe đỗ che khuất | Khắc phục bất đồng sau khi 6 thành viên gắn nhãn độc lập trên tập ảnh calibration | Kết quả đo đạc calibration tại `06_calibration_report.csv` (các ảnh BDD03, BDD06, BDD10) |
