# Key Generator and Validator Guide

## Overview

This document explains, from the beginning, how the supplied GameMaker key-validation function works and how the accompanying Python key generator reproduces that logic.

The original validator is:

```gml
/// key_valid(key)
/// @arg key

function key_valid(key)
{
    var keystr;
    key = string_upper(key)
    keystr = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    if (string_length(key) != 8)
        return false

    for (var c = 0; c < 8; c += 2)
    {
        var pos1, pos2;
        pos1 = string_pos(string_char_at(key, c + 1), keystr)
        pos2 = string_pos(string_char_at(key, 8 - c), keystr)
        if (pos1 = 0 || pos2 = 0)
            return false
        if (pos1 != string_length(keystr) + 1 - pos2)
            return false
    }

    return true
}
```

At first glance, the loop may look complicated. In practice, the rule is simple:

> A valid key contains exactly eight characters. The first four characters can be chosen freely from `A-Z` and `0-9`. The final four characters are determined automatically by mirroring the first four through a fixed 36-character alphabet and placing those mirrored characters in reverse order.

For example:

```text
ABCD -> ABCD6789
```

`ABCD6789` passes the original validator.

---

## 1. The Allowed Character Set

The validator defines this string:

```text
ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789
```

It contains 36 characters:

- 26 uppercase letters, `A` through `Z`
- 10 digits, `0` through `9`

No spaces, punctuation, hyphens, symbols, or other characters are valid.

The original function first converts the supplied key to uppercase:

```gml
key = string_upper(key)
```

This means lowercase letters are accepted but are treated as uppercase.

For example:

```text
abcd6789
ABCD6789
AbCd6789
```

are all evaluated as:

```text
ABCD6789
```

---

## 2. The Key Must Be Exactly Eight Characters Long

The validator performs this check:

```gml
if (string_length(key) != 8)
    return false
```

Therefore:

```text
ABCD6789   -> correct length
ABC6789    -> too short
ABCDE6789  -> too long
```

A key cannot pass unless its length is exactly eight characters.

---

## 3. How GameMaker `string_pos()` Is Used

The key algorithm depends on the position of a character inside the 36-character string.

GameMaker's `string_pos()` uses one-based positions. That means the first character has position 1, not position 0.

The beginning of the table therefore looks like this:

| Character | Position |
|---|---:|
| A | 1 |
| B | 2 |
| C | 3 |
| D | 4 |
| E | 5 |
| F | 6 |
| G | 7 |
| H | 8 |
| I | 9 |
| J | 10 |
| K | 11 |
| L | 12 |
| M | 13 |
| N | 14 |
| O | 15 |
| P | 16 |
| Q | 17 |
| R | 18 |
| S | 19 |
| T | 20 |
| U | 21 |
| V | 22 |
| W | 23 |
| X | 24 |
| Y | 25 |
| Z | 26 |
| 0 | 27 |
| 1 | 28 |
| 2 | 29 |
| 3 | 30 |
| 4 | 31 |
| 5 | 32 |
| 6 | 33 |
| 7 | 34 |
| 8 | 35 |
| 9 | 36 |

If `string_pos()` cannot find a character, GameMaker returns `0`.

That is why the original code contains:

```gml
if (pos1 = 0 || pos2 = 0)
    return false
```

Any character outside the allowed character set immediately invalidates the key.

---

## 4. The Central Mathematical Rule

The most important line is:

```gml
if (pos1 != string_length(keystr) + 1 - pos2)
    return false
```

The character set is 36 characters long, so:

```text
string_length(keystr) = 36
```

Substituting 36 gives:

```text
pos1 != 36 + 1 - pos2
```

or:

```text
pos1 != 37 - pos2
```

For the pair to be valid:

```text
pos1 = 37 - pos2
```

Rearranging that equation:

```text
pos1 + pos2 = 37
```

So every pair of characters must have positions that add up to 37.

Examples:

```text
A is position 1
9 is position 36
1 + 36 = 37
```

Therefore:

```text
A <-> 9
```

Another example:

```text
D is position 4
6 is position 33
4 + 33 = 37
```

Therefore:

```text
D <-> 6
```

---

## 5. Complete Character Mapping

Because every position must pair with the position counted from the opposite end of the character set, the complete mapping is:

```text
A <-> 9
B <-> 8
C <-> 7
D <-> 6
E <-> 5
F <-> 4
G <-> 3
H <-> 2
I <-> 1
J <-> 0
K <-> Z
L <-> Y
M <-> X
N <-> W
O <-> V
P <-> U
Q <-> T
R <-> S
```

The relationship works in both directions. For example:

```text
A maps to 9
9 maps to A

K maps to Z
Z maps to K

R maps to S
S maps to R
```

Another way to visualize it is to place the alphabet above its reverse:

```text
ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789
9876543210ZYXWVUTSRQPONMLKJIHGFEDCBA
```

Characters directly above and below each other are partners.

---

## 6. Which Positions in the Key Are Compared

The loop is:

```gml
for (var c = 0; c < 8; c += 2)
```

The values of `c` are therefore:

```text
0
2
4
6
```

For every iteration, the validator reads:

```gml
string_char_at(key, c + 1)
```

and:

```gml
string_char_at(key, 8 - c)
```

That produces these comparisons:

| `c` | First position | Second position |
|---:|---:|---:|
| 0 | 1 | 8 |
| 2 | 3 | 6 |
| 4 | 5 | 4 |
| 6 | 7 | 2 |

At first this ordering looks unusual. Because the mirror rule is symmetrical, the overall requirement is equivalent to:

```text
Position 1 <-> Position 8
Position 2 <-> Position 7
Position 3 <-> Position 6
Position 4 <-> Position 5
```

In other words, the key is validated from the outside inward.

An eight-character key can be visualized as:

```text
1 2 3 4 5 6 7 8
| | | | | | | |
| | | +-----+ |
| | +---------+
| +-------------+
+-----------------
```

More clearly:

```text
1 <-> 8
2 <-> 7
3 <-> 6
4 <-> 5
```

Each pair must contain mirror characters from the mapping table.

---

## 7. Why Only the First Four Characters Matter

Suppose we choose these first four characters:

```text
A B C D
```

Their mirror characters are:

```text
A -> 9
B -> 8
C -> 7
D -> 6
```

The final half must be placed in reverse order because position 4 pairs with position 5, position 3 with position 6, and so on.

Start with:

```text
A B C D
```

Mirror each character:

```text
9 8 7 6
```

Reverse those mirrored characters:

```text
6 7 8 9
```

Append them to the prefix:

```text
ABCD6789
```

That is a valid key.

The general formula is:

```text
A B C D mirror(D) mirror(C) mirror(B) mirror(A)
```

Here `A`, `B`, `C`, and `D` are placeholders for any four valid characters; they do not have to literally be the letters A, B, C, and D.

---

## 8. Worked Example: `TEST`

Take this four-character prefix:

```text
TEST
```

Look up each character in the mapping:

```text
T -> Q
E -> 5
S -> R
T -> Q
```

If we simply wrote the mirrors in that order, we would have:

```text
Q5RQ
```

However, the suffix has to correspond to the prefix from right to left.

Reverse the prefix first:

```text
TSET
```

Then mirror each character:

```text
T -> Q
S -> R
E -> 5
T -> Q
```

The suffix is therefore:

```text
QR5Q
```

The complete key is:

```text
TESTQR5Q
```

Check each pair:

```text
Position 1: T <-> Q
Position 2: E <-> 5
Position 3: S <-> R
Position 4: T <-> Q
```

Every pair satisfies the rule, so the key is valid.

---

## 9. The Python Generator

The accompanying file is:

```text
keygen.py
```

It contains both a generator and an independent implementation of the validator.

The generator uses the same character set:

```python
CHARSET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
```

### Mirror function

The most important Python operation is conceptually:

```python
CHARSET[-1 - index]
```

Python normally indexes strings from zero:

```text
A -> index 0
B -> index 1
...
9 -> index 35
```

If a character is located at index `index`, then its mirror is located at:

```text
-1 - index
```

For example, `A` is at index 0:

```python
CHARSET[-1 - 0]
```

which becomes:

```python
CHARSET[-1]
```

The last character is `9`, so:

```text
A -> 9
```

For `B`, whose index is 1:

```python
CHARSET[-2]
```

The second-to-last character is `8`, so:

```text
B -> 8
```

This is a compact Python representation of exactly the same mirror operation performed by the GameMaker mathematics.

---

## 10. Generating a Key from a Prefix

Run:

```bash
python keygen.py --prefix ABCD
```

Output:

```text
ABCD6789
```

Another example:

```bash
python keygen.py --prefix TEST
```

Output:

```text
TESTQR5Q
```

The prefix must contain exactly four characters and may contain only `A-Z` and `0-9`.

Lowercase letters are automatically converted to uppercase:

```bash
python keygen.py --prefix test
```

produces:

```text
TESTQR5Q
```

---

## 11. Generating Random Valid Keys

If the script is run with no arguments:

```bash
python keygen.py
```

it generates one random valid key.

For example:

```text
F2KPULH4
```

Because the prefix is random, the exact output will normally be different each time.

To generate multiple keys, use `--count`:

```bash
python keygen.py --count 10
```

This prints ten valid keys, one per line.

The script uses Python's `secrets` module when selecting the random prefix. `secrets` is intended for generating values that should not be trivially predictable.

That does **not** make the original key-validation system cryptographically secure. The validator itself still exposes a simple mathematical rule. `secrets` merely provides good randomness when selecting among the possible valid prefixes.

---

## 12. Validating an Existing Key

The Python script can also check an existing key:

```bash
python keygen.py --validate ABCD6789
```

Output:

```text
VALID
```

An invalid example:

```bash
python keygen.py --validate ABCD1234
```

Output:

```text
INVALID
```

The Python validation routine duplicates the logical behavior of the GameMaker function, making it useful for testing generated keys without launching the original program.

---

## 13. Displaying the Complete Mapping

Run:

```bash
python keygen.py --show-mapping
```

The script prints every mirror pair.

Example beginning:

```text
Character mapping:

  A <-> 9
  B <-> 8
  C <-> 7
  D <-> 6
  ...
```

This can be useful when manually checking a key.

---

## 14. Number of Possible Valid Keys

Only the first four characters are independent.

Each position can contain any of the 36 allowed characters.

Therefore the number of possible prefixes is:

```text
36 x 36 x 36 x 36
```

which is:

```text
36^4 = 1,679,616
```

For every possible four-character prefix there is exactly one matching four-character suffix.

Therefore the validator accepts exactly:

```text
1,679,616 unique normalized keys
```

Here, "normalized" means uppercase. Because the GameMaker function converts input to uppercase, lowercase spellings are not genuinely separate keys; they resolve to the same uppercase value.

---

## 15. Why This Is Not a Secure License-Key System

This algorithm verifies a pattern, not a secret.

There is no hidden password, secret signing key, server request, cryptographic signature, database lookup, or protected checksum.

The complete acceptance rule exists directly in the client-side function:

```text
1. Key must contain eight characters.
2. Characters must belong to A-Z or 0-9.
3. Opposite character positions must contain mirror partners.
```

Once the validation function is visible, valid keys can be generated without guessing.

The first four characters contain all of the independent information. The final four are determined by them.

That gives the key approximately:

```text
log2(36^4) ~= 20.68 bits
```

of independent combinatorial space.

More importantly, an attacker does not need to brute-force that space if they understand the algorithm. They can construct a valid key directly.

This is why an algorithm like this is appropriate only when the goal is something such as:

- a simple puzzle,
- a formatting check,
- an easter egg,
- a low-stakes offline code system,
- testing,
- development tooling,
- or intentionally reversible codes.

It should not be relied on as the sole protection mechanism for paid software, accounts, valuable digital items, or other security-sensitive authorization.

---

## 16. If This Were a Real Licensing System

A more secure licensing design would normally avoid putting enough information in the client to manufacture arbitrary licenses.

A common approach is asymmetric digital signatures.

Conceptually:

```text
License data
    |
    v
Private signing key
    |
    v
Digital signature
    |
    v
License delivered to user
```

The application contains only the public verification key:

```text
License + signature
       |
       v
Public verification key
       |
       v
Valid / Invalid
```

The important distinction is that a public key can verify a signature but cannot practically be used to create new valid signatures.

That is very different from the supplied GameMaker validator, where the validation rule itself tells you exactly how to manufacture accepted keys.

Another option is server-side activation, where a client asks a trusted server whether a license is valid. This allows additional controls such as activation limits, revocation, expiration, account binding, and purchase verification, although it introduces networking and server-maintenance requirements.

---

## 17. Python Source Structure

The script is intentionally separated into small functions.

### `mirror_character(character)`

Returns the mirror partner for one character.

Example:

```python
mirror_character("A")
```

returns:

```text
9
```

### `generate_key(prefix)`

Takes exactly four valid characters and produces the matching eight-character key.

Example:

```python
generate_key("ABCD")
```

returns:

```text
ABCD6789
```

### `generate_random_key()`

Creates a random four-character prefix and passes it to `generate_key()`.

### `key_valid(key)`

Checks whether a supplied key follows the same rules as the GameMaker function.

### `print_mapping()`

Prints the complete character mapping for inspection.

### `main()`

Handles command-line arguments and decides which operation to perform.

---

## 18. Installing Python on Windows

If Python is already installed, check it with:

```powershell
python --version
```

or:

```powershell
py --version
```

You should see a Python version number.

The script requires no third-party packages. Everything it uses is included with normal Python installations.

There is therefore no `pip install` step.

---

## 19. Running the Script on Windows

Open PowerShell in the folder containing `keygen.py`.

For example, if it is in Downloads:

```powershell
cd "$HOME\Downloads"
```

Generate one key:

```powershell
python .\keygen.py
```

Generate five keys:

```powershell
python .\keygen.py --count 5
```

Generate a key from a chosen prefix:

```powershell
python .\keygen.py --prefix ABCD
```

Validate a key:

```powershell
python .\keygen.py --validate ABCD6789
```

Show the mapping:

```powershell
python .\keygen.py --show-mapping
```

If your system uses the Windows Python launcher instead of the `python` command, replace `python` with `py`:

```powershell
py .\keygen.py --prefix ABCD
```

---

## 20. Summary of the Entire Algorithm

The complete system can be reduced to these steps:

1. Convert the supplied key to uppercase.
2. Require exactly eight characters.
3. Allow only `A-Z` and `0-9`.
4. Use this ordered character set:

   ```text
   ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789
   ```

5. Treat characters at opposite ends of that set as partners.
6. Require key positions `1/8`, `2/7`, `3/6`, and `4/5` to contain partner characters.
7. Therefore, choose any four-character prefix.
8. Reverse the prefix.
9. Replace every character in that reversed prefix with its mirror partner.
10. Append the resulting four characters to the original prefix.

In compact form:

```text
PREFIX = A B C D
KEY    = A B C D mirror(D) mirror(C) mirror(B) mirror(A)
```

Example:

```text
Prefix: ABCD

D -> 6
C -> 7
B -> 8
A -> 9

Key: ABCD6789
```

That is the entire mechanism implemented by both the original GameMaker validator and the accompanying Python generator.
