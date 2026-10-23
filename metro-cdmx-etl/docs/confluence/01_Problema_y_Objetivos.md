# 1. Problema y objetivos

## Problema
El STC Metro transporta a millones de usuarios en 12 líneas y 195 estaciones. Sus datos abiertos de afluencia se publican como archivos planos (CSV/Excel) con tres limitaciones:

- **Sin modelo multidimensional:** no permiten consultas analíticas (OLAP), historización ni agregaciones temporales/geográficas interactivas.
- **Heterogeneidad:** texto redundante, nombres de estaciones y líneas con variaciones, acentos corruptos y formatos de fecha inconsistentes.
- **Silos:** la afluencia está desconectada de datos operativos (frecuencias, averías, clima), lo que impide correlacionar causas de retraso o saturación.

## Objetivo general
Diseñar e implementar una solución de inteligencia de negocios para procesar, almacenar dimensionalmente (Data Warehouse y Data Mart) y explotar el histórico de afluencia del Metro CDMX, para evaluar la movilidad urbana y apoyar la toma de decisiones.

## Objetivos específicos
| # | Objetivo | Entregable |
|---|---|---|
| 1 | **ETL:** extraer, limpiar y estandarizar los datos abiertos; fechas en formato Kimball (`YYYYMMDD`) | `src/` en el repositorio |
| 2 | **Modelado dimensional:** DW en copo de nieve y Data Mart en estrella | `sql/` y página 4 |
| 3 | **Explotación:** tableros con `afluencia_pasajeros`, `afluencia_hora_pico`, `porcentaje_ocupacion` por estación y línea | `DASHBOARD_METRO_CDMX` |
| 4 | **Análisis predictivo:** proyectar días y horarios de mayor saturación (trabajo futuro) | Pendiente |

## Herramienta de explotación
La capa semántica y los dashboards se construyeron en **IBM Cognos Analytics**, según la propuesta del profesor. Power BI queda como alternativa compatible vía MySQL (ODBC), no como herramienta principal.
