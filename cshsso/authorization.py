"""Authorization checks."""

from cshsso.orm import User
from cshsso.roles import Group


__all__ = ['is_authorized']


def is_authorized(user: User, group: Group) -> bool:
    """Determines whether the account is authorized for the given group."""

    if user.group == Group.INNER:
        return True

    if user.group == Group.OUTER:
        return group in {Group.OUTER, Group.GUEST}

    return group == Group.GUEST
