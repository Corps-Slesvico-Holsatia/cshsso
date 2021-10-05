"""Single Sign-On framework for the Corps."""

from cshsso.application import Application
from cshsso.init import init
from cshsso.orm import User
from cshsso.decorators import authenticated, authorized
from cshsso.localproxies import SESSION, USER


__all__ = [
    'SESSION',
    'USER',
    'Application',
    'User',
    'authenticated',
    'authorized',
    'init'
]
