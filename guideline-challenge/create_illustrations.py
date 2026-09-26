#!/usr/bin/env python3
"""
Script to generate high quality visual illustrations for BDD100K 2D Annotation Guideline.
Saves images to guideline-challenge/assets/images/ and guideline-challenge/project/assets/images/
"""

import os
import cv2
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.lines import Line2D

BASE = os.path.dirname(os.path.abspath(__file__))
OUT_DIRS = [
    os.path.join(BASE, 'assets/images'),
    os.path.join(BASE, 'project/assets/images')
]
for d in OUT_DIRS:
    os.makedirs(d, exist_ok=True)

# -------------------------------------------------------------
# 1. Bounding Box Illustration (Tight vs Loose, Occluded, Truncated, Classes, Exclusions)
# -------------------------------------------------------------
def create_bbox_illustration():
    img_bgr = cv2.imread(os.path.join(BASE, 'data/bdd100k/') + 'BDD01.jpg')
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 11), dpi=150)
    fig.patch.set_facecolor('#f8f9fa')
    
    # Subplot 1: DO vs DON'T (Tight BBox vs Loose BBox / Shadow inclusion)
    ax1 = axes[0, 0]
    # Crop around the black SUV in BDD01 (x: 480 to 720, y: 300 to 450)
    crop1 = img_rgb[300:460, 480:740]
    ax1.imshow(crop1)
    ax1.set_title("1. Bounding Box: Bao sát (Tight) vs Thừa nền/bóng (Loose)", fontsize=13, fontweight='bold', pad=10)
    
    # Correct BBox (Green)
    rect_correct = patches.Rectangle((50, 25), 160, 115, linewidth=2.5, edgecolor='#00E676', facecolor='none')
    ax1.add_patch(rect_correct)
    ax1.text(50, 18, "DO: car [Tight, không lấy bóng]", color='#00E676', fontsize=11, fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.2", facecolor='#1b5e20', alpha=0.8, edgecolor='none'))
    
    # Wrong BBox (Red dashed - loose, including shadow)
    rect_wrong = patches.Rectangle((35, 10), 195, 145, linewidth=2, edgecolor='#FF1744', linestyle='--', facecolor='none')
    ax1.add_patch(rect_wrong)
    ax1.text(35, 150, "DON'T: Thừa nền & ôm cả bóng xe!", color='#FF1744', fontsize=11, fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.2", facecolor='#b71c1c', alpha=0.8, edgecolor='none'))
    ax1.axis('off')
    
    # Subplot 2: Occluded vs Truncated
    ax2 = axes[0, 1]
    # Crop right side of BDD01 showing the white car and right edge (x: 750 to 1280, y: 300 to 520)
    crop2 = img_rgb[310:510, 780:1280]
    ax2.imshow(crop2)
    ax2.set_title("2. Attributes: Occluded (Bị che) & Truncated (Cắt mép ảnh)", fontsize=13, fontweight='bold', pad=10)
    
    # Car partially visible / ahead (occluded)
    rect_car_ahead = patches.Rectangle((20, 25), 200, 150, linewidth=2.5, edgecolor='#00E676', facecolor='none')
    ax2.add_patch(rect_car_ahead)
    ax2.text(20, 18, "car [occluded=false, truncated=false]", color='#00E676', fontsize=10, fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.2", facecolor='#1b5e20', alpha=0.8, edgecolor='none'))
    
    # Car touching/cut by image right border (truncated)
    rect_trunc = patches.Rectangle((370, 60), 125, 135, linewidth=2.5, edgecolor='#FF9100', facecolor='none')
    ax2.add_patch(rect_trunc)
    ax2.text(270, 52, "car [truncated=true]", color='#FF9100', fontsize=10, fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.2", facecolor='#e65100', alpha=0.8, edgecolor='none'))
    ax2.axis('off')

    # Subplot 3: Multi-class instances on BDD02 (Intersection: traffic light, traffic sign, pedestrian, car)
    ax3 = axes[1, 0]
    img2_bgr = cv2.imread(os.path.join(BASE, 'data/bdd100k/') + 'BDD02.jpg')
    img2_rgb = cv2.cvtColor(img2_bgr, cv2.COLOR_BGR2RGB)
    crop3 = img2_rgb[150:550, 300:900]
    ax3.imshow(crop3)
    ax3.set_title("3. Đa dạng đối tượng (pedestrian, traffic light, traffic sign, car)", fontsize=13, fontweight='bold', pad=10)
    
    # Traffic light
    rect_tl = patches.Rectangle((180, 20), 45, 75, linewidth=2.5, edgecolor='#FFD600', facecolor='none')
    ax3.add_patch(rect_tl)
    ax3.text(140, 12, "traffic light", color='#FFD600', fontsize=10, fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.2", facecolor='#f57f17', alpha=0.8, edgecolor='none'))
    
    # Traffic sign
    rect_ts = patches.Rectangle((480, 60), 40, 45, linewidth=2.5, edgecolor='#00B0FF', facecolor='none')
    ax3.add_patch(rect_ts)
    ax3.text(450, 50, "traffic sign", color='#00B0FF', fontsize=10, fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.2", facecolor='#01579b', alpha=0.8, edgecolor='none'))
    
    # Pedestrians
    rect_ped = patches.Rectangle((60, 160), 35, 95, linewidth=2.5, edgecolor='#E040FB', facecolor='none')
    ax3.add_patch(rect_ped)
    ax3.text(50, 150, "pedestrian", color='#E040FB', fontsize=10, fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.2", facecolor='#4a148c', alpha=0.8, edgecolor='none'))
    
    # Car in intersection
    rect_car_cross = patches.Rectangle((230, 160), 160, 110, linewidth=2.5, edgecolor='#00E676', facecolor='none')
    ax3.add_patch(rect_car_cross)
    ax3.text(230, 150, "car [occluded=true]", color='#00E676', fontsize=10, fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.2", facecolor='#1b5e20', alpha=0.8, edgecolor='none'))
    ax3.axis('off')

    # Subplot 4: Exclusions (Billboard, Reflection, Shadow)
    ax4 = axes[1, 1]
    # Blank/diagrammatic visual guide for exclusion
    ax4.set_facecolor('#ffffff')
    ax4.set_xlim(0, 10)
    ax4.set_ylim(0, 10)
    ax4.set_title("4. Quy tắc LOẠI TRỪ (EXCLUSION) - KHÔNG ĐƯỢC VẼ", fontsize=13, fontweight='bold', pad=10)
    
    rules = [
        ("❌ BÓNG ĐỔ (Shadow):", "Không vẽ box cho bóng xe/người trên mặt đường. Không kéo rộng box xe để bao bóng."),
        ("❌ PHẢN CHIẾU (Reflection):", "Không vẽ hình ảnh phản chiếu của xe/đèn qua gương chiếu hậu, kính xe, vũng nước."),
        ("❌ HÌNH IN / MÀN HÌNH (Billboard):", "Không vẽ người/xe in trên biển quảng cáo, áp phích, màn hình LED ven đường."),
        ("❌ GỘP OBJECT (Multi-object):", "Không dùng 1 box chung bao 2 xe gần nhau. Mỗi đối tượng phải có 1 box độc lập."),
        ("❌ VƯỢT BIÊN ẢNH:", "Box không được vượt quá tọa độ biên ảnh (0, 0, W, H). Bị cắt thì bật truncated=true.")
    ]
    
    y = 8.8
    for title, desc in rules:
        ax4.text(0.5, y, title, fontsize=11, fontweight='bold', color='#D50000')
        ax4.text(0.5, y - 0.7, desc, fontsize=10, color='#263238', wrap=True)
        y -= 1.8
        
    ax4.axis('off')
    
    plt.tight_layout()
    for d in OUT_DIRS:
        fig.savefig(os.path.join(d, '01_bbox_illustration.png'), bbox_inches='tight')
    plt.close(fig)
    print("Created 01_bbox_illustration.png")

# -------------------------------------------------------------
# 2. Drivable Area Polygon Illustration (Direct vs Alternative, Geometry rules)
# -------------------------------------------------------------
def create_drivable_illustration():
    # Use BDD03 (curved highway with drivable area ground truth)
    img_bgr = cv2.imread(os.path.join(BASE, 'data/bdd100k/') + 'BDD03.jpg')
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    H, W, _ = img_rgb.shape

    fig, axes = plt.subplots(1, 2, figsize=(16, 6.5), dpi=150)
    fig.patch.set_facecolor('#f8f9fa')
    
    # Left: Drivable Direct vs Alternative
    ax1 = axes[0]
    ax1.imshow(img_rgb)
    ax1.set_title("Drivable Area: area/drivable (Xanh lá) vs area/alternative (Xanh dương)", fontsize=12, fontweight='bold')
    
    # Polygons based on ground truth for c3cd6c82-b5d52beb.jpg
    # direct drivable polygon
    poly_direct = np.array([
        [484.13, 580.21], [753.64, 555.25], [1020.66, 576.46], [1277.70, 715.0],
        [100.0, 715.0], [484.13, 580.21]
    ])
    patch_direct = patches.Polygon(poly_direct, closed=True, facecolor=(0, 0.9, 0.2, 0.35), edgecolor='#00E676', linewidth=2.5)
    ax1.add_patch(patch_direct)
    ax1.text(650, 640, "area/drivable\n(Làn xe ego đang đi)", color='white', fontsize=11, fontweight='bold',
             ha='center', bbox=dict(boxstyle="round,pad=0.3", facecolor='#1b5e20', alpha=0.85, edgecolor='none'))
    
    # alternative drivable polygon (adjacent highway lanes)
    poly_alt = np.array([
        [701.24, 345.0], [898.31, 372.11], [1085.63, 416.13], [1277.70, 455.43],
        [1277.70, 700.0], [1020.66, 576.46], [753.64, 555.25], [484.13, 580.21],
        [520.0, 460.0], [620.0, 380.0]
    ])
    patch_alt = patches.Polygon(poly_alt, closed=True, facecolor=(0, 0.6, 1.0, 0.35), edgecolor='#00B0FF', linewidth=2.5)
    ax1.add_patch(patch_alt)
    ax1.text(1050, 490, "area/alternative\n(Làn phụ / làn kế cận)", color='white', fontsize=11, fontweight='bold',
             ha='center', bbox=dict(boxstyle="round,pad=0.3", facecolor='#01579b', alpha=0.85, edgecolor='none'))
    ax1.axis('off')

    # Right: Polygon Rules & Common Mistakes
    ax2 = axes[1]
    ax2.set_facecolor('#ffffff')
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.set_title("Quy tắc hình học Polygon (Geometry Rules & Do/Don't)", fontsize=12, fontweight='bold')
    
    rules = [
        ("✅ BÁM SÁT BIÊN ĐƯỜNG QUAN SÁT ĐƯỢC:", "Vẽ theo mép vỉa hè (curb), rào chắn, hoặc vạch mép đường. Không đoán mò phần đường bị che khuất hoàn toàn."),
        ("✅ MẬT ĐỘ ĐIỂM (Point Density):", "Đoạn đường thẳng dùng ít điểm (2-3 điểm). Đoạn cua/cong tăng mật độ điểm để bám mượt mà đường cong."),
        ("❌ KHÔNG TỰ CẮT (Self-Intersection):", "Tuyệt đối không để cạnh polygon bắt chéo nhau tạo thành hình xoắn số 8 — lỗi này làm hỏng validation pipeline."),
        ("❌ KHÔNG TRÀN LÊN VỈA HÈ / CHƯỚNG NGẠI:", "Không vẽ polygon đè lên vỉa hè (sidewalk), dải phân cách cứng, hoặc bồn cây."),
        ("❌ KHÔNG OVERLAP VÔ NGHĨA:", "area/drivable và area/alternative phải tiếp giáp nhau tại ranh giới làn, KHÔNG đè chồng lên nhau.")
    ]
    
    y = 8.8
    for title, desc in rules:
        color = '#2E7D32' if title.startswith("✅") else '#C62828'
        ax2.text(0.5, y, title, fontsize=10.5, fontweight='bold', color=color)
        ax2.text(0.5, y - 0.7, desc, fontsize=9.5, color='#37474f', wrap=True)
        y -= 1.8
        
    ax2.axis('off')
    
    plt.tight_layout()
    for d in OUT_DIRS:
        fig.savefig(os.path.join(d, '02_polygon_drivable_illustration.png'), bbox_inches='tight')
    plt.close(fig)
    print("Created 02_polygon_drivable_illustration.png")

# -------------------------------------------------------------
# 3. Lane Marking Polyline Illustration (Dashed single polyline, Stopping rules, Classes)
# -------------------------------------------------------------
def create_lane_illustration():
    # Use BDD01 (highway with clear dashed lines and occluding SUV)
    img_bgr = cv2.imread(os.path.join(BASE, 'data/bdd100k/') + 'BDD01.jpg')
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6.5), dpi=150)
    fig.patch.set_facecolor('#f8f9fa')
    
    # Left: Overlay of lane polylines on BDD01
    ax1 = axes[0]
    ax1.imshow(img_rgb)
    ax1.set_title("Lane Marking Polyline: Vạch đứt = 1 đường qua tim; Dừng khi bị che", fontsize=12, fontweight='bold')
    
    # Ground truth polylines for bb890202
    # 1. Dashed line left of ego: [243, 548] -> [316, 498] -> [477, 355] -> [517, 325]
    pts_dash1 = np.array([[243, 548], [316, 498], [477, 355], [517, 325]])
    ax1.plot(pts_dash1[:, 0], pts_dash1[:, 1], color='#FFFF00', linewidth=3, marker='o', markersize=4)
    ax1.text(320, 520, "lane/single white (dashed)\n[1 polyline qua tim vạch đứt]", color='black', fontsize=9.5, fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.2", facecolor='#fff59d', alpha=0.9, edgecolor='none'))
    
    # 2. Stopping at SUV tail (Occlusion rule)
    pts_dash2 = np.array([[794, 480], [707, 403], [634, 339], [625, 331]])
    ax1.plot(pts_dash2[:, 0], pts_dash2[:, 1], color='#FFFF00', linewidth=3, marker='o', markersize=4)
    # Highlight stop point
    ax1.plot(625, 331, marker='X', color='red', markersize=10, markeredgewidth=2)
    ax1.text(635, 320, "DỪNG TẠI ĐUÔI XE!\n(Bị che - KHÔNG vẽ xuyên)", color='white', fontsize=9, fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.2", facecolor='#d32f2f', alpha=0.85, edgecolor='none'))
    
    # 3. Solid line right border: [1280, 470] -> [1000, 397] -> [775, 337] -> [700, 315] -> [650, 292]
    pts_solid = np.array([[1280, 470], [1000, 397], [775, 337], [700, 315], [650, 292]])
    ax1.plot(pts_solid[:, 0], pts_solid[:, 1], color='#00E5FF', linewidth=3, marker='o', markersize=4)
    ax1.text(950, 420, "lane/single white (solid)", color='white', fontsize=9.5, fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.2", facecolor='#00838f', alpha=0.85, edgecolor='none'))

    # 4. Yellow line far left: [125, 350] -> [200, 338] -> [318, 320]
    pts_yellow = np.array([[125, 350], [200, 338], [318, 320]])
    ax1.plot(pts_yellow[:, 0], pts_yellow[:, 1], color='#FF9100', linewidth=3, marker='o', markersize=4)
    ax1.text(140, 330, "lane/single yellow", color='white', fontsize=9.5, fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.2", facecolor='#e65100', alpha=0.85, edgecolor='none'))
    
    ax1.axis('off')

    # Right: Polyline rules and classes reference
    ax2 = axes[1]
    ax2.set_facecolor('#ffffff')
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.set_title("Quy tắc vẽ Polyline & Phân loại vạch kẻ đường", fontsize=12, fontweight='bold')
    
    rules = [
        ("1. VẠCH ĐỨT (Dashed Lane):", "Một polyline duy nhất bám theo tim các đoạn đứt. KHÔNG vẽ đứt quãng từng nét ngắn."),
        ("2. ĐIỂM DỪNG (Termination):", "Dừng ngay tại vị trí vạch bị xe/vật khác che, hoặc nơi vạch quá mờ không còn bằng chứng thị giác."),
        ("3. KHÔNG VẼ XUYÊN QUA XE:", "Tuyệt đối không nối polyline xuyên qua thân xe phía trước dù thấy mặt đường phía xa hơn."),
        ("4. KHÔNG DÙNG POLYGON:", "Không vẽ Polygon cho lane marking dù vạch sơn có bề rộng đáng kể trên ảnh."),
        ("5. PHÂN BIỆT CLASS:", "lane/single white (làn cùng chiều), lane/double yellow (cấm vượt ngược chiều), lane/crosswalk (vạch sang đường), lane/road curb (mép vỉa).")
    ]
    
    y = 8.8
    for title, desc in rules:
        ax2.text(0.5, y, title, fontsize=10.5, fontweight='bold', color='#1565C0')
        ax2.text(0.5, y - 0.7, desc, fontsize=9.5, color='#263238', wrap=True)
        y -= 1.8
        
    ax2.axis('off')

    plt.tight_layout()
    for d in OUT_DIRS:
        fig.savefig(os.path.join(d, '03_polyline_lane_illustration.png'), bbox_inches='tight')
    plt.close(fig)
    print("Created 03_polyline_lane_illustration.png")

# -------------------------------------------------------------
# 4. CVAT Decision Matrix & QA Reviewer Flowchart
# -------------------------------------------------------------
def create_decision_flowchart():
    fig, ax = plt.subplots(figsize=(15, 8), dpi=150)
    fig.patch.set_facecolor('#f8f9fa')
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    ax.text(7.5, 9.4, "QUY TRÌNH XỬ LÝ QUYẾT ĐỊNH & ESCALATION TRONG CVAT", fontsize=14, fontweight='bold', ha='center', color='#0d47a1')
    
    # 4 Decision boxes
    boxes = [
        ("LABEL", "#2e7d32", "#e8f5e9", 0.6, 5.0, 3.2, 3.6,
         "Đối tượng RÕ RÀNG\n- Đúng taxonomy\n- Đủ bằng chứng thị giác\n- Vẽ đúng shape bắt buộc\n- Gán occluded / truncated"),
        ("IGNORE", "#455a64", "#eceff1", 4.2, 5.0, 3.2, 3.6,
         "Ngoài phạm vi (SCOPE)\n- Bóng đổ (shadow)\n- Phản chiếu (reflection)\n- Hình in trên billboard\n- Vật thể ngoài taxonomy\n-> KHÔNG VẼ GÌ CẢ"),
        ("UNKNOWN / REVIEW", "#f57f17", "#fffde7", 7.8, 5.0, 3.2, 3.6,
         "Thuộc scope nhưng MỜ/NHỎ\n- Không rõ class hoặc boundary\n- Vẫn vẽ nếu định vị được\n- Tạo CVAT Issue:\n  • UNCERTAIN_CLASS\n  • UNCERTAIN_BOUNDARY"),
        ("ESCALATE", "#c62828", "#ffebee", 11.4, 5.0, 3.2, 3.6,
         "EDGE CASE chưa có tiền lệ\n- Rule chưa cover tình huống\n- Dừng suy đoán\n- Tạo CVAT Issue:\n  • UNCERTAIN_SCOPE\n- Gửi Mentor/Lead chốt rule")
    ]
    
    for title, border_col, bg_col, x, y, w, h, body in boxes:
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.2", edgecolor=border_col, facecolor=bg_col, linewidth=2.5)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h - 0.5, title, fontsize=12, fontweight='bold', ha='center', color=border_col)
        ax.text(x + 0.2, y + h - 1.2, body, fontsize=9.5, color='#212121', va='top')
        
    # Bottom Table: Reviewer Checklist
    rect_check = patches.FancyBboxPatch((0.6, 0.5), 14.0, 3.8, boxstyle="round,pad=0.2", edgecolor='#1565c0', facecolor='#e3f2fd', linewidth=2)
    ax.add_patch(rect_check)
    ax.text(7.6, 3.8, "CHECKLIST KIỂM TRA TRƯỚC KHI SUBMIT (REVIEWER QC CRITERIA)", fontsize=11.5, fontweight='bold', ha='center', color='#0d47a1')
    
    checklist_text = [
        "☑ 1. Taxonomy: Đúng class, đúng shape (BBox cho object, Polygon cho drivable, Polyline cho lane).",
        "☑ 2. Completeness: Không bỏ sót xe, người, biển báo, vạch đường rõ ràng trong phạm vi quan sát.",
        "☑ 3. Bounding Box Geometry: Ôm sát biên dạng vật thể, không thừa nền, không lấy bóng đổ, không vượt mép ảnh.",
        "☑ 4. Polygon Geometry: Bám sát mép đường, không tự cắt (no self-intersection), không overlap vô nghĩa.",
        "☑ 5. Polyline Geometry: Đi theo tim vạch đứt, dừng ngay khi bị che hoặc hết bằng chứng thị giác, không vẽ xuyên qua xe.",
        "☑ 6. Attributes: Gán chính xác occluded=true khi bị che, truncated=true khi chạm/cắt mép ảnh.",
        "☑ 7. No Guessing: Tất cả trường hợp không chắc chắn đều đã được gắn Issue (UNCERTAIN_*) để Reviewer xử lý."
    ]
    
    cy = 3.3
    for item in checklist_text:
        ax.text(1.0, cy, item, fontsize=9.5, color='#1a237e')
        cy -= 0.4
        
    plt.tight_layout()
    for d in OUT_DIRS:
        fig.savefig(os.path.join(d, '04_cvat_decision_flowchart.png'), bbox_inches='tight')
    plt.close(fig)
    print("Created 04_cvat_decision_flowchart.png")

if __name__ == '__main__':
    create_bbox_illustration()
    create_drivable_illustration()
    create_lane_illustration()
    create_decision_flowchart()
    print("All illustrations generated successfully!")
