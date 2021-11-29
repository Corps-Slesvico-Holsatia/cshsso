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

    def __init__(self, verified: bool, locked: bool,
                 failed_logins_exceeded: bool):
        super().__init__(verified, locked)
        self.verified = verified
        self.locked = locked
        self.failed_logins_exceeded = failed_logins_exceeded


class NotAuthorized(Exception):
    """Indicates that the user is not authorized to perform a request."""

    def __init__(self, target: str):
        super().__init__(target)
        self.target = target


class NotLoggedIn(Exception):
    """Indicates that the user is not logged in."""
