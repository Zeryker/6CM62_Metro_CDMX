# 2. Arquitectura

| Capa | Componente | Tecnología |
|---|---|---|
| 1. Fuentes (OLTP) | Afluencia diaria (real); despachos, incidencias y clima (simulados) | CSV / Excel |
| 2. Integración y ETL | Extracción, limpieza, claves Kimball, carga | Python (pandas, SQLAlchemy) |
| 3. Almacenamiento | Data Warehouse (copo de nieve) y Data Mart (estrella, vista `VW_DM_OPERACION`) | MySQL |
| 4. Explotación | Módulo de datos `DM_METRO_CDMX`, dashboard `DASHBOARD_METRO_CDMX` | IBM Cognos Analytics |

## Flujo
`CSV crudo → extract → clean → transform → (simulate) → CSV + MySQL → Cognos`

## Decisiones de diseño
- **Procesamiento por lotes (batch):** el histórico es estático; no se requiere tiempo real.
- **Doble salida (CSV y MySQL):** Cognos consume los CSV (como ya se hizo en el módulo de datos); MySQL aporta integridad referencial y la vista estrella.
- **Miembro "Sin dato" (id 0)** en cada dimensión opcional, para que ninguna fila de hechos se pierda en los joins.
- **Estación = (nombre, línea):** una estación de correspondencia aparece una vez por línea.
