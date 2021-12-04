"""Local proxies."""

from functools import partial

from flask import request
from werkzeug.local import LocalProxy

from cshsso.constants import USER_ID
from cshsso.orm import Session, User
from cshsso.ormfuncs import get_user
from cshsso.session import get_session


__all__ = ['SESSION', 'USER']


class ModelProxy(LocalProxy):
    """Extended local proxy for database models."""

    def __enter__(self):
        return self._get_current_object()

    def __exit__(self, typ, value, traceback):
        pass

    def __int__(self) -> int:
        return self._get_current_object()._pk


def get_current_user(session: Session) -> User:
    """Returns the current user."""

    if not session.user.admin:
        return session.user

    try:
        uid = int(request.cookies[USER_ID])
    except KeyError:
        return session.user

    return get_user(uid)


SESSION = ModelProxy(get_session)
USER = ModelProxy(partial(get_current_user, SESSION))
