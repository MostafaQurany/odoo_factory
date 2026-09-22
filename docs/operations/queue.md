# Factory Asynchronous Job Queue & Audit Logging — Production Guide

**Technical Addons**: `queue_job`, `queue_job_cron`  
**Capability**: `background_jobs`  
**Profile**: `operations`, `advanced`, `full`  

---

## 1. Overview
Heavy computational tasks in a manufacturing plant (mass stock revaluation, large BOM explosion, automatic replenishment runs, and legacy data imports) must run asynchronously in the background rather than blocking HTTP worker threads. The Factory Platform standardizes on OCA `queue_job` and cron-based dispatching.

---

## 2. Docker & Odoo Server Configuration
In production, Odoo must be booted with the `queue_job` server environment options in `odoo.conf`:

```ini
[options]
server_wide_modules = base,web,queue_job
limit_time_cpu = 600
limit_time_real = 1200
limit_memory_hard = 2684354560
limit_memory_soft = 2147483648

[queue_job]
channels = root:2,root.factory_mrp:1,root.factory_inventory:1
```

---

## 3. Dedicated Factory Channels
The platform defines specific queue channels:
1. `root.factory_inventory`: Mass inventory adjustments, stock quant recalculations.
2. `root.factory_mrp`: Multi-level BOM explosions and mass MO scheduling.
3. `root.reporting`: Heavy periodic production costing statements.

---

## 4. Failure Handling & Audit Visibility
- All failed jobs are logged in `queue.job` with complete Python tracebacks.
- Queue failures trigger notification chatter on the target manufacturing or inventory records.
- Dead letter jobs can be retried or requeued with single-click manual or scheduled retry policies.
