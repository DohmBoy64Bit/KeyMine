import tempfile
import unittest
from pathlib import Path

from keymine.keyfile import delete_keyfile, keyfile_path


class KeyfileTests(unittest.TestCase):
    def test_keyfile_path_is_fixed_under_data_directory(self) -> None:
        install_dir = Path("C:/Mine-imator 2.0.2")
        self.assertEqual(
            keyfile_path(install_dir),
            install_dir / "Data" / "key.midata",
        )

    def test_delete_keyfile_removes_only_expected_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            install_dir = Path(temp_dir)
            data_dir = install_dir / "Data"
            data_dir.mkdir()
            keyfile = data_dir / "key.midata"
            unrelated = data_dir / "keep.midata"
            keyfile.write_text("key", encoding="utf-8")
            unrelated.write_text("keep", encoding="utf-8")

            self.assertTrue(delete_keyfile(install_dir))
            self.assertFalse(keyfile.exists())
            self.assertTrue(unrelated.exists())

    def test_delete_keyfile_returns_false_when_keyfile_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            self.assertFalse(delete_keyfile(Path(temp_dir)))


if __name__ == "__main__":
    unittest.main()
