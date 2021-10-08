"""Manage sessions."""

from datetime import datetime, timedelta
from typing import Optional

from argon2.exceptions import VerifyMismatchError
from flask import request, Response
from peewee import JOIN

from cshsso.config import CONFIG
from cshsso.exceptions import NotLoggedIn
from cshsso.functions import genpw
from cshsso.orm import User, Session, UserCommission


__all__ = ['get_session', 'create', 'for_user', 'set_cookies']


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
        session = Session.select(Session, User, UserCommission).join(
            User).join(UserCommission, on=UserCommission.user == User.id,
                       join_type=JOIN.LEFT_OUTER).where(
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


def set_cookies(response: Response, session: Session, *,
                passwd: Optional[str] = None) -> Response:
    """Sets session cookies."""

    if passwd is None:
        passwd = session.renew()

    for domain in CONFIG.get('session', 'domains').split():
        response.set_cookie('cshsso-session-id', str(session.id),
                            domain=domain, secure=True, samesite=None)
        response.set_cookie('cshsso-session-passwd', passwd,
                            domain=domain, secure=True, samesite=None)
    return response


def terminate(response: Response) -> Response:
    """Terminates the given session."""

    for domain in CONFIG.get('session', 'domains').split():
        response.delete_cookie('cshsso-session-id', domain=domain)
        response.delete_cookie('cshsso-session-passwd', domain=domain)
