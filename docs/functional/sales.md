# Factory Sales & Demand Orchestration — Functional Guide

**Technical Module**: `custom/factory_sale`  
**Odoo Core Depends**: `sale_management`, `sale_stock`  
**Capability**: `sales`  
**Profile**: `core`, `operations`, `advanced`, `full`  

---

## 1. Overview
The Factory Sales module orchestrates industrial customer demand into concrete shop-floor fulfillment strategies, supporting both Make-to-Stock (MTS) and Make-to-Order (MTO) manufacturing, customer delivery tolerances, and direct linkage from sales lines to manufacturing orders.

---

## 2. Industrial Fulfillment Strategies
Every quotation and sales order (`sale.order`) specifies an fulfillment strategy:
- **Make to Stock (MTS)**: Order is reserved and fulfilled directly from certified `finished_goods` warehouse stock.
- **Make to Order (MTO)**: Order confirmation triggers demand procurement directly generating a corresponding `mrp.production` order. The sales form provides a smart button showing the live status of all linked manufacturing orders.

---

## 3. Customer Delivery Tolerances & Tiers
- **Delivery Tolerance (Days)**: Specifies agreed flexibility in ship dates without incurring contract penalties.
- **Customer Tiers**: Categorizes clients into Key Industrial Accounts, OEM Partners, Wholesale Distributors, and Standard Clients.
