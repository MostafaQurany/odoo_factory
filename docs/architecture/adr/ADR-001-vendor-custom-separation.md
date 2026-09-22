# ADR-001: Strict Separation of Vendor and Custom Code

## Status
Accepted

## Context
The codebase previously contained custom modules embedded inside OCA repository directories (`addons/manufacture/clothing_factory_demo` and `addons/server-tools/odoo_factory_all`). This created maintenance friction, risked accidental overrides of vendor code, and confused automated agents.

## Decision
1. `addons/**` is designated as upstream/vendor code and is strictly READ-ONLY.
2. `custom/**` is designated as the sole home for project-owned addons.
3. Custom addons will always reside in a flat directory under `custom/` to avoid recursive discovery issues in Odoo.

## Consequences
- Upstream updates can be pulled without merge conflicts in proprietary code.
- Agents have an unambiguous answer to "Am I allowed to edit this file?".
