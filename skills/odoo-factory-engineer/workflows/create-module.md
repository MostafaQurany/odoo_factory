# Workflow: Create Custom Module

1. **Target Directory:**
   - Must be created directly under `custom/<module_name>`.
   - Never nest directories inside `custom/`.
2. **Scaffold Structure:**
   ```text
   custom/factory_<name>/
   ├── __init__.py
   ├── __manifest__.py
   ├── models/
   ├── views/
   ├── security/
   │   └── ir.model.access.csv
   └── data/
   ```
3. **Manifest Standard:**
   - Specify `name`, `version`, `category: 'Manufacturing'`, `license: 'LGPL-3'`, `depends`, `data`, `installable: True`, `application: False`.
4. **Rescan & Validate:**
   - Run `python scripts/factory/scan_modules.py`.
   - Run `python scripts/factory/build_graph.py`.
   - Run `python scripts/ci_gate.py`.
5. **Install via Bootstrap:**
   - `./scripts/bootstrap.ps1 -Modules factory_<name>`
