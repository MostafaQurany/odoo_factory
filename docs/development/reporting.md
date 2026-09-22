# Factory Industrial Reports — Technical & Functional Reference

**Technical Module**: `custom/factory_reports`  
**Odoo Core Depends**: `base`, `mrp`, `stock`, `purchase`  
**Capability**: `reporting`  
**Profile**: `core`, `operations`, `advanced`, `full`  

---

## 1. Overview
The Factory Reports module provides 16 production-grade QWeb PDF documents formatted for rugged industrial shop floor use, quality audits, customer documentation, and management costing reviews.

---

## 2. Complete Industrial Reports Directory

| Report Title | Report XML ID | Target Model | Key Content |
|---|---|---|---|
| **Manufacturing Order Card / Traveler** | `factory_reports.action_report_mrp_order_card` | `mrp.production` | Routing operations, component pick list, barcodes, shift info |
| **BOM Material Requirement Sheet** | `factory_reports.action_report_mrp_bom_sheet` | `mrp.bom` | Engineering revision code, component hierarchy, notes |
| **Production Pick List** | `factory_reports.action_report_production_pick_list` | `mrp.production` | Store warehouse locations, quantities to stage |
| **Material Consumption Report** | `factory_reports.action_report_material_consumption` | `mrp.production` | Planned vs actual component consumption & variance % |
| **Finished Production Slip** | `factory_reports.action_report_finished_production` | `mrp.production` | Certified output quantity, lot numbers, handover signatures |
| **Scrap Report** | `factory_reports.action_report_stock_scrap` | `stock.scrap` | Defect reason code, work center attribution, financial loss |
| **Controlled Rework Traveler** | `factory_reports.action_report_rework_order` | `factory.rework.order` | Root cause analysis, rework instructions, re-inspection sign-off |
| **Quality Inspection Certificate** | `factory_reports.action_report_qc_inspection` | `qc.inspection` | 4-gate classification, test specifications, pass/hold disposition |
| **Lot/Serial Traceability Report** | `factory_reports.action_report_lot_traceability` | `stock.lot` | Origin supplier, vendor lot ref, COA number, downstream pickings |
| **Stock Availability Statement** | `factory_reports.action_report_stock_availability` | `stock.warehouse` | Free vs reserved inventory across all 10 factory locations |
| **Inventory Valuation Report** | `factory_reports.action_report_inventory_valuation` | `stock.location` | Location asset valuation audit |
| **Purchase Receipt Incoming Slip** | `factory_reports.action_report_purchase_incoming` | `purchase.order` | Vendor order items, delivery note, receiving location |
| **Supplier Performance Report** | `factory_reports.action_report_supplier_performance` | `res.partner` | Delivery timeliness, defect rate, tier classification |
| **Production Cost Report** | `factory_reports.action_report_production_costing` | `mrp.production` | Materials + Direct Labor + Overhead unit cost breakdown |
| **Planned vs Actual Variance** | `factory_reports.action_report_manufacturing_variance` | `mrp.production` | Duration variance % and scrap variance % |
| **Factory Delivery Slip** | `factory_reports.action_report_factory_delivery_slip` | `stock.picking` | Final customer dispatch notice, packing checklist |
