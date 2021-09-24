"""Miscellaneous functions."""

from random import choices
from string import ascii_letters, digits


__all__ = ['genpw']


def genpw(*, pool: str = ascii_letters + digits, length: int = 16) -> str:
    """Generates a password."""

    return ''.join(choices(pool, k=length))
