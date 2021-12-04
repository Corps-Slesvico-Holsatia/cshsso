"""Single Sign-On framework for the Corps."""

from cshsso.application import Application
from cshsso.decorators import admin, authenticated, Authorization
from cshsso.localproxies import SESSION, USER
from cshsso.mailinglist import get_emails
from cshsso.orm import User
from cshsso.roles import Circle, Commission, CommissionGroup, Status
from cshsso.semester import Semester
from cshsso.wsgi import APPLICATION


__all__ = [
    'APPLICATION',
    'SESSION',
    'USER',
    'Application',
    'Authorization',
    'Circle',
    'Commission',
    'CommissionGroup',
    'Semester',
    'Status',
    'User',
    'admin',
    'authenticated',
    'get_emails'
]
