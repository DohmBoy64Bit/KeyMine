import unittest

from keymine.core import (
    CHARSET,
    KEY_LENGTH,
    PREFIX_LENGTH,
    generate_key,
    generate_random_key,
    key_valid,
    mapping_lines,
    mirror_character,
)


class CoreKeyTests(unittest.TestCase):
    def test_known_custom_prefix_generates_expected_key(self) -> None:
        self.assertEqual(generate_key("DOHM"), "DOHMX2V6")
        self.assertEqual(generate_key("abcd"), "ABCD6789")

    def test_generated_keys_pass_validation(self) -> None:
        for _ in range(20):
            key = generate_random_key()
            self.assertEqual(len(key), KEY_LENGTH)
            self.assertTrue(key_valid(key))

    def test_invalid_keys_are_rejected(self) -> None:
        self.assertFalse(key_valid("ABCD1234"))
        self.assertFalse(key_valid("TOO-SHORT"))
        self.assertFalse(key_valid("ABCD67!9"))

    def test_invalid_prefixes_raise_value_error(self) -> None:
        with self.assertRaises(ValueError):
            generate_key("ABC")
        with self.assertRaises(ValueError):
            generate_key("AB!D")

    def test_character_mapping_matches_original_rule(self) -> None:
        self.assertEqual(CHARSET, "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
        self.assertEqual(PREFIX_LENGTH, 4)
        self.assertEqual(mirror_character("A"), "9")
        self.assertEqual(mirror_character("M"), "X")
        self.assertEqual(mirror_character("0"), "J")
        self.assertEqual(len(mapping_lines()), len(CHARSET) // 2)


if __name__ == "__main__":
    unittest.main()
