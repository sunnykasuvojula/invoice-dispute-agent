from decimal import Decimal, ROUND_HALF_UP
CENT =Decimal("0.01")
def to_money(value:str):
    return Decimal(value).quantize(CENT,rounding=ROUND_HALF_UP)

to_money("10.50")
print(to_money("10.50"))  # Output: 10.50


def within_tolerance(a:Decimal, b:Decimal, tolerance:Decimal):
    return abs(a - b) <= tolerance

print(within_tolerance(Decimal("10.50"), Decimal("10.55"), Decimal("0.05")))  # Output: True