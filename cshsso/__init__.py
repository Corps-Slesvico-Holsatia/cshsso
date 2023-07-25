"""Single Sign-On framework for the Corps."""

from cshsso.application import Application
from cshsso.authorization import check_convent
from cshsso.convents import Convent, ConventAuth
from cshsso.decorators import admin, authenticated, Authorization
from cshsso.localproxies import SESSION, USER
from cshsso.mailinglist import get_emails
from cshsso.orm import BaseModel, User
from cshsso.roles import Circle, Commission, CommissionGroup, Status
from cshsso.semester import Semester
from cshsso.wsgi import APPLICATION


__all__ = [
    "APPLICATION",
    "SESSION",
    "USER",
    "check_convent",
    "get_emails",
    "Application",
    "Authorization",
    "BaseModel",
    "Circle",
    "Commission",
    "CommissionGroup",
    "Convent",
    "ConventAuth",
    "Semester",
    "Status",
    "User",
    "admin",
    "authenticated",
]
