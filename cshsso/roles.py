"""User roles."""

from enum import Enum
from typing import NamedTuple, Optional


__all__ = ['MemberType', 'Member', 'Guest', 'Group']


class MemberType(NamedTuple):
    """Role names."""

    name: str
    abbreviation: Optional[str] = None

    def __str__(self):
        return self.abbreviation or self.name


class Member(Enum):
    """Member roles."""

    EB = MemberType('Ehrenbursche', 'EB')
    CB = MemberType('Corpsbursche', 'CB')
    IACB = MemberType('inaktiver Corpsbursche', 'iaCB')
    IACBOB = MemberType('inaktiver Corpsbursche ohne Band', 'iaCBoB')
    AH = MemberType('Alter Herr', 'AH')
    BBZ = MemberType('Burschenbierzipfler', 'BBZ')
    F = MemberType('Fuchs', 'F')
    FCK = MemberType('Fuchsenconkneipant', 'FCK')


class Guest(Enum):
    """Gues roles."""

    SPEF = MemberType('Spefuchs', 'Spef.')
    CS = MemberType('Corpsschwester')
    FDC = MemberType('Freund des Corps', 'FdC')
    VG = MemberType('Verkehrsgast', 'VG')


class Group(Enum):
    """Corps groups."""

    INNER = frozenset({Member.EB, Member.CB, Member.IACB, Member.AH})
    OUTER = frozenset({Member.IACBOB, Member.BBZ, Member.F, Member.FCK})
    GUEST = frozenset({Guest.SPEF, Guest.CS, Guest.FDC, Guest.VG})
