# Convenciones de código — React

> Homogeneidad extrema. La IA predice mejor cuando el repositorio se parece
> a sí mismo en todas partes.

## Estilo React / TypeScript

- **Versión:** React 18+ / TypeScript 5+ / Vite.
- **Formato:** ESLint + Prettier. Líneas máximo 100 caracteres.
- **Imports:** ESM. Path aliases con `@/`.
- **Strings:** comillas dobles `"..."`.

## Nombres

| Tipo                    | Convención              | Ejemplo                    |
|-------------------------|-------------------------|----------------------------|
| Componentes             | `PascalCase.tsx`        | `UserProfile.tsx`         |
| Hooks                   | `useCamelCase.ts`       | `useAuth.ts`              |
| Utilidades              | `camelCase.ts`          | `formatDate.ts`           |
| Tipos / Interfaces      | `PascalCase`            | `UserProfile` / `UserData` |
| Constantes              | `UPPER_SNAKE`           | `API_BASE_URL`            |
| CSS Modules             | `Component.module.css`  | `Button.module.css`       |

## Estructura de archivos

```
src/
  components/
    ui/                    Reusable UI components
    features/              Feature-specific components
  hooks/                   Custom hooks
  lib/                     Utility functions
  types/                   Shared TypeScript types
  App.tsx                  Root component
  main.tsx                 Entry point
```

## Patrones de componente

```tsx
// Componente funcional con tipado
interface UserProfileProps {
  userId: string;
}

export function UserProfile({ userId }: UserProfileProps) {
  const { data, isLoading } = useUserProfile(userId);

  if (isLoading) return <LoadingSkeleton />;

  return <div>{data.name}</div>;
}
```

## Hooks custom

```tsx
function useUserProfile(userId: string) {
  const [data, setData] = useState<UserData | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchUser(userId).then(setData).finally(() => setIsLoading(false));
  }, [userId]);

  return { data, isLoading };
}
```

## Tests

- Un archivo de test por componente: `tests/Component.test.tsx`.
- Usa `@testing-library/react` + `vitest`.
- Nombres de test descriptivos: `it("renders user name when loaded")`.
- Testea comportamiento, no implementación.

## Comentarios

Por defecto **no** se escriben. Solo se permiten cuando explican un *por qué*
no obvio. Los nombres deben hacer el resto.
