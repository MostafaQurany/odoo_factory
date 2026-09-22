# Workflow: Inspect Requirement

1. Parse user requirement to identify target business process (e.g. Manufacturing Order, Vendor Intake, Quality Gate).
2. Check `.factory/project.yml` for active localization and project constraints.
3. Query `agent_helper.py --capability <keyword>` to check if an existing capability covers it.
4. Locate underlying model using `references/odoo-model-map.md`.
5. Check if fields already exist in upstream OCA/vendor code (`.factory/generated/module_catalog.json`).
6. Identify target custom module in `custom/` or plan new extension module.
