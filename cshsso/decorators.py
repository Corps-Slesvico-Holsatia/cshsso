"""Decorators for authentication and authorization."""

from enum import Enum
from functools import partial, wraps
from typing import Any, Callable

from cshsso.authorization import check_circle, check_convent, check_group
from cshsso.convents import ConventAuthorization
from cshsso.exceptions import NotAuthenticated, NotAuthorized
from cshsso.localproxies import USER, SESSION
from cshsso.orm import User
from cshsso.roles import Circle, CommissionGroup
from cshsso.typing import Decorator


__all__ = ['authenticated', 'admin', 'Authorization']


def authenticated(function: Callable[..., Any]) -> Callable[..., Any]:
    """Ensures authentication."""

    @wraps(function)
    def wrapper(*args, **kwargs) -> Any:
        if (user := SESSION.user).verified and not user.disabled:
            return function(*args, **kwargs)

        raise NotAuthenticated(user.verified, user.locked)

    return wrapper


def authorized(check_func: partial[[User], bool]) -> Decorator:
    """Determines whether the current user is authorized."""

    def decorator(function: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(function)
        def wrapper(*args, **kwargs) -> Any:
            if check_func(USER):
                return function(*args, **kwargs)

            raise NotAuthorized(list(check_func.keywords.values())[0].name)

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
    INNER = authorized(partial(check_circle, circle=Circle.INNER))
    OUTER = authorized(partial(check_circle, circle=Circle.OUTER))
    GUESTS = authorized(partial(check_circle, circle=Circle.GUESTS))
    # Commissions
    CHARGES = authorized(partial(check_group, group=CommissionGroup.CHARGES))
    AHV = authorized(partial(check_group, group=CommissionGroup.AHV))
    # Convents
    AHC = authorized(partial(check_convent, convent=ConventAuthorization.AHC))
    AHC_VOTE = authorized(
        partial(check_convent, convent=ConventAuthorization.AHC_VOTE))
    CC = authorized(partial(check_convent, convent=ConventAuthorization.CC))
    CC_VOTE = authorized(
        partial(check_convent, convent=ConventAuthorization.CC_VOTE))
    FC = authorized(partial(check_convent, convent=ConventAuthorization.FC))
    FC_VOTE = authorized(
        partial(check_convent, convent=ConventAuthorization.FC_VOTE))
    FCC = authorized(partial(check_convent, convent=ConventAuthorization.FCC))
    FCC_VOTE = authorized(
        partial(check_convent, convent=ConventAuthorization.FCC_VOTE))

    def __call__(self, *args, **kwargs) -> Any:
        """Delegate to decorator function."""
        return self.value(*args, **kwargs)
