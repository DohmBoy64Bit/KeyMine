from __future__ import annotations

import sys
from pathlib import Path


MUSIC_PATH = Path(__file__).resolve().parents[1] / "tune" / "MinefieldMelody.wav"


def play_loop(path: str | Path = MUSIC_PATH) -> bool:
    if sys.platform != "win32":
        return False

    import winsound

    try:
        winsound.PlaySound(
            str(path),
            winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP,
        )
    except RuntimeError:
        return False

    return True


def stop() -> None:
    if sys.platform != "win32":
        return

    import winsound

    winsound.PlaySound(None, 0)
