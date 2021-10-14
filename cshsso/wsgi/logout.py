"""Handle logouts."""

from typing import Union

from flask import request, Response, jsonify, make_response

from cshsso.decorators import authenticated
from cshsso.localproxies import USER, SESSION
from cshsso.orm import User, Session
from cshsso.session import delete_session_cookies


__all__ = ['logout']


def terminate_all_sessions(user: Union[User, int]) -> Response:
    """Terminates all sessions of the given user."""

    sessions = []

    for session in Session.select().where(Session.user == user):
        sessions.append(session.id)
        session.delete_instance()

    return delete_session_cookies(make_response(jsonify(sessions)))


def terminate_session(session: Session) -> Response:
    """Terminates the given session."""

    session.delete_instance()
    return delete_session_cookies(make_response(jsonify([session.id])))


@authenticated
def logout() -> Response:
    """Terminate sessions for the current user."""

    if request.json.get('all', False):
        return terminate_all_sessions(USER.id)

    return terminate_session(SESSION)
