"""Common type hints."""

from typing import Callable, NamedTuple

from flask import Response

from cshsso.orm import Session


__all__ = ['ErrorHandler', 'ErrorHandlers', 'NewSession']


ErrorHandler = Callable[[Exception], Response]
ErrorHandlers = dict[type, ErrorHandler]


class NewSession(NamedTuple):
    """Representas a new session with its password in clear text."""

    session: Session
    passwd: str
