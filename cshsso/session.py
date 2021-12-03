"""Manage sessions."""

from argon2.exceptions import VerifyMismatchError
from flask import request, Response
from peewee import JOIN
from werkzeug.http import dump_cookie

from cshsso.config import CONFIG
from cshsso.constants import SESSION_ID, SESSION_SECRET
from cshsso.exceptions import NotLoggedIn
from cshsso.functions import genpw
from cshsso.orm import User, Session, UserCommission


__all__ = [
    'get_session',
    'for_user',
    'set_session_cookies',
    'delete_session_cookies',
    'postprocess_response'
]


def get_session() -> Session:
    """Returns the current session object."""

    try:
        session_id = request.cookies[SESSION_ID]
        secret = request.cookies[SESSION_SECRET]
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
        session.secret.verify(secret)
    except VerifyMismatchError:
        raise NotLoggedIn() from None

    return session


def for_user(user: User) -> tuple[Session, str]:
    """Opens a new session for the given user."""

    session = Session(user=user, secret=(secret := genpw()))
    return (session, secret)


def set_cookie(response: Response, *args, **kwargs):
    """A workaround for explicitly setting SameSite to None
    Until the following fix is released:
    https://github.com/pallets/werkzeug/issues/1549
    """

    cookie = dump_cookie(*args, **kwargs)

    if 'samesite' in kwargs and kwargs['samesite'] is None:
        cookie = f'{cookie}; SameSite=None'

    response.headers.add('Set-Cookie', cookie)


def set_session_cookies(response: Response, session: Session,
                        secret: str = None) -> Response:
    """Sets the session cookie."""

    if secret is None:
        session.secret = secret = genpw()
        session.save()

    for domain in CONFIG.get('auth', 'domains').split():
        set_cookie(
            response, SESSION_ID, str(session.id),
            expires=session.end, domain=domain, secure=True, samesite=None)
        set_cookie(
            response, SESSION_SECRET, secret,
            expires=session.end, domain=domain, secure=True, samesite=None)

    return response


def delete_session_cookies(response: Response) -> Response:
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
        return delete_session_cookies(response)

    return set_session_cookies(response, session)
