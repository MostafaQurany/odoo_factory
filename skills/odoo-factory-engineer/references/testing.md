# Reference: Testing & Golden Scenario Impact Analysis

## Testing Strategy

### 1. Disposable Test Runner
Always execute tests against isolated, disposable test databases to prevent polluting operational data:
```powershell
./scripts/test.ps1 -Module factory_base
./scripts/test.sh --module factory_base
```

### 2. Impact-Driven Scenario Testing
After making changes to any module, check its scenario mapping:
```bash
python skills/odoo-factory-engineer/scripts/agent_helper.py --impact <module_name>
```
Then execute the mapped scenario:
```bash
python scripts/factory/run_scenario.py --scenario <CODE>
```

### 3. CI Quality Gate
Run `python scripts/ci_gate.py` before committing any substantive changes.
