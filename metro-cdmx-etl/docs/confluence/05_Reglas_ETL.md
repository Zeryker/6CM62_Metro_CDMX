# 5. Reglas del ETL

| ID | Regla | Si no se cumple |
|---|---|---|
| R01 | Reparar acentos corruptos (doble codificación UTF-8) | n/a (se corrige) |
| R02 | Quitar espacios extra y normalizar Unicode | n/a (se corrige) |
| R03 | `fecha` convertible a fecha (ISO o día/mes/año) | Rechazo `fecha_invalida` |
| R04 | `linea` reconocible (1 a 9, A, B, 12) | Rechazo `linea_no_reconocida` |
| R05 | `estacion` no vacía; `afluencia` numérica | Rechazo `estacion_vacia` / `afluencia_nula_o_no_numerica` |
| R06 | `afluencia` ≥ 0 | Rechazo `afluencia_negativa` |
| R07 | `anio` y `mes` coherentes con `fecha` | Se reporta; la fecha manda |
| R08 | Unificar variantes de nombre de estación; nombre canónico = el más frecuente | n/a (se corrige) |
| R09 | Eliminar duplicados exactos | Se descarta y se cuenta |
| R10 | Conflicto de llave (misma fecha, línea y estación con distinta afluencia) | Se conserva el primero y se reporta |

## Trazabilidad
- Las filas rechazadas se guardan en `RECHAZADOS.csv` con el número de fila original y el motivo.
- Cada ejecución genera `REPORTE_CALIDAD.md` con el flujo de registros (entrada, rechazos, duplicados, salida).
- Alias manuales de estaciones: `ALIAS_ESTACIONES` en `src/config.py`.

## Resultado sobre la muestra (19 filas)
19 entradas, 0 rechazos, 0 duplicados, 19 salidas, 8 nombres de estación reparados.
