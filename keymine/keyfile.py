from __future__ import annotations

from pathlib import Path


KEYFILE_RELATIVE_PATH = Path("Data") / "key.midata"


def keyfile_path(install_dir: str | Path) -> Path:
    return Path(install_dir).expanduser() / KEYFILE_RELATIVE_PATH


def delete_keyfile(install_dir: str | Path) -> bool:
    path = keyfile_path(install_dir)
    if not path.is_file():
        return False

    path.unlink()
    return True
