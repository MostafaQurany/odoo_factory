# Odoo Factory Platform Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transform the monolithic Odoo 18 codebase into a modular, reusable Factory ERP Framework with decoupled runtime, declarative engine, automated validation, and an AI Agent operating skill.

**Architecture:** Approach 1.1 (Flat `custom/` addon root, read-only `addons/`, declarative `.factory/` engine with JSON schemas, decoupled Docker runtime/bootstrap/test, and an authoritative `odoo-factory-engineer` skill).

**Tech Stack:** Odoo 18.0 Community, Python 3.10+, PostgreSQL 16, Docker Compose, PowerShell / Bash, JSON Schema, YAML.

**Spec:** [docs/superpowers/specs/2026-09-22-odoo-factory-architecture-design.md](file:///e:/C/production%20projects/amgad/odoo_factory/docs/superpowers/specs/2026-09-22-odoo-factory-architecture-design.md)

## Global Constraints
- `addons/**` is vendor-owned and strictly READ-ONLY.
- `custom/**` is flat (no nested directories like `custom/profiles/`).
- Never rename module directory names during initial relocation (preserve `clothing_factory_demo` and `odoo_factory_all`).
- `.factory/install_profiles.yml` is the sole source of truth for profiles; manifests are generated or verified from it.
- All newly discovered modules start as `UNCLASSIFIED` and cannot enter production profiles.
- Dependency graph scanner must detect and report cycles.
- Every substantive change requires code, tests, docs, and metadata updates (Spec-Kit synchronization).

---

### Task 1: Architecture Skeleton Scaffolding (Phase 2)

**Files:**
- Create: `custom/.gitkeep`
- Create: `.factory/schemas/.gitkeep`
- Create: `.factory/generated/.gitkeep`
- Create: `skills/odoo-factory-engineer/.gitkeep`
- Create: `scripts/factory/.gitkeep`
- Create: `docs/architecture/adr/.gitkeep`
- Create: `docs/functional/.gitkeep`
- Create: `docs/development/.gitkeep`
- Create: `docs/operations/.gitkeep`

**Interfaces:**
- Produces: Base directory structure adhering to Approach 1.1 layout.

- [ ] **Step 1: Create target directory tree**
```powershell
New-Item -ItemType Directory -Force -Path custom, .factory/schemas, .factory/generated, skills/odoo-factory-engineer/references, skills/odoo-factory-engineer/workflows, skills/odoo-factory-engineer/scripts, scripts/factory, docs/architecture/adr, docs/functional, docs/development, docs/operations
```

- [ ] **Step 2: Verify directories exist**
```powershell
Test-Path custom, .factory/schemas, .factory/generated, skills/odoo-factory-engineer, scripts/factory, docs/architecture/adr
```

- [ ] **Step 3: Commit scaffolding**
```bash
git add custom .factory skills scripts docs
git commit -m "chore(arch): scaffold approach 1.1 directory skeleton"
```

---

### Task 2: Safe Legacy Relocation (Phase 3)

**Files:**
- Move: `addons/manufacture/clothing_factory_demo` -> `custom/clothing_factory_demo`
- Move: `addons/server-tools/odoo_factory_all` -> `custom/odoo_factory_all`

**Interfaces:**
- Consumes: Existing custom modules in vendor tree.
- Produces: Relocated modules in `custom/` preserving exact technical names and git history.

- [ ] **Step 1: Verify source paths exist before moving**
```powershell
Test-Path addons/manufacture/clothing_factory_demo; Test-Path addons/server-tools/odoo_factory_all
```

- [ ] **Step 2: Relocate modules via git mv**
```bash
git mv addons/manufacture/clothing_factory_demo custom/clothing_factory_demo
git mv addons/server-tools/odoo_factory_all custom/odoo_factory_all
```

- [ ] **Step 3: Verify git status reflects pure renames**
```bash
git status --short
```
Expected: `R  addons/manufacture/clothing_factory_demo -> custom/clothing_factory_demo` and `R  addons/server-tools/odoo_factory_all -> custom/odoo_factory_all`.

- [ ] **Step 4: Commit relocation**
```bash
git commit -m "refactor(modules): relocate custom modules from vendor trees to custom/ preserving technical names"
```

---

### Task 3: Docker Runtime Decoupling & Environment Setup (Phase 4)

**Files:**
- Create: `.env.example`
- Modify: `.gitignore`
- Modify: `docker-compose.yml`
- Create: `scripts/bootstrap.ps1`
- Create: `scripts/bootstrap.sh`
- Create: `scripts/test.ps1`
- Create: `scripts/test.sh`

**Interfaces:**
- Produces: Decoupled Docker runtime (no `-i` flag) with database healthcheck, mounted `./custom`, and dedicated bootstrap/test scripts.

- [ ] **Step 1: Create `.env.example`**
```bash
# PostgreSQL Configuration
POSTGRES_DB=postgres
POSTGRES_USER=odoo
POSTGRES_PASSWORD=odoo
PGDATA=/var/lib/postgresql/data/pgdata

# Odoo Runtime Configuration
ODOO_DB=odoo
ODOO_ADMIN_PASSWD=admin
QUEUE_JOB_CHANNELS=root:4

# Factory Localization
FACTORY_COUNTRY=EG
FACTORY_CURRENCY=EGP
FACTORY_CHART_TEMPLATE=eg
```

- [ ] **Step 2: Ensure `.env` is gitignored**
Verify `.gitignore` contains `.env`.

- [ ] **Step 3: Update `docker-compose.yml`**
Add:
- PostgreSQL service healthcheck (`pg_isready -U odoo -d postgres`)
- `depends_on: db: condition: service_healthy`
- Volume: `./custom:/mnt/custom-addons`
- Updated addons-path containing `/mnt/custom-addons`
- Clean runtime command: `odoo --load=base,web,queue_job -d ${ODOO_DB:-odoo}` (no `-i` flags)

- [ ] **Step 4: Create `scripts/bootstrap.ps1` and `scripts/bootstrap.sh`**
Implement idempotent bootstrap runner executing:
`docker compose run --rm web odoo -d $DbName -i $Modules --stop-after-init`

- [ ] **Step 5: Create `scripts/test.ps1` and `scripts/test.sh`**
Implement isolated test runner with disposable DB `odoo_test_<timestamp>` and `--test-enable`.

- [ ] **Step 6: Validate `docker compose config`**
```powershell
docker compose config
```
Expected: Valid YAML output without syntax errors.

- [ ] **Step 7: Commit Docker changes**
```bash
git add .env.example .gitignore docker-compose.yml scripts/
git commit -m "feat(docker): decouple runtime from bootstrap/testing and add environment configuration"
```

---

### Task 4: Module Discovery Engine & Dependency Graph (Phase 5)

**Files:**
- Create: `scripts/factory/scan_modules.py`
- Create: `scripts/factory/build_graph.py`
- Produces: `.factory/generated/module_catalog.json`
- Produces: `.factory/generated/dependency_graph.json`
- Produces: `.factory/generated/repository_catalog.json`

**Interfaces:**
- Produces: Fully populated module catalog with technical name, repository, license, dependencies, ownership, and cycle-detected graph.

- [ ] **Step 1: Write test for manifest parser and cycle detector**
Create `tests/test_scanner.py` verifying AST extraction of manifests and cycle detection on sample graphs.

- [ ] **Step 2: Run test to verify it fails**
```powershell
python -m unittest tests/test_scanner.py
```

- [ ] **Step 3: Implement `scripts/factory/scan_modules.py`**
AST-safe parser reading all `__manifest__.py` files across `addons/` and `custom/`. Extract fields:
- `technical_name`, `display_name`, `repository`, `path`, `version`, `license`, `category`, `summary`, `depends`, `auto_install`, `installable`, `application`, `external_dependencies`, `ownership` (`vendor` vs `custom`), `classification` (`UNCLASSIFIED` by default).

- [ ] **Step 4: Implement `scripts/factory/build_graph.py`**
Construct directed graph, detect cycles, find missing or unavailable dependencies, and output `dependency_graph.json`.

- [ ] **Step 5: Run scanner and tests**
```powershell
python scripts/factory/scan_modules.py
python scripts/factory/build_graph.py
python -m unittest tests/test_scanner.py
```
Expected: PASS, `.factory/generated/module_catalog.json` and `dependency_graph.json` generated.

- [ ] **Step 6: Commit scanner and generated metadata**
```bash
git add scripts/factory/ tests/ .factory/generated/
git commit -m "feat(engine): add automated module scanner and dependency graph generator with cycle detection"
```

---

### Task 5: Contract Schemas & Declarative Metadata Engine (Phase 6 - Phase 8)

**Files:**
- Create: `.factory/schemas/project.schema.json`
- Create: `.factory/schemas/capabilities.schema.json`
- Create: `.factory/schemas/module_policy.schema.json`
- Create: `.factory/schemas/install_profiles.schema.json`
- Create: `.factory/schemas/golden_scenario.schema.json`
- Create: `.factory/schemas/health_checks.schema.json`
- Create: `scripts/factory/validate_schemas.py`
- Create: `.factory/project.yml`
- Create: `.factory/module_policy.yml`
- Create: `.factory/capabilities.yml`
- Create: `.factory/install_profiles.yml`
- Create: `.factory/golden_scenario.yml`
- Create: `.factory/health_checks.yml`
- Create: `scripts/factory/generate_profiles.py`

**Interfaces:**
- Consumes: Generated module catalog.
- Produces: Validated YAML contracts and generator for `custom/factory_profile_*` manifests.

- [ ] **Step 1: Write JSON schemas in `.factory/schemas/`**
Define schemas with strict typing, required fields, and disallowed additional properties where appropriate.

- [ ] **Step 2: Implement `scripts/factory/validate_schemas.py`**
Validate all `.factory/*.yml` against their corresponding `.factory/schemas/*.schema.json`.

- [ ] **Step 3: Create `.factory/project.yml`**
Specify project metadata, Odoo version (18.0), edition (community), localization (country, currency, chart), and strict policies.

- [ ] **Step 4: Create `.factory/module_policy.yml`**
Classify modules (`CORE`, `OPERATIONS`, `ADVANCED`, `INFRASTRUCTURE`, `INTEGRATION`, `UI`, `DEV`, `TEST`, `HARDWARE`, `LEGACY`, `UNCLASSIFIED`). Ensure `test_*` are `TEST` and lifts/VLMs are `HARDWARE`.

- [ ] **Step 5: Create `.factory/capabilities.yml`**
Define explicit capabilities (`sales`, `purchasing`, `inventory`, `manufacturing`, `manufacturing_quality`, `scrap_management`, `background_jobs`, `ddmrp`, `localization`, etc.) with `requires`, `modules` (required/optional), `conflicts`, `profiles`, and `tests`.

- [ ] **Step 6: Create `.factory/install_profiles.yml`**
Authoritative profile definition: `core`, `operations`, `advanced`, `full`.

- [ ] **Step 7: Implement `scripts/factory/generate_profiles.py`**
Generate or verify `custom/factory_profile_core`, `factory_profile_operations`, etc., directly from `.factory/install_profiles.yml`.

- [ ] **Step 8: Validate all schemas**
```powershell
python scripts/factory/validate_schemas.py
```
Expected: All schemas pass validation without errors.

- [ ] **Step 9: Commit declarative engine contracts**
```bash
git add .factory/ scripts/factory/
git commit -m "feat(contracts): add json schemas, declarative yaml policies, and profile generator"
```

---

### Task 6: CI Quality Gate Automation (Phase 9)

**Files:**
- Create: `scripts/ci_gate.py`
- Create: `tests/test_ci_gate.py`

**Interfaces:**
- Consumes: Git tree, `.factory/`, manifests, and schemas.
- Produces: Single gate script validating vendor integrity, schema conformity, catalog sync, policy compliance, and test exclusion.

- [ ] **Step 1: Implement `scripts/ci_gate.py`**
Verify:
1. Vendor code integrity (`addons/**` unchanged relative to upstream baseline).
2. Schema validation passes for all `.factory/*.yml`.
3. Generated catalog and dependency graph are up to date.
4. No `TEST` modules in production profiles (`install_profiles.yml`).
5. No `HARDWARE` or `UNCLASSIFIED` modules in production profiles without explicit review.
6. Manifest validity for all custom addons.

- [ ] **Step 2: Run CI gate locally**
```powershell
python scripts/ci_gate.py
```
Expected: All checks PASS.

- [ ] **Step 3: Commit CI quality gate**
```bash
git add scripts/ci_gate.py tests/
git commit -m "feat(ci): add automated quality gate script for metadata, vendor integrity, and profile validation"
```

---

### Task 7: Factory Core V1 Profile & Meta-Addons (Phase 10)

**Files:**
- Create: `custom/factory_base/` (`__init__.py`, `__manifest__.py`, `models/`, `views/`, `security/`)
- Create: `custom/factory_profile_core/` (`__manifest__.py`)
- Create: `custom/factory_profile_operations/` (`__manifest__.py`)
- Create: `custom/factory_profile_advanced/` (`__manifest__.py`)
- Create: `custom/factory_profile_full/` (`__manifest__.py`)

**Interfaces:**
- Consumes: Generated manifests from `.factory/install_profiles.yml`.
- Produces: Production-ready core factory meta-addons and foundational module.

- [ ] **Step 1: Generate profile meta-addons**
```powershell
python scripts/factory/generate_profiles.py
```

- [ ] **Step 2: Create `custom/factory_base`**
Add company settings, industrial dashboard entry points, factory menus, and security groups baseline (`security/factory_security.xml`).

- [ ] **Step 3: Run CI Gate to verify profile correctness**
```powershell
python scripts/ci_gate.py
```
Expected: PASS.

- [ ] **Step 4: Commit Core meta-addons**
```bash
git add custom/factory_base custom/factory_profile_*
git commit -m "feat(core): implement factory_base and generate profile meta-addons from install_profiles.yml"
```

---

### Task 8: Generic Universal Demo & Golden Scenarios (Phase 11 - Phase 13)

**Files:**
- Create: `custom/factory_demo/` (`__init__.py`, `__manifest__.py`, `data/`)
  - `data/products_data.xml` (`RM-001`, `RM-002`, `COMP-001`, `PKG-001`, `FG-001`)
  - `data/workcenters_data.xml` (`WC-CUTTING`, `WC-WELDING`, `WC-ASSEMBLY`, `WC-QUALITY`, `WC-PACKING`)
  - `data/routing_bom_data.xml`
  - `data/accounting_fixture.xml`
- Create: `.factory/golden_scenario.yml` (GS-001 to GS-014 and GX-001 to GX-004)
- Create: `scripts/factory/run_scenario.py`

**Interfaces:**
- Consumes: Factory profiles and generic demo data.
- Produces: Executable verification harness for transactional and cross-cutting scenario suites.

- [ ] **Step 1: Create generic demo data in `custom/factory_demo`**
Build domain-neutral master data for raw materials, subassemblies, finished goods, and work centers.

- [ ] **Step 2: Define `.factory/golden_scenario.yml`**
Detail steps, expected inputs, assertions, and impacted modules for GS-001..GS-014 and GX-001..GX-004.

- [ ] **Step 3: Implement `scripts/factory/run_scenario.py`**
Scenario runner that maps scenario codes to Odoo test executions and produces a health report.

- [ ] **Step 4: Validate scenario definitions against schema**
```powershell
python scripts/factory/validate_schemas.py
```
Expected: PASS.

- [ ] **Step 5: Commit generic demo and scenario harness**
```bash
git add custom/factory_demo .factory/golden_scenario.yml scripts/factory/run_scenario.py
git commit -m "feat(demo): add generic universal factory demo data and golden scenario execution harness"
```

---

### Task 9: AI Agent Operating Skill Deployment (Phase 14)

**Files:**
- Create: `skills/odoo-factory-engineer/SKILL.md`
- Create: `skills/odoo-factory-engineer/references/` (9 reference guides)
- Create: `skills/odoo-factory-engineer/workflows/` (13 operational workflows)
- Create: `skills/odoo-factory-engineer/scripts/agent_helper.py`
- Create: `docs/architecture/adr/ADR-001-to-006.md`

**Interfaces:**
- Consumes: All `.factory/` contracts, directories, and tooling.
- Produces: Complete, self-contained AI Agent operating capability.

- [ ] **Step 1: Create `SKILL.md`**
Adhere strictly to `writing-skills` standards:
- YAML frontmatter with `name: odoo-factory-engineer`
- Description starting with "Use when..." describing triggering symptoms (modifying models, views, reports, security, workflows in `odoo_factory`), with ZERO workflow process leakage.
- Overview, Core Principles, Discovery Workflow, and Error Counters.

- [ ] **Step 2: Create reference guides in `references/`**
- `architecture.md`: Ownership boundaries (`addons/` vs `custom/`).
- `odoo-model-map.md`: Core ERP models cheat sheet.
- `factory-capability-map.md`: Capabilities and profiles navigation.
- `reporting.md`: QWeb inheritance and PDF generation.
- `security.md`: ACLs, record rules, groups.
- `migrations.md`: Non-breaking vs schema migrations, zero SQL surgery.
- `testing.md`: Running disposable tests and scenario impact analysis.
- `docker-runtime.md`: Decoupled container operations.
- `troubleshooting.md`: Common traps (cache, missing XML IDs, duplicate keys).

- [ ] **Step 3: Create operational workflows in `workflows/`**
- `inspect-requirement.md`, `enable-capability.md`, `disable-capability.md`, `add-field.md`, `modify-view.md`, `modify-report.md`, `modify-security.md`, `create-module.md`, `upgrade-module.md`, `migrate-module.md`, `modify-integration.md`, `debug.md`, `release-check.md`.

- [ ] **Step 4: Create `agent_helper.py`**
CLI utility allowing agents to query module metadata, check capabilities, and run impact checks with single commands.

- [ ] **Step 5: Author ADR-001 through ADR-006 in `docs/architecture/adr/`**
Document architectural decisions for vendor separation, declarative engine, profile source of truth, Docker decoupling, legacy migration, and agent boundaries.

- [ ] **Step 6: Run CI gate to ensure documentation and skill synchronization**
```powershell
python scripts/ci_gate.py
```
Expected: PASS.

- [ ] **Step 7: Commit Skill and ADRs**
```bash
git add skills/odoo-factory-engineer docs/architecture/adr/
git commit -m "feat(skill): deploy odoo-factory-engineer skill, workflows, references, helper scripts, and ADRs"
```

---

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-09-22-odoo-factory-platform.md`.

Two execution options:
1. **Subagent-Driven (recommended)** - Fresh subagent per task, review between tasks, fast iteration.
2. **Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints.
