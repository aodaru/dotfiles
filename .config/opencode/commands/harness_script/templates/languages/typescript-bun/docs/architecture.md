# Arquitectura — Qué significa "hacer un buen trabajo"

> Este documento define el estándar de calidad. Los agentes revisores
> evalúan código contra este archivo. Si no está aquí, no es un requisito.

## Principios

1. **Tipos estrictos.** `tsconfig.json` con `strict: true`. Nada de `any`
   salvo en casos excepcionales documentados.

2. **Módulos ES.** Usa ESM (`import`/`export`) por defecto.

3. **Separación de responsabilidades.** Lógica de dominio separada de IO
   y presentación. No mezclar capas.

4. **Errores explícitos.** Las funciones que pueden fallar lanzan errores
   nombrados (clases que extienden `Error`), no devuelven `null`.

5. **Inmutabilidad por defecto.** Usa `const` siempre. `let` solo cuando
   la reasignación es necesaria. `readonly` para propiedades de interfaz.

6. **Funciones puras.** La lógica de dominio debe ser testeable sin
   efectos secundarios. IO va en las capas externas.

## Flujo de datos

```
usuario  ─→  CLI / entrada
               │
               ├─ construye modelos de dominio (tipados)
               │
               └─→  persistencia / IO
```

## Qué NO hacer

- No usar `console.log()` para errores. Usa `console.error()` y process.exit(1).
- No mezclar IO con lógica de dominio.
- No mutar parámetros de función.
- No usar `any`. Usa `unknown` y type guards si el tipo no se conoce.
- No añadir dependencias sin discutirlo primero en `feature_list.json`.
