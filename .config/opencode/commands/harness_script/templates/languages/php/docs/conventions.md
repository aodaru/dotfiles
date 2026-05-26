# Convenciones de código

> Homogeneidad extrema. La IA predice mejor cuando el repositorio se parece
> a sí mismo en todas partes.

## Estilo PHP

- **Versión:** PHP 8.1+.
- **Formato:** PSR-12. Líneas máximo 120 caracteres.
- **strict_types:** `declare(strict_types=1);` siempre al inicio.
- **Imports:** `use` statements agrupados. Uno por línea.
- **Strings:** comillas dobles `"..."` con interpolación, simples `'...'` sin.

## Nombres

| Tipo                    | Convención        | Ejemplo               |
|-------------------------|-------------------|-----------------------|
| Namespaces              | `PascalCase`      | `App\Domain`          |
| Clases                  | `PascalCase`      | `Note`                |
| Interfaces              | `PascalCase` + `Interface` | `NoteRepositoryInterface` |
| Métodos / funciones     | `camelCase`       | `loadNotes`           |
| Constantes              | `UPPER_SNAKE`     | `DEFAULT_PATH`        |
| Variables               | `snake_case`      | `$note_list`          |

## Estructura de archivo

Cada archivo en `src/` empieza con:

```php
<?php

declare(strict_types=1);

namespace App\Module;

use App\Other\Thing;
```

## Tests

- Un archivo de test por clase: `tests/ModuleTest.php`.
- Extiende `PHPUnit\Framework\TestCase`.
- Cada test limpia su estado (usar `setUp()`/`tearDown()`).
- Nombres de test descriptivos: `testLoadReturnsEmptyWhenFileMissing`.

## Manejo de errores

Excepciones del dominio:

```php
class DomainException extends \Exception
{
}

class NotFoundException extends DomainException
{
    public function __construct(string $id)
    {
        parent::__construct("Resource not found: {$id}");
    }
}
```

El CLI captura excepciones del dominio, imprime mensaje a `STDERR` y sale
con código 1. Nunca propaga stack traces al usuario.

## Comentarios

Por defecto **no** se escriben. Solo se permiten cuando explican un *por qué*
no obvio. Los nombres deben hacer el resto.
