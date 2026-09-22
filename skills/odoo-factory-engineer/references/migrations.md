# Reference: Database Migrations & Upgrades

## Migration Protocol
1. **Backward-Compatible Changes (Non-breaking):**
   - Adding new nullable fields or fields with defaults.
   - Adding new views, reports, security groups.
   - Protocol: Deploy code -> run module upgrade (`-u <module>`).
2. **Schema / Breaking Changes:**
   - Renaming fields, changing data types, splitting tables.
   - Protocol:
     - Pre-migration script (`migrations/18.0.x/pre-migration.py`)
     - Core upgrade
     - Post-migration data backfill (`migrations/18.0.x/post-migration.py`)
3. **STRICT PROHIBITIONS:**
   - Never execute manual `DROP COLUMN` or `DELETE FROM` in production databases.
   - Never solve migration errors by dropping database tables or records.
