# Workflow: Migrate Module & Schema Changes

## Protocol for Breaking / Data Changes
1. **Never drop columns manually in SQL.**
2. **If renaming a field:**
   - In pre-migration (`migrations/18.0.x/pre-migrate.py`):
     Rename column in database before Odoo model loads:
     `openupgrade.rename_columns(cr, {'table_name': [('old_field', 'new_field')]})`
3. **If changing field type or structure:**
   - Add new field.
   - In post-migration (`migrations/18.0.x/post-migrate.py`):
     Migrate values from old field to new field.
4. **Upgrade with Migration:**
   - `./scripts/bootstrap.ps1 -Update -Modules <module_name>`
5. **Verify Data Integrity:**
   - Run tests against disposable test database to confirm data survived migration without loss.
