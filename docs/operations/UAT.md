# Factory ERP V1 — User Acceptance Testing (UAT) Guide & Checklist

This document provides a non-technical, business-oriented User Acceptance Testing (UAT) manual for plant managers, department heads, warehouse supervisors, and quality inspectors validating **Factory ERP V1**.

---

## 1. UAT Roles & Test Personas

| Persona | Role in System | Key Testing Responsibilities |
|---|---|---|
| **Sales Rep / Officer** | `factory_security.group_factory_sales_user` | Creating quotations, confirming SOs, checking stock allocations. |
| **Purchasing Officer** | `factory_security.group_factory_purchase_officer` | Generating RFQs, managing supplier MOQs, sending purchase orders. |
| **Warehouse Keeper** | `factory_security.group_factory_warehouse_user` | Inbound receiving, putting away stock, internal transfers, scrap. |
| **Quality Inspector** | `factory_security.group_factory_quality_inspector` | Inspecting receipts, in-process testing, dispositioning rework/scrap. |
| **Production Supervisor** | `factory_security.group_factory_production_supervisor`| Scheduling MOs, managing work orders, logging material consumption. |
| **Maintenance Engineer**| `factory_security.group_factory_maintenance_engineer`| Logging workcenter breakdowns, tracking MTBF/MTTR, repairs. |
| **Cost Accountant** | `factory_security.group_factory_cost_accountant` | Reviewing manufacturing cost absorption, variance, valuation. |
| **Plant / Factory Manager** | `factory_security.group_factory_plant_manager` | PO limit approvals, BOM engineering revisions, master sign-offs. |

---

## 2. Test Execution Checklist

### Section A: Sales & Demand Management
- [ ] **TC-SALES-01: MTS Order Confirmation & Reservation**
  - Navigate to **Sales > Orders > Create**. Select customer `Customer Alpha`, add finished good `FG-001` (Qty: 10).
  - Confirm quotation into Sales Order.
  - *Expected Result*: Delivery Order is generated. Stock reservation status shows *Reserved* if warehouse has stock on hand.
- [ ] **TC-SALES-02: MTO Demand Triggering Manufacturing**
  - Create SO for a configured Make-To-Order item.
  - Confirm SO.
  - *Expected Result*: A draft/confirmed Manufacturing Order (MO) is automatically spawned with source document linked to SO.
- [ ] **TC-SALES-03: Delivery Tolerance & Customer Specs**
  - Check customer record under **Sales > Customers > Factory Settings**. Configure under/over delivery tolerance (e.g., ±5%).
  - Deliver within vs outside tolerance.
  - *Expected Result*: Warning or block triggered if shipping quantity exceeds permitted variance.

---

### Section B: Procurement & Supplier Management
- [ ] **TC-PURCH-01: Supplier MOQ Enforcement**
  - Navigate to **Purchase > Orders > Create**. Select `Vendor MetalWorks Ltd`.
  - Add Raw Material `RAW-STEEL-01` with quantity lower than supplier MOQ (e.g. 5 units when MOQ is 100).
  - Try to confirm the RFQ.
  - *Expected Result*: System raises a validation warning/error that quantity must meet or exceed MOQ.
- [ ] **TC-PURCH-02: Tiered PO Approval Thresholds**
  - Log in as Purchasing Officer. Create PO with total value > Factory Manager approval limit (e.g., > 50,000 EGP).
  - Confirm the order.
  - *Expected Result*: PO transitions into `To Approve` status. Only Factory / Plant Manager can click **Approve Order**.
- [ ] **TC-PURCH-03: Industrial Procurement Categories**
  - Verify purchase order lines categorize items by `Raw Materials`, `Packaging`, `Consumables`, or `Tooling`.

---

### Section C: Warehouse, Locations & Lot Traceability
- [ ] **TC-WH-01: Industrial Warehouse Classification**
  - Navigate to **Inventory > Configuration > Locations**.
  - Verify the presence of all 10 core industrial location types:
    `Raw Materials (RM)`, `Work In Progress (WIP)`, `Finished Goods (FG)`, `Quarantine (QC)`, `Scrap`, `Rework`, `Transit`, `Spare Parts`, `Packaging`, `Customer Returns`.
- [ ] **TC-WH-02: Supplier Lot & Expiry Ingestion**
  - When validating incoming receipt from supplier, enter Supplier Lot Number and internal Lot ID.
  - *Expected Result*: Lot is created under `stock.lot` with full upstream traceability.
- [ ] **TC-WH-03: Negative Inventory Prevention**
  - Attempt to deliver or consume more stock than physically available in a location.
  - *Expected Result*: System prevents negative inventory (`stock_no_negative` rule blocks validation).

---

### Section D: Quality Control & Scrap/Rework
- [ ] **TC-QC-01: Incoming Goods Inspection Gate**
  - Receive shipment from PO. Item routed to `Quarantine` location.
  - Perform Quality Inspection. Click **Pass**.
  - *Expected Result*: Stock moves from Quarantine to `Raw Materials` main storage.
- [ ] **TC-QC-02: Quality Rejection & Rework Order**
  - Perform Quality Inspection on WIP or Finished Goods. Click **Reject**.
  - System generates a controlled `factory.rework.order`.
  - Supervisor assigns rework route. Material moves to `Rework` location.
  - Inspect reworked batch and pass. Stock returns to production or FG.
- [ ] **TC-QC-03: Scrap Classification & Reason Codes**
  - During manufacturing work order, declare scrap.
  - Select scrap reason code (`Machining Defect`, `Operator Error`, `Material Flaw`).
  - *Expected Result*: Material moves to `Scrap` location; scrap loss financial impact is computed and audited.

---

### Section E: Manufacturing & Work Centers
- [ ] **TC-MRP-01: Multi-Pillar Work Center Costing**
  - Navigate to **Manufacturing > Configuration > Work Centers**.
  - Inspect a work center. Verify breakdown: *Base Machine Rate*, *Direct Labor Rate*, and *Overhead Absorption Rate*.
- [ ] **TC-MRP-02: Manufacturing Execution & Work Orders**
  - Confirm a Manufacturing Order with BOM.
  - Work Order 1 (Cutting) -> Start timer -> Log duration -> Complete.
  - Work Order 2 (Assembly) -> Start timer -> Log duration -> Complete.
  - *Expected Result*: Actual hours recorded against planned hours; labor cost computed automatically.
- [ ] **TC-MRP-03: BOM Engineering Revision Control**
  - Modify a BOM. Increase revision index (e.g. Rev 1 -> Rev 2) and record engineering change note.
  - *Expected Result*: Past MOs maintain traceability to Rev 1; new MOs adopt Rev 2.

---

### Section F: Maintenance & Equipment Downtime
- [ ] **TC-MAINT-01: Equipment Breakdown & Work Center Downtime Sync**
  - Navigate to **Maintenance > Maintenance Requests > Create**.
  - Select Equipment `CNC Milling Machine 01`. Set category to `Corrective` and priority `High`.
  - Mark status as `In Progress`.
  - *Expected Result*: Linked Work Center status automatically switches to `Under Maintenance / Blocked`. New work order scheduling displays a warning.
- [ ] **TC-MAINT-02: Preventive Maintenance Completion**
  - Complete repair and click **Resolve**.
  - *Expected Result*: Work Center status automatically restores to `Available`. MTTR/MTBF metrics update.

---

### Section G: Cost Accounting & Egypt Localization
- [ ] **TC-ACC-01: Production Cost Absorption Breakdown**
  - Open a finished Manufacturing Order. Inspect the **Factory Cost Analysis** tab.
  - Verify complete split:
    - *Direct Materials Cost*
    - *Direct Labor Cost*
    - *Overhead Absorption Cost*
    - *Total & Unit Finished Good Cost*
- [ ] **TC-ACC-02: Variance Auditing**
  - Produce MO with material over-consumption (e.g., 12m of fabric used vs 10m planned).
  - *Expected Result*: System computes Material Usage Variance and Duration Variance in reports and accounting summary.
- [ ] **TC-ACC-03: Egyptian Tax & Currency Readiness**
  - Check Company Settings. Currency is `EGP`, Country `Egypt`.
  - Generate an invoice with standard 14% VAT.
  - *Expected Result*: Clean journal entries with localized tax account assignment.

---

### Section H: Industrial Reports & PDF Generation
- [ ] **TC-REP-01: Production Order Traveler / Card**
  - Print Manufacturing Order Traveler from MO form view.
  - *Expected Result*: Professional PDF containing barcode, routing operations, BOM items, and inspection sign-off blocks.
- [ ] **TC-REP-02: 16 Core QWeb Reports Audit**
  - Verify printing for: MO Card, BOM Sheet, Warehouse Picking List, Consumption Report, Scrap Report, Rework Order Sheet, QC Inspection Certificate, Upstream/Downstream Lot Traceability, and Costing Variance Sheet.

---

## 3. UAT Sign-Off Template

**Testing Project**: Factory ERP V1 Deployment  
**Test Cycle**: UAT Cycle 1  
**Factory / Plant Name**: ___________________________  

| Functional Area | Test Status (PASS / FAIL / BLOCK) | Responsible Lead | Signature & Date |
|---|---|---|---|
| Sales & Customer Delivery | [ ] PASS  [ ] FAIL | ________________ | ________________ |
| Procurement & Vendor MOQs | [ ] PASS  [ ] FAIL | ________________ | ________________ |
| Inventory & Traceability | [ ] PASS  [ ] FAIL | ________________ | ________________ |
| Quality, Scrap & Rework | [ ] PASS  [ ] FAIL | ________________ | ________________ |
| Manufacturing & BOM Control | [ ] PASS  [ ] FAIL | ________________ | ________________ |
| Maintenance & Downtime | [ ] PASS  [ ] FAIL | ________________ | ________________ |
| Cost Accounting & Taxes | [ ] PASS  [ ] FAIL | ________________ | ________________ |
| Security & Role Separation | [ ] PASS  [ ] FAIL | ________________ | ________________ |

**Final Plant Acceptance Status**:
- [ ] **ACCEPTED FOR PRODUCTION**
- [ ] **ACCEPTED WITH RESERVATIONS** (list punch-list items below)
- [ ] **REJECTED**

*Factory General Manager Name*: _______________________________  
*Signature*: _______________________________________________  
*Date*: ____________________
