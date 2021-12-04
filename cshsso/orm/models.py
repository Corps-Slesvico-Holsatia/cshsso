"""Object-relational mappings."""

from __future__ import annotations
from datetime import datetime, timedelta
from uuid import uuid4

from argon2.exceptions import VerifyMismatchError
from peewee import AutoField
from peewee import BooleanField
from peewee import CharField
from peewee import DateField
from peewee import DateTimeField
from peewee import ForeignKeyField
from peewee import IntegerField
from peewee import Model
from peewee import ModelSelect
from peewee import UUIDField

from peeweeplus import Argon2Field, EnumField, MySQLDatabaseProxy

from cshsso.config import CONFIG
from cshsso.constants import PW_RESET_TOKEN_VALIDITY, SESSION_VALIDITY
from cshsso.roles import Status, Commission


__all__ = [
    'DATABASE',
    'MODELS',
    'User',
    'Session',
    'UserCommission',
    'PasswordResetToken'
]


DATABASE = MySQLDatabaseProxy('cshsso')


class CSHSSOModel(Model):   # pylint: disable=R0903
    """Base model for the CSH-SSO database."""

    class Meta:     # pylint: disable=C0115,R0903
        database = DATABASE
        schema = database.database


class User(CSHSSOModel):     # pylint: disable=R0903
    """A user account."""

    id = AutoField()
    email = CharField(unique=True)
    passwd = Argon2Field()
    first_name = CharField()
    last_name = CharField()
    registered = DateTimeField(default=datetime.now)
    verified = BooleanField(default=False)
    locked = BooleanField(default=False)
    failed_logins = IntegerField(default=0)
    admin = BooleanField(default=False)
    # Corps-related information
    status = EnumField(Status, use_name=True)
    name_number = IntegerField(null=True)
    corps_list_number = IntegerField(null=True)
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

    def has_commission(self, commission: Commission) -> ModelSelect:
        """Selects commissions of the given type of the user."""
        return self.user_commissions.where(
            UserCommission.commission == commission)


class Session(CSHSSOModel):     # pylint: disable=R0903
    """A user session."""

    id = AutoField()
    user = ForeignKeyField(User, column_name='user', on_delete='CASCADE',
                           lazy_load=False)
    secret = Argon2Field()
    valid_until = DateTimeField(
        default=lambda: datetime.now() + SESSION_VALIDITY)

    def is_valid(self) -> bool:
        """Checks whether the session is valid."""
        return self.valid_until > datetime.now()

    def extend(self, duration: timedelta = SESSION_VALIDITY) -> Session:
        """Extends the session."""
        self.valid_until = datetime.now() + duration
        self.save()
        return self


class UserCommission(CSHSSOModel):  # pylint: disable=R0903
    """User commissions."""

    class Meta:     # pylint: disable=C0115,R0903
        table_name = 'user_commission'

    id = AutoField()
    occupant = ForeignKeyField(User, column_name='occupant',
                               backref='user_commissions', on_delete='CASCADE',
                               lazy_load=False)
    commission = EnumField(Commission, use_name=True, unique=True)


class PasswordResetToken(CSHSSOModel):  # pylint: disable=R0903
    """A per-user password reset token."""

    class Meta:     # pylint: disable=C0115,R0903
        table_name = 'password_reset_token'

    id = AutoField()
    user = ForeignKeyField(User, column_name='user', on_delete='CASCADE',
                           lazy_load=False)
    token = UUIDField(default=uuid4)
    issued = DateTimeField(default=datetime.now)

    def is_valid(self) -> bool:
        """Determines whether the password reset token is currently valid."""
        return self.issued + PW_RESET_TOKEN_VALIDITY > datetime.now()


MODELS = [User, Session, UserCommission, PasswordResetToken]
