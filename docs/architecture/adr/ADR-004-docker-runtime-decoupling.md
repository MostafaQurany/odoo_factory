# ADR-004: Decoupling Docker Runtime from Bootstrap and Testing

## Status
Accepted

## Context
Previously, `docker-compose.yml` had `-i odoo_factory_all,clothing_factory_demo` hardcoded in the main command. Every container start attempted to reinstall/update these modules.

## Decision
1. `docker compose up` serves purely as a clean web runtime (PostgreSQL + Odoo HTTP server).
2. Initialization and profile installation are offloaded to headless script runners (`scripts/bootstrap.ps1` / `.sh`).
3. Automated tests run against disposable databases (`odoo_test_<run_id>`) via `scripts/test.ps1` / `.sh`.

## Consequences
- Fast server startup without unintended database mutations on reboot.
- Isolated test environments preventing test pollution in operational databases.
