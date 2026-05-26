# Convenciones de código

> Homogeneidad extrema. La IA predice mejor cuando el repositorio se parece
> a sí mismo en todas partes.

## Estilo TypeScript (Bun)

- **Runtime:** Bun 1.0+ (ejecuta .ts nativamente, sin paso de compilación).
- **Formato:** ESLint + Prettier + strict. Líneas máximo 100 caracteres.
- **Imports:** ESM (`import`/`export`). Bun soporta ESM y .ts nativamente.
- **Strings:** comillas dobles `"..."` siempre (Prettier default).
- **Template literals** para interpolación. Nada de concatenación.

## Nombres

| Tipo                    | Convención        | Ejemplo               |
|-------------------------|-------------------|-----------------------|
| Archivos                | `camelCase.ts`    | `noteService.ts`      |
| Interfaces / Tipos      | `PascalCase`      | `Note` / `NoteData`   |
| Clases                  | `PascalCase`      | `NoteService`         |
| Funciones / variables   | `camelCase`       | `loadNotes`           |
| Constantes              | `UPPER_SNAKE`     | `DEFAULT_PATH`        |
| Privadas                | prefijo `_`       | `_internal`           |

## Estructura de archivo

Cada archivo en `src/` empieza con:

```typescript
/** Una línea describiendo el propósito del módulo. */
import type { Something } from "./types.ts";
import { something } from "./dependency.ts";
```

Nota: Bun resuelve extensiones `.ts` nativamente. Usa `.ts` en los imports.

## Tests

- Un archivo de test por módulo: `tests/<módulo>.test.ts`.
- Usa `bun:test` con `describe`/`it`/`expect`.
- Cada test limpia su estado (usar `beforeEach`/`afterEach`).
- Nombres de test descriptivos: `it("returns empty when file is missing")`.

## Manejo de errores

Errores del dominio:

```typescript
class DomainError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "DomainError";
  }
}

class NotFoundError extends DomainError {
  constructor(id: string) {
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
