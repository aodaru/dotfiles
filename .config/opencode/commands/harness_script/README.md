# install-harness

Genera el arnés de agentes (AGENTS.md, init.sh, docs/, .claude/, etc.) para
cualquier proyecto de software, parametrizado por lenguaje, runtime y
framework.

## Uso

```bash
# Auto-detectar lenguaje y generar arnés
python3 install.py

# Especificar lenguaje
python3 install.py --language python

# Con runtime y framework
python3 install.py --language typescript --runtime bun --framework react

# Angular con test runner específico
python3 install.py --language typescript --runtime node --framework angular --angular-test-runner jest

# Preview sin escribir
python3 install.py --dry-run

# Sobrescribir existente
python3 install.py --force
```

## Parámetros

| Parámetro                 | Descripción                                            |
|---------------------------|--------------------------------------------------------|
| `--language`              | python, javascript, typescript, php, nextjs (auto-detect) |
| `--runtime`               | node, bun (solo JS/TS/Next.js, default: node)         |
| `--framework`             | react, angular, vue (no aplica a nextjs)               |
| `--angular-test-runner`   | ng-test, jest (solo si --framework angular)            |
| `--dry-run`               | Preview sin escribir archivos                          |
| `--force`                 | Sobrescribir archivos existentes                       |
| `--target-dir`            | Directorio destino (default: directorio actual)        |

## Estructura

```
harness-subagents/
├── registry.json           # Variables por lenguaje/framework
├── install.py              # Script principal del installer
├── templates/
│   ├── core/               # Archivos genéricos (siempre se copian)
│   ├── languages/          # Templates por lenguaje+runtime
│   │   ├── python/
│   │   ├── javascript-node/
│   │   ├── javascript-bun/
│   │   ├── typescript-node/
│   │   ├── typescript-bun/
│   │   ├── php/
│   │   ├── nextjs-node/
│   │   └── nextjs-bun/
│   └── frameworks/         # Overlays por framework
│       ├── react/
│       ├── angular/
│       └── vue/
└── tests/
    ├── test_installer.py
    └── test_templates.py
```

## Tests

```bash
python3 -m unittest discover -s tests -v
```
