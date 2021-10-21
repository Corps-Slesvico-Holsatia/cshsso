"""Miscellaneous functions."""

from datetime import date
from functools import partial
from secrets import choice
from string import ascii_letters, digits
from typing import Any, Callable, Optional


__all__ = ['genpw', 'parse_or_none', 'date_or_none']


def genpw(*, pool: str = ascii_letters + digits, length: int = 16) -> str:
    """Generates a password."""

    return ''.join(choice(pool) for _ in range(length))


def parse_or_none(value: Optional[str], parser: Callable[[str], Any]) -> Any:
    """Parse a value or return None."""

    return None if value is None else parser(value)


date_or_none = partial(parse_or_none, parser=date.fromisoformat)
