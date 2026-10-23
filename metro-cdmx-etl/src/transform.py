"""Transformación: construye dimensiones (copo de nieve) y la tabla de hechos."""
import pandas as pd

from . import config

SIN_DATO = 0   # miembro "Sin dato" de cada dimensión (práctica Kimball)


def _periodo(anio: int) -> str:
    # Convención del proyecto (ajustable): ver docs/confluence/07
    if anio <= 2019:
        return "Pre-pandemia"
    return "Pandemia" if anio <= 2021 else "Post-pandemia"


def es_festivo(ts: pd.Timestamp) -> int:
    """Festivos oficiales fijos y de lunes. Aproximado: no incluye Semana Santa ni 1-oct sexenal."""
    if (ts.month, ts.day) in {(1, 1), (5, 1), (9, 16), (12, 25)}:
        return 1
    if ts.weekday() == 0:
        n = (ts.day - 1) // 7 + 1
        return int((ts.month == 2 and n == 1) or (ts.month == 3 and n == 3) or (ts.month == 11 and n == 3))
    return 0


def build_dim_fecha(fmin, fmax):
    dias = pd.date_range(fmin, fmax, freq="D")
    dim = pd.DataFrame({"fecha": dias})
    dim.insert(0, "id_fecha", dim["fecha"].dt.strftime("%Y%m%d").astype(int))   # clave Kimball
    dim["dia_semana"] = dim["fecha"].dt.weekday.map(lambda i: config.DIAS_SEMANA[i])
    dim["es_fin_de_semana"] = (dim["fecha"].dt.weekday >= 5).astype(int)
    dim["es_festivo"] = dim["fecha"].map(es_festivo)
    dim["id_mes"] = dim["fecha"].dt.year * 100 + dim["fecha"].dt.month
    dim["fecha"] = dim["fecha"].dt.date
    return dim


def build_dim_mes(fmin, fmax):
    meses = pd.period_range(fmin, fmax, freq="M")
    return pd.DataFrame({
        "id_mes": [p.year * 100 + p.month for p in meses],
        "nombre_mes": [config.MESES[p.month] for p in meses],
        "trimestre": [(p.month - 1) // 3 + 1 for p in meses],
        "anio": [p.year for p in meses],
    })


def build_dim_anio(fmin, fmax):
    anios = range(fmin.year, fmax.year + 1)
    return pd.DataFrame({"anio": list(anios), "tipo_periodo": [_periodo(a) for a in anios]})


def build_dim_linea(codigos):
    filas = sorted((config.LINEAS[c][0], f"Linea {c}", config.LINEAS[c][1]) for c in set(codigos))
    return pd.DataFrame(filas, columns=["id_linea", "nombre_linea", "color"])


def build_dim_estacion(df):
    est = df[["linea_codigo", "estacion"]].drop_duplicates().copy()
    est["id_linea"] = est["linea_codigo"].map(lambda c: config.LINEAS[c][0])
    est = est.sort_values(["id_linea", "estacion"]).reset_index(drop=True)
    est.insert(0, "id_estacion", est.index + 1)
    return est.rename(columns={"estacion": "nombre_estacion"})[["id_estacion", "nombre_estacion", "id_linea"]]


def build_catalogos():
    """Catálogos de dimensiones operativas. Definiciones ilustrativas, no datos oficiales."""
    clima = pd.DataFrame({
        "id_clima": [0, 1, 2, 3],
        "clima_estado": ["Sin dato", "Despejado", "Nublado", "Lluvia"],
        "aplica_marcha_seguridad": [0, 0, 0, 1]})
    incidencia = pd.DataFrame({
        "id_incidencia": [0, 1, 2, 3, 4],
        "tipo_incidencia": ["Sin incidencia registrada", "Falla de tren", "Falla de energia",
                            "Persona en vias", "Falla de senalizacion"],
        "descripcion": ["No se registró incidencia", "Avería de material rodante",
                        "Interrupción de suministro eléctrico", "Retiro de persona de la vía",
                        "Falla en sistema de señalización"],
        "gravedad": ["Ninguna", "Media", "Alta", "Alta", "Media"]})
    modelo = pd.DataFrame({"id_modelo": [0], "modelo_tren": ["Sin dato"], "capacidad_pasajeros": [pd.NA],
                           "num_wagones": [pd.NA], "velocidad_diseno_kmh": [pd.NA]}).astype(
        {"capacidad_pasajeros": "Int64", "num_wagones": "Int64", "velocidad_diseno_kmh": "Int64"})
    tren = pd.DataFrame({"id_tren": [0], "id_modelo": [0]})
    return clima, incidencia, modelo, tren


def build_fact(df, dim_estacion):
    f = df.copy()
    f["id_fecha"] = f["fecha"].dt.strftime("%Y%m%d").astype(int)
    f["id_linea"] = f["linea_codigo"].map(lambda c: config.LINEAS[c][0])
    est = dim_estacion.rename(columns={"nombre_estacion": "estacion"})
    f = f.merge(est, on=["estacion", "id_linea"], how="left")
    f = f.sort_values(["id_fecha", "id_estacion"]).reset_index(drop=True)
    f.insert(0, "id_afluencia", f.index + 1)
    f = f.rename(columns={"afluencia": "afluencia_pasajeros"})
    # Métrica derivada (proxy): % respecto al máximo histórico de la estación
    maximo = f.groupby("id_estacion")["afluencia_pasajeros"].transform("max")
    f["porcentaje_ocupacion"] = (f["afluencia_pasajeros"] / maximo.where(maximo > 0) * 100).fillna(0).round(2)
    f["alerta_dosificacion"] = (f["porcentaje_ocupacion"] >= config.UMBRAL_DOSIFICACION).astype(int)
    for col in ("id_clima", "id_incidencia", "id_tren"):
        f[col] = SIN_DATO
    for col in ("afluencia_hora_pico", "intervalo_headway_seg", "distancia_intertren_m", "tiempo_retraso_min"):
        f[col] = pd.array([pd.NA] * len(f), dtype="Int64")
    f["velocidad_operativa_real_kmh"] = pd.Series([pd.NA] * len(f), dtype="Float64")
    f["es_dato_simulado"] = 0
    cols = ["id_afluencia", "id_fecha", "id_estacion", "id_clima", "id_incidencia", "id_tren",
            "afluencia_pasajeros", "afluencia_hora_pico", "porcentaje_ocupacion",
            "velocidad_operativa_real_kmh", "intervalo_headway_seg", "distancia_intertren_m",
            "tiempo_retraso_min", "alerta_dosificacion", "es_dato_simulado"]
    return f[cols]


def construir_tablas(df: pd.DataFrame) -> dict:
    """Devuelve las tablas en orden de carga (respeta llaves foráneas)."""
    fmin, fmax = df["fecha"].min(), df["fecha"].max()
    dim_estacion = build_dim_estacion(df)
    clima, incidencia, modelo, tren = build_catalogos()
    return {
        "DIM_ANIO": build_dim_anio(fmin, fmax),
        "DIM_MES": build_dim_mes(fmin, fmax),
        "DIM_FECHA": build_dim_fecha(fmin, fmax),
        "DIM_LINEA": build_dim_linea(df["linea_codigo"]),
        "DIM_ESTACION": dim_estacion,
        "DIM_CLIMA": clima,
        "DIM_INCIDENCIA": incidencia,
        "CAT_MODELO_TREN": modelo,
        "DIM_TREN": tren,
        "FACT_OPERACION": build_fact(df, dim_estacion),
    }
