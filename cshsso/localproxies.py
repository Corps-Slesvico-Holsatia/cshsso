"""Local proxies."""

from functools import partial

from flask import request
from werkzeug.local import LocalProxy

from cshsso.orm import Session, User
from cshsso.ormfuncs import get_user
from cshsso.session import get_session


__all__ = ['SESSION', 'USER']


def get_current_user(session: Session) -> User:
    """Returns the current user."""

    if not session.user.admin:
        return session.user

    try:
        uid = int(request.cookies['cshsso-user-id'])
    except KeyError:
        return session.user

    return get_user(uid)


SESSION = LocalProxy(get_session)
USER = LocalProxy(partial(get_current_user, SESSION))
