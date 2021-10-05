"""Common type hints."""

from typing import Callable

from flask import Response


__all__ = ['ErrorHandlers']


ErrorHandlers = dict[type, Callable[[Exception], Response]]
