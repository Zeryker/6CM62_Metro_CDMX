"""Reporte de calidad del ETL (Markdown)."""
from datetime import datetime

from . import config


def generar_reporte(stats: dict, tablas: dict, rechazados) -> str:
    fact, dim_fecha, dim_est, dim_lin = (tablas[k] for k in ("FACT_OPERACION", "DIM_FECHA", "DIM_ESTACION", "DIM_LINEA"))
    codigo = {r.id_linea: r.nombre_linea.replace("Linea ", "") for r in dim_lin.itertuples()}
    por_linea = dim_est.groupby("id_linea").size()
    dias_con_datos = fact["id_fecha"].nunique()

    L = [f"# Reporte de calidad del ETL", f"_Generado: {datetime.now():%Y-%m-%d %H:%M}_", "",
         "## Flujo de registros", "",
         "| Etapa | Registros |", "|---|---:|",
         f"| Entrada (crudo) | {stats['filas_entrada']:,} |",
         f"| Rechazados (validaciones) | {stats['filas_rechazadas']:,} |",
         f"| Duplicados exactos eliminados | {stats['duplicados_exactos_eliminados']:,} |",
         f"| Conflictos de llave descartados | {stats['conflictos_de_llave_descartados']:,} |",
         f"| **Salida (FACT_OPERACION)** | **{stats['filas_salida']:,}** |", ""]
    if stats["rechazos_por_motivo"]:
        L += ["### Rechazos por motivo", ""] + [f"- `{m}`: {n:,}" for m, n in stats["rechazos_por_motivo"].items()] + [""]
    L += ["## Correcciones", "",
          f"- Nombres de estación con codificación reparada: {stats['estaciones_con_codificacion_reparada']:,}",
          f"- Filas con anio/mes inconsistente respecto a `fecha`: {stats['inconsistencias_anio_mes']:,}", "",
          "## Cobertura", "",
          f"- Rango de fechas: {dim_fecha['fecha'].min()} a {dim_fecha['fecha'].max()}",
          f"- Días calendario: {len(dim_fecha):,} | días con datos: {dias_con_datos:,}",
          f"- Registros con afluencia = 0: {int((fact['afluencia_pasajeros'] == 0).sum()):,}",
          f"- Estaciones (estación-línea) en DIM_ESTACION: {len(dim_est):,}", "",
          "## Estaciones por línea vs. referencia", "",
          "| Línea | En datos | Referencia (aprox.) |", "|---|---:|---:|"]
    for id_l, n in por_linea.items():
        c = codigo[id_l]
        L.append(f"| {c} | {n} | {config.ESTACIONES_ESPERADAS.get(c, '-')} |")
    L += ["", "> Una muestra parcial tendrá menos estaciones que la referencia; con el histórico completo deberían coincidir.",
          "", f"## Datos simulados", "",
          f"- Filas con columnas operativas simuladas: {int(fact['es_dato_simulado'].sum()):,}"]
    return "\n".join(L) + "\n"
