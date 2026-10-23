# Reporte de calidad del ETL
_Generado: 2026-10-23 02:11_

## Flujo de registros

| Etapa | Registros |
|---|---:|
| Entrada (crudo) | 19 |
| Rechazados (validaciones) | 0 |
| Duplicados exactos eliminados | 0 |
| Conflictos de llave descartados | 0 |
| **Salida (FACT_OPERACION)** | **19** |

## Correcciones

- Nombres de estación con codificación reparada: 8
- Filas con anio/mes inconsistente respecto a `fecha`: 0

## Cobertura

- Rango de fechas: 2010-01-01 a 2010-01-01
- Días calendario: 1 | días con datos: 1
- Registros con afluencia = 0: 0
- Estaciones (estación-línea) en DIM_ESTACION: 19

## Estaciones por línea vs. referencia

| Línea | En datos | Referencia (aprox.) |
|---|---:|---:|
| 1 | 5 | 20 |
| 3 | 1 | 21 |
| 4 | 3 | 10 |
| 5 | 2 | 13 |
| 6 | 2 | 11 |
| 7 | 3 | 14 |
| 8 | 1 | 19 |
| 9 | 2 | 12 |

> Una muestra parcial tendrá menos estaciones que la referencia; con el histórico completo deberían coincidir.

## Datos simulados

- Filas con columnas operativas simuladas: 19
