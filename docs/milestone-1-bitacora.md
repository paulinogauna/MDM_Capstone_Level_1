# Bitácora de viaje — Milestone 1

## 1. Contexto del milestone

### Requerimiento original
Para el **Milestone 1** debíamos asegurar, como mínimo:

- **A catalogue of every file, its columns, and row counts**
- **A first read of data quality per file (rough % of obvious garbage)**
- **A short memo to the CIO: “here is what we think we have” with no conclusions yet**

Además, se esperaba:

- abrir y catalogar cada archivo en las cuatro carpetas;
- distinguir archivos fuente crudos vs. consolidado/golden draft;
- reconocer que los extractos de pacientes se superponen entre sí;
- no asumir que archivos pequeños o casi vacíos están correctos;
- posicionar el valor de **cloud MDM vs on-premises**;
- bosquejar los servicios de **IDMC / Informatica Cloud** y el flujo conceptual de datos.

---

## 2. Qué decidimos hacer primero

Antes de entrar en MDM 360 o en una configuración SaaS, definimos que el primer paso debía hacerse **offline en el workspace**, porque:

- los datos están disponibles localmente en CSV;
- necesitábamos entender la estructura real antes de modelar reglas en la plataforma;
- convenía producir artefactos reproducibles;
- el repositorio ya estaba preparado para trabajar con `scripts/`, `notebooks/`, `outputs/` y `rules/`.

La decisión fue: **arrancar con profiling estructural y una primera lectura de calidad sobre las fuentes de pacientes**.

---

## 3. Qué revisamos al inicio

Se inspeccionó la estructura del repositorio y se confirmó la existencia de estas carpetas fuente:

- `Data_Source/1_Sources/`
- `Data_Source/2_Transactional/`
- `Data_Source/3_Reference/`
- `Data_Source/4_Master_Golden_Draft/`

También se revisaron los documentos guía del proyecto:

- `docs/workflow-mdm.md`
- `docs/mdm-scope.md`
- `docs/setup.md`
- `docs/mcp-options.md`
- `.github/mdm-data.instructions.md`

Hallazgo inicial importante:

- el repositorio tenía la **estructura correcta**, pero `scripts/`, `notebooks/` y `rules/` estaban vacíos;
- no había `requirements.txt`, `pyproject.toml`, `environment.yml` ni `.venv`;
- sí existían los datos y la guía metodológica para empezar.

---

## 4. Qué construimos en este milestone

### 4.1 Script reusable de profiling
Se creó:

- `scripts/profile_sources.py`

Este script:

- lee los CSV de `Data_Source/1_Sources/`;
- calcula por archivo y por columna:
  - cantidad de filas,
  - cantidad de columnas,
  - nulos,
  - porcentaje de nulos,
  - cantidad de valores distintos,
  - muestras de valores;
- detecta issues básicos de calidad:
  - identificadores faltantes,
  - identificadores inválidos o negativos,
  - duplicados por `patient_id`,
  - nombres inválidos,
  - emails inválidos,
  - teléfonos placeholder,
  - fechas inválidas o futuras,
  - secuencias de fechas inconsistentes,
  - medidas fuera de rango,
  - dominios inválidos,
  - JSON roto en `address`.

### 4.2 Notebook exploratorio
Se creó:

- `notebooks/01_source_profiling.ipynb`

Objetivo del cuaderno:

- iniciar el flujo exploratorio;
- verificar rutas y archivos;
- revisar rápidamente los reportes generados por el script;
- dejar una base para análisis posterior sin perder reproducibilidad.

### 4.3 Reglas iniciales documentadas
Se creó:

- `rules/patient_quality_rules.md`

Este documento formaliza las reglas iniciales del milestone 1 para que el análisis no quede implícito.

### 4.4 Reportes generados
Se generaron:

- `outputs/reports/source_profile_details.csv`
- `outputs/reports/source_profile_summary.csv`
- `outputs/reports/patient_quality_issues.csv`
- `outputs/reports/full_data_catalog.csv`

---

## 5. Cómo ayudó la IA / el agente vs hacerlo manualmente

### Si se hacía manualmente
Hacer este milestone a mano implicaba:

- abrir archivo por archivo;
- contar filas y columnas manualmente o con Excel;
- revisar columnas una por una;
- detectar patrones de basura visualmente;
- anotar hallazgos en documentos separados;
- repetir el proceso si cambiaba una regla o aparecía un nuevo archivo.

Eso hubiera sido:

- más lento;
- menos consistente;
- menos reproducible;
- más propenso a omisiones;
- difícil de escalar a los cuatro grupos de datos.

### Cómo ayudó la IA / el agente
La IA ayudó a:

- ordenar el milestone en entregables concretos;
- revisar la estructura del repo y detectar faltantes;
- proponer el primer entregable correcto para MDM;
- generar el script reusable;
- generar el notebook inicial;
- documentar reglas de calidad;
- ejecutar y validar el script;
- corregir un problema de compatibilidad con `pandas` durante la ejecución;
- dejar artefactos listos para iterar.

### Valor concreto del apoyo de IA
El valor no fue “hacer magia”, sino **acelerar y estructurar**:

- menos trabajo repetitivo;
- más trazabilidad;
- más velocidad para pasar de idea a artefacto;
- mejor documentación desde el inicio;
- base más sólida para continuar con matching, survivorship y golden record.

---

## 6. Qué obtuvimos hasta ahora

---

## 7. Avance posterior: cierre de profiling y arranque de Milestone 3

Después de completar el profiling inicial y los entregables asociados, se avanzó con dos frentes adicionales: el cierre del análisis comparativo de fuentes y el inicio del trabajo de reference data para `Milestone 3`.

### 7.1 Cierre del profiling comparativo
Se consolidó el trabajo de profiling exportado desde MDM Cloud / IDMC y se dejó una skill reutilizable para resumir resultados.

Artefactos relevantes:

- `.github/skills/profiling-summary/SKILL.md`
- `outputs/reports/profiling_scorecard.csv`
- `outputs/reports/profiling_ranking.md`
- `outputs/reports/profiling_cio_summary.md`

Con esto quedó resuelto el paso de:

- comparar calidad por fuente;
- rankear atributos por sistema;
- proponer trust anchors preliminares;
- dejar un resumen ejecutivo reutilizable.

### 7.2 Decisión para Milestone 3
Se evaluó si era necesario depender exclusivamente de nuevos profiling exports para construir los catálogos de referencia. La conclusión fue que el repositorio ya contiene una base suficiente en:

- `Data_Source/3_Reference/`

Por lo tanto, se decidió usar esa carpeta como **seed canonical source** para Reference 360, y dejar los profiling adicionales como complemento para descubrir aliases, valores fuera de catálogo y conflictos semánticos.

### 7.3 Revisión de la carpeta de reference
Se inspeccionaron los archivos:

- `Data_Source/3_Reference/Hospitals.csv`
- `Data_Source/3_Reference/Departments.csv`
- `Data_Source/3_Reference/Hierarchy.csv`
- `Data_Source/3_Reference/Insurance_Provider_Hierarchy.csv`
- `Data_Source/3_Reference/Procedure_Codes.csv`
- `Data_Source/3_Reference/Data_Sources.csv`

Hallazgos principales:

- existe material suficiente para construir dominios de `Hospital`, `Department`, `Payer`, `Procedure Category` y `Procedure Code`;
- las jerarquías existen, pero contienen errores intencionales o datos inconsistentes;
- no todo está listo para carga directa en Reference 360;
- era necesario crear una capa curada antes de cargar.

### 7.4 Script de curación para cargas de Reference 360
Se creó:

- `scripts/build_reference_loads.py`

Este script:

- lee los CSV de `Data_Source/3_Reference/`;
- genera datasets curados para carga;
- separa entidades y relaciones;
- expande algunos nombres canónicos de departamentos;
- excluye relaciones inválidas de la carga;
- genera un reporte de issues para revisión steward.

### 7.5 Outputs generados para Milestone 3
Se generaron en `outputs/curated/`:

- `reference_hospital.csv`
- `reference_department.csv`
- `reference_payer.csv`
- `reference_procedure_category.csv`
- `reference_procedure_code.csv`
- `reference_relationship_hospital_department.csv`
- `reference_relationship_payer_hierarchy.csv`
- `reference_relationship_procedure_hierarchy.csv`

Y además:

- `outputs/reports/reference_data_issues.csv`

### 7.6 Problemas detectados en reference data
El proceso de curación detectó, entre otros:

- hospitales con `accreditation=None`;
- años sospechosos como `1800`;
- referencias inválidas a doctores en departamentos;
- relaciones `hospital_id` fuera del catálogo en `Hierarchy.csv`;
- payers con padres inexistentes o autorreferencia;
- procedimientos con padres faltantes, nombres duplicados o categoría `Unknown`.

Esto confirma que el milestone no consiste solo en “cargar catálogos”, sino en **gobernar y depurar reference data antes de usarlo en MDM**.

### 7.7 Valor del apoyo de IA en esta etapa
En esta fase, la IA ayudó a:

- decidir que `3_Reference/` era la base correcta para arrancar Milestone 3;
- inspeccionar rápidamente la calidad de los catálogos;
- diseñar la estructura de outputs curados;
- generar el script de curación;
- instalar dependencias faltantes (`pandas`) en el entorno Python;
- corregir una incompatibilidad menor del script durante la ejecución;
- dejar listos los CSV de carga y el backlog de issues.

### 7.8 Estado al cierre de esta etapa
Al cierre de este avance, quedó listo el insumo técnico para pasar al siguiente paso de `Milestone 3`:

- diseñar el mapeo exacto de dominios y relaciones en `Reference 360`;
- definir qué CSV carga cada dominio;
- decidir qué registros entran como `Approved` y cuáles quedan para revisión steward.

### 7.9 Modelado final en Reference 360 para Milestone 3
Una vez generados los CSV curados, se avanzó en la configuración del modelo dentro de `Reference 360`.

#### Dataset de referencia creado
Se definió un dataset contenedor para agrupar los catálogos canónicos del dominio healthcare, con el enfoque de:

- un único `Reference Data Set`;
- múltiples `Code Lists` dentro del dataset;
- jerarquías separadas cuando la herramienta no soporta self-hierarchy sobre la misma lista.

#### Code lists cargadas
Se cargaron listas canónicas para:

- `HOSPITAL`
- `DEPARTMENT`
- `PAYER_GROUP`
- `PAYER`
- `PAYER_PLAN`
- `PROCEDURE_GROUP`
- `PROCEDURE_FAMILY`
- `PROCEDURE_CODE`

#### Ajuste de diseño por restricción de la herramienta
Durante la configuración se detectó que `Reference 360` no permitía modelar jerarquías usando la misma code list como padre e hijo. Eso obligó a rediseñar dos dominios:

##### Payers
El modelo inicial de `PAYER -> PAYER` fue reemplazado por tres niveles:

- `PAYER_GROUP`
- `PAYER`
- `PAYER_PLAN`

Y se regeneraron los archivos:

- `outputs/curated/reference_payer_group.csv`
- `outputs/curated/reference_payer.csv`
- `outputs/curated/reference_payer_plan.csv`
- `outputs/curated/reference_relationship_payer_group_to_payer.csv`
- `outputs/curated/reference_relationship_payer_to_plan.csv`

##### Procedures
El modelo inicial de `PROCEDURE_CODE -> PROCEDURE_CODE` también fue reemplazado por tres niveles:

- `PROCEDURE_GROUP`
- `PROCEDURE_FAMILY`
- `PROCEDURE_CODE`

Y se regeneraron los archivos:

- `outputs/curated/reference_procedure_group.csv`
- `outputs/curated/reference_procedure_family.csv`
- `outputs/curated/reference_procedure_code.csv`
- `outputs/curated/reference_relationship_procedure_group_to_family.csv`
- `outputs/curated/reference_relationship_procedure_family_to_code.csv`

#### Jerarquías creadas
Con el rediseño anterior, quedaron listas las jerarquías compatibles con la herramienta:

- `PAYER_GROUP -> PAYER`
- `PAYER -> PAYER_PLAN`
- `PROCEDURE_GROUP -> PROCEDURE_FAMILY`
- `PROCEDURE_FAMILY -> PROCEDURE_CODE`

#### Resultado del milestone 3
Con esto quedó cubierto el núcleo funcional del milestone:

- listas canónicas para dominios ruidosos;
- estructura parent-child gobernada;
- separación entre registros válidos y registros con issues;
- evidencia de enforcement mediante exclusión de relaciones inválidas y carga de listas curadas en `Reference 360`.

#### Entregables técnicos consolidados
Al cierre de este paso, los principales artefactos de `Milestone 3` quedaron en:

- `scripts/build_reference_loads.py`
- `outputs/curated/reference_hospital.csv`
- `outputs/curated/reference_department.csv`
- `outputs/curated/reference_payer_group.csv`
- `outputs/curated/reference_payer.csv`
- `outputs/curated/reference_payer_plan.csv`
- `outputs/curated/reference_procedure_group.csv`
- `outputs/curated/reference_procedure_family.csv`
- `outputs/curated/reference_procedure_code.csv`
- `outputs/curated/reference_relationship_hospital_department.csv`
- `outputs/curated/reference_relationship_payer_group_to_payer.csv`
- `outputs/curated/reference_relationship_payer_to_plan.csv`
- `outputs/curated/reference_relationship_procedure_group_to_family.csv`
- `outputs/curated/reference_relationship_procedure_family_to_code.csv`
- `outputs/reports/reference_data_issues.csv`

#### Cierre operativo
Se consideró `Milestone 3` completado a nivel operativo, quedando como cierre documental recomendado:

- documentar explícitamente las reglas de estandarización;
- documentar evidencia de enforcement y carga exitosa en la herramienta.

### 6.1 Catálogo completo de archivos en las cuatro carpetas
En este milestone se extendió el catálogo a las cuatro carpetas de `Data_Source/`.

Resumen por carpeta:

| Carpeta | Tipo conceptual | Cantidad de archivos catalogados |
|---|---|---:|
| `1_Sources/` | fuentes maestras de pacientes | 5 |
| `2_Transactional/` | datos operacionales/transaccionales | 12 |
| `3_Reference/` | catálogos y jerarquías | 8 |
| `4_Master_Golden_Draft/` | borrador consolidado / golden draft | 2 |

Total catalogado: **27 artefactos**.

El catálogo completo quedó en:

- `outputs/reports/full_data_catalog.csv`

Este catálogo incluye por archivo:

- carpeta de origen;
- nombre de archivo;
- workbook y hoja cuando aplica;
- ruta relativa;
- cantidad de filas;
- cantidad de columnas;
- listado de columnas;
- clasificación conceptual.

Con esto queda cubierto explícitamente el entregable de:

- **A catalogue of every file**;
- **its columns**;
- **and row counts**.

#### Detalle resumido del catálogo completo

| Carpeta | Archivo | Filas | Columnas |
|---|---|---:|---:|
| `1_Sources/` | `Patients_EMR_Cerner.csv` | 1236 | 35 |
| `1_Sources/` | `Patients_EMR_Epic.csv` | 2002 | 35 |
| `1_Sources/` | `Patients_ManualEntry.csv` | 821 | 35 |
| `1_Sources/` | `Patients_MultiDomain_Conflicts.csv` | 22 | 35 |
| `1_Sources/` | `Patients_RegistrationDB.csv` | 1064 | 35 |
| `2_Transactional/` | `Admissions.csv` | 360 | 9 |
| `2_Transactional/` | `Appointments.csv` | 269 | 11 |
| `2_Transactional/` | `Billing.csv` | 263 | 13 |
| `2_Transactional/` | `Insurance_Claims.csv` | 258 | 11 |
| `2_Transactional/` | `Medical_Records.csv` | 212 | 20 |
| `2_Transactional/` | `Nurse_Assignments.csv` | 355 | 6 |
| `2_Transactional/` | `Patient_Insurance.csv` | 300 | 10 |
| `2_Transactional/` | `Patient_Procedures.csv` | 256 | 8 |
| `2_Transactional/` | `Prescription_Administration.csv` | 405 | 9 |
| `2_Transactional/` | `Prescriptions.csv` | 509 | 11 |
| `2_Transactional/` | `Referrals.csv` | 203 | 8 |
| `2_Transactional/` | `Visits.csv` | 410 | 12 |
| `3_Reference/` | `Data_Sources.csv` | 10 | 13 |
| `3_Reference/` | `Departments.csv` | 21 | 17 |
| `3_Reference/` | `Doctors.csv` | 622 | 12 |
| `3_Reference/` | `Hierarchy.csv` | 644 | 4 |
| `3_Reference/` | `Hospitals.csv` | 25 | 12 |
| `3_Reference/` | `Insurance_Provider_Hierarchy.csv` | 45 | 9 |
| `3_Reference/` | `Nurses.csv` | 120 | 11 |
| `3_Reference/` | `Procedure_Codes.csv` | 49 | 5 |
| `4_Master_Golden_Draft/` | `Patients_AllSources.csv` | 5123 | 35 |
| `4_Master_Golden_Draft/` | `HCLS.xlsx::Patients` | 5005 | 34 |
| `4_Master_Golden_Draft/` | `HCLS.xlsx::Hospitals` | 25 | 12 |
| `4_Master_Golden_Draft/` | `HCLS.xlsx::Departments` | 21 | 17 |
| `4_Master_Golden_Draft/` | `HCLS.xlsx::Doctors` | 620 | 12 |
| `4_Master_Golden_Draft/` | `HCLS.xlsx::Appointments` | 250 | 10 |
| `4_Master_Golden_Draft/` | `HCLS.xlsx::Medical_Records` | 206 | 19 |
| `4_Master_Golden_Draft/` | `HCLS.xlsx::Billing` | 250 | 12 |
| `4_Master_Golden_Draft/` | `HCLS.xlsx::Visits` | 400 | 12 |
| `4_Master_Golden_Draft/` | `HCLS.xlsx::Prescriptions` | 500 | 11 |
| `4_Master_Golden_Draft/` | `HCLS.xlsx::Insurance_Claims` | 250 | 11 |
| `4_Master_Golden_Draft/` | `HCLS.xlsx::Admissions` | 350 | 9 |
| `4_Master_Golden_Draft/` | `HCLS.xlsx::Hierarchy` | 641 | 4 |
| `4_Master_Golden_Draft/` | `HCLS.xlsx::Nurses` | 120 | 11 |
| `4_Master_Golden_Draft/` | `HCLS.xlsx::Nurse_Assignments` | 350 | 6 |
| `4_Master_Golden_Draft/` | `HCLS.xlsx::Referrals` | 200 | 8 |
| `4_Master_Golden_Draft/` | `HCLS.xlsx::Patient_Insurance` | 300 | 10 |
| `4_Master_Golden_Draft/` | `HCLS.xlsx::Prescription_Administration` | 400 | 9 |
| `4_Master_Golden_Draft/` | `HCLS.xlsx::Procedure_Codes` | 45 | 5 |
| `4_Master_Golden_Draft/` | `HCLS.xlsx::Patient_Procedures` | 250 | 8 |
| `4_Master_Golden_Draft/` | `HCLS.xlsx::Referential_Integrity` | 20 | 5 |

Con esto, `HCLS.xlsx` ya quedó inspeccionado hoja por hoja dentro del catálogo automatizado.

#### Resumen de calidad para las fuentes de pacientes

| Archivo | Filas | Columnas | Filas con `patient_id` duplicado | Issues detectados |
|---|---:|---:|---:|---:|
| `Patients_EMR_Cerner.csv` | 1236 | 35 | 34 | 491 |
| `Patients_EMR_Epic.csv` | 2002 | 35 | 96 | 797 |
| `Patients_ManualEntry.csv` | 821 | 35 | 20 | 346 |
| `Patients_MultiDomain_Conflicts.csv` | 22 | 35 | 12 | 49 |
| `Patients_RegistrationDB.csv` | 1064 | 35 | 40 | 440 |

Observaciones tempranas:

- los cinco archivos comparten la misma estructura de 35 columnas;
- `Patients_MultiDomain_Conflicts.csv` es pequeño, pero no por eso “sano”; de hecho concentra conflictos intencionales;
- los extractos de pacientes claramente se superponen;
- hay evidencia de duplicidad e inconsistencias entre fuentes.

Con esto queda cubierto explícitamente el segundo entregable de:

- **A first read of data quality per file**;
- con una medida aproximada de **rough % of obvious garbage** para los archivos fuente de pacientes.

### 6.2 Primera lectura de calidad por archivo
Sin sacar conclusiones finales todavía, la primera lectura muestra basura obvia como:

- emails inválidos: `user@.com`, `not-an-email`, vacíos;
- nombres inválidos o placeholders: `###`, `UNKNOWN`, vacíos;
- `patient_id` faltante, duplicado o negativo;
- fechas imposibles o sospechosas: `2099-06-15`, `1800-01-01`, `tomorrow`, `2025-13-01`;
- `height_cm`, `weight_kg` y `bmi` fuera de rango o no numéricos;
- `blood_type` fuera del dominio esperado;
- `patient_status` con casing inconsistente;
- teléfonos placeholder como `000-000-0000`;
- direcciones con JSON mal formado.

Como lectura rápida de “rough % of obvious garbage”, el volumen de issues detectados sobre filas por archivo es aproximadamente:

| Archivo | Issues / filas |
|---|---:|
| `Patients_EMR_Cerner.csv` | 39.7% |
| `Patients_EMR_Epic.csv` | 39.8% |
| `Patients_ManualEntry.csv` | 42.1% |
| `Patients_MultiDomain_Conflicts.csv` | 222.7% |
| `Patients_RegistrationDB.csv` | 41.4% |

**Nota:** este porcentaje no significa “porcentaje exacto de registros malos”, porque una fila puede tener múltiples issues. Se usa solo como **indicador temprano de densidad de problemas obvios**.

### 6.3 Ejemplos de hallazgos tempranos
- `Patients_EMR_Cerner.csv` contiene `blood_type = AB` sin signo.
- `Patients_EMR_Cerner.csv` contiene `bmi = normal` y alturas como `9999`.
- `Patients_EMR_Epic.csv` contiene `email = user@.com` y nombres faltantes.
- `Patients_ManualEntry.csv` contiene `registration_date = 2025-13-01`, `bmi = -5`, `date_of_birth = 2099-06-15`.
- `Patients_MultiDomain_Conflicts.csv` contiene conflictos explícitos de identidad y `patient_id` negativos.
- `Patients_RegistrationDB.csv` contiene formatos mixtos y placeholders en varios campos.

---

## 7. Qué falta para completar totalmente el requerimiento del milestone

### 7.1 Catálogo de **every file** en las cuatro carpetas
Estado actual:

- **completo para las cuatro carpetas a nivel de inventario estructural**;
- **completo incluyendo la inspección hoja por hoja de `HCLS.xlsx`**.

Es decir: el requerimiento de catálogo ya quedó cubierto en términos de inventario, filas, columnas y clasificación conceptual.

Esto incluye de forma explícita:

- every file;
- its columns;
- row counts.

### 7.2 Memo corto al CIO
Estado actual:

- **completo** en `docs/milestone-1-memo-cio.md`

El memo quedó redactado en tono descriptivo y sin conclusiones definitivas.

---

## 8. Clasificación conceptual de los cuatro grupos de datos

### `Data_Source/1_Sources/`
Extractos fuente crudos de pacientes desde múltiples sistemas.

### `Data_Source/2_Transactional/`
Datos operacionales/transaccionales para validar uso, relaciones y futura integridad referencial.

### `Data_Source/3_Reference/`
Catálogos y jerarquías de soporte: hospitales, departamentos, doctores, enfermeros, procedimientos, aseguradoras.

### `Data_Source/4_Master_Golden_Draft/`
Borrador consolidado del maestro/golden patient list para comparación conceptual, no como verdad absoluta.

---

## 9. Posicionamiento: cloud MDM vs on-premises

Para este capstone, el valor de **cloud MDM** frente a un enfoque on-premises se puede resumir así:

### Ventajas de cloud MDM
- menor tiempo de puesta en marcha;
- servicios administrados;
- escalabilidad más simple;
- integración nativa con servicios cloud de calidad, integración y gobierno;
- menor carga operativa de infraestructura;
- mejor alineación con un modelo SaaS para dominios maestros compartidos.

### Limitaciones típicas de on-premises
- mayor esfuerzo de instalación y mantenimiento;
- upgrades más pesados;
- más dependencia de infraestructura local;
- menor agilidad para iterar rápidamente en un MVP.

Para este proyecto, la propuesta conceptual es apoyarse en **IDMC / Informatica Cloud** para pasar del análisis offline a una implementación gobernada.

---

## 10. Servicios IDMC / Informatica Cloud y flujo conceptual

Servicios conceptuales a utilizar:

- **Cloud Data Integration** para ingesta y transformación;
- **Cloud Data Quality** para profiling, reglas y validación;
- **MDM SaaS / Business 360 / Customer 360** para consolidación, match/merge y golden record;
- **Reference 360** si se decide gobernar catálogos y jerarquías de referencia;
- APIs / servicios de publicación para consumo posterior.

Flujo conceptual propuesto:

1. Ingesta de CSV fuente.
2. Profiling y data quality.
3. Estandarización.
4. Match y survivorship.
5. Construcción del golden record.
6. Validación con transaccionales y referencias.
7. Exposición y gobierno del dato maestro.

---

## 10.1 Ejecución de Data Profiling en MDM Cloud

Para avanzar del profiling offline a una medición más alineada con la plataforma objetivo, se ejecutó **Data Profiling directamente en MDM Cloud / IDMC**.

### Configuración realizada
- se creó una conexión de profiling apuntando a la carpeta donde estaban los extractos fuente de pacientes;
- se configuró un **profile job por archivo** para los cinco extractos de `Data_Source/1_Sources/`;
- se ejecutaron perfiles individuales para:
  - `Patients_EMR_Epic.csv`
  - `Patients_EMR_Cerner.csv` *(exportado con typo como `Center` en el nombre del Excel)*
  - `Patients_RegistrationDB.csv`
  - `Patients_ManualEntry.csv`
  - `Patients_MultiDomain_Conflicts.csv`
- cada ejecución generó un workbook de salida con hojas como:
  - `Column Profile`
  - `Values`
  - `Statistics`
  - `Patterns`
  - `Data Types`
  - `Properties`

### Export de resultados
Los resultados se exportaron a:

- `outputs/profiling/Patients_EMR_Epic_Summary.xlsx`
- `outputs/profiling/Patients_EMR_Center_Summary.xlsx`
- `outputs/profiling/Patients_EMR_RegistrationDB_Summary.xlsx`
- `outputs/profiling/Patients_EMR_ManualEntry_Summary.xlsx`
- `outputs/profiling/Patients_EMR_MultiDomain_Conflicts_Summary.xlsx`

Con esto se obtuvo evidencia reproducible desde la propia herramienta de profiling de Informatica, sin modificar los datos fuente.

### Requerimientos que debíamos cubrir en este paso
El objetivo del step era responder con evidencia a estas preguntas de negocio:

- qué fuente es más completa para `name`, `DOB`, `email`, `phone` e `insurance`;
- qué fuente tiene más valores nulos, vacíos o inválidos;
- qué sistema puede actuar como **trust anchor** por atributo;
- qué resumen honesto puede presentar el CIO al board.

Los entregables esperados eran:

- un **per-source completeness/quality report**;
- un **ranking claro por atributo**;
- un **data profiling summary** listo para comunicación ejecutiva.

### Cómo resolvimos el análisis con una skill reutilizable
Para no hacer la consolidación manual de cada Excel, se creó una skill nueva:

- `.github/skills/profiling-summary/SKILL.md`

La skill se diseñó para:

- leer exports de profiling desde `outputs/profiling/`;
- identificar métricas por fuente y por atributo;
- separar **blank/null** de **invalid**;
- cruzar resultados con `Data_Source/3_Reference/Data_Sources.csv` para incorporar:
  - `trust_score`
  - `data_quality_score`
- detectar patrones esperados como:
  - emails inválidos;
  - DOB fuera de rango;
  - phone-like strings en email;
  - SSN/PII en campos incorrectos;
- producir entregables listos para negocio.

### Entregables generados a partir de la skill
Con los exports de MDM Cloud y la skill de resumen se generaron:

- `outputs/reports/profiling_scorecard.csv`
- `outputs/reports/profiling_ranking.md`
- `outputs/reports/profiling_cio_summary.md`

Estos artefactos cubren el cierre del step de profiling porque permiten:

- comparar fuentes por atributo;
- proponer trust anchors;
- documentar hallazgos clave;
- dejar un resumen ejecutivo trazable.

### Limitaciones observadas
Los workbooks exportados desde profiling contienen **resúmenes** y no siempre incluyen el detalle completo de:

- `rule occurrences`
- `exception records`
- evidencia exhaustiva de todos los inválidos

Por eso, el scorecard generado debe interpretarse como una **primera consolidación basada en profiling summary exports**. Si se requiere una versión final más fuerte para board-level review, conviene exportar también exceptions y rule occurrences desde IICS.

---

## 11. Estado del milestone 1 al cierre de esta bitácora

### Ya logrado
- estructura del repo revisada;
- primer entregable offline definido;
- profiling reproducible implementado para `1_Sources/`;
- catálogo completo de las cuatro carpetas generado;
- catálogo completo con columnas y row counts documentado;
- reglas iniciales documentadas;
- reportes generados;
- primera lectura de calidad disponible;
- primera lectura de calidad por archivo documentada;
- data profiling ejecutado en MDM Cloud / IDMC sobre los extractos fuente;
- exports de profiling por archivo generados y almacenados en `outputs/profiling/`;
- skill reutilizable creada para resumir exports de profiling;
- scorecard, ranking y resumen CIO generados desde los exports de profiling;
- base para notebook exploratorio creada;
- memo corto al CIO generado.

### Pendiente para cerrar milestone 1 al 100%
- consolidar una vista única final para presentación si se quiere empaquetar el milestone como entrega ejecutiva.

---

## 12. Próximo paso recomendado

Extender ahora el mismo enfoque de **profiling de calidad e integridad** a:

- `Data_Source/2_Transactional/`
- `Data_Source/3_Reference/`
- hojas relevantes de `Data_Source/4_Master_Golden_Draft/HCLS.xlsx`

para pasar del inventario estructural a validaciones de relaciones, orfandades y consistencia entre dominios.