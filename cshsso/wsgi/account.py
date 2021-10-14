"""Manage accounts."""

from datetime import date
from typing import Optional

from flask import request

from wsgilib import JSON, JSONMessage

from cshsso.decorators import authenticated, Authorization
from cshsso.exceptions import InvalidPassword
from cshsso.localproxies import SESSION, USER
from cshsso.orm import Session, User, UserCommission
from cshsso.roles import Commission, Status


__all__ = [
    'show',
    'patch',
    'delete',
    'set_acception',
    'set_reception',
    'set_status',
    'set_commissions'
]


USER_VIEW_FIELDS = {
    'email', 'first_name', 'last_name', 'status', 'registered', 'acception',
    'reception'
}
USER_PATCH_FIELDS = {'first_name', 'last_name'}


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


@authenticated
def show() -> JSON:
    """Shows the user's profile."""

    return JSON(get_user_as_json(SESSION, USER))


@authenticated
def patch() -> JSONMessage:
    """Updates the user's profile."""

    user = patch_user(SESSION, USER, request.json)
    user.save()
    return JSONMessage('User patched.', status=200)


@authenticated
def delete() -> JSONMessage:
    """Deletes the user's account."""

    delete_user(SESSION, USER, passwd=request.json.get('passwd'))
    return JSONMessage('User deleted.', status=200)


@authenticated
@Authorization.OUTER
def set_acception() -> JSONMessage:
    """Set the acception date."""

    user = USER._get_current_object()   # pylint: disable=W0212

    try:
        acception = request.json['acception']
    except KeyError:
        return JSONMessage('No acception date provided.', status=400)

    if acception is not None:
        try:
            acception = date.fromisoformat(acception)
        except ValueError:
            return JSONMessage('Invalid acception date provided.', status=400)

    user.acception = acception
    user.save()
    return JSONMessage('Acception date set.', status=200)


@authenticated
@Authorization.INNER
def set_reception() -> JSONMessage:
    """Set the reception date."""

    user = USER._get_current_object()   # pylint: disable=W0212

    try:
        reception = request.json['reception']
    except KeyError:
        return JSONMessage('No reception date provided.', status=400)

    if reception is not None:
        try:
            reception = date.fromisoformat(reception)
        except ValueError:
            return JSONMessage('Invalid reception date provided.', status=400)

    user.reception = reception
    user.save()
    return JSONMessage('Reception date set.', status=200)


@authenticated
@Authorization.CHARGES
def set_status() -> JSONMessage:
    """Sets the status of a user."""

    try:
        status = Status[request.json['status']]
    except KeyError:
        return JSONMessage('No status provied.', status=400)
    except ValueError:
        return JSONMessage('Invalid status provied.', status=400)

    user = USER._get_current_object()   # pylint: disable=W0212
    old_status, user.status = user.status, status
    user.save()
    return JSONMessage('Status updated.', old=old_status.name, new=status.name,
                       status=200)


@authenticated
@Authorization.CHARGES
def set_commissions() -> JSONMessage:
    """Sets the commissions for a user."""

    try:
        commissions = {Commission[c] for c in request.json['commissions']}
    except KeyError:
        return JSONMessage('No commissions provied.', status=400)
    except ValueError:
        return JSONMessage('Invalid commission provied.', status=400)

    user = USER._get_current_object()   # pylint: disable=W0212
    old_commissions = set()

    for user_commission in user.commissions:
        old_commissions.add(user_commission.commission)
        user_commission.delete_instance()

    for commission in commissions:
        user_commission = UserCommission(user=user, commission=commission)
        user_commission.save()

    return JSONMessage('Commissions updated.',
                       old={c.name for c in old_commissions},
                       new={c.name for c in commissions},
                       status=200)
