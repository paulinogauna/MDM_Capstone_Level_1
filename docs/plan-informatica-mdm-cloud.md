# Plan de implementación paso a paso — Informatica MDM Cloud

## Objetivo
Definir un plan de ejecución del proyecto usando **Informatica MDM Cloud / Informatica Intelligent Cloud Services (IICS)** como plataforma principal, evitando una implementación basada en Python. El foco es construir un flujo funcional de MDM para pacientes, desde la preparación de fuentes hasta la consolidación del golden record y su gobierno operativo.

## Alcance del proyecto
Este proyecto trabajará sobre datos de pacientes provenientes de múltiples sistemas fuente, tablas transaccionales y tablas de referencia. El objetivo es usar capacidades de Informatica Cloud para:
- ingestar y perfilar datos,
- evaluar calidad,
- estandarizar atributos,
- detectar duplicados,
- definir reglas de match/merge,
- construir golden records,
- validar relaciones y jerarquías,
- y preparar una operación gobernada del dominio maestro.

## Supuestos
- `Data_Source/` se usa como fuente de entrada de laboratorio.
- Los archivos fuente no se modifican.
- Los resultados del análisis y documentación se guardan en `outputs/` y `docs/`.
- La implementación funcional se realizará en Informatica Cloud, no en scripts Python.
- El dominio inicial es **Patient MDM**.

---

## Fase 1 — Definición funcional y alcance MDM
**Objetivo:** dejar claro qué resolverá el proyecto dentro de Informatica MDM Cloud.

### Actividades
1. Definir el dominio maestro principal: **Pacientes**.
2. Identificar dominios relacionados:
   - hospitales,
   - departamentos,
   - doctores,
   - enfermeros,
   - procedimientos,
   - aseguradoras.
3. Definir objetivos de negocio:
   - consolidar pacientes desde múltiples fuentes,
   - detectar duplicados,
   - resolver conflictos de identidad,
   - construir golden record,
   - mantener trazabilidad entre source record y master record.
4. Definir alcance inicial del MVP:
   - solo pacientes como dominio maestro principal,
   - referencias y transaccionales como soporte de validación,
   - sin integración en tiempo real en la primera iteración.

### Entregables
- Documento de alcance funcional.
- Lista de entidades y atributos críticos.
- Definición del MVP.

---

## Fase 2 — Inventario y análisis de fuentes
**Objetivo:** entender qué fuentes entrarán al modelo MDM y cómo se usarán en Informatica.

### Actividades
1. Clasificar datasets:
   - `1_Sources/` como sistemas fuente maestros.
   - `2_Transactional/` como validación y contexto operacional.
   - `3_Reference/` como catálogos y jerarquías.
   - `4_Master_Golden_Draft/` como referencia comparativa.
2. Identificar por cada fuente:
   - nombre del sistema,
   - tipo de archivo,
   - frecuencia esperada,
   - entidad principal,
   - clave de negocio,
   - calidad esperada.
3. Mapear equivalencias entre columnas de pacientes de distintas fuentes.
4. Identificar atributos obligatorios para match y survivorship.
5. Identificar problemas conocidos del dataset:
   - emails inválidos,
   - nombres numéricos,
   - PII en campos libres,
   - huérfanos,
   - jerarquías rotas,
   - duplicados exactos y fuzzy.

### Entregables
- Inventario de fuentes.
- Matriz source-to-entity.
- Matriz de atributos críticos.

---

## Fase 3 — Diseño del modelo maestro en Informatica MDM Cloud
**Objetivo:** definir cómo se representará el dominio Patient dentro de Informatica.

### Actividades
1. Diseñar la entidad maestra **Patient**.
2. Definir atributos principales:
   - identificadores fuente,
   - nombre,
   - apellido,
   - fecha de nacimiento,
   - género,
   - email,
   - teléfono,
   - dirección,
   - identificadores clínicos o administrativos.
3. Definir relaciones con entidades de referencia.
4. Definir si habrá entidades relacionadas separadas o atributos embebidos.
5. Diseñar el crosswalk entre source records y master record.
6. Definir atributos de auditoría y trazabilidad.

### Entregables
- Modelo lógico del dominio Patient.
- Definición de atributos maestros.
- Diseño de crosswalk.

---

## Fase 4 — Preparación del ambiente en Informatica Cloud
**Objetivo:** dejar lista la plataforma para comenzar la implementación.

### Actividades
1. Confirmar acceso a Informatica Intelligent Cloud Services.
2. Identificar servicios disponibles:
   - Cloud Data Integration,
   - Cloud Data Quality,
   - MDM SaaS / Customer 360 / Business 360 según licencia,
   - Reference 360 si aplica,
   - API Manager si aplica.
3. Definir ambientes:
   - desarrollo,
   - prueba,
   - productivo futuro.
4. Configurar conexiones a archivos o almacenamiento donde residan las fuentes.
5. Definir estrategia de carga inicial y cargas incrementales.
6. Definir roles de trabajo:
   - administrador,
   - implementador,
   - steward,
   - consumidor de datos.

### Entregables
- Checklist de ambiente Informatica.
- Lista de conexiones y accesos.
- Estrategia de ambientes.

---

## Fase 5 — Ingesta y landing de datos
**Objetivo:** cargar las fuentes al entorno de trabajo de Informatica.

### Actividades
1. Configurar conexiones a archivos CSV/XLSX.
2. Crear tareas de ingesta o mappings para cada fuente.
3. Definir naming convention para objetos de Informatica.
4. Cargar datasets de pacientes por fuente.
5. Cargar datasets de referencia.
6. Cargar datasets transaccionales para validación posterior.
7. Validar conteos de registros cargados.

### Entregables
- Objetos de ingesta creados.
- Landing datasets disponibles.
- Validación de conteos por fuente.

---

## Fase 6 — Profiling y data quality en Informatica
**Objetivo:** usar capacidades de profiling y calidad para medir el estado real de los datos.

### Actividades
1. Ejecutar profiling sobre fuentes de pacientes.
2. Medir:
   - completitud,
   - unicidad,
   - patrones,
   - dominios,
   - valores inválidos.
3. Crear reglas de calidad para:
   - email válido,
   - nombres no numéricos,
   - identificadores obligatorios,
   - detección de PII en campos libres,
   - formatos esperados.
4. Ejecutar profiling sobre referencias y transaccionales.
5. Documentar hallazgos y severidad.

### Entregables
- Reporte de profiling.
- Catálogo de reglas de calidad.
- Lista priorizada de issues.

---

## Fase 7 — Estandarización y normalización
**Objetivo:** preparar los datos para matching y consolidación.

### Actividades
1. Definir reglas de estandarización para nombres.
2. Normalizar teléfonos y emails.
3. Homogeneizar formatos de fecha.
4. Estandarizar valores de género, estado y otros dominios.
5. Resolver diferencias de formato entre sistemas fuente.
6. Definir qué transformaciones ocurren antes del match.

### Entregables
- Reglas de estandarización.
- Diseño de transformaciones previas al match.

---

## Fase 8 — Integridad referencial y jerarquías
**Objetivo:** validar consistencia entre maestros, referencias y transaccionales.

### Actividades
1. Validar `patient_id` en tablas transaccionales.
2. Detectar registros huérfanos.
3. Validar relaciones hospital-departamento.
4. Validar jerarquías de procedimientos.
5. Validar jerarquías de aseguradoras.
6. Detectar ciclos, padres inexistentes y relaciones inválidas.

### Entregables
- Reporte de integridad referencial.
- Reporte de jerarquías inválidas.

---

## Fase 9 — Diseño de match rules
**Objetivo:** definir cómo Informatica identificará duplicados y posibles merges.

### Actividades
1. Definir criterios de match exacto.
2. Definir criterios de match probabilístico o fuzzy.
3. Identificar atributos de alta confianza:
   - documento,
   - DOB,
   - email,
   - teléfono,
   - nombre + apellido.
4. Diseñar survivorship preliminar alineado al match.
5. Configurar thresholds de confianza.
6. Probar casos conocidos del dataset.

### Entregables
- Matriz de reglas de match.
- Configuración de thresholds.
- Casos de prueba de matching.

---

## Fase 10 — Merge, survivorship y golden record
**Objetivo:** consolidar registros en un master record confiable.

### Actividades
1. Definir reglas de survivorship por atributo.
2. Definir precedencia entre fuentes.
3. Configurar merge automático o asistido.
4. Diseñar el golden record de paciente.
5. Mantener crosswalk con IDs fuente.
6. Validar trazabilidad completa.

### Entregables
- Matriz de survivorship.
- Diseño del golden record.
- Estrategia de merge.

---

## Fase 11 — Stewardship y gobierno operativo
**Objetivo:** preparar la operación del dominio maestro dentro de Informatica.

### Actividades
1. Definir qué casos requieren revisión manual.
2. Diseñar colas de stewardship.
3. Definir roles y responsabilidades.
4. Definir métricas operativas:
   - duplicados detectados,
   - merges aprobados,
   - registros rechazados,
   - issues de calidad abiertos.
5. Definir proceso de remediación con sistemas fuente.

### Entregables
- Modelo operativo de stewardship.
- KPIs de gobierno.
- Flujo de remediación.

---

## Fase 12 — Publicación y consumo
**Objetivo:** definir cómo se consumirá el master data consolidado.

### Actividades
1. Definir salidas del golden record.
2. Definir si habrá exportación batch, APIs o vistas.
3. Definir consumidores:
   - analítica,
   - operaciones,
   - sistemas clínicos,
   - sistemas administrativos.
4. Definir frecuencia de publicación.
5. Definir estrategia de sincronización con sistemas fuente.

### Entregables
- Diseño de publicación.
- Lista de consumidores.
- Estrategia de sincronización.

---

## Fase 13 — Pruebas integrales
**Objetivo:** validar que la solución MDM cumple el objetivo funcional.

### Actividades
1. Ejecutar pruebas de carga inicial.
2. Ejecutar pruebas de calidad.
3. Ejecutar pruebas de matching con casos conocidos.
4. Ejecutar pruebas de merge y survivorship.
5. Validar golden record contra casos esperados.
6. Validar trazabilidad y auditoría.

### Entregables
- Plan de pruebas.
- Evidencia de resultados.
- Lista de ajustes pendientes.

---

## Fase 14 — Go-live controlado
**Objetivo:** preparar una salida controlada a operación.

### Actividades
1. Definir alcance del primer release.
2. Cargar subconjunto o lote controlado.
3. Monitorear calidad y merges.
4. Ajustar reglas según resultados.
5. Formalizar operación recurrente.

### Entregables
- Plan de salida.
- Checklist de go-live.
- Plan de soporte inicial.

---

## Orden recomendado de ejecución
1. Alcance funcional.
2. Inventario de fuentes.
3. Modelo maestro.
4. Setup de Informatica Cloud.
5. Ingesta.
6. Profiling y calidad.
7. Estandarización.
8. Integridad referencial y jerarquías.
9. Match rules.
10. Survivorship y golden record.
11. Stewardship.
12. Publicación.
13. Pruebas.
14. Go-live controlado.

---

## MVP recomendado
Para una primera versión, el MVP debería incluir:
- dominio **Patient**,
- 4 fuentes maestras de pacientes,
- reglas básicas de calidad,
- match exacto + fuzzy básico,
- survivorship inicial,
- golden record,
- crosswalk,
- revisión manual de casos ambiguos.

No incluir en el MVP:
- integraciones en tiempo real,
- automatización avanzada multi-dominio,
- gobierno extendido para todos los catálogos,
- APIs complejas de consumo.

---

## Riesgos principales
- mala calidad de identificadores fuente,
- conflictos de identidad entre sistemas,
- falta de reglas claras de survivorship,
- jerarquías inconsistentes en referencias,
- exceso de falsos positivos o falsos negativos en matching,
- falta de definición operativa para stewardship.

---

## Próximos pasos inmediatos
1. Documentar atributos críticos del dominio Patient.
2. Crear inventario formal de fuentes.
3. Definir modelo maestro inicial.
4. Confirmar qué módulos/licencias de Informatica Cloud están disponibles.
5. Diseñar la primera iteración del flujo de ingesta + profiling + quality + match.
