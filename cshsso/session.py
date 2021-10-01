"""Manage sessions."""

from datetime import datetime, timedelta

from flask import request, Response

from cshsso.config import CONFIG
from cshsso.exceptions import NotLoggedIn
from cshsso.functions import genpw
from cshsso.localproxies import SESSION
from cshsso.orm import Account, Session


__all__ = ['get_session', 'create', 'renew', 'set_cookies']


DEFAULT_DURATION = 60 * 60      # One hour.
MAX_DURATION = 24 * 60 * 60     # One day.


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


def get_duration() -> timedelta:
    """Returns the session duration."""

    try:
        duration = int(request.cookies['cshsso-session-duration'])
    except (KeyError, ValueError):
        duration = CONFIG.getint('session', 'duration',
                                 fallback=DEFAULT_DURATION)

    return timedelta(seconds=min((duration, MAX_DURATION)))


def get_deadline() -> datetime:
    """Returns the session deadline."""

    return datetime.now() + get_duration()


def create(account: Account) -> tuple[int, str]:
    """Creates a new session for the given account."""

    password = genpw()
    session = Session(account=account, deadline=get_deadline(),
                      password=password)
    session.save()
    return (session.id, password)


def renew(session: Session) -> tuple[int, str]:
    """Renews the session and returns the new password."""

    session.password = password = genpw()
    session.deadline = get_deadline()
    session.save()
    return (session.id, password)


def set_cookies(response: Response) -> None:
    """Sets session cookies."""

    ident, password = renew(SESSION)
    response.set_cookie('cshsso-session-id', str(ident))
    response.set_cookie('cshsso-session-password', password)
