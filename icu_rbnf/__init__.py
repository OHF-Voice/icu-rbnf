"""ICU RBNF - Spell out numbers into words using ICU's Rule-Based Number Format."""

from __future__ import annotations

from icu_rbnf._icu import (
    error,
    icu_version,
    is_locale_supported,
    ordinal,
    spellout,
    spellout_ordinal,
)

__all__ = [
    "spellout",
    "ordinal",
    "spellout_ordinal",
    "is_locale_supported",
    "icu_version",
    "error",
]
__version__ = "0.2.0"
