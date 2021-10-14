"""Authorization checks."""

from typing import Union

from cshsso.convents import Convent, ConventAuthorization
from cshsso.orm import User
from cshsso.roles import Circle, Commission, CommissionGroup, Status


__all__ = ['check_minimum_circle', 'check_commission_group', 'check_target']


AuthorizationTarget = Union[Circle, CommissionGroup, ConventAuthorization]


def is_in_inner_circle(user: User) -> bool:
    """Checks whether the user is member of the inner circle."""

    return user.status in Circle.INNER


def is_in_outer_circle(user: User) -> bool:
    """Checks whether the user is member of the outer circle."""

    return user.status in Circle.OUTER


def check_minimum_circle(user: User, circle: Circle) -> bool:
    """Determines whether the user is authorized for the given circle."""

    if circle is Circle.INNER:
        return user.status in Circle.INNER

    if circle is Circle.OUTER:
        return user.status in {*Circle.INNER, *Circle.OUTER}

    if circle is Circle.GUESTS:
        return user.status in {*Circle.INNER, *Circle.OUTER, *Circle.GUESTS}

    raise NotImplementedError(f'Handling of circle {circle} not implemented.')


def check_commission_group(user: User, group: CommissionGroup) -> bool:
    """Checks whether the user is authorized for the given commission group."""

    return any(uc.commission in group for uc in user.commissions)


def can_sit_ahc(user: User) -> bool:
    """Determines whether the user can sit on the AHC."""

    return user.status in {Status.AH, Status.BBZ} or any(
        uc.commission is Commission.SENIOR for uc in user.commissions
    )


def check_ahc(user: User, vote: bool) -> bool:
    """Checks authorization for the AHC."""

    return user.status is Status.AH if vote else can_sit_ahc(user)


def can_vote_cc(user: User) -> bool:
    """Determines whether the user can vote on the CC."""

    return user.status is Status.CB or any(
        uc.commission in CommissionGroup.AHV for uc in user.commissions
    )


def check_cc(user: User, vote: bool) -> bool:
    """Checks authorization for the CC."""

    return can_vote_cc(user) if vote else user.status in Circle.INNER


def can_vote_fc(user: User) -> bool:
    """Determines whether the user can vote on the FC."""

    return user.status is Status.F or any(
        uc.commission is Commission.FM for uc in user.commissions
    )


def check_fc(user: User, vote: bool) -> bool:
    """Checks authorization for the FC."""

    if vote:
        return can_vote_fc(user)

    return user.status in {*Circle.INNER, *Circle.OUTER}


def check_convent(user: User, convent: ConventAuthorization) -> bool:
    """Checks whether the user is authorized for the given convent."""

    if convent.convent is Convent.AHC:
        return check_ahc(user, convent.vote)

    if convent.convent is Convent.FCC:
        return user.status in Circle.INNER

    if convent.convent is Convent.CC:
        return check_cc(user, convent.vote)

    if convent.convent is Convent.FC:
        return check_fc(user, convent.vote)

    raise NotImplementedError(f'Convent {convent.convent} is not implemented.')


def check_target(user: User, target: AuthorizationTarget) -> bool:
    """Checks a user against a Corps circle or commission group."""

    if isinstance(target, Circle):
        return check_minimum_circle(user, target)

    if isinstance(target, CommissionGroup):
        return check_commission_group(user, target)

    if isinstance(target, ConventAuthorization):
        return check_convent(user, target)

    raise TypeError('Must specify either Circle or CommissionGroup.')
