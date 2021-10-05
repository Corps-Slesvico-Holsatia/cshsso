"""Decorators for authentication and authorization."""

from configparser import ConfigParser
from enum import Enum
from functools import wraps
from typing import Any, Callable, Union

from flask import request
from recaptcha import verify

from cshsso.authorization import check_minimum_circle
from cshsso.authorization import check_commission_group
from cshsso.exceptions import NotAuthorized, NotLoggedIn
from cshsso.localproxies import USER, SESSION
from cshsso.roles import Circle, CommissionGroup
from cshsso.typing import Decorator


__all__ = ['authenticated', 'authorized', 'Authorization']


def authenticated(function: Callable[..., Any]) -> Callable[..., Any]:
    """Ensures authentication."""

    @wraps(function)
    def wrapper(*args, **kwargs) -> Any:
        if SESSION.active:
            return function(*args, **kwargs)

        raise NotLoggedIn()

    return wrapper


def authorized(target: Union[Circle, CommissionGroup]) -> Decorator:
    """Determines whether the current user is authorized."""

    if isinstance(target, Circle):
        check = check_minimum_circle
    elif isinstance(target, CommissionGroup):
        check = check_commission_group
    else:
        raise TypeError('Must specify either Circle or CommissionGroup.')

    def decorator(function: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(function)
        def wrapper(*args, **kwargs) -> Any:
            if check(USER, target):
                return function(*args, **kwargs)

            raise NotAuthorized()

        return wrapper

    return decorator


def recaptcha(config: ConfigParser, section: str = 'recaptcha') -> Decorator:
    """Decorator to run a function with previous recaptcha check."""

    def decorator(function: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(function)
        def wrapper(*args, **kwargs) -> Any:
            secret = config.get(section, 'secret')
            check_ip = config.get(section, 'check_ip', fallback=False)
            remote_ip = request.remote_addr if check_ip else None
            json_key = config.get(section, 'json_key', fallback='response')
            response = request.json.get(json_key)

            if verify(secret, response, remote_ip, fail_silently=True):
                return function(*args, **kwargs)

            raise NotAuthorized()

        return wrapper

    return decorator


class Authorization(Enum):
    """Authorization modes."""

    INNER = authorized(Circle.INNER)
    OUTER = authorized(Circle.OUTER)
    GUESTS = authorized(Circle.GUESTS)
    CHARGES = authorized(CommissionGroup.CHARGES)
    AHV = authorized(CommissionGroup.AHV)

    def __call__(self, *args, **kwargs) -> Any:
        """Delegate to decorator function."""
        return self.value(*args, **kwargs)
