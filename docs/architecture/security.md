# Factory Industrial Role-Based Access Control (RBAC) & Security

**Technical Module**: `custom/factory_security`  
**Odoo Core Depends**: `base`, `stock`, `mrp`, `purchase`, `sale_management`, `account`  
**Capability**: `security_baseline`  
**Profile**: `core`, `operations`, `advanced`, `full`  

---

## 1. Overview
The Factory Security module enforces strict segregation of duties across twelve manufacturing personas. It establishes precise access boundaries between shop-floor execution, storekeeping, quality enforcement, procurement, and management oversight.

---

## 2. The 12 Industrial Personas & Role Hierarchy
```text
                       [Administrator]
                              │
                      [Factory Manager]
            ┌─────────────────┼─────────────────┐
            │                 │                 │
   [Production Supv]   [Purchase Mgr]     [Quality Insp]
            │                 │                 │
       [Operator]     [Purchase Officer]  [Process Eng]
            │
     [Store Keeper]   [Sales Officer]     [Accountant]
            │
            └───────── [Executive Read-Only]
```

| Persona Role | Technical XML ID | Key Permissions |
|---|---|---|
| **Operator** | `factory_base.group_factory_user` | Shop floor work order clocking, consumption logging |
| **Store Keeper** | `factory_security.group_factory_storekeeper` | Inventory receipts, internal transfers, lot issuing |
| **Quality Inspector** | `factory_base.group_factory_quality` | Inspection execution, Gate disposition (Pass, Hold, Rework, Scrap) |
| **Process Engineer** | `factory_base.group_factory_engineer` | Work center parameters, BOM engineering revisions |
| **Production Supervisor** | `factory_security.group_factory_production_supervisor` | MO creation, work order dispatch, shift scheduling |
| **Purchase Officer** | `factory_security.group_factory_purchase_officer` | RFQ creation, standard purchase orders below threshold |
| **Purchase Manager** | `factory_security.group_factory_purchase_manager` | High-value PO approval/rejection |
| **Sales User** | `factory_security.group_factory_sales_officer` | Quotations, sales orders, demand strategy selection |
| **Accountant** | `factory_security.group_factory_accountant` | Vendor bill validation, customer invoices, valuation review |
| **Factory Manager** | `factory_base.group_factory_manager` | Plant-wide approval override, setup configuration |
| **Executive Read-Only** | `factory_security.group_factory_executive_readonly` | Cross-department read-only visibility for auditing |
| **Administrator** | `base.group_system` | Technical IT administration, users, backups |
