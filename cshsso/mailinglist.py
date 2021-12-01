"""Maling list creation."""

from functools import partial
from typing import Iterator, Union

from peewee import Expression, ModelSelect

from cshsso.orm import User, UserCommission
from cshsso.roles import Status, Circle, Commission, CommissionGroup


__all__ = ['get_users', 'get_emails']


Target = Union[Status, Circle, Commission, CommissionGroup, User, int]


def get_condition(*targets: Target) -> Expression:
    """Returns a select expression."""

    status = {status for status in targets if isinstance(status, Status)}

    for circle in filter(partial(isinstance, class_or_tuple=Circle), targets):
        status |= set(circle)

    commissions = {comm for comm in targets if isinstance(comm, Commission)}

    for cgroup in filter(partial(isinstance, class_or_tuple=CommissionGroup),
                         targets):
        commissions |= set(cgroup)

    user_ids = {user.id for user in targets if isinstance(user, User)}
    user_ids |= {user_id for user_id in targets if isinstance(user_id, int)}
    condition = False

    if status:
        condition |= User.status << status

    if commissions:
        condition |= UserCommission.commission << commissions

    if user_ids:
        condition |= User.id << user_ids

    return condition


def get_users(*targets: Target) -> ModelSelect:
    """Yields email addresses."""

    return User.select(User, UserCommission).join(UserCommission).where(
        get_condition(targets))


def get_emails(*targets: Target) -> Iterator[str]:
    """Yields email addresses for the given targets."""

    for user in get_users(*targets):
        yield user.email
