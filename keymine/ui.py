from __future__ import annotations

import sys
import tkinter as tk
from tkinter import messagebox

from .core import (
    CHARSET,
    PREFIX_LENGTH,
    generate_key,
    generate_random_key,
    key_valid,
    mapping_lines,
    mirror_character,
)


class RetroKeygenApp:
    """Compact Tkinter UI modeled after early-2000s scene utilities."""

    BG = "#030303"
    PANEL = "#111315"
    PANEL_2 = "#090909"
    BORDER = "#d6d6d6"
    TEXT = "#eeeeee"
    MUTED = "#7f9aa8"
    NEON = "#c8f3ff"
    CYAN = "#9fc7db"
    MAGENTA = "#a8c5d3"
    WARNING = "#ffcc66"
    BAD = "#ff6b7a"
    CONTROL = "#b9b9b9"
    CONTROL_DARK = "#5e5e5e"

    _LOGO_GLYPHS = {
        "K": (
            "10001",
            "10010",
            "10100",
            "11000",
            "10100",
            "10010",
            "10001",
        ),
        "E": (
            "11111",
            "10000",
            "10000",
            "11110",
            "10000",
            "10000",
            "11111",
        ),
        "Y": (
            "10001",
            "01010",
            "00100",
            "00100",
            "00100",
            "00100",
            "00100",
        ),
        "M": (
            "10001",
            "11011",
            "10101",
            "10101",
            "10001",
            "10001",
            "10001",
        ),
        "I": (
            "11111",
            "00100",
            "00100",
            "00100",
            "00100",
            "00100",
            "11111",
        ),
        "N": (
            "10001",
            "11001",
            "11001",
            "10101",
            "10011",
            "10011",
            "10001",
        ),
    }

    _LOGO_ROWS = (
        "#607987",
        "#8da8b6",
        "#dbefff",
        "#f6fdff",
        "#c8f3ff",
        "#8da8b6",
        "#4b6471",
    )

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("KEYMINE // SERIAL UTILITY")
        self.root.geometry("520x390")
        self.root.resizable(False, False)
        self.root.configure(bg=self.BG)

        self.prefix_var = tk.StringVar(value="DOHM")
        self.key_var = tk.StringVar(value=generate_key("DOHM"))
        self.validate_var = tk.StringVar(value=generate_key("DOHM"))
        self.status_var = tk.StringVar(value="READY // CUSTOM PREFIX LOADED")

        self._build_ui()
        self._bind_events()
        self._refresh_custom_preview()

    def _build_ui(self) -> None:
        outer = tk.Frame(self.root, bg=self.BG, padx=8, pady=6)
        outer.pack(fill="both", expand=True)

        self._build_header(outer)
        self._rule(outer).pack(fill="x", pady=(3, 7))
        self._build_generator_panel(outer)
        self._rule(outer).pack(fill="x", pady=(7, 6))
        self._build_validator_panel(outer)
        self._build_footer(outer)

    def _build_header(self, parent: tk.Widget) -> None:
        canvas = tk.Canvas(
            parent,
            width=500,
            height=92,
            bg=self.BG,
            highlightthickness=0,
            bd=0,
        )
        canvas.pack(fill="x")

        canvas.create_text(
            5,
            6,
            text="DOHM PRESENTS",
            anchor="nw",
            fill=self.MUTED,
            font=("Courier New", 8, "bold"),
        )
        canvas.create_text(
            495,
            6,
            text="KEY GENERATOR / VALIDATOR",
            anchor="ne",
            fill=self.MUTED,
            font=("Courier New", 8),
        )

        self._draw_pixel_logo(canvas, "KEYMINE", center_x=250, top=24)

        canvas.create_line(4, 82, 496, 82, fill="#363636")
        canvas.create_line(4, 83, 496, 83, fill=self.BORDER)
        canvas.create_line(4, 84, 496, 84, fill="#607987")

    def _draw_pixel_logo(
        self,
        canvas: tk.Canvas,
        text: str,
        *,
        center_x: int,
        top: int,
    ) -> None:
        pixel = 6
        letter_width = 5 * pixel
        letter_gap = 7
        width = len(text) * letter_width + (len(text) - 1) * letter_gap
        left = center_x - width // 2

        for letter_index, letter in enumerate(text):
            glyph = self._LOGO_GLYPHS[letter]
            letter_left = left + letter_index * (letter_width + letter_gap)

            for row_index, row in enumerate(glyph):
                fill = self._LOGO_ROWS[row_index]
                for column_index, enabled in enumerate(row):
                    if enabled != "1":
                        continue

                    x1 = letter_left + column_index * pixel
                    y1 = top + row_index * pixel
                    canvas.create_rectangle(
                        x1 + 1,
                        y1 + 1,
                        x1 + pixel,
                        y1 + pixel,
                        fill="#25323a",
                        outline="",
                    )
                    canvas.create_rectangle(
                        x1,
                        y1,
                        x1 + pixel - 2,
                        y1 + pixel - 2,
                        fill=fill,
                        outline="",
                    )

    def _build_generator_panel(self, parent: tk.Widget) -> None:
        panel = tk.Frame(parent, bg=self.BG)
        panel.pack(fill="x")

        tk.Label(
            panel,
            text="[ GENERATOR ]",
            bg=self.BG,
            fg=self.CYAN,
            font=("Courier New", 9, "bold"),
        ).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 4))

        tk.Label(
            panel,
            text="CUSTOM PREFIX",
            bg=self.BG,
            fg=self.TEXT,
            font=("Tahoma", 8, "bold"),
        ).grid(row=1, column=0, sticky="w")

        tk.Label(
            panel,
            text="4 CHARS // A-Z 0-9",
            bg=self.BG,
            fg=self.MUTED,
            font=("Courier New", 8),
        ).grid(row=1, column=1, columnspan=3, sticky="e")

        self.prefix_entry = tk.Entry(
            panel,
            textvariable=self.prefix_var,
            width=9,
            justify="center",
            bg=self.PANEL_2,
            fg=self.NEON,
            insertbackground=self.NEON,
            selectbackground="#607987",
            selectforeground="#ffffff",
            relief="sunken",
            bd=2,
            highlightthickness=0,
            font=("Courier New", 11, "bold"),
        )
        self.prefix_entry.grid(row=2, column=0, sticky="ew", padx=(0, 6), pady=(2, 0))

        self._button(panel, "GENERATE CUSTOM", self.generate_custom).grid(
            row=2,
            column=1,
            sticky="ew",
            padx=(0, 5),
            pady=(2, 0),
        )
        self._button(panel, "RANDOM", self.generate_random).grid(
            row=2,
            column=2,
            sticky="ew",
            padx=(0, 5),
            pady=(2, 0),
        )
        self._button(panel, "MAPPING", self.show_mapping).grid(
            row=2,
            column=3,
            sticky="ew",
            pady=(2, 0),
        )

        tk.Label(
            panel,
            text="GENERATED KEY",
            bg=self.BG,
            fg=self.TEXT,
            font=("Tahoma", 8, "bold"),
        ).grid(row=3, column=0, columnspan=4, sticky="w", pady=(9, 2))

        key_frame = tk.Frame(
            panel,
            bg="#050505",
            relief="sunken",
            bd=2,
            padx=5,
            pady=2,
        )
        key_frame.grid(row=4, column=0, columnspan=3, sticky="nsew", padx=(0, 5))

        self.key_label = tk.Label(
            key_frame,
            textvariable=self.key_var,
            bg="#050505",
            fg=self.NEON,
            anchor="center",
            font=("Courier New", 16, "bold"),
        )
        self.key_label.pack(fill="x")

        self._button(panel, "COPY", self.copy_key).grid(
            row=4,
            column=3,
            sticky="nsew",
        )

        self.preview_label = tk.Label(
            panel,
            text="",
            bg=self.BG,
            fg=self.MUTED,
            anchor="w",
            justify="left",
            font=("Courier New", 8),
        )
        self.preview_label.grid(
            row=5,
            column=0,
            columnspan=4,
            sticky="ew",
            pady=(5, 0),
        )

        panel.grid_columnconfigure(0, weight=1, minsize=100)
        panel.grid_columnconfigure(1, weight=2, minsize=148)
        panel.grid_columnconfigure(2, weight=1, minsize=88)
        panel.grid_columnconfigure(3, weight=1, minsize=88)

    def _build_validator_panel(self, parent: tk.Widget) -> None:
        panel = tk.Frame(parent, bg=self.BG)
        panel.pack(fill="x")

        tk.Label(
            panel,
            text="[ VALIDATOR ]",
            bg=self.BG,
            fg=self.CYAN,
            font=("Courier New", 9, "bold"),
        ).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 4))

        self.validate_entry = tk.Entry(
            panel,
            textvariable=self.validate_var,
            bg=self.PANEL_2,
            fg=self.TEXT,
            insertbackground=self.NEON,
            selectbackground="#607987",
            selectforeground="#ffffff",
            relief="sunken",
            bd=2,
            highlightthickness=0,
            justify="center",
            font=("Courier New", 10, "bold"),
        )
        self.validate_entry.grid(row=1, column=0, sticky="ew", padx=(0, 5))

        self._button(panel, "CHECK KEY", self.validate_key).grid(
            row=1,
            column=1,
            sticky="ew",
            padx=(0, 5),
        )

        self.validation_result = tk.Label(
            panel,
            text="VALID",
            bg=self.PANEL_2,
            fg=self.NEON,
            relief="sunken",
            bd=2,
            padx=8,
            pady=3,
            font=("Courier New", 9, "bold"),
        )
        self.validation_result.grid(row=1, column=2, sticky="nsew")

        panel.grid_columnconfigure(0, weight=3)
        panel.grid_columnconfigure(1, weight=1, minsize=100)
        panel.grid_columnconfigure(2, weight=1, minsize=84)

    def _build_footer(self, parent: tk.Widget) -> None:
        footer = tk.Frame(parent, bg=self.BG)
        footer.pack(fill="x", side="bottom", pady=(7, 0))

        self._rule(footer).pack(fill="x", pady=(0, 4))

        tk.Label(
            footer,
            textvariable=self.status_var,
            bg=self.BG,
            fg=self.MUTED,
            anchor="w",
            font=("Courier New", 8),
        ).pack(side="left", fill="x", expand=True)

        tk.Label(
            footer,
            text="MIRROR-36",
            bg=self.BG,
            fg=self.CYAN,
            font=("Courier New", 8, "bold"),
        ).pack(side="right")

    def _rule(self, parent: tk.Widget) -> tk.Frame:
        return tk.Frame(parent, bg="#363636", height=2, bd=0)

    def _button(self, parent: tk.Widget, text: str, command) -> tk.Button:
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=self.CONTROL,
            fg="#101010",
            activebackground="#e2e2e2",
            activeforeground="#000000",
            disabledforeground=self.CONTROL_DARK,
            relief="raised",
            bd=2,
            highlightthickness=0,
            padx=5,
            pady=2,
            takefocus=True,
            font=("Tahoma", 8, "bold"),
        )

    def _bind_events(self) -> None:
        self.prefix_var.trace_add("write", lambda *_: self._on_prefix_changed())
        self.prefix_entry.bind("<Return>", lambda _event: self.generate_custom())
        self.validate_entry.bind("<Return>", lambda _event: self.validate_key())
        self.root.bind("<Control-c>", lambda _event: self.copy_key())

    def _on_prefix_changed(self) -> None:
        cleaned = "".join(
            character
            for character in self.prefix_var.get().upper()
            if character in CHARSET
        )[:PREFIX_LENGTH]

        if cleaned != self.prefix_var.get():
            self.prefix_var.set(cleaned)
            return

        self._refresh_custom_preview()

    def _refresh_custom_preview(self) -> None:
        prefix = self.prefix_var.get().upper()

        if len(prefix) != PREFIX_LENGTH:
            self.preview_label.config(
                text=(
                    f"SUFFIX PATH: WAITING // {PREFIX_LENGTH - len(prefix)} "
                    "CHAR(S) REMAINING"
                )
            )
            return

        pairs = [
            f"{character}->{mirror_character(character)}"
            for character in reversed(prefix)
        ]
        self.preview_label.config(
            text=f"SUFFIX PATH: {'  '.join(pairs)}  //  RESULT: {generate_key(prefix)}"
        )

    def generate_custom(self) -> None:
        try:
            key = generate_key(self.prefix_var.get())
        except ValueError as exc:
            self.status_var.set(f"ERROR // {exc}")
            messagebox.showerror("Invalid prefix", str(exc), parent=self.root)
            return

        self.key_var.set(key)
        self.validate_var.set(key)
        self.validation_result.config(text="VALID", fg=self.NEON)
        self.status_var.set(
            f"CUSTOM KEY GENERATED // {self.prefix_var.get().upper()} -> {key}"
        )

    def generate_random(self) -> None:
        key = generate_random_key()
        self.prefix_var.set(key[:PREFIX_LENGTH])
        self.key_var.set(key)
        self.validate_var.set(key)
        self.validation_result.config(text="VALID", fg=self.NEON)
        self.status_var.set(f"RANDOM KEY GENERATED // {key}")

    def validate_key(self) -> None:
        key = self.validate_var.get().strip().upper()
        self.validate_var.set(key)
        valid = key_valid(key)

        if valid:
            self.validation_result.config(text="VALID", fg=self.NEON)
            self.status_var.set(f"VALIDATOR // {key} PASSED")
            return

        self.validation_result.config(text="NOT VALID", fg=self.BAD)
        self.status_var.set(f"VALIDATOR // {key or '<EMPTY>'} FAILED")

    def copy_key(self) -> None:
        key = self.key_var.get().strip()
        if not key:
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(key)
        self.root.update_idletasks()
        self.status_var.set(f"COPIED TO CLIPBOARD // {key}")

    def show_mapping(self) -> None:
        window = tk.Toplevel(self.root)
        window.title("KEYMINE // MIRROR TABLE")
        window.geometry("340x390")
        window.resizable(False, False)
        window.configure(bg=self.BG)
        window.transient(self.root)

        outer = tk.Frame(window, bg=self.BG, padx=8, pady=7)
        outer.pack(fill="both", expand=True)

        tk.Label(
            outer,
            text="[ MIRROR TABLE ]",
            bg=self.BG,
            fg=self.CYAN,
            font=("Courier New", 10, "bold"),
        ).pack(anchor="w")

        tk.Label(
            outer,
            text="OPPOSITE POSITIONS // 1-BASED PAIRS TOTAL 37",
            bg=self.BG,
            fg=self.MUTED,
            justify="left",
            font=("Courier New", 8),
        ).pack(anchor="w", pady=(2, 5))

        self._rule(outer).pack(fill="x", pady=(0, 6))

        text = tk.Text(
            outer,
            bg=self.PANEL_2,
            fg=self.NEON,
            insertbackground=self.NEON,
            selectbackground="#607987",
            selectforeground="#ffffff",
            relief="sunken",
            bd=2,
            padx=8,
            pady=6,
            font=("Courier New", 9, "bold"),
        )
        text.pack(fill="both", expand=True)
        text.insert("1.0", "\n".join(mapping_lines()))
        text.config(state="disabled")


def launch_gui() -> int:
    try:
        root = tk.Tk()
    except tk.TclError as exc:
        print(f"Unable to start the graphical interface: {exc}", file=sys.stderr)
        return 2

    RetroKeygenApp(root)
    root.mainloop()
    return 0
