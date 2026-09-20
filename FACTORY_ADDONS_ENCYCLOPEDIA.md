# 📚 The Master Encyclopedia of Odoo Factory Addons & Customization Guide
## A Comprehensive Reference Manual for Factory Owners, Operations Directors & Customizers
**Total Modules Documented**: 389 Modules across 10 Industrial Suites  
**Target Platform**: Odoo 18.0 + OCA Enterprise Addons  
**Version**: 2.0 (Comprehensive Edition)  

---

## 📑 Manual Overview
1. [The Golden Rules of Modifying & Removing Addons](#1-the-golden-rules-of-modifying--removing-addons)
2. [Effort, Cost & Complexity Estimation Framework](#2-effort-cost--complexity-estimation-framework)
3. [How to Safely Remove or Deactivate an Addon in 4 Steps](#3-how-to-safely-remove-or-deactivate-an-addon-in-4-steps)
4. [How to Customize an Addon Without Touching Original Code (The Odoo Way)](#4-how-to-customize-an-addon-without-touching-original-code-the-odoo-way)
5. [Curated Factory Presets (Lean, High-Tech, Small Workshop)](#5-curated-factory-presets)
6. [Complete Module-by-Module Reference Catalog (Categorized by Suite)](#6-complete-module-by-module-reference-catalog)
   - [Suite A: Demand Driven MRP (`ddmrp`)](#suite-a-demand-driven-mrp-ddmrp)
   - [Suite B: Advanced Manufacturing (`manufacture`)](#suite-b-advanced-manufacturing-manufacture)
   - [Suite C: Warehouse & Storage Logistics (`stock-logistics-warehouse`)](#suite-c-warehouse--storage-logistics-stock-logistics-warehouse)
   - [Suite D: Procurement & Orderpoints (`stock-logistics-orderpoint`)](#suite-d-procurement--orderpoints-stock-logistics-orderpoint)
   - [Suite E: Stock Movements & Workflows (`stock-logistics-workflow`)](#suite-e-stock-movements--workflows-stock-logistics-workflow)
   - [Suite F: Stock Availability & Priority Allocation (`stock-logistics-availability`)](#suite-f-stock-availability--priority-allocation-stock-logistics-availability)
   - [Suite G: Asynchronous Background Queue (`queue`)](#suite-g-asynchronous-background-queue-queue)
   - [Suite H: Modern Responsive UI & Visual Tools (`web`)](#suite-h-modern-responsive-ui--visual-tools-web)
   - [Suite I: Server Backend Utilities (`server-backend`)](#suite-i-server-backend-utilities-server-backend)
   - [Suite J: Server Tools & Management (`server-tools`)](#suite-j-server-tools--management-server-tools)

---

## 1. The Golden Rules of Modifying & Removing Addons

### Rule 1: The Dependency Cascade Rule
In Odoo, addons never live in isolation. If Module **B** depends on Module **A**:
- You **cannot** remove Module **A** while Module **B** is installed.
- If you attempt to delete Module **A**, Odoo will either block the uninstallation or force-uninstall Module **B** as well!
- *Before removing any module, always check its "Dependents" list in this encyclopedia.*

### Rule 2: Never Edit the Original Addon Code Directly
If you open a file inside `addons/manufacture/...` and change the code:
1. When you pull updates from GitHub, your changes will be overwritten and lost.
2. If you make a syntax error, the entire server may fail to start.
- **The Correct Odoo Way**: Always create a custom companion module (e.g., `my_factory_custom`) that **inherits** (`_inherit`) the model or view. You write only 5 lines of code, and the original module remains pristine and upgradeable!

### Rule 3: Database Column Persistence
When a module adds a new column to a database table (e.g., `fabric_weight` on products):
- Uninstalling the module hides the field from the web UI, but PostgreSQL keeps the column in the database table so your data is not destroyed immediately.

---

## 2. Effort, Cost & Complexity Estimation Framework

When you want to customize an addon or build new functionality, how much will it cost, and how many hours will it take? We use this standardized industrial framework:

| Complexity Tier | Typical Scope | Estimated Hours | Market Cost (Freelance / Agency) | Technical Skills Needed |
|:---|:---|:---|:---|:---|
| **Tier 1: Minor View / UI Tweak** | Hiding a button, renaming a field, rearranging a form layout, adding a help tooltip. | **1 – 4 Hours** | **$50 – $250** | Basic XML knowledge (no Python needed). |
| **Tier 2: Field & Simple Logic** | Adding a new field (e.g. Fabric GSM), simple automated calculation (e.g. Total Area = Length × Width). | **4 – 12 Hours** | **$250 – $800** | Basic Python + XML model inheritance. |
| **Tier 3: Moderate Workflow** | Custom approval step (e.g. Manager must approve scrap > $500), new PDF report, automated email trigger. | **1 – 3 Days** | **$800 – $2,500** | Intermediate Python, Odoo ORM, QWeb reporting. |
| **Tier 4: Complex Industrial Engine** | Custom algorithm for nesting cut patterns, integration with automated CNC/cutting hardware, custom scheduling rule. | **1 – 3 Weeks** | **$2,500 – $10,000+** | Senior Odoo Architect, algorithms, external APIs. |

---

## 3. How to Safely Remove or Deactivate an Addon in 4 Steps

If you decide you do not need a specific module (e.g., `stock_picking_batch_extended`):

### Step 1: Check Who Depends on It
Look up the module in this catalog under **"Who Depends on This (Dependents)"**:
- If it says **None**, it is **100% safe to remove**.
- If it lists other modules, you must also remove those dependent modules.

### Step 2: Remove It from `odoo_factory_all`
Open `addons/server-tools/odoo_factory_all/__manifest__.py`:
- Find the module name in the `'depends': [...]` list.
- Delete that line or comment it out.

### Step 3: Uninstall in the Odoo Database
Run this one-line command to uninstall the module cleanly from the PostgreSQL database:
```powershell
docker exec odoo_factory_system odoo -d odoo -u odoo_factory_all --stop-after-init
```

### Step 4: Restart the Web Container
```powershell
docker-compose restart web
```

---

## 4. How to Customize an Addon Without Touching Original Code (The Odoo Way)

Here is a 5-minute template showing how professionals customize Odoo modules safely:

### Example: Adding a "Fabric GSM Weight" Field to Products
Instead of editing `addons/manufacture`, you create a small custom module `addons/my_factory_custom`:

1. **`addons/my_factory_custom/__manifest__.py`**:
```python
{
    "name": "My Factory Customizations",
    "version": "18.0.1.0.0",
    "depends": ["product", "mrp"],
    "data": ["views/product_views.xml"],
    "installable": True,
}
```

2. **`addons/my_factory_custom/models/product.py`**:
```python
from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    fabric_gsm = fields.Float(string="Fabric GSM (Grams/m²)", help="Weight of the fabric per square meter")
```

3. **`addons/my_factory_custom/views/product_views.xml`**:
```xml
<odoo>
    <record id="view_product_form_inherit_gsm" model="ir.ui.view">
        <field name="name">product.template.gsm.form</field>
        <field name="model">product.template</field>
        <field name="inherit_id" ref="product.product_template_only_form_view"/>
        <field name="arch" type="xml">
            <field name="default_code" position="after">
                <field name="fabric_gsm"/>
            </field>
        </field>
    </record>
</odoo>
```
*Result: Your custom field appears on the product form. When you update Odoo or pull new addons from GitHub, your field and its data are completely safe and untouched!*

---

## 5. Curated Factory Presets

Depending on the size and complexity of your factory, you can choose one of these recommended profiles:

### Profile 1: The Lean Garment & Workshop Factory (Lightweight)
- **Goal**: Fast, simple, minimum complexity.
- **Includes**: Core MRP (`mrp`), Stock (`stock`), `web_responsive` (App drawer), `web_timeline` (Visual schedule), `clothing_factory_demo`.
- **Excludes**: Deep DDMRP buffers, complex batch routing.
- **Memory Footprint**: Low (~500MB RAM).

### Profile 2: The High-Tech Discrete Manufacturing Plant (Full Enterprise)
- **Goal**: Full DDMRP replenishment, automated orderpoints, multi-tier warehouse routing, background job processing.
- **Includes**: All 388 modules active.
- **Memory Footprint**: Medium (~1.5GB - 2GB RAM).

---

## 6. Complete Module-by-Module Reference Catalog


### Suite A: Demand Driven MRP (`ddmrp`)

**Total Modules in this Suite**: 16

#### `ddmrp` — DDMRP
- **Summary**: Demand Driven Material Requirements Planning
- **Removal Safety**: 🔴 Core Dependency: 11 Modules Depend on It
- **Removal Impact**: Critical foundation module. Removing it will disable 11 other modules.
- **Dependencies (Requires)**: `purchase_stock, stock_demand_estimate, web_widget_bokeh_chart, mrp_multi_level, base_cron_exclusion, stock_warehouse_calendar, stock_location_is_sublocation, stock_move_quantity_product_uom`
- **Dependents (Required By)**: `ddmrp_chatter, ddmrp_coverage_days, ddmrp_cron_actions_as_job, ddmrp_exclude_moves_adu_calc, ddmrp_packaging, ddmrp_purchase_hide_onhand_status, ddmrp_report_part_flow_index, ddmrp_warning, stock_buffer_capacity_limit, stock_buffer_route, stock_buffer_sales_analysis`
- **Codebase Size**: 6473 Python lines, 3239 XML lines
- **Customization Complexity**: **Enterprise (Tier 4)** | **Effort**: 1 – 3 Weeks | **Estimated Cost**: $3,500 – $10,000+

---

#### `ddmrp_chatter` — DDMRP Chatter
- **Summary**: Adds chatter and activities to stock buffers.
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (ddmrp_product_replace)
- **Removal Impact**: If you remove this, you must also remove: ddmrp_product_replace.
- **Dependencies (Requires)**: `ddmrp`
- **Dependents (Required By)**: `ddmrp_product_replace`
- **Codebase Size**: 42 Python lines, 27 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `ddmrp_coverage_days` — DDMRP Coverage Days
- **Summary**: Implements Coverage Days.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `ddmrp`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 113 Python lines, 26 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `ddmrp_cron_actions_as_job` — DDMRP Buffer Calculation as job
- **Summary**: Run DDMRP Buffer Calculation as jobs
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (ddmrp_warning_as_job)
- **Removal Impact**: If you remove this, you must also remove: ddmrp_warning_as_job.
- **Dependencies (Requires)**: `ddmrp, queue_job`
- **Dependents (Required By)**: `ddmrp_warning_as_job`
- **Codebase Size**: 145 Python lines, 18 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `ddmrp_exclude_moves_adu_calc` — DDMRP Exclude Moves ADU Calc
- **Summary**: Define additional rules to exclude certain moves from ADU calculation
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (ddmrp_exclude_moves_adu_calc_sales)
- **Removal Impact**: If you remove this, you must also remove: ddmrp_exclude_moves_adu_calc_sales.
- **Dependencies (Requires)**: `ddmrp`
- **Dependents (Required By)**: `ddmrp_exclude_moves_adu_calc_sales`
- **Codebase Size**: 329 Python lines, 61 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `ddmrp_exclude_moves_adu_calc_sales` — DDMRP Exclude Moves ADU Calc Sales
- **Summary**: DDMRP Exclude Moves ADU Calc integration with Sales app.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `sale, ddmrp_exclude_moves_adu_calc`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 134 Python lines, 20 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `ddmrp_packaging` — DDMRP Packaging
- **Summary**: DDMRP integration with packaging
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (ddmrp_packaging_product_replace)
- **Removal Impact**: If you remove this, you must also remove: ddmrp_packaging_product_replace.
- **Dependencies (Requires)**: `ddmrp`
- **Dependents (Required By)**: `ddmrp_packaging_product_replace`
- **Codebase Size**: 218 Python lines, 34 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `ddmrp_packaging_product_replace` — DDMRP Packaging Product Replace
- **Summary**: Glue module for DDMRP packaging and product replace
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `ddmrp_product_replace, ddmrp_packaging`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 63 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `ddmrp_product_replace` — DDMRP Product Replace
- **Summary**: Provides a assisting tool for product replacement.
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (ddmrp_packaging_product_replace)
- **Removal Impact**: If you remove this, you must also remove: ddmrp_packaging_product_replace.
- **Dependencies (Requires)**: `ddmrp_chatter`
- **Dependents (Required By)**: `ddmrp_packaging_product_replace`
- **Codebase Size**: 646 Python lines, 209 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `ddmrp_purchase_hide_onhand_status` — DDMRP Purchase Hide On-Hand Status
- **Summary**: Replace purchase onhand status with smart button.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `ddmrp`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 53 Python lines, 38 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `ddmrp_report_part_flow_index` — DDMRP Report Part Flow Index
- **Summary**: Provides the DDMRP Parts Flow Index Report
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `ddmrp`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 258 Python lines, 178 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `ddmrp_warning` — DDMRP Warning
- **Summary**: Adds configuration warnings on stock buffers.
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (ddmrp_warning_as_job)
- **Removal Impact**: If you remove this, you must also remove: ddmrp_warning_as_job.
- **Dependencies (Requires)**: `ddmrp`
- **Dependents (Required By)**: `ddmrp_warning_as_job`
- **Codebase Size**: 286 Python lines, 291 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `ddmrp_warning_as_job` — DDMRP Warning as job
- **Summary**: Run DDMRP Warning as jobs
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `ddmrp_warning, ddmrp_cron_actions_as_job`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 87 Python lines, 10 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_buffer_capacity_limit` — Stock Buffer Capacity Limit
- **Summary**: Ensures that the limits of storage are never surpassed
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `ddmrp`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 188 Python lines, 16 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_buffer_route` — Stock Buffer Route
- **Summary**: Allows to force a route to be used when procuring from Stock Buffers
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `ddmrp`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 337 Python lines, 54 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_buffer_sales_analysis` — Stock Buffer Sales Analysis
- **Summary**: Allows to access the Sales Analysis from Stock Buffers
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `ddmrp, sale, sales_team`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 45 Python lines, 36 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---


### Suite B: Advanced Manufacturing (`manufacture`)

**Total Modules in this Suite**: 56

#### `account_move_line_mrp_info` — Account Move Line Mrp Info
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `account_move_line_stock_info, mrp`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 419 Python lines, 93 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `clothing_factory_demo` — Clothing Factory Demo Data
- **Summary**: Realistic Apparel & Garment Manufacturing Demo Data (Fabrics, BOMs, Work Centers, DDMRP Buffers)
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mrp, stock, ddmrp, web_responsive, web_timeline`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 26 Python lines, 391 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `mrp_attachment_mgmt` — Mrp Attachment Mgmt
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mrp`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 346 Python lines, 212 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `mrp_bom_assign_auto` — MRP BOM Assign Auto
- **Summary**: Auto select th first BoM that has all components available
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mrp`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 211 Python lines, 16 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `mrp_bom_attribute_match` — BOM Attribute Match
- **Summary**: Dynamic BOM component based on product attribute
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mrp`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 1075 Python lines, 32 XML lines
- **Customization Complexity**: **High (Tier 3)** | **Effort**: 2 – 5 Days | **Estimated Cost**: $1,000 – $3,500

---

#### `mrp_bom_component_menu` — MRP BOM Component Menu
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mrp`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 16 Python lines, 68 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `mrp_bom_hierarchy` — MRP BoM Hierarchy
- **Summary**: Make it easy to navigate through BoM hierarchy.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mrp`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 278 Python lines, 86 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `mrp_bom_image` — MRP BoM Image
- **Summary**: Add product Images to BoM
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mrp`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 35 Python lines, 56 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `mrp_bom_line_formula_quantity` — MRP BoM Line formula for quantity
- **Summary**: Compute the quantity of a Production Line using a formula in the BoM Line.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mrp`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 213 Python lines, 37 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `mrp_bom_line_uom_rounding` — MRP BoM Line UoM Rounding
- **Summary**: Enforce Unit of Measure rounding on BoM component quantities
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mrp`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 103 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `mrp_bom_location` — MRP BOM Location
- **Summary**: Adds location field to Bill of Materials and its components.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mrp`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 195 Python lines, 113 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `mrp_bom_note` — Notes in Bill of Materials
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mrp`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 38 Python lines, 28 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `mrp_bom_select_product_variant` — MRP BoM Select Product Variant
- **Summary**: Favors Product variant selection for BOM creation.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mrp`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 63 Python lines, 79 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `mrp_bom_tracking` — MRP BoM Tracking
- **Summary**: Logs any change to a BoM in the chatter
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mrp`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 258 Python lines, 57 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `mrp_bom_version` — MRP - BoM version
- **Summary**: BoM versioning
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mrp`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 355 Python lines, 238 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `mrp_bom_warn_message_oca` — MRP BOM Warn Message OCA
- **Summary**: 
        Add a configurable warning when a bill of materials
        is selected on a MRP manufacturing order.
    
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mrp`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 163 Python lines, 89 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `mrp_bom_widget_section_and_note_one2many` — MRP Widget Section and Note in BoM
- **Summary**: Add section and note in Bills of Materials
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mrp, account`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 89 Python lines, 124 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `mrp_byproduct_auto_create_lot` — MRP Byproduct Auto Create Lot
- **Summary**: Auto create lots for byproducts on manufacturing orders
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mrp, stock, stock_picking_auto_create_lot`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 308 Python lines, 0 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `mrp_lot_number_propagation` — MRP Serial Number Propagation
- **Summary**: Propagate a serial number from a component to a finished product
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mrp`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 1199 Python lines, 127 XML lines
- **Customization Complexity**: **High (Tier 3)** | **Effort**: 2 – 5 Days | **Estimated Cost**: $1,000 – $3,500

---

#### `mrp_mass_production_order` — MRP Mass Production Order
- **Summary**: Create multiple manufacturing orders in one step
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mrp_tag`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 445 Python lines, 86 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `mrp_multi_level` — MRP Multi Level
- **Summary**: Adds an MRP Scheduler
- **Removal Safety**: 🔴 Core Dependency: 3 Modules Depend on It
- **Removal Impact**: Critical foundation module. Removing it will disable 3 other modules.
- **Dependencies (Requires)**: `mrp, purchase_stock, mrp_warehouse_calendar`
- **Dependents (Required By)**: `ddmrp, mrp_multi_level_consume_safety_stock, mrp_multi_level_estimate`
- **Codebase Size**: 4053 Python lines, 1487 XML lines
- **Customization Complexity**: **Enterprise (Tier 4)** | **Effort**: 1 – 3 Weeks | **Estimated Cost**: $3,500 – $10,000+

---

#### `mrp_multi_level_consume_safety_stock` — MRP Multi Level Consume Safety Stock
- **Summary**: MRP scheduler: use safety stock during stress periods
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mrp_multi_level`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 174 Python lines, 24 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `mrp_multi_level_estimate` — MRP Multi Level Estimate
- **Summary**: Allows to consider demand estimates using MRP multi level.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mrp_multi_level, stock_demand_estimate`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 691 Python lines, 27 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `mrp_package_propagation` — MRP Package Propagation
- **Summary**: Propagate a package from a component to a finished product
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mrp`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 522 Python lines, 50 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `mrp_packaging_default` — MRP Default Packaging
- **Summary**: Include packaging info in MRP by default
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mrp, stock_move_packaging_qty`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 503 Python lines, 72 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `mrp_production_allow_recursive` — MRP Production Allow Recursive
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mrp`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 115 Python lines, 34 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `mrp_production_auto_validate` — Manufacturing Order Auto-Validate
- **Summary**: Manufacturing Order Auto-Validation when components are picked
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mrp`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 573 Python lines, 39 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `mrp_production_back_to_draft` — MRP Production Back to Draft
- **Summary**: Allows to return to draft a confirmed or cancelled MO.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mrp`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 210 Python lines, 23 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `mrp_production_check_bom_alignment` — MRP Production Check BoM Alignment
- **Summary**: Verify that a Manufacturing Order's components and workorder are consistent with its Bill of Materials.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mrp`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 564 Python lines, 74 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `mrp_production_date_planned_finished` — MRP Production Date Planned Finished
- **Summary**: Allows to plan production from the desired finish date
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mrp`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 155 Python lines, 42 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `mrp_production_location_picking_type` — MRP Production Location Picking Type
- **Summary**: Add production location field to picking types for MRP operations.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mrp`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 323 Python lines, 16 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `mrp_production_note` — Notes in production orders
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mrp`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 32 Python lines, 15 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `mrp_production_picking_type_from_route` — MRP Production Picking Type From Route
- **Summary**: Updates the operation type creating MO based on the product
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mrp`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 124 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `mrp_production_putaway_strategy` — MRP Production Putaway Strategy
- **Summary**: Applies putaway strategies to manufacturing orders for finished products.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mrp`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 136 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `mrp_propagate_lot_info` — MRP Propagate Lot Info
- **Summary**: Propagate lot data from the origin consuming materials
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mrp`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 670 Python lines, 197 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `mrp_repair_order` — MRP Repair Order
- **Summary**: Create repair order from manufacturing order
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mrp, repair`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 110 Python lines, 62 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `mrp_restrict_lot` — MRP Restrict Lot
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock_restrict_lot, mrp`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 304 Python lines, 0 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `mrp_sale_info` — MRP Sale Info
- **Summary**: Adds sale information to Manufacturing models
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `sale_mrp, sale_stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 353 Python lines, 106 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `mrp_stock_move_actual_date` — MRP Stock Move Actual Date
- **Summary**: Extend actual date handling to manufacturing and unbuild orders
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mrp, stock_move_actual_date`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 195 Python lines, 94 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `mrp_stock_move_line_qty_picked` — MRP Stock Move Line Qty Picked
- **Summary**: Adapt functionality of stock_move_line_qty_picked into MRP
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mrp, stock_move_line_qty_picked`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 16 Python lines, 21 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `mrp_subcontracting_inhibit` — Inhibit subcontracting flow on demand
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mrp_subcontracting, purchase`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 242 Python lines, 43 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `mrp_subcontracting_purchase_link` — Link Purchase Order Line to Subcontract Productions
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `purchase, mrp_subcontracting`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 201 Python lines, 41 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `mrp_subcontracting_skip_no_negative` — MRP Subcontracting Skip No Negative
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mrp_subcontracting, stock_no_negative`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 287 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `mrp_tag` — MRP Tags
- **Summary**: Allows to add multiple tags to Manufacturing Orders
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (mrp_mass_production_order)
- **Removal Impact**: If you remove this, you must also remove: mrp_mass_production_order.
- **Dependencies (Requires)**: `mrp`
- **Dependents (Required By)**: `mrp_mass_production_order`
- **Codebase Size**: 92 Python lines, 115 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `mrp_unbuild_move_link` — Stock moves of manufacturing orders added to unbuild orders
- **Summary**: Link the stock moves of manufacturing orders to the
    respective unbuild orders
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mrp_account`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 101 Python lines, 13 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `mrp_unbuild_valuation_layer_link` — Valuation layers for unbuild orders
- **Summary**: Unbuild orders display the connected valuation layers
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mrp_account`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 103 Python lines, 20 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `mrp_warehouse_calendar` — MRP Warehouse Calendar
- **Summary**: Considers the warehouse calendars in manufacturing
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (mrp_multi_level)
- **Removal Impact**: If you remove this, you must also remove: mrp_multi_level.
- **Dependencies (Requires)**: `mrp, stock_warehouse_calendar`
- **Dependents (Required By)**: `mrp_multi_level`
- **Codebase Size**: 235 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `mrp_workcenter_scrap_reason` — Workcenter Scrap Reason Code
- **Summary**: Filter allowed reason codes with workcenter assigned.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mrp, scrap_reason_code`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 287 Python lines, 28 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `mrp_workorder_blocking_time` — MRP Work Order Blocking Time
- **Summary**: Allow to block time on work orders
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mrp`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 341 Python lines, 134 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `mrp_workorder_sequence` — MRP Work Order Sequence
- **Summary**: adds sequence to production work orders.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mrp`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 332 Python lines, 16 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `product_mrp_info` — Product MRP Info
- **Summary**: Adds smart button in product form view linking to manufacturing order list.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mrp`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 177 Python lines, 46 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `quality_control_mrp_oca` — MRP extension for quality control (OCA)
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `quality_control_oca, quality_control_stock_oca, mrp`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 264 Python lines, 124 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `quality_control_oca` — Quality Control OCA
- **Summary**: Generic infrastructure for quality tests.
- **Removal Safety**: 🟡 Caution: 2 Dependent Modules (quality_control_mrp_oca, quality_control_stock_oca)
- **Removal Impact**: If you remove this, you must also remove: quality_control_mrp_oca, quality_control_stock_oca.
- **Dependencies (Requires)**: `product`
- **Dependents (Required By)**: `quality_control_mrp_oca, quality_control_stock_oca`
- **Codebase Size**: 1103 Python lines, 1010 XML lines
- **Customization Complexity**: **High (Tier 3)** | **Effort**: 2 – 5 Days | **Estimated Cost**: $1,000 – $3,500

---

#### `quality_control_stock_oca` — Quality control - Stock (OCA)
- **Summary**: No summary provided.
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (quality_control_mrp_oca)
- **Removal Impact**: If you remove this, you must also remove: quality_control_mrp_oca.
- **Dependencies (Requires)**: `quality_control_oca, stock`
- **Dependents (Required By)**: `quality_control_mrp_oca`
- **Codebase Size**: 933 Python lines, 314 XML lines
- **Customization Complexity**: **High (Tier 3)** | **Effort**: 2 – 5 Days | **Estimated Cost**: $1,000 – $3,500

---

#### `sale_mrp_bom_menu` — Sale MRP - Bills of Materials menu
- **Summary**: Add a Sales > Products > Bills of Materials menu
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `sale, mrp`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 15 Python lines, 13 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_whole_kit_constraint` — Stock whole kit constraint
- **Summary**: Avoid to deliver a kit partially
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mrp`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 250 Python lines, 29 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---


### Suite C: Warehouse & Storage Logistics (`stock-logistics-warehouse`)

**Total Modules in this Suite**: 72

#### `account_move_line_stock_info` — Account Move Line Stock Info
- **Summary**: No summary provided.
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (account_move_line_mrp_info)
- **Removal Impact**: If you remove this, you must also remove: account_move_line_mrp_info.
- **Dependencies (Requires)**: `stock_account`
- **Dependents (Required By)**: `account_move_line_mrp_info`
- **Codebase Size**: 236 Python lines, 87 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `procurement_auto_create_group` — Procurement Auto Create Group
- **Summary**: Allows to configure the system to propose automatically new procurement groups during the procurement run.
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (procurement_auto_create_group_carrier)
- **Removal Impact**: If you remove this, you must also remove: procurement_auto_create_group_carrier.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `procurement_auto_create_group_carrier`
- **Codebase Size**: 329 Python lines, 16 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `product_route_profile` — Product Route Profile
- **Summary**: Add Route profile concept on product
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (product_route_profile_internal_resupply)
- **Removal Impact**: If you remove this, you must also remove: product_route_profile_internal_resupply.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `product_route_profile_internal_resupply`
- **Codebase Size**: 418 Python lines, 82 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `product_route_profile_internal_resupply` — Product Route Profile - Internal Resupply
- **Summary**: Add dedicated Internal Routes on products.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `product_route_profile`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 142 Python lines, 22 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_archive_constraint` — Stock archive constraint
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 369 Python lines, 0 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_change_qty_reason` — Stock Change Quantity Reason
- **Summary**: 
        Stock Quantity Change Reason 
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 197 Python lines, 126 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_cycle_count` — Stock Cycle Count
- **Summary**: Adds the capability to schedule cycle counts in a warehouse through different rules defined by the user.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock_account, stock_inventory_discrepancy, stock_inventory`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 1816 Python lines, 678 XML lines
- **Customization Complexity**: **High (Tier 3)** | **Effort**: 2 – 5 Days | **Estimated Cost**: $1,000 – $3,500

---

#### `stock_demand_estimate` — Stock Demand Estimate
- **Summary**: Allows to create demand estimates.
- **Removal Safety**: 🟡 Caution: 2 Dependent Modules (ddmrp, mrp_multi_level_estimate)
- **Removal Impact**: If you remove this, you must also remove: ddmrp, mrp_multi_level_estimate.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `ddmrp, mrp_multi_level_estimate`
- **Codebase Size**: 402 Python lines, 170 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_inventory` — Stock Inventory Adjustment
- **Summary**: Allows to do an easier follow up of the Inventory Adjustments
- **Removal Safety**: 🔴 Core Dependency: 5 Modules Depend on It
- **Removal Impact**: Critical foundation module. Removing it will disable 5 other modules.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `stock_cycle_count, stock_inventory_location_state, stock_inventory_lockdown, stock_inventory_preparation_filter, stock_inventory_verification_request`
- **Codebase Size**: 1221 Python lines, 275 XML lines
- **Customization Complexity**: **High (Tier 3)** | **Effort**: 2 – 5 Days | **Estimated Cost**: $1,000 – $3,500

---

#### `stock_inventory_count_to_zero` — Stock Inventory Count To Zero
- **Summary**: Request an inventory count filling the quantities to zero as default
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 119 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_inventory_discrepancy` — Stock Inventory Discrepancy
- **Summary**: Adds the capability to show the discrepancy of every line in an inventory and to block the inventory validation when the discrepancy is over a user defined threshold.
- **Removal Safety**: 🟡 Caution: 2 Dependent Modules (stock_cycle_count, stock_inventory_verification_request)
- **Removal Impact**: If you remove this, you must also remove: stock_cycle_count, stock_inventory_verification_request.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `stock_cycle_count, stock_inventory_verification_request`
- **Codebase Size**: 466 Python lines, 198 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_inventory_hide_apply_all` — Stock Inventory Hide Apply All
- **Summary**: Hide the 'Apply All' button on the inventory adjustment list
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 19 Python lines, 24 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_inventory_location_state` — Stock Inventory Location State
- **Summary**: Verify that all locations are counted.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock_inventory`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 302 Python lines, 111 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_inventory_lockdown` — Inventory Lock Down
- **Summary**: Lock down stock locations during inventories.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock, stock_inventory`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 316 Python lines, 0 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_inventory_preparation_filter` — Extended Inventory Preparation Filters
- **Summary**: More filters for inventory adjustments
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock, stock_inventory, base_view_inheritance_extension`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 214 Python lines, 26 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_inventory_verification_request` — Stock Inventory Verification Request
- **Summary**: Adds the capability to request a Slot Verification when a inventory is Pending to Approve
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock_inventory, stock_inventory_discrepancy, mail`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 1152 Python lines, 321 XML lines
- **Customization Complexity**: **High (Tier 3)** | **Effort**: 2 – 5 Days | **Estimated Cost**: $1,000 – $3,500

---

#### `stock_location_bin_name` — Stock Location Bin Name
- **Summary**: Compute bin stock location name automatically
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock_location_zone, stock_location_position`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 234 Python lines, 13 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_location_children` — Stock location children
- **Summary**: Add relation between stock location and all its children
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 174 Python lines, 22 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_location_empty` — Stock Location Empty
- **Summary**: Adds a filter for empty stock location
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 112 Python lines, 87 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_location_fill_state` — Stock Location Fill State
- **Summary**: This module allows to identify the fill state of stock locations
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (stock_location_fill_state_qty_picked)
- **Removal Impact**: If you remove this, you must also remove: stock_location_fill_state_qty_picked.
- **Dependencies (Requires)**: `base_partition, stock, stock_location_pending_move`
- **Dependents (Required By)**: `stock_location_fill_state_qty_picked`
- **Codebase Size**: 394 Python lines, 80 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_location_fill_state_qty_picked` — Stock Location Fill State Qty Picked
- **Summary**: Glue module between stock_location_fill_state and stock_move_line_qty_picked
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock_location_fill_state, stock_move_line_qty_picked`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 94 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_location_is_sublocation` — Stock Location Is Sublocation
- **Summary**: Add method to check stock location is sublocation
- **Removal Safety**: 🟡 Caution: 2 Dependent Modules (ddmrp, stock_move_source_relocate)
- **Removal Impact**: If you remove this, you must also remove: ddmrp, stock_move_source_relocate.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `ddmrp, stock_move_source_relocate`
- **Codebase Size**: 109 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_location_lockdown` — Stock Location Lockdown
- **Summary**: Prevent to add stock on locked locations
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 186 Python lines, 14 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_location_pending_move` — Stock Location Pending Move
- **Summary**: 
        This module allows to show pending stock moves (outgoing and incoming)
        on a stock location
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (stock_location_fill_state)
- **Removal Impact**: If you remove this, you must also remove: stock_location_fill_state.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `stock_location_fill_state`
- **Codebase Size**: 174 Python lines, 31 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_location_position` — Stock Location Position
- **Summary**: Add coordinate attributes on stock location.
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (stock_location_bin_name)
- **Removal Impact**: If you remove this, you must also remove: stock_location_bin_name.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `stock_location_bin_name`
- **Codebase Size**: 106 Python lines, 37 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_location_tray` — Location Trays
- **Summary**: Organize a location as a matrix of cells
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (stock_vertical_lift)
- **Removal Impact**: If you remove this, you must also remove: stock_vertical_lift.
- **Dependencies (Requires)**: `stock, base_sparse_field`
- **Dependents (Required By)**: `stock_vertical_lift`
- **Codebase Size**: 905 Python lines, 322 XML lines
- **Customization Complexity**: **High (Tier 3)** | **Effort**: 2 – 5 Days | **Estimated Cost**: $1,000 – $3,500

---

#### `stock_location_zone` — Stock Location Zone
- **Summary**: Classify locations with zones.
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (stock_location_bin_name)
- **Removal Impact**: If you remove this, you must also remove: stock_location_bin_name.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `stock_location_bin_name`
- **Codebase Size**: 190 Python lines, 51 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_lot_catalog` — Stock Lot Catalog
- **Summary**: No summary provided.
- **Removal Safety**: 🔴 Core Dependency: 3 Modules Depend on It
- **Removal Impact**: Critical foundation module. Removing it will disable 3 other modules.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `stock_lot_catalog_condition, stock_lot_catalog_price, stock_lot_catalog_warehouse`
- **Codebase Size**: 171 Python lines, 298 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_lot_catalog_condition` — Stock Lot Catalog Condition
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock_lot_catalog, stock_lot_condition`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 31 Python lines, 43 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_lot_catalog_price` — StockLot Catalog Price
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock_lot_catalog, stock_lot_list_price`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 28 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_lot_catalog_warehouse` — Stock Lot Catalog Warehouse
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock_lot_catalog, stock_lot_warehouse`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 16 Python lines, 23 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_lot_condition` — Stock Lot Condition
- **Summary**: No summary provided.
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (stock_lot_catalog_condition)
- **Removal Impact**: If you remove this, you must also remove: stock_lot_catalog_condition.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `stock_lot_catalog_condition`
- **Codebase Size**: 67 Python lines, 147 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_lot_image` — Stock Lot Image
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 105 Python lines, 129 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_lot_list_price` — Stock Lot List Price
- **Summary**: No summary provided.
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (stock_lot_catalog_price)
- **Removal Impact**: If you remove this, you must also remove: stock_lot_catalog_price.
- **Dependencies (Requires)**: `stock_account`
- **Dependents (Required By)**: `stock_lot_catalog_price`
- **Codebase Size**: 27 Python lines, 19 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_lot_multi_image` — Multiple Images in Stock Lot
- **Summary**: This module implements the possibility to
    have multiple images for a stock lot
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock, base_multi_image`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 181 Python lines, 32 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_lot_warehouse` — Stock Lot Warehouse
- **Summary**: No summary provided.
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (stock_lot_catalog_warehouse)
- **Removal Impact**: If you remove this, you must also remove: stock_lot_catalog_warehouse.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `stock_lot_catalog_warehouse`
- **Codebase Size**: 27 Python lines, 45 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_move_common_dest` — Stock Move Common Destination
- **Summary**: Adds field for common destination moves
- **Removal Safety**: 🟡 Caution: 2 Dependent Modules (stock_checkout_sync, stock_picking_completion_info)
- **Removal Impact**: If you remove this, you must also remove: stock_checkout_sync, stock_picking_completion_info.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `stock_checkout_sync, stock_picking_completion_info`
- **Codebase Size**: 272 Python lines, 27 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_move_line_lot_link` — Stock Move Line Lot Link
- **Summary**: Display Lot/SN column on Detailed Operations to allow navigation.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 49 Python lines, 67 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_move_line_reference_link` — Stock Move Line Reference Link
- **Summary**: Add link in stock move line references.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 119 Python lines, 15 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_move_location` — Move Stock Location
- **Summary**: This module allows to move all stock in a stock location to an other one.
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (stock_move_location_purchase_uom)
- **Removal Impact**: If you remove this, you must also remove: stock_move_location_purchase_uom.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `stock_move_location_purchase_uom`
- **Codebase Size**: 1293 Python lines, 253 XML lines
- **Customization Complexity**: **High (Tier 3)** | **Effort**: 2 – 5 Days | **Estimated Cost**: $1,000 – $3,500

---

#### `stock_move_location_purchase_uom` — Move Stock Location Purchase UoM
- **Summary**: This module 'glues' the modules stock_move_location and stock_move_purchase_uom.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock_move_location, stock_move_purchase_uom`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 197 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_move_packaging_qty` — Stock Packaging Qty
- **Summary**: Add packaging fields in the stock moves
- **Removal Safety**: 🟡 Caution: 2 Dependent Modules (mrp_packaging_default, stock_picking_batch_packaging_qty)
- **Removal Impact**: If you remove this, you must also remove: mrp_packaging_default, stock_picking_batch_packaging_qty.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `mrp_packaging_default, stock_picking_batch_packaging_qty`
- **Codebase Size**: 439 Python lines, 263 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_move_purchase_uom` — Stock Move Purchase UoM
- **Summary**: Allow to use the purchase UoM in a stock move
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (stock_move_location_purchase_uom)
- **Removal Impact**: If you remove this, you must also remove: stock_move_location_purchase_uom.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `stock_move_location_purchase_uom`
- **Codebase Size**: 391 Python lines, 18 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_move_reset_quantity` — Move Stock Reset Quantity
- **Summary**: Reset quantity to zero
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 75 Python lines, 42 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_mts_mto_rule` — Stock MTS+MTO Rule
- **Summary**: Add a MTS+MTO route
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 439 Python lines, 66 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_package_type_volume` — Stock Package Type Volume
- **Summary**: Compute volume of a package type
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 110 Python lines, 19 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_picking_batch_packaging_qty` — Stock Batch Packaging Qty
- **Summary**: Add packaging fields in stock picking batch
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock_picking_batch, stock_move_packaging_qty`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 19 Python lines, 47 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_picking_commercial_partner` — Stock Picking Commercial Entity
- **Summary**: 
        Add Commercial Partner on the Stock Picking
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 66 Python lines, 51 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_picking_completion_info` — Stock Picking Completion Info
- **Summary**: Display on current document completion information according to next operations
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock_move_common_dest`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 376 Python lines, 44 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_picking_procure_method` — Stock Picking Procure Method
- **Summary**: Allows to force the procurement method from the picking
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 350 Python lines, 17 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_picking_show_linked` — Stock Picking Show Linked
- **Summary**: 
       This addon allows to easily access related pickings
       (in the case of chained routes) through a button
       in the parent picking view.
    
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 64 Python lines, 25 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_picking_stage` — Stock Picking Stages
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 59 Python lines, 86 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_picking_supplier_ref` — Stock Picking Supplier Reference
- **Summary**: 
        Adds a supplier reference field inside supplier's pickings and
        allows search for this reference.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 112 Python lines, 37 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_putaway_product_template` — Product template in putaway strategies
- **Summary**: Add product template in putaway strategies from the product view
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 224 Python lines, 25 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_quant_cost_info` — Stock Quant Cost Info
- **Summary**: Shows the cost of the quants
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 118 Python lines, 37 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_quant_reservation_info` — Stock Move Reservation Info
- **Summary**: Allows to see the reserved info of Products
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (stock_quant_reservation_info_mrp)
- **Removal Impact**: If you remove this, you must also remove: stock_quant_reservation_info_mrp.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `stock_quant_reservation_info_mrp`
- **Codebase Size**: 74 Python lines, 79 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_quant_reservation_info_mrp` — Stock Move Reservation Info MRP
- **Summary**: Allows to see the manufacturing order related to the reserved info of Products
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock_quant_reservation_info, mrp`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 37 Python lines, 39 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_removal_location_by_priority` — Stock Removal Location by Priority
- **Summary**: Establish a removal priority on stock locations.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 307 Python lines, 46 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_restrict_immediate_adjustment` — Stock Restrict Immediate Adjustment
- **Summary**: Restrict immediate stock adjustments from Stock On Hand view
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 19 Python lines, 23 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_route_location_source` — Stock Route Location Source
- **Summary**: Add method to get source location of Inventory Routes
- **Removal Safety**: 🟡 Caution: 2 Dependent Modules (stock_location_orderpoint, stock_move_source_relocate)
- **Removal Impact**: If you remove this, you must also remove: stock_location_orderpoint, stock_move_source_relocate.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `stock_location_orderpoint, stock_move_source_relocate`
- **Codebase Size**: 136 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_route_mto` — Stock Route Mto
- **Summary**: 
        Allows to identify MTO routes through a checkbox and availability to filter
        them.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 45 Python lines, 45 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_storage_category_capacity_name` — Stock Storage Category Capacity Name
- **Summary**: Allows to have a better display name for Stock Storage Category Capacity model
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 152 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_valuation_layer_inventory_filter` — Stock Valuation Layer Inventory Filter
- **Summary**: Allows to filter Inventory Adjustments on Stock Valuation Layers
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock_account`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 34 Python lines, 33 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_vertical_lift` — Vertical Lift
- **Summary**: Provides the core for integration with Vertical Lifts
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (stock_vertical_lift_empty_tray_check)
- **Removal Impact**: If you remove this, you must also remove: stock_vertical_lift_empty_tray_check.
- **Dependencies (Requires)**: `stock, barcodes, base_sparse_field, stock_location_tray, web_notify`
- **Dependents (Required By)**: `stock_vertical_lift_empty_tray_check`
- **Codebase Size**: 3512 Python lines, 1015 XML lines
- **Customization Complexity**: **Enterprise (Tier 4)** | **Effort**: 1 – 3 Weeks | **Estimated Cost**: $3,500 – $10,000+

---

#### `stock_vertical_lift_empty_tray_check` — Vertical Lift Empty Tray Check
- **Summary**: Checks if the tray is actually empty.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock, stock_vertical_lift`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 263 Python lines, 66 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_vlm_mgmt` — Vertical Lift Module management
- **Summary**: Light self contained alternative for VLM integrations
- **Removal Safety**: 🟡 Caution: 2 Dependent Modules (stock_vlm_mgmt_kardex, stock_vlm_mgmt_modula)
- **Removal Impact**: If you remove this, you must also remove: stock_vlm_mgmt_kardex, stock_vlm_mgmt_modula.
- **Dependencies (Requires)**: `stock, base_sparse_field`
- **Dependents (Required By)**: `stock_vlm_mgmt_kardex, stock_vlm_mgmt_modula`
- **Codebase Size**: 1177 Python lines, 815 XML lines
- **Customization Complexity**: **High (Tier 3)** | **Effort**: 2 – 5 Days | **Estimated Cost**: $1,000 – $3,500

---

#### `stock_vlm_mgmt_kardex` — Kardex integration with stock_vlm_mgmt
- **Summary**: Light alternative for Kardex VLM integrations
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock_vlm_mgmt`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 204 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_vlm_mgmt_modula` — Modula integration with stock_vlm_mgmt
- **Summary**: Light alternative for Modula VLM integrations
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock_vlm_mgmt`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 204 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_warehouse_calendar` — Stock Warehouse Calendar
- **Summary**: Adds a calendar to the Warehouse
- **Removal Safety**: 🟡 Caution: 2 Dependent Modules (ddmrp, mrp_warehouse_calendar)
- **Removal Impact**: If you remove this, you must also remove: ddmrp, mrp_warehouse_calendar.
- **Dependencies (Requires)**: `stock, resource`
- **Dependents (Required By)**: `ddmrp, mrp_warehouse_calendar`
- **Codebase Size**: 424 Python lines, 15 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_warehouse_out_pull` — Stock Warehouse Out Pull
- **Summary**: Restore delivery pull rules as in Odoo <= 17.0
- **Removal Safety**: 🟡 Caution: 2 Dependent Modules (stock_picking_consolidation_priority, stock_picking_group_by_partner_by_carrier)
- **Removal Impact**: If you remove this, you must also remove: stock_picking_consolidation_priority, stock_picking_group_by_partner_by_carrier.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `stock_picking_consolidation_priority, stock_picking_group_by_partner_by_carrier`
- **Codebase Size**: 234 Python lines, 15 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_warehouse_resupply_route_push` — Stock Warehouse Resupply Route Push
- **Summary**: Use push rules for resupply from other warehouse routes.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 700 Python lines, 30 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_warehouse_security` — Stock Warehouse Security
- **Summary**: Restrict user access in multi-warehouse environment
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 632 Python lines, 116 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---


### Suite D: Procurement & Orderpoints (`stock-logistics-orderpoint`)

**Total Modules in this Suite**: 9

#### `purchase_stock_product_replenish_supplier` — Purchase Stock Product Replenish Default Supplier
- **Summary**: Set default supplier in product replenish wizard
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `purchase_stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 93 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_location_orderpoint` — Stock Location Orderpoint
- **Summary**: Declare orderpoint on a location allowing to replenish any product with the same criteria.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock_available_base_exclude_location, stock_route_location_source, queue_job`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 2668 Python lines, 308 XML lines
- **Customization Complexity**: **High (Tier 3)** | **Effort**: 2 – 5 Days | **Estimated Cost**: $1,000 – $3,500

---

#### `stock_orderpoint_default_location` — Stock Orderpoint Default Location
- **Summary**: 
        This module allows to define a different default location than the
        stock location
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock, base_partition`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 128 Python lines, 23 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_orderpoint_generator` — Order point generator
- **Summary**: Mass configuration of stock order points
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 745 Python lines, 241 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_orderpoint_manual_procurement` — Stock Orderpoint Manual Procurement
- **Summary**: Allows to create procurement orders from orderpoints instead of relying only on the scheduler.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `purchase_stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 434 Python lines, 159 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_orderpoint_move_link` — Stock Orderpoint Move Link
- **Summary**: Link Reordering rules to stock moves
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (stock_orderpoint_purchase_link)
- **Removal Impact**: If you remove this, you must also remove: stock_orderpoint_purchase_link.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `stock_orderpoint_purchase_link`
- **Codebase Size**: 235 Python lines, 33 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_orderpoint_no_horizon` — Stock Orderpoint No Horizon
- **Summary**: Consider all future moves, do not limit horizon to the rule lead days.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 120 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_orderpoint_purchase_link` — Stock Orderpoint Purchase Link
- **Summary**: Link Reordering rules to purchase orders
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock_orderpoint_move_link, purchase_stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 187 Python lines, 36 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_orderpoint_uom` — Stock Orderpoint UoM
- **Summary**: Allows to create procurement orders in the UoM indicated in the orderpoint
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `purchase_stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 281 Python lines, 26 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---


### Suite E: Stock Movements & Workflows (`stock-logistics-workflow`)

**Total Modules in this Suite**: 96

#### `delivery_procurement_group_carrier` — Delivery Procurement Group Carrier
- **Summary**: No summary provided.
- **Removal Safety**: 🔴 Core Dependency: 3 Modules Depend on It
- **Removal Impact**: Critical foundation module. Removing it will disable 3 other modules.
- **Dependencies (Requires)**: `sale_stock, stock_delivery`
- **Dependents (Required By)**: `procurement_auto_create_group_carrier, stock_dynamic_routing_delivery_procurement_group_carrier, stock_picking_group_by_partner_by_carrier`
- **Codebase Size**: 367 Python lines, 13 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `procurement_auto_create_group_carrier` — Procurement Auto Create Group Carrier
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `delivery_procurement_group_carrier, procurement_auto_create_group`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 92 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `product_cost_price_avco_sync` — Product cost price avco sync
- **Summary**: Set product cost price from updated moves
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock_account`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 1071 Python lines, 0 XML lines
- **Customization Complexity**: **High (Tier 3)** | **Effort**: 2 – 5 Days | **Estimated Cost**: $1,000 – $3,500

---

#### `purchase_stock_picking_invoice_link` — Purchase Stock Picking Invoice Link
- **Summary**: Adds link between purchases, pickings and invoices
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock_picking_invoice_link, purchase_stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 332 Python lines, 0 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `sale_line_returned_qty` — Sale Line Returned Qty
- **Summary**: Track returned quantity of sale order lines.
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (sale_line_returned_qty_mrp)
- **Removal Impact**: If you remove this, you must also remove: sale_line_returned_qty_mrp.
- **Dependencies (Requires)**: `sale_stock`
- **Dependents (Required By)**: `sale_line_returned_qty_mrp`
- **Codebase Size**: 129 Python lines, 40 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `sale_line_returned_qty_mrp` — Sale Line Returned Qty Mrp
- **Summary**: Track returned quantity of sale order lines for BoM products.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `sale_line_returned_qty, mrp`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 316 Python lines, 0 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `sale_order_global_stock_route` — Sale Order Global Stock Route
- **Summary**: Add the possibility to choose one warehouse path for an order
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `sale_stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 189 Python lines, 17 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `sale_stock_picking_invoice_link` — Stock Picking Invoice Link
- **Summary**: Adds link between pickings and invoices
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `sale_stock, stock_picking_invoice_link`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 555 Python lines, 0 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `sale_stock_restocking_fee_invoicing` — Sale Stock Restocking Fee Invoicing
- **Summary**: 
        On demand charge restocking fee for accepting returned goods .
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `sale, stock, sale_stock, stock_account, stock_picking_kind`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 547 Python lines, 112 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `scrap_reason_code` — Scrap Reason Code
- **Summary**: Reason code for scrapping
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (mrp_workcenter_scrap_reason)
- **Removal Impact**: If you remove this, you must also remove: mrp_workcenter_scrap_reason.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `mrp_workcenter_scrap_reason`
- **Codebase Size**: 372 Python lines, 113 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_account_product_run_fifo_hook` — Stock Account Product Run FIFO Hook
- **Summary**: Add more flexibility in the run fifo method.
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (stock_valuation_layer_usage)
- **Removal Impact**: If you remove this, you must also remove: stock_valuation_layer_usage.
- **Dependencies (Requires)**: `stock_account`
- **Dependents (Required By)**: `stock_valuation_layer_usage`
- **Codebase Size**: 454 Python lines, 0 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_account_show_automatic_valuation` — Show Automatic Valuation for Stock Moves in CE
- **Summary**: Allow automatic valuation for stock moves in community edition
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock_account`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 40 Python lines, 23 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_checkout_sync` — Stock Checkout Synchronization
- **Summary**: Sync location for Checkout operations
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (stock_dynamic_routing_checkout_sync)
- **Removal Impact**: If you remove this, you must also remove: stock_dynamic_routing_checkout_sync.
- **Dependencies (Requires)**: `stock_move_common_dest`
- **Dependents (Required By)**: `stock_dynamic_routing_checkout_sync`
- **Codebase Size**: 497 Python lines, 104 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_dynamic_routing` — Stock Dynamic Routing
- **Summary**: Dynamic routing of stock moves
- **Removal Safety**: 🔴 Core Dependency: 3 Modules Depend on It
- **Removal Impact**: Critical foundation module. Removing it will disable 3 other modules.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `stock_dynamic_routing_checkout_sync, stock_dynamic_routing_delivery, stock_move_source_relocate_dynamic_routing`
- **Codebase Size**: 3311 Python lines, 196 XML lines
- **Customization Complexity**: **Enterprise (Tier 4)** | **Effort**: 1 – 3 Weeks | **Estimated Cost**: $3,500 – $10,000+

---

#### `stock_dynamic_routing_checkout_sync` — Stock Dynamic Routing - Checkout Sync
- **Summary**: Glue module for tests when dynamic routing and checkout sync are used 
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock_dynamic_routing, stock_checkout_sync`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 228 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_dynamic_routing_delivery` — Stock Dynamic Routing Delivery
- **Summary**: Glue module between stock dynamic routing and delivery
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (stock_dynamic_routing_delivery_procurement_group_carrier)
- **Removal Impact**: If you remove this, you must also remove: stock_dynamic_routing_delivery_procurement_group_carrier.
- **Dependencies (Requires)**: `stock_dynamic_routing, stock_delivery`
- **Dependents (Required By)**: `stock_dynamic_routing_delivery_procurement_group_carrier`
- **Codebase Size**: 217 Python lines, 22 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_dynamic_routing_delivery_procurement_group_carrier` — Stock Dynamic Routing Delivery Procurement Group Carrier
- **Summary**: Use the carrier set on the procurement group for propagation
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock_dynamic_routing_delivery, delivery_procurement_group_carrier`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 205 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_landed_costs_priority` — Stock Landed Costs Priority
- **Summary**: Add priority to landed costs
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock_landed_costs`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 41 Python lines, 87 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_landed_costs_purchase_auto` — Stock landed costs purchase auto
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock_landed_costs, purchase_stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 223 Python lines, 54 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_lock_lot` — Stock Lock Lot
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock, product`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 309 Python lines, 96 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_lot_scrap` — Scrap Production Lot
- **Summary**: This module adds a button in Production Lot/Serial Number view form to Scrap all products contained.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 202 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_move_actual_date` — Stock Move Actual Date
- **Summary**: No summary provided.
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (mrp_stock_move_actual_date)
- **Removal Impact**: If you remove this, you must also remove: mrp_stock_move_actual_date.
- **Dependencies (Requires)**: `stock_account`
- **Dependents (Required By)**: `mrp_stock_move_actual_date`
- **Codebase Size**: 607 Python lines, 226 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_move_backdating` — Stock Move Backdating
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock_account`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 678 Python lines, 120 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_move_forced_lot` — Stock Move Forced Lot
- **Summary**: 
        This module allows you to set a lot_id in a procurement
         to force the stock move generated to only reserve the selected lot.
    
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 188 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_move_line_change_lot` — Stock Move Line Change Lot
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 693 Python lines, 0 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_move_line_dates` — Stock Move Line Dates
- **Summary**: Add Date Scheduled and Deadline dates in move lines
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 56 Python lines, 81 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_move_line_expiration_date_required` — Stock Move Line Expiration Date Required
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `product_expiry`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 278 Python lines, 43 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_move_line_qty_picked` — Stock Move Line Qty Picked
- **Summary**: Separate quantity picked from the reserved quantity
- **Removal Safety**: 🟡 Caution: 2 Dependent Modules (mrp_stock_move_line_qty_picked, stock_location_fill_state_qty_picked)
- **Removal Impact**: If you remove this, you must also remove: mrp_stock_move_line_qty_picked, stock_location_fill_state_qty_picked.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `mrp_stock_move_line_qty_picked, stock_location_fill_state_qty_picked`
- **Codebase Size**: 386 Python lines, 49 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_move_original_date` — Stock Move Original Scheduled Date
- **Summary**: adds the Original Date Scheduled to stock moves.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 156 Python lines, 47 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_move_propagate_first_move` — Stock Move Picking Type Origin
- **Summary**: 
        This addon propagate the picking type of the original move to all next moves
        created from procurement
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (stock_picking_batch_outgoing)
- **Removal Impact**: If you remove this, you must also remove: stock_picking_batch_outgoing.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `stock_picking_batch_outgoing`
- **Codebase Size**: 449 Python lines, 15 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_move_quantity_product_uom` — Stock Move Quantity Product UOM
- **Summary**: computes stock.move's quantity in the uom of the product.
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (ddmrp)
- **Removal Impact**: If you remove this, you must also remove: ddmrp.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `ddmrp`
- **Codebase Size**: 133 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_move_source_relocate` — Stock Move Source Relocation
- **Summary**: Change source location of unavailable moves
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (stock_move_source_relocate_dynamic_routing)
- **Removal Impact**: If you remove this, you must also remove: stock_move_source_relocate_dynamic_routing.
- **Dependencies (Requires)**: `stock, stock_location_is_sublocation, stock_route_location_source`
- **Dependents (Required By)**: `stock_move_source_relocate_dynamic_routing`
- **Codebase Size**: 571 Python lines, 94 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_move_source_relocate_dynamic_routing` — Stock Source Relocate - Dynamic Routing
- **Summary**: Glue module
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock_dynamic_routing, stock_move_source_relocate`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 403 Python lines, 41 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_move_vendor_comment` — Stock Move Vendor Comment
- **Summary**: Add the vendor comment field to stock move
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 50 Python lines, 63 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_no_negative` — Stock Disallow Negative
- **Summary**: Disallow negative stock levels by default
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (mrp_subcontracting_skip_no_negative)
- **Removal Impact**: If you remove this, you must also remove: mrp_subcontracting_skip_no_negative.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `mrp_subcontracting_skip_no_negative`
- **Codebase Size**: 347 Python lines, 49 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_override_procurement` — Stock Override Procurement
- **Summary**: 
        This technical module allow to override procurement values
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 166 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_owner_restriction` — Stock Owner Restriction
- **Summary**: Do not reserve quantity with assigned owner
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 595 Python lines, 87 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_picking_auto_create_lot` — Stock Picking Auto Create Lot
- **Summary**: Auto create lots for incoming pickings
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (mrp_byproduct_auto_create_lot)
- **Removal Impact**: If you remove this, you must also remove: mrp_byproduct_auto_create_lot.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `mrp_byproduct_auto_create_lot`
- **Codebase Size**: 460 Python lines, 45 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_picking_auto_create_package` — Stock Picking Auto Create Package
- **Summary**: 
        Put all move lines in packs on validation.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 418 Python lines, 39 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_picking_back2draft` — Pickings back to draft
- **Summary**: Reopen canceled transfers
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 119 Python lines, 19 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_picking_backorder_strategy_cancel` — Picking backordering strategies
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 133 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_picking_batch_account` — Stock batch picking account
- **Summary**: Generates invoices when batch is set to Done state
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock_picking_batch, sale`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 236 Python lines, 38 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_picking_batch_extended` — Stock batch picking extended
- **Summary**: Allows manage a lot of pickings in batch
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock_picking_batch, stock_delivery`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 987 Python lines, 494 XML lines
- **Customization Complexity**: **High (Tier 3)** | **Effort**: 2 – 5 Days | **Estimated Cost**: $1,000 – $3,500

---

#### `stock_picking_batch_operation_quick_change` — Stock Picking Batch Operation Quick Change
- **Summary**: Change location of all picking batch operations
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock_picking_batch`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 285 Python lines, 72 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_picking_batch_outgoing` — Stock picking batch outgoing
- **Summary**: Allows set on pickings the batch picking from last picking (out)
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock_move_propagate_first_move, stock_picking_batch`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 164 Python lines, 66 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_picking_batch_planner` — Stock Picking Batch Planner
- **Summary**: Allow planning origin batches/waves from destination batch/wave
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock_picking_batch`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 664 Python lines, 76 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_picking_batch_print_invoices` — Stock Picking Batch Print Invoices
- **Summary**: Print invoices from stock picking batchs
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `sale, stock_picking_batch_print_pickings`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 299 Python lines, 105 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_picking_batch_print_pickings` — Stock Picking Batch Print Pickings
- **Summary**: Print Picking from Stock Picking Batch
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (stock_picking_batch_print_invoices)
- **Removal Impact**: If you remove this, you must also remove: stock_picking_batch_print_invoices.
- **Dependencies (Requires)**: `stock_picking_batch`
- **Dependents (Required By)**: `stock_picking_batch_print_invoices`
- **Codebase Size**: 260 Python lines, 132 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_picking_batch_validate_confirm` — Stock Picking Batch Validate Confirm
- **Summary**: Request confirmation when validating batch if any pending origin moves
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock_picking_batch`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 188 Python lines, 44 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_picking_consolidation_priority` — Stock Transfers Consolidation Priority
- **Summary**: Raise priority of all transfers for a chain when started
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock, stock_warehouse_out_pull`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 534 Python lines, 13 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_picking_customer_ref` — Stock Picking Customer Reference
- **Summary**: This module displays the sale reference/description in the pickings
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `sale_stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 121 Python lines, 45 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_picking_date_deadline_syncs_scheduled_date` — Stock Picking Date Deadline syncs Scheduled Date
- **Summary**: Sync Scheduled Date with Date Deadline in Stock Picking
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 130 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_picking_filter_lot` — Stock picking filter lot
- **Summary**: In picking out lots' selection, filter lots based on their location
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 111 Python lines, 76 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_picking_group_by_base` — Stock Picking Group By Base
- **Summary**: 
        Allows to define a way to create index on extensible domain
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (stock_picking_group_by_partner_by_carrier)
- **Removal Impact**: If you remove this, you must also remove: stock_picking_group_by_partner_by_carrier.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `stock_picking_group_by_partner_by_carrier`
- **Codebase Size**: 134 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_picking_group_by_partner_by_carrier` — Stock Picking: group by partner and carrier
- **Summary**: No summary provided.
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (stock_picking_group_by_partner_by_carrier_force_move_type)
- **Removal Impact**: If you remove this, you must also remove: stock_picking_group_by_partner_by_carrier_force_move_type.
- **Dependencies (Requires)**: `delivery_procurement_group_carrier, sale_stock, stock_delivery, stock_picking_group_by_base, stock_warehouse_out_pull`
- **Dependents (Required By)**: `stock_picking_group_by_partner_by_carrier_force_move_type`
- **Codebase Size**: 3100 Python lines, 392 XML lines
- **Customization Complexity**: **Enterprise (Tier 4)** | **Effort**: 1 – 3 Weeks | **Estimated Cost**: $3,500 – $10,000+

---

#### `stock_picking_group_by_partner_by_carrier_force_move_type` — Stock Picking Type Force Shipping Policy - Group By Partner and Carrier
- **Summary**: Glue module for Picking Type Force Shipping Policy and Group Transfers by Partner and Carrier
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock_picking_type_force_move_type, stock_picking_group_by_partner_by_carrier`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 88 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_picking_immediate_transfer_warning` — Stock Picking Immediate Transfer Warning
- **Summary**: 
        Warn before processing a reserved transfer when no
        moves have been explicitly picked.
    
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 263 Python lines, 87 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_picking_import_serial_number` — Stock Picking Import Serial Numbers
- **Summary**: Import S/N from excel file for incoming pickings
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 490 Python lines, 108 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_picking_invoice_link` — Stock Picking Invoice Link
- **Summary**: Adds link between pickings and invoices
- **Removal Safety**: 🟡 Caution: 2 Dependent Modules (purchase_stock_picking_invoice_link, sale_stock_picking_invoice_link)
- **Removal Impact**: If you remove this, you must also remove: purchase_stock_picking_invoice_link, sale_stock_picking_invoice_link.
- **Dependencies (Requires)**: `stock_account`
- **Dependents (Required By)**: `purchase_stock_picking_invoice_link, sale_stock_picking_invoice_link`
- **Codebase Size**: 386 Python lines, 76 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_picking_kind` — Stock Picking Kind
- **Summary**: 
        Computes the kind of picking based on locations
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (sale_stock_restocking_fee_invoicing)
- **Removal Impact**: If you remove this, you must also remove: sale_stock_restocking_fee_invoicing.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `sale_stock_restocking_fee_invoicing`
- **Codebase Size**: 213 Python lines, 43 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_picking_line_sequence` — Stock picking lines with sequence number
- **Summary**: Manages the order of stock moves by displaying its sequence
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock, sale, sale_stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 318 Python lines, 68 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_picking_mass_action` — Stock Picking Mass Action
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock_account`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 245 Python lines, 53 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_picking_operation_quick_change` — Stock Picking Operation Quick Change
- **Summary**: Change location of all picking operations
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 301 Python lines, 76 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_picking_origin_reference` — Stock Picking Origin Reference
- **Summary**: Add clickable button to the Transfer Source Document.
- **Removal Safety**: 🟡 Caution: 2 Dependent Modules (stock_picking_origin_reference_purchase, stock_picking_origin_reference_sale)
- **Removal Impact**: If you remove this, you must also remove: stock_picking_origin_reference_purchase, stock_picking_origin_reference_sale.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `stock_picking_origin_reference_purchase, stock_picking_origin_reference_sale`
- **Codebase Size**: 108 Python lines, 16 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_picking_origin_reference_purchase` — Stock Picking Origin Reference Purchase
- **Summary**: Transfer to Purchase Order navigation from the Source Document.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock_picking_origin_reference, purchase`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 97 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_picking_origin_reference_sale` — Stock Picking Origin Reference Sale
- **Summary**: Transfer to Sales Order navigation from the Source Document.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock_picking_origin_reference, sale`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 91 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_picking_partner_note` — Stock Picking Partner Note
- **Summary**: Add partner notes on picking
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `sale_stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 245 Python lines, 130 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_picking_partner_vat` — Stock Picking - Partner/Customer VAT
- **Summary**: 
        This module extends the picking functionality. It allows:
        * Displaying the partner's VAT on the picking form view.
        * Displaying the partner's VAT on reports:
            * Picking Operations
            * Delivery Slip
    
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 30 Python lines, 40 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_picking_propagate_scheduled_date` — Stock Picking Propagate Scheduled Date
- **Summary**: Propagate Stock Picking Scheduled Date
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 339 Python lines, 0 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_picking_purchase_order_link` — Stock Picking Purchase Order Link
- **Summary**: Link between picking and purchase order
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `purchase_stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 94 Python lines, 25 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_picking_restrict_cancel_printed` — Stock Picking - restrict cancelation if printed
- **Summary**: Prevent canceling a stock transfer if printed.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 170 Python lines, 26 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_picking_restrict_cancel_with_orig_move` — Stock Picking Restrict Cancel with Original Moves
- **Summary**: Restrict cancellation of dest moves according to origin.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 285 Python lines, 13 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_picking_restrict_partial_validation` — Stock Picking Restrict Partial Validation
- **Summary**: Block validation of transfers that are not fully reserved and processed in full
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 279 Python lines, 15 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_picking_return_empty_package` — Empty Package At Picking Return
- **Summary**: Ensure that only package content is put in stock during
    a picking return
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 143 Python lines, 14 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_picking_return_lot` — Stock Picking Return Lot
- **Summary**: Propagate SN/lots from origin picking to return picking.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock_restrict_lot, stock_picking_return_restricted_qty`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 395 Python lines, 24 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_picking_return_restricted_qty` — Stock Picking Return Restricted Qty
- **Summary**: Restrict the return to delivered quantity
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (stock_picking_return_lot)
- **Removal Impact**: If you remove this, you must also remove: stock_picking_return_lot.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `stock_picking_return_lot`
- **Codebase Size**: 223 Python lines, 13 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_picking_sale_order_link` — Stock Picking Sale Order Link
- **Summary**: Link between picking and sale order
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `sale_stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 100 Python lines, 23 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_picking_send_by_mail` — Stock Picking by Mail
- **Summary**: Send stock picking by email
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock, mail`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 107 Python lines, 19 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_picking_show_backorder` — Stock Picking Show Backorder
- **Summary**: Provides a new field on stock pickings, allowing to display the corresponding backorders.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 92 Python lines, 23 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_picking_show_lot` — Stock Picking Show Lot
- **Summary**: 
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 40 Python lines, 19 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_picking_show_return` — Show returns on stock pickings
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 134 Python lines, 28 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_picking_type_bypass_reservation` — Stock Picking Type Bypass Reservation
- **Summary**: Bypass reservation on desired Stock Picking Types
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 178 Python lines, 36 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_picking_type_force_move_type` — Stock Picking Type Force Shipping Policy
- **Summary**: Force shipping policies on operation types
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (stock_picking_group_by_partner_by_carrier_force_move_type)
- **Removal Impact**: If you remove this, you must also remove: stock_picking_group_by_partner_by_carrier_force_move_type.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `stock_picking_group_by_partner_by_carrier_force_move_type`
- **Codebase Size**: 183 Python lines, 18 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_picking_variable_qty` — Stock Picking Variable Qty
- **Summary**: Handle variable quantity in multi-step deliveries/receptions
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `sale_stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 618 Python lines, 16 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_picking_warn_message` — Stock Picking Warn Message
- **Summary**: 
        Add a popup warning on picking to ensure warning is populated
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 212 Python lines, 39 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_picking_whole_scrap` — Stock Picking Whole Scrap
- **Summary**: Create whole scrap from a picking for move lines
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 269 Python lines, 78 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_production_lot_active` — Stock Production Lot Active
- **Summary**: Allow to archive/unarchive lots/serial numbers
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 72 Python lines, 35 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_receipt_lot_info` — Stock Receipt Lot Info
- **Summary**: Be able to introduce more info on lot/serial number while processing a receipt.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock, product_expiry`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 150 Python lines, 77 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_reception_discrepancy_distribution` — Stock Reception Discrepancy Distribution
- **Summary**: Change demand in stock moves linked to reception one
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `sale_purchase_stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 197 Python lines, 131 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_reporting_access` — Stock Reporting Access
- **Summary**: Add a security group for inventory reporting access
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 78 Python lines, 20 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_restrict_lot` — Stock Restrict Lot
- **Summary**: Base module that add back the concept of restrict lot on stock move
- **Removal Safety**: 🟡 Caution: 2 Dependent Modules (mrp_restrict_lot, stock_picking_return_lot)
- **Removal Impact**: If you remove this, you must also remove: mrp_restrict_lot, stock_picking_return_lot.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `mrp_restrict_lot, stock_picking_return_lot`
- **Codebase Size**: 673 Python lines, 75 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_scrap_cancel` — Stock Scrap Cancel
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 93 Python lines, 26 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_scrap_security` — Stock Scrap Security
- **Summary**: 
        Manage stock scrap access rights with dedicated security groups.
    
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 120 Python lines, 43 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_split_picking` — Split picking
- **Summary**: Split a picking in two not transferred pickings
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (stock_split_picking_kit)
- **Removal Impact**: If you remove this, you must also remove: stock_split_picking_kit.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `stock_split_picking_kit`
- **Codebase Size**: 783 Python lines, 87 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_split_picking_kit` — Stock Split Picking Kit
- **Summary**: Split a picking by a number of kits.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock_split_picking, mrp`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 439 Python lines, 16 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_valuation_layer_usage` — Stock Valuation Layer Usage
- **Summary**: Trace where has the stock valuation been used in, including the quantities taken.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `sale, stock_account_product_run_fifo_hook`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 631 Python lines, 132 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---


### Suite F: Stock Availability & Priority Allocation (`stock-logistics-availability`)

**Total Modules in this Suite**: 8

#### `stock_available` — Stock available to promise
- **Summary**: No summary provided.
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (stock_available_immediately)
- **Removal Impact**: If you remove this, you must also remove: stock_available_immediately.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `stock_available_immediately`
- **Codebase Size**: 378 Python lines, 164 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_available_base_exclude_location` — Stock Available Base Exclude Location
- **Summary**: 
        Base module to exclude locations for product available quantities
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (stock_location_orderpoint)
- **Removal Impact**: If you remove this, you must also remove: stock_location_orderpoint.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `stock_location_orderpoint`
- **Codebase Size**: 287 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_available_immediately` — Ignore planned receptions in quantity available to promise
- **Summary**: No summary provided.
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (stock_available_immediately_exclude_location)
- **Removal Impact**: If you remove this, you must also remove: stock_available_immediately_exclude_location.
- **Dependencies (Requires)**: `stock_available`
- **Dependents (Required By)**: `stock_available_immediately_exclude_location`
- **Codebase Size**: 175 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_available_immediately_exclude_location` — Exclude locations from immediately usable quantity
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock_available_immediately, stock_available_location_get_domain`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 289 Python lines, 33 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_available_location_get_domain` — Stock Available Location Get Domain
- **Summary**: 
        This is a technical helper module in order to reuse the standard
        _get_domain_locations() function for locations and not quants
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (stock_available_immediately_exclude_location)
- **Removal Impact**: If you remove this, you must also remove: stock_available_immediately_exclude_location.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `stock_available_immediately_exclude_location`
- **Codebase Size**: 312 Python lines, 0 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_available_unreserved` — Stock Available Unreserved
- **Summary**: Quantity of stock available for immediate use
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 517 Python lines, 126 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `stock_free_quantity` — Stock Free Quantity
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 95 Python lines, 119 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `stock_picking_product_availability_inline` — Stock Picking Product Availability Inline
- **Summary**: Show product availability in product drop-down of picking form view.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `stock, base_view_inheritance_extension`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 143 Python lines, 50 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---


### Suite G: Asynchronous Background Queue (`queue`)

**Total Modules in this Suite**: 9

#### `base_import_async` — Asynchronous Import
- **Summary**: Import CSV files in the background
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `base_import, queue_job`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 347 Python lines, 45 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `queue_job` — Job Queue
- **Summary**: No summary provided.
- **Removal Safety**: 🔴 Core Dependency: 9 Modules Depend on It
- **Removal Impact**: Critical foundation module. Removing it will disable 9 other modules.
- **Dependencies (Requires)**: `mail, base_sparse_field, web`
- **Dependents (Required By)**: `base_import_async, ddmrp_cron_actions_as_job, queue_job_batch, queue_job_cron, queue_job_cron_jobrunner, queue_job_profiler, queue_job_subscribe, stock_location_orderpoint, test_queue_job`
- **Codebase Size**: 6854 Python lines, 648 XML lines
- **Customization Complexity**: **Enterprise (Tier 4)** | **Effort**: 1 – 3 Weeks | **Estimated Cost**: $3,500 – $10,000+

---

#### `queue_job_batch` — Job Queue Batch
- **Summary**: No summary provided.
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (test_queue_job_batch)
- **Removal Impact**: If you remove this, you must also remove: test_queue_job_batch.
- **Dependencies (Requires)**: `queue_job`
- **Dependents (Required By)**: `test_queue_job_batch`
- **Codebase Size**: 301 Python lines, 332 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `queue_job_cron` — Scheduled Actions as Queue Jobs
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `queue_job`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 182 Python lines, 54 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `queue_job_cron_jobrunner` — Queue Job Cron Jobrunner
- **Summary**: Run jobs without a dedicated JobRunner
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `queue_job`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 289 Python lines, 30 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `queue_job_profiler` — Job Queue Profiler
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `queue_job`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 312 Python lines, 49 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `queue_job_subscribe` — Queue Job Subscribe
- **Summary**: Control which users are subscribed to queue job notifications
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `queue_job`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 152 Python lines, 17 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `test_queue_job` — Queue Job Tests
- **Summary**: No summary provided.
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (test_queue_job_batch)
- **Removal Impact**: If you remove this, you must also remove: test_queue_job_batch.
- **Dependencies (Requires)**: `queue_job`
- **Dependents (Required By)**: `test_queue_job_batch`
- **Codebase Size**: 2643 Python lines, 101 XML lines
- **Customization Complexity**: **High (Tier 3)** | **Effort**: 2 – 5 Days | **Estimated Cost**: $1,000 – $3,500

---

#### `test_queue_job_batch` — Test Job Queue Batch
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `queue_job_batch, test_queue_job`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 77 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---


### Suite H: Modern Responsive UI & Visual Tools (`web`)

**Total Modules in this Suite**: 63

#### `web_action_conditionable` — web_action_conditionable
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `base, web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 16 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_calendar_slot_duration` — Calendar slot duration
- **Summary**: Customizable calendar slot durations
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 23 Python lines, 8 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_chatter_position` — Chatter Position
- **Summary**: Add an option to change the chatter position
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web, mail`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 58 Python lines, 55 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_company_color` — Web Company Color
- **Summary**: No summary provided.
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (web_responsive_company_color)
- **Removal Impact**: If you remove this, you must also remove: web_responsive_company_color.
- **Dependencies (Requires)**: `web, base_sparse_field`
- **Dependents (Required By)**: `web_responsive_company_color`
- **Codebase Size**: 624 Python lines, 73 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `web_copy_confirm` — Show confirmation dialogue before copying records
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 23 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_dark_mode` — Dark Mode
- **Summary**: Enabled Dark Mode for the Odoo Backend
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 156 Python lines, 14 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_datetime_picker_default_time` — Web Datetime Picker Default Time
- **Summary**: Allows to define a default time on datetime picker
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 23 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_dialog_size` — Web Dialog Size
- **Summary**: 
        A module that lets the user expand a
        dialog box to the full screen width.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 80 Python lines, 42 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_disable_export_group` — Web Disable Export Group
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 106 Python lines, 19 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_editor_class_selector` — Web editor class selector
- **Summary**: 
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web_editor`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 53 Python lines, 104 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_editor_disable_chatgpt` — Web Disable ChatGPT
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web_editor`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 28 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_environment_ribbon` — Web Environment Ribbon
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 93 Python lines, 20 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_excel_export_dynamic_expand` — Web Excel Export Dynamic Expand
- **Summary**: Export collapsed groups or the full tree, based on its view.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 58 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_favicon` — Custom shortcut icon
- **Summary**: Allows to set a custom shortcut icon (aka favicon)
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 222 Python lines, 42 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_filter_header_button` — Filter Button
- **Summary**: Show selected filters as buttons in the control panel
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 19 Python lines, 98 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_font_size_report_layout` — Report Font Size in Document Layout
- **Summary**: Adds a font size selector (pt) to the Document Layout wizard
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 138 Python lines, 128 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_form_banner` — Web Form Banner
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 542 Python lines, 268 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `web_group_expand` — Group Expand Buttons
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 20 Python lines, 23 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_help` — Help Framework
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 26 Python lines, 80 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_ir_actions_act_multi` — Web Actions Multi
- **Summary**: Enables triggering of more than one action on ActionManager
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 78 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_ir_actions_act_window_message` — Client side message boxes
- **Summary**: Show a message box to users
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 66 Python lines, 19 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_m2x_options` — web_m2x_options
- **Summary**: No summary provided.
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (web_m2x_options_manager)
- **Removal Impact**: If you remove this, you must also remove: web_m2x_options_manager.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `web_m2x_options_manager`
- **Codebase Size**: 96 Python lines, 38 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_m2x_options_manager` — Web M2X Options Manager
- **Summary**: Adds an interface to manage the "Create" and "Create and Edit" options for specific models and fields.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `base_view_inheritance_extension, web_m2x_options`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 743 Python lines, 246 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `web_no_bubble` — Web No Bubble
- **Summary**: Remove the bubbles from the web interface
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 19 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_notify` — Web Notify
- **Summary**: 
        Send notification messages to user
- **Removal Safety**: 🔴 Core Dependency: 3 Modules Depend on It
- **Removal Impact**: Critical foundation module. Removing it will disable 3 other modules.
- **Dependencies (Requires)**: `web, bus, base, mail`
- **Dependents (Required By)**: `stock_vertical_lift, web_notify_channel_message, web_notify_upgrade`
- **Codebase Size**: 317 Python lines, 62 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `web_notify_channel_message` — Web Notify Channel Message
- **Summary**: 
        Send an instant notification to channel users when a new message is posted
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web_notify, mail`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 154 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_notify_upgrade` — Web Notify Upgrade
- **Summary**: Notify active users when a module is installed or updated
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web_notify`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 77 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_pivot_computed_measure` — Web Pivot Computed Measure
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 54 Python lines, 243 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_portal_properties` — Web Portal Properties
- **Summary**: Add a new field on properties to show them on portal
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `portal`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 58 Python lines, 112 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_pwa_customize` — Web Pwa Customize
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 259 Python lines, 38 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_quick_start_screen` — Quick Start Screen
- **Summary**: Configurable start screen for quick actions
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 206 Python lines, 231 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `web_refresher` — Web Refresher
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 29 Python lines, 35 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_remember_tree_column_width` — Web Remember Tree Column Width
- **Summary**: Remember the tree columns' widths across sessions.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 24 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_responsive` — Web Responsive
- **Summary**: Responsive web client, community-supported
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (web_responsive_company_color)
- **Removal Impact**: If you remove this, you must also remove: web_responsive_company_color.
- **Dependencies (Requires)**: `web, web_tour, mail`
- **Dependents (Required By)**: `web_responsive_company_color`
- **Codebase Size**: 195 Python lines, 800 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `web_responsive_company_color` — Web Responsive Company Color
- **Summary**: Styling hooks for web_responsive elements
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web_company_color, web_responsive`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 86 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_save_discard_button` — Save & Discard Buttons
- **Summary**: Save & Discard Buttons
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 41 Python lines, 25 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_search_with_and` — Use AND conditions on omnibar search
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 20 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_send_message_popup` — Web Send Message as Popup
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web, mail`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 13 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_session_auto_close` — Web Session Auto Close
- **Summary**: Automatically logs out inactive users based on a configurable
    timeout.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 53 Python lines, 16 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_sort_menu` — Web Sort Menu
- **Summary**: Sort Apps in DropDown/NavBar Menu alphabetically
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 18 Python lines, 8 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_systray_button_init_action` — Web Systray Button Init Action
- **Summary**: Add a button to go to the user init action.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 46 Python lines, 16 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_theme_classic` — Web Theme Classic
- **Summary**: Contrasted style on fields to improve the UI.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 203 Python lines, 27 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_time_range_menu_custom` — Web Time Range Menu Custom
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 24 Python lines, 96 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_timeline` — Web timeline
- **Summary**: Interactive visualization chart to show events in time
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 123 Python lines, 91 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_toggle_chatter` — Web Toggle Chatter
- **Summary**: Toggle chatter in backend form views
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 26 Python lines, 15 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_touchscreen` — Web Touchscreen
- **Summary**: UX improvements for touch screens
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 20 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_tree_column_keyboard_resize` — Web Tree Column Keyboard Resize
- **Summary**: Allow resizing tree view columns using keyboard shortcuts
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 20 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_tree_dynamic_colored_field` — Colorize field in tree views
- **Summary**: Allows you to dynamically color fields on tree views
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 21 Python lines, 40 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_tree_many2one_clickable` — Clickable many2one fields for tree views
- **Summary**: Open the linked resource when clicking on their name
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 33 Python lines, 12 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_widget_char_size` — Widget Char size
- **Summary**: Add size option to Char widget
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 18 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_widget_domain_editor_dialog` — Web Widget Domain Editor Dialog
- **Summary**: Recovers the Domain Editor Dialog functionality
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 18 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_widget_dropdown_dynamic` — Dynamic Dropdown Widget
- **Summary**: This module adds support for dynamic dropdown widget
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 51 Python lines, 28 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_widget_image_download` — Web Widget - Image Download
- **Summary**: Allows to download any image from its widget
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 20 Python lines, 27 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_widget_numeric_step` — Web Widget Numeric Step
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 22 Python lines, 60 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_widget_o2m_attachment_image_gallery` — Widget o2m Attachment Image Gallery Widget
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 19 Python lines, 12 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_widget_one2many_tree_line_duplicate` — Web Widget One2many Tree Line Duplicate
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 25 Python lines, 69 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_widget_open_tab` — Widget Open on new Tab
- **Summary**: 
        Allow to open record from trees on new tab from tree views
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 83 Python lines, 37 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_widget_pattern` — Input patterns
- **Summary**: Allows to define a regex for validating input on the backend
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 88 Python lines, 23 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_widget_popover` — Web Widget Popover
- **Summary**: Render an icon that displays the field content in a popover
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 20 Python lines, 19 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_widget_product_label_section_and_note_full_label` — Web Widget Product Label Section And Note Full Label
- **Summary**: Display the full label in the product_label_section_and_note widget.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `account, web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 22 Python lines, 23 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_widget_product_label_section_and_note_name_visibility` — Web widget product label section and note
- **Summary**: Alternate the visibility of the product and description.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web, account`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 24 Python lines, 15 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_widget_url_advanced` — Web URL widget advanced
- **Summary**: This module extends URL widget for displaying anchors with custom labels.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 20 Python lines, 26 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `web_widget_x2many_2d_matrix` — 2D matrix for x2many fields
- **Summary**: Show list fields as a matrix
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 63 Python lines, 223 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---


### Suite I: Server Backend Utilities (`server-backend`)

**Total Modules in this Suite**: 14

#### `base_external_dbsource` — External Database Sources
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `base`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 628 Python lines, 88 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `base_external_system` — Base External System
- **Summary**: Data models allowing for connection to external systems.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `base`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 409 Python lines, 146 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `base_global_discount` — Base Global Discount
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `product`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 189 Python lines, 142 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `base_group_backend` — Group backend
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `base, mail, calendar`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 167 Python lines, 135 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `base_ical` — Readonly publishing of calendars
- **Summary**: Provide (readonly) .ics URLs to calendar-like models
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 678 Python lines, 214 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `base_import_match` — Base Import Match
- **Summary**: Try to avoid duplicates before importing
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `base_import`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 400 Python lines, 157 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `base_portal_type` — Portal types
- **Summary**: Base module to allow different types of portals
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `portal`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 125 Python lines, 17 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `base_user_effective_permissions` — Effective permissions
- **Summary**: Inspect effective permissions applying to a user
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `base`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 132 Python lines, 75 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `base_user_role` — User roles
- **Summary**: No summary provided.
- **Removal Safety**: 🔴 Core Dependency: 3 Modules Depend on It
- **Removal Impact**: Critical foundation module. Removing it will disable 3 other modules.
- **Dependencies (Requires)**: `base`
- **Dependents (Required By)**: `base_user_role_company, base_user_role_history, base_user_role_profile`
- **Codebase Size**: 1034 Python lines, 339 XML lines
- **Customization Complexity**: **High (Tier 3)** | **Effort**: 2 – 5 Days | **Estimated Cost**: $1,000 – $3,500

---

#### `base_user_role_company` — User roles by company
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `base_user_role`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 297 Python lines, 38 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `base_user_role_history` — Base User Role History
- **Summary**: 
        This module allows to track the changes on users roles.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mail, base_user_role`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 496 Python lines, 135 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `base_user_role_profile` — User profiles
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `base_user_role, web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 367 Python lines, 187 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `server_action_navigate` — Server Actions - Navigate
- **Summary**: Navigate between any items of any Odoo Models
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `base_automation`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 227 Python lines, 66 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `server_action_sort` — Server Actions - Mass Sort Lines
- **Summary**: Sort any lines of any models by any criterias
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `base`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 149 Python lines, 78 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---


### Suite J: Server Tools & Management (`server-tools`)

**Total Modules in this Suite**: 46

#### `attachment_delete_restrict` — Restrict Deletion of Attachments
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `base, base_setup`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 461 Python lines, 127 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `attachment_unindex_content` — Attachment Unindex Content
- **Summary**: Disable indexing of attachments
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `base`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 39 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `auditlog` — Audit Log
- **Summary**: No summary provided.
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (test_auditlog)
- **Removal Impact**: If you remove this, you must also remove: test_auditlog.
- **Dependencies (Requires)**: `base`
- **Dependents (Required By)**: `test_auditlog`
- **Codebase Size**: 2148 Python lines, 580 XML lines
- **Customization Complexity**: **High (Tier 3)** | **Effort**: 2 – 5 Days | **Estimated Cost**: $1,000 – $3,500

---

#### `autovacuum_message_attachment` — AutoVacuum Mail Message and Attachment
- **Summary**: Automatically delete old mail messages and attachments
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mail`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 487 Python lines, 103 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `base_conditional_image` — Conditional Images
- **Summary**: This module extends the functionality to support conditional images
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `base`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 117 Python lines, 60 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `base_cron_exclusion` — Base Cron Exclusion
- **Summary**: Allow you to select scheduled actions that should not run simultaneously.
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (ddmrp)
- **Removal Impact**: If you remove this, you must also remove: ddmrp.
- **Dependencies (Requires)**: `base`
- **Dependents (Required By)**: `ddmrp`
- **Codebase Size**: 142 Python lines, 21 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `base_exception` — Exception Rule
- **Summary**: 
    This module provide an abstract model to manage customizable
    exceptions to be applied on different models (sale order, invoice, ...)
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `base_setup`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 935 Python lines, 158 XML lines
- **Customization Complexity**: **High (Tier 3)** | **Effort**: 2 – 5 Days | **Estimated Cost**: $1,000 – $3,500

---

#### `base_fontawesome` — Base Fontawesome
- **Summary**: Up to date Fontawesome resources.
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (base_fontawesome_web_editor)
- **Removal Impact**: If you remove this, you must also remove: base_fontawesome_web_editor.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `base_fontawesome_web_editor`
- **Codebase Size**: 42 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `base_fontawesome_web_editor` — Base Fontawesome Web Editor
- **Summary**: Integration between base_fontawesome and web_editor for FontAwesome >= 6.7.2 support.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web_editor, base_fontawesome`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 25 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `base_force_record_noupdate` — Force Record No-update
- **Summary**: Manually force noupdate=True on models
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `base`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 184 Python lines, 23 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `base_m2m_custom_field` — Base Many2many Custom Field
- **Summary**: Customizations of Many2many
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `base`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 35 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `base_model_restrict_update` — Update Restrict Model
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `base_setup`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 249 Python lines, 69 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `base_multi_image` — Multiple images base
- **Summary**: Allow multiple images for database objects
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (stock_lot_multi_image)
- **Removal Impact**: If you remove this, you must also remove: stock_lot_multi_image.
- **Dependencies (Requires)**: `base`
- **Dependents (Required By)**: `stock_lot_multi_image`
- **Codebase Size**: 739 Python lines, 160 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `base_name_search_improved` — Improved Name Search
- **Summary**: Friendlier search when typing in relation fields
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `base`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 465 Python lines, 165 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `base_partition` — Base Partition
- **Summary**: Base module that provide the partition method on all models
- **Removal Safety**: 🟡 Caution: 2 Dependent Modules (stock_location_fill_state, stock_orderpoint_default_location)
- **Removal Impact**: If you remove this, you must also remove: stock_location_fill_state, stock_orderpoint_default_location.
- **Dependencies (Requires)**: `base`
- **Dependents (Required By)**: `stock_location_fill_state, stock_orderpoint_default_location`
- **Codebase Size**: 218 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `base_remote` — Remote Base
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 203 Python lines, 48 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `base_search_fuzzy` — Fuzzy Search
- **Summary**: Fuzzy search with the PostgreSQL trigram extension
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `base`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 351 Python lines, 77 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `base_sparse_field_list_support` — Base Sparse Field List Support
- **Summary**: add list support to convert_to_cache()
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `base, base_sparse_field`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 31 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `base_technical_user` — Base Technical User
- **Summary**: 
        Add a technical user parameter on the company 
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `base`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 151 Python lines, 24 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `base_temporary_action` — Base Temporary Action
- **Summary**: This addon allows to create temporary actions
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `base`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 73 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `base_time_parameter` — Time Parameter
- **Summary**: 
        Time dependent parameters
        Adds the feature to define parameters
        with time based versions.
    
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `base`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 440 Python lines, 177 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `base_time_window` — Base Time Window
- **Summary**: Base model to handle time windows
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (test_base_time_window)
- **Removal Impact**: If you remove this, you must also remove: test_base_time_window.
- **Dependencies (Requires)**: `base`
- **Dependents (Required By)**: `test_base_time_window`
- **Codebase Size**: 412 Python lines, 40 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `base_view_inheritance_extension` — Extended view inheritance
- **Summary**: Adds more operators for view inheritance
- **Removal Safety**: 🔴 Core Dependency: 3 Modules Depend on It
- **Removal Impact**: Critical foundation module. Removing it will disable 3 other modules.
- **Dependencies (Requires)**: `base`
- **Dependents (Required By)**: `stock_inventory_preparation_filter, stock_picking_product_availability_inline, web_m2x_options_manager`
- **Codebase Size**: 416 Python lines, 29 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `bus_alt_connection` — Bus Alt Connection
- **Summary**: Needed when using PgBouncer as a connection pooler
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `bus`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 223 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `database_autovacuum_tuning` — Database Autovacuum Tuning
- **Summary**: Scheduled checks for Odoo autovacuum thresholds and scale factors
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `base_setup`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 163 Python lines, 104 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `database_cleanup` — Database cleanup
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `base`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 1405 Python lines, 515 XML lines
- **Customization Complexity**: **High (Tier 3)** | **Effort**: 2 – 5 Days | **Estimated Cost**: $1,000 – $3,500

---

#### `database_size` — Database Size
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `base_setup`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 867 Python lines, 249 XML lines
- **Customization Complexity**: **High (Tier 3)** | **Effort**: 2 – 5 Days | **Estimated Cost**: $1,000 – $3,500

---

#### `dbfilter_from_header` — dbfilter_from_header
- **Summary**: Filter databases with HTTP headers
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 47 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `excel_import_export` — Excel Import/Export/Report
- **Summary**: Base module for developing Excel import/export/report
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mail`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 2250 Python lines, 614 XML lines
- **Customization Complexity**: **High (Tier 3)** | **Effort**: 2 – 5 Days | **Estimated Cost**: $1,000 – $3,500

---

#### `fetchmail_attach_from_folder` — Email gateway - folders
- **Summary**: Attach mails in an IMAP folder to existing objects
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mail`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 1202 Python lines, 177 XML lines
- **Customization Complexity**: **High (Tier 3)** | **Effort**: 2 – 5 Days | **Estimated Cost**: $1,000 – $3,500

---

#### `fetchmail_notify_error_to_sender` — Fetchmail Notify Error to Sender
- **Summary**: If fetching mails gives error, send an email to sender
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mail`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 177 Python lines, 52 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `html_text` — Text from HTML field
- **Summary**: Generate excerpts from any HTML field
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `base`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 158 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `iap_alternative_provider` — IAP Alternative Provider
- **Summary**: Base module for providing alternative provider for iap apps
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `iap`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 132 Python lines, 23 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `jsonifier` — JSONifier
- **Summary**: JSON-ify data for all models
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `base`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 1151 Python lines, 83 XML lines
- **Customization Complexity**: **High (Tier 3)** | **Effort**: 2 – 5 Days | **Estimated Cost**: $1,000 – $3,500

---

#### `mail_template_attachment_per_lang` — Mail Template Language Specific Attachments
- **Summary**: Set language specific attachments on mail templates.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mail`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 330 Python lines, 35 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `module_auto_update` — Module Auto Update
- **Summary**: Automatically update Odoo modules
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `base`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 601 Python lines, 55 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `module_change_auto_install` — Change auto installable modules
- **Summary**: Customize auto installables modules by configuration
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `base`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 154 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `onchange_helper` — Onchange Helper
- **Summary**: Technical module that ease execution of onchange in Python code
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `web`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 129 Python lines, 0 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `rpc_helper` — Disable RPC
- **Summary**: Helpers for disabling RPC calls
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `base_sparse_field`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 271 Python lines, 23 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `scheduler_error_mailer` — Scheduler Error Mailer
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `mail`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 165 Python lines, 86 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `sequence_python` — Sequence from Python expression
- **Summary**: Calculate a sequence number from a Python expression
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `base`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 144 Python lines, 52 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

#### `session_db` — Store sessions in DB
- **Summary**: No summary provided.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `None`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 368 Python lines, 0 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `test_auditlog` — Audit Log Tests
- **Summary**: Additional unit tests for Audit Log based on accounting models
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `account, auditlog`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 326 Python lines, 0 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `test_base_time_window` — Test Base Time Window
- **Summary**: Test Base model to handle time windows
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `base_time_window`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 318 Python lines, 23 XML lines
- **Customization Complexity**: **Medium (Tier 2)** | **Effort**: 4 – 16 Hours | **Estimated Cost**: $250 – $1,000

---

#### `tracking_manager` — Tracking Manager
- **Summary**: This module tracks all fields of a model,
                including one2many and many2many ones.
- **Removal Safety**: 🟡 Caution: 1 Dependent Modules (tracking_manager_domain)
- **Removal Impact**: If you remove this, you must also remove: tracking_manager_domain.
- **Dependencies (Requires)**: `mail`
- **Dependents (Required By)**: `tracking_manager_domain`
- **Codebase Size**: 1029 Python lines, 172 XML lines
- **Customization Complexity**: **High (Tier 3)** | **Effort**: 2 – 5 Days | **Estimated Cost**: $1,000 – $3,500

---

#### `tracking_manager_domain` — Tracking Manager Domain
- **Summary**: This module extends the tracking manager to allow to define a domain on fields to track changes only when certain conditions apply.
- **Removal Safety**: 🟢 Safe to Remove (Zero other modules depend on it)
- **Removal Impact**: None. Removing this module will not break any other addon in the system.
- **Dependencies (Requires)**: `tracking_manager`
- **Dependents (Required By)**: `None`
- **Codebase Size**: 231 Python lines, 21 XML lines
- **Customization Complexity**: **Low (Tier 1)** | **Effort**: 1 – 4 Hours | **Estimated Cost**: $50 – $250

---

