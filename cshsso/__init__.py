"""Single Sign-On framework for the Corps."""

from cshsso.application import Application
from cshsso.decorators import authenticated, authorized, Authorization
from cshsso.init import init
from cshsso.localproxies import SESSION, USER
from cshsso.orm import User
from cshsso.wsgi import APPLICATION


__all__ = [
    'APPLICATION',
    'SESSION',
    'USER',
    'Application',
    'Authorization',
    'User',
    'authenticated',
    'authorized',
    'init'
]
