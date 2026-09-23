# Milestone 3 — The Reference Data Mess

## 1. Objetivo del milestone
Resolver el desorden en datos de referencia para que los reportes, la estandarización y el MDM trabajen sobre listas canónicas gobernadas en lugar de valores ambiguos o inconsistentes.

Problemas de negocio abordados:

- múltiples variantes de pagadores;
- departamentos con abreviaturas y nombres inconsistentes;
- jerarquías rotas entre hospitales y departamentos;
- procedimientos con padres faltantes, duplicados y categorías ambiguas;
- necesidad de modelar reference data como estructura gobernada con ownership, null handling y versioning básico.

---

## 2. Decisión de diseño
Se decidió usar `Data_Source/3_Reference/` como fuente base para construir los catálogos canónicos iniciales y usar profiling adicional como complemento para detectar aliases, valores fuera de catálogo y conflictos semánticos.

También se decidió modelar el milestone en `Reference 360` con:

- un único `Reference Data Set` contenedor;
- múltiples `Code Lists` por dominio;
- jerarquías separadas cuando la herramienta no soporta self-hierarchy sobre la misma lista.

---

## 3. Insumos revisados
Se revisaron los siguientes archivos de referencia:

- `Data_Source/3_Reference/Hospitals.csv`
- `Data_Source/3_Reference/Departments.csv`
- `Data_Source/3_Reference/Hierarchy.csv`
- `Data_Source/3_Reference/Insurance_Provider_Hierarchy.csv`
- `Data_Source/3_Reference/Procedure_Codes.csv`
- `Data_Source/3_Reference/Data_Sources.csv`

Hallazgos principales:

- había suficiente material para construir listas canónicas;
- las jerarquías contenían errores intencionales o inconsistencias;
- no era seguro cargar los archivos crudos directamente en `Reference 360`;
- era necesaria una capa curada y un backlog de issues.

---

## 4. Curación y generación de archivos de carga
Se creó el script:

- `scripts/build_reference_loads.py`

Este script:

- lee los CSV de `Data_Source/3_Reference/`;
- genera archivos curados en `outputs/curated/`;
- separa entidades y relaciones;
- expande algunos nombres canónicos de departamentos;
- excluye relaciones inválidas;
- genera un reporte de issues para revisión steward.

Reporte de issues generado:

- `outputs/reports/reference_data_issues.csv`

---

## 5. Restricción encontrada en Reference 360
Durante la configuración se detectó que la herramienta no permitía crear una jerarquía usando la misma code list como padre e hijo.

Esto obligó a rediseñar dos dominios:

### 5.1 Payers
El modelo inicial de una sola lista fue reemplazado por:

- `PAYER_GROUP`
- `PAYER`
- `PAYER_PLAN`

Relaciones:

- `PAYER_GROUP -> PAYER`
- `PAYER -> PAYER_PLAN`

### 5.2 Procedures
El modelo inicial de una sola lista fue reemplazado por:

- `PROCEDURE_GROUP`
- `PROCEDURE_FAMILY`
- `PROCEDURE_CODE`

Relaciones:

- `PROCEDURE_GROUP -> PROCEDURE_FAMILY`
- `PROCEDURE_FAMILY -> PROCEDURE_CODE`

---

## 6. Code lists finales cargadas
Se cargaron o dejaron listas para carga las siguientes code lists:

- `HOSPITAL`
- `DEPARTMENT`
- `PAYER_GROUP`
- `PAYER`
- `PAYER_PLAN`
- `PROCEDURE_GROUP`
- `PROCEDURE_FAMILY`
- `PROCEDURE_CODE`

---

## 7. Archivos curados generados
### Entidades
- `outputs/curated/reference_hospital.csv`
- `outputs/curated/reference_department.csv`
- `outputs/curated/reference_payer_group.csv`
- `outputs/curated/reference_payer.csv`
- `outputs/curated/reference_payer_plan.csv`
- `outputs/curated/reference_procedure_group.csv`
- `outputs/curated/reference_procedure_family.csv`
- `outputs/curated/reference_procedure_code.csv`

### Relaciones
- `outputs/curated/reference_relationship_hospital_department.csv`
- `outputs/curated/reference_relationship_payer_group_to_payer.csv`
- `outputs/curated/reference_relationship_payer_to_plan.csv`
- `outputs/curated/reference_relationship_procedure_group_to_family.csv`
- `outputs/curated/reference_relationship_procedure_family_to_code.csv`

### Issues
- `outputs/reports/reference_data_issues.csv`

---

## 8. Problemas detectados y tratados
Se detectaron y documentaron problemas como:

- `accreditation=None` en hospitales;
- años sospechosos como `1800`;
- referencias inválidas a doctores en departamentos;
- relaciones `hospital_id` fuera del catálogo;
- payers con padres inexistentes o autorreferencia;
- procedimientos con padres faltantes;
- nombres duplicados en procedimientos;
- categorías `Unknown`.

Tratamiento aplicado:

- exclusión de relaciones inválidas de la carga;
- separación de niveles jerárquicos;
- conservación de issues para revisión steward;
- carga de listas canónicas curadas en lugar de archivos crudos.

---

## 9. Deliverables logrados
### 9.1 Standard code lists for the noisy domains
Cumplido mediante las code lists canónicas para hospitales, departamentos, pagadores y procedimientos.

### 9.2 Lookup / standardisation rule set
Cumplido parcialmente en la lógica del script y en la curación aplicada. Recomendado formalizarlo en un documento adicional de reglas.

### 9.3 Proof that the canonical lists are being enforced
Cumplido operativamente mediante:

- exclusión de relaciones inválidas;
- carga de listas curadas;
- separación entre registros válidos y backlog de issues;
- jerarquías compatibles con la herramienta.

---

## 10. Conclusión
`Milestone 3` quedó completado a nivel operativo.

Se logró:

- construir listas canónicas para dominios ruidosos;
- reconciliar parte de las inconsistencias entre catálogos y jerarquías;
- adaptar el modelo a las restricciones reales de `Reference 360`;
- dejar listas y jerarquías cargables y gobernables;
- generar evidencia técnica y backlog de issues para stewardship.

Siguiente recomendación:

- formalizar reglas de estandarización en `rules/`;
- documentar evidencia de enforcement con capturas o notas de carga;
- avanzar al siguiente milestone usando estos catálogos como base gobernada.
