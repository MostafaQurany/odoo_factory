# Workflow: Disable Capability

1. Look up capability in `.factory/capabilities.yml`.
2. Check if other active capabilities depend on it (`requires` check).
3. If dependencies exist, inform user or disallow disabling without disabling dependents.
4. Remove capability from target profile in `.factory/install_profiles.yml`.
5. Regenerate manifests: `python scripts/factory/generate_profiles.py`.
6. Run `python scripts/ci_gate.py`.
7. Verify that remaining capabilities and tests pass cleanly.
