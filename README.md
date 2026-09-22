# Odoo Factory ERP Platform V1 (Enterprise Industrial Edition)

[![CI Quality Gate](https://img.shields.io/badge/CI%20Gate-Passing-brightgreen.svg)](scripts/ci_gate.py)
[![Odoo Version](https://img.shields.io/badge/Odoo-18.0%20Community-purple.svg)](https://www.odoo.com/)
[![Architecture](https://img.shields.io/badge/Architecture-Clean%20Decoupled%20Vendor%2FCustom-blue.svg)](docs/architecture/overview.md)
[![Localization](https://img.shields.io/badge/Localization-Egypt%20(EGP%20%2F%20ETA)-green.svg)](docs/functional/accounting.md)

An end-to-end, multi-pillar, modular Factory ERP framework built on top of **Odoo 18 Community** and verified **OCA (Odoo Community Association)** repositories. Engineered for industrial production across assembly, garment, chemical, metalworking, and general discrete manufacturing.

---

## 1. Architectural Principles

1. **Strict Vendor Immutability**: All vendor/OCA repositories reside under `addons/*` and are strictly **READ-ONLY**. No custom code touches vendor paths.
2. **Flat Custom Modules**: All factory domain logic, integrations, and extensions live in flat directories under `custom/*` (`custom/factory_*`).
3. **Declarative Metadata Engine**: Profiles, capabilities, and dependencies are orchestrated via declarative YAML definitions under `.factory/` (`capabilities.yml`, `install_profiles.yml`, `module_policy.yml`).
4. **Decoupled Docker Runtime**: Docker boots a clean Odoo runtime container without hardcoded auto-installation of business modules; database installation and migrations are executed dynamically via declarative profiles.
5. **Standard-First Philosophy**: Maximum reuse of tested OCA modules (`stock_no_negative`, `scrap_reason_code`, `mrp_workcenter_scrap_reason`, `quality_control_oca`, `queue_job`, `partner_firstname`, etc.) with zero unnecessary code bloat.

---

## 2. Core Custom Modules (`custom/`)

| Module | Technical Name | Primary Industrial Responsibilities |
|---|---|---|
| **Factory Security** | `factory_security` | 12 segregated industrial roles, approval matrix, multi-company rules. |
| **Factory Inventory** | `factory_inventory` | 10 warehouse location types, supplier lot tracking, negative inventory block. |
| **Factory Purchase** | `factory_purchase` | Industrial procurement categories, supplier MOQ check, tiered approval limit. |
| **Factory MRP** | `factory_mrp` | 3-pillar work center costing (machine/labor/overhead), shift logs, BOM revision control. |
| **Factory Quality** | `factory_quality` | 4 inspection gates (Inbound, WIP, FG, Returns), controlled rework orders (`factory.rework.order`), scrap auditing. |
| **Factory Sales** | `factory_sale` | MTS/MTO demand orchestration, linked MO visibility, customer delivery tolerance. |
| **Factory Accounting**| `factory_accounting` | Manufacturing cost absorption breakdown, material/duration variance, Egyptian VAT & currency (`EGP`). |
| **Factory Maintenance**| `factory_maintenance` | Equipment register, corrective/preventive requests, automatic workcenter downtime lock. |
| **Factory Reports** | `factory_reports` | 16 industrial QWeb PDF reports (Traveler, BOM, Picking, Scrap, Rework, QC, Traceability, Valuation, Costing). |
| **Factory Demo** | `factory_demo` | Master industrial test fixtures, vendor/customer partners, end-to-end golden scenario tests. |

---

## 3. Installation Profiles (`.factory/install_profiles.yml`)

The platform defines 4 progressive installation tiers:

- **`core` (`factory_profile_core`)**: Base ERP setup (Contacts, Invoicing, Base Manufacturing, Base Inventory).
- **`operations` (`factory_profile_operations`)**: Standard factory stack (MRP, Purchases, Stock, Quality Control, Maintenance).
- **`advanced` (`factory_profile_advanced`)**: Full industrial platform (Multi-pillar MRP costing, Scrap/Rework orchestration, Segregation of duties, 16 QWeb reports, Queue jobs).
- **`full` (`factory_profile_full`)**: Complete suite including all demo fixtures and golden scenario validation modules.

Generate and sync profile manifests dynamically:
```powershell
python scripts/factory/generate_profiles.py
```

---

## 4. Quick Start & Execution

### 1. Environment Configuration
Copy `.env.example` to `.env`:
```powershell
cp .env.example .env
```

### 2. Verify Architecture & Quality Gate
Run the automated pre-flight CI gate:
```powershell
python scripts/ci_gate.py
```

### 3. Build & Run Containers
Start the PostgreSQL and Odoo services:
```powershell
docker compose up -d
```
Access the web interface at: `http://localhost:8069` (Default master password in `.env`).

### 4. Bootstrap / Initialize a Profile
To initialize a database with a specific factory profile:
```powershell
python scripts/factory/bootstrap_db.py --profile operations --db factory_prod_db
```

---

## 5. Testing & Verification

### Run Declarative Verification Suite
Validate YAML schemas, manifest dependencies, acyclic graph, and profile completeness:
```powershell
python tests/test_platform.py
```

### Run End-to-End Golden Scenarios (Inside Odoo)
Execute all 14 end-to-end transactional industrial flows (GS-001 through GS-014 and GX-001 through GX-004):
```powershell
python scripts/run_tests.py --test-tags factory_demo
```

### User Acceptance Testing (UAT)
Refer to the step-by-step business checklist in [docs/operations/UAT.md](docs/operations/UAT.md).

---

## 6. Operations, Hardening & Backups

- **Disaster Recovery & Backups**: Automated PowerShell scripts with hash verification and retention pruning:
  - Backup: `powershell -File scripts/backup.ps1 -DatabaseName factory_prod_db`
  - Restore: `powershell -File scripts/restore.ps1 -BackupFile backups/factory_prod_db_YYYYMMDD.dump -TargetDatabase factory_test_db`
  - Detailed manual: [docs/operations/backup-restore.md](docs/operations/backup-restore.md)
- **Production Hardening**: Complete server, PostgreSQL, reverse proxy, and queue worker tuning guide: [docs/operations/production-hardening.md](docs/operations/production-hardening.md)
- **Queue Jobs**: Configuration of dedicated background job workers: [docs/operations/queue.md](docs/operations/queue.md)

---

## 7. Documentation Directory

- **Functional Guides**: [docs/functional/](docs/functional/) (`inventory.md`, `manufacturing.md`, `quality.md`, `purchase.md`, `sales.md`, `accounting.md`, `maintenance.md`).
- **Architecture**: [docs/architecture/](docs/architecture/) (`overview.md`, `security.md`, `profiles.md`).
- **Operations & Runbooks**: [docs/operations/](docs/operations/) (`backup-restore.md`, `production-hardening.md`, `queue.md`, `UAT.md`).
- **Implementation Status**: [docs/implementation/FACTORY_ERP_PROGRESS.md](docs/implementation/FACTORY_ERP_PROGRESS.md).
- **Engineering Skill**: [skills/odoo-factory-engineer/SKILL.md](skills/odoo-factory-engineer/SKILL.md).
