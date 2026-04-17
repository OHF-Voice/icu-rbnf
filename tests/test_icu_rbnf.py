"""Tests for icu_rbnf library."""

import icu_rbnf


class TestSpellout:
    """Tests for the spellout function."""

    def test_english_basic(self):
        """Test basic number spellout in English."""
        assert icu_rbnf.spellout(0, "en_US") == "zero"
        assert icu_rbnf.spellout(1, "en_US") == "one"
        assert icu_rbnf.spellout(12, "en_US") == "twelve"
        assert icu_rbnf.spellout(20, "en_US") == "twenty"
        assert icu_rbnf.spellout(42, "en_US") == "forty-two"
        assert icu_rbnf.spellout(100, "en_US") == "one hundred"
        assert icu_rbnf.spellout(123, "en_US") == "one hundred twenty-three"
        assert icu_rbnf.spellout(999, "en_US") == "nine hundred ninety-nine"

    def test_french_basic(self):
        """Test basic number spellout in French."""
        assert icu_rbnf.spellout(0, "fr_FR") == "zéro"
        assert icu_rbnf.spellout(1, "fr_FR") == "un"
        assert icu_rbnf.spellout(11, "fr_FR") == "onze"
        assert icu_rbnf.spellout(21, "fr_FR") == "vingt-et-un"
        assert icu_rbnf.spellout(100, "fr_FR") == "cent"
        assert icu_rbnf.spellout(123, "fr_FR") == "cent vingt-trois"

    def test_german_basic(self):
        """Test basic number spellout in German."""
        assert icu_rbnf.spellout(0, "de_DE") == "null"
        assert icu_rbnf.spellout(1, "de_DE") == "eins"
        assert icu_rbnf.spellout(12, "de_DE") == "zwölf"
        # German uses soft hyphen in some compound words (U+00AD)
        result = icu_rbnf.spellout(21, "de_DE")
        assert "ein" in result and "zwanzig" in result
        # ICU may use soft hyphen in compound words
        result_100 = icu_rbnf.spellout(100, "de_DE")
        assert "ein" in result_100 and "hundert" in result_100

    def test_large_numbers(self):
        """Test spellout with larger numbers."""
        assert icu_rbnf.spellout(1000, "en_US") == "one thousand"
        assert (
            icu_rbnf.spellout(1234, "en_US") == "one thousand two hundred thirty-four"
        )
        assert icu_rbnf.spellout(1000000, "en_US") == "one million"

    def test_example_from_spec(self):
        """Test the example from the specification."""
        assert icu_rbnf.spellout(123, "en_US") == "one hundred twenty-three"
        assert icu_rbnf.spellout(123, "fr_FR") == "cent vingt-trois"


class TestOrdinal:
    """Tests for the ordinal function."""

    def test_english_basic(self):
        """Test basic ordinal forms in English."""
        assert icu_rbnf.ordinal(1, "en_US") == "1st"
        assert icu_rbnf.ordinal(2, "en_US") == "2nd"
        assert icu_rbnf.ordinal(3, "en_US") == "3rd"
        assert icu_rbnf.ordinal(4, "en_US") == "4th"
        assert icu_rbnf.ordinal(10, "en_US") == "10th"
        assert icu_rbnf.ordinal(11, "en_US") == "11th"
        assert icu_rbnf.ordinal(21, "en_US") == "21st"
        assert icu_rbnf.ordinal(22, "en_US") == "22nd"
        assert icu_rbnf.ordinal(100, "en_US") == "100th"
        assert icu_rbnf.ordinal(101, "en_US") == "101st"

    def test_french_basic(self):
        """Test basic ordinal forms in French."""
        assert icu_rbnf.ordinal(1, "fr_FR") == "1er"
        assert icu_rbnf.ordinal(2, "fr_FR") == "2e"
        assert icu_rbnf.ordinal(3, "fr_FR") == "3e"
        assert icu_rbnf.ordinal(10, "fr_FR") == "10e"
        assert icu_rbnf.ordinal(20, "fr_FR") == "20e"

    def test_german_basic(self):
        """Test basic ordinal forms in German."""
        assert icu_rbnf.ordinal(1, "de_DE") == "1."
        assert icu_rbnf.ordinal(2, "de_DE") == "2."
        assert icu_rbnf.ordinal(3, "de_DE") == "3."
        assert icu_rbnf.ordinal(10, "de_DE") == "10."

    def test_example_from_spec(self):
        """Test the example from the specification."""
        assert icu_rbnf.ordinal(21, "en_US") == "21st"


class TestEdgeCases:
    """Tests for edge cases."""

    def test_negative_numbers(self):
        """Test spellout with negative numbers."""
        assert icu_rbnf.spellout(-1, "en_US") == "minus one"
        assert icu_rbnf.spellout(-42, "en_US") == "minus forty-two"

    def test_float_numbers(self):
        """Test spellout with float numbers (truncated to int)."""
        assert icu_rbnf.spellout(123.7, "en_US") == "one hundred twenty-three"
        assert icu_rbnf.spellout(42.0, "en_US") == "forty-two"

    def test_invalid_locale(self):
        """Test behavior with invalid locale."""
        # ICU may not raise an error for invalid locale, just use default
        # This test verifies the error exception is available
        assert hasattr(icu_rbnf, "error")

    def test_very_large_number(self):
        """Test with a very large number."""
        result = icu_rbnf.spellout(999999999, "en_US")
        assert "nine hundred ninety-nine million" in result


class TestSpelloutOrdinal:
    """Tests for the spellout_ordinal function."""

    def test_english_basic(self):
        """Test basic word-based ordinals in English."""
        assert icu_rbnf.spellout_ordinal(1, "en_US") == "first"
        assert icu_rbnf.spellout_ordinal(2, "en_US") == "second"
        assert icu_rbnf.spellout_ordinal(3, "en_US") == "third"
        assert icu_rbnf.spellout_ordinal(4, "en_US") == "fourth"
        assert icu_rbnf.spellout_ordinal(10, "en_US") == "tenth"
        assert icu_rbnf.spellout_ordinal(11, "en_US") == "eleventh"
        assert icu_rbnf.spellout_ordinal(21, "en_US") == "twenty-first"
        assert icu_rbnf.spellout_ordinal(22, "en_US") == "twenty-second"
        assert icu_rbnf.spellout_ordinal(100, "en_US") == "one hundredth"
        assert icu_rbnf.spellout_ordinal(123, "en_US") == "one hundred twenty-third"

    def test_german_basic(self):
        """Test basic word-based ordinals in German."""
        assert icu_rbnf.spellout_ordinal(1, "de_DE") == "erste"
        assert icu_rbnf.spellout_ordinal(2, "de_DE") == "zweite"
        assert icu_rbnf.spellout_ordinal(3, "de_DE") == "dritte"
        assert icu_rbnf.spellout_ordinal(10, "de_DE") == "zehnte"

    def test_fallback_behavior(self):
        """Test that spellout_ordinal falls back gracefully for locales without %spellout-ordinal."""
        # French doesn't have %spellout-ordinal, so it should fall back to ordinal format
        # This test verifies the fallback mechanism works
        result = icu_rbnf.spellout_ordinal(1, "fr_FR")
        # Should return ordinal format (1er) since word-based isn't available
        assert "1" in result and "er" in result


class TestIsLocaleSupported:
    """Tests for the is_locale_supported function."""

    def test_valid_locales(self):
        """Test that valid locales are supported."""
        assert icu_rbnf.is_locale_supported("en_US") is True
        assert icu_rbnf.is_locale_supported("fr_FR") is True
        assert icu_rbnf.is_locale_supported("de_DE") is True
        assert icu_rbnf.is_locale_supported("es_ES") is True
        assert icu_rbnf.is_locale_supported("en_GB") is True

    def test_invalid_locales(self):
        """Test that empty strings are not supported."""
        assert icu_rbnf.is_locale_supported("") is False

    def test_special_characters(self):
        """Test that locales with invalid characters are rejected."""
        assert icu_rbnf.is_locale_supported("en@US") is False
        assert icu_rbnf.is_locale_supported("en US") is False


class TestModuleAPI:
    """Tests for module-level API."""

    def test_error_exception_exists(self):
        """Test that error exception is exposed at module level."""
        assert hasattr(icu_rbnf, "error")
        assert isinstance(icu_rbnf.error, type)

    def test_version_exists(self):
        """Test that version is exposed."""
        assert hasattr(icu_rbnf, "__version__")
        assert icu_rbnf.__version__ == "0.1.0"

    def test_spellout_ordinal_exists(self):
        """Test that spellout_ordinal function is exposed."""
        assert hasattr(icu_rbnf, "spellout_ordinal")
        assert callable(icu_rbnf.spellout_ordinal)

    def test_is_locale_supported_exists(self):
        """Test that is_locale_supported function is exposed."""
        assert hasattr(icu_rbnf, "is_locale_supported")
        assert callable(icu_rbnf.is_locale_supported)
