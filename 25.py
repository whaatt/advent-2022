# mypy: ignore-errors
# flake8: noqa

from functools import cache
from math import ceil


def snafu_to_decimal(snafu: str) -> int:
    base_five = (
        snafu.replace("2", "4")
        .replace("1", "3")
        .replace("0", "2")
        .replace("-", "1")
        .replace("=", "0")
    )
    decimal = int(base_five, 5)
    for power in range(len(snafu)):
        decimal -= 2 * (5**power)
    return decimal


@cache
def max_for_power(power):
    return sum(2 * (5**i) for i in range(power + 1))


def decimal_to_snafu(decimal: int) -> str:
    power = 0
    snafu = ""
    while decimal > max_for_power(power):
        power += 1
    while power >= 0:
        max_for_next = max_for_power(power - 1)
        if decimal == 0:
            snafu += "0"
        elif decimal > 0:
            units = int(ceil((decimal - max_for_next) / (5**power)))
            assert units <= 2
            decimal -= units * (5**power)
            snafu += "012"[units]
        else:
            units = int(ceil((-decimal - max_for_next) / (5**power)))
            assert units <= 2
            decimal += units * (5**power)
            snafu += "0-="[units]
        power -= 1
    assert decimal == 0
    return snafu


snafus = open("input.txt", "r").read().split("\n")
print(decimal_to_snafu(sum(snafu_to_decimal(snafu) for snafu in snafus)))
