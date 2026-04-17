# icu_rbnf

A Python library for spelling out numbers into words using ICU's Rule-Based Number Format (RBNF).

## Installation

```bash
pip install icu_rbnf
```

## Usage

```python
import icu_rbnf

icu_rbnf.spellout(123, "en_US")   # "one hundred twenty-three"
icu_rbnf.spellout(123, "fr_FR")   # "cent vingt-trois"
icu_rbnf.ordinal(21, "en_US")     # "21st" or locale-equivalent
```

## API

### `spellout(number: int | float, locale: str) -> str`

Spell out a number into words for the given locale.

### `ordinal(number: int | float, locale: str) -> str`

Get the ordinal form of a number for the given locale.
