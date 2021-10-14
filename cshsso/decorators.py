"""Decorators for authentication and authorization."""

from enum import Enum
from functools import wraps
from typing import Any, Callable

from cshsso.authorization import AuthorizationTarget, check_target
from cshsso.convents import Convent, ConventAuthorization
from cshsso.exceptions import NotAuthenticated, NotAuthorized
from cshsso.localproxies import USER, SESSION
from cshsso.roles import Circle, CommissionGroup
from cshsso.typing import Decorator


__all__ = ['authenticated', 'authorized', 'admin', 'Authorization']


def authenticated(function: Callable[..., Any]) -> Callable[..., Any]:
    """Ensures authentication."""

    @wraps(function)
    def wrapper(*args, **kwargs) -> Any:
        if (user := SESSION.user).verified and not user.disabled:
            return function(*args, **kwargs)

        raise NotAuthenticated(user.verified, user.locked)

    return wrapper


def authorized(target: AuthorizationTarget) -> Decorator:
    """Determines whether the current user is authorized."""

    def decorator(function: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(function)
        def wrapper(*args, **kwargs) -> Any:
            if check_target(USER, target):
                return function(*args, **kwargs)

            raise NotAuthorized(target.name)

        return wrapper

    return decorator


def admin(function: Callable[..., Any]) -> Callable[..., Any]:
    """Checks whether the user is an admin."""

    @wraps(function)
    def wrapper(*args, **kwargs) -> Any:
        if USER.admin:
            return function(*args, **kwargs)

        raise NotAuthorized('Admin')

    return wrapper


class Authorization(Enum):
    """Authorization modes."""

    # Circles
    INNER = authorized(Circle.INNER)
    OUTER = authorized(Circle.OUTER)
    GUESTS = authorized(Circle.GUESTS)
    # Commissions
    CHARGES = authorized(CommissionGroup.CHARGES)
    AHV = authorized(CommissionGroup.AHV)
    # Convents
    AHC = authorized(ConventAuthorization(Convent.AHC))
    AHC_VOTE = authorized(ConventAuthorization(Convent.AHC, True))
    CC = authorized(ConventAuthorization(Convent.CC))
    CC_VOTE = authorized(ConventAuthorization(Convent.CC, True))
    FC = authorized(ConventAuthorization(Convent.FC))
    FC_VOTE = authorized(ConventAuthorization(Convent.FC, True))
    FCC = authorized(ConventAuthorization(Convent.FCC))
    FCC_VOTE = authorized(ConventAuthorization(Convent.FCC, True))

    def __call__(self, *args, **kwargs) -> Any:
        """Delegate to decorator function."""
        return self.value(*args, **kwargs)
