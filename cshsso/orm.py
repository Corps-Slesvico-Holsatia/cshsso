"""Object-relational mappings."""

from __future__ import annotations

from argon2.exceptions import VerifyMismatchError
from peewee import CharField, DateTimeField, ForeignKeyField, IntegerField

from peeweeplus import Argon2Field, EnumField, JSONModel, MySQLDatabase

from cshsso.roles import Role, Charge


__all__ = ['DATABASE', 'User', 'Session', 'UserCharge']


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
    role = EnumField(Role, use_name=True)
    failed_logins = IntegerField(default=0)

    @property
    def charged(self) -> bool:
        """Determines whether the user is charged."""
        return self.charges.count() > 0

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

        return True


class Session(CSHSSOModel):     # pylint: disable=R0903
    """A user session."""

    user = ForeignKeyField(User, column_name='user', on_delete='CASCADE')
    deadline = DateTimeField()
    passwd = Argon2Field()


class UserCharge(CSHSSOModel):  # pylint: disable=R0903
    """Charges."""

    occupant = ForeignKeyField(User, column_name='occupant', backref='charges',
                               on_delete='CASCADE')
    charge = EnumField(Charge, use_name=True, unique=True)
