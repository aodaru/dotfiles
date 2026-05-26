# Arquitectura — Qué significa "hacer un buen trabajo"

> Este documento define el estándar de calidad para un proyecto Vue.
> Los agentes revisores evalúan código contra este archivo.

## Principios

1. **Composition API.** Usa la Composition API con `<script setup>` por
   defecto. Options API solo para migraciones documentadas.

2. **SFC (Single File Components).** Cada componente es un archivo `.vue`
   con `<template>`, `<script setup>`, y `<style scoped>`.

3. **Composables para lógica.** La lógica reutilizable vive en composables
   (`use*`). Los componentes solo orquestan composables y renderizan.

4. **Estado mínimo.** Usa `ref` y `reactive` para estado local. Pinia
   para estado global. Proporciona/inyecta para dependencias cercanas.

5. **Unidireccional.** Los datos fluyen de arriba a abajo vía props.
   Los eventos fluyen de abajo a arriba vía `emit`.

6. **Vite como build tool.** Configuración estándar con Vite + Vue plugin.

## Flujo de datos

```
usuario  ─→  Template (event binding)
               │
               ├─ Script setup (composable / función local)
               │
               └─→  Composable (lógica reutilizable)
                        │
                        └─→  Store (Pinia) / HTTP / Storage
```

## Qué NO hacer

- No usar `console.log()` en producción.
- No mutar props directamente.
- No usar `any` en TypeScript. Usa tipos específicos.
- No poner lógica de negocio en componentes. Usa composables.
- No añadir dependencias sin discutirlo primero en `feature_list.json`.
