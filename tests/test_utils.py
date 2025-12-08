import pytest
from src.fx_calc.utils import *


class TestParseSymbol:
    def test_parse_symbol_with_valid_values(self):
        assert parse_symbol("EURUSD") == ("EUR", "USD")
        assert parse_symbol("eur/USD") == ("EUR", "USD")
        assert parse_symbol("Eur-uSd") == ("EUR", "USD")

    def test_parse_symbol_with_invalid_values(self):
        with pytest.raises(ValueError, match="Symbol must contain only 6 letters."):
            parse_symbol("EURUS")
        with pytest.raises(ValueError, match="Symbol must contain only letters."):
            parse_symbol("EUR123")
        with pytest.raises(TypeError, match="Symbol must be a non-empty string."):
            parse_symbol(None)
        with pytest.raises(TypeError, match="Symbol must be a non-empty string."):
            parse_symbol(123456)


class TestValidateSymbol:
    def test_validate_symbol_with_valid_values(self):
        assert validate_symbol("EURUSD") is True
        assert validate_symbol("EUR/USD") is True
        assert validate_symbol("EUR-USD") is True
        assert validate_symbol("EurUsd") is True

    def test_validate_symbol_with_invalid_values(self):
        assert validate_symbol("EUR") is False
        assert validate_symbol("1EURUS") is False


class TestExtractFromSymbol:
    def test_extract_from_symbol_with_valid_values(self):
        assert extract_base_from_symbol("eurUSD") == "EUR"
        assert extract_base_from_symbol("GbPUSD") == "GBP"
        assert extract_base_from_symbol("USdJPY") == "USD"
        assert extract_quote_from_symbol("EURuSD") == "USD"
        assert extract_quote_from_symbol("GBPUsD") == "USD"
        assert extract_quote_from_symbol("USDJPy") == "JPY"

    def test_extract_from_symbol_with_invalid_values(self):
        with pytest.raises(ValueError):
            extract_base_from_symbol("EUR")
        with pytest.raises(ValueError):
            extract_quote_from_symbol("123EUR")


class TestToDecimal:
    def test_to_decimal_with_valid_values(self):
        assert to_decimal(Decimal(1.0)) == Decimal(1.0)
        assert to_decimal(1) == Decimal("1")
        assert to_decimal(1.0) == Decimal("1.0")
        assert to_decimal("1.0") == Decimal(1.0)
        assert to_decimal("1") == Decimal(1)

    def test_to_decimal_with_invalid_values(self):
        with pytest.raises(TypeError):
            to_decimal(None)
        with pytest.raises(TypeError):
            to_decimal(object())
        with pytest.raises(ValueError):
            to_decimal("12f")
        with pytest.raises(ValueError):
            to_decimal("invalid")


class TestParseCurrency:
    def test_parse_currency_with_valid_values(self):
        assert parse_currency("EUR") == "EUR"
        assert parse_currency("eUr") == "EUR"

    def test_parse_currency_with_invalid_values(self):
        with pytest.raises(TypeError):
            parse_currency(None)
        with pytest.raises(TypeError):
            parse_currency(object())
        with pytest.raises(ValueError):
            parse_currency("123")
        with pytest.raises(ValueError):
            parse_currency("invalid")


class TestExchangeCurrencyByRate:
    def test_exchange_currency_by_rate_with_valid_values(self):
        assert exchange_currency_by_rate(
            source_amount=Decimal("100"),
            source_currency="Eur",
            exchange_symbol="EUR/usd",
            exchange_rate=Decimal("1.21868")
        ) == (Decimal("121.868"), "USD")
        assert exchange_currency_by_rate(
            source_amount=Decimal("20586.8"),
            source_currency="jPy",
            exchange_symbol="gbp-JPY",
            exchange_rate=Decimal("205.868")
        ) == (Decimal("100"), "GBP")

    def test_exchange_currency_by_rate_with_invalid_values(self):
        with pytest.raises(TypeError):
            exchange_currency_by_rate(
                source_amount=None,
                source_currency="EUR",
                exchange_symbol="EUR/usd",
                exchange_rate=Decimal("1.21868")
            )
        with pytest.raises(TypeError):
            exchange_currency_by_rate(
                source_amount=Decimal("100"),
                source_currency="EUR",
                exchange_symbol="EUR/usd",
                exchange_rate=None
            )
        with pytest.raises(ValueError):
            exchange_currency_by_rate(
                source_amount=Decimal("100"),
                source_currency="EUR",
                exchange_symbol="EUR/usd",
                exchange_rate=Decimal("-1")
            )
        with pytest.raises(ValueError, match="Exchange symbol must contain different base and quote currencies."):
            exchange_currency_by_rate(
                source_amount=Decimal("100"),
                source_currency="EUR",
                exchange_symbol="usd/usd",
                exchange_rate=Decimal("1.21868")
            )
        with pytest.raises(ValueError, match="Source currency 'GBP' does not match exchange symbol 'EURUSD'."):
            exchange_currency_by_rate(
                source_amount=Decimal("100"),
                source_currency="GBP",
                exchange_symbol="EUR/usd",
                exchange_rate=Decimal("1.21868")
            )
