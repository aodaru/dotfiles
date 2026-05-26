# Arquitectura — Qué significa "hacer un buen trabajo"

> Este documento define el estándar de calidad para un proyecto React.
> Los agentes revisores evalúan código contra este archivo.

## Principios

1. **Componentes como unidad base.** La UI se construye con componentes
   React funcionales. No hay class components salvo error boundaries.

2. **Hooks para lógica.** La lógica reutilizable vive en custom hooks
   (`use*`). Los componentes solo orquestan hooks y renderizan.

3. **Estado mínimo.** Usa `useState` para estado local, `useReducer` para
   estado complejo, y levanta el estado solo lo necesario. Context solo
   cuando el prop drilling sea un problema real.

4. **Unidireccional.** Los datos fluyen de arriba a abajo vía props.
   Los eventos fluyen de abajo a arriba vía callbacks.

5. **Separación de responsabilidades.** Componentes de UI (presentacionales)
   separados de componentes contenedores (con lógica).

6. **Vite como build tool.** Configuración estándar con Vite + React plugin.

## Flujo de datos

```
usuario  ─→  Event Handler
               │
               ├─ actualiza estado (useState / useReducer)
               │
               └─→  re-render del componente
                        │
                        └─→  efectos secundarios (useEffect / hooks custom)
```

## Qué NO hacer

- No usar `console.log()` en producción.
- No mutar estado directamente. Usa setters o dispatch.
- No usar `any` en TypeScript. Usa `unknown` y type guards.
- No poner lógica de negocio en componentes. Usa hooks o servicios.
- No añadir dependencias sin discutirlo primero en `feature_list.json`.
