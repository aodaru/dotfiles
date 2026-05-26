# Arquitectura — Qué significa "hacer un buen trabajo"

> Este documento define el estándar de calidad para un proyecto Angular.
> Los agentes revisores evalúan código contra este archivo.

## Principios

1. **Módulos como unidad de organización.** La app se organiza en NgModules
   o Standalone Components (Angular 14+). Standalone preferido para nuevos
   proyectos.

2. **Servicios + DI.** La lógica de negocio vive en servicios inyectables.
   Los componentes delegan a servicios, no contienen lógica de negocio.

3. **Inyección de dependencias.** Los servicios se inyectan vía constructor.
   No usar `new` para crear servicios. Usar `providedIn: 'root'` por defecto.

4. **Reactividad.** Usa RxJS para flujos asíncronos. Signals (Angular 16+)
   para estado reactivo simple.

5. **Componentes como presentación.** Los componentes solo orquestan
   servicios y renderizan templates. Lógica de negocio en servicios.

6. **Patrón Smart/Dumb.** Componentes smart (con servicios) y dumb
   (presentacionales, solo @Input/@Output).

## Flujo de datos

```
usuario  ─→  Template (event binding)
               │
               ├─ Component (método del controller)
               │
               └─→  Service (lógica de negocio)
                        │
                        └─→  HTTP / Estado / Storage
```

## Qué NO hacer

- No usar `console.log()` en producción.
- No acceder al DOM directamente. Usa templates y bindings.
- No poner lógica de negocio en componentes.
- No usar `any` en TypeScript. Usa tipos específicos.
- No añadir dependencias sin discutirlo primero en `feature_list.json`.
