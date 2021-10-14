"""Miscellaneous functions."""

from datetime import date
from functools import partial
from random import choices
from string import ascii_letters, digits
from typing import Any, Callable, Optional


__all__ = ['genpw', 'parse_or_none', 'date_or_none']


def genpw(*, pool: str = ascii_letters + digits, length: int = 16) -> str:
    """Generates a password."""

    return ''.join(choices(pool, k=length))


def parse_or_none(value: Optional[str], parser: Callable[[str], Any]) -> Any:
    """Parse a value or return None."""

    return None if value is None else parser(value)


date_or_none = partial(parse_or_none, parser=date.isoformat)
