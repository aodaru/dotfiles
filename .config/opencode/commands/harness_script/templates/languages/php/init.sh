#!/usr/bin/env bash
set -u
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

ok()    { printf "${GREEN}[OK]${NC}    %s\n" "$1"; }
warn()  { printf "${YELLOW}[WARN]${NC}  %s\n" "$1"; }
fail()  { printf "${RED}[FAIL]${NC}  %s\n" "$1"; }

EXIT_CODE=0

echo "── 1. Verificando entorno ─────────────────────────────"

if ! command -v php >/dev/null 2>&1; then
  fail "php no está instalado"
  exit 1
fi
ok "php -> $(php --version | head -1)"

PHP_VERSION_OK=$(php -r 'echo PHP_VERSION_ID >= 80100 ? "1" : "0";')
if [ "$PHP_VERSION_OK" != "1" ]; then
  fail "Se requiere PHP >= 8.1"
  exit 1
fi
ok "Versión de PHP compatible"

if [ -f "composer.json" ]; then
  ok "composer.json existe"
  if command -v composer >/dev/null 2>&1; then
    ok "composer -> $(composer --version 2>/dev/null | head -1)"
  else
    warn "composer no está instalado (necesario para dependencias)"
  fi
else
  warn "composer.json no encontrado"
fi

echo ""
echo "── 2. Verificando archivos base del arnés ──────────────"

for f in AGENTS.md feature_list.json progress/current.md docs/architecture.md docs/conventions.md docs/verification.md CHECKPOINTS.md; do
  if [ ! -f "$f" ]; then
    fail "Falta archivo base: $f"
    EXIT_CODE=1
  else
    ok "Existe $f"
  fi
done

echo ""
echo "── 3. Validando feature_list.json ──────────────────────"

php -r '
$json = file_get_contents("feature_list.json");
$data = json_decode($json, true);
if ($data === null) { echo "[FAIL]  feature_list.json inválido: " . json_last_error_msg() . "\n"; exit(1); }
$valid = ["pending", "in_progress", "done", "blocked"];
$inProgress = array_filter($data["features"], fn($f) => $f["status"] === "in_progress");
if (count($inProgress) > 1) { echo "[FAIL]  Hay " . count($inProgress) . " features en in_progress (máximo 1)\n"; exit(1); }
foreach ($data["features"] as $f) {
    if (!in_array($f["status"], $valid)) { echo "[FAIL]  Estado inválido en feature {$f["id"]}: {$f["status"]}\n"; exit(1); }
}
echo "[OK]    feature_list.json válido (" . count($data["features"]) . " features)\n";
'

if [ $? -ne 0 ]; then EXIT_CODE=1; fi

echo ""
echo "── 4. Ejecutando tests ─────────────────────────────────"

if [ -f "vendor/bin/phpunit" ]; then
  if ./vendor/bin/phpunit 2>&1; then
    ok "Todos los tests pasan"
  else
    fail "Hay tests rotos"
    EXIT_CODE=1
  fi
else
  warn "PHPUnit no instalado (ejecuta composer install)"
fi

echo ""
echo "── 5. Resumen ──────────────────────────────────────────"

if [ $EXIT_CODE -eq 0 ]; then
  ok "Entorno listo. Puedes empezar a trabajar."
else
  fail "Entorno NO está listo. Resuelve los errores antes de avanzar."
fi

exit $EXIT_CODE
