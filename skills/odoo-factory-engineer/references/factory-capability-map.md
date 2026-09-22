# Reference: Factory Capability Map

Maps human business requirements to technical Odoo capability identifiers:

| Business Need | Capability Identifier | Core Modules | Target Profile |
|---------------|-----------------------|--------------|----------------|
| Quality Inspection Gates | `manufacturing_quality` | `quality_control_oca`, `quality_control_mrp_oca` | `operations` |
| Scrap Reason Tracking | `scrap_management` | `scrap_reason_code`, `mrp_workcenter_scrap_reason` | `operations` |
| Asynchronous Queues | `background_jobs` | `queue_job`, `queue_job_cron` | `operations` |
| Demand Driven Planning | `ddmrp` | `ddmrp`, `ddmrp_history` | `advanced` |
| Multi-level BOM Versions | `advanced_bom` | `mrp_bom_hierarchy`, `mrp_bom_version` | `advanced` |
| Automated Orderpoints | `advanced_replenishment` | `stock_orderpoint_manual_procurement` | `advanced` |
| Core Sales Demand | `sales` | `sale_management`, `sale_stock` | `core` |
| Procurement Intake | `purchasing` | `purchase`, `purchase_stock` | `core` |
| Warehouse & Lots | `inventory` | `stock`, `stock_account` | `core` |
| Industrial Security | `security_baseline` | `factory_base` | `core` |
| Financial Accounting | `accounting` | `account`, `account_payment` | `core` |
