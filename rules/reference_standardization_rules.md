# Reference Standardization Rules

## Objetivo
Definir las reglas de estandarización, validación y tratamiento de excepciones para los dominios de referencia gobernados en `Milestone 3`, de modo que `Reference 360` opere con listas canónicas y relaciones válidas.

## Alcance
Aplica a los dominios curados desde `Data_Source/3_Reference/` y cargados o preparados para carga en `Reference 360`:

- `HOSPITAL`
- `DEPARTMENT`
- `HOSPITAL_DEPARTMENT_REL`
- `PAYER_GROUP`
- `PAYER`
- `PAYER_PLAN`
- `PROCEDURE_GROUP`
- `PROCEDURE_FAMILY`
- `PROCEDURE_CODE`
- relaciones jerárquicas de payer y procedure

## Principios de gobierno
- No se cargan archivos crudos directamente desde `Data_Source/3_Reference/`.
- Toda carga gobernada debe salir de `outputs/curated/`.
- Todo valor inválido, ambiguo o incompleto debe quedar en una de estas dos situaciones:
  - excluido de la carga gobernada;
  - cargado con estado controlado y marcado para revisión steward.
- Toda excepción detectada debe registrarse en `outputs/reports/reference_data_issues.csv`.

---

## 1. Reglas generales

### 1.1 Identificadores
- Todo registro de referencia debe tener identificador técnico no vacío.
- El identificador debe ser único dentro de su code list.
- Si falta el identificador o no es confiable, el registro no debe cargarse.

### 1.2 Nombre canónico
- Todo registro debe tener un nombre de negocio legible.
- Cuando exista variante abreviada o alias, debe mapearse a un `canonical_name` o equivalente.
- Si hay duplicados semánticos, deben quedar para revisión antes de consolidar catálogo productivo.

### 1.3 Estado
- Los registros válidos para uso operativo deben quedar como `Approved`.
- Los registros inactivos o no vigentes pueden quedar como `Retired`.
- Los registros con estructura inválida no deben quedar `Approved` automáticamente.

### 1.4 Relaciones
- Ninguna relación parent-child debe cargarse si el padre no existe en el catálogo curado.
- Ninguna relación parent-child debe cargarse si el hijo no existe en el catálogo curado.
- No se permiten autorreferencias.
- No se permiten jerarquías con niveles incompatibles.

---

## 2. Reglas por dominio

## 2.1 HOSPITAL
### Reglas
- `hospital_id` es obligatorio.
- `hospital_name` es obligatorio.
- `canonical_name` debe reflejar el nombre estándar del hospital.
- `accreditation` no debe contener placeholders como `None`, `N/A`, `Unknown`, `Null`.
- `established_year` debe ser numérico.
- `established_year` debe estar en rango razonable para negocio.

### Tratamiento
- Si `accreditation` contiene placeholder, el hospital puede permanecer en catálogo pero debe quedar con issue para revisión.
- Si `established_year` es inválido o sospechoso, debe quedar issue para steward.

### Evidencia actual
Ejemplos detectados en `outputs/reports/reference_data_issues.csv`:
- `HOSPITAL,3,placeholder_value,accreditation,None`
- `HOSPITAL,18,suspicious_year,established_year,1800`

---

## 2.2 DEPARTMENT
### Reglas
- `department_id` es obligatorio.
- `department_name` es obligatorio.
- Debe existir una forma canónica cuando haya abreviaturas.
- Referencias a doctores responsables no deben usar valores dummy como `-1`, `888`, `999`, `9999`.

### Estandarización aplicada
Se normalizan abreviaturas frecuentes, por ejemplo:
- `Internal Med` -> `Internal Medicine`
- `Family Med` -> `Family Medicine`
- `Emergency Med` -> `Emergency Medicine`
- `ENT` -> `Ear, Nose, and Throat`
- `Gastro` -> `Gastroenterology`

### Tratamiento
- El departamento puede cargarse como catálogo si su identidad es válida.
- Las referencias inválidas a doctores quedan en revisión y documentadas como issue.

### Evidencia actual
Ejemplos detectados:
- `DEPARTMENT,1,invalid_reference,subhead_doctor_id,999`
- `DEPARTMENT,20,invalid_reference,head_doctor_id,888`

---

## 2.3 HOSPITAL_DEPARTMENT_REL
### Reglas
- Toda relación debe tener hospital padre existente.
- Toda relación debe tener department hijo existente.
- Si falta padre o hijo, la relación no debe cargarse.

### Tratamiento
- Relaciones con `missing_parent` o `missing_child` se excluyen del archivo curado final.
- El issue queda registrado para remediación.

### Evidencia actual
Ejemplos detectados:
- `HOSPITAL_DEPARTMENT_REL,68,missing_parent,hospital_id,99`
- `HOSPITAL_DEPARTMENT_REL,206,missing_child,department_id,99`

---

## 2.4 PAYER_GROUP / PAYER / PAYER_PLAN
### Reglas
- `provider_id` es obligatorio.
- `provider_name` es obligatorio.
- `tier` debe mapearse a un nivel soportado:
  - `1` -> `PAYER_GROUP`
  - `2` -> `PAYER`
  - `3` -> `PAYER_PLAN`
- `is_active=true` se normaliza a `Approved`.
- `is_active=false` se normaliza a `Retired`.
- No se permiten autorreferencias en `parent_provider_id`.
- No se permiten padres inexistentes.
- No se permiten relaciones entre tiers incompatibles.

### Tratamiento
- Si el tier no es soportado, el registro queda con issue.
- Si el padre no existe, la relación no se carga.
- Si el padre y el hijo no respetan la secuencia de niveles, la relación no se carga.
- Si un hijo activo apunta a un padre retirado, debe quedar issue para revisión.

### Validación jerárquica esperada
- `PAYER_GROUP -> PAYER`
- `PAYER -> PAYER_PLAN`

---

## 2.5 PROCEDURE_GROUP / PROCEDURE_FAMILY / PROCEDURE_CODE
### Reglas
- `code_id` es obligatorio.
- `procedure_name` es obligatorio.
- La jerarquía debe resolverse por `parent_code_id`.
- No se permiten referencias circulares.
- No se permiten padres inexistentes.
- No se permiten profundidades no soportadas.
- Los nombres duplicados deben revisarse antes de consolidación final.

### Tratamiento
- Si el padre no existe, la relación queda fuera de la carga.
- Si hay circularidad, el registro queda en revisión.
- Si la profundidad excede el modelo soportado, queda issue.
- Si hay duplicados semánticos, queda issue para decisión steward.

### Validación jerárquica esperada
- `PROCEDURE_GROUP -> PROCEDURE_FAMILY`
- `PROCEDURE_FAMILY -> PROCEDURE_CODE`

---

## 3. Cómo evidenciar enforcement
La evidencia de enforcement puede demostrarse en tres niveles.

### 3.1 Evidencia por exclusión en archivos curados
Si una relación inválida aparece en `reference_data_issues.csv` pero no aparece en el archivo curado de salida, eso demuestra rechazo o exclusión previa a la carga.

Ejemplo:
- si una fila tiene `missing_parent` en `HOSPITAL_DEPARTMENT_REL`, esa relación no debe existir en `outputs/curated/reference_relationship_hospital_department.csv`.

### 3.2 Evidencia por backlog de revisión
Si un valor no se rechaza completamente pero tampoco se considera limpio, debe quedar documentado en:
- `outputs/reports/reference_data_issues.csv`

Esto evidencia que el valor quedó en revisión steward.

### 3.3 Evidencia por validación en la herramienta
En `Reference 360`, la evidencia puede mostrarse con:
- rechazo de carga por clave o relación inválida;
- ausencia del valor fuera de catálogo en la code list publicada;
- estado `Retired` o equivalente cuando aplique;
- capturas o export de resultados de importación.

---

## 4. Qué significa valor inválido en este milestone
Se considera inválido cualquiera de estos casos:
- placeholder en atributos críticos;
- referencia a padre inexistente;
- referencia a hijo inexistente;
- autorreferencia;
- tier no soportado;
- profundidad jerárquica no soportada;
- circularidad;
- identificador faltante o inconsistente;
- nombre duplicado que impide consolidación segura.

---

## 5. Resultado esperado de control
Todo valor fuera de catálogo o relación inválida debe terminar en uno de estos estados:

1. **Rechazado / excluido**
   - no aparece en el CSV curado final;
   - aparece en `reference_data_issues.csv`.

2. **En revisión**
   - aparece en catálogo solo si el registro base sigue siendo utilizable;
   - el atributo o relación conflictiva queda documentado en `reference_data_issues.csv`.

3. **Aceptado**
   - aparece en `outputs/curated/`;
   - no presenta violaciones estructurales para el modelo gobernado.

---

## 6. Artefactos de control asociados
- `scripts/build_reference_loads.py`
- `outputs/curated/reference_hospital.csv`
- `outputs/curated/reference_department.csv`
- `outputs/curated/reference_relationship_hospital_department.csv`
- `outputs/curated/reference_payer_group.csv`
- `outputs/curated/reference_payer.csv`
- `outputs/curated/reference_payer_plan.csv`
- `outputs/curated/reference_relationship_payer_group_to_payer.csv`
- `outputs/curated/reference_relationship_payer_to_plan.csv`
- `outputs/curated/reference_procedure_group.csv`
- `outputs/curated/reference_procedure_family.csv`
- `outputs/curated/reference_procedure_code.csv`
- `outputs/curated/reference_relationship_procedure_group_to_family.csv`
- `outputs/curated/reference_relationship_procedure_family_to_code.csv`
- `outputs/reports/reference_data_issues.csv`

---

## 7. Recomendación de cierre
Para auditoría o demo final, conviene complementar este documento con uno de evidencia operativa que muestre:
- ejemplos concretos de registros excluidos;
- ejemplos concretos de registros en revisión;
- validaciones de ausencia en los CSV curados;
- evidencia de importación o rechazo en `Reference 360`.
