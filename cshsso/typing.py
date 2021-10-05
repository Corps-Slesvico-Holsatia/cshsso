"""Common type hints."""

from typing import Callable

from flask import Response


__all__ = ['ErrorHandler', 'ErrorHandlers']


ErrorHandler = Callable[[Exception], Response]
ErrorHandlers = dict[type, ErrorHandler]
