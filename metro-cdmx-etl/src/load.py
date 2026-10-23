"""Carga: escribe CSV (para Cognos/Power BI) y, opcionalmente, MySQL."""
import re
from pathlib import Path

from . import config


def escribir_csv(tablas: dict, rechazados, carpeta: Path) -> None:
    carpeta = Path(carpeta)
    carpeta.mkdir(parents=True, exist_ok=True)
    for nombre, df in tablas.items():
        df.to_csv(carpeta / f"{nombre}.csv", index=False, encoding="utf-8-sig")
    rechazados.to_csv(carpeta / "RECHAZADOS.csv", index=False, encoding="utf-8-sig")


def _sentencias(ruta: Path):
    texto = re.sub(r"--[^\n]*", "", ruta.read_text(encoding="utf-8"))
    return [s.strip() for s in texto.split(";") if s.strip()]


def cargar_mysql(tablas: dict, url: str) -> None:
    """url ejemplo: mysql+pymysql://usuario:clave@localhost:3306/metro_cdmx_dw"""
    from sqlalchemy import create_engine, text
    engine = create_engine(url)
    with engine.begin() as conn:
        for archivo in ("01_create_dw_snowflake.sql", "02_data_mart_star.sql"):
            for sent in _sentencias(config.DDL_DIR / archivo):
                conn.execute(text(sent))
    for nombre, df in tablas.items():          # orden de carga = orden de dependencias
        df.to_sql(nombre, engine, if_exists="append", index=False, chunksize=5000)
