import tkinter as tk
import unittest
from unittest.mock import patch

from keymine.ui import KeyMineApp


class KeyMineUiTests(unittest.TestCase):
    def setUp(self) -> None:
        try:
            self.root = tk.Tk()
        except tk.TclError as exc:
            self.skipTest(f"Tk display unavailable: {exc}")

        self.play_patch = patch("keymine.ui.audio.play_loop", return_value=True)
        self.stop_patch = patch("keymine.ui.audio.stop")
        self.mock_play = self.play_patch.start()
        self.mock_stop = self.stop_patch.start()
        self.app = KeyMineApp(self.root)
        self.root.update_idletasks()

    def tearDown(self) -> None:
        root = getattr(self, "root", None)
        if root is not None:
            root.destroy()
        self.stop_patch.stop()
        self.play_patch.stop()

    def test_scene_panel_palette_matches_research_direction(self) -> None:
        self.assertEqual(KeyMineApp.BG, "#030303")
        self.assertEqual(KeyMineApp.PANEL, "#111315")
        self.assertEqual(KeyMineApp.TEXT, "#eeeeee")
        self.assertEqual(KeyMineApp.MUTED, "#7f9aa8")
        self.assertEqual(KeyMineApp.NEON, "#c8f3ff")
        self.assertEqual(KeyMineApp.CYAN, "#9fc7db")
        self.assertEqual(KeyMineApp.BORDER, "#d6d6d6")
        self.assertEqual(KeyMineApp.CONTROL, "#b9b9b9")

    def test_main_window_is_fixed_and_compact(self) -> None:
        self.assertEqual(self.root.geometry().split("+")[0], "520x410")
        self.assertEqual(self.root.resizable(), (False, False))

    def test_content_is_not_clipped(self) -> None:
        required = sum(
            child.winfo_reqheight() for child in self.root.winfo_children()
        )
        height = int(self.root.geometry().split("x")[1].split("+")[0])
        self.assertLessEqual(required, height)

    def test_custom_title_bar_replaces_native_chrome(self) -> None:
        self.assertTrue(self.root.overrideredirect())
        label_texts = {
            widget.cget("text")
            for widget in self._walk_widgets(self.root)
            if isinstance(widget, tk.Label)
        }
        self.assertIn("KEYMINE // SERIAL UTILITY", label_texts)

    def test_required_original_controls_remain_available(self) -> None:
        button_texts = {
            widget.cget("text")
            for widget in self._walk_widgets(self.root)
            if isinstance(widget, tk.Button)
        }

        self.assertSetEqual(
            button_texts,
            {
                "GENERATE CUSTOM",
                "RANDOM",
                "MAPPING",
                "COPY",
                "CHECK KEY",
                "X",
            },
        )
        self.assertEqual(self.app.prefix_var.get(), "DOHM")
        self.assertEqual(self.app.key_var.get(), "DOHMX2V6")
        self.assertEqual(self.app.validate_var.get(), "DOHMX2V6")
        self.assertTrue(self.app.preview_label.cget("text").startswith("SUFFIX PATH:"))
        self.assertEqual(self.app.validation_result.cget("text"), "VALID")

    def test_ui_actions_keep_existing_behavior(self) -> None:
        self.app.prefix_var.set("ABCD")
        self.app.generate_custom()
        self.assertEqual(self.app.key_var.get(), "ABCD6789")

        self.app.validate_var.set("ABCD1234")
        self.app.validate_key()
        self.assertEqual(self.app.validation_result.cget("text"), "NOT VALID")


    def test_random_copy_and_mapping_features_remain_working(self) -> None:
        from keymine.core import key_valid

        self.app.generate_random()
        generated = self.app.key_var.get()
        self.assertTrue(key_valid(generated))
        self.assertEqual(self.app.validate_var.get(), generated)

        self.app.copy_key()
        self.assertEqual(self.root.clipboard_get(), generated)

        existing = set(self.root.winfo_children())
        self.app.show_mapping()
        created = [
            widget
            for widget in self.root.winfo_children()
            if widget not in existing and isinstance(widget, tk.Toplevel)
        ]
        self.assertEqual(len(created), 1)

        text_widgets = [
            widget
            for widget in self._walk_widgets(created[0])
            if isinstance(widget, tk.Text)
        ]
        self.assertEqual(len(text_widgets), 1)
        self.assertIn("A  <->  9", text_widgets[0].get("1.0", "end-1c"))
        created[0].destroy()

    def test_lowercase_typing_refreshes_suffix_preview(self) -> None:
        self.app.prefix_var.set("")
        self.assertIn("4 CHAR(S) REMAINING", self.app.preview_label.cget("text"))

        self.app.prefix_entry.insert("end", "d")
        self.assertEqual(self.app.prefix_var.get(), "D")
        self.assertIn("3 CHAR(S) REMAINING", self.app.preview_label.cget("text"))

        self.app.prefix_entry.insert("end", "ohm")
        self.assertEqual(self.app.prefix_var.get(), "DOHM")
        self.assertTrue(self.app.preview_label.cget("text").startswith("SUFFIX PATH: M->X"))

    def test_mapping_window_is_not_styled_as_child_window(self) -> None:
        import sys

        if sys.platform != "win32":
            self.skipTest("Win32 window-style check")

        import ctypes

        user32 = ctypes.windll.user32
        self.app.show_mapping()
        self.root.update()

        windows = [
            widget
            for widget in self.root.winfo_children()
            if isinstance(widget, tk.Toplevel)
        ]
        self.assertEqual(len(windows), 1)

        hwnd = user32.GetParent(windows[0].winfo_id()) or windows[0].winfo_id()
        style = user32.GetWindowLongW(hwnd, -16) & 0xFFFFFFFF
        self.assertEqual(
            style & 0x40000000,
            0,
            "mapping dialog HWND must be WS_POPUP, not WS_CHILD",
        )
        windows[0].destroy()

    def test_mapping_window_opens_at_fixed_position(self) -> None:
        self.app.show_mapping()
        self.root.update()

        windows = [
            widget
            for widget in self.root.winfo_children()
            if isinstance(widget, tk.Toplevel)
        ]
        self.assertEqual(len(windows), 1)
        self.assertEqual(windows[0].geometry(), "340x390+1227+315")
        windows[0].destroy()

    def test_mapping_window_opens_only_once(self) -> None:
        self.app.show_mapping()
        self.app.show_mapping()
        self.app.show_mapping()
        self.root.update()

        windows = [
            widget
            for widget in self.root.winfo_children()
            if isinstance(widget, tk.Toplevel)
        ]
        self.assertEqual(len(windows), 1)
        windows[0].destroy()

    def test_music_starts_on_launch_and_toggle_stops_and_restarts_it(self) -> None:
        self.mock_play.assert_called_once()
        self.assertTrue(self.app.music_on)

        self.app.toggle_music()
        self.mock_stop.assert_called_once()
        self.assertFalse(self.app.music_on)
        self.assertEqual(self.app.status_var.get(), "MUSIC // OFF")

        self.app.toggle_music()
        self.assertEqual(self.mock_play.call_count, 2)
        self.assertTrue(self.app.music_on)
        self.assertEqual(self.app.status_var.get(), "MUSIC // ON")

    def test_keyboard_shortcuts_replace_music_and_nfo_buttons(self) -> None:
        for sequence in ("<Control-Shift-M>", "<Control-Shift-P>", "<Control-Shift-N>"):
            self.assertTrue(
                self.root.bind(sequence),
                f"missing keyboard binding for {sequence}",
            )

        self.assertTrue(self.app.music_on)
        self.app.toggle_music()
        self.assertFalse(self.app.music_on)
        self.assertEqual(self.app.status_var.get(), "MUSIC // OFF")

        self.app.toggle_music()
        self.assertTrue(self.app.music_on)
        self.assertEqual(self.app.status_var.get(), "MUSIC // ON")

        self.app.show_nfo()
        self.app.show_nfo()
        self.root.update()
        windows = [
            widget
            for widget in self.root.winfo_children()
            if isinstance(widget, tk.Toplevel)
        ]
        self.assertEqual(len(windows), 1)
        for widget in windows:
            widget.destroy()

    def test_nfo_viewer_displays_packaged_nfo_and_opens_only_once(self) -> None:
        existing = set(self.root.winfo_children())
        self.app.show_nfo()
        self.app.show_nfo()
        self.root.update()

        created = [
            widget
            for widget in self.root.winfo_children()
            if widget not in existing and isinstance(widget, tk.Toplevel)
        ]
        self.assertEqual(len(created), 1)

        text_widgets = [
            widget
            for widget in self._walk_widgets(created[0])
            if isinstance(widget, tk.Text)
        ]
        self.assertEqual(len(text_widgets), 1)
        content = text_widgets[0].get("1.0", "end-1c")
        self.assertIn("D O H M   P R E S E N T S", content)
        self.assertIn("Minefield Melody", content)
        created[0].destroy()

    def test_close_stops_music_before_destroying_root(self) -> None:
        with patch.object(self.root, "destroy") as destroy:
            self.app.close()

        self.mock_stop.assert_called_once()
        destroy.assert_called_once()

    def test_mapping_window_follows_main_window_position(self) -> None:
        self.root.geometry("+200+100")
        self.root.update()

        self.app.show_mapping()
        self.root.update()

        windows = [
            widget
            for widget in self.root.winfo_children()
            if isinstance(widget, tk.Toplevel)
        ]
        self.assertEqual(len(windows), 1)
        self.assertEqual(windows[0].geometry(), "340x390+727+80")
        windows[0].destroy()

    def test_nfo_window_shares_mapping_anchor(self) -> None:
        self.root.geometry("+200+100")
        self.root.update()

        self.app.show_nfo()
        self.root.update()

        windows = [
            widget
            for widget in self.root.winfo_children()
            if isinstance(widget, tk.Toplevel)
        ]
        self.assertEqual(len(windows), 1)
        self.assertEqual(windows[0].geometry(), "650x520+727+80")
        windows[0].destroy()

    def _walk_widgets(self, parent: tk.Misc):
        for child in parent.winfo_children():
            yield child
            yield from self._walk_widgets(child)


if __name__ == "__main__":
    unittest.main()
