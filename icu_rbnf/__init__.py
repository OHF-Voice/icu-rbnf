"""ICU RBNF - Spell out numbers into words using ICU's Rule-Based Number Format."""

from __future__ import annotations

from icu_rbnf._icu import spellout, ordinal, spellout_ordinal, error

__all__ = ["spellout", "ordinal", "spellout_ordinal", "error"]
__version__ = "0.1.0"
