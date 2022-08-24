"""Roman numerals conversion."""

from typing import Iterator


__all__ = ['roman']


NUMERALS = {
    1000: 'M',
    900: 'CM',
    500: 'D',
    400: 'CD',
    100: 'C',
    90: 'XC',
    50: 'L',
    40: 'XL',
    10: 'X',
    9: 'IX',
    5: 'V',
    4: 'IV',
    1: 'I'
}


def roman(number: int) -> str:
    """Convert an integer to roman numerals."""

    if number <= 0:
        raise ValueError(
            'Cannot convert non-positive number to roman numerals:',
            number
        )

    return ''.join(iter_numerals(number))


def iter_numerals(number: int) -> Iterator[str]:
    """Yield roman numerals of the number."""

    while number:
        for integer, numeral in NUMERALS.items():
            if integer <= number:
                number -= integer
                yield numeral
                break
