# Patient Quality Rules

## Objetivo
Definir las reglas iniciales de calidad para el primer paso offline del capstone: profiling y validación básica de las fuentes de pacientes en `Data_Source/1_Sources/`.

## Alcance
Aplica a:
- `Patients_EMR_Cerner.csv`
- `Patients_EMR_Epic.csv`
- `Patients_ManualEntry.csv`
- `Patients_MultiDomain_Conflicts.csv`
- `Patients_RegistrationDB.csv`

## Reglas iniciales

### 1. Identificador de paciente
- `patient_id` es obligatorio.
- `patient_id` debe ser numérico.
- `patient_id` debe ser mayor que 0.
- `patient_id` no debería duplicarse dentro de la misma fuente.

### 2. Nombre y apellido
- `first_name` es obligatorio.
- `last_name` es obligatorio.
- No deben contener placeholders como `###`, `N/A`, `UNKNOWN`.
- No deben contener caracteres no alfabéticos salvo espacios, apóstrofes o guiones.

### 3. Email
- `email` debe existir para los registros donde se espera contacto digital.
- `email` debe cumplir un patrón estándar de correo.
- Ejemplos inválidos: `user@.com`, `not-an-email`.

### 4. Teléfonos
- `phone_number` no debe usar placeholders como `000-000-0000`.
- `emergency_contact_phone` no debe usar placeholders.
- Los teléfonos vacíos deben quedar marcados para revisión.

### 5. Fechas
- `date_of_birth` debe ser parseable.
- `date_of_birth` no puede estar en el futuro.
- `date_of_birth` no debería ser anterior a `1900-01-01`.
- `registration_date` y `last_visit_date` deben ser parseables cuando existan.
- `last_visit_date` no debería ser anterior a `registration_date`.

### 6. Medidas clínicas
- `height_cm` debe estar entre 45 y 250.
- `weight_kg` debe estar entre 2 y 400.
- `bmi` debe ser numérico cuando exista.
- `bmi` debe estar entre 0 y 100.

### 7. Dominios controlados
- `blood_type` debe pertenecer a: `A+`, `A-`, `B+`, `B-`, `AB+`, `AB-`, `O+`, `O-`.
- `patient_status` debería normalizarse a un casing estándar, por ejemplo `Active`, `Inactive`, `Deceased`.

### 8. Dirección
- `address` debería ser JSON válido.
- Si el JSON está roto o mal escapado, debe marcarse como issue estructural.

## Tipos de issue esperados
- `missing_identifier`
- `invalid_identifier`
- `duplicate_identifier`
- `invalid_name`
- `invalid_email`
- `placeholder_phone`
- `invalid_date`
- `future_date`
- `suspicious_date`
- `date_sequence_issue`
- `invalid_numeric`
- `out_of_range_measure`
- `invalid_domain_value`
- `standardization_needed`
- `invalid_json`

## Entregables asociados
- `outputs/reports/source_profile_summary.csv`
- `outputs/reports/source_profile_details.csv`
- `outputs/reports/patient_quality_issues.csv`
- `scripts/profile_sources.py`
- `notebooks/01_source_profiling.ipynb`

## Próximo paso
Con estos resultados, el siguiente entregable será priorizar issues por severidad y preparar validaciones de integridad referencial con tablas transaccionales y de referencia.
