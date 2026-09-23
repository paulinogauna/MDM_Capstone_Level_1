# Setup del ambiente MDM Healthcare

## Objetivo
Preparar un ambiente base para analizar, validar y consolidar datos maestros de pacientes a partir de múltiples fuentes clínicas y administrativas.

## Principios
- `Data_Source/` es solo lectura.
- Todo resultado derivado debe guardarse en `outputs/`.
- Las reglas deben documentarse en `rules/`.
- Los notebooks son exploratorios; la lógica reusable debe migrarse a `scripts/`.

## Herramientas recomendadas
- VS Code
- Git
- Python 3.12+
- Node.js LTS opcional
- Docker Desktop opcional

## Extensiones recomendadas
- Python
- Pylance
- Jupyter
- Docker
- YAML
- REST Client
- Excel Viewer

## Comandos base en Windows
### Crear entorno Python
```powershell
py -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
```

### Instalar librerías base
```powershell
pip install pandas polars duckdb pyarrow openpyxl jupyter rapidfuzz great-expectations
```

### Iniciar notebooks
```powershell
jupyter lab
```

### Opcional Node.js
```powershell
npm init -y
npm install -D typescript tsx eslint prettier
```

## Primer flujo recomendado
1. Perfilar `1_Sources/`.
2. Validar calidad de pacientes.
3. Detectar huérfanos en tablas transaccionales.
4. Revisar jerarquías rotas en referencias.
5. Preparar reglas de matching y survivorship.
