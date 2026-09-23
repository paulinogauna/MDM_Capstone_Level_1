# Copilot instructions for MDM Healthcare project

## Project intent
This repository is a healthcare MDM capstone focused on patient master data, data quality, matching, survivorship, and golden record construction.

## Working rules
- Treat `Data_Source/` as read-only.
- Write all derived outputs to `outputs/`.
- Prefer reproducible scripts over ad-hoc notebook-only logic.
- Keep exploratory work in `notebooks/` and reusable logic in `scripts/`.
- Document business rules in `rules/`.
- Preserve traceability between source records and consolidated records.

## Analysis priorities
When asked to work on data tasks, prioritize:
1. Source profiling
2. Data quality validation
3. Referential integrity checks
4. Hierarchy validation
5. Entity matching
6. Survivorship and golden record logic

## Data quality expectations
Look for issues such as:
- invalid emails
- numeric names
- null or malformed identifiers
- orphan foreign keys
- circular or broken hierarchies
- duplicate or fuzzy duplicate patients
- PII leakage in free-text fields

## Implementation guidance
- Prefer Python for profiling, validation, matching, and reporting.
- Use DuckDB for fast local SQL over CSV files when useful.
- Keep rules modular: quality, matching, survivorship, referential integrity.
- Avoid hidden assumptions; document them in markdown.
- Do not overwrite source files.

## Output conventions
- Save reports under `outputs/reports/`.
- Save cleaned or standardized datasets under `outputs/curated/`.
- Save matching candidates under `outputs/matching/`.
- Save golden record drafts under `outputs/golden/`.
