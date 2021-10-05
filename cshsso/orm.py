"""Object-relational mappings."""

from __future__ import annotations

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
    password = Argon2Field()
    first_name = CharField()
    last_name = CharField()
    role = EnumField(Role, use_name=True)
    failed_logins = IntegerField(default=0)


class Session(CSHSSOModel):     # pylint: disable=R0903
    """A user session."""

    user = ForeignKeyField(User, column_name='user', on_delete='CASCADE')
    deadline = DateTimeField()
    password = Argon2Field()

    @property
    def charged(self) -> bool:
        """Determines whether the user is charged."""
        return self.charges.count() > 0


class UserCharge(CSHSSOModel):  # pylint: disable=R0903
    """Charges."""

    occupant = ForeignKeyField(User, column_name='occupant', backref='charges',
                               on_delete='CASCADE')
    charge = EnumField(Charge, use_name=True, unique=True)
