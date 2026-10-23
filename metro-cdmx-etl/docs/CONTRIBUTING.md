# Flujo de trabajo con Git

## Ramas
- `main`: solo código que corre y pasa las pruebas. No se hace commit directo.
- `develop`: integración del equipo.
- `feature/<nombre>-<tema>`: una rama por tarea (ej. `feature/jazmin-sql-ddl`).

## Mensajes de commit
`tipo: descripción corta en infinitivo`. Tipos: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`.
Ejemplos: `feat: agregar reparación de acentos corruptos`, `test: cubrir rechazo de afluencia negativa`.

## Ciclo de una tarea
```bash
git checkout develop && git pull
git checkout -b feature/<nombre>-<tema>
# ... trabajar ...
python -m pytest -q
git add <archivos> && git commit -m "feat: ..."
git push -u origin feature/<nombre>-<tema>
# Abrir Pull Request hacia develop; otro integrante lo revisa antes de fusionar
```

## Reparto sugerido
| Integrante | Área |
|---|---|
| Juan Carlos | `extract.py`, `clean.py`, reglas de limpieza |
| Ernesto | `transform.py`, `simulate.py`, modelo dimensional |
| Diego | `sql/`, `load.py`, carga a MySQL y conexión con Cognos |
| Jazmin | `tests/`, `quality.py`, documentación en Confluence |
