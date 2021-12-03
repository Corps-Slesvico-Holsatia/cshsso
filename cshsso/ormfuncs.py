"""ORM-related functions."""

from peewee import JOIN

from cshsso.orm import User, UserCommission
from cshsso.roles import Commission


__all__ = ['get_user', 'pass_commission']


def get_user(uid: int) -> User:
    """Returns the destination user."""

    return User.select(User, UserCommission).join(
        UserCommission, on=UserCommission.user == User.id,
        join_type=JOIN.LEFT_OUTER).where(User.id == uid).group_by(User).get()


def can_pass_commission(user: User, commission: Commission) -> bool:
    """Checks whether the user can pass on the given commission."""

    return user.admin or user.has_commission(commission)


def pass_commission(commission: Commission, src: User, dst: User) -> bool:
    """Passes a commission from one user to another."""

    if not can_pass_commission(src, commission):
        return False

    # Delete all current user commissions to avoid duplicate occupants.
    for user_commission in UserCommission.select().where(
            UserCommission.commission == commission):
        user_commission.delete_instance()

    user_commission = UserCommission(occupant=dst, commission=commission)
    user_commission.save()
    return True
