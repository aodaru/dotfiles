# Convenciones de código — Angular

> Homogeneidad extrema. La IA predice mejor cuando el repositorio se parece
> a sí mismo en todas partes.

## Estilo Angular / TypeScript

- **Versión:** Angular 16+ / TypeScript 5+.
- **Formato:** ESLint + Prettier. Líneas máximo 100 caracteres.
- **Imports:** Path aliases con `@/` o paths de TypeScript.
- **Strings:** comillas dobles `"..."`.
- **Test runner:** {{ANGULAR_TEST_RUNNER}}

## Nombres

| Tipo                    | Convención                    | Ejemplo                       |
|-------------------------|-------------------------------|-------------------------------|
| Componentes             | `kebab-case.component.ts`     | `user-profile.component.ts`  |
| Servicios               | `kebab-case.service.ts`       | `user.service.ts`            |
| Módulos                 | `kebab-case.module.ts`        | `shared.module.ts`           |
| Directivas              | `kebab-case.directive.ts`     | `highlight.directive.ts`     |
| Pipes                   | `kebab-case.pipe.ts`          | `truncate.pipe.ts`           |
| Guards                  | `kebab-case.guard.ts`         | `auth.guard.ts`              |
| Interfaces / Tipos      | `PascalCase`                  | `UserProfile` / `UserData`   |
| Constantes              | `UPPER_SNAKE`                 | `API_BASE_URL`               |

## Sufijos obligatorios

Todo archivo Angular lleva el sufijo correspondiente:
- `*.component.ts` / `*.component.html` / `*.component.scss`
- `*.service.ts`
- `*.module.ts`
- `*.directive.ts`
- `*.pipe.ts`
- `*.guard.ts`

## Estructura de archivos

```
src/
  app/
    core/                   Servicios singleton, guards
    shared/                 Componentes/directivas/pipes compartidos
    features/               Módulos por feature
      user/
        user-profile/
          user-profile.component.ts
          user-profile.component.html
          user-profile.component.scss
        user.service.ts
    app.component.ts
    app.module.ts (o app.config.ts si standalone)
```

## Tests

- Un archivo `.spec.ts` junto a cada componente/servicio.
- Usa TestBed para tests de componentes.
- Nombres de test descriptivos: `it("should render user name when loaded")`.

## Comentarios

Por defecto **no** se escriben. Solo se permiten cuando explican un *por qué*
no obvio. Los nombres deben hacer el resto.
