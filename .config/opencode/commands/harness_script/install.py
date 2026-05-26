"""install-harness: Genera el arnés de agentes para un proyecto de software."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

COMMAND_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = COMMAND_DIR / "templates"
REGISTRY_PATH = COMMAND_DIR / "registry.json"
MANIFEST_FILE = ".harness_manifest.json"

LANG_ALIASES: dict[str, str] = {
    "js": "javascript",
    "ts": "typescript",
}

LANG_RUNTIME_MAP: dict[str, str] = {
    "javascript": "node",
    "typescript": "node",
    "nextjs": "node",
}


def load_registry() -> dict[str, Any]:
    with open(REGISTRY_PATH, encoding="utf-8") as f:
        return json.load(f)


def detect_language(target_dir: Path) -> tuple[str | None, str | None, str | None]:
    if (target_dir / "angular.json").exists():
        return "typescript", "node", "angular"
    if (target_dir / "next.config.js").exists() or (target_dir / "next.config.mjs").exists() or (target_dir / "next.config.ts").exists():
        return "nextjs", "node", None
    if (target_dir / "composer.json").exists():
        return "php", None, None
    if (target_dir / "requirements.txt").exists() or (target_dir / "pyproject.toml").exists():
        return "python", None, None
    if (target_dir / "package.json").exists():
        has_tsconfig = (target_dir / "tsconfig.json").exists()
        lang = "typescript" if has_tsconfig else "javascript"
        return lang, "node", None
    return None, None, None


def resolve_language_key(lang: str, runtime: str | None) -> str:
    if lang == "python" or lang == "php":
        return lang
    runtime = runtime or LANG_RUNTIME_MAP.get(lang, "node")
    return f"{lang}-{runtime}"


def validate_framework(lang: str, framework: str | None, registry: dict[str, Any]) -> str | None:
    if framework is None:
        return None
    if lang == "nextjs" and framework is not None:
        return f"nextjs no acepta --framework (ya es fullstack). Se pasó: {framework}"
    fw_data = registry["frameworks"].get(framework)
    if fw_data is None:
        return f"Framework desconocido: {framework}. Válidos: {', '.join(registry['frameworks'].keys())}"
    lang_key_prefix = lang.split("-")[0] if "-" in lang else lang
    compatible = [c.split("-")[0] if "-" in c else c for c in fw_data["compatible_languages"]]
    if lang_key_prefix not in compatible:
        return f"Framework {framework} no es compatible con {lang}. Compatibles: {', '.join(fw_data['compatible_languages'])}"
    return None


def resolve_angular_test_runner(
    framework: str | None,
    angular_test_runner: str | None,
    runtime: str | None,
    registry: dict[str, Any],
) -> str | None:
    if framework != "angular":
        return None
    fw_data = registry["frameworks"]["angular"]
    if angular_test_runner == "jest":
        return fw_data["test_cmd_jest"]
    if angular_test_runner == "ng-test":
        return fw_data["test_cmd_ng"]
    default = fw_data["test_runner_default_node"] if runtime == "node" else fw_data["test_runner_default_bun"]
    return fw_data["test_cmd_jest"] if default == "jest" else fw_data["test_cmd_ng"]


def collect_template_files(
    language_key: str,
    framework: str | None,
) -> list[tuple[Path, Path]]:
    files: list[tuple[Path, Path]] = []

    core_dir = TEMPLATES_DIR / "core"
    for root, _dirs, filenames in os.walk(core_dir):
        for fname in filenames:
            src = Path(root) / fname
            rel = src.relative_to(core_dir)
            files.append((src, rel))

    lang_dir = TEMPLATES_DIR / "languages" / language_key
    if not lang_dir.exists():
        print(f"[ERROR] No hay templates para language key: {language_key}", file=sys.stderr)
        sys.exit(1)
    lang_files: dict[Path, Path] = {}
    for root, _dirs, filenames in os.walk(lang_dir):
        for fname in filenames:
            src = Path(root) / fname
            rel = src.relative_to(lang_dir)
            lang_files[rel] = (src, rel)
    files_with_lang: dict[Path, tuple[Path, Path]] = {}
    for src, rel in files:
        files_with_lang[rel] = (src, rel)
    for rel, pair in lang_files.items():
        files_with_lang[rel] = pair
    files = list(files_with_lang.values())

    if framework:
        fw_dir = TEMPLATES_DIR / "frameworks" / framework
        if fw_dir.exists():
            fw_files: dict[Path, tuple[Path, Path]] = {}
            for root, _dirs, filenames in os.walk(fw_dir):
                for fname in filenames:
                    src = Path(root) / fname
                    rel = src.relative_to(fw_dir)
                    fw_files[rel] = (src, rel)
            current: dict[Path, tuple[Path, Path]] = {rel: (s, r) for s, r in files}
            for rel, pair in fw_files.items():
                current[rel] = pair
            files = list(current.values())

    return files


def build_variables(
    language_key: str,
    framework: str | None,
    angular_test_runner_cmd: str | None,
    registry: dict[str, Any],
) -> dict[str, str]:
    lang_data = registry["languages"][language_key]
    variables: dict[str, str] = {}
    for key, value in lang_data.items():
        variables[key.upper()] = str(value)
    variables["LANG"] = lang_data["lang"]
    variables["RUNTIME"] = lang_data["runtime"]
    variables["LANGUAGE_KEY"] = language_key
    variables["PROJECT_NAME"] = Path(os.getcwd()).resolve().name
    variables["TEST_RUNNER"] = lang_data["test_runner"]
    variables["INIT_CMD"] = lang_data.get("init_cmd", lang_data["test_runner"])

    if framework:
        fw_data = registry["frameworks"][framework]
        if framework == "angular" and angular_test_runner_cmd:
            variables["TEST_RUNNER"] = angular_test_runner_cmd
            variables["ANGULAR_TEST_RUNNER"] = angular_test_runner_cmd
        elif framework == "angular":
            variables["ANGULAR_TEST_RUNNER"] = lang_data["test_runner"]
        else:
            if "test_cmd" in fw_data:
                variables["TEST_RUNNER"] = fw_data["test_cmd"]

        for key in ("build_cmd", "dev_cmd", "lint_cmd"):
            if key in fw_data:
                variables[key.upper()] = fw_data[key]

    return variables


def render_content(content: str, variables: dict[str, str]) -> str:
    def replace_var(match: re.Match[str]) -> str:
        var_name = match.group(1)
        return variables.get(var_name, match.group(0))

    return re.sub(r"\{\{(\w+)\}\}", replace_var, content)


def render_file(src: Path, variables: dict[str, str]) -> str:
    try:
        content = src.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ""
    return render_content(content, variables)


def preview_changes(
    files: list[tuple[Path, Path]],
    target_dir: Path,
    force: bool,
) -> tuple[list[str], list[str]]:
    to_create: list[str] = []
    to_overwrite: list[str] = []
    for _src, rel in files:
        dest = target_dir / rel
        rel_str = str(rel)
        if dest.exists():
            if force:
                to_overwrite.append(rel_str)
            else:
                pass
        else:
            to_create.append(rel_str)
    return to_create, to_overwrite


def write_files(
    files: list[tuple[Path, Path]],
    variables: dict[str, str],
    target_dir: Path,
    force: bool,
    dry_run: bool,
) -> list[str]:
    written: list[str] = []
    for src, rel in files:
        dest = target_dir / rel
        if dest.exists() and not force:
            continue
        rendered = render_file(src, variables)
        if dry_run:
            written.append(str(rel))
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(rendered, encoding="utf-8")
        if src.name == "init.sh":
            dest.chmod(dest.stat().st_mode | 0o755)
        written.append(str(rel))
    return written


def write_manifest(target_dir: Path, written_files: list[str]) -> None:
    manifest_path = target_dir / MANIFEST_FILE
    manifest = {
        "version": "1.0",
        "files": written_files,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")


def rollback(target_dir: Path) -> None:
    manifest_path = target_dir / MANIFEST_FILE
    if not manifest_path.exists():
        return
    with open(manifest_path, encoding="utf-8") as f:
        manifest = json.load(f)
    for rel in reversed(manifest.get("files", [])):
        p = target_dir / rel
        if p.exists() and p.is_file():
            p.unlink()
            parent = p.parent
            while parent != target_dir and parent.exists() and not any(parent.iterdir()):
                parent.rmdir()
                parent = parent.parent
    manifest_path.unlink()


def run_init(target_dir: Path) -> bool:
    init_sh = target_dir / "init.sh"
    if not init_sh.exists():
        print("[WARN] init.sh no encontrado, saltando ejecución.", file=sys.stderr)
        return True
    result = subprocess.run(
        [str(init_sh)],
        cwd=str(target_dir),
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        return False
    return True


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Instala el arnés de agentes en el directorio actual.",
    )
    parser.add_argument(
        "--language",
        choices=["python", "javascript", "typescript", "php", "nextjs"],
        default=None,
        help="Lenguaje del proyecto (auto-detect si no se pasa)",
    )
    parser.add_argument(
        "--runtime",
        choices=["node", "bun"],
        default=None,
        help="Runtime para JS/TS/Next.js (default: node)",
    )
    parser.add_argument(
        "--framework",
        choices=["react", "angular", "vue"],
        default=None,
        help="Framework overlay (no aplica a nextjs)",
    )
    parser.add_argument(
        "--angular-test-runner",
        choices=["ng-test", "jest"],
        default=None,
        help="Test runner para Angular (default según runtime)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Preview sin escribir archivos",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Sobrescribir archivos existentes",
    )
    parser.add_argument(
        "--target-dir",
        default=".",
        help="Directorio destino (default: directorio actual)",
    )

    args = parser.parse_args()
    target_dir = Path(args.target_dir).resolve()
    registry = load_registry()

    lang = args.language
    runtime = args.runtime
    framework = args.framework

    if lang is None:
        det_lang, det_runtime, det_framework = detect_language(target_dir)
        if det_lang is None:
            print("[ERROR] No se pudo detectar el lenguaje. Usa --language.", file=sys.stderr)
            sys.exit(1)
        lang = det_lang
        if runtime is None and det_runtime:
            runtime = det_runtime
        if framework is None and det_framework:
            framework = det_framework
        print(f"[INFO] Detectado: language={lang}, runtime={runtime or 'N/A'}, framework={framework or 'N/A'}")

    if lang in LANG_ALIASES:
        lang = LANG_ALIASES[lang]

    if runtime is None and lang in LANG_RUNTIME_MAP:
        runtime = LANG_RUNTIME_MAP[lang]

    error = validate_framework(lang, framework, registry)
    if error:
        print(f"[ERROR] {error}", file=sys.stderr)
        sys.exit(1)

    language_key = resolve_language_key(lang, runtime)
    if language_key not in registry["languages"]:
        print(f"[ERROR] Combinación no soportada: {language_key}", file=sys.stderr)
        print(f"  Válidas: {', '.join(registry['languages'].keys())}", file=sys.stderr)
        sys.exit(1)

    angular_test_runner_cmd = resolve_angular_test_runner(framework, args.angular_test_runner, runtime, registry)

    files = collect_template_files(language_key, framework)
    variables = build_variables(language_key, framework, angular_test_runner_cmd, registry)

    to_create, to_overwrite = preview_changes(files, target_dir, args.force)

    print("\n── Preview ──────────────────────────────────────────")
    if to_create:
        print(f"\n  Se crearán {len(to_create)} archivos:")
        for f in to_create[:20]:
            print(f"    + {f}")
        if len(to_create) > 20:
            print(f"    ... y {len(to_create) - 20} más")
    if to_overwrite:
        print(f"\n  Se sobrescribirán {len(to_overwrite)} archivos:")
        for f in to_overwrite[:20]:
            print(f"    ~ {f}")
        if len(to_overwrite) > 20:
            print(f"    ... y {len(to_overwrite) - 20} más")

    existing_no_force = len(files) - len(to_create) - len(to_overwrite)
    if existing_no_force > 0 and not args.force:
        print(f"\n  {existing_no_force} archivos ya existen (usa --force para sobrescribir)")

    print(f"\n  Configuración:")
    print(f"    language_key   = {language_key}")
    print(f"    framework      = {framework or 'N/A'}")
    print(f"    test_runner    = {variables.get('TEST_RUNNER', 'N/A')}")
    print(f"    init_cmd       = {variables.get('INIT_CMD', 'N/A')}")

    if args.dry_run:
        print("\n[dry-run] No se escribieron archivos.")
        return

    try:
        response = input("\n¿Continuar? [y/N] ")
    except EOFError:
        response = "n"
    if response.lower() not in ("y", "yes", "s", "si", "sí"):
        print("Cancelado.")
        return

    written = write_files(files, variables, target_dir, args.force, dry_run=False)
    write_manifest(target_dir, written)
    print(f"\n[OK] {len(written)} archivos escritos.")

    print("\n── Ejecutando init.sh ────────────────────────────────")
    if run_init(target_dir):
        print("[OK] init.sh pasó. Arnés instalado correctamente.")
    else:
        print("[FAIL] init.sh falló. Haciendo rollback...", file=sys.stderr)
        rollback(target_dir)
        sys.exit(1)


if __name__ == "__main__":
    main()
