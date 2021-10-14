"""Single Sign-On framework for the Corps."""

from cshsso.application import Application
from cshsso.decorators import admin, authenticated, Authorization
from cshsso.init import init
from cshsso.localproxies import SESSION, USER
from cshsso.orm import User
from cshsso.semester import Semester
from cshsso.wsgi import APPLICATION


__all__ = [
    'APPLICATION',
    'SESSION',
    'USER',
    'Application',
    'Authorization',
    'Semester',
    'User',
    'admin',
    'authenticated',
    'init'
]
