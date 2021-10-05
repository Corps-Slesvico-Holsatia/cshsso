"""Object-relational mappings."""

from __future__ import annotations

from peewee import CharField, DateTimeField, ForeignKeyField, MySQLDatabase

from peeweeplus import Argon2Field, EnumField, JSONModel

from cshsso.roles import Role


__all__ = ['User', 'Session']


DATABASE = MySQLDatabase('cshsso')


class CSHSSOModel(JSONModel):   # pylint: disable=R0903
    """Base model for the CSH-SSO database."""

    class Meta:     # pylint: disable=C0115,R0903
        database = DATABASE
        schema = database.database


class User(CSHSSOModel):     # pylint: disable=R0903
    """A user account."""

    name = CharField()
    email = CharField()
    password = Argon2Field()
    first_name = CharField()
    last_name = CharField()
    role = EnumField(Role, use_name=True)


class Session(CSHSSOModel):     # pylint: disable=R0903
    """A user session."""

    user = ForeignKeyField(User, column_name='account', on_delete='CASCADE')
    deadline = DateTimeField()
    password = Argon2Field()
