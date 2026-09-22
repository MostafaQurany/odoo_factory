# Workflow: Debugging & Root Cause Analysis

1. **Reproduce & Trace:**
   - Inspect error trace in `docker compose logs -f web`.
   - Identify offending model, XML ID, or constraint.
2. **Missing XML ID or View Error:**
   - Verify that all referenced external IDs are present in the dependencies declared in `__manifest__.py`.
3. **Parse Error / Syntax Error:**
   - Run AST parser: `python -m py_compile <file>`.
   - Validate XML structure with standard parser.
4. **Registry / Cache Corruption:**
   - Restart container with upgrade: `./scripts/bootstrap.ps1 -Update -Modules <target_module>`.
5. **Never patch vendor code directly:**
   - If an error originates in OCA, inspect how to override via Python inheritance in `custom/`.
