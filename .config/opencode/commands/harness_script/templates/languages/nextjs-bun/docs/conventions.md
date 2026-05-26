# Convenciones de código

> Homogeneidad extrema. La IA predice mejor cuando el repositorio se parece
> a sí mismo en todas partes.

## Estilo Next.js / TypeScript (Bun)

- **Runtime:** Bun 1.0+ / Next.js 14+ / TypeScript 5+.
- **Formato:** ESLint + Prettier + strict. Líneas máximo 100 caracteres.
- **Imports:** ESM (`import`/`export`). Path aliases con `@/`. Bun resuelve `.ts` nativamente.
- **Strings:** comillas dobles `"..."` siempre (Prettier default).

## Nombres

| Tipo                    | Convención           | Ejemplo                    |
|-------------------------|----------------------|----------------------------|
| Páginas / rutas         | `kebab-case` dirs    | `app/user-profile/`       |
| Componentes             | `PascalCase.tsx`     | `UserProfile.tsx`         |
| Server Actions          | `camelCase.ts`       | `createUser.ts`           |
| Utilidades              | `camelCase.ts`       | `formatDate.ts`           |
| Tipos / Interfaces      | `PascalCase`         | `UserProfile` / `UserData` |
| Constantes              | `UPPER_SNAKE`        | `API_BASE_URL`            |

## Estructura de archivos

```
app/
  layout.tsx              Root layout
  page.tsx                Home page
  api/
    route.ts              API route handler
  [dynamic]/
    page.tsx              Dynamic route
components/
  ui/                     Reusable UI components
  features/               Feature-specific components
lib/
  actions.ts              Server Actions
  utils.ts                Utility functions
  types.ts                Shared types
```

## Tests

- Tests E2E: `e2e/<feature>.spec.ts` con Playwright.
- Componentes: `@testing-library/react` + bun:test.
- Nombres de test descriptivos: `it("renders user profile")`.

## Server vs Client

```tsx
// Server Component (default) — sin "use client"
export default function UserProfile({ params }: Props) {
  // Puede hacer fetch, acceder a DB, etc.
}

// Client Component — requiere "use client"
"use client"
import { useState } from "react"
export default function Counter() {
  const [count, setCount] = useState(0)
}
```

## Manejo de errores

Errores del dominio:

```typescript
class AppError extends Error {
  constructor(message: string, public statusCode: number = 500) {
    super(message);
    this.name = "AppError";
  }
}

class NotFoundError extends AppError {
  constructor(resource: string) {
    super(`${resource} not found`, 404);
    this.name = "NotFoundError";
  }
}
```

Usa `error.tsx` para error boundaries en el App Router.

## Comentarios

Por defecto **no** se escriben. Solo se permiten cuando explican un *por qué*
no obvio. Los nombres deben hacer el resto.
