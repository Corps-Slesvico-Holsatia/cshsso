"""Authorization checks."""

from cshsso.convents import Convent, ConventAuth
from cshsso.orm.models import User
from cshsso.roles import Circle, Commission, CommissionGroup, Status


__all__ = [
    'is_in_inner_circle',
    'is_in_outer_circle',
    'is_corps_member',
    'check_circle',
    'check_convent',
    'check_group'
]


INNER_OUTER = {*Circle.INNER, *Circle.OUTER}
INNER_OUTER_GUEST = {*INNER_OUTER, *Circle.GUESTS}


def is_in_inner_circle(user: User) -> bool:
    """Checks whether the user is member of the inner circle."""

    return user.status in Circle.INNER


def is_in_outer_circle(user: User) -> bool:
    """Checks whether the user is member of the outer circle."""

    return user.status in Circle.OUTER


def is_corps_member(user: User) -> bool:
    """Checks whether the user is a member of the corps."""

    return is_in_inner_circle(user) or is_in_outer_circle(user)


def check_circle(user: User, circle: Circle) -> bool:
    """Determines whether the user is authorized for the given circle."""

    if circle is Circle.INNER:
        return user.status in Circle.INNER

    if circle is Circle.OUTER:
        return user.status in INNER_OUTER

    if circle is Circle.GUESTS:
        return user.status in INNER_OUTER_GUEST

    raise NotImplementedError(f'Handling of circle {circle} not implemented.')


def check_group(user: User, group: CommissionGroup) -> bool:
    """Checks whether the user is authorized for the given commission group."""

    return any(commission in group for commission in user.commissions)


def can_sit_ahc(user: User) -> bool:
    """Determines whether the user can sit on the AHC."""

    return (user.status in {Status.AH, Status.EB, Status.BBZ}
            or user.has_commission(Commission.SENIOR))


def can_vote_ahc(user: User) -> bool:
    """Checks whether the user can vote on the AHC."""

    return user.status in {Status.AH, Status.EB}


def check_ahc(user: User, vote: bool) -> bool:
    """Checks authorization for the AHC."""

    return can_vote_ahc(user) if vote else can_sit_ahc(user)


def can_sit_cc(user: User) -> bool:
    """Checks whether the user can sit on the CC."""

    return user.status in Circle.INNER


def can_vote_cc(user: User) -> bool:
    """Determines whether the user can vote on the CC."""

    return user.status in {Status.CB, Status.EB} or check_group(
        user, CommissionGroup.AHV)


def check_cc(user: User, vote: bool) -> bool:
    """Checks authorization for the CC."""

    return can_vote_cc(user) if vote else can_sit_cc(user)


def can_sit_fc(user: User):
    """Checks whether the user can sit on the FC."""

    return user.status in INNER_OUTER


def can_vote_fc(user: User) -> bool:
    """Determines whether the user can vote on the FC."""

    return user.status in {Status.F, Status.EB} or user.has_commission(
        Commission.FM)


def check_fc(user: User, vote: bool) -> bool:
    """Checks authorization for the FC."""

    return can_vote_fc(user) if vote else can_sit_fc(user)


def check_convent(user: User, convent: ConventAuth) -> bool:
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
