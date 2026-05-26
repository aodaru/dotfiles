# Convenciones de código — Vue

> Homogeneidad extrema. La IA predice mejor cuando el repositorio se parece
> a sí mismo en todas partes.

## Estilo Vue / TypeScript

- **Versión:** Vue 3+ / TypeScript 5+ / Vite.
- **Formato:** ESLint + Prettier. Líneas máximo 100 caracteres.
- **Imports:** Path aliases con `@/`.
- **Strings:** comillas dobles `"..."`.

## Nombres

| Tipo                    | Convención              | Ejemplo                    |
|-------------------------|-------------------------|----------------------------|
| Componentes             | `PascalCase.vue`        | `UserProfile.vue`         |
| Composables             | `useCamelCase.ts`       | `useAuth.ts`              |
| Utilidades              | `camelCase.ts`          | `formatDate.ts`           |
| Tipos / Interfaces      | `PascalCase`            | `UserProfile` / `UserData` |
| Constantes              | `UPPER_SNAKE`           | `API_BASE_URL`            |
| Stores (Pinia)          | `useCamelCaseStore.ts`  | `useUserStore.ts`         |

## Estructura de archivos

```
src/
  components/
    ui/                    Reusable UI components
    features/              Feature-specific components
  composables/             Custom composables
  stores/                  Pinia stores
  lib/                     Utility functions
  types/                   Shared TypeScript types
  App.vue                  Root component
  main.ts                  Entry point
```

## SFC Pattern

```vue
<script setup lang="ts">
interface Props {
  userId: string;
}

const props = defineProps<Props>();
const emit = defineEmits<{
  (e: "update", id: string): void;
}>();

const { data, isLoading } = useUserProfile(props.userId);
</script>

<template>
  <div v-if="isLoading">Loading...</div>
  <div v-else>{{ data.name }}</div>
</template>

<style scoped>
/* Scoped styles here */
</style>
```

## Tests

- Un archivo de test por componente: `tests/Component.test.ts`.
- Usa `@vue/test-utils` + `vitest`.
- Nombres de test descriptivos: `it("renders user name when loaded")`.
- Testea comportamiento, no implementación.

## Comentarios

Por defecto **no** se escriben. Solo se permiten cuando explican un *por qué*
no obvio. Los nombres deben hacer el resto.
