# Factory Inventory & Warehousing — Functional Guide

**Technical Module**: `custom/factory_inventory`  
**Odoo Core Depends**: `stock`  
**OCA Depends**: `stock_no_negative`, `stock_available`, `stock_free_quantity`  
**Capability**: `inventory`  
**Profile**: `core`, `operations`, `advanced`, `full`  

---

## 1. Overview
The Factory Inventory module configures the standard industrial warehouse topology required for manufacturing operations. It enforces zero negative inventory, strict lot/serial number tracking, and end-to-end traceability from raw materials intake through shop floor consumption to finished product shipment.

---

## 2. Configurable Industrial Warehouse Topology
Rather than hardcoding global static paths, the module provides a repeatable, idempotent setup method on every warehouse (`stock.warehouse`).

Clicking **"Initialize Factory Locations"** on the warehouse creates or links the 10 industrial locations under the primary warehouse stock location:

| Location Type | Technical Code | Usage | Industrial Purpose |
|---|---|---|---|
| **Input / Receiving** | `input` | Internal | Raw materials unloading and initial staging |
| **Quality Hold** | `quality_hold` | Internal | Quarantine staging prior to QC pass/fail |
| **Raw Materials** | `raw_materials` | Internal | Certified raw materials storage ready for issue |
| **Components** | `components` | Internal | Sub-assemblies, hardware, and packaging stock |
| **WIP / Production** | `wip` | Internal | Work-in-process staging at work centers |
| **Finished Goods** | `finished_goods` | Internal | Quality-approved manufactured items for shipping |
| **Packaging** | `packaging` | Internal | Boxes, pallets, protective wrap, labels |
| **Returns** | `returns` | Internal | Customer or vendor returns pending disposition |
| **Scrap** | `scrap` | Inventory | Defective, damaged, or un-reworkable materials |
| **Spare Parts** | `spare_parts` | Internal | Maintenance equipment, toolings, wear parts |

---

## 3. Strict Inventory Controls
1. **No-Negative-Stock Policy**: Leveraging OCA `stock_no_negative`, all factory-controlled internal locations disallow negative stock balances. If an operator attempts to issue or transfer more stock than physically recorded, Odoo rejects the move with a clear validation error.
2. **Lot / Serial Tracking**: Raw materials and finished goods are flagged for mandatory lot tracking. Lots store the originating vendor, vendor batch reference, production date, and inspection certificate number.
3. **Traceability**: An upstream/downstream traceability chain links the customer delivery slip back through the manufacturing order to the exact vendor lots consumed.
