# Arquitectura — Qué significa "hacer un buen trabajo"

> Este documento define el estándar de calidad. Los agentes revisores
> evalúan código contra este archivo. Si no está aquí, no es un requisito.

## Principios

1. **PSR-4 Autoload.** Todo el código en `src/` sigue PSR-4 con namespace
   raíz definido en `composer.json`. No hay `require`/`include` manuales.

2. **Separación de responsabilidades.** Lógica de dominio separada de IO
   y presentación. Controladores delegan a servicios, servicios a repositorios.

3. **Errores explícitos.** Las funciones que pueden fallar lanzan excepciones
   nombradas, no devuelven `null`.

4. **Inmutabilidad por defecto.** Usa `readonly` en propiedades de clases
   (PHP 8.1+). Los value objects son inmutables.

5. **Tipado estricto.** `declare(strict_types=1);` al inicio de cada archivo.

## Flujo de datos

```
usuario  ─→  controlador / entry point
               │
               ├─ construye modelos de dominio
               │
               └─→  repositorio / persistencia
```

## Qué NO hacer

- No usar `echo` para errores en CLI. Usa `fwrite(STDERR, ...)` y exit(1).
- No mezclar IO con lógica de dominio.
- No usar funciones globales para lógica de negocio.
- No añadir dependencias sin discutirlo primero en `feature_list.json`.
