# ADR-003: Single Source of Truth for Install Profiles

## Status
Accepted

## Context
If install profiles are maintained both in `.factory/install_profiles.yml` and in individual meta-addon `__manifest__.py` files, they will inevitably drift apart over time.

## Decision
1. `.factory/install_profiles.yml` is the sole authoritative definition of deployment profiles.
2. `scripts/factory/generate_profiles.py` automatically generates or verifies `custom/factory_profile_*` manifests.

## Consequences
- Meta-addon manifests are completely deterministic and never hand-edited.
