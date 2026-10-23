# 8. Control de versiones (Git)

Repositorio: `<URL>`. Flujo completo en `docs/CONTRIBUTING.md`.

- **Ramas:** `main` (estable), `develop` (integración), `feature/<nombre>-<tema>` (una por tarea).
- **Commits:** `tipo: descripción` (`feat`, `fix`, `docs`, `test`, `refactor`, `chore`).
- **Pull Requests:** cada cambio entra a `develop` con revisión de otro integrante.
- **Datos:** no se versionan (`data/raw` y `data/clean` están en `.gitignore`).

| Integrante | Área |
|---|---|
| Juan Carlos | Extracción y limpieza |
| Ernesto | Transformación y modelo |
| Diego | SQL, carga y Cognos |
| Jazmin | Pruebas, calidad y documentación |
