"""Local proxies."""

from functools import partial

from flask import request
from peewee import JOIN
from werkzeug.local import LocalProxy

from cshsso.orm import Session, User, UserCommission
from cshsso.session import get_session


__all__ = ['SESSION', 'USER']


def get_user(session: Session) -> User:
    """Returns the current user."""

    if not session.user.admin:
        return session.user

    try:
        uid = request.cookies['cshsso-user-id']
    except KeyError:
        return session.user

    return User.select(User, UserCommission).join(
        UserCommission, on=UserCommission.user == User.id,
        join_type=JOIN.LEFT_OUTER).where(User.id == uid).get()


SESSION = LocalProxy(get_session)
USER = LocalProxy(partial(get_user, SESSION))
