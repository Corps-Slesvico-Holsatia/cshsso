"""User roles."""

from enum import Enum
from typing import Iterator, NamedTuple, Optional


__all__ = ['RoleType', 'Status', 'Circle', 'Commission', 'CommissionGroup']


class RoleType(NamedTuple):
    """Status names."""

    name: str
    abbreviation: Optional[str] = None

    def __str__(self):
        return self.abbreviation or self.name

    def to_json(self) -> dict:
        """Returns a JSON-ish dict."""
        return {'name': self.name, 'abbreviation': self.abbreviation}


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

    def to_json(self) -> dict:
        """Returns a JSON-ish dict."""
        return self.value.to_json()


class Circle(Enum):
    """Corps circles."""

    INNER = {Status.EB, Status.CB, Status.IACB, Status.AH}
    OUTER = {Status.IACBOB, Status.BBZ, Status.F, Status.FCK}
    GUESTS = {Status.SPEF, Status.CS, Status.FDC, Status.VG}

    def __contains__(self, value: Status) -> bool:
        return value in self.value

    def __iter__(self) -> Iterator[Status]:
        return iter(self.value)


class Commission(Enum):
    """Commission types."""

    # Chargen
    SENIOR = RoleType('Senior', 'xxx')
    CONSENIOR = RoleType('Consenior', 'xx')
    SUBSENIOR = RoleType('Subsenior', 'x')
    FM = RoleType('Fuchsmajor', 'FM')
    # Ämter
    KW = RoleType('CC-Kassenwart', 'KW')
    HW = RoleType('Hauswart', 'HW')
    GW = RoleType('Getränkewart', 'GW')
    KEILWART = RoleType('Keilwart')
    EDV = RoleType('EDV-Wart')
    # AHV
    AHV = RoleType('Altherrenvorstandsvorsitzender', 'AHV')
    AHV_STELLV = RoleType('stellvertretender Altherrenvorstandsvorsitzender',
                          'stellv. AHV')
    AHKW = RoleType('Altherren-Kassenwart', 'AHKW')

    def to_json(self) -> dict:
        """Returns a JSON-ish dict."""
        return self.value.to_json()


class CommissionGroup(Enum):
    """Commission groups."""

    CHARGES = {Commission.SENIOR, Commission.CONSENIOR, Commission.SUBSENIOR,
               Commission.FUCHSMAJOR}
    COMMISSIONS = {Commission.KW, Commission.HW, Commission.GW,
                   Commission.KEILWART, Commission.EDV}
    AHV = {Commission.AHV, Commission.AHV_STELLV, Commission.AHKW}

    def __contains__(self, value: Commission) -> bool:
        return value in self.value

    def __iter__(self) -> Iterator[Status]:
        return iter(self.value)
