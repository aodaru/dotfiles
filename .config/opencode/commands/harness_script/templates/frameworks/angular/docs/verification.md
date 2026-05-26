# Verificación — Cómo demostrar que el trabajo funciona

> Regla de oro: **el agente no dice "funciona", lo demuestra**.
> Toda feature termina con evidencia ejecutable, no con afirmaciones.

## Nivel 1 — Tests unitarios (obligatorio)

Todo componente y servicio público tiene al menos un test `.spec.ts` que:

1. Cubre el camino feliz.
2. Cubre al menos un camino de error si puede fallar.

Comando:
```bash
{{TEST_RUNNER}}
```

## Nivel 2 — Build (obligatorio antes de cerrar)

```bash
ng build
```

No debe haber errores de build.

## Nivel 3 — Lint (obligatorio antes de cerrar)

```bash
ng lint
```

## Anti-patrones (no hacer)

- ❌ "He añadido el componente, debería funcionar." → falta test ejecutable.
- ❌ Testear implementación interna. → testea comportamiento.
- ❌ Marcar la feature como `done` sin pasar `./init.sh`.

## Verificación final antes de cerrar

```bash
./init.sh           # debe terminar con [OK] Entorno listo
```

Si `./init.sh` está rojo, **no** marques nada como `done`. Anota el bloqueo
en `progress/current.md` con estado `blocked` en `feature_list.json`.
