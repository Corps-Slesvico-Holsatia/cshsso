"""Manage sessions."""

from datetime import datetime, timedelta

from argon2.exceptions import VerifyMismatchError
from flask import request, Response

from cshsso.config import CONFIG
from cshsso.exceptions import NotLoggedIn
from cshsso.functions import genpw
from cshsso.orm import User, Session


__all__ = ['get_session', 'create', 'for_user', 'renew', 'set_cookies']


DEFAULT_DURATION = 60 * 60      # One hour.
MAX_DURATION = 24 * 60 * 60     # One day.


def get_session() -> Session:
    """Returns the current session object."""

    try:
        session_id = request.cookies['cshsso-session-id']
        session_password = request.cookies['cshsso-session-passwd']
    except KeyError:
        raise NotLoggedIn() from None

    try:
        session = Session.select(Session, User).join(User).where(
            Session.id == session_id).get()
    except Session.DoesNotExist:
        raise NotLoggedIn() from None

    try:
        session.passwd.verify(session_password)
    except VerifyMismatchError:
        raise NotLoggedIn() from None

    return session


def get_duration() -> timedelta:
    """Returns the session duration."""

    try:
        duration = int(request.cookies['cshsso-session-duration'])
    except (KeyError, ValueError):
        duration = CONFIG.getint('session', 'duration',
                                 fallback=DEFAULT_DURATION)

    return timedelta(seconds=min([duration, MAX_DURATION]))


def get_deadline() -> datetime:
    """Returns the session deadline."""

    return datetime.now() + get_duration()


def create(user: User, deadline: datetime) -> tuple[Session, str]:
    """Opens a new session for the given user."""

    session = Session(user=user, deadline=deadline, passwd=(passwd := genpw()))
    return (session, passwd)


def for_user(user: User, deadline: datetime) -> tuple[Session, str]:
    """Returns a session and a session password for the given user."""

    sessions = set()

    for session in Session.select().where(Session.user == user):
        if session.active:
            sessions.add(session)
        else:
            session.delete_instance()

    try:
        *old, last = sessions
    except ValueError:
        return create(user=user, deadline=deadline)

    for session in old:
        session.delete_instance()

    return (last, last.renew(deadline))


def renew(session: Session) -> tuple[Session, str]:
    """Renews the session and returns the new password."""

    session.passwd = passwd = genpw()
    session.deadline = get_deadline()
    session.save()
    return (session, passwd)


def set_cookies(response: Response, session: Session) -> None:
    """Sets session cookies."""

    session, passwd = renew(session)
    response.set_cookie('cshsso-session-id', str(session.id))
    response.set_cookie('cshsso-session-passwd', passwd)
