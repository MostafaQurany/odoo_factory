# Factory Manufacturing & Work Centers — Functional Guide

**Technical Module**: `custom/factory_mrp`  
**Odoo Core Depends**: `mrp`  
**Capability**: `manufacturing`  
**Profile**: `core`, `operations`, `advanced`, `full`  

---

## 1. Overview
The Factory Manufacturing module extends standard Odoo MRP with true industrial work center costing, multi-shift assignment, planned vs. actual material and labor variance auditing, and engineering revision control on Bills of Materials.

---

## 2. Work Centers & Cost Aggregation
Industrial work centers (`mrp.workcenter`) aggregate three distinct cost pillars to establish a comprehensive hourly machine rate (`total_hourly_rate`):
1. **Base Machine Rate** (`costs_hour`): Capital depreciation and baseline equipment allocation.
2. **Direct Labor Rate** (`hourly_labor_cost`): Operator and technician wages allocated per hour.
3. **Overhead Rate** (`hourly_overhead_cost`): Power, tooling wear, factory space, and environmental maintenance.

Work centers are assigned to factory sections (Cutting, Machining, Welding, Assembly, Finishing, Packaging, QA Station) and maintain an operating status (`operational`, `maintenance`, `restricted`).

---

## 3. Production Auditing & Variances
On every Manufacturing Order (`mrp.production`):
- **Shift & Supervision**: Orders track the working shift (Morning, Evening, Night) and floor supervisor responsible.
- **Material Variance %**: Automatic auditing computes percentage deviation between planned component quantities and actual shop floor consumption.
- **Labor / Duration Variance %**: Auditing compares standard routing expected duration against logged work order operator time.
- **Rework Flag**: Highlights orders undergoing non-standard correction cycles.

---

## 4. Engineering BOM Revisions
Bills of Materials (`mrp.bom`) support formal engineering revision codes (e.g. `REV-01`), sign-off signatures from engineering leads, and technical process documentation.
