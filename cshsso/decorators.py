"""Decorators for authentication and authorization."""

from functools import wraps
from typing import Any, Callable

from cshsso.authorization import is_authorized
from cshsso.exceptions import NotAuthorized, NotLoggedIn
from cshsso.localproxies import ACCOUNT, SESSION
from cshsso.roles import Group


__all__ = ['authenticated', 'authorized']


Decorator = Callable[Callable[..., Any], Callable[..., Any]]


def authenticated(function: Callable[..., Any]) -> Callable[..., Any]:
    """Ensures authentication."""

    @wraps(function)
    def wrapper(*args, **kwargs) -> Any:
        if SESSION.active:
            return function(*args, **kwargs)

        raise NotLoggedIn()

    return wrapper


def authorized(group: Group) -> Decorator:
    """Determines whether the current account is authorized."""

    def decorator(function: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(function)
        def wrapper(*args, **kwargs) -> Any:
            if is_authorized(ACCOUNT, group):
                return function(*args, **kwargs)

            raise NotAuthorized()

        return wrapper

    return decorator
