"""Manage sessions."""

from datetime import datetime, timedelta

from argon2.exceptions import VerifyMismatchError
from flask import request, Response
from peewee import JOIN
from werkzeug.http import dump_cookie

from cshsso.config import CONFIG
from cshsso.exceptions import NotLoggedIn
from cshsso.functions import genpw
from cshsso.orm import User, Session, UserCommission


__all__ = [
    'get_session',
    'create',
    'for_user',
    'set_session_cookie',
    'delete_session_cookie',
    'postprocess_response'
]


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


def set_cookie(response: Response, *args, **kwargs):
    """A workaround for explicitly setting SameSite to None
    Until the following fix is released:
    https://github.com/pallets/werkzeug/issues/1549
    """

    cookie = dump_cookie(*args, **kwargs)

    if 'samesite' in kwargs and kwargs['samesite'] is None:
        cookie = f'{cookie}; SameSite=None'

    response.headers.add('Set-Cookie', cookie)


def set_session_cookie(response: Response, session: Session,
                       secret: str = None) -> Response:
    """Sets the session cookie."""

    secret = session.renew() if secret is None else secret

    for domain in CONFIG.get('auth', 'domains').split():
        set_cookie(
            response, 'cshsso-session-id', str(session.id),
            expires=session.end, domain=domain, secure=True, samesite=None)
        set_cookie(
            response, 'cshsso-session-secret', secret,
            expires=session.end, domain=domain, secure=True, samesite=None)

    return response


def delete_session_cookie(response: Response) -> Response:
    """Deletes the session cookie."""

    for domain in CONFIG.get('auth', 'domains').split():
        response.delete_cookie('cshsso-session-id', domain=domain)
        response.delete_cookie('cshsso-session-secret', domain=domain)

    return response


def postprocess_response(response: Response) -> Response:
    """Sets the session cookie on the respective response."""

    # Do not override an already set session cookie i.e. on deletion.
    if 'Set-Cookie' in response.headers:
        return response

    try:
        session = get_session()
    except NotLoggedIn:
        return delete_session_cookie(response)

    return set_session_cookie(response, session)
