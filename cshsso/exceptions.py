"""Common exceptions."""


__all__ = ['NotLoggedIn', 'NotAuthorized']


class NotLoggedIn(Exception):
    """Indicates that the user is not logged in."""


class NotAuthorized(Exception):
    """Indicates that the user is not authorized to perform a request."""
