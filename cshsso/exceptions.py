"""Common exceptions."""


__all__ = ['InvalidPassword', 'NotLoggedIn', 'NotAuthorized']


class InvalidPassword(Exception):
    """Indicates an invalid password."""


class NotLoggedIn(Exception):
    """Indicates that the user is not logged in."""


class NotAuthorized(Exception):
    """Indicates that the user is not authorized to perform a request."""
