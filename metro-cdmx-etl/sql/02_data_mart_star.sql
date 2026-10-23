-- Data Mart (modelo estrella): vista desnormalizada sobre el DW, lista para Cognos / Power BI.
CREATE OR REPLACE VIEW VW_DM_OPERACION AS
SELECT f.id_afluencia, d.id_fecha, d.fecha, d.dia_semana, d.es_fin_de_semana, d.es_festivo,
       m.nombre_mes, m.trimestre, a.anio, a.tipo_periodo,
       l.nombre_linea, e.nombre_estacion,
       c.clima_estado, c.aplica_marcha_seguridad,
       i.tipo_incidencia, i.gravedad,
       f.afluencia_pasajeros, f.afluencia_hora_pico, f.porcentaje_ocupacion,
       f.tiempo_retraso_min, f.alerta_dosificacion, f.es_dato_simulado
FROM FACT_OPERACION f
JOIN DIM_FECHA d       ON d.id_fecha = f.id_fecha
JOIN DIM_MES m         ON m.id_mes = d.id_mes
JOIN DIM_ANIO a        ON a.anio = m.anio
JOIN DIM_ESTACION e    ON e.id_estacion = f.id_estacion
JOIN DIM_LINEA l       ON l.id_linea = e.id_linea
JOIN DIM_CLIMA c       ON c.id_clima = f.id_clima
JOIN DIM_INCIDENCIA i  ON i.id_incidencia = f.id_incidencia
