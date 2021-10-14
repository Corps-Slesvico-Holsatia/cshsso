"""Decorators for authentication and authorization."""

from enum import Enum
from functools import wraps
from typing import Any, Callable, Union

from cshsso.authorization import check_target
from cshsso.exceptions import NotAuthenticated, NotAuthorized
from cshsso.localproxies import USER, SESSION
from cshsso.roles import Circle, CommissionGroup
from cshsso.typing import Decorator


__all__ = ['authenticated', 'authorized', 'admin', 'Authorization']


def authenticated(function: Callable[..., Any]) -> Callable[..., Any]:
    """Ensures authentication."""

    @wraps(function)
    def wrapper(*args, **kwargs) -> Any:
        if (user := SESSION.user).verified and not user.locked:
            return function(*args, **kwargs)

        raise NotAuthenticated()

    return wrapper


def authorized(target: Union[Circle, CommissionGroup]) -> Decorator:
    """Determines whether the current user is authorized."""

    def decorator(function: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(function)
        def wrapper(*args, **kwargs) -> Any:
            if check_target(USER, target):
                return function(*args, **kwargs)

            raise NotAuthorized()

        return wrapper

    return decorator


def admin(function: Callable[..., Any]) -> Callable[..., Any]:
    """Checks whether the user is an admin."""

    @wraps(function)
    def wrapper(*args, **kwargs) -> Any:
        if USER.admin:
            return function(*args, **kwargs)

        raise NotAuthorized()

    return wrapper


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
