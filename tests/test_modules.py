"""Verify independent module installs and release completeness."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

from test_scripts import module, ROOT

installer = module("module_installer", ROOT / "scripts/install.py")
packager = module("module_packager", ROOT / "scripts/package.py")


class ModuleTests(unittest.TestCase):
    def test_every_module_installs_repeats_and_protects_existing_edits(self):
        with tempfile.TemporaryDirectory() as temporary:
            for name, source in installer.skill_sources().items():
                with self.subTest(skill=name):
                    target = Path(temporary).resolve() / name
                    self.assertEqual(installer.install(target, skill=name)[0], "installed")
                    self.assertEqual(installer.inventory(target), installer.inventory(source))
                    self.assertEqual(installer.install(target, skill=name)[0], "already-installed")
                    (target / "SKILL.md").write_text("custom user edit")
                    with self.assertRaises(ValueError):
                        installer.install(target, skill=name)
                    self.assertEqual((target / "SKILL.md").read_text(), "custom user edit")

    def test_cli_selects_requested_module_without_installing_core(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary).resolve() / "council"
            result = subprocess.run([sys.executable, str(ROOT / "scripts/install.py"),
                                     "--skill", "exobrain-council", "--dest", str(target)],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((target / "references/roster.json").is_file())
            self.assertFalse((target / "scripts/init_brain.py").exists())

    def test_release_archives_contain_all_resources_and_exact_bytes(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary).resolve() / "release"
            report = packager.package(output)
            catalog = json.loads((ROOT / "catalog.json").read_text())
            self.assertEqual(len(report["archives"]), len(catalog["skills"]) + 1)
            for entry in catalog["skills"]:
                archive = output / f"{entry['name']}-skill-v{entry['version']}.zip"
                with zipfile.ZipFile(archive) as bundle:
                    self.assertIsNone(bundle.testzip())
                    for relative, digest in installer.inventory(ROOT / entry["path"]).items():
                        self.assertEqual(hashlib.sha256(bundle.read(f"{entry['name']}/{relative}")).hexdigest(), digest)
                    self.assertEqual(bundle.read(f"{entry['name']}/LICENSE"), (ROOT / "LICENSE").read_bytes())
                    self.assertFalse(any(".git/" in name or "__pycache__" in name for name in bundle.namelist()))
            full = output / f"exobrain-skill-v{catalog['version']}.zip"
            with zipfile.ZipFile(full) as bundle:
                self.assertIsNone(bundle.testzip())
                self.assertEqual(bundle.read("exobrain-skill/catalog.json"), (ROOT / "catalog.json").read_bytes())
            with self.assertRaises(ValueError):
                packager.package(output)


if __name__ == "__main__":
    unittest.main()
