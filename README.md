# icu_rbnf

A Python library for spelling out numbers into words using ICU's Rule-Based Number Format (RBNF).

## Installation

```bash
pip install icu_rbnf
```

## Usage

```python
import icu_rbnf

# Spell out numbers in words
icu_rbnf.spellout(123, "en_US")     # "one hundred twenty-three"
icu_rbnf.spellout(123.7, "en_US")   # "one hundred twenty-three point seven"
icu_rbnf.spellout(123, "fr_FR")     # "cent vingt-trois"

# Get ordinal form (e.g., "1st", "2nd")
icu_rbnf.ordinal(21, "en_US")       # "21st"

# Get word-based ordinal (e.g., "first", "twenty-first")
icu_rbnf.spellout_ordinal(21, "en_US")  # "twenty-first"

# Check if a locale is supported
icu_rbnf.is_locale_supported("en_US")  # True
```

## API

### `spellout(number: int | float, locale: str) -> str`

Spell out a number into words for the given locale. Supports both integers and floats.

### `ordinal(number: int | float, locale: str) -> str`

Get the ordinal form of a number for the given locale (e.g., "1st", "2nd"). Floats are truncated to integers.

### `spellout_ordinal(number: int | float, locale: str) -> str`

Spell out ordinal form of a number for the given locale (e.g., "first", "twenty-first"). Floats are truncated to integers. Note: Not all locales support word-based ordinals; some may fall back to numeric format.

### `is_locale_supported(locale: str) -> bool`

Check if a locale is supported by ICU RBNF.

### `error`

Exception class raised when ICU RBNF operations fail.

## Requirements

- Python 3.9+
- ICU library (dynamically linked, no separate installation required)
