"""Authorization checks."""

from cshsso.orm import Account
from cshsso.roles import Group


__all__ = ['is_authorized']


def is_authorized(account: Account, group: Group) -> bool:
    """Determines whether the account is authorized for the given group."""

    if account.group == Group.INNER:
        return True

    if account.group == Group.OUTER:
        return group in {Group.OUTER, Group.GUEST}

    return group == Group.GUEST
