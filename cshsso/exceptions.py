"""Common exceptions."""


__all__ = [
    'InvalidPassword',
    'NotAuthenticated',
    'NotAuthorized',
    'NotLoggedIn'
]


class InvalidPassword(Exception):
    """Indicates an invalid password."""


class NotAuthenticated(Exception):
    """Indicates that the user is not authenticated."""


class NotAuthorized(Exception):
    """Indicates that the user is not authorized to perform a request."""


class NotLoggedIn(Exception):
    """Indicates that the user is not logged in."""
