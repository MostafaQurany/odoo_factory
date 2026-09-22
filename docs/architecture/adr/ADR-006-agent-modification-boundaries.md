# ADR-006: AI Agent Operating Boundaries and Modification Protocol

## Status
Accepted

## Context
Automated coding agents risk guessing model names, inventing XML IDs, patching vendor code directly, or performing manual database schema alterations when attempting tasks.

## Decision
1. Deploy `skills/odoo-factory-engineer/` as the mandatory operating manual for all agents.
2. Agents must execute the Absolute Operating Rule:
   Requirement -> Inspect Contract -> Discover Implementation -> Resolve Ownership -> Resolve Capability -> Smallest Safe Change -> Implement -> Test Impact -> Update Knowledge.
3. Raw SQL DDL/DML surgery is strictly forbidden.
4. Definition of Done mandates synchronization of Code, Tests, `.factory/` metadata, Docs, and Spec-Kit.

## Consequences
- Agents act deterministically with zero loss of context or code collisions.
