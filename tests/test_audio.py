import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from keymine import audio


class AudioTests(unittest.TestCase):
    def test_music_asset_is_packaged(self) -> None:
        self.assertEqual(audio.MUSIC_PATH.name, "MinefieldMelody.wav")
        self.assertTrue(audio.MUSIC_PATH.is_file())

    def test_play_loop_uses_windows_async_loop_flags(self) -> None:
        play_sound = Mock()
        fake_winsound = SimpleNamespace(
            PlaySound=play_sound,
            SND_FILENAME=1,
            SND_ASYNC=2,
            SND_LOOP=4,
        )
        path = Path("C:/KeyMine/tune/MinefieldMelody.wav")

        with (
            patch.object(sys, "platform", "win32"),
            patch.dict(sys.modules, {"winsound": fake_winsound}),
        ):
            self.assertTrue(audio.play_loop(path))

        play_sound.assert_called_once_with(str(path), 1 | 2 | 4)

    def test_stop_stops_windows_playback(self) -> None:
        play_sound = Mock()
        fake_winsound = SimpleNamespace(PlaySound=play_sound)

        with (
            patch.object(sys, "platform", "win32"),
            patch.dict(sys.modules, {"winsound": fake_winsound}),
        ):
            audio.stop()

        play_sound.assert_called_once_with(None, 0)


if __name__ == "__main__":
    unittest.main()
