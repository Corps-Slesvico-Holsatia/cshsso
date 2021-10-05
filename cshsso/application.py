"""CSH-SSO application base."""

from flask import Flask

from cshsso.errors import ERRORS
from cshsso.typing import ErrorHandlers


__all__ = ['Application']


class Application(Flask):
    """Common CSH-SSO base application."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register_error_handlers(ERRORS)

    def register_error_handlers(self, handlers: ErrorHandlers) -> None:
        """Add error handlers."""
        for exception, function in handlers.items():
            self.register_error_handler(exception, function)
