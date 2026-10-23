"""Configuración central del ETL del Metro CDMX."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
CLEAN_DIR = ROOT / "data" / "clean"
DDL_DIR = ROOT / "sql"

COLUMNAS_REQUERIDAS = ["fecha", "linea", "estacion", "afluencia"]

MESES = {1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
         7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre",
         12: "Diciembre"}
MESES_INV = {v.lower(): k for k, v in MESES.items()}
DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

# código de línea -> (id_linea, color hex referencial)
LINEAS = {
    "1": (1, "#F04E98"), "2": (2, "#005EB8"), "3": (3, "#AF9800"),
    "4": (4, "#6BBBAE"), "5": (5, "#FFD100"), "6": (6, "#DA291C"),
    "7": (7, "#E87722"), "8": (8, "#009A44"), "9": (9, "#5C462B"),
    "A": (10, "#9F2F67"), "B": (11, "#B0B3B2"), "12": (12, "#C99700"),
}

# Referencia aproximada (estaciones por línea) SOLO para el reporte de calidad.
# Verificar contra la fuente oficial antes de citarla como cifra definitiva.
ESTACIONES_ESPERADAS = {"1": 20, "2": 24, "3": 21, "4": 10, "5": 13, "6": 11,
                        "7": 14, "8": 19, "9": 12, "A": 10, "B": 21, "12": 20}

# Variantes de nombre -> nombre canónico (ambos como "estacion_key", sin acentos,
# minúsculas). Se amplía a mano al revisar el reporte de calidad.
ALIAS_ESTACIONES: dict[str, str] = {}

UMBRAL_DOSIFICACION = 90.0   # % del máximo histórico de la estación
