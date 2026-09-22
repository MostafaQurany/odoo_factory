# Factory Platform — Production Hardening & Tuning Guide

---

## 1. Odoo Worker Allocation Formula
In production, Odoo must run in multiprocess mode with gevent longpolling:
```text
Workers = (2 * CPU Cores) + 1
Cron Workers = 2 (for Queue Job & scheduled maintenance)
```
Example for an 8-core server:
- `workers = 17`
- `max_cron_threads = 2`

---

## 2. Memory & Limit Tuning (`odoo.conf`)
```ini
[options]
proxy_mode = True
limit_memory_hard = 2684354560
limit_memory_soft = 2147483648
limit_request = 8192
limit_time_cpu = 600
limit_time_real = 1200
```

---

## 3. Reverse Proxy (Nginx) & SSL Termination
- Terminate SSL at the reverse proxy (Nginx or Traefik).
- Set `X-Forwarded-Proto https` and `X-Forwarded-Host`.
- Configure buffer sizes to accommodate large batch imports and multi-page engineering BOM documents.

---

## 4. PostgreSQL Tuning (`postgresql.conf`)
For dedicated 16GB RAM production database server:
- `shared_buffers = 4GB`
- `effective_cache_size = 12GB`
- `work_mem = 64MB`
- `maintenance_work_mem = 1GB`
- `wal_buffers = 16MB`
