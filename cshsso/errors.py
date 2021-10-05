"""Common error handlers."""

from flask import jsonify
from recaptcha import VerificationError

from cshsso.orm import User, Session


__all__ = ['ERRORS']


ERRORS = {
    User.DoesNotExist: lambda _: ('No such user.', 404),
    Session.DoesNotExist: lambda _: ('No such session.', 404),
    VerificationError: lambda error: (jsonify(error.json), 400)
}
