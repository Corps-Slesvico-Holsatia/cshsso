"""Common error handlers."""

from cshsso.orm import Account, Session


__all__ = ['ERRORS']


ERRORS = {
    Account.DoesNotExist: lambda _: ('No such account.', 404),
    Session.DoesNotExist: lambda _: ('No such session.', 404)
}
