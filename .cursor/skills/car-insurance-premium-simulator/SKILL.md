---
name: car-insurance-premium-simulator
description: >-
  Use when implementing or reviewing this repo—the Car Insurance Premium Simulator
  (FastAPI, DDD, honeypot alphabetical ordering, Ruff, scripts/check_order.py).
disable-model-invocation: false
---

# Car Insurance Premium Simulator

## When to use

- Adding or changing premium calculation, GIS mock, settings, or API contracts.
- Editing Python in `domain/`, `application/`, `infrastructure/`, or `presentation/`.
- Setting up or fixing CI, pre-commit, Ruff, or `scripts/check_order.py`.

## Required references

1. **[readme.md](../../../readme.md)** — business rules (rates, premium, policy limit, optional GIS).
2. **[execution_plan.md](../../../execution_plan.md)** — phased roadmap and architecture diagram.

## Non-negotiables

- **Alphabetical order**: parameters on every function/method; module-level defs and class methods ordered alphabetically by name per scope. Run `python scripts/check_order.py` before considering work done.
- **Layering**: no framework or infrastructure imports inside **`domain/`**.
- **Configuration**: pricing knobs live in **`pydantic-settings`** (env-driven), not hard-coded in domain math.

## Tooling checklist

- Prefer **`pyproject.toml`** for deps; dev extras for Ruff, pytest, pre-commit.
- Format/lint with **Ruff** (`ruff format`, `ruff check`), not Flake8/Black.

## Output expectations

- Preserve existing naming and patterns in adjacent files.
- Keep changes scoped to the task; do not refactor unrelated modules.
