# Reference: Decoupled Docker Runtime Operations

## Container Topology
- `odoo_factory_system`: Odoo 18 Community runtime. Serves HTTP on port 8069.
- `odoo_factory_db`: PostgreSQL 16 server with automated healthcheck.

## Operational Commands
- **Start continuous runtime:**
  ```bash
  docker compose up -d
  ```
- **Idempotent bootstrap & install profile:**
  ```powershell
  ./scripts/bootstrap.ps1 -Profile core
  ./scripts/bootstrap.ps1 -Profile operations -Demo
  ```
- **Run module upgrade:**
  ```powershell
  ./scripts/bootstrap.ps1 -Update -Modules factory_base
  ```
- **Inspect container logs:**
  ```bash
  docker compose logs -f web
  ```
