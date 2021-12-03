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


def pass_commission(commission: Commission, src: User, dst: User) -> bool:
    """Passes a commission from one user to another."""

    try:
        src_commission = UserCommission.get(UserCommission.occupant == src.id)
    except UserCommission.DoesNotExist:
        src_commission = None

    if src_commission is None and not src.admin:
        return False

    dst_commission = UserCommission(occupant=dst, commission=commission)
    dst_commission.save()

    if src_commission is not None:
        src_commission.delete_instance()

    return True
