"""Single Sign-On framework for the Corps."""

from cshsso.application import Application
from cshsso.convents import Convent
from cshsso.decorators import admin, authenticated, Authorization
from cshsso.localproxies import SESSION, USER
from cshsso.mailinglist import get_emails
from cshsso.orm import BaseModel, User
from cshsso.roles import Circle, Commission, CommissionGroup, Status
from cshsso.semester import Semester
from cshsso.wsgi import APPLICATION


__all__ = [
    'APPLICATION',
    'SESSION',
    'USER',
    'get_emails',
    'Application',
    'Authorization',
    'BaseModel',
    'Circle',
    'Commission',
    'CommissionGroup',
    'Convent',
    'Semester',
    'Status',
    'User',
    'admin',
    'authenticated'
]
