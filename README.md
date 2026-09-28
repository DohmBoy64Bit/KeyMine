# RetroMine - Key Generator for Mine-imator

A Python key generator and validator for the 8-character key format used by [Mine-imator](https://github.com/stuffbydavid/mine-imator). Generate random keys, build a key around your own 4-character prefix, and check whether an existing key is valid — from a desktop interface or the command line.

No third-party packages required.

## Features

- Desktop interface and optional command-line usage
- Generate random valid keys
- Create a valid key from your own 4-character prefix
- Live preview while entering a custom prefix
- Validate existing keys
- Copy generated keys to the clipboard
- View the supported character mapping

## Requirements

- Python 3
- Windows, Linux, or macOS with Tkinter available

Tkinter is included with most standard Python installations.

## Running the App

Download `keygen.py`, open a terminal in the same folder, and run:

```bash
python keygen.py
```

On Windows, you may also be able to use:

```powershell
py keygen.py
```

The graphical key generator will open automatically.

## Custom Keys

The generator can build a valid 8-character key around a custom 4-character prefix.

For example, entering:

```text
DOHM
```

produces:

```text
DOHMX2V6
```

This lets you create recognizable keys while still following the format expected by the validator.

Custom prefixes must:

- Be exactly 4 characters long
- Use letters A-Z and/or numbers 0-9
- Avoid spaces and special characters

Input is automatically treated as uppercase.

A typical custom-key workflow:

1. Launch the program.
2. Choose the custom key option.
3. Enter `DOHM`.
4. The generator produces `DOHMX2V6`.
5. Copy the finished key.

## Using the Interface

### Generate a Random Key

Use the random generation option to create a new valid key immediately.

The generated key can then be copied to the clipboard.

### Generate a Custom Key

Enter a 4-character prefix such as:

```text
DOHM
```

The app will calculate the completed key:

```text
DOHMX2V6
```

This is useful when you want the beginning of the key to contain a recognizable word, abbreviation, or identifier.

### Validate a Key

Paste or type an 8-character key into the validation field.

The app will tell you whether the key matches the supported format.

### Copy a Key

Use the **Copy** button to place the current generated key on your clipboard.

## Command-Line Usage

The graphical interface is the default, but the generator also supports command-line commands.

### Generate From a Prefix

```bash
python keygen.py --prefix DOHM
```

Example output:

```text
DOHMX2V6
```

### Validate a Key

```bash
python keygen.py --validate DOHMX2V6
```

### Generate Multiple Random Keys

```bash
python keygen.py --count 10
```

### Show the Character Mapping

```bash
python keygen.py --show-mapping
```

## Algorithm Documentation

The full explanation of the validation format — character set, mirror mapping, and worked examples — is in [docs/KEYGEN_GUIDE.md](docs/KEYGEN_GUIDE.md).

## Troubleshooting

### The window does not open

Make sure Python is installed:

```bash
python --version
```

On Windows, also try:

```powershell
py --version
```

If Python is installed but Tkinter is missing, install or repair a standard Python distribution that includes Tkinter.

### My custom prefix is rejected

Make sure the prefix contains exactly four characters and only uses:

```text
A-Z
0-9
```

For example:

```text
DOHM
GAME
AB12
2026
```

### A generated key is lowercase

The generator normalizes supported input to uppercase, so lowercase custom prefixes are handled automatically.

For example:

```text
dohm
```

is treated as:

```text
DOHM
```

## Files

```text
keygen.py               Graphical application and command-line interface
README.md               This file
docs/KEYGEN_GUIDE.md    Algorithm documentation
```

## About

[Mine-imator](https://github.com/stuffbydavid/mine-imator) is a free 3D movie maker based on Minecraft. The software itself is free, and the developer accepts donations in exchange for a key — but if you'd rather not donate, a key can be generated for free on the [official website](https://www.mineimator.com).

This project was meant to be a fun little thing: a small side project for seeing how the key format works, and nothing more. It isn't affiliated with Mine-imator or its developer. If you enjoy the software, please consider supporting its creator.

## Notes

This generator is designed specifically for the validation format it implements. Keys produced by it are not universal license keys and will not work with unrelated software or other validation systems.

## License

Use, modify, and adapt the project according to the license you choose for your repository.
