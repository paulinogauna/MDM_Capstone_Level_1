# Memo corto al CIO — Milestone 1

## Asunto
Milestone 1 — Inventario inicial de datos y primera lectura de calidad

## Resumen ejecutivo
Completamos un primer inventario offline del material disponible para el capstone de MDM Healthcare. El objetivo de esta etapa fue entender qué archivos tenemos, cómo están organizados, qué estructura presentan y qué señales tempranas de calidad aparecen, sin emitir todavía conclusiones de negocio ni decisiones de diseño definitivas.

## Qué creemos que tenemos
El repositorio contiene cuatro grupos principales de datos:

1. **Fuentes maestras de pacientes** en `Data_Source/1_Sources/`
   - 5 extractos de pacientes provenientes de sistemas distintos.
   - Todos comparten una estructura muy similar de 35 columnas.
   - Hay evidencia de superposición entre fuentes para una misma persona.

2. **Datos transaccionales** en `Data_Source/2_Transactional/`
   - 12 archivos operacionales.
   - Incluyen admisiones, citas, billing, claims, medical records, prescriptions, referrals y visits.
   - Estos archivos parecen útiles para validar integridad referencial y contexto operacional.

3. **Datos de referencia** en `Data_Source/3_Reference/`
   - 8 archivos de catálogos y jerarquías.
   - Incluyen hospitales, departamentos, doctores, enfermeros, códigos de procedimiento y jerarquías de aseguradoras.

4. **Borrador de consolidado/golden** en `Data_Source/4_Master_Golden_Draft/`
   - Un archivo consolidado `Patients_AllSources.csv`.
   - Un workbook `HCLS.xlsx` ya inspeccionado hoja por hoja dentro del catálogo automatizado.
   - El workbook contiene pestañas de pacientes, hospitales, departamentos, doctores, citas, historias clínicas, billing, visitas, prescripciones, claims, admisiones, jerarquías, enfermería, procedimientos e integridad referencial.

## Catálogo actual
Se generó un catálogo completo en:

- `outputs/reports/full_data_catalog.csv`

Este catálogo incluye por archivo:
- carpeta de origen
- nombre de archivo
- workbook y hoja cuando aplica
- cantidad de filas
- cantidad de columnas
- listado de columnas
- clasificación conceptual del archivo

Con esto queda cubierto el entregable de **a catalogue of every file, its columns, and row counts**.

## Primera lectura de calidad
Sobre las fuentes de pacientes ya contamos con una primera lectura de calidad. Se observan señales tempranas como:

- identificadores faltantes, duplicados o inválidos
- emails inválidos o vacíos
- nombres con placeholders o faltantes
- fechas imposibles o inconsistentes
- medidas clínicas fuera de rango
- dominios no estandarizados
- direcciones con estructura JSON inconsistente

Esto no constituye todavía una conclusión final, pero sí confirma que el dominio requerirá reglas explícitas de calidad, estandarización, matching y survivorship.

También queda cubierta una **first read of data quality per file**, con una medida aproximada de densidad de problemas obvios en las fuentes de pacientes.

## Extensión del análisis con MDM Cloud Data Profiling
Además del profiling offline, se ejecutó **Data Profiling en MDM Cloud / IDMC** sobre los extractos de pacientes.

Se configuró:
- una conexión a la carpeta con los archivos fuente;
- un profile job por archivo;
- export de los resultados resumen a `outputs/profiling/`.

Luego se consolidaron esos exports con una skill reutilizable:

- `.github/skills/profiling-summary/SKILL.md`

Esto permitió generar tres entregables adicionales para el step de profiling:

- `outputs/reports/profiling_scorecard.csv`
- `outputs/reports/profiling_ranking.md`
- `outputs/reports/profiling_cio_summary.md`

Con esto ya no solo tenemos una lectura temprana de calidad, sino también una **comparación por fuente y por atributo** para `name`, `DOB`, `email`, `phone` e `insurance`.

## Posicionamiento tecnológico
Para este proyecto vemos valor en un enfoque **cloud MDM** sobre on-premises por:

- mayor velocidad de implementación
- menor carga operativa de infraestructura
- mejor integración con servicios de calidad, integración y gobierno
- mejor alineación con un MVP iterativo

Conceptualmente, el flujo objetivo en IDMC / Informatica Cloud sería:

1. ingesta de fuentes
2. profiling y data quality
3. estandarización
4. matching y survivorship
5. golden record
6. validación con transaccionales y referencias
7. publicación y gobierno

## Estado actual
En esta etapa ya contamos con una base objetiva más fuerte para comparar fuentes. Aun así, los trust anchors deben considerarse **preliminares** mientras no se exporten también `rule occurrences` y `exception records` desde profiling.

## Próximo paso
El siguiente paso será profundizar el análisis de calidad e integridad referencial, exportar exceptions/rule occurrences desde profiling y preparar una visión más clara de cómo modelar el dominio Patient en un flujo MDM gobernado.
