"""Common error handlers."""

from cshsso.orm import User, Session


__all__ = ['ERRORS']


ERRORS = {
    User.DoesNotExist: lambda _: ('No such user.', 404),
    Session.DoesNotExist: lambda _: ('No such session.', 404)
}
