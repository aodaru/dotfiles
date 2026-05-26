# Arquitectura — Qué significa "hacer un buen trabajo"

> Este documento define el estándar de calidad. Los agentes revisores
> evalúan código contra este archivo. Si no está aquí, no es un requisito.

## Principios

1. **Módulos ES.** Usa ESM (`import`/`export`) por defecto. CommonJS solo
   si el entorno lo requiere explícitamente.

2. **Separación de responsabilidades.** Lógica de dominio separada de IO
   y presentación. No mezclar capas.

3. **Errores explícitos.** Las funciones que pueden fallar lanzan errores
   nombrados (clases que extienden `Error`), no devuelven `null`.

4. **Inmutabilidad por defecto.** Usa `const` siempre. `let` solo cuando
   la reasignación es necesaria. Nunca `var`.

5. **Funciones puras.** La lógica de dominio debe ser testeable sin
   efectos secundarios. IO va en las capas externas.

## Flujo de datos

```
usuario  ─→  CLI / entrada
               │
               ├─ construye modelos de dominio
               │
               └─→  persistencia / IO
```

## Qué NO hacer

- No usar `console.log()` para errores. Usa `console.error()` y process.exit(1).
- No mezclar IO con lógica de dominio.
- No mutar parámetros de función.
- No añadir dependencias sin discutirlo primero en `feature_list.json`.
