# Factory Industrial Accounting & Costing — Functional Guide

**Technical Module**: `custom/factory_accounting`  
**Odoo Core Depends**: `account`, `stock_account`  
**Capability**: `accounting`  
**Profile**: `core`, `operations`, `advanced`, `full`  

---

## 1. Overview
The Factory Industrial Accounting module integrates shop-floor production events into financial costing and inventory valuation without reinventing standard double-entry bookkeeping. It decomposes manufacturing costs into distinct components and provides clean localization configuration for Egypt (EGP currency).

---

## 2. Manufacturing Cost Breakdown
On every Manufacturing Order (`mrp.production`), industrial costs are computed and tracked:
- **Actual Raw Material Cost** (`cost_raw_materials`): Sum of all consumed component quantities valued at their standard cost.
- **Direct Labor Cost** (`cost_workcenter_labor`): Work order recorded operator duration multiplied by work center hourly labor rate.
- **Industrial Overhead Cost** (`cost_workcenter_overhead`): Work order duration multiplied by work center hourly overhead rate.
- **Total Manufacturing Cost** (`cost_manufacturing_total`): Total cost absorbed by the production batch.
- **Unit Cost Manufactured** (`unit_cost_manufactured`): Exact cost per finished unit produced.

---

## 3. Egyptian Localization Profile
- Configurable toggle on the company (`res.company`).
- Idempotent action sets country to Egypt (`EG`) and activates/sets company currency to Egyptian Pound (`EGP`).
- Compatible with Odoo 18 standard `l10n_eg` localization modules when installed.
