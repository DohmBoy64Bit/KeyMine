#!/usr/bin/env python3
"""Retro desktop key generator for the supplied GameMaker key_valid() algorithm.

The validator uses this character set:
    ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789

A valid key is exactly 8 characters. The last four characters are determined by
mirroring the first four against the character set and reversing their order.
For example:
    ABCD -> ABCD6789
    DOHM -> DOHMX2V6

Run with no arguments to open the GUI.

CLI examples:
    python keygen.py --prefix DOHM
    python keygen.py --validate DOHMX2V6
    python keygen.py --count 10
    python keygen.py --show-mapping
"""

from __future__ import annotations

import argparse
import secrets
import sys
import tkinter as tk
from tkinter import messagebox

CHARSET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
KEY_LENGTH = 8
PREFIX_LENGTH = KEY_LENGTH // 2


# ---------------------------------------------------------------------------
# Key algorithm
# ---------------------------------------------------------------------------


def mirror_character(character: str) -> str:
    """Return the character paired with *character* by the original validator."""
    character = character.upper()

    if len(character) != 1 or character not in CHARSET:
        raise ValueError(
            f"Invalid character {character!r}. Allowed characters are A-Z and 0-9."
        )

    index = CHARSET.index(character)
    return CHARSET[-1 - index]


def generate_key(prefix: str) -> str:
    """Generate a valid 8-character key from a 4-character prefix."""
    prefix = prefix.upper()

    if len(prefix) != PREFIX_LENGTH:
        raise ValueError(f"Prefix must be exactly {PREFIX_LENGTH} characters long.")

    invalid = [character for character in prefix if character not in CHARSET]
    if invalid:
        raise ValueError(
            "Prefix may contain only A-Z and 0-9. "
            f"Invalid character(s): {', '.join(repr(c) for c in invalid)}"
        )

    suffix = "".join(mirror_character(character) for character in reversed(prefix))
    return prefix + suffix


def generate_random_key() -> str:
    """Generate one random valid key."""
    prefix = "".join(secrets.choice(CHARSET) for _ in range(PREFIX_LENGTH))
    return generate_key(prefix)


def key_valid(key: str) -> bool:
    """Replicate the supplied GameMaker key_valid() function."""
    key = key.upper()

    if len(key) != KEY_LENGTH:
        return False

    if any(character not in CHARSET for character in key):
        return False

    for left_index in range(PREFIX_LENGTH):
        right_index = KEY_LENGTH - 1 - left_index
        if mirror_character(key[left_index]) != key[right_index]:
            return False

    return True


def mapping_lines() -> list[str]:
    """Return the unique mirror pairs used by the validator."""
    seen: set[str] = set()
    lines: list[str] = []

    for character in CHARSET:
        partner = mirror_character(character)
        pair_key = "".join(sorted((character, partner)))
        if pair_key in seen:
            continue
        seen.add(pair_key)
        lines.append(f"{character}  <->  {partner}")

    return lines


# ---------------------------------------------------------------------------
# Retro GUI
# ---------------------------------------------------------------------------


class RetroKeygenApp:
    """Tkinter UI inspired by classic release-group keygen aesthetics."""

    BG = "#08090d"
    PANEL = "#10141b"
    PANEL_2 = "#141a22"
    BORDER = "#2c3848"
    TEXT = "#d8e6f3"
    MUTED = "#7d8da3"
    NEON = "#55ff9a"
    CYAN = "#4bdfff"
    MAGENTA = "#ff55d5"
    WARNING = "#ffcc66"
    BAD = "#ff6b7a"

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("DOHM // Retro Key Generator")
        self.root.geometry("720x560")
        self.root.minsize(680, 520)
        self.root.configure(bg=self.BG)

        self.prefix_var = tk.StringVar(value="DOHM")
        self.key_var = tk.StringVar(value=generate_key("DOHM"))
        self.validate_var = tk.StringVar(value=generate_key("DOHM"))
        self.status_var = tk.StringVar(value="READY // CUSTOM PREFIX LOADED")

        self._build_ui()
        self._bind_events()
        self._refresh_custom_preview()

    def _build_ui(self) -> None:
        outer = tk.Frame(self.root, bg=self.BG, padx=18, pady=16)
        outer.pack(fill="both", expand=True)

        self._build_header(outer)
        self._build_generator_panel(outer)
        self._build_validator_panel(outer)
        self._build_footer(outer)

    def _build_header(self, parent: tk.Widget) -> None:
        header = tk.Frame(
            parent,
            bg=self.PANEL,
            highlightbackground=self.CYAN,
            highlightthickness=1,
            padx=16,
            pady=12,
        )
        header.pack(fill="x", pady=(0, 12))

        tk.Label(
            header,
            text="D O H M   K E Y G E N",
            bg=self.PANEL,
            fg=self.NEON,
            font=("Consolas", 22, "bold"),
        ).pack(anchor="w")

        tk.Label(
            header,
            text="[ 36-CHAR MIRROR ENGINE // 8-CHAR SERIAL FORMAT // PYTHON EDITION ]",
            bg=self.PANEL,
            fg=self.CYAN,
            font=("Consolas", 9),
        ).pack(anchor="w", pady=(3, 0))

        tk.Label(
            header,
            text="Classic keygen-inspired interface. No external packages required.",
            bg=self.PANEL,
            fg=self.MUTED,
            font=("Consolas", 9),
        ).pack(anchor="w", pady=(8, 0))

    def _build_generator_panel(self, parent: tk.Widget) -> None:
        panel = tk.Frame(
            parent,
            bg=self.PANEL,
            highlightbackground=self.BORDER,
            highlightthickness=1,
            padx=16,
            pady=14,
        )
        panel.pack(fill="x", pady=(0, 12))

        tk.Label(
            panel,
            text="[ GENERATOR ]",
            bg=self.PANEL,
            fg=self.MAGENTA,
            font=("Consolas", 11, "bold"),
        ).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 10))

        tk.Label(
            panel,
            text="CUSTOM PREFIX",
            bg=self.PANEL,
            fg=self.TEXT,
            font=("Consolas", 10, "bold"),
        ).grid(row=1, column=0, sticky="w")

        tk.Label(
            panel,
            text="Exactly 4 characters (A-Z / 0-9)",
            bg=self.PANEL,
            fg=self.MUTED,
            font=("Consolas", 8),
        ).grid(row=2, column=0, sticky="w", pady=(2, 8))

        self.prefix_entry = tk.Entry(
            panel,
            textvariable=self.prefix_var,
            width=12,
            justify="center",
            bg=self.BG,
            fg=self.NEON,
            insertbackground=self.NEON,
            selectbackground=self.CYAN,
            selectforeground=self.BG,
            relief="flat",
            font=("Consolas", 18, "bold"),
        )
        self.prefix_entry.grid(row=3, column=0, sticky="ew", padx=(0, 10))

        self._button(
            panel,
            "GENERATE CUSTOM",
            self.generate_custom,
            fg=self.BG,
            bg=self.NEON,
        ).grid(row=3, column=1, sticky="ew", padx=(0, 8))

        self._button(
            panel,
            "RANDOM",
            self.generate_random,
            fg=self.BG,
            bg=self.CYAN,
        ).grid(row=3, column=2, sticky="ew", padx=(0, 8))

        self._button(
            panel,
            "MAPPING",
            self.show_mapping,
            fg=self.TEXT,
            bg=self.PANEL_2,
        ).grid(row=3, column=3, sticky="ew")

        tk.Label(
            panel,
            text="GENERATED KEY",
            bg=self.PANEL,
            fg=self.TEXT,
            font=("Consolas", 10, "bold"),
        ).grid(row=4, column=0, columnspan=4, sticky="w", pady=(14, 5))

        key_frame = tk.Frame(panel, bg=self.BG, padx=10, pady=9)
        key_frame.grid(row=5, column=0, columnspan=3, sticky="ew", padx=(0, 8))

        self.key_label = tk.Label(
            key_frame,
            textvariable=self.key_var,
            bg=self.BG,
            fg=self.NEON,
            font=("Consolas", 24, "bold"),
        )
        self.key_label.pack(fill="x")

        self._button(
            panel,
            "COPY",
            self.copy_key,
            fg=self.BG,
            bg=self.MAGENTA,
        ).grid(row=5, column=3, sticky="nsew")

        self.preview_label = tk.Label(
            panel,
            text="",
            bg=self.PANEL,
            fg=self.MUTED,
            justify="left",
            font=("Consolas", 9),
        )
        self.preview_label.grid(row=6, column=0, columnspan=4, sticky="w", pady=(8, 0))

        panel.grid_columnconfigure(0, weight=1)
        panel.grid_columnconfigure(1, weight=1)
        panel.grid_columnconfigure(2, weight=1)
        panel.grid_columnconfigure(3, weight=1)

    def _build_validator_panel(self, parent: tk.Widget) -> None:
        panel = tk.Frame(
            parent,
            bg=self.PANEL,
            highlightbackground=self.BORDER,
            highlightthickness=1,
            padx=16,
            pady=14,
        )
        panel.pack(fill="x", pady=(0, 12))

        tk.Label(
            panel,
            text="[ VALIDATOR ]",
            bg=self.PANEL,
            fg=self.MAGENTA,
            font=("Consolas", 11, "bold"),
        ).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 10))

        self.validate_entry = tk.Entry(
            panel,
            textvariable=self.validate_var,
            bg=self.BG,
            fg=self.TEXT,
            insertbackground=self.NEON,
            selectbackground=self.CYAN,
            selectforeground=self.BG,
            relief="flat",
            justify="center",
            font=("Consolas", 15, "bold"),
        )
        self.validate_entry.grid(row=1, column=0, sticky="ew", padx=(0, 8))

        self._button(
            panel,
            "CHECK KEY",
            self.validate_key,
            fg=self.BG,
            bg=self.CYAN,
        ).grid(row=1, column=1, sticky="ew", padx=(0, 8))

        self.validation_result = tk.Label(
            panel,
            text="VALID",
            bg=self.PANEL_2,
            fg=self.NEON,
            padx=14,
            pady=8,
            font=("Consolas", 11, "bold"),
        )
        self.validation_result.grid(row=1, column=2, sticky="ew")

        panel.grid_columnconfigure(0, weight=2)
        panel.grid_columnconfigure(1, weight=1)
        panel.grid_columnconfigure(2, weight=1)

    def _build_footer(self, parent: tk.Widget) -> None:
        footer = tk.Frame(parent, bg=self.BG)
        footer.pack(fill="x", side="bottom")

        tk.Label(
            footer,
            textvariable=self.status_var,
            bg=self.BG,
            fg=self.MUTED,
            anchor="w",
            font=("Consolas", 9),
        ).pack(side="left", fill="x", expand=True)

        tk.Label(
            footer,
            text="PREFIX + MIRRORED(REVERSED PREFIX)",
            bg=self.BG,
            fg=self.MUTED,
            font=("Consolas", 8),
        ).pack(side="right")

    def _button(
        self,
        parent: tk.Widget,
        text: str,
        command,
        *,
        fg: str,
        bg: str,
    ) -> tk.Button:
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=fg,
            activebackground=self.TEXT,
            activeforeground=self.BG,
            relief="flat",
            bd=0,
            padx=10,
            pady=8,
            cursor="hand2",
            font=("Consolas", 9, "bold"),
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
                text=f"ENTER {PREFIX_LENGTH} CHARACTERS // {PREFIX_LENGTH - len(prefix)} REMAINING"
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
        self.status_var.set(f"CUSTOM KEY GENERATED // {self.prefix_var.get().upper()} -> {key}")

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
        else:
            self.validation_result.config(text="INVALID", fg=self.BAD)
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
        window.title("Character Mapping")
        window.geometry("360x520")
        window.configure(bg=self.BG)
        window.transient(self.root)

        tk.Label(
            window,
            text="[ MIRROR TABLE ]",
            bg=self.BG,
            fg=self.MAGENTA,
            font=("Consolas", 14, "bold"),
        ).pack(anchor="w", padx=14, pady=(14, 8))

        tk.Label(
            window,
            text="Each pair occupies opposite positions in the 36-character set.\n"
            "Their 1-based positions always add up to 37.",
            bg=self.BG,
            fg=self.MUTED,
            justify="left",
            font=("Consolas", 9),
        ).pack(anchor="w", padx=14, pady=(0, 10))

        text = tk.Text(
            window,
            bg=self.PANEL,
            fg=self.NEON,
            insertbackground=self.NEON,
            relief="flat",
            padx=14,
            pady=12,
            font=("Consolas", 11, "bold"),
        )
        text.pack(fill="both", expand=True, padx=14, pady=(0, 14))
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


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def print_mapping() -> None:
    print("Character mapping:")
    print()
    for line in mapping_lines():
        print(f"  {line}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Retro GUI and CLI key generator for the supplied GameMaker key algorithm. "
            "Run without arguments to open the GUI."
        )
    )

    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--prefix",
        metavar="TEXT",
        help="generate a key from an exact 4-character A-Z/0-9 prefix",
    )
    mode.add_argument(
        "--validate",
        metavar="KEY",
        help="check whether an 8-character key passes the original validator",
    )
    mode.add_argument(
        "--show-mapping",
        action="store_true",
        help="display the complete mirror-character mapping",
    )
    mode.add_argument(
        "--count",
        type=int,
        metavar="N",
        help="generate N random keys in the terminal instead of launching the GUI",
    )

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.prefix is not None:
            print(generate_key(args.prefix))
            return 0

        if args.validate is not None:
            valid = key_valid(args.validate)
            print("VALID" if valid else "INVALID")
            return 0 if valid else 1

        if args.show_mapping:
            print_mapping()
            return 0

        if args.count is not None:
            if args.count < 1:
                parser.error("--count must be at least 1")

            for _ in range(args.count):
                print(generate_random_key())
            return 0

        return launch_gui()

    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
