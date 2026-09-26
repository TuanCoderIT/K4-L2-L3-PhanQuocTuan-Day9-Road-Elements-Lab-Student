# Annotation guideline — Lane Boundary tại merge/split + vạch mờ/tạm thời

**Version:** v2

---

## ⚡ Đọc nhanh trong 60 giây

1. **Công cụ & Đối tượng:** Sử dụng **Polyline** để gắn nhãn vạch kẻ đường (`lane_marking`). Chỉ tập trung gắn nhãn vạch đường, **KHÔNG** tô vùng đa giác Drivable Area.
2. **Quy tắc tâm vạch:** Mọi điểm Polyline bắt buộc đặt chính xác tại **tâm hình học (centerline)** của dải sơn, vẽ theo chiều **từ dưới lên trên** (từ cự ly gần xe ego tiến ra xa).
3. **Vạch đứt:** Toàn bộ chuỗi nét đứt cùng làn được vẽ bằng **1 Polyline duy nhất** xuyên suốt qua các khoảng trống (`laneStyle = dashed`). Tuyệt đối không cắt vụn thành từng vệt ngắn.
4. **Vạch đôi (vàng đôi / trắng đôi):** Vẽ **1 Polyline duy nhất ở chính giữa hai vạch**, chọn `laneTypes = double yellow` hoặc `double white`.
5. **Xe che khuất (Occlusion):** **Dừng Polyline ngay tại mép thân/lốp xe phía trước**, tuyệt đối **KHÔNG vẽ nối xuyên qua xe**. Bắt đầu Polyline mới ở phía bên kia nếu vạch lộ ra rõ ràng.
6. **Vạch qua đường (Crosswalk):** **CHỈ vẽ 2 đường Polyline biên giới hạn mép trên và mép dưới** của cụm vạch qua đường (`laneDirection = vertical`, `laneTypes = crosswalk`). **KHÔNG** vẽ từng vệt gạch sọc bên trong.
7. **Khu vực Tách/Nhập làn (Split/Merge Gore Area):** Vẽ bám theo hai đường biên ngoài của dải tam giác đệm (gore boundary). **KHÔNG** vẽ các vạch chéo/chữ V bên trong.
8. **Vạch mờ / Bóng râm / Kính lóa:** Vẫn vẽ xuyên qua nếu mắt người còn nhận biết rõ xu hướng hướng tuyến; dừng lại nếu vạch biến mất hoàn toàn $> 1.5 - 2.0$ mét.
9. **Điểm kết thúc ở xa (Cutoff):** Dừng Polyline khi bề rộng vạch thu hẹp $< 3$ pixel HOẶC khoảng cách giữa hai vạch cạnh nhau $< 10$ pixel.
10. **Nguyên tắc không đoán:** Không chắc chắn $\rightarrow$ vẽ theo khả năng cao nhất + tick `needs_review = true`. Tuyệt đối không để sót giá trị `__undefined__`.

---

## 1. Objective + scope

### 1.1. Mục tiêu Downstream
Dữ liệu nhãn phục vụ huấn luyện và kiểm thử các thuật toán tự lái cấp độ L2+/L3:
- **Lane Keeping Assist (LKA) & Lane Centering:** Định vị xe luôn chạy ổn định ở chính giữa tâm làn đường.
- **Lane Change & Trajectory Planning:** Nhận diện loại vạch được phép đè (`dashed`) hoặc cấm đè (`solid`, `double yellow`) để lập quỹ đạo chuyển làn hoặc tách/nhập làn an toàn.

### 1.2. Mức độ rủi ro (Defect Severity)
- **Critical (Nguy hiểm chết người):** 
  - Nối vạch xuyên qua xe phía trước (tạo làn ảo dẫn đến va chạm).
  - Gán nhầm vạch liền / vạch vàng đôi thành vạch đứt (`dashed`) khiến xe tự lái lấn làn ngược chiều hoặc vượt sai quy định.
  - Vẽ lệch hoặc bỏ sót ranh giới tách làn (gore area) dẫn đến xe lao vào dải phân cách cứng / đảo mềm.
- **Major (Lỗi ngữ nghĩa lớn):** Bỏ sót vạch phân làn chính; nhầm lẫn giữa vạch vàng và vạch trắng; vẽ nhầm vệt nứt nhựa đường / vết trám bitum.
- **Minor (Lỗi hình học nhỏ):** Lệch tim vạch 4–5 px ở cự ly xa; điểm bắt đầu bị hụt vài pixel sát mép nắp capo.

### 1.3. Trong Scope (Bắt buộc Label)
- Mọi vạch sơn kẻ đường dọc nhìn thấy được trên mặt đường xe chạy (vạch trắng / vàng; liền / đứt / vạch đôi).
- Đường biên mép đường không có vạch sơn nhưng có ranh giới vật lý rõ ràng (bó vỉa hè, chân rào chắn bê tông Jersey Barrier, chân lan can bảo vệ, mép thảm nhựa giáp lề đất/cỏ) $\rightarrow$ gán `laneTypes = road_edge`.
- Hai đường biên mép (trên và dưới) của vạch người đi bộ qua đường (Crosswalk).
- Vạch dừng dừng đèn đỏ / vạch dừng ưu tiên (Stop line).
- Hai đường viền ranh giới bao ngoài của vùng phân tách/nhập làn (Gore area).

### 1.4. Ngoài Scope (Tuyệt đối IGNORE)
- Các nét sọc chéo / chữ V nằm bên trong vùng đệm gạch chéo (Gore zone).
- Từng vệt sọc gạch ngắn bên trong cụm vạch đi bộ qua đường (Zebra stripes).
- Mũi tên chỉ hướng, chữ viết, số giới hạn tốc độ, logo xe đạp hoặc biểu tượng xe buýt sơn trên mặt đường.
- Vết trám nhựa đường màu đen (bitumen tar seams), vệt nứt bê tông, vết hằn cao su của lốp xe.
- Vệt nước mưa đọng phản chiếu ánh sáng đèn đường / đèn pha.
- Các vật thể dính trên kính lái xe ego (giá đỡ điện thoại, decal dán kính, giọt nước mưa đọng trên kính, gạt nước) và nắp capo xe mình.

---

## 2. Annotation unit

- **Đơn vị gắn nhãn:** Ảnh tĩnh đơn lẻ 2D (Single Static Image 1280×720). Gán nhãn bằng chế độ **Shape** (Polyline), không dùng Track.
- **Định nghĩa Instance:** Mỗi dải vạch sơn vật lý liên tục cùng chức năng là **MỘT instance Polyline**.
- **Quy tắc tổ chức thực thể:**
  - **Vạch đứt (Dashed line):** Vẽ **1 Polyline duy nhất** chạy xuyên suốt qua các khoảng trống giữa các nét đứt.
  - **Vạch đôi (Double lines):** Vẽ **1 Polyline duy nhất chạy chính giữa hai vạch**.
  - **Vạch chuyển đổi kiểu dáng giữa chừng (đang đứt $\rightarrow$ liền):** Tách làm **2 Polyline độc lập**, ngắt tại đúng vị trí chuyển tiếp để gán thuộc tính `laneStyle` chuẩn xác cho từng đoạn.
  - **Vạch phân nhánh (Split/Merge Point):** Tại điểm chạc ba (chạc chữ V tách làn), Polyline của dải vạch cũ phải kết thúc ngay tại điểm tách. Bắt đầu 2 Polyline mới riêng biệt cho 2 nhánh rẽ. Không bao giờ vẽ 1 đường cong bẻ ngoặt sang một nhánh mà bỏ rơi nhánh kia.

---

## 3. Geometry rule

### 3.1. Vị trí và Hướng vẽ
- **Tâm vạch (Centerline):** Đặt điểm đúng tâm hình học của dải sơn. Với `road_edge`, đặt điểm đúng mép giao tuyến giữa mặt nhựa đường và chân bó vỉa/rào chắn bê tông.
- **Hướng vẽ (Drawing Direction):** **Bắt buộc vẽ từ Dưới lên Trên (Gần $\rightarrow$ Xa)** theo chiều chuyển động của xe ego để đảm bảo tính nhất quán cho mô hình mạng nơ-ron học luồng di chuyển.

### 3.2. Mật độ điểm (Point Density)
- **Đoạn thẳng:** Chỉ cần đặt 2–3 điểm (khoảng cách giữa các điểm có thể $> 30$ px đến 100 px).
- **Đoạn cong uốn lượn:** Tăng mật độ điểm (cách nhau khoảng 10–15 px/điểm) tại các điểm uốn của đường cong để Polyline ôm mượt mà theo quỹ đạo thực tế, **tuyệt đối không vẽ đường gấp khúc thô kệch (zig-zag)**.

### 3.3. Điểm bắt đầu và Kết thúc (Cutoff Threshold)
- **Điểm bắt đầu (cự ly gần):** Bắt đầu tại mép dưới của ảnh hoặc ngay tại mép trên nắp capo xe ego. Không kéo điểm đè lên phần kim loại của nắp capo.
- **Điểm kết thúc (cự ly xa):** Dừng Polyline ngay khi gặp một trong các điều kiện sau:
  1. Bề rộng hiển thị của vạch thu hẹp xuống **$< 3$ pixel**.
  2. Khoảng cách giữa hai vạch cạnh nhau thu hẹp xuống **$< 10$ pixel** do góc tụ phối cảnh chân trời.
  3. Vạch mờ hoàn toàn hoặc biến thành cụm pixel nhiễu không còn nhận diện được biên vạch với độ tự tin trên 80%.
  4. Vạch kết thúc tại vạch dừng (Stop line) hoặc chạm vào đường biên giao lộ.
- **Chiều dài tối thiểu:** Đoạn vạch nhìn thấy ngắn hơn **30 pixel** ở mép ảnh thì bỏ qua (không vẽ).
- **Dung sai hình học:** Sai số lệch tâm vạch $\le 3$ px ở nửa dưới ảnh; $\le 1$ bề rộng thân vạch ở cự ly xa.

---

## 4. Taxonomy & Attributes

Tất cả các Polyline thuộc class `lane_marking` bắt buộc phải gán đầy đủ các thuộc tính sau (không được để sót `__undefined__`):

### 4.1. Bảng thuộc tính chuẩn

| Thuộc tính | Giá trị cho phép | Ý nghĩa & Quy tắc gán |
|---|---|---|
| `laneTypes` | `single white` | Vạch đơn màu trắng (phân cách các làn cùng chiều, vạch mép phải đường cao tốc). |
| | `single yellow` | Vạch đơn màu vàng (mép trái cao tốc, dải phân cách đường 2 chiều). |
| | `double white` | Vạch đôi màu trắng (ngăn cách chuyển làn). Vẽ 1 line ở giữa. |
| | `double yellow` | Vạch đôi màu vàng (phân chia 2 chiều ngược nhau cấm lấn làn). Vẽ 1 line ở giữa. |
| | `crosswalk` | Đường biên giới hạn (trên và dưới) của khu vực người đi bộ qua đường. |
| | `road curb` | Mép đường vật lý không có sơn (chân bó vỉa, thành cầu, rào chắn Jersey). |
| | `single other` / `double other` | Vạch sơn màu cam/đỏ thi công tạm thời, hoặc vạch cảnh báo đặc biệt. |
| `laneStyle` | `solid` | Vạch sơn liền mạch, liên tục trên toàn đoạn nhìn thấy. |
| | `dashed` | Vạch sơn đứt quãng (có ít nhất 2 khoảng trống đều nhau dọc theo tuyến vạch). |
| `laneDirection` | `parallel` | Vạch chạy dọc song song với chiều di chuyển của xe. |
| | `vertical` | Vạch cắt ngang mặt đường (2 vạch biên của Crosswalk, vạch Stop line). |
| `visibility` | `visible` | Vạch sơn rõ nét, nhận diện dễ dàng. |
| | `partially_occluded` | Vạch bị che khuất một phần bởi bóng râm tòa nhà, cây cối hoặc lóa kính lái. |
| | `faded` | Vạch bị mài mòn, bạc màu, bong tróc hoặc bị ngập nước/bụi bẩn phủ mờ. |
| | `truncated` | Vạch bị cắt cụt đột ngột bởi rìa mép khung hình camera. |
| `needs_review` | `false` (mặc định) | Ca chuẩn xác, rõ ràng theo đúng hướng dẫn. |
| | `true` | Ca bất định, vạch mờ gây tranh cãi hoặc thi công đè lớp vạch cũ. |

---

## 5. Inclusion / exclusion

| Tình huống thực tế | Hành động đối với Polyline | Thuộc tính gán |
|---|---|---|
| Vạch trắng đứt giữa các làn cùng chiều | Vẽ 1 Polyline xuyên qua các nét đứt | `single white`, `dashed`, `parallel` |
| Vạch vàng đôi giữa đường phố 2 chiều | Vẽ 1 Polyline ở chính giữa hai vạch | `double yellow`, `solid`, `parallel` |
| Vạch vàng kép 1 liền + 1 đứt | Vẽ 1 Polyline ở chính giữa hai vạch | `double yellow`, `solid`, `needs_review=true` |
| Vạch trắng liền mép ngoài cùng cao tốc | Vẽ bám tim dải sơn trắng | `single white`, `solid`, `parallel` |
| Bó vỉa hè / Thành rào bê tông không có vạch sơn | Vẽ bám sát giao tuyến chân rào/mép nhựa | `road curb`, `solid`, `parallel` |
| Mép đường đã có vạch trắng liền sát bó vỉa | **CHỈ vẽ vạch sơn trắng**, KHÔNG vẽ thêm `road curb` | `single white`, `solid` |
| Vạch đi bộ qua đường (Crosswalk) | Vẽ **2 đường Polyline** ở biên trên và biên dưới | `crosswalk`, `solid`, `vertical` |
| Vạch sọc gạch bên trong Crosswalk | **BỎ QUA (IGNORE)** | Không gán nhãn |
| Vạch dừng đỗ xe / dừng đèn đỏ (Stop line) | Vẽ 1 đường Polyline ngang mặt đường | `single other`, `solid`, `vertical` |
| Hai viền ngoài vùng tách/nhập làn (Gore area) | Vẽ 2 Polyline bám theo 2 cạnh chữ V | `single white`, `solid`, `parallel` |
| Vạch sơn chéo bên trong vùng Gore area | **BỎ QUA (IGNORE)** | Không gán nhãn |
| Vết trám nhựa đường (bitumen) / Vết nứt đen | **BỎ QUA (IGNORE)** | Không gán nhãn |
| Mũi tên rẽ / Biểu tượng sơn trên mặt đường | **BỎ QUA (IGNORE)** | Không gán nhãn |

---

## 6. Visibility / occlusion

### 6.1. Vật cản che khuất do Phương tiện (Vehicle Occlusion)
- **Quy tắc an toàn sống còn:** Khi vạch kẻ bị che khuất bởi bánh xe hoặc thân xe phía trước, **DỪNG Polyline ngay tại mép thân/lốp xe**.
- **Tuyệt đối KHÔNG vẽ nối xuyên qua xe.** Nếu phía trước xe vạch sơn lại xuất hiện rõ ràng, tạo **MỘT Polyline MỚI** bắt đầu từ mép bên kia của xe.

### 6.2. Vết vá đường & Đứt đoạn mặt đường (Pavement Patching)
- Khi mặt đường có mảng bê tông vá hoặc đào đường làm mất dấu vết sơn:
  - Nếu khoảng đứt đoạn ngắn $\le 1.5$ mét và hai đầu thẳng hàng: Cho phép vẽ nối qua, gán `visibility = faded`.
  - Nếu khoảng đứt đoạn $> 1.5 - 2.0$ mét: **Ngắt Polyline**, dừng tại mép vết vá và bắt đầu Polyline mới khi vạch sơn xuất hiện lại.

### 6.3. Bóng râm & Lóa kính lái (Shadows & Glare)
- **Bóng cây / Bóng tòa nhà / Bóng cầu vượt:** Vẫn vẽ Polyline xuyên qua vùng bóng râm nếu mắt người nhìn xuyên được cấu trúc vạch sơn, gán `visibility = partially_occluded`.
- **Kính chắn gió bị lóa sáng (như góc dưới trái ảnh BDD06):** Vẽ liền nét Polyline xuyên qua vùng lóa nếu xu hướng tuyến đường hai đầu thẳng hàng rõ ràng; gán `visibility = partially_occluded`.
- **Giọt mưa / Decal trên kính:** Bỏ qua các vật dính trên kính, chỉ vẽ vạch sơn thật trên mặt đường.

### 6.4. Vệt nước mưa phản quang (Reflective Puddles)
- Trời mưa mặt đường ướt tạo ra các dải sáng phản chiếu đèn thẳng tắp rất giống vạch sơn. Annotator phải zoom kiểm tra kỹ: chỉ vẽ khi thấy rõ kết cấu hạt sơn nổi; **BỎ QUA** nếu chỉ là dải sáng phản quang của nước.

---

## 7. Ambiguity / escalation

Quy tắc phân xử minh bạch và ghi nhận trong file xuất CVAT:
- **LABEL:** Vạch sơn hoặc mép đường nhận diện rõ ràng, có đầy đủ bằng chứng hình ảnh.
- **IGNORE:** Các đối tượng ngoài scope (vết nứt, bóng đổ, vạch sọc trong gore, mũi tên).
- **UNKNOWN:** Task này không sử dụng class unknown. Mọi trường hợp phân vân màu sắc (do ám màu đèn đêm hoặc chói chang) $\rightarrow$ chọn màu theo khả năng cao nhất + tick `needs_review = true`.
- **ESCALATE (Bật `needs_review = true`):**
  1. **Vạch cũ chưa xóa sạch (Ghost Lines):** Có vết cạo vạch cũ màu xám mờ chạy song song vạch mới $\rightarrow$ chỉ vẽ vạch mới rõ nhất, nếu hai vạch tranh chấp khó phân biệt thì vẽ vạch rõ hơn và bật `needs_review = true`.
  2. **Vạch mòn nặng bất thường:** Vạch bị bào mòn loang lổ nhiều đoạn không rõ nguyên nhân $\rightarrow$ vẽ đoạn còn dấu vết + bật `needs_review = true`.
  3. **Vạch vàng kép kết hợp (1 vạch liền + 1 vạch đứt song song):** Vẽ 1 Polyline ở giữa hai vạch, chọn `laneTypes = double yellow`, `laneStyle = solid` và bật `needs_review = true`.

---

## 8. Temporal rule

- Không áp dụng — Task thực hiện trên tập ảnh tĩnh đơn lẻ 2D (Static Images).
- Mỗi ảnh được xử lý hoàn toàn độc lập bằng công cụ **Shape**, không liên kết ID giữa các ảnh.

---

## 9. Examples

| Sample ID | Tình huống quan sát | Expected Output chuẩn | Quy tắc áp dụng |
|---|---|---|---|
| **BDD01** | Cao tốc ban ngày; lối ra có vùng đệm tam giác (Gore area); xe SUV đen phía trước. | Vẽ 1 Polyline xuyên vạch đứt bên trái; vẽ 2 Polyline cho 2 viền ngoài vùng Gore (`single white`, `solid`); **không vẽ** vạch sọc chéo bên trong; dừng Polyline tại đuôi xe SUV. | Mục 1.4, 2, 5 & 6.1 |
| **BDD04** | Tuyến phố 2 chiều; vạch vàng đôi giữa đường; mép phải có vỉa hè không vạch sơn. | Vẽ **1 Polyline ở chính giữa vạch vàng đôi** (`double yellow`, `solid`, `parallel`); vẽ 1 Polyline mép bó vỉa hè (`road curb`, `solid`); không vẽ logo xe đạp trên đường. | Mục 2, 4.1 & 5 |
| **BDD06** | Cao tốc uốn cong; kính lái góc dưới trái bị lóa sáng; vạch xa mờ dần. | Vẽ xuyên qua vùng lóa kính (`partially_occluded`); tăng mật độ điểm uốn cua (10–15 px/điểm); dừng Polyline ở cự ly xa khi bề rộng $< 3$ px hoặc khoảng cách $< 10$ px. | Mục 3.2, 3.3 & 6.3 |
| **BDD07** | Đường đô thị có vết vá nhựa đường vuông vức; bóng cây che ngang; vạch vàng phân làn. | Nếu vết vá nhựa cắt đứt vạch $> 1.5$m $\rightarrow$ ngắt thành 2 Polyline riêng biệt; đoạn vạch dưới bóng cây vẽ bình thường kèm gán `partially_occluded`. | Mục 6.2 & 6.3 |
| **BDD09** | Nút giao nhập làn cong (Merge Ramp); vạch đứt trắng mở rộng theo nhánh rẽ. | Polyline kết thúc tại điểm chia tách chạc ba; tạo 2 Polyline mới rẽ sang 2 nhánh; vẽ mượt theo độ cong đường nhánh. | Mục 2 & 3.2 |
| **BDD02** | Ngã tư đô thị; có vạch người đi bộ Crosswalk bản lớn và vạch Stop line. | Vẽ **2 Polyline giới hạn biên trên và biên dưới của Crosswalk** (`crosswalk`, `vertical`); không vẽ từng sọc ngắn; các vạch phân làn dọc dừng lại tại mép vạch dừng. | Mục 1.3 & 5 |
| **BDD08** | Cao tốc nhiều làn; vạch trắng liền mép đường; xe phía trước đè lên vạch phân làn. | Vẽ vạch mép đường (`single white`, `solid`); tại vị trí xe phía trước đè lên vạch, **dừng Polyline ngay tại mép bánh xe**, không nối xuyên qua gầm xe. | Mục 5 & 6.1 |

---

## 10. Common mistakes (10 lỗi thường gặp & cách khắc phục)

1. **Nối xuyên qua xe khác (Critical):** Kéo vạch xuyên qua gầm hoặc thân ô tô phía trước. $\rightarrow$ *Khắc phục: Luôn dừng Polyline sát mép thân/bánh xe.*
2. **Cắt vụn vạch đứt (Major):** Vẽ mỗi nét đứt thành 1 đường line 10 px. $\rightarrow$ *Khắc phục: Chỉ dùng 1 Polyline duy nhất nối qua tâm toàn bộ chuỗi nét đứt.*
3. **Vẽ 2 đường cho vạch đôi (Major):** Vẽ 2 Polyline song song cho vạch vàng đôi. $\rightarrow$ *Khắc phục: Chỉ vẽ 1 Polyline duy nhất ở giữa hai vạch, chọn `double yellow`.*
4. **Vẽ vạch chéo trong vùng Gore (Major):** Vẽ toàn bộ các vạch sơn chéo bên trong tam giác đệm lối ra. $\rightarrow$ *Khắc phục: Chỉ vẽ 2 đường viền ranh giới bao ngoài.*
5. **Vẽ từng sọc vạch người đi bộ (Major):** Bỏ thời gian vẽ hàng chục nét gạch ngang của Crosswalk. $\rightarrow$ *Khắc phục: Chỉ vẽ đúng 2 đường biên trên và dưới của cụm vạch.*
6. **Vẽ theo vết nứt / vết trám nhựa đường (Major):** Nhầm vết bitum trám đường là vạch sơn. $\rightarrow$ *Khắc phục: Kiểm tra tính đối xứng và màu sắc sơn thực tế.*
7. **Nhầm vệt nước phản chiếu là vạch sơn (Critical):** Vẽ đường line lên vệt sáng phản quang trên đường ướt sũng. $\rightarrow$ *Khắc phục: Phóng to 100% kiểm tra kết cấu hạt sơn.*
8. **Đoạn cong bị gấp khúc thô (Minor):** Đặt quá ít điểm trên đường cong cao tốc khiến Polyline cắt góc. $\rightarrow$ *Khắc phục: Thêm điểm dày hơn (10–15 px) tại khúc cua.*
9. **Kéo dài vô tận về đường chân trời (Minor):** Cố đoán vẽ vạch về cự ly 100m khi chỉ còn là đốm mờ. $\rightarrow$ *Khắc phục: Dừng ngay khi bề rộng vạch $< 3$ px.*
10. **Bỏ quên giá trị `__undefined__` (Major):** Không gán thuộc tính sau khi vẽ. $\rightarrow$ *Khắc phục: Bật Attribute Annotation Mode rà soát lại toàn bộ ảnh trước khi xuất file.*

---

## Phụ lục: Quy trình gán nhãn 1 ảnh chuẩn (Checklist 5 phút)

1. **Quan sát tổng thể (15 giây):** Xác định làn xe ego $\rightarrow$ Vị trí vạch đôi giữa đường $\rightarrow$ Điểm tách/nhập làn $\rightarrow$ Khu vực có xe che hoặc vết vá đường.
2. **Lượt 1 — Vẽ Geometry (Polyline):**
   - Vẽ từ trái sang phải, mỗi vạch bắt đầu **từ dưới lên trên**.
   - Vẽ 1 line xuyên tim cho vạch đứt; 1 line chính giữa cho vạch đôi.
   - Nhớ vẽ `road_edge` ở mép đường không có sơn; vẽ 2 đường biên của Crosswalk nếu có.
   - Dừng vạch tại mép chướng ngại vật (xe đỗ, xe phía trước).
3. **Lượt 2 — Gán thuộc tính (Attribute Mode):**
   - Chuyển sang chế độ **Attribute Annotation** trên góc phải CVAT.
   - Đi qua từng Polyline, chọn đúng `laneTypes`, `laneStyle`, `laneDirection`, `visibility`.
   - Nếu gặp ca khó/mờ/chắp vá $\rightarrow$ tick chọn `needs_review = true`.
4. **Tự kiểm tra (Self-QC):** Đảm bảo không còn bất kỳ object nào giữ giá trị `__undefined__`.
5. **Lưu bài:** Bấm `Ctrl + S` để lưu kết quả.
