# Arquitectura — Qué significa "hacer un buen trabajo"

> Este documento define el estándar de calidad. Los agentes revisores
> evalúan código contra este archivo. Si no está aquí, no es un requisito.

## Principios

1. **App Router.** Usa el App Router (`app/`) por defecto. No Pages Router
   salvo migración explícitamente documentada.

2. **Server Components por defecto.** Los componentes son Server Components
   a menos que necesiten interactividad (`"use client"`).

3. **Separación Server/Client.** Lógica de servidor en Server Components y
   Server Actions. Lógica de cliente mínima y aislada en Client Components.

4. **API Routes.** Usa Route Handlers (`app/api/`) para endpoints REST.
   Server Actions preferidos para mutaciones.

5. **Tipos estrictos.** `tsconfig.json` con `strict: true`. Nada de `any`
   salvo en casos excepcionales documentados.

6. **Errores explícitos.** Las funciones que pueden fallar lanzan errores
   nombrados o devuelven Result types, no `null` silencioso.

## Flujo de datos

```
usuario  ─→  Server Component / Route Handler
               │
               ├─ Server Actions (mutaciones)
               │
               ├─ consulta datos (fetch / ORM)
               │
               └─→  base de datos / API externa
```

## Qué NO hacer

- No usar `console.log()` en producción. Usa un logger estructurado.
- No mezclar lógica de servidor en Client Components.
- No usar `any`. Usa `unknown` y type guards.
- No acceder a variables de servidor en código de cliente.
- No añadir dependencias sin discutirlo primero en `feature_list.json`.
