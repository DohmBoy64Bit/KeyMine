import tkinter as tk
import unittest

from keymine.ui import RetroKeygenApp


class RetroUiTests(unittest.TestCase):
    def setUp(self) -> None:
        try:
            self.root = tk.Tk()
        except tk.TclError as exc:
            self.skipTest(f"Tk display unavailable: {exc}")

        self.app = RetroKeygenApp(self.root)
        self.root.update_idletasks()

    def tearDown(self) -> None:
        root = getattr(self, "root", None)
        if root is not None:
            root.destroy()

    def test_scene_panel_palette_matches_research_direction(self) -> None:
        self.assertEqual(RetroKeygenApp.BG, "#030303")
        self.assertEqual(RetroKeygenApp.PANEL, "#111315")
        self.assertEqual(RetroKeygenApp.TEXT, "#eeeeee")
        self.assertEqual(RetroKeygenApp.MUTED, "#7f9aa8")
        self.assertEqual(RetroKeygenApp.NEON, "#c8f3ff")
        self.assertEqual(RetroKeygenApp.CYAN, "#9fc7db")
        self.assertEqual(RetroKeygenApp.BORDER, "#d6d6d6")
        self.assertEqual(RetroKeygenApp.CONTROL, "#b9b9b9")

    def test_main_window_is_fixed_and_compact(self) -> None:
        self.assertEqual(self.root.geometry().split("+")[0], "520x390")
        self.assertEqual(self.root.resizable(), (False, False))

    def test_required_original_controls_remain_available(self) -> None:
        button_texts = {
            widget.cget("text")
            for widget in self._walk_widgets(self.root)
            if isinstance(widget, tk.Button)
        }

        self.assertSetEqual(
            button_texts,
            {"GENERATE CUSTOM", "RANDOM", "MAPPING", "COPY", "CHECK KEY"},
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

    def _walk_widgets(self, parent: tk.Misc):
        for child in parent.winfo_children():
            yield child
            yield from self._walk_widgets(child)


if __name__ == "__main__":
    unittest.main()
