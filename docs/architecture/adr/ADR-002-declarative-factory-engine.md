# ADR-002: Declarative Factory Engine and Schema Validation

## Status
Accepted

## Context
Relying solely on Odoo module manifests forces users and developers to memorize hundreds of technical addon names and dependency quirks.

## Decision
1. Establish a declarative knowledge layer in `.factory/`.
2. Distinguish generated facts (`.factory/generated/`) from curated policies (`.factory/*.yml`).
3. Enforce JSON schema validation (`.factory/schemas/*.json`) on all declarative contracts.

## Consequences
- Business capabilities (e.g., quality, scrap, ddmrp) are mapped directly to technical modules.
- Changes to declarative architecture are validated automatically in CI.
