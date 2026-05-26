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

if ! command -v bun >/dev/null 2>&1; then
  fail "bun no está instalado"
  exit 1
fi
ok "bun -> $(bun --version)"

for f in package.json next.config.js next.config.mjs next.config.ts; do
  if [ -f "$f" ]; then
    ok "Config de Next.js encontrado: $f"
    break
  fi
done

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

bun -e '
const fs = require("fs");
try {
  const data = JSON.parse(fs.readFileSync("feature_list.json", "utf8"));
  const valid = new Set(["pending", "in_progress", "done", "blocked"]);
  const inProgress = data.features.filter(f => f.status === "in_progress");
  if (inProgress.length > 1) {
    console.log("[FAIL]  Hay " + inProgress.length + " features en in_progress (máximo 1)");
    process.exit(1);
  }
  for (const f of data.features) {
    if (!valid.has(f.status)) {
      console.log("[FAIL]  Estado inválido en feature " + f.id + ": " + f.status);
      process.exit(1);
    }
  }
  console.log("[OK]    feature_list.json válido (" + data.features.length + " features)");
} catch (e) {
  console.log("[FAIL]  feature_list.json inválido: " + e.message);
  process.exit(1);
}
'

if [ $? -ne 0 ]; then EXIT_CODE=1; fi

echo ""
echo "── 4. Ejecutando tests ─────────────────────────────────"

if [ -d "tests" ] || [ -d "__tests__" ] || [ -d "e2e" ]; then
  if bunx playwright test 2>&1; then
    ok "Todos los tests pasan"
  else
    fail "Hay tests rotos"
    EXIT_CODE=1
  fi
else
  warn "Carpeta de tests no existe todavía"
fi

echo ""
echo "── 5. Resumen ──────────────────────────────────────────"

if [ $EXIT_CODE -eq 0 ]; then
  ok "Entorno listo. Puedes empezar a trabajar."
else
  fail "Entorno NO está listo. Resuelve los errores antes de avanzar."
fi

exit $EXIT_CODE
