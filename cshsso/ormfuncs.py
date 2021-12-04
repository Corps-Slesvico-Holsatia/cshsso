"""ORM-related functions."""

from contextlib import suppress
from typing import Iterable, Optional

from peewee import JOIN

from cshsso.exceptions import InvalidPassword
from cshsso.orm import Session, User, UserCommission
from cshsso.roles import Commission, Status


__all__ = ['get_user', 'get_user_as_json', 'patch_user', 'delete_user']


USER_PATCH_FIELDS = {'first_name', 'last_name'}


def get_user(uid: int) -> User:
    """Returns the destination user."""

    return User.select(User, UserCommission).join(
        UserCommission, on=UserCommission.occupant == User.id,
        join_type=JOIN.LEFT_OUTER).where(User.id == uid).group_by(User).get()


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
            user.acception = json['acception']

        with suppress(KeyError):
            user.reception = json['reception']

    with suppress(KeyError):
        user.first_name = json['first_name']

    with suppress(KeyError):
        user.last_name = json['last_name']


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
