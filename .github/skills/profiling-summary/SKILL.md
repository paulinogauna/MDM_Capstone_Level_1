---
name: profiling-summary
description: "Use when summarizing Informatica/IICS/Business 360 data profiling exports for healthcare MDM, especially to build per-source completeness and quality scorecards, rank trust anchors by field, and draft a CIO-ready profiling summary from files in outputs/profiling/."
---

# Profiling Summary Skill

Use this skill when the user has exported profiling results, scorecards, rule occurrences, or exception reports and wants a reusable workflow to turn them into business-facing deliverables.

## Goal

Produce a consistent summary from profiling exports without modifying source data. The expected outputs are:

1. A per-source completeness and quality report
2. A ranking of sources by attribute
3. Trust-anchor recommendations by field
4. A concise CIO-ready executive summary

## Expected inputs

Look first in `outputs/profiling/` and its subfolders for exported profiling artifacts such as:

- profile summaries
- column profiles
- rule occurrence exports
- exception reports
- scorecards
- screenshots or evidence files

Also read reference metadata when needed:

- `Data_Source/3_Reference/Data_Sources.csv`
- `rules/patient_quality_rules.md`
- relevant docs under `docs/`

## Core workflow

### 1. Inventory the profiling exports

Identify what files exist under `outputs/profiling/`.
Group them by source system and by artifact type.
Normalize source names where needed:

- Epic
- Cerner
- RegistrationDB
- ManualEntry

If filenames are ambiguous, infer source from file content before summarizing.

### 2. Extract the required metrics

For each source, capture metrics for these business attributes when available:

- name
- DOB
- email
- phone
- insurance

Prefer these measures:

- blank/null percentage
- invalid percentage
- completeness percentage
- distinctness or uniqueness when relevant
- rule violations and exception counts

Keep completeness separate from validity.
A present but malformed value is not complete-and-valid.

### 3. Flag expected issue patterns

Specifically look for evidence of:

- invalid email formats
- phone-like strings in email fields
- missing or malformed DOB values
- impossible dates or unreasonable ages
- numeric or nonsense names
- SSN or other PII in the wrong fields
- missing or malformed insurance values

When possible, include counts and a few representative examples.

### 4. Cross-reference source trust metadata

Use `Data_Source/3_Reference/Data_Sources.csv` when available to bring in:

- `trust_score`
- `data_quality_score`

Use these as supporting evidence, not as a replacement for measured profiling results.
If measured quality conflicts with the reference ranking, call that out explicitly.

### 5. Build the comparative scorecard

Create a single comparison table with one row per source and columns for:

- source
- name blank %
- name invalid %
- DOB blank %
- DOB invalid %
- email blank %
- email invalid %
- phone blank %
- phone invalid %
- insurance blank %
- insurance invalid %
- trust_score
- data_quality_score

If a metric is unavailable, mark it clearly as unavailable rather than guessing.

### 6. Rank sources by attribute

Rank the sources separately for each attribute.
Use measured blank and invalid rates first.
Use trust metadata as a tiebreaker when needed.
Do not produce only an overall ranking; include field-level ranking.

### 7. Recommend trust anchors

Recommend the best source for each attribute based on the evidence.
Typical attributes:

- name
- DOB
- email
- phone
- insurance

Explain why each trust anchor was chosen.
If no source is strong enough for an attribute, say so plainly.

### 8. Draft the executive summary

Produce a short business summary suitable for the CIO. It should answer:

- Is the data quality consistent across sources?
- Which source is strongest for which fields?
- Which source is weakest?
- What are the main quality risks?
- What should leadership do next?

Keep it factual and measurable.
Avoid unsupported claims.

## Output format

When asked to generate the summary, prefer producing these sections:

### A. Per-source scorecard
A compact comparison table.

### B. Attribute ranking
A ranked list for name, DOB, email, phone, and insurance.

### C. Trust-anchor recommendations
A short justification per attribute.

### D. Key findings
3 to 7 bullets with the most important issues.

### E. CIO summary
A concise executive paragraph or memo-style summary.

## Guardrails

- Treat `Data_Source/` as read-only.
- Write derived outputs only under `outputs/`.
- Do not invent metrics that are not present in the exports.
- Distinguish blank, invalid, and conflicting values.
- Prefer reproducible summaries over ad-hoc interpretation.
- If exports are incomplete, state exactly what is missing.

## Suggested derived outputs

When creating files, prefer:

- `outputs/reports/profiling_scorecard.csv`
- `outputs/reports/profiling_ranking.md`
- `outputs/reports/profiling_cio_summary.md`

## Trigger phrases

This skill is especially relevant when the user asks to:

- summarize profiling exports
- build a per-source quality report
- rank source systems by field quality
- decide trust anchors
- prepare a CIO profiling summary
- analyze Informatica or IICS profiling results
- turn profiling scorecards into executive findings
