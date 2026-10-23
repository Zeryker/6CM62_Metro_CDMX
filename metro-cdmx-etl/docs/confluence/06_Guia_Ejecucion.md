# 6. Guía de ejecución

## Requisitos
Python 3.10+, MySQL 8 (opcional) y acceso a IBM Cognos Analytics.

## Pasos
1. Clonar el repositorio y crear el entorno: `python -m venv .venv`, activarlo e instalar con `pip install -r requirements.txt`.
2. Descargar el CSV de afluencia diaria de Datos Abiertos CDMX y guardarlo en `data/raw/`.
3. Ejecutar `python -m src.run_etl --input data/raw/<archivo>.csv --simulate`.
4. Revisar `data/clean/REPORTE_CALIDAD.md` y `data/clean/RECHAZADOS.csv`.
5. (Opcional) Crear la BD con `sql/00_create_database.sql` y repetir el paso 3 agregando `--mysql-url mysql+pymysql://usuario:clave@localhost:3306/metro_cdmx_dw`.
6. En Cognos: **Cargar datos** con los CSV de `data/clean/`, crear el módulo de datos `DM_METRO_CDMX` y definir las relaciones del esquema.
7. Construir `DASHBOARD_METRO_CDMX` sobre ese módulo.

## Pruebas
`python -m pytest -q`
