# ADR-005: Safe Legacy Module Relocation Preserving Technical Names

## Status
Accepted

## Context
Renaming Odoo module directories during filesystem relocation breaks database module registry state, external XML IDs, and upgrade histories.

## Decision
1. Relocate `clothing_factory_demo` and `odoo_factory_all` to `custom/` using `git mv` without changing technical directory names.
2. Mark `odoo_factory_all` and `clothing_factory_demo` as `LEGACY` in `.factory/module_policy.yml`.
3. Introduce replacement profiles (`factory_profile_core`, etc.) and generic demo (`factory_demo`) cleanly.
4. Retire legacy modules in a later controlled deprecation cycle.

## Consequences
- Zero breaking changes to existing databases or Git history.
