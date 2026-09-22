# Factory Procurement & Purchasing — Functional Guide

**Technical Module**: `custom/factory_purchase`  
**Odoo Core Depends**: `purchase`, `purchase_stock`  
**Capability**: `purchasing`  
**Profile**: `core`, `operations`, `advanced`, `full`  

---

## 1. Overview
The Factory Procurement module handles vendor sourcing, lead time tracking, strict MOQ policies, and approval hierarchies for manufacturing inputs (Raw Materials, Hardware/Components, Packaging, and Maintenance/Spares).

---

## 2. Procurement Categories
Every purchase order is categorized into an industrial procurement type:
- **Raw Materials**: Basic industrial materials (sheet metal, fabric, chemicals, timber) destined for processing.
- **Components & Hardware**: Fasteners, electronic sub-assemblies, and standard parts.
- **Packaging Materials**: Cartons, crates, wrapping, palletizing accessories.
- **Maintenance & Spares**: Replacement machine parts, lubricants, consumables.
- **General Supplies**: Administrative and factory consumables.

---

## 3. High-Value PO Approval Hierarchy
To prevent unauthorized expenditure, purchase orders are checked against the company's configurable threshold (`factory_po_approval_limit`):
1. **Standard Confirmation**: POs with total amount below the threshold confirm immediately into purchase orders.
2. **Approval Gate**: POs exceeding the threshold cannot be confirmed by standard purchase officers; they are automatically placed into `to_approve` status.
3. **Manager Disposition**: Only users with `Factory Manager` rights can execute `action_factory_approve()` or `action_factory_reject()`.
