"""Manage accounts."""

from flask import request

from wsgilib import JSON, JSONMessage

from cshsso.decorators import authenticated, Authorization
from cshsso.functions import date_or_none
from cshsso.localproxies import SESSION, USER
from cshsso.ormfuncs import delete_user
from cshsso.ormfuncs import get_user_as_json
from cshsso.ormfuncs import patch_user
from cshsso.ormfuncs import set_commissions as _set_commissions
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
        user.acception = date_or_none(request.json['acception'])
    except KeyError:
        return JSONMessage('No acception date provided.', status=400)
    except ValueError:
        return JSONMessage('Invalid acception date provided.', status=400)

    user.save()
    return JSONMessage('Acception date set.', status=200)


@authenticated
@Authorization.INNER
def set_reception() -> JSONMessage:
    """Set the reception date."""

    user = USER._get_current_object()   # pylint: disable=W0212

    try:
        user.reception = date_or_none(request.json['reception'])
    except KeyError:
        return JSONMessage('No reception date provided.', status=400)
    except ValueError:
        return JSONMessage('Invalid reception date provided.', status=400)

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

    _set_commissions(USER, commissions)
    return JSONMessage('Commissions updated.',
                       commissions={c.to_json() for c in commissions},
                       status=200)
