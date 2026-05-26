# {{PROJECT_NAME}}

> Proyecto generado con install-harness — {{LANG}} / {{RUNTIME}}

## Comandos

| Acción        | Comando                                      |
|---------------|----------------------------------------------|
| Tests         | `{{TEST_RUNNER}}`                            |
| Init/verify   | `./init.sh`                                  |
| Dev           | `{{DEV_CMD}}`                                |
| Build         | `{{BUILD_CMD}}`                              |
| Lint          | `{{LINT_CMD}}`                               |

## Estructura

```
src/            Código fuente (App Router)
app/            Rutas y páginas (App Router)
tests/          Tests automáticos
e2e/            Tests end-to-end (Playwright)
docs/           Arquitectura, convenciones, verificación
progress/       Bitácora de sesiones del arnés
```
