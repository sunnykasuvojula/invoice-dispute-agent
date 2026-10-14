from decimal import Decimal

from invoice_agent.common.money import to_money, within_tolerance


def test_decimal_addition_is_exact():
    assert Decimal("0.1") + Decimal("0.2") == Decimal("0.3")
    assert 0.1 + 0.2 != 0.3          # floats get this wrong


def test_to_money_uses_two_decimal_places():
    assert str(to_money("10.5")) == "10.50"
    assert str(to_money("0")) == "0.00"
    assert to_money("-5.25") == Decimal("-5.25")


def test_to_money_rounds_to_cents():
    assert to_money("20.0449") == Decimal("20.04")
    assert to_money("20.045") == Decimal("20.05")     # half rounds up


def test_within_tolerance_boundary():
    assert within_tolerance(Decimal("10.50"), Decimal("10.55"), Decimal("0.05")) is True
    assert within_tolerance(Decimal("10.50"), Decimal("10.60"), Decimal("0.05")) is False


def test_chocolates_price_within_tolerance():
    assert within_tolerance(Decimal("20.04"), Decimal("20.00"), Decimal("0.05")) is True
    assert within_tolerance(Decimal("20.10"), Decimal("20.00"), Decimal("0.05")) is False