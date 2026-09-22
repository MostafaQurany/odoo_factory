---
name: odoo-factory-engineer
description: Use when modifying, extending, debugging, migrating, or configuring models, fields, views, reports, security, workflows, or capabilities in the odoo_factory project
---

# Odoo Factory Engineer Operating Manual

## Overview
The definitive operating manual for AI agents modifying the Odoo Factory Platform. Enforces strict vendor/custom boundaries, declarative ERP contracts, and systematic verification.

## The Absolute Operating Rule
```text
User Requirement
↓
1. Inspect Project Contract (.factory/project.yml)
↓
2. Discover Module Catalog (.factory/generated/module_catalog.json)
↓
3. Resolve Ownership Boundary (addons/ is READ-ONLY, edit in custom/ only)
↓
4. Resolve Capability Contract (.factory/capabilities.yml)
↓
5. Select Target Addon & Smallest Safe Change
↓
6. Implement Extension (Inherit Python Model, Inherit View, Inherit QWeb)
↓
7. Run Impact Tests (scripts/factory/run_scenario.py -s <CODE>)
↓
8. Update Knowledge, Tests & Documentation (Spec-Kit Synchronization)
```

## When to Use This Skill
- Adding or modifying fields in existing Odoo models (`mrp.production`, `stock.picking`, etc.).
- Inheriting or modifying views (form, list, kanban, search).
- Customizing or inheriting QWeb PDF reports (invoices, production orders, picking slips).
- Enabling or configuring factory capabilities (quality, scrap, ddmrp, background jobs).
- Upgrading modules or executing schema/data migrations.
- Diagnosing errors, broken XML IDs, or dependency conflicts.

## Core Rules & Non-Negotiable Boundaries
1. **NEVER edit `addons/**` directly.** All vendor code is strictly READ-ONLY. All proprietary changes live in `custom/**`.
2. **NEVER guess model names or XML IDs.** Always verify against `.factory/generated/module_catalog.json` or source files before inheriting.
3. **NEVER install unreviewed addons in production.** All unclassified modules are blocked by policy.
4. **NEVER execute raw SQL schema surgery.** Schema modifications must follow `workflows/migrate-module.md`.
5. **NEVER declare completion without impact verification.** Modifying a component requires running its associated Golden Scenario (GS-xxx / GX-xxx).

## Red Flags — STOP and Re-evaluate
- Attempting to edit a file under `addons/`
- Adding a field in Python without checking if an existing OCA field already provides it
- Editing a PostgreSQL table with raw SQL `ALTER TABLE` or `DROP COLUMN`
- Modifying a report without checking whether underlying model fields exist
- Renaming module technical names directly on the filesystem

## Quick Reference Workflows
| Task | Workflow Guide |
|------|----------------|
| Understand requirement & locate models | `workflows/inspect-requirement.md` |
| Add field to model & view | `workflows/add-field.md` |
| Inherit & modify form/list view | `workflows/modify-view.md` |
| Inherit & customize QWeb PDF report | `workflows/modify-report.md` |
| Enable business capability | `workflows/enable-capability.md` |
| Migrate model / field schema | `workflows/migrate-module.md` |
| Upgrade module in database | `workflows/upgrade-module.md` |
| Diagnose and recover from errors | `workflows/debug.md` |
| Final release & quality check | `workflows/release-check.md` |

## Agent Helper CLI
Use `python skills/odoo-factory-engineer/scripts/agent_helper.py` to inspect project contracts:
```bash
python skills/odoo-factory-engineer/scripts/agent_helper.py --module mrp
python skills/odoo-factory-engineer/scripts/agent_helper.py --capability quality
python skills/odoo-factory-engineer/scripts/agent_helper.py --model mrp.production
```
