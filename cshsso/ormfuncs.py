"""ORM-related functions."""

from peewee import JOIN

from cshsso.authorization import check_group
from cshsso.orm import User, UserCommission
from cshsso.roles import Commission, CommissionGroup, Status


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


def can_change_status(user: User) -> bool:
    """Checks whether the user can change status of arbitrary users."""

    return user.admin or check_group(user, CommissionGroup.CHARGES)


def set_status(status: Status, actor: User, target: User) -> bool:
    """Sets the status of the target user."""

    if not can_change_status(actor):
        return False

    target.status = status
    target.save()
    return True
