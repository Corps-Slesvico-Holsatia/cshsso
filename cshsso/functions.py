"""Miscellaneous functions."""

from random import choices
from string import ascii_letters, digits
from typing import Any, Callable, Optional


__all__ = ['genpw', 'parse_or_none']


def genpw(*, pool: str = ascii_letters + digits, length: int = 16) -> str:
    """Generates a password."""

    return ''.join(choices(pool, k=length))


def parse_or_none(value: Optional[str], parser: Callable[[str], Any]) -> Any:
    """Parses a JSON value or returns None."""

    return None if value is None else parser(value)
