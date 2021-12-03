"""CSH-SSO application base."""

from flask import Flask

from cshsso.config import CONFIG, CONFIG_FILE
from cshsso.errors import ERRORS
from cshsso.session import postprocess_response
from cshsso.typing import ErrorHandlers


__all__ = ['Application']


class Application(Flask):
    """Common CSH-SSO base application."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register_error_handlers(ERRORS)
        self.before_first_request(lambda: CONFIG.read(CONFIG_FILE))
        self.after_request(postprocess_response)

    def register_error_handlers(self, handlers: ErrorHandlers) -> None:
        """Add error handlers."""
        for exception, function in handlers.items():
            self.register_error_handler(exception, function)
