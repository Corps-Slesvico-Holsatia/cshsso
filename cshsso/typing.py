"""Common type hints."""

from typing import Any, Callable, NamedTuple

from flask import Response


__all__ = [
    'AnyCallable',
    'Decorator',
    'ErrorHandler',
    'ErrorHandlers',
    'SessionCredentials'
]


AnyCallable = Callable[..., Any]
Decorator = Callable[[AnyCallable], AnyCallable]
ErrorHandler = Callable[[Exception], Response]
ErrorHandlers = dict[type, ErrorHandler]


class SessionCredentials(NamedTuple):
    """Represents session ID and secret."""

    id: int
    secret: str
