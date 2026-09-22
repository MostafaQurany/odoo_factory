# Reference: Architecture & Ownership Boundaries

## The Ownership Contract

### 1. Vendor Code (`addons/**`)
- **Status:** Upstream OCA & vendor repositories.
- **Rule:** **STRICTLY READ-ONLY**.
- **Prohibition:** Never edit, format, or commit manual changes inside `addons/**`.
- **Inheritance:** If you need to extend an OCA model, create an inheriting model inside `custom/**`.

### 2. Project-Owned Code (`custom/**`)
- **Status:** All custom and proprietary modules.
- **Structure:** **Flat directory structure** (`custom/factory_*`).
- **Rule:** All new features, business models, views, and QWeb templates belong here.
- **Naming:** Follow standard Odoo naming (`factory_<domain>`).

### 3. Declarative Engine (`.factory/**`)
- **Generated (`.factory/generated/`):** Auto-generated machine facts. Do not hand-edit. Run `scripts/factory/scan_modules.py`.
- **Curated Contracts (`.factory/*.yml`):** Human-curated architecture policies, capabilities, profiles, and golden scenarios.
- **Schemas (`.factory/schemas/*.json`):** Strict JSON schemas validating all YAML contracts.

### 4. Deterministic Automation (`scripts/**`)
- Automated lifecycle runners for bootstrap, testing, CI gate, and scenario execution.
