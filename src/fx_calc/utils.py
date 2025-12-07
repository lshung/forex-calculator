import re
from decimal import Decimal
from typing import Tuple, Union


def parse_symbol(symbol: str) -> Tuple[str, str]:
    cleaned = re.sub(r'[-/]', '', symbol.upper())

    if len(cleaned) != 6:
        raise ValueError(f"Invalid symbol format: '{symbol}'. Symbol must contain only 6 letters.")

    if not cleaned.isalpha():
        raise ValueError(f"Invalid symbol format: '{symbol}'. Symbol must contain only letters.")

    base = cleaned[:3]
    quote = cleaned[3:]

    return base, quote

def validate_symbol(symbol: str) -> bool:
    try:
        parse_symbol(symbol)
        return True
    except ValueError:
        return False

def extract_base_from_symbol(symbol: str) -> str:
    base, _ = parse_symbol(symbol)
    return base

def extract_quote_from_symbol(symbol: str) -> str:
    _, quote = parse_symbol(symbol)
    return quote

def to_decimal(value: Union[Decimal, int, float, str]) -> Decimal:
    if isinstance(value, Decimal):
        return value

    try:
        return Decimal(str(value))
    except:
        raise ValueError(f"Cannot convert value '{value}' to Decimal.")
