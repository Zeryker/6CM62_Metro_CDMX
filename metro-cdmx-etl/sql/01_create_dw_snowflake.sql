-- Data Warehouse (modelo copo de nieve). MySQL 8 / MariaDB 10.5+
-- Jerarquía de tiempo: DIM_ANIO -> DIM_MES -> DIM_FECHA | Jerarquía geográfica: DIM_LINEA -> DIM_ESTACION
DROP VIEW IF EXISTS VW_DM_OPERACION;
DROP TABLE IF EXISTS FACT_OPERACION;
DROP TABLE IF EXISTS DIM_TREN;
DROP TABLE IF EXISTS CAT_MODELO_TREN;
DROP TABLE IF EXISTS DIM_INCIDENCIA;
DROP TABLE IF EXISTS DIM_CLIMA;
DROP TABLE IF EXISTS DIM_ESTACION;
DROP TABLE IF EXISTS DIM_LINEA;
DROP TABLE IF EXISTS DIM_FECHA;
DROP TABLE IF EXISTS DIM_MES;
DROP TABLE IF EXISTS DIM_ANIO;

CREATE TABLE DIM_ANIO (
  anio          SMALLINT    NOT NULL PRIMARY KEY,
  tipo_periodo  VARCHAR(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE DIM_MES (
  id_mes      INT         NOT NULL PRIMARY KEY,   -- YYYYMM
  nombre_mes  VARCHAR(15) NOT NULL,
  trimestre   TINYINT     NOT NULL,
  anio        SMALLINT    NOT NULL,
  CONSTRAINT fk_mes_anio FOREIGN KEY (anio) REFERENCES DIM_ANIO (anio)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE DIM_FECHA (
  id_fecha          INT         NOT NULL PRIMARY KEY,   -- YYYYMMDD (Kimball)
  fecha             DATE        NOT NULL UNIQUE,
  dia_semana        VARCHAR(12) NOT NULL,
  es_fin_de_semana  TINYINT(1)  NOT NULL,
  es_festivo        TINYINT(1)  NOT NULL,
  id_mes            INT         NOT NULL,
  CONSTRAINT fk_fecha_mes FOREIGN KEY (id_mes) REFERENCES DIM_MES (id_mes)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE DIM_LINEA (
  id_linea      TINYINT     NOT NULL PRIMARY KEY,
  nombre_linea  VARCHAR(20) NOT NULL UNIQUE,
  color         VARCHAR(7)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE DIM_ESTACION (
  id_estacion      INT          NOT NULL PRIMARY KEY,
  nombre_estacion  VARCHAR(100) NOT NULL,
  id_linea         TINYINT      NOT NULL,
  UNIQUE KEY uq_estacion_linea (nombre_estacion, id_linea),
  CONSTRAINT fk_estacion_linea FOREIGN KEY (id_linea) REFERENCES DIM_LINEA (id_linea)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE DIM_CLIMA (
  id_clima                 TINYINT     NOT NULL PRIMARY KEY,
  clima_estado             VARCHAR(30) NOT NULL,
  aplica_marcha_seguridad  TINYINT(1)  NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE DIM_INCIDENCIA (
  id_incidencia    TINYINT      NOT NULL PRIMARY KEY,
  tipo_incidencia  VARCHAR(50)  NOT NULL,
  descripcion      VARCHAR(200),
  gravedad         VARCHAR(20)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE CAT_MODELO_TREN (
  id_modelo             INT         NOT NULL PRIMARY KEY,
  modelo_tren           VARCHAR(30) NOT NULL,
  capacidad_pasajeros   INT NULL,
  num_wagones           TINYINT NULL,
  velocidad_diseno_kmh  SMALLINT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE DIM_TREN (
  id_tren    INT NOT NULL PRIMARY KEY,
  id_modelo  INT NOT NULL,
  CONSTRAINT fk_tren_modelo FOREIGN KEY (id_modelo) REFERENCES CAT_MODELO_TREN (id_modelo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE FACT_OPERACION (
  id_afluencia                  INT NOT NULL PRIMARY KEY,
  id_fecha                      INT NOT NULL,
  id_estacion                   INT NOT NULL,
  id_clima                      TINYINT NOT NULL DEFAULT 0,
  id_incidencia                 TINYINT NOT NULL DEFAULT 0,
  id_tren                       INT NOT NULL DEFAULT 0,
  afluencia_pasajeros           INT NOT NULL,
  afluencia_hora_pico           INT NULL,
  porcentaje_ocupacion          DECIMAL(5,2) NULL,
  velocidad_operativa_real_kmh  DECIMAL(5,1) NULL,
  intervalo_headway_seg         INT NULL,
  distancia_intertren_m         INT NULL,
  tiempo_retraso_min            INT NULL,
  alerta_dosificacion           TINYINT(1) NOT NULL DEFAULT 0,
  es_dato_simulado              TINYINT(1) NOT NULL DEFAULT 0,
  UNIQUE KEY uq_fecha_estacion (id_fecha, id_estacion),
  CONSTRAINT fk_fact_fecha      FOREIGN KEY (id_fecha)      REFERENCES DIM_FECHA (id_fecha),
  CONSTRAINT fk_fact_estacion   FOREIGN KEY (id_estacion)   REFERENCES DIM_ESTACION (id_estacion),
  CONSTRAINT fk_fact_clima      FOREIGN KEY (id_clima)      REFERENCES DIM_CLIMA (id_clima),
  CONSTRAINT fk_fact_incidencia FOREIGN KEY (id_incidencia) REFERENCES DIM_INCIDENCIA (id_incidencia),
  CONSTRAINT fk_fact_tren       FOREIGN KEY (id_tren)       REFERENCES DIM_TREN (id_tren)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
