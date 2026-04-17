"""Type stubs for icu_rbnf."""

from typing import Union

class RBNFError(Exception):
    """Exception raised when ICU RBNF operations fail."""

def spellout(number: Union[int, float], locale: str) -> str:
    """Spell out a number into words for the given locale."""
    ...

def ordinal(number: Union[int, float], locale: str) -> str:
    """Get the ordinal form of a number for the given locale (e.g., '1st', '2nd')."""
    ...

def spellout_ordinal(number: Union[int, float], locale: str) -> str:
    """Spell out ordinal form of a number for the given locale (e.g., 'first', 'twenty-first')."""
    ...

def is_locale_supported(locale: str) -> bool:
    """Check if a locale is supported by ICU RBNF."""
    ...

error: RBNFError
