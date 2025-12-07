from src.fx_calc import Calculator


calc = Calculator()
calc.set_symbol("EURUSD")
calc.set_position_size_in_lots(1.0)
calc.set_is_long(True)
calc.set_entry_price(1.2000)
calc.set_sl_price(1.1900)
calc.set_tp_price(1.2100)
calc.set_sl_in_pips(10)
calc.set_tp_in_pips(10)
calc.set_sl_in_points(10)
calc.set_tp_in_points(10)
calc.set_sl_in_money(10)
