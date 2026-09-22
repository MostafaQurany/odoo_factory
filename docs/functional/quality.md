# Factory Quality & Controlled Rework — Functional Guide

**Technical Module**: `custom/factory_quality`  
**Odoo Core Depends**: `stock`, `mrp`  
**OCA Depends**: `quality_control_oca`, `quality_control_mrp_oca`, `scrap_reason_code`, `mrp_workcenter_scrap_reason`  
**Capability**: `manufacturing_quality`, `scrap_management`  
**Profile**: `operations`, `advanced`, `full`  

---

## 1. Overview
The Factory Quality & Controlled Rework module establishes four systematic quality control gates throughout the industrial lifecycle. Defective items do not merely sit in text notes; they trigger a formal controlled Rework loop or immediate scrap cost attribution.

---

## 2. Four Industrial Quality Gates
Every quality inspection record (`qc.inspection`) is categorized into a mandatory gate:

1. **Gate 1 — Incoming Receiving Inspection**:
   - Executed upon vendor PO receipt.
   - Evaluates raw materials and components against specifications and Certificates of Analysis (COA).
   - Outcomes: `PASS` (released to `raw_materials` location) or `HOLD` (quarantined in `quality_hold`).
2. **Gate 2 — In-Process Manufacturing Check**:
   - Executed at designated work centers during work order progression.
   - Verifies intermediate tolerances, weld integrity, and machining dimensions.
3. **Gate 3 — Final Finished Goods Acceptance**:
   - Executed prior to finished product entry into `finished_goods` warehouse location.
   - Validates final functionality, finish, and packaging.
4. **Gate 4 — Customer / RMA Return Inspection**:
   - Executed upon receipt of customer returns.
   - Identifies root cause and routes item to Restock, Rework, or Scrap.

---

## 3. Controlled Rework Workflow
When an inspection yields defects that can be corrected:
```text
Quality Inspection [REWORK]
       ↓
Factory Rework Order [Draft]
       ↓
Assigned to Work Center & Operator [In Progress]
       ↓
Correction Executed [Pending Re-inspection]
       ↓
Quality Re-inspection
   ├── PASS → Released to Production / Finished Goods
   └── FAIL → Rejected & Scrapped
```

---

## 4. Scrap Reason & Cost Loss Attribution
Unrecoverable scrap recorded via `stock.scrap` is automatically linked to the origin inspection and estimates financial loss based on the product standard cost multiplied by scrap quantity.
