# 3. Fuentes de datos

| Fuente | Formato | Estado | Campos clave |
|---|---|---|---|
| Afluencia diaria del Metro (Datos Abiertos CDMX) | CSV | **Real** | fecha, anio, mes, linea, estacion, afluencia |
| Despacho de convoyes (PCC) | Excel / logs | Simulado / pendiente | id_tren, id_linea, fecha_hora_salida, intervalo_headway_seg |
| Bitácora de incidencias | CSV / XLSX | **Simulado** | id_incidencia, tipo_incidencia, gravedad, tiempo_retraso_min |
| Registro meteorológico por zona | JSON / CSV | **Simulado** | id_sensor, fecha_hora, temperatura_c, clima_estado |

## Fuente real: afluencia diaria
- **Granularidad:** un registro por fecha, línea y estación.
- **Volumen:** cientos de miles de registros (histórico desde 2010).
- **Ingesta:** por lotes, con `python -m src.run_etl`.

## Problemas detectados en la muestra revisada
Muestra de 19 filas (1 de enero de 2010, líneas 1 y 3 a 9):
- **Acentos corruptos por doble codificación** en 8 de 19 nombres de estación (ej. `Isabel la CatÃƒÂ³lica`). Se reparan en la regla R01.
- Nombres con separadores especiales (`La Villa/Basílica`, `Etiopía/Plaza de la Transparencia`).
- Línea escrita como `Linea 1` (sin acento), sin código numérico independiente.
- Las columnas `anio` y `mes` son redundantes con `fecha`.
