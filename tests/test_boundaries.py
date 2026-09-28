import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ModuleBoundaryTests(unittest.TestCase):
    def test_cli_does_not_import_ui(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "-c",
                "import sys; import keymine.cli; print('keymine.ui' in sys.modules)",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "False")

    def test_entry_point_does_not_import_ui_until_gui_is_needed(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "-c",
                "import sys; import keygen; print('keymine.ui' in sys.modules)",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "False")


if __name__ == "__main__":
    unittest.main()
