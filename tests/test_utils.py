import pytest
from src.fx_calc.utils import *


class TestParseSymbol:
    def test_parse_standard_format(self):
        base, quote = parse_symbol("EURUSD")
        assert base == "EUR"
        assert quote == "USD"

    def test_parse_with_separator_slash(self):
        base, quote = parse_symbol("EUR/USD")
        assert base == "EUR"
        assert quote == "USD"

    def test_parse_with_separator_dash(self):
        base, quote = parse_symbol("EUR-USD")
        assert base == "EUR"
        assert quote == "USD"

    def test_parse_case_insensitive(self):
        base, quote = parse_symbol("eurusd")
        assert base == "EUR"
        assert quote == "USD"

    def test_parse_invalid_length(self):
        with pytest.raises(ValueError, match="Invalid symbol format: 'EURUS'. Symbol must contain only 6 letters."):
            parse_symbol("EURUS")

    def test_parse_invalid_characters(self):
        with pytest.raises(ValueError, match="Invalid symbol format: 'EUR123'. Symbol must contain only letters."):
            parse_symbol("EUR123")


class TestValidateSymbol:
    def test_validate_valid_symbols(self):
        assert validate_symbol("EURUSD") is True
        assert validate_symbol("EUR/USD") is True
        assert validate_symbol("EUR-USD") is True
        assert validate_symbol("EurUsd") is True

    def test_validate_invalid_symbols(self):
        assert validate_symbol("EUR") is False
        assert validate_symbol("1EURUS") is False


class TestExtractFromSymbol:
    def test_extract_base_from_symbol(self):
        assert extract_base_from_symbol("eurUSD") == "EUR"
        assert extract_base_from_symbol("GbPUSD") == "GBP"
        assert extract_base_from_symbol("USdJPY") == "USD"

    def test_extract_quote_from_symbol(self):
        assert extract_quote_from_symbol("EURuSD") == "USD"
        assert extract_quote_from_symbol("GBPUsD") == "USD"
        assert extract_quote_from_symbol("USDJPy") == "JPY"

    def test_extract_with_invalid_pair(self):
        with pytest.raises(ValueError):
            extract_base_from_symbol("EUR")

        with pytest.raises(ValueError):
            extract_quote_from_symbol("123EUR")
