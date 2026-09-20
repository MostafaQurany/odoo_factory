# Clothing Factory System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Configure Odoo 18 for 100% automated startup with 392 custom addons, inject realistic clothing manufacturing mock data, enable a responsive timeline-driven UI, and provide a comprehensive zero-jargon beginner guide.

**Architecture:** A dedicated companion module `clothing_factory_demo` under `addons/manufacture/` defines the clothing factory domain (fabrics, trims, work centers, BOMs, DDMRP buffers, sample orders) via declarative XML records. `docker-compose.yml` automatically triggers `-i odoo_factory_all,clothing_factory_demo -d odoo` on startup. The UI is enhanced via `web_responsive` and `web_timeline`, accompanied by a complete handbook `FACTORY_GUIDE.md`.

**Tech Stack:** Odoo 18.0, PostgreSQL 16, Docker Compose, Python, XML, OCA web client tools (`web_responsive`, `web_timeline`).

**Spec:** [2026-09-20-clothing-factory-system-design.md](file:///E:/C/production%20projects/amgad/odoo_factory/docs/superpowers/specs/2026-09-20-clothing-factory-system-design.md)

## Global Constraints
- Target Odoo database name: `odoo`
- Only install the 392 verified modules in `odoo_factory_all` (exclude the 48 unresolvable modules)
- All new demo records must use standard Odoo XML `<record>` syntax with clear IDs
- Documentation must be zero-jargon, suitable for someone with zero ERP/manufacturing background

---

### Task 1: Create `clothing_factory_demo` Module

**Files:**
- Create: `addons/manufacture/clothing_factory_demo/__init__.py`
- Create: `addons/manufacture/clothing_factory_demo/__manifest__.py`
- Create: `addons/manufacture/clothing_factory_demo/data/product_data.xml`
- Create: `addons/manufacture/clothing_factory_demo/data/mrp_routing_data.xml`
- Create: `addons/manufacture/clothing_factory_demo/data/mrp_bom_data.xml`
- Create: `addons/manufacture/clothing_factory_demo/data/ddmrp_buffer_data.xml`
- Create: `addons/manufacture/clothing_factory_demo/data/mrp_production_data.xml`

**Interfaces:**
- Consumes: `mrp`, `stock`, `ddmrp`, `web_responsive`, `web_timeline`
- Produces: Installed demo records for 7 raw materials, 2 finished garments, 4 work centers, 2 BOMs, 3 DDMRP buffers, and 3 sample manufacturing orders.

- [ ] **Step 1: Create module structure and `__manifest__.py`**

Create `addons/manufacture/clothing_factory_demo/__init__.py` (empty) and `addons/manufacture/clothing_factory_demo/__manifest__.py`:
```python
{
    "name": "Clothing Factory Demo Data",
    "version": "18.0.1.0.0",
    "category": "Manufacturing",
    "summary": "Realistic Apparel & Garment Manufacturing Demo Data",
    "author": "Odoo Factory",
    "license": "AGPL-3",
    "depends": [
        "mrp",
        "stock",
        "ddmrp",
        "web_responsive",
        "web_timeline",
    ],
    "data": [
        "data/product_data.xml",
        "data/mrp_routing_data.xml",
        "data/mrp_bom_data.xml",
        "data/ddmrp_buffer_data.xml",
        "data/mrp_production_data.xml",
    ],
    "installable": True,
    "application": False,
}
```

- [ ] **Step 2: Create `product_data.xml`**

Define raw materials and finished goods:
- Raw Materials: `RAW-COT-01` (Organic Cotton Fabric), `RAW-DEN-01` (Indigo Denim Fabric), `RAW-THR-01` (Polyester Thread), `RAW-BTN-01` (Brass Buttons), `RAW-ZIP-01` (YKK Zippers), `RAW-LBL-01` (Neck Labels), `PKG-BAG-01` (Poly Bags).
- Finished Goods: `FG-TSHIRT-01` (Classic Organic Cotton T-Shirt), `FG-DENIM-01` (Classic Denim Jacket).

- [ ] **Step 3: Create `mrp_routing_data.xml`**

Define work centers:
- `WC-CUT` (Fabric Cutting Station)
- `WC-SEW` (Assembly & Sewing Line)
- `WC-QPR` (Quality Inspection & Steam Pressing)
- `WC-PKG` (Folding & Barcode Packaging Station)

- [ ] **Step 4: Create `mrp_bom_data.xml`**

Define Bills of Materials with operations:
- BOM for `FG-TSHIRT-01`: 1.5m Cotton, 0.05 spool Thread, 1 Neck Label, 1 Poly Bag. Operations at Cutting, Sewing, Quality/Pressing, Packaging.
- BOM for `FG-DENIM-01`: 2.8m Denim, 0.20 spool Thread, 6 Buttons, 1 Zipper, 1 Neck Label, 1 Poly Bag. Operations at Cutting, Sewing, Quality/Pressing, Packaging.

- [ ] **Step 5: Create `ddmrp_buffer_data.xml`**

Define `stock.buffer` records for `RAW-COT-01`, `RAW-DEN-01`, and `FG-TSHIRT-01` with Red/Yellow/Green stock thresholds.

- [ ] **Step 6: Create `mrp_production_data.xml`**

Define sample manufacturing orders:
- `MO/00001`: 50 T-Shirts (In Progress)
- `MO/00002`: 25 Denim Jackets (Confirmed / Ready)
- `MO/00003`: 100 T-Shirts (Done)

---

### Task 2: Update Docker Compose & Execute 100% Automated Installation

**Files:**
- Modify: `docker-compose.yml:14-16`

**Interfaces:**
- Consumes: `odoo_factory_all`, `clothing_factory_demo`
- Produces: Running Docker container with all 392 modules and demo records installed in PostgreSQL database `odoo`.

- [ ] **Step 1: Update `docker-compose.yml`**

Modify `command` in `docker-compose.yml` to:
```yaml
    command: odoo --load=base,web,queue_job -d odoo -i odoo_factory_all,clothing_factory_demo --addons-path=/mnt/extra-addons/manufacture,/mnt/extra-addons/ddmrp,/mnt/extra-addons/stock-logistics-warehouse,/mnt/extra-addons/stock-logistics-orderpoint,/mnt/extra-addons/server-backend,/mnt/extra-addons/server-tools,/mnt/extra-addons/stock-logistics-workflow,/mnt/extra-addons/web,/mnt/extra-addons/stock-logistics-availability,/mnt/extra-addons/queue,/usr/lib/python3/dist-packages/odoo/addons
```

- [ ] **Step 2: Execute installation via `docker exec`**

Run:
```powershell
docker exec odoo_factory_system odoo -d odoo -i odoo_factory_all,clothing_factory_demo --stop-after-init
```
Verify the command exits with code 0 and logs show `Modules loaded: ...`.

- [ ] **Step 3: Verify database records in PostgreSQL**

Run query to verify:
- `odoo_factory_all` and `clothing_factory_demo` are `installed`.
- Products `RAW-COT-01` and `FG-TSHIRT-01` exist.
- Work centers and BOM records exist.

---

### Task 3: Configure and Validate Modern UI/UX

**Files:**
- Test via browser / container verification

**Interfaces:**
- Consumes: `web_responsive`, `web_timeline`, `web_widget_x2many_2d_matrix`
- Produces: Responsive App Drawer, visual Gantt timeline on Manufacturing Orders.

- [ ] **Step 1: Verify `web_responsive` is active**

Check that the App Drawer assets are loaded in web client bundles and web response returns 200 at `http://localhost:8069`.

- [ ] **Step 2: Verify `web_timeline` on Manufacturing Orders**

Inspect `mrp.production` views to confirm timeline view is registered and accessible.

---

### Task 4: Author Zero-Jargon Beginner Factory Guide

**Files:**
- Create: `FACTORY_GUIDE.md`

**Interfaces:**
- Consumes: Clothing factory demo data, Odoo module architecture
- Produces: Complete educational handbook for non-developers.

- [ ] **Step 1: Write Section 1 - How a Factory Works (Plain English)**

Explain the 5 stages: Procurement -> Warehousing -> Manufacturing -> Quality -> Shipping.

- [ ] **Step 2: Write Section 2 - Odoo Jargon Buster & Glossary**

Translate terms (BOM, Work Center, Routing, MO, WO, DDMRP Buffer, Decoupling Point) into everyday analogies (recipes, kitchen stations, tickets, traffic lights).

- [ ] **Step 3: Write Section 3 - Visual Flowcharts (Mermaid)**

Include:
- Factory workflow diagram (Cotton Roll -> T-Shirt).
- DDMRP traffic light buffer diagram (Red/Yellow/Green zones).

- [ ] **Step 4: Write Section 4 - Step-by-Step System Walkthrough**

Provide clear instructions with exact UI clicks:
- Logging in and opening App Drawer.
- Checking Raw Materials in Inventory.
- Creating and completing a Manufacturing Order for T-Shirts.
- Viewing the visual schedule on the Timeline.
