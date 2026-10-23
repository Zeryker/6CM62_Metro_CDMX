# 4. Modelo dimensional y diccionario de datos

## Esquemas
- **Data Warehouse (copo de nieve):** `DIM_ANIO → DIM_MES → DIM_FECHA` y `DIM_LINEA → DIM_ESTACION`, normalizados.
- **Data Mart (estrella):** vista `VW_DM_OPERACION`, que desnormaliza todo alrededor de `FACT_OPERACION`.
- **Granularidad de la tabla de hechos:** una fila por estación por día.

## Diccionario de datos

### FACT_OPERACION
| Columna | Tipo | Descripción | Origen |
|---|---|---|---|
| id_afluencia (PK) | INT | Llave sustituta | Generada |
| id_fecha (FK) | INT | `YYYYMMDD` | Real |
| id_estacion (FK) | INT | Estación-línea | Real |
| id_clima, id_incidencia, id_tren (FK) | INT | 0 = "Sin dato" | Simulado o 0 |
| afluencia_pasajeros | INT | Pasajeros que ingresan en el día | **Real** |
| afluencia_hora_pico | INT | Estimación de hora pico | Simulado |
| porcentaje_ocupacion | DECIMAL(5,2) | % respecto al máximo histórico de la estación (proxy) | Derivado |
| velocidad_operativa_real_kmh, intervalo_headway_seg, distancia_intertren_m | numérico | Sin fuente pública | Vacío |
| tiempo_retraso_min | INT | Minutos de retraso | Simulado |
| alerta_dosificacion | TINYINT | 1 si `porcentaje_ocupacion` ≥ 90 | Derivado |
| es_dato_simulado | TINYINT | 1 si las columnas operativas son simuladas | Control |

### Dimensiones
| Tabla | Columnas |
|---|---|
| DIM_FECHA | id_fecha (PK), fecha, dia_semana, es_fin_de_semana, es_festivo, id_mes (FK) |
| DIM_MES | id_mes (PK, `YYYYMM`), nombre_mes, trimestre, anio (FK) |
| DIM_ANIO | anio (PK), tipo_periodo (Pre-pandemia / Pandemia / Post-pandemia) |
| DIM_LINEA | id_linea (PK), nombre_linea, color |
| DIM_ESTACION | id_estacion (PK), nombre_estacion, id_linea (FK) |
| DIM_CLIMA | id_clima (PK), clima_estado, aplica_marcha_seguridad |
| DIM_INCIDENCIA | id_incidencia (PK), tipo_incidencia, descripcion, gravedad |
| DIM_TREN | id_tren (PK), id_modelo (FK) |
| CAT_MODELO_TREN | id_modelo (PK), modelo_tren, capacidad_pasajeros, num_wagones, velocidad_diseno_kmh |

> `DIM_AÑO` de la propuesta se llama `DIM_ANIO` en el código para evitar problemas con la Ñ en nombres de archivo y tablas.

## Cardinalidades
`FACT_OPERACION` N:1 con DIM_FECHA, DIM_ESTACION, DIM_CLIMA, DIM_INCIDENCIA y DIM_TREN. Segundo nivel: DIM_FECHA N:1 DIM_MES N:1 DIM_ANIO; DIM_ESTACION N:1 DIM_LINEA; DIM_TREN N:1 CAT_MODELO_TREN.
