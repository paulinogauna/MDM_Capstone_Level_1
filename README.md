# MDM_Capstone_Level_1

Repository for a healthcare MDM capstone focused on patient master data, data quality, profiling, matching, survivorship, and golden record design.

## Current project outputs
- Offline profiling and cataloging scripts under `scripts/`
- Initial quality rules under `rules/`
- Profiling exports from MDM Cloud under `outputs/profiling/`
- Derived reports under `outputs/reports/`, including:
	- `full_data_catalog.csv`
	- `source_profile_summary.csv`
	- `patient_quality_issues.csv`
	- `profiling_scorecard.csv`
	- `profiling_ranking.md`
	- `profiling_cio_summary.md`

## Profiling workflow
1. Profile local source files offline for reproducible checks.
2. Run Data Profiling in MDM Cloud / IDMC with one profile job per patient source file.
3. Export profiling summary workbooks to `outputs/profiling/`.
4. Use the reusable skill in `.github/skills/profiling-summary/SKILL.md` to consolidate scorecards, rankings, and CIO-ready summaries.
