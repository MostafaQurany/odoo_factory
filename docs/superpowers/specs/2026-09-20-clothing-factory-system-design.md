# Clothing Factory System Design: Automated Docker Setup, Demo Data, Enhanced UI, and Beginner Documentation

**Date**: 2026-09-20  
**Status**: Draft (Pending User Review)  
**Author**: Antigravity  

---

## 1. Context & Objectives

The `odoo_factory` project is an enterprise-grade Odoo 18.0 deployment containing 10 major addon suites (DDMRP, Advanced Manufacturing, Queue Jobs, Warehouse Logistics, Orderpoints, Workflows, Web UI, etc.) comprising 440 modules.

The user requires:
1. **100% Automated System Startup**: Make Odoo start automatically with all verified custom modules installed, eliminating manual one-by-one installation in the Apps UI.
2. **Realistic Clothing Factory Demo Data**: Pre-load realistic Garment & Apparel manufacturing data (raw materials, work centers, routing, BOMs, DDMRP buffers, sample manufacturing orders) so the system is immediately illustrative.
3. **Enhanced, User-Friendly UI**: Modernize the interface using `web_responsive` (app drawer, mobile/tablet layout), `web_timeline` (visual Gantt timeline for production), and 2D matrix views for size/color entry.
4. **Comprehensive Beginner Documentation**: A plain-English, zero-jargon handbook explaining how a factory works, how MRP and DDMRP operate, and how to navigate the system without any programming or ERP background.

---

## 2. Architecture & Container Orchestration

### 2.1 Services & Volumes
- **Odoo Web Service (`odoo_factory_system`)**:
  - Image: `odoo:18.0`
  - Ports: `8069:8069`
  - Volumes:
    - `odoo-web-data:/var/lib/odoo`
    - `./addons:/mnt/extra-addons`
  - Command:
    ```bash
    odoo --load=base,web,queue_job -d odoo -i odoo_factory_all,clothing_factory_demo --addons-path=/mnt/extra-addons/manufacture,/mnt/extra-addons/ddmrp,/mnt/extra-addons/stock-logistics-warehouse,/mnt/extra-addons/stock-logistics-orderpoint,/mnt/extra-addons/server-backend,/mnt/extra-addons/server-tools,/mnt/extra-addons/stock-logistics-workflow,/mnt/extra-addons/web,/mnt/extra-addons/stock-logistics-availability,/mnt/extra-addons/queue,/usr/lib/python3/dist-packages/odoo/addons
    ```
- **PostgreSQL Service (`odoo_factory_db`)**:
  - Image: `postgres:16`
  - Environment: `POSTGRES_DB=postgres`, `POSTGRES_USER=odoo`, `POSTGRES_PASSWORD=odoo`
  - Volume: `odoo-db-data:/var/lib/postgresql/data`

### 2.2 Addon Modules Management
- **`odoo_factory_all` (Server-Tools Meta Module)**:
  - Depends on all 392 verified, conflict-free modules across all 10 mounted directories.
  - Excludes 48 unresolvable modules that require external uninstalled C-libraries or missing external upstream repos.
- **`clothing_factory_demo` (Dedicated Demo Module)**:
  - Depends on `mrp`, `stock`, `ddmrp`, `web_responsive`, `web_timeline`.
  - Ingests XML/CSV demo records on module installation.

---

## 3. Clothing Factory Domain & Mock Data Design

### 3.1 Raw Materials (Stock Items)
| Internal Reference | Name | Category | Unit of Measure | Initial Qty | Cost |
|--------------------|------|----------|-----------------|-------------|------|
| `RAW-COT-01` | 100% Organic Cotton Fabric Roll | Raw Materials / Fabrics | Meters (m) | 500 m | $4.50 / m |
| `RAW-DEN-01` | Indigo Raw Denim Fabric Roll | Raw Materials / Fabrics | Meters (m) | 350 m | $7.20 / m |
| `RAW-THR-01` | Heavy Polyester Sewing Thread | Raw Materials / Notions | Units (Spools) | 120 Spools | $2.10 / spool |
| `RAW-BTN-01` | Antique Brass Shank Buttons | Raw Materials / Trims | Units | 1,500 pcs | $0.25 / pc |
| `RAW-ZIP-01` | Metal YKK Zipper 20cm | Raw Materials / Trims | Units | 400 pcs | $1.15 / pc |
| `RAW-LBL-01` | Woven Neck Labels & Care Tags | Raw Materials / Trims | Units | 2,000 pcs | $0.10 / pc |
| `PKG-BAG-01` | Biodegradable Poly Bag | Packaging Materials | Units | 1,000 pcs | $0.08 / pc |

### 3.2 Work Centers (Shop Floor Stations)
1. **`WC-CUT` (Fabric Cutting Station)**:
   - Capacity: 100 meters/hour.
   - Equipment: Laser cutter & industrial spreading table.
2. **`WC-SEW` (Assembly & Sewing Line)**:
   - Capacity: 30 garments/hour.
   - Equipment: 6x High-speed lockstitch sewing machines, overlock machines.
3. **`WC-QPR` (Quality Inspection & Steam Pressing)**:
   - Capacity: 40 garments/hour.
   - Equipment: Vacuum ironing tables, high-pressure steam boilers, inspection mannequins.
4. **`WC-PKG` (Folding & Barcode Packaging Station)**:
   - Capacity: 60 garments/hour.
   - Equipment: Automatic garment folding board, barcode label printer.

### 3.3 Finished Products & Bills of Materials (BOM)
1. **Product: Classic Organic Cotton T-Shirt (`FG-TSHIRT-01`)**:
   - Product Type: Storable Product.
   - BOM Components:
     - `RAW-COT-01`: 1.50 m
     - `RAW-THR-01`: 0.05 spool
     - `RAW-LBL-01`: 1.00 pc
     - `PKG-BAG-01`: 1.00 pc
   - Operations / Routing:
     1. Cut front, back, and collar ribs at `WC-CUT` (10 min).
     2. Stitch body panels and hem sleeves at `WC-SEW` (20 min).
     3. Inspect seams and steam iron at `WC-QPR` (5 min).
     4. Fold, attach care tag, and pack into poly bag at `WC-PKG` (5 min).

2. **Product: Classic Denim Jacket (`FG-DENIM-01`)**:
   - Product Type: Storable Product.
   - BOM Components:
     - `RAW-DEN-01`: 2.80 m
     - `RAW-THR-01`: 0.20 spool
     - `RAW-BTN-01`: 6.00 pcs
     - `RAW-ZIP-01`: 1.00 pc
     - `RAW-LBL-01`: 1.00 pc
     - `PKG-BAG-01`: 1.00 pc
   - Operations / Routing:
     1. Cut denim panels at `WC-CUT` (25 min).
     2. Stitch panels, attach collar, and press brass buttons at `WC-SEW` (50 min).
     3. Distress inspection and steam press at `WC-QPR` (15 min).
     4. Tag and bag at `WC-PKG` (8 min).

### 3.4 DDMRP Buffers
- Decoupled stock buffers for:
  - `RAW-COT-01`: Min 100m (Red Zone), Reorder point 250m (Yellow Zone), Max 600m (Green Zone).
  - `RAW-DEN-01`: Min 80m (Red Zone), Reorder point 200m (Yellow Zone), Max 450m (Green Zone).
  - `FG-TSHIRT-01`: Finished goods buffer to decouple customer demand from factory lead time.

### 3.5 Sample Transactions & Pre-Loaded Orders
- **Order 1 (`MO/00001`)**: 50x Classic T-Shirts (State: In Progress, operations partially recorded).
- **Order 2 (`MO/00002`)**: 25x Denim Jackets (State: Confirmed / Ready to start).
- **Order 3 (`MO/00003`)**: 100x Classic T-Shirts (State: Done / Completed with serial tracking).

---

## 4. UI/UX Modernization & Simplification

1. **`web_responsive` Integration**:
   - Full-screen App Drawer replacing traditional nested top navigation.
   - Quick module search bar built into the app drawer.
   - Adaptive mobile/tablet layout for shop floor touchscreens.
2. **`web_timeline` Integration**:
   - Gantt-style interactive timeline view added to Manufacturing Orders and Work Orders (`mrp.production` and `mrp.workorder`).
   - Color-coded by status (Ready, In Progress, Blocked, Done).
3. **`web_widget_x2many_2d_matrix`**:
   - Size/Color variant entry matrix on sales and production lines.
4. **Ergonomic Defaults**:
   - Sticky headers on inventory moves and production lists.
   - Clear visual status badges.

---

## 5. Beginner-Friendly Factory Guide & Reference Manual

A comprehensive, zero-jargon markdown guide will be generated at `FACTORY_GUIDE.md` covering:
1. **The Anatomy of a Modern Garment Factory**:
   - Procurement -> Warehouse -> Cutting -> Sewing -> Finishing/QC -> Packaging -> Shipping.
2. **ERP & Odoo Jargon Buster**:
   - Simple analogies for BOM, Work Centers, Routing, MO, WO, Pickings, and Lots.
3. **Demystifying MRP and DDMRP**:
   - Why traditional MRP causes shortages or overstocking (the Bullwhip Effect).
   - How DDMRP solves this with Red/Yellow/Green traffic-light buffers.
4. **End-to-End Walkthrough**:
   - Step 1: Checking fabric stock in the Warehouse.
   - Step 2: Creating a Manufacturing Order for 50 T-Shirts.
   - Step 3: Executing Work Orders at Cutting and Sewing stations.
   - Step 4: Completing the order and viewing the finished goods in inventory.
   - Step 5: Visualizing the production schedule on the timeline.

---

## 6. Verification & Validation Plan

1. **Container Startup Check**:
   - Verify `docker-compose up` launches `odoo_factory_system` and `odoo_factory_db` without errors.
   - Check Odoo logs for successful module installation of `odoo_factory_all` and `clothing_factory_demo`.
2. **Database Verification**:
   - Query `ir_module_module` to verify `odoo_factory_all` and `clothing_factory_demo` are in state `installed`.
   - Verify products (`RAW-COT-01`, `FG-TSHIRT-01`, etc.) exist in `product_template`.
   - Verify BOMs exist in `mrp_bom` and Work Centers exist in `mrp_workcenter`.
   - Verify Manufacturing Orders exist in `mrp_production`.
3. **UI Verification**:
   - Verify web interface is accessible at `http://localhost:8069`.
   - Verify App Drawer renders properly via `web_responsive`.
   - Verify timeline view is available on Manufacturing Orders.
4. **Documentation Verification**:
   - Verify `FACTORY_GUIDE.md` exists, is well-structured, contains Mermaid diagrams, and links directly to relevant modules.
