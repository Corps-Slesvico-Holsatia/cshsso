"""Authorization checks."""

from typing import Union

from cshsso.orm import User
from cshsso.roles import Circle, CommissionGroup


__all__ = ['check_minimum_circle', 'check_commission_group', 'check_target']


def is_in_inner_circle(user: User) -> bool:
    """Checks whether the user is member of the inner circle."""

    return user.status in Circle.INNER


def is_in_outer_circle(user: User) -> bool:
    """Checks whether the user is member of the outer circle."""

    return user.status in Circle.OUTER


def is_guest(user: User) -> bool:
    """Checks whether the user is a guest."""

    return user.status in Circle.GUESTS


def check_minimum_circle(user: User, circle: Circle) -> bool:
    """Determines whether the user is authorized for the given group."""

    if circle is Circle.INNER:
        return is_in_inner_circle(user)

    if circle is Circle.OUTER:
        return is_in_inner_circle(user) or is_in_outer_circle(user)

    if circle is Circle.GUESTS:
        return True

    return False


def check_commission_group(user: User, group: CommissionGroup) -> bool:
    """Checks whether the user is charged."""

    return any(uc.commission in group for uc in user.commissions)


def check_target(user: User, target: Union[Circle, CommissionGroup]) -> bool:
    """Checks a user against a Corps circle or commission group."""

    if isinstance(target, Circle):
        return check_minimum_circle(user, target)

    if isinstance(target, CommissionGroup):
        return check_commission_group(user, target)

    raise TypeError('Must specify either Circle or CommissionGroup.')
