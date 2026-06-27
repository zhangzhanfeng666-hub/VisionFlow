# AGENTS

## Purpose

This repository is the `HDR Creator` DCTL workspace for first-phase MVP development.

It is not:

- a generic LUT lab
- a full GUI product repo
- a raw media archive

It is for validating:

- `Pocket + iPhone -> HDR publish`
- DCTL experiments for HDR release workflow
- lightweight, reproducible collaboration between humans and AI agents

## Read Order

Read these files in order before proposing or making changes:

1. `README.md`
2. `docs/repo-scope.md`
3. `docs/product-intent.md`
4. `docs/current-priority.md`
5. `docs/dev-workflow.md`
6. `docs/validation-playbook.md`

## Current Priority

Only optimize for the current first-phase path:

- capture HDR
- normalize input if needed
- publish HDR correctly

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

- `src/` contains editable source
- `release/dctl/` contains deployment-ready copies
- `docs/` contains project intent and workflow rules

Do not treat `release/` as the authoring source.

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
