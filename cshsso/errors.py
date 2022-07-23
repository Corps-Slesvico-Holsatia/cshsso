"""Common error handlers."""

from flask import jsonify
from recaptcha import VerificationError

from wsgilib import JSONMessage

from cshsso.exceptions import InvalidPassword
from cshsso.exceptions import NotAuthenticated
from cshsso.exceptions import NotAuthorized
from cshsso.exceptions import NotLoggedIn
from cshsso.orm.models import User, Session


__all__ = ['ERRORS']


ERRORS = {
    InvalidPassword: lambda _: ('Invalid password.', 400),
    NotAuthenticated: lambda error: JSONMessage(
        'Not authenticated.', verified=error.verified, locked=error.locked,
        failed_logins_exceeded=error.failed_logins_exceeded, status=401
    ),
    NotAuthorized: lambda error: JSONMessage(
        'Not authorized.', target=error.target, status=403
    ),
    NotLoggedIn: lambda _: ('Not logged in.', 401),
    Session.DoesNotExist: lambda _: ('No such session.', 404),
    User.DoesNotExist: lambda _: ('No such user.', 404),
    VerificationError: lambda error: (jsonify(error.json), 400)
}
