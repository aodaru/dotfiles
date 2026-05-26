"""Tests para la integridad de los templates."""

from __future__ import annotations

import json
import os
import unittest
from pathlib import Path

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
REGISTRY_PATH = Path(__file__).resolve().parent.parent / "registry.json"


class TestCoreTemplatesExist(unittest.TestCase):
    def test_agents_md(self):
        self.assertTrue((TEMPLATES_DIR / "core" / "AGENTS.md").exists())

    def test_claude_md(self):
        self.assertTrue((TEMPLATES_DIR / "core" / "CLAUDE.md").exists())

    def test_checkpoints_md(self):
        self.assertTrue((TEMPLATES_DIR / "core" / "CHECKPOINTS.md").exists())

    def test_progress_current(self):
        self.assertTrue((TEMPLATES_DIR / "core" / "progress" / "current.md").exists())

    def test_progress_history(self):
        self.assertTrue((TEMPLATES_DIR / "core" / "progress" / "history.md").exists())

    def test_claude_settings(self):
        self.assertTrue((TEMPLATES_DIR / "core" / ".claude" / "settings.json").exists())

    def test_leader_agent(self):
        self.assertTrue((TEMPLATES_DIR / "core" / ".claude" / "agents" / "leader.md").exists())

    def test_implementer_agent(self):
        self.assertTrue((TEMPLATES_DIR / "core" / ".claude" / "agents" / "implementer.md").exists())

    def test_reviewer_agent(self):
        self.assertTrue((TEMPLATES_DIR / "core" / ".claude" / "agents" / "reviewer.md").exists())


class TestLanguageTemplatesExist(unittest.TestCase):
    LANGUAGES = [
        "python",
        "javascript-node",
        "javascript-bun",
        "typescript-node",
        "typescript-bun",
        "php",
        "nextjs-node",
        "nextjs-bun",
    ]

    REQUIRED_FILES = [
        "init.sh",
        "README.md",
        ".gitignore",
        "docs/architecture.md",
        "docs/conventions.md",
        "docs/verification.md",
    ]

    def test_all_languages_have_required_files(self):
        for lang in self.LANGUAGES:
            lang_dir = TEMPLATES_DIR / "languages" / lang
            self.assertTrue(lang_dir.exists(), f"Missing language dir: {lang}")
            for fname in self.REQUIRED_FILES:
                fpath = lang_dir / fname
                self.assertTrue(fpath.exists(), f"Missing {fname} in {lang}")


class TestFrameworkTemplatesExist(unittest.TestCase):
    FRAMEWORKS = ["react", "angular", "vue"]

    REQUIRED_FILES = [
        "docs/architecture.md",
        "docs/conventions.md",
        "docs/verification.md",
        "feature_list.json",
    ]

    def test_all_frameworks_have_required_files(self):
        for fw in self.FRAMEWORKS:
            fw_dir = TEMPLATES_DIR / "frameworks" / fw
            self.assertTrue(fw_dir.exists(), f"Missing framework dir: {fw}")
            for fname in self.REQUIRED_FILES:
                fpath = fw_dir / fname
                self.assertTrue(fpath.exists(), f"Missing {fname} in {fw}")


class TestRegistryConsistency(unittest.TestCase):
    def setUp(self):
        with open(REGISTRY_PATH, encoding="utf-8") as f:
            self.registry = json.load(f)

    def test_every_language_has_template_dir(self):
        for lang_key in self.registry["languages"]:
            lang_dir = TEMPLATES_DIR / "languages" / lang_key
            self.assertTrue(lang_dir.exists(), f"Missing template dir for: {lang_key}")

    def test_every_framework_has_template_dir(self):
        for fw_key in self.registry["frameworks"]:
            fw_dir = TEMPLATES_DIR / "frameworks" / fw_key
            self.assertTrue(fw_dir.exists(), f"Missing template dir for: {fw_key}")

    def test_compatible_languages_reference_valid_keys(self):
        lang_keys = set(self.registry["languages"].keys())
        for fw_key, fw_data in self.registry["frameworks"].items():
            for compat in fw_data.get("compatible_languages", []):
                self.assertIn(compat, lang_keys, f"{fw_key} references invalid language: {compat}")

    def test_angular_has_special_test_runner_fields(self):
        angular = self.registry["frameworks"]["angular"]
        self.assertIn("test_cmd_ng", angular)
        self.assertIn("test_cmd_jest", angular)
        self.assertIn("test_runner_default_node", angular)
        self.assertIn("test_runner_default_bun", angular)


class TestTemplatesUseVariables(unittest.TestCase):
    def test_checkpoints_uses_test_runner(self):
        content = (TEMPLATES_DIR / "core" / "CHECKPOINTS.md").read_text()
        self.assertIn("{{TEST_RUNNER}}", content)

    def test_settings_uses_test_runner(self):
        content = (TEMPLATES_DIR / "core" / ".claude" / "settings.json").read_text()
        self.assertIn("{{TEST_RUNNER}}", content)

    def test_settings_uses_init_cmd(self):
        content = (TEMPLATES_DIR / "core" / ".claude" / "settings.json").read_text()
        self.assertIn("{{INIT_CMD}}", content)

    def test_readme_uses_project_name(self):
        for lang_dir in (TEMPLATES_DIR / "languages").iterdir():
            if lang_dir.is_dir():
                readme = lang_dir / "README.md"
                if readme.exists():
                    content = readme.read_text()
                    self.assertIn("{{PROJECT_NAME}}", content, f"README in {lang_dir.name} missing {{PROJECT_NAME}}")

    def test_gitignore_uses_extra(self):
        for lang_dir in (TEMPLATES_DIR / "languages").iterdir():
            if lang_dir.is_dir():
                gitignore = lang_dir / ".gitignore"
                if gitignore.exists():
                    content = gitignore.read_text()
                    self.assertIn("{{GITIGNORE_EXTRA}}", content, f".gitignore in {lang_dir.name} missing {{GITIGNORE_EXTRA}}")

    def test_angular_verification_uses_test_runner(self):
        content = (TEMPLATES_DIR / "frameworks" / "angular" / "docs" / "verification.md").read_text()
        self.assertIn("{{TEST_RUNNER}}", content)

    def test_angular_conventions_uses_angular_test_runner(self):
        content = (TEMPLATES_DIR / "frameworks" / "angular" / "docs" / "conventions.md").read_text()
        self.assertIn("{{ANGULAR_TEST_RUNNER}}", content)


if __name__ == "__main__":
    unittest.main()
