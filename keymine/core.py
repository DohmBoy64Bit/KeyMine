from __future__ import annotations

import secrets

CHARSET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
KEY_LENGTH = 8
PREFIX_LENGTH = KEY_LENGTH // 2


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
