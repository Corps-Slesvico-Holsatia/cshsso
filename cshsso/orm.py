"""Object-relational mappings."""

from __future__ import annotations
from datetime import datetime, timedelta
from uuid import uuid4

from argon2.exceptions import VerifyMismatchError
from peewee import BooleanField
from peewee import CharField
from peewee import DateField
from peewee import DateTimeField
from peewee import ForeignKeyField
from peewee import IntegerField
from peewee import UUIDField

from peeweeplus import Argon2Field, EnumField, JSONModel, MySQLDatabase

from cshsso.config import CONFIG
from cshsso.roles import Status, Commission


__all__ = [
    'DATABASE',
    'User',
    'Session',
    'UserCommission',
    'PasswordResetToken'
]


DATABASE = MySQLDatabase('cshsso')


class CSHSSOModel(JSONModel):   # pylint: disable=R0903
    """Base model for the CSH-SSO database."""

    class Meta:     # pylint: disable=C0115,R0903
        database = DATABASE
        schema = database.database


class User(CSHSSOModel):     # pylint: disable=R0903
    """A user account."""

    email = CharField(unique=True)
    passwd = Argon2Field()
    first_name = CharField()
    last_name = CharField()
    status = EnumField(Status, use_name=True)
    registered = DateTimeField(default=datetime.now)
    verified = BooleanField(default=False)
    locked = BooleanField(default=False)
    failed_logins = IntegerField(default=0)
    admin = BooleanField(default=False)
    acception = DateField(null=True)
    reception = DateField(null=True)

    @property
    def failed_logins_exceeded(self) -> bool:
        """Checks whether the failed logins are exceeded."""
        return self.failed_logins > CONFIG.getint(
            'user', 'max_failed_logins', fallback=3)

    @property
    def disabled(self) -> bool:
        """Determines whether the user is diabled."""
        return not self.verified or self.locked or self.failed_logins_exceeded

    @property
    def commissions(self) -> set[Commission]:
        """Returns the user's commissions."""
        return {uc.commission for uc in self.user_commissions}

    def login(self, passwd: str) -> bool:
        """Attempts a login."""
        try:
            self.passwd.verify(passwd)
        except VerifyMismatchError:
            self.failed_logins += 1
            self.save()
            return False

        if self.passwd.needs_rehash:
            self.passwd = passwd

        self.failed_logins = 0
        self.save()
        return True

    def to_json(self, *args, **kwargs) -> dict:
        """Returns a JSON-ish dict of core information."""
        json = super().to_json(*args, **kwargs)
        json['commissions'] = [c.to_json() for c in self.commissions]
        return json


class Session(CSHSSOModel):     # pylint: disable=R0903
    """A user session."""

    user = ForeignKeyField(User, column_name='user', on_delete='CASCADE')
    secret = Argon2Field()


class UserCommission(CSHSSOModel):  # pylint: disable=R0903
    """User commissions."""

    occupant = ForeignKeyField(User, column_name='occupant',
                               backref='user_commissions', on_delete='CASCADE')
    commission = EnumField(Commission, use_name=True, unique=True)


class PasswordResetToken(CSHSSOModel):
    """A per-user password reset token."""

    VALIDITY = timedelta(days=1)

    user = ForeignKeyField(User, column_name='user', on_delete='CASCADE')
    token = UUIDField(default=uuid4)
    issued = DateTimeField(default=datetime.now)

    def is_valid(self) -> bool:
        """Determines whether the password reset token is currently valid."""
        return self.issued + self.VALIDITY > datetime.now()
