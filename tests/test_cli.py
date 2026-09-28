import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
KEYGEN = ROOT / "keygen.py"


class CliTests(unittest.TestCase):
    def run_keygen(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(KEYGEN), *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_prefix_mode_keeps_existing_output(self) -> None:
        result = self.run_keygen("--prefix", "DOHM")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "DOHMX2V6")
        self.assertEqual(result.stderr, "")

    def test_validate_mode_keeps_existing_exit_codes(self) -> None:
        valid = self.run_keygen("--validate", "DOHMX2V6")
        invalid = self.run_keygen("--validate", "ABCD1234")

        self.assertEqual(valid.returncode, 0)
        self.assertEqual(valid.stdout.strip(), "VALID")
        self.assertEqual(invalid.returncode, 1)
        self.assertEqual(invalid.stdout.strip(), "INVALID")

    def test_count_mode_generates_requested_number_of_valid_keys(self) -> None:
        from keymine.core import key_valid

        result = self.run_keygen("--count", "5")
        keys = result.stdout.splitlines()

        self.assertEqual(result.returncode, 0)
        self.assertEqual(len(keys), 5)
        self.assertTrue(all(key_valid(key) for key in keys))

    def test_mapping_mode_keeps_existing_heading(self) -> None:
        result = self.run_keygen("--show-mapping")
        self.assertEqual(result.returncode, 0)
        self.assertTrue(result.stdout.startswith("Character mapping:\n\n"))
        self.assertIn("A  <->  9", result.stdout)

    def test_delete_keyfile_mode_deletes_expected_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            install_dir = Path(temp_dir)
            data_dir = install_dir / "Data"
            data_dir.mkdir()
            keyfile = data_dir / "key.midata"
            keyfile.write_text("key", encoding="utf-8")

            result = self.run_keygen("--delete-keyfile", str(install_dir))

            self.assertEqual(result.returncode, 0)
            self.assertIn(f"KEYFILE: {keyfile}", result.stdout)
            self.assertTrue(result.stdout.rstrip().endswith("DELETED"))
            self.assertFalse(keyfile.exists())

    def test_delete_keyfile_mode_reports_missing_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            install_dir = Path(temp_dir)
            expected = install_dir / "Data" / "key.midata"

            result = self.run_keygen("--delete-keyfile", str(install_dir))

            self.assertEqual(result.returncode, 1)
            self.assertIn(f"KEYFILE: {expected}", result.stdout)
            self.assertTrue(result.stdout.rstrip().endswith("NOT FOUND"))


if __name__ == "__main__":
    unittest.main()
