"""ORM-related functions."""

from contextlib import suppress
from typing import Optional

from flask import request
from peewee import JOIN
from wsgilib import JSONMessage

from cshsso.authorization import is_corps_member, is_in_inner_circle
from cshsso.constants import USER_ID
from cshsso.exceptions import InvalidPassword
from cshsso.functions import date_or_none
from cshsso.orm.models import Session, User, UserCommission
from cshsso.roles import Status


__all__ = [
    'get_user',
    'get_current_user',
    'user_to_json',
    'patch_user',
    'delete_user'
]


def get_user(uid: int) -> User:
    """Returns the destination user."""

    return User.select(User, UserCommission).join(
        UserCommission, on=UserCommission.occupant == User.id,
        join_type=JOIN.LEFT_OUTER
    ).where(
        User.id == uid
    ).group_by(User).get()


def get_current_user(session: Session, *, allow_other: bool = False) -> User:
    """Returns the current user."""

    if session.user.admin or allow_other:
        try:
            uid = int(request.cookies[USER_ID])
        except KeyError:
            return session.user

        return get_user(uid)

    return session.user


def user_to_json(user: User, *, actor: User) -> dict:
    """Returns the current user as JSON."""

    json = {
        'id': user.id,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'name_number': user.name_number,
        'status': user.status.to_json(),
        'registered': user.registered.isoformat(),
        'admin': user.admin,
        'bio': user.bio,
        'corps_list_number': user.corps_list_number,
        'acception': user.acception.isodormat() if user.acception else None,
        'reception': user.reception.isoformat() if user.reception else None,
        'commissions': [c.to_json() for c in user.commissions]
    }

    if actor.admin:
        json.update({
            'verified': user.verified,
            'locked': user.locked,
            'failed_logins': user.failed_logins
        })

    return json


def patch_user_admin(user: User, json: dict) -> None:
    """Patches a user from an admin context."""

    with suppress(KeyError):
        user.email = json['email']

    try:
        status = json['status']
    except KeyError:
        pass
    else:
        try:
            user.status = Status[status]
        except KeyError:
            raise JSONMessage('Invalid status provided.', status=400)

    with suppress(KeyError):
        user.verified = json['verified']

    with suppress(KeyError):
        user.locked = json['locked']

    with suppress(KeyError):
        user.failed_logins = json['failed_logins']

    with suppress(KeyError):
        user.admin = json['admin']


def patch_user_corps(user: User, json: dict) -> None:
    """Patches a user from an Corps member context."""

    with suppress(KeyError):
        user.name_number = json['name_number']

    with suppress(KeyError):
        user.acception = date_or_none(json['acception'])

    with suppress(KeyError):
        user.corps_list_number = json['corps_list_number']


def patch_user_inner_circle(user: User, json: dict) -> None:
    """Patches a user from an inner circle context."""

    with suppress(KeyError):
        user.reception = date_or_none(json['reception'])


def patch_user(user: User, json: dict, *, actor: User) -> User:
    """Patches the user."""

    with suppress(KeyError):
        user.first_name = json['first_name']

    with suppress(KeyError):
        user.last_name = json['last_name']

    with suppress(KeyError):
        user.bio = json['bio']

    if actor.admin:
        patch_user_admin(user, json)

    if actor.admin or is_corps_member(actor):
        patch_user_corps(user, json)

    if actor.admin or is_in_inner_circle(actor):
        patch_user_inner_circle(user, json)

    return user


def delete_user(user: User, *, actor: User,
                passwd: Optional[str] = None) -> bool:
    """Deletes the user."""

    if actor.admin and actor != user:
        return user.delete_instance()

    if passwd is not None and user.login(passwd):
        return user.delete_instance()

    raise InvalidPassword()
