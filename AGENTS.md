# AGENTS

## Purpose

This repository is the `HDR Creator` Resolve plugin/script workspace for first-phase MVP development.

It is not:

- a generic LUT lab
- a full GUI product repo
- a raw media archive

It is for validating:

- `Pocket + iPhone -> HDR publish`
- plugin/script orchestration for HDR release workflow
- DCTL-based color modules used by that workflow
- lightweight, reproducible collaboration between humans and AI agents

## Read Order

Read these files in order before proposing or making changes:

1. `README.md`
2. `docs/repo-scope.md`
3. `docs/product-intent.md`
4. `docs/current-priority.md`
5. `docs/dev-workflow.md`
6. `docs/plugin-architecture.md`
7. `docs/resolve-plugin-v1.md`
8. `docs/validation-playbook.md`

## Current Priority

Only optimize for the current first-phase path:

- capture HDR
- normalize input if needed
- publish HDR correctly
- orchestrate the above through a Resolve-facing shell

Current device focus:

- DJI Pocket family
- iPhone Pro family

## Scope Guardrails

Do not expand scope without explicit confirmation into:

- GUI app implementation
- automated editing pipelines
- LUT marketplace / style pack ecosystem
- HDR to SDR compatibility as the main line
- raw footage management

## Source Of Truth

- `src/plugin/` contains plugin/script shell work
- `src/workflow/` contains recognition and planning logic
- `src/dctl/` contains color-processing modules
- `release/dctl/` contains deployment-ready DCTL copies
- `docs/` contains project intent and workflow rules

Do not treat `release/` as the authoring source, and do not treat `DCTL` as the whole product.

## Naming Conventions

- DCTL: `HDRC_<stage>_<family>_<purpose>.dctl`
- Branches: `feature/<topic>`, `fix/<topic>`, `exp/<topic>`
- Screenshots: `<device>_<scene>_<variant>_<date>.png`

## Evidence Expectations

When changing behavior, also update at least one of:

- a relevant doc in `docs/`
- a validation still in `tests/stills/`

Changes should state:

- intended result
- assumption
- what was validated
- what remains unvalidated
