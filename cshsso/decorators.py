"""Decorators for authentication and authorization."""

from __future__ import annotations
from enum import Enum
from functools import partial, wraps
from typing import Any

from cshsso.authorization import check_circle, check_convent, check_group
from cshsso.convents import ConventAuth
from cshsso.exceptions import NotAuthenticated, NotAuthorized
from cshsso.localproxies import USER, SESSION
from cshsso.roles import Circle, CommissionGroup
from cshsso.typing import AnyCallable, Decorator, NamedFunction


__all__ = ["authenticated", "admin", "Authorization"]


def authenticated(function: AnyCallable) -> AnyCallable:
    """Ensures authentication."""

    @wraps(function)
    def wrapper(*args, **kwargs) -> Any:
        if (user := SESSION.user).disabled:
            raise NotAuthenticated(
                user.verified, user.locked, user.failed_logins_exceeded
            )

        return function(*args, **kwargs)

    return wrapper


def authorized(check_func: NamedFunction) -> Decorator:
    """Determines whether the current user is authorized."""

    def decorator(function: AnyCallable) -> AnyCallable:
        @wraps(function)
        def wrapper(*args, **kwargs) -> Any:
            if USER.admin or check_func(USER):
                return function(*args, **kwargs)

            raise NotAuthorized(check_func.name)

        return wrapper

    return decorator


def admin(function: AnyCallable) -> AnyCallable:
    """Checks whether the user is an admin."""

    @wraps(function)
    def wrapper(*args, **kwargs) -> Any:
        if USER.admin:
            return function(*args, **kwargs)

        raise NotAuthorized("Admin")

    return wrapper


class Authorization(Enum):
    """Authorization modes."""

    # Circles
    INNER = partial(check_circle, circle=Circle.INNER)
    OUTER = partial(check_circle, circle=Circle.OUTER)
    GUESTS = partial(check_circle, circle=Circle.GUESTS)
    # Commissions
    CHARGES = partial(check_group, group=CommissionGroup.CHARGES)
    AHV = partial(check_group, group=CommissionGroup.AHV)
    # Convents
    AHC = partial(check_convent, convent=ConventAuth.AHC)
    AHC_VOTE = partial(check_convent, convent=ConventAuth.AHC_VOTE)
    CC = partial(check_convent, convent=ConventAuth.CC)
    CC_VOTE = partial(check_convent, convent=ConventAuth.CC_VOTE)
    FC = partial(check_convent, convent=ConventAuth.FC)
    FC_VOTE = partial(check_convent, convent=ConventAuth.FC_VOTE)
    FCC = partial(check_convent, convent=ConventAuth.FCC)
    FCC_VOTE = partial(check_convent, convent=ConventAuth.FCC_VOTE)

    def __call__(self, function: AnyCallable) -> AnyCallable:
        """Decorate the given function."""
        return authorized(NamedFunction(self.name, self.value))(function)

    @staticmethod
    def all(*authorizations: Authorization) -> Decorator:
        """Combine authorization checks via the all() function."""
        return authorized(
            NamedFunction(
                " & ".join(a.name for a in authorizations),
                lambda user: all(a.value(user) for a in authorizations),
            )
        )

    @staticmethod
    def any(*authorizations: Authorization) -> Decorator:
        """Combine authorization checks via any()."""
        return authorized(
            NamedFunction(
                " | ".join(a.name for a in authorizations),
                lambda user: any(a.value(user) for a in authorizations),
            )
        )
