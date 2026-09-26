# Peer feedback + owner response

Phần 1 do **nhóm peer** trả lời (gửi kèm file export). Phần 2 do **nhóm owner** điền. Thay mọi placeholder mới là xong (gate G5).

- **Nhóm peer:** Nhóm 04
- **Người label blind:** Lê Văn Hoàng (QA & Annotator Nhóm 04)

## 1. Peer trả lời

1. Rule nào rõ nhất / giúp quyết định nhanh nhất? 
   - Quy tắc Mục 5 & 6.1 về việc dừng polyline ngay tại mép bánh xe đè lên vạch (BDD14) và quy tắc Mục 1.4 vẽ vùng Gore (BDD19) chỉ bám viền ngoài, không vẽ hoa văn sọc chéo bên trong. Hướng dẫn trực quan, có ví dụ cụ thể nên thao tác dứt khoát không cần phân vân.
2. Rule nào mơ hồ hoặc phải tự suy diễn? 
   - Quy tắc phân biệt vạch sơn mờ (`faded`) do mòn vs vạch đứt quãng do chắp vá thi công ở BDD12. Chưa có định lượng cụ thể về độ dài đoạn đứt quãng bao nhiêu mét thì cần bật cờ `needs_review=true`.
3. Sample nào khiến guideline "vỡ"? 
   - BDD17 (mặt đường ướt mưa phản quang chói lóa). Ban đầu rất dễ nhầm vệt nước kéo dài là vạch kẻ đường, phải đối chiếu kỹ mục 6.3 và hỏi clarification mới tự tin bỏ qua vệt phản quang.
4. Attribute / default nào trong CVAT dễ gây thao tác sai? 
   - Thuộc tính `needs_review` có default là `false`. Khi annotator phát hiện vạch mòn bất thường (BDD12), nếu thao tác vội rất dễ quên tick chọn `true`.
5. Một thay đổi cụ thể giúp annotator mới ít hỏi hơn? 
   - Thêm hình ảnh minh họa so sánh trực tiếp Side-by-Side giữa "vạch sơn thật dưới mưa (faded)" và "vệt phản chiếu ánh sáng trên mặt nước (negative case)" vào Mục 6.3 của Guideline.

## 2. Owner phân loại

Owner không tranh luận để bảo vệ guideline. Mỗi feedback và mỗi decision peer làm sai được xếp vào một hướng xử lý.

| Feedback / decision sai | Nguyên nhân (guideline gap / data ambiguity / execution error) | Xử lý (accept + revise / reject with evidence / add escalation rule) | Bằng chứng |
|---|---|---|---|
| BDD17: Nguy cơ nhầm vệt nước mưa phản quang thành vạch sơn | data_ambiguity | revise_rule | Clarification log dòng 1, feedback mục 3 của Peer |
| BDD12: Tiêu chí bật cờ `needs_review=true` khi vạch mòn đứt quãng | guideline_gap | add_escalation | Feedback mục 2 & 4 của Peer, gold decision BDD12-d2 |
| BDD14 & BDD19: Dừng tại mép xe và viền ngoài Gore area thực hiện tốt | execution_error | add_example | BDD14-d1, BDD19-d2 trong transfer_score.csv đạt 100% |
