"""Common type hints."""

from typing import Any, Callable, NamedTuple

from flask import Response


__all__ = ['Decorator', 'ErrorHandler', 'ErrorHandlers', 'SessionCredentials']


Decorator = Callable[[Callable[..., Any]], Callable[..., Any]]
ErrorHandler = Callable[[Exception], Response]
ErrorHandlers = dict[type, ErrorHandler]


class SessionCredentials(NamedTuple):
    """Represents session ID and secret."""

    id: int
    secret: str
