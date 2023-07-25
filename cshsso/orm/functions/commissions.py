"""Commissions-related functions."""

from typing import Iterable

from cshsso.orm.models import Commission, User, UserCommission


__all__ = ["set_commissions"]


def set_commissions(user: User, commissions: Iterable[Commission]) -> None:
    """Sets the commissions of the user."""

    current = user.user_commissions
    new = {c for c in commissions if c not in {c.commission for c in current}}
    delete = {uc for uc in current if uc.commission not in commissions}

    for user_commission in delete:
        user_commission.delete_instance()

    for commission in new:
        user_commission = UserCommission(user=user, commission=commission)
        user_commission.save()
