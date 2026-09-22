# Workflow: Enable Capability

1. Look up requested capability in `.factory/capabilities.yml`.
2. Inspect required and optional modules, plus prerequisite capabilities (`requires`).
3. If prerequisite capabilities are missing in the target profile, enable them first.
4. Add capability to the target profile in `.factory/install_profiles.yml`.
5. Run `python scripts/factory/generate_profiles.py` to regenerate meta-addon manifests.
6. Run `python scripts/ci_gate.py` to ensure zero dependency cycles or unapproved modules.
7. Run bootstrap installer: `./scripts/bootstrap.ps1 -Profile <target_profile>`.
8. Execute mapped Golden Scenario tests to verify functional activation.
