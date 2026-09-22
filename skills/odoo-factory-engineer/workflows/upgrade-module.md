# Workflow: Upgrade Module

1. Save code changes in target module.
2. Verify Python syntax (`python -m py_compile <file>`).
3. Run upgrade runner:
   ```powershell
   ./scripts/bootstrap.ps1 -Update -Modules <module_name>
   ```
4. Verify standard output for upgrade completion without tracebacks or exceptions.
5. Inspect Odoo container logs:
   ```bash
   docker compose logs --tail=50 web
   ```
6. Run scenario impact check:
   ```bash
   python skills/odoo-factory-engineer/scripts/agent_helper.py --impact <module_name>
   ```
