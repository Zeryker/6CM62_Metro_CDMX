"""Limpieza y estandarización de la afluencia diaria del Metro CDMX."""
import re
import unicodedata

import pandas as pd

from . import config

_MOJIBAKE = re.compile("[ÃÂ]")


def fix_mojibake(text):
    """Repara texto UTF-8 mal decodificado (hasta 3 niveles): 'CatÃƒÂ³lica' -> 'Católica'."""
    if not isinstance(text, str):
        return text
    for _ in range(3):
        if not _MOJIBAKE.search(text):
            break
        for enc in ("cp1252", "latin-1"):
            try:
                text = text.encode(enc).decode("utf-8")
                break
            except (UnicodeEncodeError, UnicodeDecodeError):
                continue
        else:
            break
    return text


def clean_text(value):
    """Repara codificación, normaliza Unicode y colapsa espacios."""
    if not isinstance(value, str):
        return value
    text = unicodedata.normalize("NFC", fix_mojibake(value))
    text = text.replace("\u00a0", " ").replace("\u00ad", "")
    return re.sub(r"\s+", " ", text).strip()


def make_key(text: str) -> str:
    """Llave de comparación: sin acentos, minúsculas, sin signos ('La Villa/Basílica' -> 'la villa basilica')."""
    t = unicodedata.normalize("NFKD", text)
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", t.lower()).strip()


def extraer_codigo_linea(valor):
    """'Linea 1' / 'Línea A' / '12' -> '1' / 'A' / '12'. None si no es reconocible."""
    if not isinstance(valor, str):
        return None
    s = unicodedata.normalize("NFKD", clean_text(valor)).upper()
    s = "".join(c for c in s if not unicodedata.combining(c))
    m = re.search(r"(?:^|\s)(12|[1-9]|A|B)\s*$", s)
    return m.group(1) if m and m.group(1) in config.LINEAS else None


def parsear_fechas(serie: pd.Series) -> pd.Series:
    s = serie.astype(str).str.strip()
    f = pd.to_datetime(s, format="ISO8601", errors="coerce")
    pendientes = f.isna()
    if pendientes.any():
        f[pendientes] = pd.to_datetime(s[pendientes], dayfirst=True, errors="coerce", format="mixed")
    return f


def parsear_numero(serie: pd.Series) -> pd.Series:
    s = serie.astype(str).str.replace(",", "", regex=False).str.replace(r"\s+", "", regex=True)
    return pd.to_numeric(s, errors="coerce")


def clean(df_raw: pd.DataFrame):
    """Devuelve (datos_limpios, rechazados, estadisticas)."""
    stats = {"filas_entrada": len(df_raw)}
    df = df_raw.copy()
    df.columns = [str(c).strip().lower() for c in df.columns]
    faltantes = [c for c in config.COLUMNAS_REQUERIDAS if c not in df.columns]
    if faltantes:
        raise ValueError(f"Faltan columnas requeridas: {faltantes}. Encontradas: {list(df.columns)}")
    df = df.reset_index(drop=True)
    df["fila_origen"] = df.index + 2          # +2: encabezado y base 1 (como en Excel)
    raw = df[["fila_origen", "fecha", "linea", "estacion", "afluencia"]].copy()

    # R01-R02: codificación y espacios
    est_raw = df["estacion"]
    stats["estaciones_con_codificacion_reparada"] = int(
        sum(isinstance(a, str) and a != fix_mojibake(a) for a in est_raw))
    df["estacion"] = est_raw.map(clean_text)
    df["linea_codigo"] = df["linea"].map(extraer_codigo_linea)
    df["fecha"] = parsear_fechas(df["fecha"])
    df["afluencia"] = parsear_numero(df["afluencia"])

    # R03-R06: validaciones -> rechazados con motivo
    motivo = pd.Series("", index=df.index)

    def marcar(mask, texto):
        motivo.loc[mask & (motivo == "")] = texto

    marcar(df["fecha"].isna(), "fecha_invalida")
    marcar(df["linea_codigo"].isna(), "linea_no_reconocida")
    marcar(df["estacion"].isna() | (df["estacion"] == ""), "estacion_vacia")
    marcar(df["afluencia"].isna(), "afluencia_nula_o_no_numerica")
    marcar(df["afluencia"] < 0, "afluencia_negativa")
    mask_rech = motivo != ""
    rechazados = raw[mask_rech].assign(motivo_rechazo=motivo[mask_rech])
    valid = df[~mask_rech].copy()
    valid["afluencia"] = valid["afluencia"].astype("int64")
    stats["filas_rechazadas"] = int(mask_rech.sum())
    stats["rechazos_por_motivo"] = rechazados["motivo_rechazo"].value_counts().to_dict()

    # R07: consistencia de anio/mes contra fecha (la fecha manda)
    inc = 0
    if "mes" in valid:
        mes_num = valid["mes"].map(clean_text).map(
            lambda x: config.MESES_INV.get(make_key(x)) if isinstance(x, str) else None)
        inc += int(((mes_num != valid["fecha"].dt.month) & mes_num.notna()).sum())
    if "anio" in valid:
        anio = pd.to_numeric(valid["anio"], errors="coerce")
        inc += int(((anio != valid["fecha"].dt.year) & anio.notna()).sum())
    stats["inconsistencias_anio_mes"] = inc

    # R08: estaciones -> llave normalizada + alias + nombre canónico (el más frecuente)
    valid["estacion_key"] = valid["estacion"].map(make_key).replace(config.ALIAS_ESTACIONES)
    grupo = ["linea_codigo", "estacion_key"]
    canon = (valid.groupby(grupo)["estacion"].agg(lambda s: s.value_counts().idxmax())
             .rename("estacion_canonica").reset_index())
    valid = valid.merge(canon, on=grupo, how="left")
    valid["estacion"] = valid["estacion_canonica"]

    # R09-R10: duplicados
    antes = len(valid)
    valid = valid.drop_duplicates(subset=["fecha", "linea_codigo", "estacion_key", "afluencia"])
    stats["duplicados_exactos_eliminados"] = antes - len(valid)
    conflicto = valid.duplicated(subset=["fecha", "linea_codigo", "estacion_key"], keep="first")
    stats["conflictos_de_llave_descartados"] = int(conflicto.sum())
    valid = valid[~conflicto]

    valid["_orden"] = valid["linea_codigo"].map(lambda c: config.LINEAS[c][0])
    valid = valid.sort_values(["fecha", "_orden", "estacion"]).reset_index(drop=True)
    out = valid[["fecha", "linea_codigo", "estacion", "estacion_key", "afluencia"]]
    stats["filas_salida"] = len(out)
    return out, rechazados, stats
