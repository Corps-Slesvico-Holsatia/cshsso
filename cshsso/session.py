"""Manage sessions."""

from flask import request

from cshsso.exceptions import NotLoggedIn
from cshsso.orm import Account, Session


__all__ = ['get_session']


def get_session() -> Session:
    """Returns the current session object."""

    try:
        session_id = request.cookies['cshsso-session-id']
        session_password = request.cookies['cshsso-session-password']
    except KeyError:
        raise NotLoggedIn() from None

    try:
        session = Session.select(Session, Account).join(Account).where(
            Session.id == session_id).get()
    except Session.DoesNotExist:
        raise NotLoggedIn() from None

    if session.password.verify(session_password):
        return session

    raise NotLoggedIn()
