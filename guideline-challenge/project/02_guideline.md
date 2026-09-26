# Annotation Guideline — BDD100K 2D Road Elements & Lane Markings
## Bounding Box, Polygon & Polyline

**Version: v3**

> **Tài liệu tham chiếu & Nguồn chuẩn hóa chính thức:**
> 1. **Qatar Road Marking Guidelines** (`https://www.roadmarkingqatar.com/post/road-marking-guideline`):
>    - *"Single Solid Yellow Line: Indicates the center of a road with two-way traffic, helping drivers understand the flow of oncoming vehicles."*
>    - *"Double Solid Yellow Line: Represents a strict no-passing zone, indicating that drivers must not cross these lines to overtake another vehicle."*
>    - *"Broken Yellow Line: Allows passing when the broken line is adjacent to the driver's lane."*
>    - *"Single Solid White Line: Marks traffic lanes moving in the same direction... Crossing is discouraged."*
>    - *"Double Solid White Lines: Serve as a barrier between regular use lanes and preferential use lanes... Drivers are prohibited from crossing."*
>    - *"Broken White Lines: Separate traffic lanes on roads with two or more lanes moving in the same direction, allowing for lane changes."*
>    - *"End of Lane Marking: Indicates that a lane is about to end, prompting drivers to prepare to exit or merge."*
>    - *"Yield Line: Composed of a line of solid triangles, indicating to approaching vehicles where they must yield or stop."*
> 2. **Kognic Edge Cases in Autonomous Driving** (`https://www.kognic.com/articles/edge-cases-autonomous-driving`):
>    - *"Edge cases in autonomous driving represent rare or complex visual scenarios, degraded road markings, severe occlusion, extreme weather (rain, snow, fog), and night glare where standard perception models fail without clear annotation guidelines."*
> 3. **ResearchGate Computer Vision Traffic Monitoring & Control Metrics** (`https://www.researchgate.net/publication/386284928_Computer_Vision_for_Intelligent_Traffic_Monitoring_and_Control`):
>    - *"Evaluating computer vision models for traffic monitoring relies on object detection metrics (mAP, F1-score), polygon segmentation metrics (mIoU, Boundary F1), polyline alignment metrics (Chamfer distance, Fréchet distance), and inter-annotator agreement statistics (Fleiss' Kappa)."*
> 4. **Guideline Lane & Drivable Area v1** (`Guideline_Lane_Drivable_v1.docx`):
>    - *"1 vạch sơn dọc đường = 1 polyline, đặt điểm ở tâm vạch, vẽ từ dưới lên. Vạch đứt vẫn là 1 polyline liền. Vạch đôi = 1 polyline ở giữa hai vạch. Polygon dừng ở mép dưới xe đầu tiên phía me trong làn đó. Không tô lên xe, không tô lên nắp capo."*

---

## 1. Objective + Scope

- **Mục tiêu:** Tạo dữ liệu annotation 2D **nhất quán, đúng taxonomy và đạt chuẩn chất lượng sản xuất** trên tập ảnh giao thông đường bộ BDD100K (`data/bdd100k/*.jpg`). Dữ liệu này đủ tiêu chuẩn để phục vụ công tác review độc lập, đo lường độ trùng khớp với Ground Truth (GTS / Calibration / Blind Test), và cấp vào pipeline huấn luyện/đánh giá (training/evaluation) cho các mô hình tự hành Multi-Task Learning (Detection + Segmentation + Lane Perception).
- **Công cụ thực hiện:** CVAT (Computer Vision Annotation Tool).
- **Phạm vi gồm 3 nhóm nhãn độc lập**, mỗi nhóm bắt buộc sử dụng đúng một loại shape hình học duy nhất trong CVAT:

| Nhóm nhãn | CVAT Shape | Mục đích & Ý nghĩa |
|---|---|---|
| **Object instance** | **Rectangle / Bounding Box** | Định vị và phân loại từng đối tượng giao thông rời rạc (phương tiện, người, biển báo, đèn giao thông). |
| **Drivable area** | **Polygon** | Khoanh vùng chính xác bề mặt lòng đường mà xe có thể / được phép lưu thông (`area/drivable` vs `area/alternative`). |
| **Lane marking** | **Polyline** | Vẽ bám theo tim hoặc biên của các vạch sơn kẻ đường và mép bó vỉa theo quy chuẩn Qatar & Kognic. |

> [!IMPORTANT]
> **Quy tắc bất biến:**
> - Tuyệt đối **không dùng Polygon và Polyline thay thế lẫn nhau** trong cùng một bài làm. Drivable area bắt buộc dùng Polygon; Lane marking bắt buộc dùng Polyline.
> - **Chỉ annotate các class được quy định trong tài liệu này (Mục 4).**
> - Không tự ý tạo class mới, không đổi tên class, không gộp class theo suy đoán cảm tính.

---

## 2. Annotation Unit

- **Bounding Box (Object instance):**
  - **Một box = Một đối tượng độc lập (Single instance).**
  - Không bao giờ gộp nhiều đối tượng đứng sát nhau vào cùng một box chung.
- **Polygon (Drivable area):**
  - **Một polygon = Một vùng bề mặt đường liên tục.**
  - Phân định rõ ràng giữa làn đường xe ego đang chạy trực tiếp (`area/drivable`) và các làn kế cận/thay thế (`area/alternative`). Dừng polygon tại mép cản dưới xe đầu tiên phía trước.
- **Polyline (Lane marking):**
  - **Một polyline = Một vệt vạch kẻ đường liên tục** cùng ý nghĩa ngữ nghĩa (semantic).
  - Vạch đứt quãng (dashed line) được tính là **một polyline duy nhất** chạy dọc qua tim của các nét đứt, không ngắt quãng thành từng polyline nhỏ theo từng sọc sơn.
  - Vạch đôi song song (`double yellow` / `double white`) được vẽ bằng **một polyline duy nhất ở chính giữa hai nét sơn**.

---

## 3. Geometry Rule

### 3.1. Bounding Box (Object Instance)
- **Bao sát đối tượng (Tight Box):** Vẽ box ôm khít các mép ngoài cùng nhìn thấy được của đối tượng (visible boundary), hạn chế tối đa phần nền thừa (background padding). Lệch biên chấp nhận $\le 2\text{ px}$.
- **Không bao giờ vẽ box vượt ra ngoài mép ảnh:** Giới hạn tọa độ luôn nằm trong $[0, 0, W, H]$. Đối tượng bị cắt ở biên ảnh phải dừng đúng mép frame và bật thuộc tính `truncated = true`.
- **Loại trừ bóng đổ và phản chiếu:** Không bao gồm bóng của xe/người trên mặt đường; không kéo dài box để ôm bóng đổ.
- **Vật thể bị che khuất một phần (Occluded):** Vẫn vẽ box ôm trọn phần nhìn thấy của vật thể nếu còn đủ bằng chứng thị giác để nhận diện class; bật `occluded = true`.

### 3.2. Polygon (Drivable Area)
- **Bám sát biên quan sát được:** Vẽ bám khít mép lòng đường nhìn thấy được (mép vỉa hè, rào chắn hộ lan, vạch mép đường). Tuyệt đối không phóng to hoặc vẽ tràn ra ngoài theo suy đoán.
- **Không tự cắt (No Self-Intersection):** Không để các cạnh của cùng một polygon chéo qua nhau tạo thành hình xoắn số 8 hoặc nút thắt.
- **Mật độ điểm tối ưu:** Trên các đoạn đường thẳng chỉ dùng ít điểm (2–3 điểm); tăng dày mật độ điểm tại các đoạn đường cong hoặc nút giao phức tạp.
- **Không tạo vùng overlap vô nghĩa:** Vùng `area/drivable` và `area/alternative` tiếp giáp nhau tại ranh giới làn đường, không được đè chồng chéo lên nhau. Không vẽ tràn lên vỉa hè (sidewalk) hay dải phân cách.

### 3.3. Polyline (Lane Marking)
- **Bám tim vạch kẻ đường:** Polyline phải đi chính xác theo đường tim (centerline) của vạch sơn.
- **Hướng vẽ nhất quán:** Giữ chiều vẽ từ dưới lên (gần đến xa theo chiều di chuyển của xe).
- **Quy tắc dừng polyline (Termination Rule):**
  - Dừng polyline ngay tại điểm vạch sơn bị phương tiện khác che khuất (**không vẽ xuyên qua xe**).
  - Dừng polyline tại điểm vạch sơn mờ dần và không còn đủ bằng chứng thị giác rõ ràng trên ảnh.

---

## 4. Taxonomy (Class vs. Attribute Design)

Bảng taxonomy chuẩn hóa gồm 19 classes chia làm 3 nhóm hình học và 2 attributes:

| Nhóm | CVAT Shape | Danh sách Class chính thức |
|---|---|---|
| **Object instance** | Rectangle / BBox | `pedestrian`, `rider`, `car`, `truck`, `bus`, `train`, `motorcycle`, `bicycle`, `traffic light`, `traffic sign` |
| **Drivable area** | Polygon | `area/drivable`, `area/alternative` |
| **Lane marking** | Polyline | `lane/crosswalk`, `lane/double white`, `lane/double yellow`, `lane/road curb`, `lane/single other`, `lane/single white`, `lane/single yellow` |

### Hệ thống Attributes (Áp dụng cho Object Instance — BBox):

| Tên Attribute | Kiểu / Giá trị | Mặc định | Khi nào bật |
|---|---|---|---|
| `occluded` | `true` / `false` | `false` | Bật `true` khi vật thể bị che khuất một phần bởi đối tượng khác. |
| `truncated` | `true` / `false` | `false` | Bật `true` khi vật thể bị cắt bởi mép biên ảnh. |

---

## 5. Inclusion / Exclusion

### 5.1. Bắt buộc Annotate (Inclusion)
- Tất cả các đối tượng thuộc 10 class object instance, 2 class drivable area và 7 class lane marking nhìn thấy được trong ảnh và có đủ bằng chứng thị giác.
- Các đối tượng bị che một phần hoặc bị cắt mép nhưng vẫn nhận diện được class rõ ràng.
- Các loại vạch theo Qatar Road Marking: Solid Yellow, Double Solid Yellow, Broken Yellow, Solid White, Double Solid White, Broken White, End of Lane, Yield Line (hàng tam giác).

### 5.2. Tuyệt đối Loại trừ (Exclusion — IGNORE)
- **Bóng đổ (Shadows):** Không vẽ bóng của xe cộ, người đi bộ, cột điện đổ xuống mặt đường.
- **Hình phản chiếu (Reflections):** Không annotate hình ảnh phản chiếu trên mặt kính xe, vũng nước đọng, gương chiếu hậu.
- **Hình in trên biển quảng cáo/màn hình (Billboard / Advertisements):** Không annotate hình ảnh người, xe hơi hoặc đồ vật in trên các pano quảng cáo.
- **Vật thể ngoài danh mục:** Rào chắn tạm thời không phải curb, cây cối, động vật, tòa nhà, thùng rác.

---

## 6. Visibility / Occlusion

| Tình huống hiển thị | Giá trị Attribute | Tiêu chuẩn áp dụng & Ví dụ |
|---|---|---|
| **Hiển thị đầy đủ** | `occluded=false`<br>`truncated=false` | Vật thể nằm trọn vẹn trong ảnh, không bị che khuất. |
| **Bị che một phần** | `occluded=true`<br>`truncated=false` | Xe con đỗ sau xe tải lớn, người chỉ nhìn thấy nửa thân trên. |
| **Bị cắt bởi biên ảnh** | `occluded=false`<br>`truncated=true` | Xe nằm ở sát mép trái/phải, một phần thân nằm ngoài tầm nhìn camera. |
| **Vừa che vừa cắt mép** | `occluded=true`<br>`truncated=true` | Xe xuất hiện ở mép ảnh và đồng thời bị cây cối che lấp một phần. |

---

## 7. Ambiguity & Escalation (LABEL / IGNORE / UNKNOWN / ESCALATE)

| Quyết định | Khi nào áp dụng | Cách thể hiện trong CVAT |
|---|---|---|
| **LABEL** | Đối tượng có class và boundary rõ ràng, đủ bằng chứng thị giác. | Vẽ đúng shape (BBox/Polygon/Polyline), chọn đúng class và gán attribute chuẩn. |
| **IGNORE** | Nằm trong danh sách Exclusion (bóng đổ, phản chiếu, hình in trên pano, vật ngoài taxonomy). | Bỏ qua hoàn toàn, không tạo annotation. |
| **UNKNOWN / CẦN REVIEW** | Thuộc scope nhưng quá mờ, bị che khuất nặng, hoặc phân vân giữa 2 class. | Vẽ shape nếu còn xác định được vị trí, tạo **CVAT Issue** tương ứng. |
| **ESCALATE** | Tình huống lạ (Edge Case) theo quy chuẩn Kognic chưa từng có tiền lệ. | Tạo **CVAT Issue** loại `UNCERTAIN_SCOPE`, gắn cờ escalate để Mentor/Lead duyệt quy tắc mới. |

---

## 8. Temporal Rule

- Dataset BDD100K trong bài thực hành gồm các ảnh tĩnh độc lập (`.jpg`).
- Mỗi ảnh được gán nhãn hoàn toàn độc lập (Independent image-level annotation).
- Áp dụng nguyên tắc "Draw what you see" (Vẽ chính xác những gì nhìn thấy trong khung hình hiện tại). Không suy diễn thông tin từ các frame ảnh khác.

---

## 9. Examples & Visual Illustrations

### Bảng tra cứu tình huống thực tế (BDD100K Samples & Edge Cases):

| Sample ID | Tình huống quan sát | Quyết định & Output | Rule áp dụng |
|---|---|---|---|
| `BDD01` | Xe SUV màu đen chạy phía trước trong làn ego | BBox `car` (`occluded=false`, `truncated=false`) | BBox ôm khít thân xe, loại trừ bóng đổ |
| `BDD01` | Vạch kẻ đứt màu trắng phân làn cao tốc | 1 Polyline `lane/single white` bám tim vạch | Vạch đứt vẽ 1 polyline liền qua tim |
| `BDD02` | Người đi bộ qua đường tại ngã tư | BBox `pedestrian` ôm khít thân người | 1 box cho 1 người |
| `BDD03` | Vạch vàng đơn mép trái cao tốc cong | Polyline `lane/single yellow` bám tim vạch | Qatar Guideline: Single Solid Yellow Line |
| `BDD04` | Vạch vàng đôi tim đường 2 chiều | 1 Polyline `lane/double yellow` ở giữa 2 nét sơn | Qatar Guideline: Double Solid Yellow Line |
| `BDD06` | Xe đi trước che vạch kẻ đường | Dừng Polyline tại mép cản sau xe | Guideline v1: Không vẽ xuyên qua thân xe |
| `BDD10` | Vạch tam giác nhường đường tại ngã tư | Polyline `lane/single other` bám chân tam giác | Qatar Guideline: Yield Line (solid triangles) |
| `BDD12` | Vạch mờ nặng và ngã tư sương mù | ESCALATE (`UNCERTAIN_SCOPE`) | Kognic Edge Case: Không suy đoán cảm tính |
| `BDD13` | Vạch trắng đôi phân làn xe buýt | Polyline `lane/double white` ở giữa 2 vạch | Qatar Guideline: Double Solid White Lines |

---

## 10. Common Mistakes & Cách khắc phục

1. **Gộp nhiều đối tượng vào một box:** Luôn tách riêng mỗi cá thể là một BBox độc lập (`1 instance = 1 box`).
2. **Kéo BBox bao trùm cả bóng đổ xe:** Chỉ ôm sát phần kim loại/bánh xe chạm đất, loại trừ toàn bộ bóng đổ.
3. **Vẽ Polyline xuyên qua xe cộ:** Gặp chướng ngại che khuất phải ngắt polyline tại mép cản trước/sau của xe.
4. **Dùng nhầm Polygon cho vạch kẻ đường:** Mọi loại vạch kẻ đường bắt buộc dùng Polyline bám tim vạch.
5. **Polygon tự cắt (Self-intersection) hoặc overlap:** Kiểm tra kỹ hình học polygon, các vùng phân chia làn phải tiếp giáp nhau chứ không chồng lấn.
6. **Đoán mò thay vì báo cáo Issue:** Dừng suy đoán khi vạch bị mờ nặng, tạo Issue `UNCERTAIN_CLASS` / `SCOPE` để Reviewer/Mentor xử lý.

---

## Phụ lục 1: Checklist Chất Lượng Trước Khi Submit

- [ ] **1. Đúng Taxonomy & Shape:** 100% đối tượng được vẽ bằng đúng loại shape quy định.
- [ ] **2. Không bỏ sót (Completeness):** Không bỏ quên xe, người, biển báo, đèn tín hiệu hoặc vạch đường rõ ràng.
- [ ] **3. BBox ôm khít (Tight Box):** Khung bao sát đối tượng, không thừa nền, không chứa bóng đổ.
- [ ] **4. Polygon chuẩn xác:** Bám sát mép lòng đường, không tự cắt (no self-intersection), không tràn lên vỉa hè.
- [ ] **5. Polyline đúng quy ước:** Bám tim vạch đứt, dừng đúng điểm khi bị che, không vẽ xuyên qua xe.
- [ ] **6. Attributes chính xác:** Gán đúng `occluded=true` khi bị che và `truncated=true` khi bị cắt mép ảnh.

---

## Phụ lục 2: Tiêu Chí Reviewer Kiểm Tra (Audit Matrix)

| Hạng mục kiểm tra | Nội dung Reviewer đánh giá | Mức độ nghiêm trọng nếu sai |
|---|---|---|
| **Taxonomy Compliance** | Gán đúng class trong 19 class; đúng loại shape quy định. | **Critical** |
| **Completeness** | Không bỏ sót đối tượng rõ ràng; không vẽ thừa đối tượng loại trừ. | **High** |
| **Geometry Accuracy** | Box ôm khít; polygon không tự cắt; polyline không vẽ xuyên xe. | **High** |
| **Attribute Precision** | Bật đúng `occluded` khi bị che và `truncated` khi bị cắt mép ảnh. | **Medium** |
| **Escalation Protocol** | Không tự ý sáng tạo quy tắc đối với edge case; escalate cho Lead. | **Critical** |

---

## Phụ lục 3: Bảng Tra Cứu Nhanh (Quick Reference)

| Tình huống thực tế | Hành động bắt buộc (Làm gì) | Hành động cấm (Không làm) | Cần Review? |
|---|---|---|---|
| Xe / Người hiển thị rõ ràng | Vẽ BBox ôm khít đối tượng | Không gộp nhiều đối tượng vào 1 box | Không |
| Xe bị che khuất một phần | BBox phần nhìn thấy + gán `occluded=true` | Không bỏ sót chỉ vì bị che | Không |
| Xe bị cắt bởi mép ảnh | BBox chạm mép + gán `truncated=true` | Không vẽ box tràn ra ngoài mép ảnh | Không |
| Lòng đường lưu thông | Vẽ Polygon bám mép đường | Không dùng Polyline tùy ý | Nếu boundary mờ |
| Vạch kẻ đường | Vẽ Polyline theo tim vạch | Không dùng Polygon thay thế | Nếu class mờ |
| Vạch kẻ đường bị xe che | Dừng Polyline tại mép thân xe | Không vẽ nối tiếp xuyên qua thân xe | Không |
| Không chắc chắn về Class | Tạo Issue `UNCERTAIN_CLASS` | Không tự đoán class cho xong việc | **Có** |
