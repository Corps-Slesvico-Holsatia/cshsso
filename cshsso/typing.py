"""Common type hints."""

from typing import Any, Callable

from flask import Response


__all__ = ['Decorator', 'ErrorHandler', 'ErrorHandlers']


Decorator = Callable[Callable[..., Any], Callable[..., Any]]
ErrorHandler = Callable[[Exception], Response]
ErrorHandlers = dict[type, ErrorHandler]
