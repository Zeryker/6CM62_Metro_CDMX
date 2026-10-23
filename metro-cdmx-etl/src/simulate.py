"""Datos operativos SIMULADOS (clima, incidencias, retraso, hora pico).

No existen como datos públicos. Se generan con semilla fija solo para poblar el modelo
y el dashboard de la entrega. Las filas quedan marcadas con es_dato_simulado = 1.
"""
import numpy as np
import pandas as pd


def simular_operacion(fact: pd.DataFrame, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    f = fact.copy()
    dias = f["id_fecha"].unique()
    clima_por_dia = pd.Series(rng.choice([1, 2, 3], size=len(dias), p=[0.60, 0.25, 0.15]), index=dias)
    f["id_clima"] = f["id_fecha"].map(clima_por_dia).astype(int)

    hay = rng.random(len(f)) < 0.03
    f["id_incidencia"] = 0
    f.loc[hay, "id_incidencia"] = rng.integers(1, 5, size=int(hay.sum()))
    retraso = np.zeros(len(f), dtype=int)
    retraso[hay] = rng.integers(3, 26, size=int(hay.sum()))
    f["tiempo_retraso_min"] = pd.array(retraso, dtype="Int64")

    factor = rng.uniform(0.10, 0.16, size=len(f))
    f["afluencia_hora_pico"] = pd.array(np.round(f["afluencia_pasajeros"].to_numpy() * factor).astype(int), dtype="Int64")
    f["es_dato_simulado"] = 1
    return f
