"""Object-relational mappings."""

from __future__ import annotations
from datetime import datetime

from argon2.exceptions import VerifyMismatchError
from peewee import CharField, DateTimeField, ForeignKeyField, IntegerField

from peeweeplus import Argon2Field, EnumField, JSONModel, MySQLDatabase

from cshsso.functions import genpw
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

    @classmethod
    def open(cls, user: User, deadline: datetime) -> tuple[Session, str]:
        """Opens a new session for the given user."""
        session = cls(user=user, deadline=deadline, passwd=(passwd := genpw()))
        return (session, passwd)

    @classmethod
    def for_user(cls, user: User, deadline: datetime) -> tuple[Session, str]:
        """Returns a session and a session password for the given user."""
        sessions = set()

        for session in cls.select().where(cls.user == user):
            if session.active:
                sessions.add(session)
            else:
                session.delete_instance()

        try:
            *old, last = sessions
        except ValueError:
            return cls.open_session(user=user, deadline=deadline)

        for session in old:
            session.delete_instance()

        return (last, last.renew(deadline))

    def renew(self, deadline: datetime) -> str:
        """Renews the session."""
        self.deadline = deadline
        self.passwd = passwd = genpw()
        return passwd


class UserCharge(CSHSSOModel):  # pylint: disable=R0903
    """Charges."""

    occupant = ForeignKeyField(User, column_name='occupant', backref='charges',
                               on_delete='CASCADE')
    charge = EnumField(Charge, use_name=True, unique=True)
