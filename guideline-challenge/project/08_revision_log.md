# Revision log

Bảng nhật ký thay đổi phiên bản Guideline qua các giai đoạn làm bài:

| Version | Đổi gì | Vì sao | Bằng chứng |
|---|---|---|---|
| `v1` | Khởi tạo bản nháp Guideline v1 tiêu chuẩn dựa trên quy ước BDD100K 2D BBox, Polygon & Polyline. | Thiết lập khung quy tắc ban đầu cho nhóm thực hiện annotation. | `01_problem_statement.md`, `02_guideline.md` v1 |
| `v2` | Cập nhật quy tắc vẽ vạch đứt nét (`lane/single white`) thành 1 polyline liền bám tim; bổ sung quy tắc gán nhãn cụm đèn giao thông trên xà ngang và vạch tam giác nhường đường (`yield line`). | Kết quả đo bất đồng Calibration cho thấy annotator An ngắt polyline theo từng sọc sơn nhỏ và bỏ sót vạch nhường đường. | `06_calibration_report.csv` (dòng 1, dòng 2, dòng 4) |
| `v3` | Bổ sung chi tiết quy chuẩn Qatar Road Marking (vạch đôi nét liền `double yellow` / `double white`, vạch kết thúc làn `end of lane`), quy tắc xử lý ca biên Kognic (vạch mờ, che khuất, thời tiết pluie/neige), và tiêu chuẩn đo lường Computer Vision (mAP, mIoU, Chamfer distance, Fleiss' Kappa). | Kết quả nhận xét từ Peer team02 và yêu cầu mở rộng bài toán đảm bảo bao phủ đầy đủ các ca biên thực tế. | `07_blind_handoff/peer_feedback.md`, `04_edge_cases/edge_case_cards.md` (CASE-01 đến CASE-10) |
