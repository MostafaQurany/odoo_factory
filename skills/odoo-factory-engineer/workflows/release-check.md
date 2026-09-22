# Workflow: Release Quality Check

Before declaring any change or feature complete:

1. **Vendor Tree Cleanliness:**
   - Verify `git status -- addons/` is completely clean.
2. **Catalog & Graph Freshness:**
   - Run `python scripts/factory/scan_modules.py`.
   - Run `python scripts/factory/build_graph.py`.
3. **Schema Compliance:**
   - Run `python scripts/factory/validate_schemas.py`.
4. **CI Quality Gate:**
   - Run `python scripts/ci_gate.py`.
5. **Scenario Impact Testing:**
   - Run mapped Golden Scenario: `python scripts/factory/run_scenario.py -s <CODE>`.
6. **Documentation & Spec-Kit:**
   - Ensure `docs/` and relevant ADRs in `docs/architecture/adr/` are updated.
