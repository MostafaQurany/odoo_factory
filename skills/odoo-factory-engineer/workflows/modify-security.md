# Workflow: Modify Security & Access Rights

1. **Classify Security Requirement:**
   - Role group creation / modification
   - Model ACLs (`ir.model.access.csv`)
   - Record-level access rules (`ir.rule`)
   - Field-level restrictions (`groups="..."` on fields)
2. **Implement in Target Custom Module:**
   - Security groups in `security/<addon>_security.xml`
   - Access rights in `security/ir.model.access.csv`
   - Record rules in `security/<addon>_rules.xml`
3. **Multi-Company & Department Separation:**
   - Always verify company isolation rules:
     ```xml
     <field name="domain_force">['|', ('company_id', '=', False), ('company_id', 'in', company_ids)]</field>
     ```
4. **Upgrade & Verify:**
   - `./scripts/bootstrap.ps1 -Update -Modules <addon_name>`
   - Run cross-cutting check: `python scripts/factory/run_scenario.py -s GX-001`
