# Verificación — Cómo demostrar que el trabajo funciona

> Regla de oro: **el agente no dice "funciona", lo demuestra**.
> Toda feature termina con evidencia ejecutable, no con afirmaciones.

## Nivel 1 — Tests unitarios (obligatorio)

Todo componente y composable público tiene al menos un test en `tests/` que:

1. Cubre el camino feliz (mount + interacción).
2. Cubre al menos un camino de error si el componente puede fallar.

Comando:
```bash
npx vitest run
```

## Nivel 2 — Build (obligatorio antes de cerrar)

```bash
npm run build
```

No debe haber errores de build.

## Anti-patrones (no hacer)

- ❌ "He añadido el componente, debería funcionar." → falta test ejecutable.
- ❌ Testear implementación (estado interno). → testea comportamiento
  visible (render, interacción).
- ❌ Marcar la feature como `done` sin pasar `./init.sh`.

## Verificación final antes de cerrar

```bash
./init.sh           # debe terminar con [OK] Entorno listo
```

Si `./init.sh` está rojo, **no** marques nada como `done`. Anota el bloqueo
en `progress/current.md` con estado `blocked` en `feature_list.json`.
