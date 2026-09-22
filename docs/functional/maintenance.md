# Factory Maintenance & Equipment Downtime — Functional Guide

**Technical Module**: `custom/factory_maintenance`  
**Odoo Core Depends**: `base`, `mrp`, `barcodes`  
**Capability**: `maintenance`  
**Profile**: `operations`, `advanced`, `full`  

---

## 1. Overview
The Factory Maintenance module connects plant equipment assets directly to manufacturing work centers. It tracks preventive scheduled service and emergency repairs, automatically reflecting machine breakdowns into work center capacity and downtime logs.

---

## 2. Equipment Asset Registry
Machines and tools are cataloged with:
- **Asset Code & Name**: Unique tag (e.g. `EQ-CNC-001`).
- **Scan Barcode**: Scannable for mobile shop floor asset identification.
- **Assigned Work Center**: Links the physical machine to the scheduling work center.
- **Technical Specs**: Manufacturer, model, serial number, commissioning date, and warranty expiration.

---

## 3. Maintenance Requests & Operational Downtime
- **Classification**: Scheduled Preventive vs. Unscheduled Emergency Corrective.
- **Downtime Hours**: Logs the exact duration the machine was out of service.
- **Root Cause Analysis**: Mechanical wear, electrical/motor failure, sensor failure, hydraulic pressure loss, or tooling failure.
- **Work Center Synchronization**: Starting a repair automatically sets the associated work center status to `Down for Maintenance`, preventing dispatchers from scheduling manufacturing orders on broken equipment until repaired.
