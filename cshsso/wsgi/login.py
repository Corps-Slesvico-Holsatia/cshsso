"""User login."""

from typing import Union

from flask import request, Response, make_response

from wsgilib import JSONMessage

from cshsso.orm.models import User
from cshsso.session import for_user, set_session_cookies


__all__ = ['login']


INVALID_USER_NAME_OR_PASSWORD = JSONMessage(
    'Invalid user name or password.', status=403
)


def login() -> Union[JSONMessage, Response]:
    """Logs in a user.
    POST: application/json
    {
        "email": <email_address>,
        "passwd": <password>
    }
    """

    if not (email := request.json.get('email')):
        return JSONMessage('No email address provided.', status=400)

    if not (passwd := request.json.get('passwd')):
        return JSONMessage('No password provided.', status=400)

    try:
        user = User.get(User.email == email)
    except User.DoesNotExist:
        return INVALID_USER_NAME_OR_PASSWORD

    if user.disabled:
        return INVALID_USER_NAME_OR_PASSWORD

    if not user.login(passwd):
        return INVALID_USER_NAME_OR_PASSWORD

    session, secret = for_user(user)
    session.save()
    return set_session_cookies(
        make_response(JSONMessage('Login successful.', status=200)),
        session,
        secret=secret
    )
