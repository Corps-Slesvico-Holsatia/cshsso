"""User roles."""

from enum import Enum
from typing import NamedTuple, Optional


__all__ = ['RoleType', 'Role', 'Charge', 'Group']


class RoleType(NamedTuple):
    """Role names."""

    name: str
    abbreviation: Optional[str] = None

    def __str__(self):
        return self.abbreviation or self.name


class Role(Enum):
    """Role roles."""

    # Members
    EB = RoleType('Ehrenbursche', 'EB')
    CB = RoleType('Corpsbursche', 'CB')
    IACB = RoleType('inaktiver Corpsbursche', 'iaCB')
    IACBOB = RoleType('inaktiver Corpsbursche ohne Band', 'iaCBoB')
    AH = RoleType('Alter Herr', 'AH')
    BBZ = RoleType('Burschenbierzipfler', 'BBZ')
    F = RoleType('Fuchs', 'F')
    FCK = RoleType('Fuchsenconkneipant', 'FCK')
    # Guests
    SPEF = RoleType('Spefuchs', 'Spef.')
    CS = RoleType('Corpsschwester')
    FDC = RoleType('Freund des Corps', 'FdC')
    VG = RoleType('Verkehrsgast', 'VG')


class Charge(Enum):
    """Charges."""

    SENIOR = RoleType('Senior', 'xxx')
    CONSENIOR = RoleType('Consenior', 'xx')
    SUBSENIOR = RoleType('Subsenior', 'x')
    FUCHSMAJOR = RoleType('Fuchsmajor', 'FM')


class Group(Enum):
    """Corps groups."""

    INNER = frozenset({Role.EB, Role.CB, Role.IACB, Role.AH})
    OUTER = frozenset({Role.IACBOB, Role.BBZ, Role.F, Role.FCK})
    GUEST = frozenset({Role.SPEF, Role.CS, Role.FDC, Role.VG})
    CHARGES = frozenset(Charge)
