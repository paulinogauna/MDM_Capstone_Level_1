# Alcance MDM del proyecto

## Dominio
Healthcare / Patient Master Data Management

## Entidades principales
- Pacientes
- Hospitales
- Departamentos
- Doctores
- Enfermeros
- Procedimientos
- Proveedores de seguro

## Objetivos funcionales
- Consolidar pacientes desde múltiples fuentes
- Detectar duplicados y conflictos de identidad
- Construir un golden record
- Validar integridad referencial con datos transaccionales
- Detectar problemas de calidad y jerarquía

## Restricciones
- No modificar archivos originales en `Data_Source/`
- Mantener trazabilidad entre fuente y golden record
- Separar reglas de calidad, matching y survivorship
