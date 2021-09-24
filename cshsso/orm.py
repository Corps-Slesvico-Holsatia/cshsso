"""Object-relational mappings."""

from __future__ import annotations

from peewee import CharField, ForeignKeyField, MySQLDatabase

from peeweeplus import Argon2Field, EnumField, JSONModel

from cshsso.functions import genpw
from cshsso.roles import Role


__all__ = ['Account', 'Session']


DATABASE = MySQLDatabase('cshsso')


class CSHSSOModel(JSONModel):   # pylint: disable=R0903
    """Base model for the CSH-SSO database."""

    class Meta:     # pylint: disable=C0115,R0903
        database = DATABASE
        schema = database.database


class Account(CSHSSOModel):     # pylint: disable=R0903
    """A user account."""

    name = CharField()
    email = CharField()
    password = Argon2Field()
    first_name = CharField()
    last_name = CharField()
    role = EnumField(Role, name=True)


class Session(CSHSSOModel):     # pylint: disable=R0903
    """A user session."""

    account = ForeignKeyField(Account, column_name='account',
                              on_delete='CASCADE')
    password = Argon2Field()

    @classmethod
    def open(cls, account: Account) -> Session:
        """Opens a new session for the given account."""
        return cls(account=account, passwd=genpw())
