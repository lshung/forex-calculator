from decimal import Decimal, ROUND_FLOOR
from src.fx_calc.utils import *
from src.fx_calc.calculator_base import CalculatorBase


class Calculator(CalculatorBase):
    def __init__(self):
        super().__init__()

    def calculate(self):
        self._validate()
        self._calculate_sl_price_and_in_pips_and_in_points()
        self._calculate_tp_price_and_in_pips_and_in_points()
        self._calculate_commission_per_lot_in_pips()
        self._calculate_rr_with_commission()
        self._calculate_position_size()
        self._calculate_sl_in_money()
        self._calculate_tp_in_money()
        self._calculate_sl_with_commission_in_money()
        self._calculate_tp_with_commission_in_money()

    def _validate(self):
        self._validate_required_fields()
        self._validate_exchange_rate()

    def _validate_required_fields(self):
        if self._symbol is None:
            raise Exception("Symbol is required.")

        if self._is_long is None:
            raise Exception("Is long is required.")

        if self._entry_price is None:
            raise Exception("Entry price is required.")

    def _validate_exchange_rate(self):
        if self._quote_currency == self._target_currency:
            return

        exchange_pair = f"{self._quote_currency}{self._target_currency}"
        reverse_exchange_pair = f"{self._target_currency}{self._quote_currency}"

        if self._exchange_rate is None or self._exchange_rate["symbol"] is None or self._exchange_rate["rate"] is None:
            raise Exception(f"Exchange rate of '{exchange_pair}' or '{reverse_exchange_pair}' is required.")

        if self._exchange_rate["rate"] <= 0:
            raise Exception("Exchange rate rate must be positive.")

        base, quote = parse_symbol(self._exchange_rate["symbol"])

        if self._quote_currency != base and self._quote_currency != quote:
            raise Exception(f"Exchange rate of '{exchange_pair}' or '{reverse_exchange_pair}' is required.")

        if self._target_currency != base and self._target_currency != quote:
            raise Exception(f"Exchange rate of '{exchange_pair}' or '{reverse_exchange_pair}' is required.")

    def _calculate_sl_price_and_in_pips_and_in_points(self):
        if self._sl_price is not None and self._sl_in_pips is None and self._sl_in_points is None:
            self._calculate_sl_in_pips_by_prices()
            self._calculate_sl_in_points_by_pips()
        elif self._sl_in_pips is not None and self._sl_price is None and self._sl_in_points is None:
            self._calculate_sl_price_by_pips()
            self._calculate_sl_in_points_by_pips()
        elif self._sl_in_points is not None and self._sl_price is None and self._sl_in_pips is None:
            self._calculate_sl_in_pips_by_points()
            self._calculate_sl_price_by_pips()
        else:
            raise Exception("Only one of the stop loss price, stop loss in pips or stop loss in points is set.")

    def _calculate_tp_price_and_in_pips_and_in_points(self):
        if self._tp_price is not None and self._tp_in_pips is None and self._tp_in_points is None:
            self._calculate_tp_in_pips_by_prices()
            self._calculate_tp_in_points_by_pips()
        elif self._tp_in_pips is not None and self._tp_price is None and self._tp_in_points is None:
            self._calculate_tp_price_by_pips()
            self._calculate_tp_in_points_by_pips()
        elif self._tp_in_points is not None and self._tp_price is None and self._tp_in_pips is None:
            self._calculate_tp_in_pips_by_points()
            self._calculate_tp_price_by_pips()
        else:
            raise Exception("Only one of the take profit price, take profit in pips or take profit in points is set.")

    def _calculate_sl_in_pips_by_prices(self):
        self._sl_in_pips = abs(self._entry_price - self._sl_price) / self._pip_value

    def _calculate_tp_in_pips_by_prices(self):
        self._tp_in_pips = abs(self._tp_price - self._entry_price) / self._pip_value

    def _calculate_sl_price_by_pips(self):
        if self._is_long:
            self._sl_price = self._entry_price - self._sl_in_pips * self._pip_value
        else:
            self._sl_price = self._entry_price + self._sl_in_pips * self._pip_value

    def _calculate_tp_price_by_pips(self):
        if self._is_long:
            self._tp_price = self._entry_price + self._tp_in_pips * self._pip_value
        else:
            self._tp_price = self._entry_price - self._tp_in_pips * self._pip_value

    def _calculate_sl_in_points_by_pips(self):
        self._sl_in_points = convert_pips_to_points(self._sl_in_pips)

    def _calculate_tp_in_points_by_pips(self):
        self._tp_in_points = convert_pips_to_points(self._tp_in_pips)

    def _calculate_sl_in_pips_by_points(self):
        self._sl_in_pips = convert_points_to_pips(self._sl_in_points)

    def _calculate_tp_in_pips_by_points(self):
        self._tp_in_pips = convert_points_to_pips(self._tp_in_points)

    def _calculate_commission_per_lot_in_pips(self):
        if self._commission_per_lot_in_money is None:
            self._commission_per_lot_in_pips = 0
            return

        if self._quote_currency == self._target_currency:
            commission_per_lot_in_quote = self._commission_per_lot_in_money
        else:
            exchange_result = exchange_currency_by_rate(
                source_amount=self._commission_per_lot_in_money,
                source_currency=self._target_currency,
                exchange_symbol=self._exchange_rate["symbol"],
                exchange_rate=self._exchange_rate["rate"],
            )
            commission_per_lot_in_quote = exchange_result[0]

        self._commission_per_lot_in_pips = commission_per_lot_in_quote / self._pip_value / self._lot_size

    def _calculate_rr_with_commission(self):
        self._sl_with_commission_in_pips = self._sl_in_pips + self._commission_per_lot_in_pips
        self._tp_with_commission_in_pips = self._tp_in_pips - self._commission_per_lot_in_pips
        self._sl_with_commission_in_points = convert_pips_to_points(self._sl_with_commission_in_pips)
        self._tp_with_commission_in_points = convert_pips_to_points(self._tp_with_commission_in_pips)

    def _calculate_position_size(self):
        if self._position_size_in_lots is not None and self._sl_in_money is None and self._sl_with_commission_in_money is None:
            return
        elif self._position_size_in_lots is None and self._sl_in_money is not None and self._sl_with_commission_in_money is None:
            self._calculate_position_size_by_sl_in_money()
        elif self._position_size_in_lots is None and self._sl_in_money is None and self._sl_with_commission_in_money is not None:
            self._calculate_position_size_by_sl_with_commission_in_money()
        else:
            raise Exception("Only one of the position size in lots, stop loss in money or stop loss with commission in money is set.")

    def _calculate_position_size_by_sl_in_money(self):
        if self._quote_currency == self._target_currency:
            sl_in_quote = self._sl_in_money
        else:
            exchange_result = exchange_currency_by_rate(
                source_amount=self._sl_in_money,
                source_currency=self._target_currency,
                exchange_symbol=self._exchange_rate["symbol"],
                exchange_rate=self._exchange_rate["rate"],
            )
            sl_in_quote = exchange_result[0]

        position_size = sl_in_quote / (self._sl_in_pips * self._pip_value * self._lot_size)
        self._position_size_in_lots = position_size.quantize(Decimal('0.01'), rounding=ROUND_FLOOR)

    def _calculate_position_size_by_sl_with_commission_in_money(self):
        if self._quote_currency == self._target_currency:
            sl_with_commission_in_quote = self._sl_with_commission_in_money
        else:
            exchange_result = exchange_currency_by_rate(
                source_amount=self._sl_with_commission_in_money,
                source_currency=self._target_currency,
                exchange_symbol=self._exchange_rate["symbol"],
                exchange_rate=self._exchange_rate["rate"],
            )
            sl_with_commission_in_quote = exchange_result[0]

        position_size = sl_with_commission_in_quote / (self._sl_with_commission_in_pips * self._pip_value * self._lot_size)
        self._position_size_in_lots = position_size.quantize(Decimal('0.01'), rounding=ROUND_FLOOR)

    def _calculate_sl_in_money(self):
        sl_in_quote = abs(self._entry_price - self._sl_price) * self._lot_size * self._position_size_in_lots

        if self._quote_currency == self._target_currency:
            self._sl_in_money = sl_in_quote
        else:
            exchange_result = exchange_currency_by_rate(
                source_amount=sl_in_quote,
                source_currency=self._quote_currency,
                exchange_symbol=self._exchange_rate["symbol"],
                exchange_rate=self._exchange_rate["rate"],
            )
            self._sl_in_money = exchange_result[0]

    def _calculate_tp_in_money(self):
        tp_in_quote = abs(self._entry_price - self._tp_price) * self._lot_size * self._position_size_in_lots

        if self._quote_currency == self._target_currency:
            self._tp_in_money = tp_in_quote
        else:
            exchange_result = exchange_currency_by_rate(
                source_amount=tp_in_quote,
                source_currency=self._quote_currency,
                exchange_symbol=self._exchange_rate["symbol"],
                exchange_rate=self._exchange_rate["rate"],
            )
            self._tp_in_money = exchange_result[0]

    def _calculate_sl_with_commission_in_money(self):
        self._sl_with_commission_in_qoute = self._sl_with_commission_in_pips * self._pip_value * self._lot_size * self._position_size_in_lots

        if self._quote_currency == self._target_currency:
            self._sl_with_commission_in_money = self._sl_with_commission_in_qoute
        else:
            exchange_result = exchange_currency_by_rate(
                source_amount=self._sl_with_commission_in_qoute,
                source_currency=self._quote_currency,
                exchange_symbol=self._exchange_rate["symbol"],
                exchange_rate=self._exchange_rate["rate"],
            )
            self._sl_with_commission_in_money = exchange_result[0]

    def _calculate_tp_with_commission_in_money(self):
        self._tp_with_commission_in_qoute = self._tp_with_commission_in_pips * self._pip_value * self._lot_size * self._position_size_in_lots

        if self._quote_currency == self._target_currency:
            self._tp_with_commission_in_money = self._tp_with_commission_in_qoute
        else:
            exchange_result = exchange_currency_by_rate(
                source_amount=self._tp_with_commission_in_qoute,
                source_currency=self._quote_currency,
                exchange_symbol=self._exchange_rate["symbol"],
                exchange_rate=self._exchange_rate["rate"],
            )
            self._tp_with_commission_in_money = exchange_result[0]

    def get_results(self) -> dict:
        result = {
            "symbol": self._symbol,
            "base_currency": self._base_currency,
            "quote_currency": self._quote_currency,
            "pip_value": self._pip_value,
            "lot_size": self._lot_size,
            "target_currency": self._target_currency,
            "exchange_rate": {
                "symbol": self._exchange_rate["symbol"],
                "rate": self._exchange_rate["rate"],
            },
            "is_long": self._is_long,
            "position_size_in_lots": self._position_size_in_lots,
            "entry_price": self._entry_price,
            "sl_price": self._sl_price,
            "tp_price": self._tp_price,
            "commission_per_lot_in_pips": self._commission_per_lot_in_pips,
            "commission_per_lot_in_points": convert_pips_to_points(self._commission_per_lot_in_pips),
            "commission_per_lot_in_money": self._commission_per_lot_in_money,
            "rr_in_pips": {
                "sl_in_pips": self._sl_in_pips,
                "tp_in_pips": self._tp_in_pips,
            },
            "rr_in_points": {
                "sl_in_points": self._sl_in_points,
                "tp_in_points": self._tp_in_points,
            },
            "rr_in_money": {
                "sl_in_money": self._sl_in_money,
                "tp_in_money": self._tp_in_money,
            },
            "rrr": self._tp_in_pips / self._sl_in_pips,
            "rr_with_commission_in_pips": {
                "sl_with_commission_in_pips": self._sl_with_commission_in_pips,
                "tp_with_commission_in_pips": self._tp_with_commission_in_pips,
            },
            "rr_with_commission_in_points": {
                "sl_with_commission_in_points": self._sl_with_commission_in_points,
                "tp_with_commission_in_points": self._tp_with_commission_in_points,
            },
            "rr_with_commission_in_money": {
                "sl_with_commission_in_money": self._sl_with_commission_in_money,
                "tp_with_commission_in_money": self._tp_with_commission_in_money,
            },
            "rrr_with_commission": self._tp_with_commission_in_pips / self._sl_with_commission_in_pips,
        }

        return result
