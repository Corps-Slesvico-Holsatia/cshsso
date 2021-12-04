"""ORM-related functions."""

from contextlib import suppress
from datetime import date
from typing import Iterable, Optional

from flask import request
from peewee import JOIN

from cshsso.constants import USER_ID
from cshsso.exceptions import InvalidPassword
from cshsso.orm import Session, User, UserCommission
from cshsso.roles import Commission, Status


__all__ = [
    'get_user',
    'get_current_user',
    'get_user_as_json',
    'patch_user',
    'delete_user'
]


def get_user(uid: int) -> User:
    """Returns the destination user."""

    return User.select(User, UserCommission).join(
        UserCommission, on=UserCommission.occupant == User.id,
        join_type=JOIN.LEFT_OUTER).where(User.id == uid).group_by(User).get()


def get_current_user(session: Session, *, allow_other: bool = False) -> User:
    """Returns the current user."""

    if session.user.admin or allow_other:
        try:
            uid = int(request.cookies[USER_ID])
        except KeyError:
            return session.user

        return get_user(uid)

    return session.user


def get_user_as_json(session: Session, user: User) -> dict:
    """Returns the current user as JSON."""

    json = {
        'id': user.id,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'status': user.status.to_json(),
        'registered': user.registered.isoformat(),
        'acception': user.acception.isodormat() if user.acception else None,
        'reception': user.reception.isoformat() if user.reception else None,
        'commissions': [c.to_json() for c in user.commissions]
    }

    if session.user.admin:
        json.update({
            'verified': user.verified,
            'locked': user.locked,
            'failed_logins': user.failed_logins,
            'admin': user.admin
        })

    return json


def patch_user(session: Session, user: User, json: dict) -> User:
    """Patches the user."""

    if session.user.admin:
        with suppress(KeyError):
            user.email = json['email']

        with suppress(KeyError):
            user.status = Status.from_string(json['status'])

        with suppress(KeyError):
            user.verified = json['verified']

        with suppress(KeyError):
            user.locked = json['locked']

        with suppress(KeyError):
            user.failed_logins = json['failed_logins']

        with suppress(KeyError):
            user.admin = json['admin']

        with suppress(KeyError):
            user.acception = date.fromisoformat(json['acception'])

        with suppress(KeyError):
            user.reception = date.fromisoformat(json['reception'])

    with suppress(KeyError):
        user.first_name = json['first_name']

    with suppress(KeyError):
        user.last_name = json['last_name']

    return user


def delete_user(session: Session, user: User, *,
                passwd: Optional[str] = None) -> bool:
    """Deletes the user."""

    if (actor := session.user).admin and actor != user:
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
        user_commission = UserCommission(user=user, commission=commission)
        user_commission.save()
