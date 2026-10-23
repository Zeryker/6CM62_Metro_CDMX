"""Punto de entrada: python -m src.run_etl --input data/raw/afluencia.csv [--simulate] [--mysql-url ...]"""
import argparse
import logging
from pathlib import Path

from . import config
from .clean import clean
from .extract import read_source
from .load import cargar_mysql, escribir_csv
from .quality import generar_reporte
from .simulate import simular_operacion
from .transform import construir_tablas

log = logging.getLogger("etl")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="ETL de afluencia del Metro CDMX")
    ap.add_argument("--input", required=True, help="CSV o XLSX crudo (fecha, anio, mes, linea, estacion, afluencia)")
    ap.add_argument("--output", default=str(config.CLEAN_DIR), help="Carpeta de salida")
    ap.add_argument("--simulate", action="store_true", help="Agregar datos operativos SIMULADOS")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--mysql-url", default=None, help="Si se indica, carga también a MySQL")
    args = ap.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    log.info("1/5 Extrayendo %s", args.input)
    crudo = read_source(args.input)
    log.info("2/5 Limpiando %s filas", f"{len(crudo):,}")
    datos, rechazados, stats = clean(crudo)
    log.info("3/5 Transformando a modelo dimensional")
    tablas = construir_tablas(datos)
    if args.simulate:
        log.warning("Se agregan datos operativos SIMULADOS (semilla=%s)", args.seed)
        tablas["FACT_OPERACION"] = simular_operacion(tablas["FACT_OPERACION"], args.seed)
    log.info("4/5 Escribiendo CSV en %s", args.output)
    escribir_csv(tablas, rechazados, Path(args.output))
    (Path(args.output) / "REPORTE_CALIDAD.md").write_text(generar_reporte(stats, tablas, rechazados), encoding="utf-8")
    if args.mysql_url:
        log.info("5/5 Cargando a MySQL")
        cargar_mysql(tablas, args.mysql_url)
    else:
        log.info("5/5 Carga a MySQL omitida (sin --mysql-url)")
    log.info("Listo: %s filas en FACT_OPERACION, %s rechazadas", f"{stats['filas_salida']:,}", stats["filas_rechazadas"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
