# Arquitectura — Qué significa "hacer un buen trabajo"

> Este documento define el estándar de calidad. Los agentes revisores
> evalúan código contra este archivo. Si no está aquí, no es un requisito.

## Principios

1. **Capas claras.** Separa lógica de dominio de IO y presentación.
   No introducir capas adicionales hasta que haya una razón concreta
   documentada en `feature_list.json`.

2. **Sin dependencias externas.** Solo stdlib de Python. Si una feature
   requiere una dependencia, primero se discute (estado `blocked`).

3. **Errores explícitos.** Las funciones que pueden fallar lanzan
   excepciones nombradas, no devuelven `None`.

4. **Inmutabilidad por defecto.** Usa `@dataclass(frozen=True)` para
   modelos de dominio. Modificar = crear una nueva instancia.

5. **Atomicidad en disco.** Toda escritura a archivos se hace primero
   en un archivo temporal y luego `os.replace()`. Nunca dejar el archivo
   a medio escribir.

## Flujo de datos

```
usuario  ─→  cli (argparse)
               │
               ├─ construye modelos de dominio
               │
               └─→  storage (persistencia)
                        │
                        └─→  archivo en disco
```

## Qué NO hacer

- No usar `print()` para errores. Usa `sys.stderr` y exit code != 0.
- No mezclar IO con lógica de dominio.
- No leer/escribir archivos en cada operación dentro de un bucle.
  Carga al inicio, modifica en memoria, guarda al final.
- No añadir un sistema de configuración. La ruta del archivo se pasa
  explícitamente o usa la constante por defecto.
