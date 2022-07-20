"""CSH-SSO application base."""

from typing import Optional
from flask import Flask

from cshsso.config import CONFIG, CONFIG_FILE
from cshsso.errors import ERRORS
from cshsso.session import postprocess_response
from cshsso.typing import ErrorHandlers, Initializers, ResponseProcessor


__all__ = ['Application']


class Application(Flask):
    """Common CSH-SSO base application."""

    error_handlers = ERRORS
    initializers = {lambda: CONFIG.read(CONFIG_FILE)}
    post_processor = staticmethod(postprocess_response)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for exception, function in self.error_handlers.items():
            self.register_error_handler(exception, function)

        for initializer in self.initializers:
            self.before_first_request(initializer)

        self.after_request(self.post_processor)

    def __init_subclass__(
            cls,
            error_handlers: Optional[ErrorHandlers] = None,
            initializers: Optional[Initializers] = None,
            post_processor: Optional[ResponseProcessor] = None
    ):
        if error_handlers is not None:
            cls.error_handlers = {**cls.error_handlers, **error_handlers}

        if initializers:
            cls.initializers = {*cls.initializers, *initializers}

        if post_processor:
            cls.post_processor = post_processor
