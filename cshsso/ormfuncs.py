"""ORM-related functions."""

from typing import Iterable, Optional

from peewee import JOIN

from cshsso.exceptions import InvalidPassword
from cshsso.orm import Session, User, UserCommission
from cshsso.roles import Commission


__all__ = ['get_user', 'get_user_as_json', 'patch_user', 'delete_user']


USER_VIEW_FIELDS = {
    'email', 'first_name', 'last_name', 'status', 'registered', 'acception',
    'reception'
}
USER_PATCH_FIELDS = {'first_name', 'last_name'}


def get_user(uid: int) -> User:
    """Returns the destination user."""

    return User.select(User, UserCommission).join(
        UserCommission, on=UserCommission.user == User.id,
        join_type=JOIN.LEFT_OUTER).where(User.id == uid).group_by(User).get()


def get_user_as_json(session: Session, user: User) -> dict:
    """Returns the current user as JSON."""

    if session.user.admin:
        return user.to_json()

    return user.to_json(only=USER_VIEW_FIELDS)


def patch_user(session: Session, user: User, json: dict) -> User:
    """Patches the user."""

    if session.user.admin:
        return user.patch_json(json).save()

    return user.patch_json(json, only=USER_PATCH_FIELDS).save()


def delete_user(session: Session, user: User, *,
                passwd: Optional[str] = None) -> bool:
    """Deletes the user."""

    if session.user.admin:
        return user.delete_instance()

    if passwd is not None and user.login(passwd):
        return user.delete_instance()

    raise InvalidPassword()


def set_commissions(user: User, commissions: Iterable[Commission]) -> None:
    """Sets the commissions of the user."""

    current = user.user_commissions
    new = {c for c in commissions if c not in {c.commission for c in current}}
    delete = {uc for uc in current if uc.commission not in commissions}

    for user_commission in delete:
        user_commission.delete_instance()

    for commission in new:
        user_commission = UserCommission(user=user.id, commission=commission)
        user_commission.save()
