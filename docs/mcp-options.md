# MCP reutilizables para este proyecto

## Recomendados
### 1. Filesystem MCP
Uso:
- explorar carpetas
- leer CSV, JSON, YAML y documentación
- generar artefactos derivados

### 2. Git MCP
Uso:
- revisar cambios
- gestionar ramas
- preparar commits limpios

### 3. GitHub MCP
Uso:
- issues
- PRs
- documentación técnica compartida

### 4. DuckDB o SQLite MCP
Uso:
- consultar datasets cargados
- validar integridad referencial
- comparar fuentes
- generar perfiles rápidos

### 5. HTTP/OpenAPI MCP
Uso:
- probar APIs futuras
- integrar servicios de validación o matching

## Cuándo crear un MCP propio
Solo cuando ya existan reglas estables de:
- profiling
- data quality
- matching
- survivorship
- golden record

## Recomendación
Primero reutilizar MCP genéricos. Después evaluar un MCP propio llamado, por ejemplo, `mdm-healthcare-tools` para exponer herramientas como:
- `profile_source`
- `validate_patient_quality`
- `find_orphans`
- `match_patients`
- `build_golden_record`
