# Convenciones de código

> Homogeneidad extrema. La IA predice mejor cuando el repositorio se parece
> a sí mismo en todas partes.

## Estilo JavaScript (Bun)

- **Runtime:** Bun 1.0+.
- **Formato:** ESLint + Prettier. Líneas máximo 100 caracteres.
- **Imports:** ESM (`import`/`export`). Bun soporta ESM nativamente.
- **Strings:** comillas dobles `"..."` siempre (Prettier default).
- **Template literals** para interpolación. Nada de concatenación.

## Nombres

| Tipo                    | Convención        | Ejemplo               |
|-------------------------|-------------------|-----------------------|
| Archivos                | `camelCase.js`    | `noteService.js`      |
| Clases                  | `PascalCase`      | `Note`                |
| Funciones / variables   | `camelCase`       | `loadNotes`           |
| Constantes              | `UPPER_SNAKE`     | `DEFAULT_PATH`        |
| Privadas                | prefijo `_`       | `_internal`           |

## Estructura de archivo

Cada archivo en `src/` empieza con:

```javascript
/** Una línea describiendo el propósito del módulo. */
import { something } from "./dependency.js";
```

## Tests

- Un archivo de test por módulo: `tests/<módulo>.test.js`.
- Usa `bun:test` con `describe`/`it`/`expect`.
- Cada test limpia su estado (usar `beforeEach`/`afterEach`).
- Nombres de test descriptivos: `it("returns empty when file is missing")`.

## Manejo de errores

Errores del dominio:

```javascript
class DomainError extends Error {
  constructor(message) {
    super(message);
    this.name = "DomainError";
  }
}

class NotFoundError extends DomainError {
  constructor(id) {
    super(`Resource not found: ${id}`);
    this.name = "NotFoundError";
  }
}
```

El CLI captura errores del dominio, imprime mensaje a `stderr` y sale
con código 1. Nunca propaga stack traces al usuario.

## Comentarios

Por defecto **no** se escriben. Solo se permiten cuando explican un *por qué*
no obvio. Los nombres deben hacer el resto.
