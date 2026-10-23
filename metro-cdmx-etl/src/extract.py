"""Extracción: lee el archivo crudo (CSV o Excel) como texto, sin interpretar tipos."""
from pathlib import Path

import pandas as pd


def read_source(path: str | Path) -> pd.DataFrame:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"No existe el archivo de entrada: {p}")
    suf = p.suffix.lower()
    if suf in (".xlsx", ".xlsm", ".xls"):
        return pd.read_excel(p, dtype=str)
    if suf in (".csv", ".txt"):
        for enc in ("utf-8-sig", "latin-1"):
            try:
                return pd.read_csv(p, dtype=str, encoding=enc)
            except UnicodeDecodeError:
                continue
    raise ValueError(f"Formato no soportado: {suf}")
