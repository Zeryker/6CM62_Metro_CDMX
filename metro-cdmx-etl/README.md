# ETL de afluencia del Metro CDMX

Proyecto de **Analítica de Datos** (6CM62, UPIICSA-IPN): *Sistema analítico para la evaluación de la afluencia y movilidad en la red del Metro de la CDMX*.

Pipeline en Python que limpia el histórico de afluencia (Datos Abiertos CDMX), lo transforma a un modelo dimensional (copo de nieve + vista estrella) y lo deja listo para **IBM Cognos Analytics** (vía CSV) y **MySQL**.

```
CSV/XLSX crudo -> extract -> clean -> transform -> [simulate] -> load (CSV + MySQL) + reporte de calidad
```

## Estructura

```
src/        extract.py  clean.py  transform.py  simulate.py  quality.py  load.py  run_etl.py  config.py
sql/        00_create_database.sql  01_create_dw_snowflake.sql  02_data_mart_star.sql
tests/      test_clean.py
data/raw/   (aquí va el CSV descargado; no se versiona)
data/clean/ (salida del ETL; no se versiona)
docs/       confluence/ (páginas listas para pegar en Confluence), CONTRIBUTING.md
```

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecución

Columnas esperadas en la entrada: `fecha, anio, mes, linea, estacion, afluencia` (solo `fecha, linea, estacion, afluencia` son obligatorias).

```bash
# Solo datos reales (a CSV)
python -m src.run_etl --input data/raw/afluencia.csv

# Con datos operativos SIMULADOS (clima, incidencias, retraso, hora pico)
python -m src.run_etl --input data/raw/afluencia.csv --simulate

# Además cargar a MySQL (crear antes la BD con sql/00_create_database.sql)
python -m src.run_etl --input data/raw/afluencia.csv --simulate \
  --mysql-url "mysql+pymysql://usuario:clave@localhost:3306/metro_cdmx_dw"
```

Salida en `data/clean/`: una tabla por archivo (`FACT_OPERACION.csv`, `DIM_*.csv`, `CAT_MODELO_TREN.csv`), `RECHAZADOS.csv` (filas descartadas con su motivo) y `REPORTE_CALIDAD.md`.

## Pruebas

```bash
python -m pytest -q
```

## Qué hace la limpieza

| Regla | Descripción |
|---|---|
| R01 | Repara acentos corruptos (doble codificación: `CatÃƒÂ³lica` → `Católica`) |
| R02 | Quita espacios extra y normaliza Unicode |
| R03 | Fechas a tipo fecha (ISO o día/mes/año); `id_fecha` en formato `YYYYMMDD` |
| R04 | `Linea 1`, `Línea A`, `12` → código de línea estándar |
| R05 | Afluencia numérica (quita comas); nula/no numérica → rechazada |
| R06 | Afluencia negativa → rechazada |
| R07 | `anio` y `mes` se validan contra `fecha` (manda la fecha) |
| R08 | Una estación = (nombre normalizado, línea); se unifican variantes de escritura |
| R09 | Duplicados exactos eliminados |
| R10 | Misma fecha+estación+línea con valores distintos: se conserva el primero y se reporta |

## Datos simulados

Clima, incidencias, retraso e hora pico **no existen como datos públicos**. Con `--simulate` se generan con semilla fija y quedan marcados con `es_dato_simulado = 1`. Sin `--simulate`, esas columnas quedan vacías y las llaves apuntan al miembro `0` ("Sin dato"). Detalle en `docs/confluence/07_Supuestos_y_Limitaciones.md`.

## Equipo

Pérez de León Hagopian Juan Carlos · Lozada Celis Ernesto · Gómez Vega Diego · Bustillos Segindo Jazmin
