"""User login."""

from flask import request, Response, make_response

from cshsso.orm import User
from cshsso.session import set_cookies


__all__ = ['login']


def login() -> Response:
    """Logs in a user."""

    if not (email := request.json.get('email')):
        return ('No email address provided.', 400)

    if not (passwd := request.json.get('passwd')):
        return ('No password provided.', 400)

    try:
        user = User.get(User.email == email)
    except User.DoesNotExist:
        return ('Invalid user name or password.', 400)

    try:
        user.passwd.verify(passwd)
    except VerificationError:
        return ('Invalid user name or password.', 400)

    session = Session(user=user, deadline=get_deadline(),
                      password=(password := genpw()))
    session.save()
    return set_cookies(make_response(('Login successful.', 200)))
