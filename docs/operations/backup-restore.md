# Factory Platform — Backup & Disaster Recovery Guide

---

## 1. Overview
This operational document establishes the automated backup and disaster recovery procedures for the Odoo Factory Platform. Regular backups consist of two artifacts:
1. **PostgreSQL Database Dump**: Stored in PostgreSQL custom format (`-Fc`) containing all transaction history, configurations, and records.
2. **Filestore Archive**: Stored under `/var/lib/odoo/filestore/<db_name>` containing uploaded CAD drawings, spec sheets, QC photos, and PDF attachments.

---

## 2. Backup Execution
Run the PowerShell or Bash backup automation:
```powershell
./scripts/backup.ps1 -DbName odoo
```
The script:
- Invokes `pg_dump` inside the database container with compression.
- Copies the binary dump archive to the local `./backups` directory with an exact UTC timestamp.
- Emits a companion `.json` manifest recording Odoo version, database name, and metadata.

---

## 3. Restore & Disaster Recovery Drill
To restore the platform to a clean state or recover from hardware failure:
```powershell
./scripts/restore.ps1 -DumpFile ./backups/odoo_20260922_120000.dump -TargetDb odoo
```
The restore procedure:
1. Resets the target database cleanly.
2. Loads the dump using `pg_restore` without ownership collisions.
3. Automatically runs Odoo health checks (`.factory/health_checks.yml`).
4. Re-evaluates Golden Scenarios to ensure transactional data integrity.
