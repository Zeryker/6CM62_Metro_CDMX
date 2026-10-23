import pandas as pd
import pytest

from src.clean import clean, extraer_codigo_linea, fix_mojibake, make_key, parsear_fechas
from src.transform import construir_tablas, es_festivo


def test_fix_mojibake_doble_codificacion():
    assert fix_mojibake("Isabel la CatÃƒÂ³lica") == "Isabel la Católica"
    assert fix_mojibake("GÃƒÂ³mez FarÃƒÂ\xadas") == "Gómez Farías"


def test_fix_mojibake_no_toca_texto_correcto():
    assert fix_mojibake("Pino Suárez") == "Pino Suárez"
    assert fix_mojibake("Zaragoza") == "Zaragoza"


@pytest.mark.parametrize("valor,esperado", [
    ("Linea 1", "1"), ("Línea 12", "12"), ("LINEA A", "A"), ("linea b", "B"),
    ("9", "9"), ("Linea 10", None), ("Linea X", None), (None, None)])
def test_codigo_linea(valor, esperado):
    assert extraer_codigo_linea(valor) == esperado


def test_make_key_unifica_variantes():
    assert make_key("La Villa/Basílica") == make_key("La Villa-Basilica")


def test_fechas_iso_y_dmy():
    f = parsear_fechas(pd.Series(["2010-01-01", "01/02/2010", "basura"]))
    assert f.iloc[0] == pd.Timestamp("2010-01-01")
    assert f.iloc[1] == pd.Timestamp("2010-02-01")
    assert pd.isna(f.iloc[2])


def _crudo():
    return pd.DataFrame({
        "fecha": ["2010-01-01"] * 4 + ["2010-01-02", "no-fecha", "2010-01-02", "2010-01-02"],
        "anio": ["2010"] * 8, "mes": ["Enero"] * 8,
        "linea": ["Linea 1", "Linea 1", "Linea 9", "Linea 9", "Linea 1", "Linea 1", "Linea 77", "Linea 1"],
        "estacion": ["Pino SuÃƒÂ¡rez", "  Pino   Suárez ", "PantitlÃƒÂ¡n", "Pantitlán",
                     "Pino Suárez", "Pino Suárez", "Pino Suárez", "Moctezuma"],
        "afluencia": ["100", "100", "5,000", "5000", "-3", "10", "10", "abc"]})


def test_pipeline_completo():
    out, rech, st = clean(_crudo())
    # Pino Suárez L1 (2 filas iguales -> 1), Pantitlán L9 (2 iguales -> 1)
    assert len(out) == 2
    assert st["duplicados_exactos_eliminados"] == 2
    assert set(out["estacion"]) == {"Pino Suárez", "Pantitlán"}
    assert set(rech["motivo_rechazo"]) == {
        "afluencia_negativa", "fecha_invalida", "linea_no_reconocida", "afluencia_nula_o_no_numerica"}
    assert st["filas_entrada"] == st["filas_salida"] + st["filas_rechazadas"] + 2


def test_faltan_columnas():
    with pytest.raises(ValueError):
        clean(pd.DataFrame({"fecha": ["2010-01-01"]}))


def test_modelo_dimensional_integridad():
    out, _, _ = clean(_crudo())
    t = construir_tablas(out)
    fact = t["FACT_OPERACION"]
    assert fact["id_fecha"].isin(t["DIM_FECHA"]["id_fecha"]).all()
    assert fact["id_estacion"].isin(t["DIM_ESTACION"]["id_estacion"]).all()
    assert fact["id_clima"].isin(t["DIM_CLIMA"]["id_clima"]).all()
    assert t["DIM_ESTACION"]["id_linea"].isin(t["DIM_LINEA"]["id_linea"]).all()
    assert t["DIM_FECHA"]["id_mes"].isin(t["DIM_MES"]["id_mes"]).all()
    assert t["DIM_MES"]["anio"].isin(t["DIM_ANIO"]["anio"]).all()
    assert fact["id_afluencia"].is_unique


def test_festivos():
    assert es_festivo(pd.Timestamp("2010-01-01")) == 1
    assert es_festivo(pd.Timestamp("2021-03-15")) == 1     # 3er lunes de marzo
    assert es_festivo(pd.Timestamp("2021-03-16")) == 0
