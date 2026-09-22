# Reference: Troubleshooting & Common Pitfalls

## Common Traps & Fixes

### 1. View Cannot Be Found (Missing XML ID)
- **Symptom:** `ValueError: External ID not found in system`
- **Cause:** Typo in `inherit_id` or referencing an addon not listed in `depends`.
- **Fix:** Verify exact XML ID in source repo and ensure target module is in `depends` in `__manifest__.py`.

### 2. Ambiguity: What Does "Table" Mean?
When the user asks to "edit the table", never assume a PostgreSQL DB table!
Clarify or inspect whether they mean:
1. Form View One2many tree table
2. List / Tree view
3. QWeb PDF printed report table
4. Pivot / Analysis table

### 3. Duplicate Key Violation
- **Symptom:** Unique constraint error on upgrade.
- **Cause:** Attempting to create existing record without `noupdate="1"`.
- **Fix:** Wrap master data in `<data noupdate="1">` or use XML IDs properly.
