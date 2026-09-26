# Team

- **Team:** team03
- **Nhóm peer test bài của mình:** team?
- **Nhóm mình test bài của:** team?
- **Problem family:** Lane geometry / semantics
- **Nguồn ảnh:** bdd100k

| Thành viên | GitHub | Vai trò chính | File phụ trách |
|---|---|---|---|
| Phan Quốc Tuấn - 2A202602298 | TuanCoderIT | Spec Owner (Lead) | `01_problem_statement.md`, `02_guideline.md` |
| Nguyễn Hải Long - 2A202602308 | LongFixBug | Co-Spec Owner & Revision | `02_guideline.md`, `08_revision_log.md` |
| Nguyễn Như Quỳnh - 2A202602336 | nnq2412 | CVAT Owner | `03_ontology_and_cvat_setup.md`, `03_cvat_labels.json`, `09_cvat_export_or_task_reference.txt` |
| Trần Minh Hiếu - 2A202602292| FN2187-TMH | Data & Sample Pack Owner | `sample_pack.csv`, `03_cvat_labels.json` |
| Nguyễn Vũ Dũng - 2A202602288| fragjkub | Gold Owner | `04_edge_cases/edge_case_cards.md`, `04_edge_cases/gold_decisions.csv` |
| Vũ Ngọc Huyền - 2A202602323| Lucy-techic | QA & Handoff Owner | `05_qa_plan.md`, `06_calibration_report.csv`, `07_blind_handoff/` |

**Phân công công việc nhóm:**
- **Spec Owner (Tuấn & Long):** Nghiên cứu downstream contract, soạn thảo và tinh chỉnh tài liệu `02_guideline.md` qua các phiên bản v1, v2, v3, cập nhật `08_revision_log.md`.
- **CVAT & Data Owner (Quỳnh & Hiếu):** Thiết lập ontology schema `03_cvat_labels.json`, phân loại chia ảnh vào `sample_pack.csv` (example, calibration, blind), tạo và cấu hình task trên CVAT.
- **Gold Owner (Dũng):** Nghiên cứu và xây dựng các ca biên `04_edge_cases/edge_case_cards.md`, chốt đáp án chuẩn cho tập blind test trong `04_edge_cases/gold_decisions.csv` và thực hiện freeze.
- **QA & Handoff Owner (Huyền):** Lập kế hoạch kiểm thử chất lượng `05_qa_plan.md`, tổng hợp đo lường calibration `06_calibration_report.csv`, phối hợp giao nhận blind pack và ghi nhận log với nhóm peer.
- **Calibration nội bộ:** Toàn bộ 6 thành viên đều tham gia gắn nhãn độc lập trên tập ảnh calibration để đo độ bất đồng.
