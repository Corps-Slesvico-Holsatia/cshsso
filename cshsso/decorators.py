"""Decorators for authentication and authorization."""

from functools import wraps
from typing import Any, Callable, Union

from cshsso.authorization import check_minimum_circle
from cshsso.authorization import check_commission_group
from cshsso.exceptions import NotAuthorized, NotLoggedIn
from cshsso.localproxies import USER, SESSION
from cshsso.roles import Circle, CommissionGroup
from cshsso.typing import Decorator


__all__ = [
    'authenticated',
    'authorized',
    'inner',
    'outer',
    'guests',
    'charged',
    'ahv'
]


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


inner = authorized(Circle.INNER)
outer = authorized(Circle.OUTER)
guests = authorized(Circle.GUESTS)
charged = authorized(CommissionGroup.CHARGES)
ahv = authorized(CommissionGroup.AHV)
