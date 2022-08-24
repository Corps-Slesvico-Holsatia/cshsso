"""Object-relational mappings."""

from __future__ import annotations
from datetime import datetime, timedelta
from uuid import uuid4

from argon2.exceptions import VerifyMismatchError
from peewee import AutoField
from peewee import BooleanField
from peewee import DateField
from peewee import DateTimeField
from peewee import ForeignKeyField
from peewee import IntegerField
from peewee import Model
from peewee import ModelSelect
from peewee import UUIDField

from peeweeplus import Argon2Field
from peeweeplus import EMailField
from peeweeplus import EnumField
from peeweeplus import HTMLTextField
from peeweeplus import MySQLDatabaseProxy
from peeweeplus import UserNameField

from cshsso.config import CONFIG
from cshsso.constants import PW_RESET_TOKEN_VALIDITY
from cshsso.constants import SESSION_VALIDITY
from cshsso.roles import Status, Commission
from cshsso.roman import roman


__all__ = [
    'DATABASE',
    'BaseModel',
    'User',
    'Session',
    'UserCommission',
    'PasswordResetToken'
]


DATABASE = MySQLDatabaseProxy('cshsso')


class BaseModel(Model):
    """Base model for the CSH-SSO database."""

    class Meta:
        database = DATABASE
        schema = database.database


class User(BaseModel):
    """A user account."""

    id = AutoField()
    email = EMailField(unique=True)
    passwd = Argon2Field()
    first_name = UserNameField()
    last_name = UserNameField()
    registered = DateTimeField(default=datetime.now)
    verified = BooleanField(default=False)
    locked = BooleanField(default=False)
    failed_logins = IntegerField(default=0)
    admin = BooleanField(default=False)
    bio = HTMLTextField(null=True)
    # Corps-related information
    status = EnumField(Status, use_name=True)
    name_number = IntegerField(null=True)
    corps_list_number = IntegerField(null=True)
    acception = DateField(null=True)
    reception = DateField(null=True)

    @property
    def failed_logins_exceeded(self) -> bool:
        """Return True if the failed logins are exceeded else False."""
        return self.failed_logins > CONFIG.getint(
            'user', 'max_failed_logins', fallback=3
        )

    @property
    def disabled(self) -> bool:
        """Return True if the user is disabled else False."""
        return not self.verified or self.locked or self.failed_logins_exceeded

    @property
    def commissions(self) -> set[Commission]:
        """Return the user's commissions."""
        return {uc.commission for uc in self.user_commissions}

    @property
    def numbered_last_name(self) -> str:
        """Return the numbered last name, if applicable, else the last name."""
        if not self.name_number:
            return self.last_name

        return f'{self.last_name} {roman(self.name_number)}'

    def login(self, passwd: str) -> bool:
        """Attempt a login."""
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
        """Select user commissions of the given type of this user."""
        return self.user_commissions.where(
            UserCommission.commission == commission
        )


class Session(BaseModel):
    """A user session."""

    id = AutoField()
    user = ForeignKeyField(
        User,
        column_name='user',
        on_delete='CASCADE',
        lazy_load=False
    )
    secret = Argon2Field()
    valid_until = DateTimeField(
        default=lambda: datetime.now() + SESSION_VALIDITY
    )

    def is_valid(self) -> bool:
        """Return True if the session is valid, else False."""
        return self.valid_until > datetime.now()

    def extend(self, duration: timedelta = SESSION_VALIDITY) -> Session:
        """Extend the session by the given duration."""
        self.valid_until = datetime.now() + duration
        self.save()
        return self


class UserCommission(BaseModel):
    """User commissions."""

    class Meta:
        table_name = 'user_commission'

    id = AutoField()
    occupant = ForeignKeyField(
        User,
        column_name='occupant',
        backref='user_commissions', on_delete='CASCADE',
        lazy_load=False
    )
    commission = EnumField(Commission, use_name=True, unique=True)


class PasswordResetToken(BaseModel):
    """A per-user password reset token."""

    class Meta:
        table_name = 'password_reset_token'

    id = AutoField()
    user = ForeignKeyField(
        User,
        column_name='user',
        on_delete='CASCADE',
        lazy_load=False
    )
    token = UUIDField(default=uuid4)
    issued = DateTimeField(default=datetime.now)

    def is_valid(self) -> bool:
        """Return True if the password reset
        token is currently valid, else False.
        """
        return self.issued + PW_RESET_TOKEN_VALIDITY > datetime.now()
