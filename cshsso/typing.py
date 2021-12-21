"""Common type hints."""

from __future__ import annotations
from typing import Any, Callable, NamedTuple

from flask import Response


__all__ = [
    'AnyCallable',
    'Decorator',
    'ErrorHandler',
    'ErrorHandlers',
    'NamedFunction',
    'SessionCredentials'
]


AnyCallable = Callable[..., Any]
Decorator = Callable[[AnyCallable], AnyCallable]
ErrorHandler = Callable[[Exception], Response]
ErrorHandlers = dict[type, ErrorHandler]


class NamedFunction(NamedTuple):
    """A function with a given name."""

    name: str
    function: AnyCallable

    def __call__(self, *args, **kwargs) -> Any:
        """Calls the function."""
        return self.function(*args, **kwargs)


class SessionCredentials(NamedTuple):
    """Represents session ID and secret."""

    id: int
    secret: str
