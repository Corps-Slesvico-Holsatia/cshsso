"""User roles."""

from enum import Enum
from typing import NamedTuple, Optional


__all__ = ['RoleType', 'Status', 'Circle', 'Commission', 'CommissionGroup']


class RoleType(NamedTuple):
    """Status names."""

    name: str
    abbreviation: Optional[str] = None

    def __str__(self):
        return self.abbreviation or self.name


class Status(Enum):
    """Member status."""

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
    VG = RoleType('Verkehrsgast', 'VG')
    CS = RoleType('Corpsschwester')
    FDC = RoleType('Freund des Corps', 'FdC')


class Circle(Enum):
    """Corps circles."""

    INNER = frozenset({Status.EB, Status.CB, Status.IACB, Status.AH})
    OUTER = frozenset({Status.IACBOB, Status.BBZ, Status.F, Status.FCK})
    GUESTS = frozenset({Status.SPEF, Status.CS, Status.FDC, Status.VG})


class Commission(Enum):
    """Commission types."""

    # Chargen
    SENIOR = RoleType('Senior', 'xxx')
    CONSENIOR = RoleType('Consenior', 'xx')
    SUBSENIOR = RoleType('Subsenior', 'x')
    FUCHSMAJOR = RoleType('Fuchsmajor', 'FM')
    # Ämter
    KW = RoleType('CC-Kassenwart', 'KW')
    HW = RoleType('Hauswart', 'HW')
    GW = RoleType('Getränkewart')
    KEILWART = RoleType('Keilwart')
    EDV = RoleType('EDV-Wart')
    # AHV
    AHV = RoleType('Altherrenvorstandsvorsitzender', 'AHV')
    AHV_STELLV = RoleType('stellvertretender Altherrenvorstandsvorsitzender',
                          'stellv. AHV')
    AHKW = RoleType('Altherren-Kassenwart', 'AHKW')


class CommissionGroup(Enum):
    """Commission groups."""

    CHARGES = frozenset({Commission.SENIOR, Commission.CONSENIOR,
                        Commission.SENIOR, Commission.FUCHSMAJOR})
    COMMISSIONS = frozenset({Commission.KW, Commission.HW, Commission.GW,
                            Commission.KEILWART, Commission.EDV})
    AHV = frozenset({Commission.AHV, Commission.AHV_STELLV,
                    Commission.AHKW})
