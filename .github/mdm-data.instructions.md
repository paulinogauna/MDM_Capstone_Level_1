---
applyTo: "Data_Source/**/*.csv,Data_Source/**/*.xlsx,notebooks/**/*.ipynb,scripts/**/*.py,docs/**/*.md"
description: "Use when working on MDM healthcare data profiling, data quality, matching, survivorship, golden record, referential integrity, or hierarchy validation."
---

# MDM healthcare data instructions

## Core behavior
- Assume healthcare patient data with multiple source systems.
- Keep source data immutable.
- Prefer deterministic checks and reproducible outputs.
- Separate profiling, validation, matching, and survivorship concerns.

## Expected workflow
1. Profile schema and nullability.
2. Validate field formats and business rules.
3. Check cross-table integrity.
4. Detect duplicates and identity conflicts.
5. Propose survivorship logic explicitly.
6. Export findings to `outputs/`.

## Guardrails
- Do not silently fix source data.
- Do not invent columns or business keys without checking files first.
- When matching patients, explain exact vs fuzzy criteria.
- When proposing a golden record, explain source precedence or survivorship rules.
