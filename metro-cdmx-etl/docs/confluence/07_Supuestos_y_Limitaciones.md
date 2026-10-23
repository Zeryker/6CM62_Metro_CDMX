# 7. Supuestos y limitaciones

## Datos simulados
Clima, incidencias, retraso y hora pico **no existen como datos públicos**. Con `--simulate` se generan con semilla fija (42) y se marcan con `es_dato_simulado = 1`:
- Clima: uno por día (60 % despejado, 25 % nublado, 15 % lluvia).
- Incidencias: 3 % de las filas, con retraso entre 3 y 25 minutos.
- Hora pico: entre 10 % y 16 % de la afluencia diaria.

Los KPI de retraso del dashboard (ej. promedio de minutos) provienen de datos simulados y no deben presentarse como mediciones reales.

## Convenciones del proyecto
- **`porcentaje_ocupacion`** es un proxy: afluencia del día entre el máximo histórico de la estación. No mide ocupación física de trenes.
- **`alerta_dosificacion`** se activa con un umbral del 90 % (configurable en `config.py`).
- **`tipo_periodo`** por año: ≤2019 pre-pandemia, 2020-2021 pandemia, ≥2022 post-pandemia.
- **`es_festivo`** es aproximado: no incluye Semana Santa ni el 1 de octubre sexenal.
- Los colores de línea y el número de estaciones por línea son referenciales; verificar contra fuente oficial.

## Limitaciones
- La afluencia es diaria; no hay granularidad horaria real.
- No hay datos públicos de trenes ni de velocidad o intervalos (`velocidad_operativa_real_kmh`, `intervalo_headway_seg` y `distancia_intertren_m` quedan vacíos).
- El análisis predictivo (objetivo 4) aún no está implementado.

## Pendientes
- Unificar en los diagramas la PK de la tabla de hechos (`id_fact` vs `id_afluencia`; el código usa `id_afluencia`).
- Corregir en los objetivos y el diagrama de arquitectura la mención a Power BI como herramienta principal.
- Ampliar `ALIAS_ESTACIONES` tras ejecutar el ETL con el histórico completo.
