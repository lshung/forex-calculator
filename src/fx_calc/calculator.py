from decimal import Decimal
from typing import Optional, Union
from src.fx_calc.utils import validate_symbol, to_decimal


class Calculator:
    def __init__(self):
        self._symbol: Optional[str] = None
        self._is_long: Optional[bool] = None
        self._position_size_in_lots: Optional[Decimal] = None
        self._entry_price: Optional[Decimal] = None
        self._sl_price: Optional[Decimal] = None
        self._tp_price: Optional[Decimal] = None
        self._sl_in_pips: Optional[Decimal] = None
        self._tp_in_pips: Optional[Decimal] = None
        self._sl_in_points: Optional[Decimal] = None
        self._tp_in_points: Optional[Decimal] = None
        self._sl_in_money: Optional[Decimal] = None
        self._tp_in_money: Optional[Decimal] = None
        self._commission_currency: Optional[str] = None
        self._commission_per_lot_in_pips: Optional[Decimal] = None
        self._commission_per_lot_in_points: Optional[Decimal] = None
        self._commission_per_lot_in_money: Optional[Decimal] = None
        self._sl_with_commission_in_pips: Optional[Decimal] = None
        self._tp_with_commission_in_pips: Optional[Decimal] = None
        self._sl_with_commission_in_points: Optional[Decimal] = None
        self._tp_with_commission_in_points: Optional[Decimal] = None
        self._sl_with_commission_in_money: Optional[Decimal] = None
        self._tp_with_commission_in_money: Optional[Decimal] = None

    def set_symbol(self, value: str):
        if not value or not isinstance(value, str):
            raise ValueError("Symbol must be a non-empty string.")

        if not validate_symbol(value):
            raise ValueError("Invalid symbol.")

        self._symbol = value

    def set_is_long(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("Is long must be a boolean.")

        self._is_long = value

    def set_position_size_in_lots(self, value: Union[Decimal, int, float, str]):
        value = to_decimal(value)

        if value <= 0:
            raise ValueError("Position size must be positive.")

        self._position_size_in_lots = value

    def set_entry_price(self, value: Union[Decimal, int, float, str]):
        value = to_decimal(value)

        if value <= 0:
            raise ValueError("Entry price must be positive.")

        self._entry_price = value

    def set_sl_price(self, value: Union[Decimal, int, float, str]):
        value = to_decimal(value)

        if value <= 0:
            raise ValueError("Stop loss price must be positive.")

        self._sl_price = value

    def set_tp_price(self, value: Union[Decimal, int, float, str]):
        value = to_decimal(value)

        if value <= 0:
            raise ValueError("Take profit price must be positive.")

        self._tp_price = value

    def set_sl_in_pips(self, value: Union[Decimal, int, float, str]):
        value = to_decimal(value)

        if value <= 0:
            raise ValueError("Stop loss in pips must be positive.")

        self._sl_in_pips = value

    def set_tp_in_pips(self, value: Union[Decimal, int, float, str]):
        value = to_decimal(value)

        if value <= 0:
            raise ValueError("Take profit in pips must be positive.")

        self._tp_in_pips = value

    def set_sl_in_points(self, value: Union[Decimal, int, float, str]):
        value = to_decimal(value)

        if value <= 0:
            raise ValueError("Stop loss in points must be positive.")

        self._sl_in_points = value

    def set_tp_in_points(self, value: Union[Decimal, int, float, str]):
        value = to_decimal(value)

        if value <= 0:
            raise ValueError("Take profit in points must be positive.")

        self._tp_in_points = value

    def set_sl_in_money(self, value: Union[Decimal, int, float, str]):
        value = to_decimal(value)

        if value <= 0:
            raise ValueError("Stop loss in money must be positive.")

        self._sl_in_money = value

    def set_commission_currency(self, value: str):
        if not value or not isinstance(value, str):
            raise ValueError("Commission currency must be a non-empty string.")

        self._commission_currency = value

    def set_commission_per_lot_in_money(self, value: Union[Decimal, int, float, str]):
        value = to_decimal(value)

        if value < 0:
            raise ValueError("Commission per lot in money must be non-negative.")

        self._commission_per_lot_in_money = value

    def set_sl_with_commission_in_money(self, value: Union[Decimal, int, float, str]):
        value = to_decimal(value)

        if value < 0:
            raise ValueError("Stop loss with commission in money must be non-negative.")

        self._sl_with_commission_in_money = value
