# Workflow MDM Healthcare

## Flujo objetivo
1. Ingesta de fuentes maestras.
2. Profiling estructural offline en workspace.
3. Data Profiling en MDM Cloud / IDMC.
4. Export de scorecards y summaries desde profiling.
5. Consolidación de resultados con skill reutilizable.
6. Reglas de calidad.
7. Estandarización.
8. Matching de entidades.
9. Survivorship.
10. Golden record.
11. Validación referencial con tablas transaccionales.
12. Exportación de resultados.

## Flujo aplicado en este milestone
1. Se revisaron los CSV locales para entender estructura y calidad básica.
2. Se creó profiling reproducible offline con `scripts/profile_sources.py`.
3. Se ejecutó Data Profiling en MDM Cloud usando una conexión a la carpeta con los extractos fuente.
4. Se configuró un profile job por archivo de pacientes.
5. Se exportaron los workbooks resumen a `outputs/profiling/`.
6. Se creó la skill `.github/skills/profiling-summary/SKILL.md` para resumir los exports.
7. Se generaron los entregables:
	- `outputs/reports/profiling_scorecard.csv`
	- `outputs/reports/profiling_ranking.md`
	- `outputs/reports/profiling_cio_summary.md`
8. Se usó el scorecard para proponer ranking por atributo y trust anchors preliminares.

## Casos del proyecto
- Emails inválidos
- Nombres numéricos
- Fugas de PII
- IDs huérfanos
- Jerarquías circulares o rotas
- Duplicados exactos y fuzzy
- Conflictos crosswalk entre sistemas

## Entregables sugeridos
- Perfil de fuentes
- Reporte de calidad
- Profiling scorecard por fuente
- Ranking por atributo y trust anchors
- CIO profiling summary
- Reporte de matching
- Borrador de golden record
- Catálogo de reglas
