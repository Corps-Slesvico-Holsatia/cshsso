"""ORM-related functions."""

from peewee import JOIN

from cshsso.orm import User, UserCommission


__all__ = ['get_user']


def get_user(uid: int) -> User:
    """Returns the destination user."""

    return User.select(User, UserCommission).join(
        UserCommission, on=UserCommission.user == User.id,
        join_type=JOIN.LEFT_OUTER).where(User.id == uid).group_by(User).get()
