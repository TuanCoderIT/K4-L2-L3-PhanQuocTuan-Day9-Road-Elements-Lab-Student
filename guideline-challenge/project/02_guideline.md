# Annotation guideline — Lane Boundary tại merge/split + vạch mờ/tạm thời

**Version:** v2

## 1. Objective + scope

- **Mục tiêu:** Cung cấp dữ liệu nhãn vạch kẻ đường (Lane Marking Boundary) độ chính xác cao cho module Lane Keeping Assist (LKA) và Trajectory Planning của xe tự hành.
- **Trong scope:** Mọi vạch sơn kẻ đường nhìn thấy được phân định làn xe chạy (vạch liền, vạch đứt, vạch đôi, vạch sơn khu vực tách/nhập làn cao tốc gore area, vạch người đi bộ qua đường crosswalk, vạch dừng xe stop line).
- **Ngoài scope:** Các vết trám nứt mặt đường bằng nhựa đường (bitumen tar seams), vệt hằn lốp xe cao su, bóng đổ của cây cối và các phương tiện khác, gờ bê tông bó vỉa (curb) không có sơn viền.

## 2. Annotation unit

- **Đơn vị gắn nhãn:** Thực thể độc lập (Instance) trên từng ảnh tĩnh 2D (Single Image).
- **Quy tắc thực thể:** Mỗi một dải sơn kẻ đường liên tục có cùng chức năng được tính là một polyline độc lập. Đối với vạch đứt quãng (dashed line), toàn bộ chuỗi nét đứt cùng một làn được coi là MỘT thực thể duy nhất xuyên suốt. Không tách mỗi vệt sơn ngắn thành một instance riêng.

## 3. Geometry rule

- **Loại hình học:** `Polyline`.
- **Đường đi của polyline:** Polyline bắt buộc phải chạy qua tim (tâm hình học) của vạch sơn.
- **Độ chính xác và dung sai:** Sai lệch tim vạch $\le 3$ pixel. Mật độ điểm phải phân bố hợp lý: đoạn thẳng chỉ cần ít điểm (điểm đầu và điểm cuối); đoạn cong tăng mật độ điểm tại các vị trí đổi độ cong để đường line mượt mà, không bị gấp khúc zig-zag.
- **Quy tắc điểm đầu và điểm kết thúc:**
  - Bắt đầu tại vị trí vạch sơn xuất hiện rõ ràng nhất trong ảnh.
  - Kết thúc khi vạch sơn biến mất ra khỏi mép ảnh, bị mờ hoàn toàn không thể nhận diện, hoặc bị che khuất bởi vật cản khác (xe cộ, người đi bộ).

## 4. Taxonomy

Mỗi đối tượng `lane_marking` bắt buộc phải có đủ các thuộc tính sau (không được để `__undefined__` khi nộp):
- `laneTypes`:
  - `single white`: Vạch đơn màu trắng (thường là vạch phân cách các làn cùng chiều hoặc vạch mép phải đường).
  - `single yellow`: Vạch đơn màu vàng (vạch phân cách hai chiều xe chạy hoặc mép trái cao tốc).
  - `double white`: Vạch đôi màu trắng (ngăn cách chuyển làn).
  - `double yellow`: Vạch đôi màu vàng (phân chia hai chiều ngược nhau nghiêm cấm lấn làn).
  - `crosswalk`: Vạch dành cho người đi bộ qua đường (thường là các sọc ngang to bản).
  - `road curb`: Vạch sơn kẻ trực tiếp trên gờ bó vỉa đường.
  - `single other` / `double other`: Vạch có màu sắc khác (đỏ, xanh, vạch thi công tạm).
- `laneStyle`:
  - `solid`: Vạch sơn liền mạch.
  - `dashed`: Vạch sơn đứt quãng.
- `laneDirection`:
  - `parallel`: Vạch chạy dọc song song với chiều di chuyển chính của đường.
  - `vertical`: Vạch cắt ngang đường (vạch dừng đèn đỏ, vạch qua đường).
- `visibility`:
  - `visible`: Nhìn rõ ràng, không bị cản trở.
  - `partially_occluded`: Bị che khuất một phần bởi xe khác hoặc bóng râm.
  - `faded`: Bị mờ do thời tiết, bào mòn hoặc lóa kính.
  - `truncated`: Bị cắt cụt ở rìa mép ảnh.
- `needs_review`:
  - `false` (mặc định): Ca rõ ràng, đúng theo guideline.
  - `true`: Ca mơ hồ đặc biệt cần xem xét lại.

## 5. Inclusion / exclusion

- **Bắt buộc vẽ:**
  - Các vạch ranh giới hình chữ V hoặc dải sọc chéo tại khu vực tách làn (split gore) và nhập làn (merge gore). Vẽ bám theo đường biên bao ngoài của vùng đệm này.
  - Vạch sơn bị mờ nhưng vẫn nhận biết được hình thái tổng thể bằng mắt thường khi zoom 100%.
- **Tuyệt đối bỏ qua (Ignore):**
  - Không vẽ theo các vệt nước mưa đọng thành rãnh song song trên mặt đường.
  - Không vẽ các vệt nối nhựa đường giữa hai lớp trải thảm bê tông at-phan.
  - Không tự ý nối dài tưởng tượng đường kẻ xuyên qua gầm hoặc thân xe phía trước.

## 6. Visibility / occlusion

- **Bị che khuất bởi xe cộ (Vehicle Occlusion):** Dừng polyline ngay tại mép thân xe phía trước. Nếu phía sau xe đó vạch kẻ tiếp tục xuất hiện rõ ràng, tạo một polyline MỚI bắt đầu từ mép bên kia của xe. Tuyệt đối không nối đường thẳng xuyên qua xe (quy tắc an toàn: tránh tạo làn ảo cho xe tự hành).
- **Vạch bị mờ dần (Fading Markings):** Khi vạch sơn mờ dần vào mặt đường xám, annotator dừng polyline tại điểm cuối cùng mắt người còn xác định được biên vạch với độ tự tin trên 80%. Không cố gắng kéo dài thêm vào khoảng không vô định.
- **Kính lái lóa sáng / trời mưa ngập nước:** Nếu hiện tượng lóa hoặc phản quang làm mất dấu vết sơn quá 10 mét, ngắt đoạn polyline và gắn nhãn `visibility = faded`.

## 7. Ambiguity / escalation

Để đảm bảo kết quả thể hiện minh bạch trong file export CVAT:
- **LABEL**: Áp dụng khi có đầy đủ bằng chứng nhìn thấy được trên ảnh.
- **IGNORE**: Khi các vệt trên đường là nứt nẻ, bóng râm hoặc vệt bánh xe.
- **UNKNOWN**: Khi không xác định được màu sắc do chói sáng hoặc ban đêm, chọn `laneTypes = single other` kèm `visibility = faded`.
- **ESCALATE**: Khi gặp các tình huống sau, annotator vẽ theo giả định hợp lý nhất và tích chọn thuộc tính `needs_review = true`:
  1. Có từ 2 lớp vạch sơn chồng chéo nhau do phân luồng tạm thời trong công trường và vạch cũ chưa tẩy sạch hoàn toàn.
  2. Vạch sơn bị ngắt quãng bất thường không rõ lý do tại khu vực ngã ba, ngã tư phức tạp.

## 8. Temporal rule

Không áp dụng — task thực hiện trên tập ảnh tĩnh đơn lẻ (Static 2D Images).

## 9. Examples

| sample_id | Thấy gì | Expected output | Rule áp dụng |
|---|---|---|---|
| BDD01 | Đường cao tốc ban ngày, vạch đứt bên trái và vạch liền bên phải | Vẽ 1 polyline xuyên tim chuỗi vạch đứt (`laneStyle=dashed`, `laneTypes=single white`); vạch liền dừng tại góc đuôi xe SUV phía trước | Quy tắc 2 & Quy tắc 6 (dừng khi bị xe che) |
| BDD02 | Ngã tư đô thị có vạch người đi bộ và vạch dừng đỗ xe | Vẽ các polyline ngang đường, gán `laneDirection=vertical`, `laneTypes=crosswalk` | Quy tắc 4 (phân loại hướng và loại vạch ngang) |
| BDD04 | Khu phố dân cư có vạch sơn hơi mờ ở đoạn xa | Vẽ bám tim vạch, gán `visibility=faded`, dừng khi vạch hoàn toàn biến mất | Quy tắc 3 & Quy tắc 6 (dừng khi mất dấu vết) |
| BDD05 | Cao tốc đoạn phân tách làn rẽ (split lane), có dải sơn chéo | Vẽ theo ranh giới phân làn chính, không bẻ nhánh polyline vào từng nét sơn chéo phụ | Quy tắc 1 & Quy tắc 5 (bám biên phân làn chính tại gore area) |

## 10. Common mistakes

1. **Ngắt vụn vạch đứt:** Nhầm lẫn vạch đứt là nhiều đối tượng riêng biệt và vẽ hàng chục polyline ngắn 10px. $\rightarrow$ *Khắc phục: Chỉ dùng đúng 1 polyline kéo dài từ nét đầu tới nét cuối của dải vạch đứt.*
2. **Nối xuyên qua xe:** Kéo polyline đi xuyên qua thân xe tải hoặc ô tô con phía trước. $\rightarrow$ *Khắc phục: Dừng ngay khi chạm mép xe, bắt đầu polyline mới nếu đoạn sau xe nhìn thấy lại.*
3. **Quên đổi giá trị default:** Để nguyên giá trị `__undefined__` trên file nộp. $\rightarrow$ *Khắc phục: Dùng chế độ Attribute Annotation Mode quét lại toàn bộ trước khi export.*
4. **Vẽ theo vết nứt đường:** Nhầm vết trám bitum màu đen là vạch kẻ đường. $\rightarrow$ *Khắc phục: Kiểm tra màu sắc và tính đối xứng làn xe.*
