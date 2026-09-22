# Reference: Odoo Core Model Map

Key ERP models used across factory operations:

| Business Concept | Odoo Technical Model | Base Addon | Key Fields / Relations |
|------------------|----------------------|------------|------------------------|
| Product Template | `product.template` | `product` | `name`, `type`, `uom_id`, `categ_id` |
| Product Variant | `product.product` | `product` | `default_code`, `barcode`, `product_tmpl_id` |
| Bill of Materials | `mrp.bom` | `mrp` | `product_tmpl_id`, `product_qty`, `bom_line_ids` |
| BOM Line | `mrp.bom.line` | `mrp` | `product_id`, `product_qty`, `bom_id` |
| Manufacturing Order | `mrp.production` | `mrp` | `product_id`, `bom_id`, `workorder_ids`, `state` |
| Work Center | `mrp.workcenter` | `mrp` | `name`, `code`, `capacity`, `costs_hour` |
| Work Order | `mrp.workorder` | `mrp` | `production_id`, `workcenter_id`, `state` |
| Warehouse | `stock.warehouse` | `stock` | `name`, `code`, `view_location_id` |
| Stock Location | `stock.location` | `stock` | `name`, `usage`, `location_id` |
| Stock Picking | `stock.picking` | `stock` | `partner_id`, `picking_type_id`, `move_ids` |
| Stock Move | `stock.move` | `stock` | `product_id`, `product_uom_qty`, `location_dest_id` |
| Lot / Serial | `stock.lot` | `stock` | `name`, `product_id`, `company_id` |
| Sales Order | `sale.order` | `sale_management` | `partner_id`, `order_line`, `state` |
| Purchase Order | `purchase.order` | `purchase` | `partner_id`, `order_line`, `state` |
| Customer Invoice / Bill | `account.move` | `account` | `partner_id`, `move_type`, `invoice_line_ids` |
| Partner / Contact | `res.partner` | `base` | `name`, `is_company`, `customer_rank` |
| Quality Check | `quality.check` | `quality_control_oca`| `product_id`, `point_id`, `status` |
