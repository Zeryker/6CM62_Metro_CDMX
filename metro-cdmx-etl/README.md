# Equipo

Pérez de León Hagopian Juan Carlos

Lozada Celis Ernesto

Gómez Vega Diego

Bustillos Segindo Jazmin

## ETL de afluencia del Metro CDMX

Proyecto de **Analítica de Datos** (6CM62): *Sistema analítico para la evaluación de la afluencia y movilidad en la red del Metro de la CDMX*.

Pipeline en Python que limpia el histórico de afluencia (Datos Abiertos CDMX), lo transforma a un modelo dimensional (copo de nieve + vista estrella) y lo deja listo para **IBM Cognos Analytics** (vía CSV) y **MySQL**.

## Estructura

```
src/        extract.py  clean.py  transform.py  simulate.py  quality.py  load.py  run_etl.py  config.py
sql/        00_create_database.sql  01_create_dw_snowflake.sql  02_data_mart_star.sql
tests/      test_clean.py
data/raw/   csv metro
data/clean/ csv clean
docs/       archivos de confluence
```

## Pruebas

```bash
python -m pytest -q
```

## Qué hace la limpieza

| Regla | Descripción |
|---|---|
| R01 | Repara acentos corruptos (doble codificación: `CatÃƒÂ³lica` → `Católica`) |
| R02 | Quita espacios extra y normaliza Unicode |
| R03 | Fechas corregidas (ISO o día/mes/año); `id_fecha` en formato `YYYYMMDD` |
| R04 | `Linea 1`, `Línea A`, `12` → código de línea estándar |
| R05 | Duplicados exactos eliminados |
| R06 | Misma fecha+estación+línea con valores distintos: se conserva el primero y se reporta |

## Datos simulados

Clima, incidencias, retraso e hora pico **no existen como datos públicos**. Con `--simulate` se generan con semilla fija y quedan marcados con `es_dato_simulado = 1`. Sin `--simulate`, esas columnas quedan vacías y las llaves apuntan al miembro `0` ("Sin dato").


