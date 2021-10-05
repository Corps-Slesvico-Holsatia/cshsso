"""Authorization checks."""

from cshsso.orm import User
from cshsso.roles import Group


__all__ = ['check_group_authorization']


def check_group_authorization(user: User, group: Group) -> bool:
    """Determines whether the user is authorized for the given group."""

    if group == Group.CHARGES:
        return any(charge in Group.CHARGES for charge in user.charges)

    if user.role in Group.INNER:
        return True

    if user.role in Group.OUTER:
        return group in {Group.OUTER, Group.GUEST}

    if user.role in Group.GUEST:
        return group == Group.GUEST

    return False
