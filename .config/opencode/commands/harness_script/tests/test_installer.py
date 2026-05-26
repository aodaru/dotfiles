"""Tests para el installer: detección, validación, renderizado, escritura."""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path

from install import (
    MANIFEST_FILE,
    REGISTRY_PATH,
    TEMPLATES_DIR,
    build_variables,
    collect_template_files,
    detect_language,
    load_registry,
    render_content,
    resolve_angular_test_runner,
    resolve_language_key,
    rollback,
    validate_framework,
    write_files,
    write_manifest,
)


class TestLoadRegistry(unittest.TestCase):
    def test_registry_loads(self):
        registry = load_registry()
        self.assertIn("languages", registry)
        self.assertIn("frameworks", registry)

    def test_all_language_keys_present(self):
        registry = load_registry()
        expected = [
            "python",
            "javascript-node",
            "javascript-bun",
            "typescript-node",
            "typescript-bun",
            "php",
            "nextjs-node",
            "nextjs-bun",
        ]
        for key in expected:
            self.assertIn(key, registry["languages"], f"Missing language key: {key}")

    def test_all_framework_keys_present(self):
        registry = load_registry()
        for key in ("react", "angular", "vue"):
            self.assertIn(key, registry["frameworks"])

    def test_language_has_required_fields(self):
        registry = load_registry()
        required = [
            "lang", "runtime", "runtime_check", "test_runner",
            "test_framework", "file_ext", "style_guide",
            "dep_file", "dep_install", "dev_cmd", "build_cmd", "lint_cmd",
        ]
        for lang_key, lang_data in registry["languages"].items():
            for field in required:
                self.assertIn(field, lang_data, f"{lang_key} missing field: {field}")


class TestDetectLanguage(unittest.TestCase):
    def test_detect_python_requirements(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "requirements.txt").write_text("flask\n")
            lang, runtime, fw = detect_language(Path(d))
            self.assertEqual(lang, "python")
            self.assertIsNone(runtime)
            self.assertIsNone(fw)

    def test_detect_python_pyproject(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "pyproject.toml").write_text("[project]\n")
            lang, runtime, fw = detect_language(Path(d))
            self.assertEqual(lang, "python")

    def test_detect_javascript(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "package.json").write_text("{}")
            lang, runtime, fw = detect_language(Path(d))
            self.assertEqual(lang, "javascript")
            self.assertEqual(runtime, "node")

    def test_detect_typescript(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "package.json").write_text("{}")
            (Path(d) / "tsconfig.json").write_text("{}")
            lang, runtime, fw = detect_language(Path(d))
            self.assertEqual(lang, "typescript")

    def test_detect_nextjs(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "next.config.js").write_text("module.exports = {}")
            lang, runtime, fw = detect_language(Path(d))
            self.assertEqual(lang, "nextjs")
            self.assertIsNone(fw)

    def test_detect_angular(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "angular.json").write_text("{}")
            lang, runtime, fw = detect_language(Path(d))
            self.assertEqual(lang, "typescript")
            self.assertEqual(fw, "angular")

    def test_detect_php(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "composer.json").write_text("{}")
            lang, runtime, fw = detect_language(Path(d))
            self.assertEqual(lang, "php")

    def test_detect_nothing(self):
        with tempfile.TemporaryDirectory() as d:
            lang, runtime, fw = detect_language(Path(d))
            self.assertIsNone(lang)


class TestResolveLanguageKey(unittest.TestCase):
    def test_python(self):
        self.assertEqual(resolve_language_key("python", None), "python")

    def test_php(self):
        self.assertEqual(resolve_language_key("php", None), "php")

    def test_javascript_node(self):
        self.assertEqual(resolve_language_key("javascript", "node"), "javascript-node")

    def test_javascript_bun(self):
        self.assertEqual(resolve_language_key("javascript", "bun"), "javascript-bun")

    def test_typescript_default_node(self):
        self.assertEqual(resolve_language_key("typescript", None), "typescript-node")


class TestValidateFramework(unittest.TestCase):
    def setUp(self):
        self.registry = load_registry()

    def test_no_framework_ok(self):
        self.assertIsNone(validate_framework("python", None, self.registry))

    def test_nextjs_rejects_framework(self):
        err = validate_framework("nextjs", "react", self.registry)
        self.assertIsNotNone(err)
        self.assertIn("fullstack", err)

    def test_unknown_framework(self):
        err = validate_framework("typescript", "svelte", self.registry)
        self.assertIsNotNone(err)
        self.assertIn("desconocido", err)

    def test_incompatible_framework(self):
        err = validate_framework("python", "react", self.registry)
        self.assertIsNotNone(err)
        self.assertIn("no es compatible", err)

    def test_compatible_framework(self):
        self.assertIsNone(validate_framework("typescript", "angular", self.registry))
        self.assertIsNone(validate_framework("javascript", "react", self.registry))


class TestResolveAngularTestRunner(unittest.TestCase):
    def setUp(self):
        self.registry = load_registry()

    def test_non_angular_returns_none(self):
        self.assertIsNone(resolve_angular_test_runner("react", None, "node", self.registry))

    def test_angular_jest(self):
        result = resolve_angular_test_runner("angular", "jest", "node", self.registry)
        self.assertIn("jest", result)

    def test_angular_ng_test(self):
        result = resolve_angular_test_runner("angular", "ng-test", "bun", self.registry)
        self.assertIn("ng test", result)

    def test_angular_default_node(self):
        result = resolve_angular_test_runner("angular", None, "node", self.registry)
        self.assertIn("jest", result)

    def test_angular_default_bun(self):
        result = resolve_angular_test_runner("angular", None, "bun", self.registry)
        self.assertNotIn("jest", result)


class TestBuildVariables(unittest.TestCase):
    def setUp(self):
        self.registry = load_registry()

    def test_python_variables(self):
        variables = build_variables("python", None, None, self.registry)
        self.assertEqual(variables["LANG"], "python")
        self.assertEqual(variables["RUNTIME"], "python3")
        self.assertIn("unittest", variables["TEST_RUNNER"])

    def test_angular_overrides_test_runner(self):
        test_cmd = "ng test --watch=false --builder @angular-builders/jest"
        variables = build_variables("typescript-node", "angular", test_cmd, self.registry)
        self.assertEqual(variables["TEST_RUNNER"], test_cmd)
        self.assertEqual(variables["ANGULAR_TEST_RUNNER"], test_cmd)

    def test_project_name_is_cwd_basename(self):
        variables = build_variables("python", None, None, self.registry)
        self.assertTrue(len(variables["PROJECT_NAME"]) > 0)


class TestRenderContent(unittest.TestCase):
    def test_simple_replacement(self):
        result = render_content("Hello {{NAME}}!", {"NAME": "World"})
        self.assertEqual(result, "Hello World!")

    def test_multiple_replacements(self):
        result = render_content("{{A}} and {{B}}", {"A": "1", "B": "2"})
        self.assertEqual(result, "1 and 2")

    def test_unknown_variable_preserved(self):
        result = render_content("{{UNKNOWN}}", {})
        self.assertEqual(result, "{{UNKNOWN}}")

    def test_no_variables(self):
        result = render_content("plain text", {"A": "1"})
        self.assertEqual(result, "plain text")


class TestCollectTemplateFiles(unittest.TestCase):
    def test_python_includes_core_and_language(self):
        files = collect_template_files("python", None)
        rel_paths = [str(rel) for _src, rel in files]
        self.assertTrue(any("AGENTS.md" in p for p in rel_paths))
        self.assertTrue(any("init.sh" in p for p in rel_paths))
        self.assertTrue(any("docs" in p for p in rel_paths))

    def test_react_overlay_overrides(self):
        files_no_fw = collect_template_files("typescript-node", None)
        files_fw = collect_template_files("typescript-node", "react")
        rel_no_fw = {str(rel) for _src, rel in files_no_fw}
        rel_fw = {str(rel) for _src, rel in files_fw}
        self.assertTrue(len(files_fw) > 0)
        self.assertTrue(any("architecture.md" in p for p in rel_fw))

    def test_invalid_language_key_exits(self):
        with self.assertRaises(SystemExit):
            collect_template_files("nonexistent-lang", None)


class TestWriteAndRollback(unittest.TestCase):
    def test_write_creates_files(self):
        registry = load_registry()
        files = collect_template_files("python", None)
        variables = build_variables("python", None, None, registry)
        with tempfile.TemporaryDirectory() as d:
            written = write_files(files, variables, Path(d), force=False, dry_run=False)
            self.assertTrue(len(written) > 0)
            for rel in written:
                self.assertTrue((Path(d) / rel).exists(), f"Missing: {rel}")

    def test_dry_run_does_not_write(self):
        registry = load_registry()
        files = collect_template_files("python", None)
        variables = build_variables("python", None, None, registry)
        with tempfile.TemporaryDirectory() as d:
            written = write_files(files, variables, Path(d), force=False, dry_run=True)
            self.assertTrue(len(written) > 0)
            for rel in written:
                self.assertFalse((Path(d) / rel).exists())

    def test_manifest_written(self):
        with tempfile.TemporaryDirectory() as d:
            write_manifest(Path(d), ["AGENTS.md", "init.sh"])
            manifest_path = Path(d) / MANIFEST_FILE
            self.assertTrue(manifest_path.exists())
            data = json.loads(manifest_path.read_text())
            self.assertEqual(data["files"], ["AGENTS.md", "init.sh"])

    def test_rollback_removes_files(self):
        with tempfile.TemporaryDirectory() as d:
            target = Path(d)
            (target / "AGENTS.md").write_text("test")
            write_manifest(target, ["AGENTS.md"])
            rollback(target)
            self.assertFalse((target / "AGENTS.md").exists())
            self.assertFalse((target / MANIFEST_FILE).exists())

    def test_init_sh_is_executable(self):
        registry = load_registry()
        files = collect_template_files("python", None)
        variables = build_variables("python", None, None, registry)
        with tempfile.TemporaryDirectory() as d:
            write_files(files, variables, Path(d), force=False, dry_run=False)
            init_sh = Path(d) / "init.sh"
            if init_sh.exists():
                self.assertTrue(os.access(init_sh, os.X_OK))


if __name__ == "__main__":
    unittest.main()
